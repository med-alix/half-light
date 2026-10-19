# DBXen

DBXen turns XEN burns into DXN.

## Rules

- Burns happen in **batches of 2.5M XEN**, 1 to 10,000 batches per transaction.
- Each burn pays an **ETH fee** ≈ gas used × gas price × batches × (1 − 0.00005 × batches).
- The fee goes to **DXN stakers**.
- Each 24-hour cycle distributes a reward pool to that cycle's burners, pro rata to batches.
- The pool starts at **10,000 DXN** and is divided by **1.002** only on cycles that see a burn. A quiet cycle pauses decay.

**R_n = 10,000 × 1.002^−n**, where n is the number of active cycles so far.

With roughly 1,000–1,300 active cycles so far, today's pool is about **1,000 DXN per cycle**. About 1,500 more active cycles before the AMP floor bring it to about **1/20 of that**.

![DBXen emission and burn flow](../assets/diagrams/dxn-emission.svg)

## Why burns fall with emission

If burners keep burning until the cost of a batch (XEN plus fee) roughly equals the DXN it earns:

**B ≈ κ × R × p_d / (2.5M × p_x + fee)**

Burn volume follows emission. Empirically, burns scale as R^ε, and ε (between about 0.3 and 1) is the single most important unknown in the whole model. See [The model](../model/README.md).

## Useful reads

`getCurrentCycle()`, `cycleTotalBatchesBurned(cycle)`, `rewardPerCycle(cycle)`, events `Burn(userAddress, batchNumber)`, `NewCycleStarted`, `Staked`, `Unstaked`.
