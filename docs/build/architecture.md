# Architecture

## Principles

- The game **never writes** to the protocols. Burns, claims, stakes and deposits happen in the protocols' own apps or via deep links; the indexer attributes them.
- All game state is derived from **append-only chain logs plus signed player orders**. Turn outputs are hashed and published, so any player can recompute the scoreboard.
- Rules are **open source** and **deterministic**. Content (regions, lore, items) is data.

## Stack

| Part | Choice |
| --- | --- |
| Indexer | Typed event indexer (Ponder or a small viem worker) writing raw logs to PostgreSQL |
| Game engine | Deterministic TypeScript service that rebuilds state from logs + orders each turn |
| Client | Next.js with a hex-map canvas, the sky view and tribe pages; wagmi/viem; sign-in with Ethereum |
| 3D world | Browser three.js client on the same data (presence only) |
| Honours | Soulbound badges off-chain first; an optional audited non-transferable ERC-721 later |
| Protocol contracts | NXN, Granary, XenVault clones, Escrow (see [The NXN protocol](../granary/README.md)) |

## Indexing rules

- Settle a turn only on blocks at least 64 deep (two Ethereum epochs) to avoid reorg flips.
- Store raw logs append-only; derive everything from them.
- Phase 1 indexes Ethereum mainnet only. Other XEN chains come later as separate realms (which chains, and whether tribes can span them, is open).

## Releases

| Release | In scope | Out of scope |
| --- | --- | --- |
| Pre-season (read-only) | Sign-in, birth rank and era card, the night sky with dying-star alerts, live AMP sun, tribe join | Territory combat, any write action |
| Season 1 | Cooling map (37 hexes), daily turns, warmth scoring, war-burns, chronicle | Reaping, temples beyond DBXen |
| Mid Season 1 | Reaping with sponsor crates, temple registry (2–3 burners), honours | NXD Council votes |
| NXN launch | Granary, Hearth, tribe treasuries, NXN prices in game, Core Council, Fenix marks | — |

The read-only pre-season is roughly 3–4 weeks of work for one or two developers using AI-assisted coding.
