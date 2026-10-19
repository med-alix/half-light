import sys, json, numpy as np
sys.path.insert(0, ".")
import hyperstructure_sim as H
from hyperstructure_sim import simulate
H.D_END = 5200; H.DAYS = np.arange(H.D0, H.D_END); H.T = len(H.DAYS)
DAYS = H.DAYS; post = DAYS >= H.D_FLOOR
out = {}
# 1) Release horizon (no cap). Metric: median post-floor flow, 10th pct of yearly flow 2031-2037, flow in 2036
for hy in (3, 5, 8):
    o = simulate(1500, seed=3, granary=True, cap=None, horizon_y=hy)
    f = o["dbx"][post]
    yearly = f[: (f.shape[0] // 365) * 365].reshape(-1, 365, f.shape[1]).mean(axis=1)
    out[f"horizon_{hy}y"] = {
        "post_floor_median": round(float(np.median(f.mean(axis=0))), 3),
        "worst_year_median": round(float(np.median(yearly.min(axis=0))), 3),
        "flow_2036_median": round(float(np.median(o["dbx"][DAYS == 5000][0])), 3),
        "store_left_2037_median": round(float(np.median(o["G"][-1] / np.maximum(o["G"][DAYS == H.D_FLOOR][0], 1e-12))), 3),
    }
base = simulate(1500, seed=3, granary=False)
f = base["dbx"][post]; yearly = f[: (f.shape[0] // 365) * 365].reshape(-1, 365, f.shape[1]).mean(axis=1)
out["no_granary"] = {"post_floor_median": round(float(np.median(f.mean(axis=0))), 3),
                     "worst_year_median": round(float(np.median(yearly.min(axis=0))), 3),
                     "flow_2036_median": round(float(np.median(base["dbx"][DAYS == 5000][0])), 3)}
# 2) Diversion vs new demand: pre-floor DBXen flow loss and post-floor gain per unit of delta
for d_lo, d_hi, lab in ((0.0, 0.05, "low_diversion"), (0.2, 0.3, "high_diversion")):
    rng_backup = H.draw_priors
    def pri(R, rng, lo=d_lo, hi=d_hi):
        p = rng_backup(R, rng); p["delta"] = rng.uniform(lo, hi, R); return p
    H.draw_priors = pri
    o = simulate(1500, seed=3, granary=True)
    H.draw_priors = rng_backup
    pre = (DAYS >= H.L_NXN) & (DAYS < H.D_FLOOR)
    out[lab] = {"pre_floor_flow_vs_no_granary": round(float(np.median(o["dbx"][pre].mean(0) / base["dbx"][pre].mean(0))), 3),
                "post_floor_flow_vs_no_granary": round(float(np.median(o["dbx"][post].mean(0) / base["dbx"][post].mean(0))), 2)}
json.dump(out, open("final_checks.json", "w"), indent=1); print(json.dumps(out, indent=1))
