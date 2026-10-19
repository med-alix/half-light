import sys, json, datetime as dt
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from hyperstructure_sim import simulate, deflation_day, DAYS, D_FLOOR

GEN = dt.date(2022, 10, 8)
to_date = lambda d: GEN + dt.timedelta(days=int(d))
dates = [to_date(d) for d in DAYS]
R = 2000
q = lambda a, ps=(10, 50, 90): np.nanpercentile(a, ps, axis=-1)
post = DAYS >= D_FLOOR
res = {}

base = simulate(R, granary=False)
gr = simulate(R, granary=True, cap=None)
grc = simulate(R, granary=True, cap=0.2)

def fmt_day(x): return "never" if np.isnan(x) else to_date(x).isoformat()

# D1/D5: XEN net deflation date
for name, o in [("no_granary", base), ("granary", gr)]:
    dd = deflation_day(o["net"])
    res[f"deflation_{name}"] = {
        "share_never": float(np.isnan(dd).mean()),
        "p10": fmt_day(np.nanpercentile(dd, 10)) if (~np.isnan(dd)).any() else "never",
        "p50": fmt_day(np.nanpercentile(dd, 50)) if (~np.isnan(dd)).any() else "never",
        "p90": fmt_day(np.nanpercentile(dd, 90)) if (~np.isnan(dd)).any() else "never",
        "S_end_p10_50_90": [float(x) for x in q(o["S"][-1])],
    }

# D2: DBXen burn flow after the AMP floor (vs today's flow = 1.0)
for name, o in [("no_granary", base), ("granary_nocap", gr), ("granary_cap20", grc)]:
    flow = o["dbx"][post]
    res[f"dbx_{name}"] = {
        "post_floor_mean_p10_50_90": [float(x) for x in q(flow.mean(axis=0))],
        "share_days_below_10pct_median": float(np.median((flow < 0.10).mean(axis=0))),
        "flow_2033_p10_50_90": [float(x) for x in q(o["dbx"][DAYS == 3800][0])],
    }
res["granary_store_at_floor_p10_50_90"] = [float(x) for x in q(gr["G"][DAYS == D_FLOOR][0])]

# DXN reward decay (deterministic given k0)
p = base["params"]
res["dxn_reward_per_cycle_today_p10_50_90"] = [float(x) for x in q(10000 / 1.002 ** p["k0"])]
res["dxn_reward_at_floor_vs_today"] = float(1 / 1.002 ** (D_FLOOR - DAYS[0]))

# D3/D4: NXN emission schedule x sink intensity
grid = {}
for decay in (1.002, 1.0005):
    for c in (0.005, 0.02, 0.05):
        o = simulate(1000, seed=11, granary=True, nxn_decay=decay, nxn_c=c)
        nx = o["nxn"]
        peak_idx = nx.argmax(axis=0)
        minted_1y = 1000 * (1 - decay ** -365) / (1 - 1 / decay)
        cap = 1000 / (1 - 1 / decay)
        grid[f"decay{decay}_c{c}"] = {
            "cap": round(cap), "first_year_share": round(minted_1y / cap, 3),
            "peak_date_p50": to_date(DAYS[int(np.median(peak_idx))]).isoformat(),
            "peak_circ_p50": round(float(np.median(nx.max(axis=0)))),
            "circ_end_p10_50_90": [round(float(x)) for x in q(nx[-1])],
            "share_runs_declining_by_2031": float((DAYS[peak_idx] < 3007).mean()),
        }
        if decay == 1.0005 and c == 0.02: nxn_example = o
res["nxn_grid"] = grid
json.dump(res, open("results.json", "w"), indent=2)
print(json.dumps(res, indent=2))

# ---- charts
def fan(ax, o, key, label, color, scale=1.0):
    lo, mid, hi = q(o[key] * scale)
    ax.fill_between(dates, lo, hi, color=color, alpha=0.18, lw=0)
    ax.plot(dates, mid, color=color, lw=1.8, label=label)

fig, axs = plt.subplots(1, 3, figsize=(16, 4.6))
fan(axs[0], base, "S", "No Granary", "#5b6b7f"); fan(axs[0], gr, "S", "With Granary", "#c8641e")
axs[0].set_title("XEN circulating supply (today = 1)"); axs[0].legend()
# smooth DBXen flow with 30-day mean
def smooth(o):
    k = 30; c = np.cumsum(np.vstack([np.zeros((1, o["dbx"].shape[1])), o["dbx"]]), axis=0)
    s = np.vstack([np.full((k - 1, o["dbx"].shape[1]), np.nan), (c[k:] - c[:-k]) / k])
    return {"dbx": s}
fan(axs[1], smooth(base), "dbx", "No Granary", "#5b6b7f")
fan(axs[1], smooth(grc), "dbx", "Granary, 20% cap", "#8a8f2e")
fan(axs[1], smooth(gr), "dbx", "Granary, no cap", "#c8641e")
axs[1].set_yscale("log"); axs[1].set_title("XEN burned via DBXen per day (today = 1, 30d avg)"); axs[1].legend()
fan(axs[2], nxn_example, "nxn", "NXN circulating", "#c8641e", 1e-3)
axs[2].set_title("NXN circulating (thousands), decay 1.0005, c = 0.02")
for ax in axs:
    ax.axvline(to_date(D_FLOOR), color="k", ls=":", lw=1); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("sim_overview.png", dpi=140)
