# The NXN protocol

**NXN is the closure token of the stack.** XEN rewards minting, DXN rewards burning now, NXD compounds DBXen fees, and NXN rewards **storing XEN to burn after AMP reaches 1**. Its contract is the **Granary**; in the game it is the **Hearth**.

![The Granary loop](../assets/charts/granary-loop.png)

## In one paragraph

People deposit XEN (and optionally DXN or NXD) into the Granary. Deposits are never withdrawable. The Granary stakes the XEN for 1,000-day terms and keeps the stake rewards. Depositors earn NXN each cycle. After the floor, the Granary burns its store into DBXen, a little every day, more when market burns are weak. The ETH income from its DXN and NXD stakes buys and burns NXN and refills the store.

## Contracts

| Contract | Job | Admin |
| --- | --- | --- |
| NXN (ERC-20) | Minted only by the Granary; burnable by holders | None |
| Granary | Takes deposits, mints NXN, runs vaults, releases XEN to DBXen, routes ETH | None, not upgradeable |
| XenVault clones | One XEN stake each (XEN allows one stake per address); 1,000-day terms, staggered | Granary only |
| Escrow | Holds ETH for future DBXen burn fees | Granary only |

No premine, no team allocation, no admin keys.

## Parameters at a glance

| Rule | Draft position |
| --- | --- |
| Emission | 1,000 × 1.001^−n NXN per active cycle; max supply ≈ 1,001,000 |
| Emission split | 60% to depositors, 40% to game territory holders |
| Deposits | XEN in 2.5M batches (plus an energy fee); DXN and NXD in any amount; never withdrawable |
| Half-burn deposits | Each XEN deposit burns 50% through DBXen at once and stores 50% (to simulate) |
| Pool weights | XEN = 0.5 + 0.4 × AMP / 3000; DXN = ⅔ of the rest; NXD = ⅓ of the rest |
| Burner bonus | 1.25× deposit weight for wallets that also burned in DBXen that cycle |
| DXN and NXD share | No hard cap; rewards taper as the Granary's share of staked DXN or NXD grows (hard 10% cap as the alternative) |
| Energy fee | DBXen's fee formula; to escrow until it holds 1.2× the fee to burn the whole store |
| Income routing | 50% buys and burns NXN, 30% buys XEN, 20% buys DXN |
| Release | From day 2,999: responsive, store ÷ τ × a multiplier that rises when market burns fall |
| Launch | Earliest 16 March 2027, only if the [launch gates](launch-gates.md) pass |

## Pages

- [Deposits and emission](deposits-and-emission.md)
- [Storage and routing](storage-and-routing.md)
- [Release](release.md)
- [Launch gates](launch-gates.md)
