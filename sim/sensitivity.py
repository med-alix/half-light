import sys, json, numpy as np
sys.path.insert(0, ".")
from hyperstructure_sim import simulate, deflation_day, DAYS, D_FLOOR
def rank(x): return np.argsort(np.argsort(x))
def spearman(a, b):
    m = ~np.isnan(a) & ~np.isnan(b); return float(np.corrcoef(rank(a[m]), rank(b[m]))[0, 1])
o = simulate(2000, granary=False); p = o["params"]
post = o["dbx"][DAYS >= D_FLOOR].mean(axis=0)
dd = deflation_day(o["net"]); dd_fill = np.where(np.isnan(dd), 9999, dd)
out = {"post_floor_dbx_flow": {k: round(spearman(post, p[k].astype(float)), 2) for k in ["b0","eps","k0","i0","be0","sigma","vol"]},
       "deflation_day": {k: round(spearman(dd_fill.astype(float), p[k].astype(float)), 2) for k in ["b0","eps","k0","i0","be0","sigma","vol"]}}
g = {}
for c in (0.02, 0.05):
    r = simulate(1000, seed=11, granary=True, nxn_decay=1.001, nxn_c=c); nx = r["nxn"]; pk = nx.argmax(axis=0)
    g[f"decay1.001_c{c}"] = {"peak_p50": int(np.median(nx.max(axis=0))), "peak_day_p50": int(np.median(DAYS[pk])),
        "end_p10_50_90": [int(x) for x in np.percentile(nx[-1], [10,50,90])], "declining_by_2031": float((DAYS[pk] < 3007).mean())}
out["nxn_decay_1.001"] = g
print(json.dumps(out, indent=1)); json.dump(out, open("sensitivity.json","w"), indent=1)
