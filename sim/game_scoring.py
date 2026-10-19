"""Tribe scoring checks: concentration of warmth and the payoff from splitting a wallet (sybil)."""
import json, numpy as np
rng = np.random.default_rng(5)
N = 3000
wealth = rng.lognormal(0, 2.0, N)                      # heavy-tailed capital
engage = rng.beta(2, 3, N)                              # time/participation, weakly tied to wealth
T = np.minimum(470 * engage * rng.uniform(0.5, 1.5, N), 470) * (1 + 0.3 * np.log1p(wealth) / 5)
B = wealth * engage * rng.uniform(0, 1, N) * 0.5        # batches burned in 7 days
S = 365 * engage * rng.uniform(0, 1, N) * (wealth > np.median(wealth) * 0.3)
a, b, c, Pmax = 1.0, 2.0, 1.0, 10.0
def P(T, B, S): return np.minimum(Pmax, a * np.log1p(T) + b * np.sqrt(B) + c * np.log1p(S))
def top10(x): xs = np.sort(x)[::-1]; return float(xs[: len(xs) // 10].sum() / xs.sum())
p = P(T, B, S)
linear = T / 47 + B + S / 36.5
res = {"top10_share_capital": round(top10(wealth), 2),
       "top10_share_linear_power": round(top10(linear), 2),
       "top10_share_dampened_capped_power": round(top10(p), 2)}
# sybil: a whale with B=100 batches/week, T=470, S=365 splits into k wallets (each needs own mint + gas)
Tw, Bw, Sw = 470, 100.0, 365
for k in (1, 2, 5, 10, 20):
    pk = P(np.full(k, Tw), np.full(k, Bw / k), np.full(k, Sw))
    res[f"split_{k}"] = {"sum_rule": round(float(pk.sum()), 1), "quadratic_rule": round(float(np.sqrt(pk).sum() ** 2), 1)}
# per-wallet daily cost of keeping a split wallet eligible, in 'power units': rank claim + claim gas every term, burns tx gas
json.dump(res, open("game_scoring.json", "w"), indent=1); print(json.dumps(res, indent=1))
