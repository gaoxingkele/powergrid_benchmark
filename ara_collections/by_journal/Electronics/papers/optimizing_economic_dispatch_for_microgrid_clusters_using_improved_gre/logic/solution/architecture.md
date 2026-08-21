# MGC System Architecture

Mirrors Figure 1 (system structure) and Figure 4 (model construction/solution flow).

## Components (from Figure 1)
- **Main Grid** — external grid; buys from / sells to the cluster.
- **Energy Management Center (EMC)** — central coordinator; orchestrates inter-MG energy exchange and
  main-grid buy/sell transactions; communicates with all MGs and the main grid.
- **Microgrid 1 / 2 / 3** — three independent MGs on local buses. Each MG contains (drawn in detail
  for MG2): Photovoltaic (PV), Wind Turbine (WT), a dispatchable non-renewable unit, Energy Storage
  System (ESS), and AC Load. Each unit couples to its Local Bus via an AC/DC converter.
  - MG2's non-renewable unit = Microturbine (MT).
  - MG1 and MG3 are "essentially identical to MG2" except their non-renewable unit = Diesel
    Generator (DG).

## Connections
- **Power Flow** (solid arrows): Main Grid ↔ each MG; unit ↔ Local Bus; MG ↔ MG (inter-cluster
  exchange P_exi-j).
- **Communication Link** (dashed arrows): EMC ↔ Main Grid and EMC ↔ each MG.

## Method flow (from Figure 4)
```
[Chaos Optimization] + [Dynamic Opposition-based Learning]
        │ Improve
        ▼
[GWO Algorithm] ──► [Improved GWO (CDGWO)]
        │ Solving
        ▼
[Economic Dispatch Model]  ◄── defined by:
        ├─ MGC Structure (Main Grid, Transformer, MG1/2/3)
        ├─ Constraints of MGC (power balance; equipment self-constraints)
        └─ Objective Function (operation, environmental, ESS loss costs; penalty terms)
        │
        ▼
[Output]: power-balance scheduling result; various costs of the MGC system
```

## Design choices
- Central EMC coordination (vs. fully distributed) — chosen for optimal energy distribution and
  reliability.
- Heterogeneous non-renewable units (MT vs DG) across MGs — enables comparison of energy-source
  types within one cluster.
- Storage + inter-MG exchange as flexibility resources for peak-shaving/valley-filling and arbitrage.
