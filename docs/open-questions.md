# Open questions

Each question has a **draft position** (or none yet). A question moves to **Decided** once there is rough agreement in the discussion, with a link to it. Open an issue to discuss one.

## Protocol

| # | Question | Draft position |
| --- | --- | --- |
| P1 | Should the Granary have a token (NXN) at all? | Yes, but only after the game proves retention without it |
| P2 | Release rule after the floor | Responsive: store ÷ 8 years × a multiplier on market burns, bounded 0.25–4 |
| P3 | NXN emission decay | 1.001 per active cycle |
| P4 | NXN emission split | 60% depositors, 40% territory |
| P5 | DXN and NXD deposits | Allowed; rewards taper as the Granary's share grows (alternatives: hard 10% cap, no cap) |
| P6 | Half-burn deposits | 50% burned through DBXen at once, 50% stored |
| P7 | Income routing | 50% NXN burn, 30% XEN, 20% DXN |
| P8 | Release when floor minting is profitable | Reduce release while minting beats gas |

## Game

| # | Question | Draft position |
| --- | --- | --- |
| G1 | Tribes | Embers, Wardens, Drifters, plus Outlaws |
| G2 | Warden limits | Deposit glow halves every 30 days; 2× defending, 0.5× attacking |
| G3 | Tribe switching | Between seasons only; 50% power for 14 days |
| G4 | Joining | Players choose; smaller tribes get a recruit bonus |
| G5 | Reaping mechanics | Simple daily choices in Season 1 |
| G6 | Format | Browser strategy game first; 3D world as a presence layer; bots for Telegram and Discord |
| G7 | Which burner projects become temples | — |
| G8 | Names | HALF-LIGHT, NXN, tribe names are working titles |

## Not solved yet

| # | Question | Notes |
| --- | --- | --- |
| U1 | Wallet splitting | The cap and √/log terms make k wallets worth slightly more than one |
| U2 | Which chain(s) the game reads | XEN and DBXen run on several chains with very different gas |
| U3 | A new player's first day | A war-burn needs 2.5M XEN; what can someone with no XEN do? |
| U4 | Funding | With no premine, who pays for development, servers and the audit? |
| U5 | Rule changes | Contracts have no admin keys; who changes game parameters between seasons? |
| U6 | The ending | What happens when the Granary is empty? |
| U7 | Daily rhythm | How does a council decide each day across time zones? |

## To simulate

- [ ] Responsive vs fixed release, with floor minting
- [ ] Half-burn deposits: does pre-floor DBXen flow reach 100% of the no-Granary case?
- [ ] DXN and NXD deposits: hard cap vs no cap vs taper
- [ ] Warden limits: does each tribe win about a third of seasons?
- [ ] Outlaws: is pure Outlaw play ever the best strategy?
- [ ] Territory share: does the winner earn 2–3× the last tribe without snowballing?
- [ ] Wallet splitting under the per-wallet cap

## To measure on chain

- [ ] DBXen batches and reward per cycle since launch (gives ε and κ)
- [ ] XEN total supply, staked total, daily mint vs burn
- [ ] Current global rank
- [ ] A public getter for a wallet's DBXen batches per cycle
- [ ] Whether NXD's sell tax applies to transfers into the Granary
- [ ] NXD's re-stake share
- [ ] Fenix and XENFT contracts
- [ ] Source matched to deployed bytecode for XEN, DBXen and NXD

## Decided

*(nothing yet)*
