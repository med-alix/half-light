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
| Forge cycles | DBXen | `getCurrentCycle()`, `cycleTotalBatchesBurned(cycle)`, `rewardPerCycle(cycle)`, `Burn(userAddress, batchNumber)`, `NewCycleStarted` | Verified in source |
| DXN stakes | DBXen | `Staked`, `Unstaked` | Verified in source |
| The Core | NXD | `HandleRewards(ethReceived, dxnAmountReceived, dxnBurned, dxnToStake, nxdBurned, ethToStakingVault)`; NXD transfers to the dead address | Verified in source |
| Gas | Chain | `block.basefee` | — |
| Prices | Uniswap | TWAP observations for XEN/ETH, DXN/ETH, NXD/ETH | To pick pools |
| Castes | XENFT | Class metadata and events | Not checked yet |
| The Fallen | Fenix | Stake start and end events | Not checked yet |

## To confirm before coding

- A public getter for a wallet's DBXen batches in a given cycle (needed for the burner bonus).
- Whether NXD's sell tax applies to transfers into a contract like the Granary.
- NXD's re-stake share ρ_N, from its reward logic.
