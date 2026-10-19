# Storage and routing

## XEN storage

- Deposited XEN is staked in **XenVault clones**, one stake per clone (XEN allows one stake per address).
- Terms are **1,000 days**, staggered so stakes mature continuously.
- Matured stakes are restaked until the floor. Stake rewards (2% APY from March 2027) stay in the store.

## DXN and NXD storage

- DXN is staked permanently in DBXen; NXD in NXD's staking vault.
- DXN earned by the Granary's own winter burns is staked in DBXen too.

## Energy fee and the small reserve

Every XEN deposit pays an energy fee, the same formula as a DBXen burn. It funds a **small ETH reserve** (escrow). The reserve does not pay for every release: callers pay the DBXen fee through the [Hearth-lighting auction](lighting-the-hearth.md), and the reserve only pays for lots the auction leaves unsold. Above its target size, the surplus buys XEN on the market and stakes it. Because the reserve pays only what the market won't, nobody has to guess what gas will cost years from now; in the synthetic test it lasted to the horizon in 83–94% of runs, against 65% for an escrow paying every burn.

## Income routing

The ETH earned by the Granary's DXN and NXD stakes:

| Share | Use |
| --- | --- |
| 50% | Buys and burns NXN |
| 30% | Buys XEN and stakes it in the store |
| 20% | Buys DXN and stakes it |

## Swaps

All swaps are Uniswap TWAP-limited: at most 0.5% of pool depth per swap, at most one swap per hour.

## Why the Granary cannot take over DXN staking by compounding

Both NXD and the Granary re-stake part of their DBXen income as DXN. Their shares of staked DXN grow at:

- NXD: **y × ρ_N × φ(1 − φ)**, with ρ_N the share NXD re-stakes (most of its 85%, minus burns);
- Granary: **d_G / D_total + y × 0.2 × φ_G (1 − φ)**, where d_G is new DXN deposited.

Since the Granary re-stakes only 20%, its compounding should be much weaker than NXD's (to confirm once ρ_N is read from the contract). Its share grows mainly through deposits, so a cap or taper only matters if DXN deposits are large.
