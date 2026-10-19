# The living world

HALF-LIGHT is meant to grow the way an online world does: players, developers and AI tools keep adding places, items, stores and characters for years. What keeps that safe is one rule.

> **Creators can add anything except power.** Nothing a creator makes can change warmth, territory, NXN flows or the Granary. Those stay in the small, open, deterministic rules engine.

## Layers

| Layer | Who changes it | Examples |
| --- | --- | --- |
| Rules core | Seasonal community votes only | Power, warmth, the Granary, NXN, the auction |
| Content packs | Anyone, by pull request | Regions, quests, lore, temples for burner projects, characters |
| Items | Creators | Banners, armour skins, tribe heraldry, Hearth decorations, scouting maps, chronicle styles |
| Stores | Players and tribes | Stalls in the 3D world, tribe markets, the Drifters' caravans |
| Characters | Creators, including AI | Merchants, chroniclers, guides; always marked as AI, never holding power |

Content is plain data (for example JSON) checked against a published schema. The rules engine ignores anything it doesn't understand, so a broken content pack can never break the game state.

## Items

| Kind | How it is made | What it does |
| --- | --- | --- |
| **Forged items** | Forged by burning XEN through DBXen in the same transaction, using a creator's recipe | Cosmetic gear and banners. Every forging is a DBXen burn. |
| **Crafted items** | Made by a creator and listed in a store | Cosmetics, tribe heraldry, decorations |
| **Information tools** | Built by developers | Scouting maps, alert bots, dashboards. They show public chain data better; they never reveal hidden game state. |

Forged items are one more route into DBXen from day one: making things creates burns.

## Stores and the creator economy

- **Items sell in NXN.** A fixed share of every sale is burned (proposal: half); the creator keeps the rest.
- **Resales pay the creator a royalty**, part of which is also burned.
- **Drifters run the caravans**, the natural traders of the world; tribes can run their own markets; Outlaws can run an unofficial black market between tribes (still cosmetic only).
- **No loot boxes and no random paid drops.** Buying an item is a sale, not a bet, so the rule against losers paying winners still holds.
- **Creators earn from sales, never from the protocol.** No NXN emission goes to content.

## Contributing content

1. Open an issue with the **Design proposal** template describing the region, item set or character.
2. Submit the content pack as a pull request against the content schema.
3. Packs that only add cosmetics or lore can be merged by maintainers; anything touching shared spaces (a new region on the map, a temple) goes to the seasonal vote.

## AI characters

AI-run characters can guide, trade cosmetics, keep the chronicle or narrate the Reaping. They are always labelled as AI, they cannot hold territory or power, and they cannot vote in tribe councils.

## Open questions

- The exact burn share on sales and royalties
- Whether items are NFTs from the start or game records first
- Who maintains the content schema, and how disputes over shared spaces are decided
