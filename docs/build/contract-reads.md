# Contract reads

The game runs on public reads and event logs. Names were read from the GitHub source; matching them to the deployed contracts is still open.

| Mechanic | Contract | Reads / events | Status |
| --- | --- | --- | --- |
| Sun temperature, dawn line | XEN | `getCurrentAMP()`, `genesisTs` | Verified in source |
| Seasons | XEN | `getCurrentAPY()` | Verified in source |
| Birth rank, era | XEN | `RankClaimed(user, term, rank)`, first per wallet; `globalRank` | Verified in source |
| Oaths | XEN | `userMints(address)` → term, maturityTs, rank, amplifier, eaaRate; `getCurrentMaxTerm()` | Verified in source |
| Dying stars | XEN | `userMints` maturityTs vs now; `MintClaimed(user, rewardAmount)` | Verified in source |
| XEN stakes | XEN | `userStakes(address)`; `Staked`, `Withdrawn`; `totalXenStaked` | Verified in source |
| Temple burns | XEN + each burner | `userBurns(address)`; per burn: XEN `Transfer(user, 0x0)` in the same tx as the burner's own event | Verified in source |
| Forge cycles | DBXen | `getCurrentCycle()`, `cycleTotalBatchesBurned(cycle)`, `rewardPerCycle(cycle)`, `Burn(userAddress, batchNumber)`, `NewCycleStarted` | Verified in source (same in v2) |
| DXN stakes | DBXen | `Staked`, `Unstaked` | Verified in source (same in v2) |
| The Core | NXD | `HandleRewards(ethReceived, dxnAmountReceived, dxnBurned, dxnToStake, nxdBurned, ethToStakingVault)`; NXD transfers to the dead address | Verified in source |
| Tribe registry | HALF-LIGHT | Wallet → tribe, updated between seasons | To build |
| Gas | Chain | `block.basefee` | — |
| Prices | Uniswap | TWAP observations for XEN/ETH, DXN/ETH, NXD/ETH | To pick pools |
| Castes | XENFT | Class metadata and events | Not checked yet |
| The Fallen | Fenix | Stake start and end events | Not checked yet |

## To confirm before coding

- A public getter for a wallet's DBXen batches in a given cycle (needed for the burner bonus).
- Whether NXD's sell tax applies to transfers into a contract like the Granary.
- NXD's re-stake share ρ_N, from its reward logic.
- DBXen on BNB Chain was exploited in March 2026 through a mix-up between `_msgSender()` (ERC-2771 forwarder) and `msg.sender` in `burnBatch`. The Granary must call DBXen directly, never through a forwarder, and every realm's DBXen copy needs its own review.
- That DBXen's `burnBatch` accepts a contract caller, lets the Granary forward the caller's ETH as the fee, and credits the burn to the Granary's address.
- How the Granary unstakes and approves XEN for DBXen before each burn (XEN's `burn` pulls through an allowance).
