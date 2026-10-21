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
| AMP | $A$ | XEN `getCurrentAMP()` |
| DBXen reward per cycle | $R$ | `rewardPerCycle` |
| DBXen market batches per cycle | $B$ | `cycleTotalBatchesBurned` minus the Granary's own |
| New XEN ranks per day | $N$ | change in `globalRank` |
| NXD burned per cycle | $K$ | NXD `HandleRewards` events |
| Granary store | $G$ | Granary contract |
| Gas | $g$ | `block.basefee` (game display only) |

No price oracle is needed for the Granary. The game may show TWAP prices for display.

## 1. XEN

**Mint reward**, and its value at the floor:

$$
r = \log_2(\Delta) \times A \times T \times (1 + \text{EAAR})
\qquad\qquad
r_{\text{floor}} \approx \log_2(\Delta) \times T
$$

**Break-even price**, with $c_m$ the gas cost of claimRank + claimMintReward. This caps supply growth at production cost; it is not a price floor.

$$
p_x^{*} = \frac{c_m}{r}
$$

**Supply**, with APY = 2% from March 2027:

$$
\frac{dS}{dt} = \text{mints} + s\,S\,\frac{\text{APY}}{365} - 2.5\text{M}\cdot B - \text{Granary deposits}
$$

## 2. DBXen

**Emission**, with $n$ the number of active cycles:

$$
R_n = 10{,}000 \times 1.002^{-n}
$$

**Free-entry burns:**

$$
B \approx \frac{\kappa \, R \, p_d}{2.5\text{M} \cdot p_x + c_b}
$$

Burn volume follows emission; empirically $B \propto R^{\varepsilon}$. About 1,500 more active cycles before the floor shrink $R$ by about 20×, so post-floor burns are about $(1/20)^{\varepsilon}$ of today (≈22% at $\varepsilon = 0.5$, ≈5% at $\varepsilon = 1$).

**Fee share**, the part of a burn's cost that is the ETH fee. It decides how useful the Granary's free XEN is to a caller (below).

$$
\rho = \frac{c_b}{2.5\text{M} \cdot p_x + c_b}
$$

## 3. NXD

NXD's share $\varphi$ of staked DXN is logistic, with $y$ the fee yield of staked DXN and $\rho_N$ the share NXD re-stakes:

$$
\frac{d\varphi}{dt} = y \, \rho_N \, \varphi \, (1 - \varphi)
$$

## 4. Climate and weather

**Climate**: slow, structural. Keeps cooling after the floor through DXN disinflation, only on active cycles.

$$
C = 1 + \tfrac{1}{2}\ln\frac{3000}{A} + \tfrac{1}{2}\ln\frac{10{,}000}{R}
$$

**Weather**, with $S[x]$ and $L[x]$ the 7- and 180-cycle running averages of a signal $x$. Its mean is about 0 over time once burns are measured per DXN emitted.

$$
w = \operatorname{clip}\!\left(
\tfrac{1}{2}\ln\frac{S[B/R]}{L[B/R]}
+ \tfrac{1}{4}\ln\frac{S[N]}{L[N]}
+ \tfrac{1}{4}\ln\frac{S[K]}{L[K]},\; -1,\; 1\right)
$$

**Game heat.** See [Climate and weather](../game/climate-and-weather.md).

$$
\text{Heat} = C \times 2^{-w}
$$

## 5. Granary

**Store:**

$$
\frac{dG}{dt} = \text{deposits} + \text{yield} - \text{release}
$$

**Allowance** per cycle, with annuity $= G \,/\, (\text{days to horizon})$ after the floor:

$$
\text{allowance} = \tfrac{1}{2}\max\!\big(0,\; L[B/R] - S[B/R]\big) \times \frac{R}{R_0} + \text{annuity}
$$

- **Budgets:** before the floor only the yield can be released; after the floor the cyclical part ≤ 3 × annuity; only on active cycles; carry-over ≤ 7 cycles.
- **Execution:** the [Hearth-lighting auction](../granary/lighting-the-hearth.md) first, then a small reserve.

### When does a caller light the Hearth?

A lot of $e$ batches earns DXN worth $V e / (B + e)$, where $V$ is the DXN value per cycle. The caller pays only the fee $c_b$ per batch (the XEN is free). Break-even share:

$$
\sigma^{*} = \frac{c_b \,(B + e)}{V}
$$

At market equilibrium $V \approx \kappa B \,(2.5\text{M} \cdot p_x + c_b)$, so

$$
\sigma^{*} \approx \frac{\rho \,(1 + e/B)}{\kappa}
$$

The most the market will absorb at $\sigma \le 1$ is

$$
e_{\max} \approx B \left(\frac{\kappa}{\rho} - 1\right)
$$

- When XEN is a large share of a burn's cost ($\rho$ small), callers can absorb many extra batches: the auction works on its own.
- When the fee dominates ($\rho$ near 1), callers absorb few: the small reserve has to pay the rest. This is why the hybrid is needed.

### Why the drawdown is optimal

Spending a fixed stock $G$ evenly over a horizon $T$ is solved by

$$
c_t = \frac{G_t}{T - t}
$$

Any extra spending in a winter automatically lowers every later day's spend, and the store still lasts to $T$.

## 6. Game

- Hex threshold: $\theta = \theta_0 \times (1 + \text{ring}) \times \text{Heat}$.
- Extra burns and deposits from the game: $\Delta B = \lambda \times \text{active players}$, with $\lambda$ to fit from the prototype.
- NXN prices adjust by a factor $(\text{target} / \text{actual})^{0.5}$, at most ±25% per season.

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
| $\kappa$, $\varepsilon$ | Burn premium and elasticity | DBXen events, prices, gas |
| $\rho$ | Fee share of a burn's cost | DBXen fees vs XEN price |
| $\rho_N$ | NXD re-stake share | NXD contract and rewards |
| $\lambda$ | Burns per active player | Game prototype |

They change the size of the results, not which mechanism is chosen.
