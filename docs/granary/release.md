# Release

From XEN day **2,999** (about 24 December 2030) the Granary starts burning its store into DBXen in whole batches, with a 90-day ramp.

## The rule

**Rel = (G / τ) × clip((B\* / B̄)^γ, m_lo, m_hi)**

| Symbol | Meaning | Draft value |
| --- | --- | --- |
| G | XEN in the store | read on chain |
| τ | Base horizon | 8 years |
| B̄ | Market DBXen batches, average of the last 7 cycles | read on chain |
| B\* | Target burn flow | to set by simulation |
| γ | Responsiveness | between 0.5 and 1, to set by simulation |
| m_lo, m_hi | Bounds on the multiplier | 0.25 and 4 |

When market burns fall, the Granary releases more. When they rise, it releases less. It works like a reserve bank that steadies DBXen's burn flow.

![Responsive release](../assets/diagrams/release-controller.svg)

- **γ = 0** is the fixed rule (store ÷ τ). It is the rule the current simulations tested: release over 8 years gave the best worst year (11% of today's flow vs about 1% with no Granary) and left about 35% of the store in 2037.
- **The bounds set how long the store lasts.** At the maximum multiplier the store's half-life is τ × ln 2 / m_hi, about 1.4 years with τ = 8 and m_hi = 4.
- **Optional:** release less while floor minting is profitable, since new XEN is arriving anyway.

## Why it uses burns, not prices

The controller reads DBXen batch counts and the store, both on chain, not prices. Prices are easier to move. A burner who withholds burns to trigger more release just loses their own DXN share to the Granary's burns.

## Rejected options

- **A 20% cap on release** (no more than 20% of market burns): it made the Granary do nothing.
- **Short horizons (3–5 years):** worst-year flow of 1.3–1.9% of today, far worse than 8 years.
- **A fixed share of the store per year (8–20%):** worst year 5–7% of today.

## What happens when the store runs dry

The game's world shrinks with the store (see [The three eras](../game/eras.md)). What the ending looks like is an [open question](../open-questions.md).
