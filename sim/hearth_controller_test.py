"""Synthetic test of the Granary release controller and the Hearth-lighting auction.

No market data: bull/bear cycles, gas regimes and burn noise are synthetic. Protocol
rules (DXN emission decay, 2% stake yield, AMP floor date) are exact. All burn
quantities are in units of "today's normal market batches per cycle" (= 1.0).

Scenarios
  none      no Granary
  fixed     fixed annuity after the floor, Granary pays fees from an escrow assumed
            always sufficient, releases every day (old design)
  bots      new controller, auction won by bots at break-even
  tribes    new controller, tribes value the Keeper title and light earlier
  cartel    new controller, only tribes may light and they collude to wait
  open      cartel tries the same but anyone (Outlaws, bots) may light
Run:  python hearth_controller_test.py
"""
import json, numpy as np

RUNS, SEED = 120, 11
DAY0 = np.datetime64("2027-03-16")          # earliest NXN launch
FLOOR = np.datetime64("2030-12-24")         # AMP = 1
T_END_YEARS = 8                              # drawdown horizon after the floor
END = np.datetime64("2040-06-30")
D = int((END - DAY0).astype(int)); D_FLOOR = int((FLOOR - DAY0).astype(int))
D_TEND = D_FLOOR + 365 * T_END_YEARS
N0, R0 = 1150, 10000 * 1.002 ** -1150        # active cycles so far, today's reward

SIG_MIN, SIG_MAX, MARGIN = 0.10, 1.00, 0.02  # auction range, bot margin
GAP_FILL, CYC_CAP = 0.5, 3.0                 # fill half the gap; cyclical <= 3x annuity
CARRY = 7                                    # allowance carries at most 7 cycles


def ema(prev, x, n):
    return prev + (x - prev) / n


def synth(rng, xscale=0.6):
    """Draw one synthetic world: cycle c(t), fee share rho(t), premium kappa(t), noise."""
    t = np.arange(D) / 365.0
    P = rng.uniform(2.5, 4.5); A = rng.uniform(0.5, 1.0); ph = rng.uniform(0, 2 * np.pi)
    ar = np.zeros(D); e = rng.normal(0, 0.03, D)
    for i in range(1, D):
        ar[i] = 0.985 * ar[i - 1] + e[i]
    c = A * np.sin(2 * np.pi * t / P + ph) + ar                  # log activity cycle
    gas = np.exp(0.6 * c + np.cumsum(rng.normal(0, 0.02, D)))    # gas higher in bulls
    xcost = xscale * np.exp(0.8 * c)                             # XEN cost per batch (vs gas fee)
    rho = gas / (gas + xcost)                                    # fee share of a burner's cost
    kappa = np.exp(0.4 * c)                                      # speculative premium
    noise = np.exp(rng.normal(0, 0.35, D))
    u = rng.uniform(size=D)
    eps = rng.uniform(0.5, 1.0)
    prestige = rng.uniform(0.05, 0.20)                           # Keeper title value, share of lot
    return c, rho, kappa, noise, u, eps, prestige, gas


def run(world, scen, deposit_share=0.15, diversion=0.5):
    c, rho, kappa, noise, u, eps, prestige, gas = world
    n = N0; G = 0.0; principal = 0.0; Y = 0.0; pend = 0.0; E = 0.0
    S = L = 1.0
    out = {k: np.zeros(D) for k in ("mkt", "tot", "rel", "G", "L", "kept", "sig", "w")}
    stall = 0; active = 0; min_margin = np.inf
    for d in range(D):
        R = 10000 * 1.002 ** -n
        Bs = (R / R0) ** eps
        Bexp = Bs * np.exp(c[d])                                  # equilibrium burns
        V = kappa[d] * Bexp                                       # DXN value per cycle (cost units)
        B = Bexp * noise[d]
        if u[d] < 0.15 * np.exp(-3 * B):                          # quiet cycle
            B = 0.0
        # deposits (before the floor): half burned at once, half stored; part diverted
        dep = 0.0
        if scen != "none" and d < D_FLOOR:
            dep = deposit_share * B
            B = B - diversion * dep
            G += dep / 2; principal += dep / 2
            E += 1.2 * gas[d] * dep / 2          # energy fee to escrow (1.2x fee at today's gas)
        burn_now = dep / 2 if scen != "none" else 0.0
        # stake yield on the store
        y = G * 0.02 / 365; G += y; Y += y
        x = B / (R / R0)                       # batches per unit of DXN emission (detrended activity)
        S, L = ema(S, x, 7), ema(L, x, 180)
        rel = 0.0
        if scen == "escrow":                 # fixed rule paid from a real, finite escrow
            if d >= D_FLOOR and G > 0:
                ramp = min(1.0, (d - D_FLOOR + 1) / 90)
                pend = min(pend + ramp * G / max(1, D_TEND - d), G)
                rel = min(pend, E / gas[d]); E -= rel * gas[d]; pend -= rel; G -= rel
                if rel > 0: out["kept"][d] = 1.0
                elif pend > 0: stall += 1
        elif scen == "fixed":
            if d >= D_FLOOR and G > 0:
                ramp = min(1.0, (d - D_FLOOR + 1) / 90)
                rel = min(G, ramp * G / max(1, D_TEND - d))
                G -= rel
                out["kept"][d] = 1.0
        elif scen != "none":
            gap = GAP_FILL * max(0.0, L - S) * (R / R0)   # back to batches
            if d < D_FLOOR:
                alloc = min(gap, Y); Y -= alloc
            else:
                rs = G / max(1, D_TEND - d) * min(1.0, (d - D_FLOOR + 1) / 90)
                alloc = rs + min(gap, CYC_CAP * rs)
            pend = min(pend + alloc, CARRY * max(alloc, 1e-12), G)
            can = (B > 0) or (scen == "anyday")
            if can and pend > 0:
                # sell the allowance in up to 3 lots; a lot sells if its break-even share <= 1
                lot = pend / 3; sold = 0.0; kept_w = 0.0
                for _ in range(3):
                    sig_bot = rho[d] * (B + rel + lot) / V + MARGIN       # fee / value of lot's DXN
                    if sig_bot > SIG_MAX:
                        break
                    sig_bot = max(SIG_MIN, sig_bot)
                    if scen in ("bots", "open", "anyday", "hybrid"):
                        sig = sig_bot
                    elif scen == "tribes":
                        sig = max(SIG_MIN, sig_bot - prestige)
                    elif scen == "cartel":
                        sig = max(sig_bot, 0.9)
                    rel += lot; kept_w += (1 - sig) * lot
                if scen == "hybrid" and rel < pend and E > 0:   # escrow pays what the auction leaves
                    extra = min(pend - rel, E / gas[d]); E -= extra * gas[d]
                    kept_w += extra; rel += extra
                pend -= rel; G -= rel
                if rel > 0:
                    out["kept"][d] = kept_w / rel
                else:
                    stall += 1
            elif pend > 0:
                stall += 1
        tot = B + burn_now + rel
        if tot > 0:
            n += 1; active += 1
        if d < D_FLOOR and scen != "none":
            min_margin = min(min_margin, G - principal)
        out["mkt"][d], out["tot"][d], out["rel"][d], out["G"][d], out["L"][d] = B, tot, rel, G, L * (R / R0)
        out["w"][d] = np.clip(np.log(max(S, 1e-9) / max(L, 1e-9)), -1, 1)
    out.update(stall=stall, active=active, min_margin=min_margin, principal=principal)
    return out


def metrics(o):
    pre, post = slice(0, D_FLOOR), slice(D_FLOOR, D_TEND)
    tot, L = o["tot"], o["L"]
    cold = lambda s: float(np.mean(m30[s] < 0.5 * L[s]))
    k = np.convolve(tot[post], np.ones(90) / 90, mode="valid")
    rel_days = o["rel"] > 0
    m30 = np.convolve(tot, np.ones(30) / 30, mode="same")
    lt = np.log(np.maximum(tot[post], 1e-6)); lm = np.log(np.maximum(o["mkt"][post], 1e-6))
    return dict(
        pre_mean=float(tot[pre].mean()), post_mean=float(tot[post].mean()),
        worst90_post=float(k.min()), cold_pre=cold(pre), cold_post=cold(post),
        store_floor=float(o["G"][D_FLOOR - 1]), store_tend=float(o["G"][min(D_TEND, D - 1)]),
        store_2y_before_end=float(o["G"][D_TEND - 730]),
        kept=float(o["kept"][rel_days].mean()) if rel_days.any() else float("nan"),
        stall_days=o["stall"], active=o["active"], min_margin=float(o["min_margin"]),
        vol_ratio=float(np.std(lt) / max(np.std(lm), 1e-9)),
    )


if __name__ == "__main__":
    scens = ["none", "fixed", "escrow", "bots", "tribes", "cartel", "open", "anyday", "hybrid"]
    worlds = {"fee_dominant": 0.15, "xen_dominant": 3.0}
    allsum, example = {}, {}
    for wname, xs in worlds.items():
        rng = np.random.default_rng(SEED)
        res = {s: [] for s in scens}
        for r in range(RUNS):
            world = synth(rng, xs)
            rho_med = float(np.median(world[1]))
            for s in scens:
                o = run(world, s)
                m = metrics(o); m["rho"] = rho_med
                res[s].append(m)
                if r == 3 and wname == "xen_dominant" and s in ("none", "bots", "hybrid", "escrow"):
                    example[s] = {k: o[k][::3].tolist() for k in ("mkt", "tot", "rel", "G", "w", "L")}
        summary = {}
        for s in scens:
            keys = res[s][0].keys()
            summary[s] = {k: float(np.nanmedian([m[k] for m in res[s]])) for k in keys}
            summary[s]["min_margin_worst"] = float(min(m["min_margin"] for m in res[s]))
            sf = np.array([m["store_floor"] for m in res[s]]); se = np.array([m["store_tend"] for m in res[s]])
            summary[s]["share_runs_store_stuck"] = float(np.mean(se > 0.10 * np.maximum(sf, 1e-9))) if sf.max() > 0 else 0.0
            summary[s]["worst90_p10"] = float(np.percentile([m["worst90_post"] for m in res[s]], 10))
        base = summary["none"]
        for s in scens:
            summary[s]["pre_vs_none"] = summary[s]["pre_mean"] / base["pre_mean"]
            summary[s]["post_vs_none"] = summary[s]["post_mean"] / base["post_mean"]
            summary[s]["worst90_vs_none"] = summary[s]["worst90_post"] / base["worst90_post"]
        allsum[wname] = summary
        print(f"== {wname}  (median fee share of a burn's cost: {summary['none']['rho']:.2f})")
        for s in scens:
            m = summary[s]
            print(f"{s:7s} pre {m['pre_vs_none']:.2f} post {m['post_vs_none']:.2f} worst90 {m['worst90_vs_none']:.2f} "
                  f"cold pre {m['cold_pre']:.2f} post {m['cold_post']:.2f} kept {m['kept']:.2f} "
                  f"store@floor {m['store_floor']:.0f} 2y-before-end {m['store_2y_before_end']:.1f} end {m['store_tend']:.1f} "
                  f"active {m['active']:.0f} minmargin {m['min_margin_worst']:.2g} stuck {m['share_runs_store_stuck']:.2f}")
    json.dump({"summary": allsum, "example": example, "runs": RUNS, "d_floor": D_FLOOR,
               "d_tend": D_TEND, "day0": str(DAY0)}, open("hearth_controller_test.json", "w"))
