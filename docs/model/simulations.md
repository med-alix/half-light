# Simulations

A Monte Carlo of XEN, DBXen and the Granary: 1,000–2,000 runs, daily steps from October 2026 to 2034–2037. XEN amounts are in units of today's circulating supply, so no live supply figure is needed. Contract rules come from the verified source; **every market input is a guessed range until measured on chain**. Treat results as directions, not forecasts.

The code is in the `sim/` folder at the root of the repository. Change the ranges in `draw_priors()` and post what you find.

![Simulation overview](../assets/charts/sim-overview.png)

## Guessed inputs

| Input | Range |
| --- | --- |
| Current XEN mint inflation | 3–25% per year |
| Current burn rate | 0.5–10% of supply per year |
| Burn response to DXN reward decay (ε) | 0.3–1.0 |
| Break-even AMP at today's price and gas | 30–1,500 |
| DBXen active cycles so far | 1,000–1,290 |
| Share of XEN staked | 2–15% |
| Granary deposits diverted from DBXen / new demand | 5–30% / 0–30% |

## Results (medians)

| Question | Result |
| --- | --- |
| DXN reward per cycle | ~1,000 today; about 5% of that by the floor |
| DBXen burn flow after the floor, no Granary | ~5–7% of today |
| Same, with the Granary (8-year release), no game | ~1.7× the no-Granary case |
| Same, with the Granary and game-driven deposits | ~2.4× the no-Granary case |
| DBXen flow before 2030 with the Granary | ~83% of the no-Granary case |
| Worst-year DBXen flow 2031–2037 | ~11% of today, vs ~1.1% with no Granary |
| Store left in 2037 (8-year release) | ~35% |
| XEN turns net deflationary | median Oct 2029; ~39% of runs never by 2034; the Granary moves it by weeks |
| NXN decay 1.002 vs 1.001 | 1.002 mints 52% in year one; 1.001 peaks supply near the floor |
| 20% cap on release | Makes the Granary do nothing |
| Quadratic tribe scoring | Splitting one wallet into k gave k² power; plain sum chosen |

**What the Granary is:** DBXen's winter reserve, not an XEN supply tool.

**Diversion matters.** With little diversion from DBXen (0–5%), pre-floor flow stayed near 97% of the no-Granary case. With 20–30% diversion it fell to about 74%. The burner bonus and half-burn deposits exist to keep diversion low.

## What drives the results

- Post-floor DBXen flow depends almost only on **ε** (rank correlation −0.70).
- The deflation date depends on today's **burn rate**, the **break-even AMP**, ε and the mint rate.

## Season simulator

The game simulator (`sim/game/half-light-simulator.html`, open it in a browser) plays seasons on the 37-hex map with AI tribes and lets you play as one. First findings: the Hearth-feeding tribe won 5 of 6 seasons (hence the Warden limits), and the Long Fire world at H = 9 is nearly empty.

## Still to simulate

- Responsive release vs the fixed 8-year rule, with floor minting included
- Half-burn deposits
- DXN and NXD deposits: hard 10% cap vs no cap vs taper
- Warden limits, Outlaws, and the 60/40 emission split against the balance targets
- Wallet splitting under the per-wallet cap

## Limits

Prices are random walks, not modelled from supply and demand. When the NXN sink exceeds supply, the model shows supply at zero instead of a price rise. Earlier runs treated floor minting as almost dead, so they probably underestimate post-floor XEN.
