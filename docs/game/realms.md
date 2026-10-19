# Realms

XEN and DBXen run on many EVM chains. In HALF-LIGHT **each chain is a realm**, and because XEN was deployed on each chain on its own day, **each realm has its own sun**: its own AMP clock, its own climate.

## The realms

The community dashboard [xen.pub](https://xen.pub/) lists XEN, with a DBXen deployment, on 14 chains.

| Chain | XEN ticker on the dashboard |
| --- | --- |
| Ethereum | XEN |
| Ethereum PoW | vvXEN |
| Avalanche | aXEN |
| Base | cbXEN |
| BNB Chain | bXEN |
| Dogechain | dcXEN |
| Evmos | coXEN |
| Fantom | fmXEN |
| Moonbeam | mbXEN |
| OKX Chain | okXEN |
| Optimism | opXEN |
| Polygon | mXEN |
| PulseChain | pXEN |
| PulseChain OG | ogXEN |

**To verify before any realm opens:** contract addresses, each chain's XEN genesis date (its AMP clock), that DBXen there is the same code, and whether NXD exists on that chain. PulseChain copied Ethereum's state when it forked, so its XEN may share Ethereum's clock.

## How realms work

- **Each realm has its own climate.** The climate formula reads that chain's AMP and DBXen emission, unchanged. Older realms are colder.
- **Each realm has its own map** and its own daily territory war.
- **Cheap realms for newcomers.** Gas differs hugely between chains, so a new player can start in a low-gas realm and learn there.
- **One identity everywhere.** An EVM address is the same on every chain, so lineage, titles and prestige follow a player. Power caps count each address once across all realms, so spreading over chains does not bypass them.
- **Tribes span realms as houses**, with a branch in each realm.
- **A cross-realm Reaping** once a season brings tributes from every realm together. Results are combined by the indexer reading every chain; nothing crosses a bridge.

## No bridges

Each realm that gets a Granary has **its own Granary**, releasing into its own chain's DBXen. Bridges are the most attacked part of crypto and the design doesn't need one.

| Question | Option A | Option B |
| --- | --- | --- |
| NXN | A separate NXN per realm: simple and safe, but liquidity is split | One NXN on a home chain: one market, but other realms would need a bridge or no NXN |
| Granaries | Only on the realms with enough activity | On every realm |

Draft position: **separate NXN per realm, Granaries only where activity justifies an audit.**

## Rollout

1. Ethereum first (the realm the protocol facts were verified on).
2. Add realms one at a time, each after its contracts are checked and the indexer is extended. Indexing many chains costs more to build and run.

## Risks

- **Cheap realms also mean cheap sybil wallets.** Low-gas realms may need a stricter eligibility gate (older first rank, more activity before power counts).
- **Contract differences.** A copy of DBXen on another chain may differ from the Ethereum code or carry its own bugs. In March 2026 DBXen on BNB Chain lost about 23 BNB to an exploit mixing up the caller identity in `burnBatch` (ERC-2771 forwarder vs the real sender). Every realm's contracts need their own check.
