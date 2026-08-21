# Constraints, Assumptions, and Limitations

## Boundary conditions (model scope)
- **Voltage levels**: three coordinated levels only — 220 kV, 110 kV, 10 kV. DC feeders and other levels are out of scope (flagged as future work).
- **110 kV topology**: two interconnection architectures — loop network and '3T' breakout; radial dual-supply enforced (each load point served by exactly two independent paths, no inadvertent loops).
- **10 kV topology**: (n+1) redundancy (n main feeders + 1 standby); N-1 security enforced.
- **Operational limits (case study)**: max substation loading factor η = 75%; max safe operating current 552 A (10 kV feeders), 718 A (110 kV lines); discount rate 8%.
- **Planning horizons**: rolling optimization across 2020 (base) → 2025 → 2035.
- **Objective**: minimize total per-horizon construction + operating cost (does not directly optimize reliability, resilience, or losses beyond the 10 kV loss-conversion term).

## Enforced physical constraints (Eqs. 13–25)
- 110 kV substation loading ≤ rated capacity × η × cosφ (Eqs. 13–15).
- 10 kV primary feeder capacity limit (Eq. 16).
- 110 kV routing / radial dual-supply / anti-loop (Eqs. 17–21).
- 110 kV line loading at critical end sections 1a, 2k (Eqs. 22–23).
- 220 kV substation loading (Eqs. 24–25).
- Constraint enforcement in the GA is soft: infeasible candidates get a large penalty cost rather than hard rejection.

## Assumptions
- A1: The five indices capture substation criticality; no additional factors (e.g., reliability, DC integration) are included (acknowledged limitation).
- A2: AHP pairwise weights (single elicited matrix, CR = 0.00726) faithfully represent planner preferences; no sensitivity analysis over alternative weightings is reported.
- A3: Minimizing per-horizon total cost yields realistic grid evolution; the automatic reconfiguration produces schemes matching real expansion patterns.
- A4: A one-horizon deferral (2020→2025) is a representative delay; other delay durations/patterns not tested.
- A5: The single regional grid (220 nodes, six new 110 kV substations) suffices to validate the score–cost relationship.
- A6: Reactive loads are neglected for the 110 kV line-loading constraints (stated at Eq. 22–23).

## Known limitations
- **Single case, small candidate set**: the score–cost regression rests on six data points from one grid; generality is asserted, not established.
- **Not strictly monotonic**: the highest incremental cost (substation 5, 4.24%) does not correspond to the highest score (substation 1, 0.2035; 3.95%) — the relationship is a strong trend with local violations.
- **"Superior accuracy vs conventional approaches"** (abstract) is not backed by a head-to-head baseline comparison in the paper — no competing method is quantitatively evaluated. (Gap.)
- **Unspecified economic/physical parameters**: per-unit line costs, depreciation lives, zigzag/network-loss coefficients, power factor are only symbolic; absolute costs cannot be reproduced.
- **Data availability**: the underlying dataset is classified and cannot be released (Data Availability Statement), preventing external replication.
- **Weighting subjectivity**: AHP weights depend on expert judgment; no objective/data-driven cross-check (e.g., entropy) is performed despite citing such methods [18].
- **Delay direction**: only delayed (not premature) commissioning is simulated, though both are motivated in §1.
