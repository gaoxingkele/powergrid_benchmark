# Experiments

## E01: 33-Bus DG and EVCS Integration Analysis
- **Verifies**: C02, C04
- **Evidence**: [Table 2](evidence/tables/table2.md), [Figure 7](evidence/figures/figure7.md)
- **Run**: The paper reports this as simulation performed in MATLAB 2022b on an Intel Core i7 3.2 GHz 8th gen with 16 GB RAM. No source code file is provided in the paper.
- **Setup**:
  - System: IEEE 33-bus radial distribution network, 12.66 kV, 10 MVA base
  - Components: 2 DGs, 2 EVCSs (no CBs)
  - EV hosting factors: 30%, 40%, 50% of total load
  - DG operation: Unity power factor
  - Objective: Minimize Ft (weighted sum of losses, VDI, cost savings, inverse CO2 reduction)
- **Procedure**:
  1. Run base-case power flow to capture initial losses and voltage profile
  2. Classify branches by active power demand
  3. Place EVCSs on high-load branches, split EV load between two stations
  4. Place DGs on high-active-power branches, size to match branch demand
  5. Iteratively adjust sizes to minimize Ft under thermal and voltage constraints
  6. Record PLoss, QLoss, Vmin, VDI, Slack PF for each hosting factor
- **Metrics**: PLoss (kW), QLoss (kVAR), Vmin (p.u.), VDI, Slack PF
- **Expected outcome**:
  - Active power loss reduction relative to base case (210.99 kW) across all hosting factors
  - Minimum voltage improvement from 0.9038 p.u. toward 0.97 p.u.
  - Substation power factor degradation below base case (0.849) due to inductive EV load without reactive compensation
  - Higher EV hosting factors result in marginally higher losses and lower minimum voltages
- **Baselines**: Base case (no DGs, no EVCSs)
- **Dependencies**: none

## E02: 33-Bus Combined DG, CB, and EVCS Integration Analysis
- **Verifies**: C02, C04
- **Evidence**: [Table 3](evidence/tables/table3.md), [Figure 8](evidence/figures/figure8.md), [Table 6](evidence/tables/table6.md)
- **Run**: The paper reports this as simulation performed in MATLAB 2022b on an Intel Core i7 3.2 GHz 8th gen with 16 GB RAM. No source code file is provided in the paper.
- **Setup**:
  - System: IEEE 33-bus radial distribution network, 12.66 kV, 10 MVA base
  - Components: 2 DGs, 2 CBs, 2 EVCSs
  - EV hosting factors: 30%, 40%, 50%
  - DG operation: Unity power factor
  - CB placement on buses classified by reactive power demand
- **Procedure**:
  1. Run base-case power flow
  2. Classify branches by active power demand (DG, EVCS) and reactive power demand (CB)
  3. Place EVCSs then DGs then CBs sequentially on highest-demand branches
  4. Iteratively adjust sizes to minimize Ft under thermal and voltage constraints
  5. Record PLoss, QLoss, Vmin, VDI, Slack PF for each hosting factor
  6. Compute economic and environmental metrics: delta QCO2, CDG+CCB, Csaved energy, payback period
- **Metrics**: PLoss (kW), QLoss (kVAR), Vmin (p.u.), VDI, Slack PF, delta QCO2 (ton/year), CDG+CCB (USD), Csaved energy (USD/year), payback period (year)
- **Expected outcome**:
  - Substantially greater loss reduction than E01 (DG+EVCS only) due to reactive compensation
  - Minimum voltage above 0.98 p.u. across all hosting factors
  - Substation power factor recovery above 0.90
  - VDI reduction by an order of magnitude compared to E01
  - Non-prohibitive payback periods (around 10-12 years)
- **Baselines**: Base case, E01 results
- **Dependencies**: E01

## E03: 69-Bus Combined DG, CB, and EVCS Integration Analysis
- **Verifies**: C02, C04
- **Evidence**: [Table 4](evidence/tables/table4.md), [Table 5](evidence/tables/table5.md), [Table 7](evidence/tables/table7.md), [Figure 10](evidence/figures/figure10.md), [Figure 11](evidence/figures/figure11.md)
- **Run**: The paper reports this as simulation performed in MATLAB 2022b on an Intel Core i7 3.2 GHz 8th gen with 16 GB RAM. No source code file is provided in the paper.
- **Setup**:
  - System: IEEE 69-bus radial distribution network, 12.66 kV, 10 MVA base
  - Components: 2 DGs, 2 CBs, 2 EVCSs
  - EV hosting factors: 30%, 40%, 50%
  - Optimal placement on buses 21 and 61 (DGs, CBs, EVCSs)
- **Procedure**:
  1. Run base-case power flow for 69-bus system
  2. Classify branches by active and reactive power demand
  3. Place EVCSs, DGs, CBs sequentially on highest-demand branches
  4. Iteratively adjust sizes to minimize Ft under constraints
  5. Record technical performance metrics for each hosting factor
  6. Compute economic and environmental metrics
- **Metrics**: PLoss (kW), QLoss (kVAR), Vmin (p.u.), VDI, Slack PF, delta QCO2 (ton/year), CDG+CCB (USD), Csaved energy (USD/year), payback period (year)
- **Expected outcome**:
  - Greater loss reduction than 33-bus case due to more optimization headroom in larger network
  - Minimum voltage improvement above 0.99 p.u.
  - VDI below 0.1 x 10^-3, indicating remarkably flat voltage profile
  - Substation PF recovery to above 0.81
  - Shorter payback periods than 33-bus due to higher absolute energy savings
- **Baselines**: Base case, E02 results
- **Dependencies**: E01, E02

## E04: Comparative Benchmark Against PSO and GWO
- **Verifies**: C01, C03
- **Evidence**: [Table 8](evidence/tables/table8.md), [Table 9](evidence/tables/table9.md), [Table 10](evidence/tables/table10.md), [Table 11](evidence/tables/table11.md)
- **Run**: The paper reports this as simulation performed in MATLAB 2022b on an Intel Core i7 3.2 GHz 8th gen with 16 GB RAM. No source code file is provided in the paper.
- **Setup**:
  - Systems: IEEE 33-bus and IEEE 69-bus
  - EV hosting factor: 30% for all methods
  - Methods compared: PSO (100 iterations), GWO (100 iterations), CGO (18 iterations for 33-bus, 22 for 69-bus)
  - Same EVCS placement and sizing across all methods
  - Same component count: 2 DGs, 2 CBs, 2 EVCSs
- **Procedure**:
  1. Apply PSO to find optimal DG and CB sizing given fixed EVCS placement
  2. Apply GWO under identical conditions
  3. Apply CGO with classification-based search
  4. Record PLoss, QLoss, Vmin, VDI, Slack PF, Run time, Required iterations for all three methods
  5. Tabulate DG and CB sizing comparison
- **Metrics**: PLoss (kW), QLoss (kVAR), Vmin (p.u.), VDI, Slack PF, Run time (s), Required iterations, DG ratings (kW), CB ratings (kVAR)
- **Expected outcome**:
  - CGO achieves the lowest or near-lowest PLoss among all three methods
  - CGO runtime is lower than both PSO and GWO
  - CGO requires substantially fewer iterations than PSO/GWO
  - DG and CB ratings differ across methods but CGO ratings are within a reasonable range comparable to alternatives
  - VDI for CGO may be slightly higher than PSO but not significantly so
- **Baselines**: PSO, GWO
- **Dependencies**: E02, E03

## E05: Thermal Capacity Limit Validation
- **Verifies**: C04
- **Evidence**: [Figure 9](evidence/figures/figure9.md), [Figure 12](evidence/figures/figure12.md)
- **Run**: The paper reports this as simulation performed in MATLAB 2022b on an Intel Core i7 3.2 GHz 8th gen with 16 GB RAM. No source code file is provided in the paper.
- **Setup**:
  - Systems: IEEE 33-bus and IEEE 69-bus with combined DG, CB, EVCS integration
  - All three hosting factors (30%, 40%, 50%)
  - Branch thermal capacity limit Sij,max is computed per branch
- **Procedure**:
  1. For each optimized solution, compute apparent power flow Sij in each branch
  2. Compare Sij against Sij,max for each branch
  3. Verify that |Sij| <= Sij,max holds for all branches
  4. Plot the comparison for visual validation
- **Metrics**: Sij (kVA), Sij,max (kVA) per branch
- **Expected outcome**:
  - All branches carry power flow below their thermal capacity limits for all hosting factors
  - No branch overloading occurs despite high EV penetration
  - The margin between Sij and Sij,max may decrease at higher hosting factors
- **Baselines**: Thermal capacity limit line on the plot
- **Dependencies**: E02, E03
