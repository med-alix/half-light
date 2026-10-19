# Deposits and emission

## What can be deposited

| Asset | Unit | Notes |
| --- | --- | --- |
| XEN | Batches of 2.5M | Pays an energy fee with DBXen's formula: gas × batches × (1 − 0.00005 × batches) |
| DXN | Any amount | Staked permanently in DBXen |
| NXD | Any amount | Staked permanently in NXD's staking vault |

Deposits are **never withdrawable**. That is what makes the store a winter reserve.

### Half-burn deposits (draft, to simulate)

Each XEN deposit burns **50% through DBXen immediately** and stores the other 50%. The depositor earns NXN on the full deposit. This removes most of the cost the Granary imposes on DBXen before the floor (simulations without it show pre-floor burn flow at about 83% of the no-Granary case).

## Emission

**NXN per active cycle = 1,000 × 1.001^−n**, n = active cycles so far. Maximum supply ≈ 1,001,000. No premine.

Why 1.001 and not DXN's 1.002: with 1.002, 52% of all NXN would be minted in the first year. With 1.001 and the game sink below, median supply peaks around October 2030, near the floor, and shrinks afterwards in 61% of simulated runs.

### The split

| Share | Goes to | How |
| --- | --- | --- |
| 60% | Depositors | By pool, then pro rata to that cycle's deposits |
| 40% | Territory holders in the game | By the yield of hexes each tribe holds at dusk, then by power contributed |

The territory share is what makes winning in the game matter. See [Winning, losing and NXN](../game/winning-and-nxn.md).

### Pool weights for the depositor share

- **XEN pool** = 0.5 + 0.4 × AMP / 3000 (0.70 today, 0.50 at the floor), read from `getCurrentAMP()`, no oracle.
- **DXN pool** = ⅔ of the rest; **NXD pool** = ⅓ of the rest.
- Inside a pool: pro rata to that cycle's deposits. An empty pool's share is not minted.

### Burner bonus

A wallet that also burned at least one batch in DBXen during the same cycle has its XEN deposit counted at **1.25×**. This rewards new deposits over burns diverted from DBXen. The Granary needs a public getter for a wallet's DBXen batches per cycle (to confirm).

### DXN and NXD share

The Granary is unlikely to compound its way to dominance in DXN staking: it re-stakes only 20% of its income as DXN, probably much less than NXD, whose share is still to read from the contract (see [Storage and routing](storage-and-routing.md)). It grows its share mainly through new deposits. Draft position: **no hard cap**, but NXN rewards for DXN and NXD deposits **taper** as the Granary's share of each stake pool grows, so dominance is possible but has to be earned. The alternative is a hard 10% cap. Both are to be simulated.

## The game sink

The game burns NXN as fuel. Target: on average **0.05 NXN per active player per day × the heat index H**. Prices adjust each season (see [Winning, losing and NXN](../game/winning-and-nxn.md)).
