# Lighting the Hearth

Every cycle the Granary has an allowance of XEN to burn into DBXen. Someone has to send that burn and pay DBXen's ETH fee. In return they keep a share of the DXN those batches earn. Nobody knows in advance what share is fair, because it depends on gas, the DXN price and how busy DBXen is that day. So the share **starts low and rises every hour**, and the first person to accept takes it: a rising-share (Dutch) auction.

## How it works

- The allowance is split into **3 lots** per cycle.
- For each lot the caller's share starts at **10%** and rises to **100%** over the 24-hour cycle.
- The first caller pays the DBXen fee for the lot, the Granary burns its XEN in the same transaction, and the caller keeps its share of the DXN. The Granary keeps the rest and stakes it.
- The XEN never leaves the contract, so nobody can take it.
- A lot nobody takes is burned by the Granary's small reserve, or carries over (see [Release](release.md)).

### Example

100 batches earn 10 DXN; the DBXen fee is 0.1 ETH plus 0.005 ETH of gas; DXN is worth 0.02 ETH, so the lot's DXN is worth 0.2 ETH.

| Hour | Caller's share | Caller gets | Worth | Cost | Worth calling? |
| --- | --- | --- | --- | --- | --- |
| 0 | 10% | 1 DXN | 0.02 ETH | 0.105 ETH | No |
| 6 | 32% | 3.2 DXN | 0.065 ETH | 0.105 ETH | No |
| **11.3** | **52.5%** | 5.25 DXN | 0.105 ETH | 0.105 ETH | **Break-even: a bot lights it** |
| 18 | 77% | 7.7 DXN | 0.155 ETH | 0.105 ETH | Already taken |

The Granary keeps 47.5% of the DXN. If gas doubles, break-even comes later in the day; in a quiet cycle each batch earns more DXN and someone lights earlier. **Nobody had to guess gas or prices; the clock found the price.**

## The tribe game

In the game the auction clock is the Hearth dimming through the day.

- The lighter's wallet earns its DXN share as usual. If that wallet is registered to a tribe, the tribe becomes **Keeper of the Hearth** for the day: prestige, plus a warmth bonus on its hexes.
- **Lighting earlier earns more prestige**, because the Granary keeps more.
- Tribe councils decide every day: light early for the title, wait for more DXN, or leave it to others. Treasuries (tribe multisigs) can pool the fee.

In the example, a tribe that values the title might light at hour 8 (40%). It pays 0.105 ETH and gets 4 DXN (0.08 ETH back), spending about 0.025 ETH for the title. The Granary keeps 60% instead of 47.5%. **Tribes pay in glory instead of DXN, and the protocol gets cheaper.** In the synthetic test, tribe prestige raised the Granary's kept share by about 12 points.

## On-chain tribe registry

A wallet declares its tribe in a small registry contract (changes only between seasons). The Granary credits the Keeper tribe directly from the registry, with no oracle and nobody posting game results on chain.

## Classic problems

| Problem | Applies? | Answer |
| --- | --- | --- |
| Byzantine agreement | No | The auction needs no agreement among players, only one rational caller out of anyone. Safety comes from the contract: the XEN never leaves it and the allowance is capped. It would come back only if the game decided something off chain, which the registry avoids. |
| Cartel of tribes waiting for a high share | Yes | **Anyone can light, not only tribes.** Outlaws and bots break any cartel at break-even. In the test a closed cartel cut the Granary's kept share to ~10%; open access restored it fully. |
| Bots and front-running | Yes, for fun not for the protocol | Bots light at the break-even second and copy pending transactions. The burn still happens. Mitigations: 3 lots per cycle, private transaction relays for tribes, prestige only for wallets that pass the eligibility gate (a bot that registers is an Outlaw mercenary). |
| Volunteer's dilemma (everyone waits) | No | Waiting is never free: someone else takes the lot. |
| Gas spikes | Handled | Callers wait for a higher share; the reserve covers what the market won't; otherwise the allowance waits. |

## Kept in reserve: a sealed-bid version

Tribes submit hidden bids for the share they would accept; the lowest wins at cycle end and executes. It removes the bot race and fits council strategy, but needs deposits and penalties in case the winner doesn't execute after gas moves. To consider only if bots spoil the game in practice.
