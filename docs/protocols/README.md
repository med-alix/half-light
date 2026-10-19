# The protocols

HALF-LIGHT and the Granary sit on three existing protocols. Everything below was read in the published Solidity source on GitHub (XEN, DBXen, NXD). **Still open:** matching that source to the deployed bytecode and reading live state from chain.

| Layer | Contract rule | In the world | Status |
| --- | --- | --- | --- |
| XEN | AMP = max(3000 − days since genesis, 1), locked into each mint at claimRank | The sun cools | Verified in source |
| XEN | globalRank increments on every claimRank; each mint stores its cRank | Birth order and era | Verified in source |
| XEN | Reward = log2(max(globalRank − cRank, 2)) × AMP × term × (1000 + EAAR) / 1000; no balance input | Power from time and arrival, not wealth | Verified in source |
| XEN | EAAR starts at 100‰ and drops 1 per 100,000 ranks (0 after rank 10M) | Early-adopter bonus already gone | Verified in source |
| XEN | Max term = 100 + 15 × log2(globalRank) days, capped at 1,000 (≈ 465–480 days today) | Oaths | Verified in source |
| XEN | Late-claim penalty by days late: 0, 1, 3, 8, 17, 35, 72%, then 99% | Dying stars | Verified in source |
| XEN | Staking burns XEN, then re-mints principal + reward at withdrawal; APY = 20% − 1 per 90 days, floor 2%, locked at stake start; one stake per address | Seasons; keepers | Verified in source |
| XEN | burn(user, amount) only from contracts implementing IBurnRedeemable; records userBurns; emits Transfer to 0x0 | Temples | Verified in source |
| DBXen | Batches of 2.5M XEN (1–10,000 per tx); ETH fee ≈ gas × batches with a small bulk discount; reward starts at 10,000 DXN per cycle and is divided by 1.002 only on cycles with burns; fees go to stakers | The Forge; one turn per cycle | Verified in source |
| NXD | 5% sell tax (governance can edit the whitelist); supply cap = initial + 730k rewards + 15k dev; the DXN→NXD mint phase has ended; DBXen fees: 85% buy DXN (part burned, part swapped to NXD and burned, rest staked), 15% to NXD stakers | The Core | Verified in source |
| XENFT | Batch mints with rarity classes | Castes | Not checked yet |
| Fenix | Mint by burning XEN; early or late stake ends forfeit to survivors | The Fallen | Not checked yet |

## Pages

- [XEN](xen.md): minting, staking and what AMP does
- [DBXen](dbxen.md): batches, emission and fees
- [NXD](nxd.md): the compounding loop
- [After the floor](after-the-floor.md): what each contract does once AMP is 1
