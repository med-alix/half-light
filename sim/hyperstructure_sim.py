"""
XEN / DXN / NXD + proposed NXN Granary -- simplified Monte Carlo model.

Contract rules (verified in published Solidity, 17 Oct 2026):
  XEN   AMP(d) = max(3000 - d, 1);  APY(d) = max(20 - floor(d/90), 2) %, locked at stake start
        mint reward = log2(rankDelta) * AMP_locked * term * (1000+EAAR)/1000   (no balance input)
        stake: XEN burned at stake, re-minted (+ APY*term/365) at maturity
  DXN   reward per active cycle R_k = 10000 / 1.002^k ; batch = 2.5M XEN ; ETH fee ~ gas x batches
NXN / Granary are PROPOSED mechanics (not deployed).

Everything uncertain is drawn from a prior per run. XEN quantities are in units of
today's circulating supply (S0 = 1), so no live supply number is needed. Replace the
priors with live chain data (supply, burn rate, mint rate, staked share) when available.
"""
import numpy as np

D0, D_FLOOR, D_END = 1470, 2999, 4400          # XEN days: today (17 Oct 2026), AMP floor, ~Oct 2034
L_NXN = 1620                                   # proposed NXN / Granary launch (16 Mar 2027)
DAYS = np.arange(D0, D_END)
T = len(DAYS)


def amp(d):
    return np.maximum(3000 - d, 1)


def apy(d):
    return np.maximum(20 - np.floor(d / 90), 2)


def draw_priors(R, rng):
    lu = lambda a, b, n: np.exp(rng.uniform(np.log(a), np.log(b), n))
    return dict(
        i0=lu(0.03, 0.25, R),          # current annual XEN mint inflation (fraction of supply)
        be0=lu(30, 1500, R),           # break-even AMP at today's XEN price and gas
        term=rng.integers(100, 400, R),  # average mint term (days)
        vol=rng.uniform(0.6, 1.2, R),  # annual volatility of XEN/ETH price
        sigma=rng.uniform(0.02, 0.15, R),  # share of supply staked in XEN
        b0=lu(0.005, 0.10, R),         # current annual market burn rate (fraction of supply)
        eps=rng.uniform(0.3, 1.0, R),  # elasticity of burn demand to DXN reward per cycle
        k0=rng.integers(1000, 1290, R),  # active DBXen cycles elapsed so far
        delta=rng.uniform(0.05, 0.30, R),  # share of market burns diverted into the Granary
        g=rng.uniform(0.0, 0.30, R),   # extra (game-driven) deposits, as share of market burns
        fbuy=rng.uniform(0.0, 0.10, R),  # energy-fee XEN buys, as share of deposits
        N0=lu(200, 5000, R),           # NXN game players at launch
        muN=rng.normal(0.0, 0.5, R),   # annual drift of player count
        phi=rng.uniform(0.0, 0.05, R),  # annual NXN buyback-burn (share of circulating) after floor
    )


def simulate(R=2000, seed=7, granary=False, cap=None, horizon_y=5.0,
             nxn_decay=1.002, nxn_c=0.02, rel_frac=None, ramp_days=0):
    """cap: None or max Granary release as a multiple of 30-day avg market DBXen burns."""
    rng = np.random.default_rng(seed)
    p = draw_priors(R, rng)

    # price path (log XEN/ETH relative to today), needed for break-even AMP of past mint starts
    dlogp = rng.normal(-0.5 * (p["vol"] ** 2) / 365, p["vol"] / np.sqrt(365), (T, R))
    logp = np.cumsum(dlogp, axis=0)
    def mint_activity(idx_start):  # idx_start: (R,) index into DAYS of mint start (may be <0)
        d_start = D0 + idx_start
        lp = np.where(idx_start >= 0, logp[np.clip(idx_start, 0, T - 1), np.arange(R)], 0.0)
        be = p["be0"] * np.exp(-lp)
        a = amp(d_start)
        return a / (1.0 + (be / a) ** 3)
    F0 = mint_activity(-p["term"])

    burn_noise = np.exp(rng.normal(-0.18, 0.6, (T, R)))  # daily lognormal, mean ~1
    regime = np.exp(np.cumsum(rng.normal(0, 0.02, (T, R)), axis=0))  # slow sentiment walk

    S = np.ones(R); S_floor = None
    G = np.zeros(R)                                   # Granary store (staked XEN)
    R0 = 10000 / 1.002 ** p["k0"]
    nxn_circ = np.zeros(R); nxn_minted = np.zeros(R)
    logN = np.log(p["N0"])
    mkt_hist = np.zeros((30, R)); mkt_ptr = 0
    out = {k: np.zeros((T, R)) for k in ["S", "net", "dbx", "G", "nxn", "mint", "mkt"]}

    base_burn = p["b0"] / 365.0
    for t, d in enumerate(DAYS):
        dxn_ratio = (1 / 1.002 ** t)              # DXN reward per cycle vs today (all cycles active)
        mint = (p["i0"] / 365.0) * mint_activity(t - p["term"]) / F0
        stake_issue = p["sigma"] * S * apy(d - 500) / 100 / 365
        mkt = base_burn * S * dxn_ratio ** p["eps"] * burn_noise[t] * regime[t]

        on = granary and d >= L_NXN
        dep = (p["delta"] + p["g"]) * mkt if on else 0.0
        buys = p["fbuy"] * dep if on else 0.0
        mkt_dbx = (1 - p["delta"]) * mkt if on else mkt
        extra = (p["g"] * mkt + buys) if on else 0.0   # XEN removed beyond the market burns

        rel = np.zeros(R)
        if on:
            G = G * (1 + 0.02 / 365) + dep + buys      # stakes compound at locked 2% APY
            if d >= D_FLOOR:
                if rel_frac is not None:            # perpetual: fixed share of store per year
                    rel = G * rel_frac / 365
                else:
                    days_left = max(D_FLOOR + horizon_y * 365 - d, 30)
                    rel = G / days_left
                if ramp_days:
                    rel = rel * min(1.0, (d - D_FLOOR + 1) / ramp_days)
                if cap is not None:
                    rel = np.minimum(rel, cap * mkt_hist.mean(axis=0))
                G = G - rel

        S = np.maximum(S + mint + stake_issue - mkt - extra, 1e-9)
        if d == D_FLOOR:
            S_floor = S.copy()
        mkt_hist[mkt_ptr % 30] = mkt_dbx; mkt_ptr += 1

        # NXN
        if on:
            e = 1000 / nxn_decay ** (d - L_NXN)
            logN = logN + p["muN"] / 365 + rng.normal(0, 0.02, R)
            N = np.minimum(np.exp(logN), 50000)
            if d < D_FLOOR:
                H = 1 + np.log(3000 / amp(d))
            else:
                H = (1 + np.log(3000)) * np.maximum(1 + np.log(S_floor / S), 1.0)
            sink = nxn_c * N * H + (p["phi"] / 365 if d >= D_FLOOR else p["phi"] / 4 / 365) * nxn_circ
            nxn_minted += e
            nxn_circ = np.maximum(nxn_circ + e - sink, 0.0)

        out["S"][t] = S; out["net"][t] = mint + stake_issue - mkt - extra
        out["dbx"][t] = (mkt_dbx + rel) / (base_burn * 1.0)   # DBXen burn flow vs today's
        out["G"][t] = G; out["nxn"][t] = nxn_circ; out["mint"][t] = mint; out["mkt"][t] = mkt
    out["params"] = p
    return out


def deflation_day(net):
    """First day after which the 90-day average net supply change stays negative for 365 days."""
    k = 90
    c = np.cumsum(np.vstack([np.zeros((1, net.shape[1])), net]), axis=0)
    ma = (c[k:] - c[:-k]) / k
    neg = ma < 0
    res = np.full(net.shape[1], np.nan)
    for r in range(net.shape[1]):
        run = 0
        for i, v in enumerate(neg[:, r]):
            run = run + 1 if v else 0
            if run >= 365:
                res[r] = DAYS[i + k - 365 + 1]
                break
    return res
