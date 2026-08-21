# Experiments

All experiments use the same park-level IES numerical case (typical day in northern China) and share the bi-level solver (improved PSO for the upper level, CPLEX 12.10 for the lower level). Exact numbers live in evidence/; only directional expectations appear here.

## E01: Single-objective vs multi-objective upper-level dispatch (Scenario 1 vs 2)
- **Verifies**: C01, C06
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure8.md
- **Run**: Scenario 1 (economic objective only) and Scenario 2 (economy + flexibility) of the upper-level model; solver per src/environment.md and logic/solution/algorithm.md.
- **Setup**:
  - Model: Bi-level IES dispatch; upper level via improved PSO, lower level via CPLEX
  - Hardware: Not specified in paper (CPLEX 12.10 software)
  - Dataset: Typical-day WT/PV and electric/heat/cooling load curves (Figure 4, ref [30]); device parameters Table 1; TOU prices Table 3
  - System: Lower level = aggregator only (no EVs); no carbon/GCT trading
- **Procedure**:
  1. Solve Scenario 1 (maximize operator revenue only)
  2. Solve Scenario 2 (add the weighted flexibility objective F2)
  3. Compare operator revenue and the four flexibility indices
- **Metrics**: Operator revenue (yuan); electrical/thermal/cooling/system flexibility indices (dimensionless)
- **Expected outcome**:
  - Multi-objective dispatch yields lower operator revenue but higher system flexibility than single-objective
  - The electrical carrier shows the largest relative flexibility headroom
- **Baselines**: Scenario 1 (single-objective economic dispatch)
- **Dependencies**: none

## E02: User-aggregator cost stability across all scenarios
- **Verifies**: C02
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure9.md; evidence/figures/figure10.md; evidence/figures/figure11.md; evidence/figures/figure12.md
- **Run**: Read out user-aggregator total cost, energy-purchase cost, and demand-response cost across Scenarios 1–5; inspect DR power profiles and prices.
- **Setup**:
  - Model: Lower-level aggregator model (min total cost, Eq. 21–25)
  - Hardware: Not specified in paper
  - Dataset: TOU prices Table 3; DR compensation prices Table 2
  - System: Aggregator with transferable/curtailable/substitutable loads
- **Procedure**:
  1. For each of the 5 scenarios, record aggregator total cost and its split (purchase vs DR)
  2. Compare the spread of total cost against the spread of operator-side cost
  3. Examine DR reallocation between adjacent scenarios (e.g. 3 vs 5)
- **Metrics**: Aggregator total cost, energy-purchase cost, DR compensation cost (yuan); DR power by type (kW)
- **Expected outcome**:
  - Aggregator total cost varies over a much narrower band than operator cost
  - DR expenditure rises to offset energy-price-driven cost increases
- **Baselines**: Cross-scenario comparison (internal)
- **Dependencies**: E01

## E03: EV enrollment as a flexibility resource (Scenario 2 vs 3)
- **Verifies**: C03, C06
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure8.md; evidence/figures/figure13.md; evidence/figures/figure14.md
- **Run**: Scenario 3 adds EV clusters to Scenario 2's lower level; compare cost, profit, and flexibility, and inspect the temporal EV charge/discharge and flexibility profiles.
- **Setup**:
  - Model: Lower-level EV cluster model (Eq. 17–20) coupled to the upper level
  - Hardware: Not specified in paper
  - Dataset: EV parameters Table 4 (5 categories)
  - System: Aggregator + EV clusters
- **Procedure**:
  1. Solve Scenario 2 (no EV) and Scenario 3 (with EV)
  2. Compare operating cost, operator profit, and electrical flexibility
  3. Plot the Scenario-5 vs Scenario-2 flexibility gap over the day and relate it to EV connection windows
- **Metrics**: Operating cost, operator profit (yuan); electrical flexibility index; EV charge/discharge power (kW) and price (yuan/kWh) by hour
- **Expected outcome**:
  - The added operating cost of EVs is repaid by a larger operator-profit gain
  - Electrical flexibility improves, with the improvement concentrated in EV grid-connection hours
- **Baselines**: Scenario 2 (no EVs)
- **Dependencies**: E01

## E04: Carbon and green-certificate mechanism ablation (Scenario 3 → 4 → 5)
- **Verifies**: C04, C05
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure6.md
- **Run**: Add carbon trading (Scenario 4) then green-certificate trading (Scenario 5) on top of Scenario 3; compare emissions, operator profit, and trading costs.
- **Setup**:
  - Model: Operator objective with GCT-CET terms (Eq. 7–10)
  - Hardware: Not specified in paper
  - Dataset: Carbon/GCT coefficients from ref [29] (values unspecified)
  - System: Full IES with EVs
- **Procedure**:
  1. Solve Scenario 3 (no carbon/GCT), Scenario 4 (+carbon), Scenario 5 (+green certificate)
  2. Compare system carbon emissions, operator profit, carbon-trading cost, GCT cost across the three
  3. Inspect device-level reallocation (gas turbine vs electric boiler) behind the emission cut
- **Metrics**: System carbon emissions (kg); operator profit; carbon-trading cost; green-certificate cost (yuan)
- **Expected outcome**:
  - Carbon trading lowers emissions but also lowers operator profit (trade-off)
  - Green-certificate trading lowers emissions further AND reduces carbon-trading cost (complementary)
- **Baselines**: Scenario 3 (no mechanisms), Scenario 4 (carbon only)
- **Dependencies**: E03

## E05: EV fleet-composition sensitivity for time-targeted flexibility
- **Verifies**: C07
- **Evidence**: evidence/figures/figure15.md; evidence/figures/figure8.md
- **Run**: Re-solve Scenario 5 with EV category proportions reweighted toward categories connected at 12:00; compare the hourly electrical-flexibility profile to the original.
- **Setup**:
  - Model: Scenario 5 with modified EV proportions
  - Hardware: Not specified in paper
  - Dataset: EV proportions changed from Table 4 baseline to the §4.2.4 set
  - System: Full IES with EVs
- **Procedure**:
  1. Identify the deficit hour (flexibility minimum ~12:00) from Figure 8
  2. Reweight EV category proportions toward categories present at that hour
  3. Re-solve and compare the flexibility at the targeted hour
- **Metrics**: Electrical flexibility index at 12:00 (dimensionless), hourly flexibility profile
- **Expected outcome**:
  - Flexibility at the targeted hour rises after reweighting; overall profile otherwise similar
- **Baselines**: Scenario 5 with baseline Table 4 proportions
- **Dependencies**: E03

## E06: Carbon-price sensitivity sweep
- **Verifies**: C08
- **Evidence**: evidence/tables/table6.md
- **Run**: Scale the carbon base price to 1.0×, 1.05×, 1.1× in Scenario 5, all else fixed; record emissions and operator revenue.
- **Setup**:
  - Model: Scenario 5
  - Hardware: Not specified in paper
  - Dataset: Same case; carbon base price scaled
  - System: Full IES
- **Procedure**:
  1. Solve Scenario 5 at each carbon-price multiple
  2. Record system carbon emissions and operator revenue
  3. Check monotonicity of both across the sweep
- **Metrics**: System carbon emissions (t); operator revenue (yuan)
- **Expected outcome**:
  - Higher carbon price → monotonically lower emissions and monotonically lower revenue
- **Baselines**: 1.0× base price
- **Dependencies**: E04

## E07: Solver comparison — improved PSO vs PSO vs DBO
- **Verifies**: C09
- **Evidence**: evidence/tables/table7.md; evidence/figures/figure16.md
- **Run**: Solve the Scenario-5 upper-level model with PSO, DBO, and improved PSO; track TOPSIS closeness vs iteration and run 30 independent trials each.
- **Setup**:
  - Model: Upper-level multi-objective model of Scenario 5
  - Hardware: Not specified in paper (runtime reported in seconds)
  - Dataset: Same case
  - System: Population 50, 200 max iterations, 30 independent runs
- **Procedure**:
  1. Run each algorithm on the same upper-level problem
  2. Record iterations-to-convergence and TOPSIS closeness at convergence
  3. Over 30 runs, compute maximum, mean, variance of closeness, and runtime
- **Metrics**: Iterations to convergence; TOPSIS closeness to ideal solution; closeness max/mean/variance; runtime (s)
- **Expected outcome**:
  - Improved PSO converges in fewer iterations, to higher closeness, with lower variance and lower runtime than PSO and DBO
- **Baselines**: PSO, DBO
- **Dependencies**: none
