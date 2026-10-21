# NXD

NXD is a protocol that holds staked DXN and spends its DBXen fees.

## Rules

- **5% tax on sells.** Governance can edit the tax whitelist.
- **Supply cap** = initial supply + 730k rewards + 15k dev.
- The 14-day DXN → NXD mint phase (rate falling from 1:1 to 1:0.5) has **ended**.
- The ETH fees earned by NXD's staked DXN are split:
  - **85% buys DXN**: part is burned (11.1%), part is swapped to NXD and burned, the rest is staked;
  - **15% goes to NXD stakers**.

## A compounding loop

Because NXD re-stakes part of its income as DXN, its share $\varphi$ of all staked DXN grows like a logistic curve:

$$
\frac{d\varphi}{dt} = y \, \rho_N \, \varphi \, (1 - \varphi)
$$

- $y$ = daily fee yield of staked DXN;
- $\rho_N$ = share of NXD's income that ends up re-staked as DXN (to read from the contract).

NXD keeps taking a larger share of DBXen fees over time. This matters for the Granary: see [Storage and routing](../granary/storage-and-routing.md).

## Useful reads

`HandleRewards(ethReceived, dxnAmountReceived, dxnBurned, dxnToStake, nxdBurned, ethToStakingVault)`; NXD transfers to the dead address.
