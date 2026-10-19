import sys, json, numpy as np
sys.path.insert(0, ".")
import hyperstructure_sim as H
H.D_END = 5200; H.DAYS = np.arange(H.D0, H.D_END); H.T = len(H.DAYS)
DAYS = H.DAYS; post = DAYS >= H.D_FLOOR
out = {}
for rf in (0.08, 0.12, 0.20):
    o = H.simulate(1500, seed=3, granary=True, rel_frac=rf, ramp_days=90)
    f = o["dbx"][post]; yearly = f[: (f.shape[0] // 365) * 365].reshape(-1, 365, f.shape[1]).mean(axis=1)
    out[f"release_{int(rf*100)}pct_per_year"] = {
        "post_floor_median": round(float(np.median(f.mean(0))), 3),
        "worst_year_median": round(float(np.median(yearly.min(0))), 3),
        "flow_2036_median": round(float(np.median(o["dbx"][DAYS == 5000][0])), 3),
        "store_left_2037_vs_floor": round(float(np.median(o["G"][-1] / np.maximum(o["G"][DAYS == H.D_FLOOR][0], 1e-12))), 2)}
json.dump(out, open("release_rule.json", "w"), indent=1); print(json.dumps(out, indent=1))
