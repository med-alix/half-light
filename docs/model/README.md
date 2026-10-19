# The model

A simplified analytical model of XEN, DBXen, NXD, the Granary and the game. The equations come from the contracts. The mechanisms are designed so that they **do not depend on data or forecasts**:

1. **Ratios, not levels.** Every signal compares the system to its own past, so it works on any chain, at any price, in any gas regime.
2. **Separate slow from fast.** Structural decline (climate) and cyclical activity (weather) are tracked apart.
3. **Bound every response.** No rule can overshoot or drain the store.
4. **Let markets price what we can't know** (gas, ETH costs) instead of guessing them.

Data, when it comes, tests the choices; it isn't needed to make them. Time step: one day = one DBXen cycle.

![The model](../assets/diagrams/model-map.svg)

## Inputs read from chain

| Input | Symbol | Source |
| --- | --- | --- |
| AMP | A | XEN `getCurrentAMP()` |
| DBXen reward per cycle | R | `rewardPerCycle` |
| DBXen market batches per cycle | B | `cycleTotalBatchesBurned` minus the Granary's own |
| New XEN ranks per day | N | change in `globalRank` |
| NXD burned per cycle | K | NXD `HandleRewards` events |
| Granary store | G | Granary contract |
| Gas | g | `block.basefee` (game display only) |

No price oracle is needed for the Granary. The game may show TWAP prices for display.

## 1. XEN

- Mint reward: **r = log2(Δ) × A × T × (1 + EAAR)**; at the floor **r ≈ log2(Δ) × T**.
- Break-even price: **p_x\* = c_m / r**, with c_m the gas cost of claimRank + claimMintReward. This caps supply growth at production cost; it is not a price floor.
- Supply: **dS/dt = mints + s·S·APY/365 − 2.5M·B − Granary deposits**, APY = 2% from March 2027.

## 2. DBXen

- Emission: **R_n = 10,000 × 1.002^−n**, n = active cycles.
- Free-entry burns: **B ≈ κ × R × p_d / (2.5M × p_x + c_b)**. Burn volume follows emission; empirically B ∝ R^ε. About 1,500 more active cycles before the floor shrink R by about 20×, so post-floor burns ≈ (1/20)^ε of today (≈22% at ε = 0.5, ≈5% at ε = 1).
- **Fee share ρ = c_b / (2.5M·p_x + c_b)**: the part of a burn's cost that is the ETH fee. It decides how useful the Granary's free XEN is to a caller (below).

## 3. NXD

NXD's share φ of staked DXN is logistic: **dφ/dt = y × ρ_N × φ × (1 − φ)**, with y the fee yield of staked DXN and ρ_N the share NXD re-stakes.

## 4. Climate and weather

- **Climate C = 1 + ½·ln(3000 / A) + ½·ln(10,000 / R)**: slow, structural. Keeps cooling after the floor through DXN disinflation, only on active cycles.
- **Weather w = clip(½·ln(S/L)[B/R] + ¼·ln(S/L)[N] + ¼·ln(S/L)[K], −1, 1)**, with S and L the 7- and 180-cycle running averages. Mean ≈ 0 over time once burns are measured per DXN emitted.
- **Game heat = C × 2^(−w).** See [Climate and weather](../game/climate-and-weather.md).

## 5. Granary

- Store: **dG/dt = deposits + yield − release**.
- **Allowance** per cycle: **½ × max(0, L − S)[B/R] × R/R₀ + annuity**, annuity = G / (days to horizon) after the floor.
- **Budgets:** before the floor only the yield can be released; after the floor the cyclical part ≤ 3 × annuity; only on active cycles; carry-over ≤ 7 cycles.
- **Execution:** the [Hearth-lighting auction](../granary/lighting-the-hearth.md) first, then a small reserve.

### When does a caller light the Hearth?

A lot of e batches earns DXN worth V × e / (B + e), where V is the DXN value per cycle. The caller pays only the fee c_b per batch (the XEN is free). Break-even share:

**σ\* = c_b × (B + e) / V**

At market equilibrium V ≈ κ × B × (2.5M·p_x + c_b), so **σ\* ≈ ρ × (1 + e/B) / κ**. The most the market will absorb at σ ≤ 1 is

**e_max ≈ B × (κ / ρ − 1)**

- When XEN is a large share of a burn's cost (ρ small), callers can absorb many extra batches: the auction works on its own.
- When the fee dominates (ρ near 1), callers absorb few: the small reserve has to pay the rest. This is why the hybrid is needed.

### Why the drawdown is optimal

Spending a fixed stock G evenly over a horizon T is solved by c_t = G_t / (T − t): any extra spending in a winter automatically lowers every later day's spend, and the store still lasts to T.

## 6. Game

- Hex threshold θ = θ₀ × (1 + ring) × heat.
- Extra burns and deposits from the game: **ΔB = λ × active players**, λ to fit from the prototype.
- NXN prices adjust ×(target / actual)^0.5, at most ±25% per season.

## Design choices (not fitted to data)

| Choice | Value | Based on |
| --- | --- | --- |
| Short window | 7 cycles | One week smooths daily noise |
| Long window | 180 cycles | Two seasons: longer than a game season, shorter than a market cycle |
| Gap filled | ½ | Can't overshoot; robust to misreading |
| Horizon | 8 years after the floor | A social choice about how long the reserve lasts |
| Auction range | 10% → 100% over a cycle, 3 lots | The market finds the actual price |
| Weather strength | 2× | Noticeable without breaking scoring |
| Cyclical cap | 3 × annuity | Limits how fast a long bear can spend the store |

## Coefficients to measure later

| Symbol | Meaning | Data |
| --- | --- | --- |
| κ, ε | Burn premium and elasticity | DBXen events, prices, gas |
| ρ | Fee share of a burn's cost | DBXen fees vs XEN price |
| ρ_N | NXD re-stake share | NXD contract and rewards |
| λ | Burns per active player | Game prototype |

They change the size of the results, not which mechanism is chosen.
