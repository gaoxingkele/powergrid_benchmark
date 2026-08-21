# Experiments

## E01: Scenario 1 — Normal IES operation (PV + wind available)
- **Verifies**: [C01, C02]
- **Evidence**: [figures/figure5.md](evidence/figures/figure5.md), [figures/figure6.md](evidence/figures/figure6.md), [figures/figure7.md](evidence/figures/figure7.md), [figures/figure8.md](evidence/figures/figure8.md), [tables/table1.md](evidence/tables/table1.md) (Scenario 1 columns)
- **Run**: Case study using the IGA algorithm defined in Section 3, with IES parameters from Section 4.1
- **Setup**:
  - IES configuration: CHP (ηCHP=0.9, 50-250 kW electric, 125 kW thermal max), GB (ηGB=0.85, 150 kW max), WHU (ηWHU=0.6), ESS (200 kWh, 30 kW max charge/discharge, 50% initial SOC)
  - Renewable: PV and wind generation operating normally
  - Pricing: tiered electricity (E0=175 kWh, 120% surcharge), tiered natural gas (V0=50 m3, 120% surcharge), tiered carbon (e1=5000, e2=6000, e3=6500 m3; 0.2/0.3/0.4 CNY/m3)
  - Grid: LMP-based electricity pricing, cgas_t = 2.5 CNY/m3
  - Algorithm: IGA with population initialization (Eq. 31), binary tournament parent selection (Section 3.2), cyclic crossover (Section 3.3), polynomial mutation (Section 3.4, βmin_m=1), fast non-dominated sorting (Section 3.6), weight-based Pareto selection (w1=w2=1)
  - Hardware: Not specified in paper
- **Procedure**:
  1. Initialize population of decision variables within boundary limits
  2. Evaluate objective functions (Eq. 26-27) and constraint violations for each individual
  3. Apply constraint-prioritizing binary tournament selection
  4. Generate offspring via cyclic crossover and polynomial mutation
  5. Evaluate offspring and select between parents and offspring (Section 3.5)
  6. Perform fast non-dominated sorting and crowding distance calculation
  7. Select Pareto front solutions and apply weight-based selection (Eq. 37)
  8. Continue until maximum generation count is reached
- **Metrics**: o1 (total operating cost, CNY), o2 (total carbon emissions, m3), V (maximum constraint violation, kW)
- **Expected outcome**:
  - IGA achieves lower constraint violations than penalty-function-based methods (MPSO, MABC)
  - The IES operator reduces electricity purchases during peak hours
  - ESS charges during low-price periods and discharges during high-price periods
  - Constraint violations remain within a small fraction of the load magnitude
- **Baselines**: MGA, MPSO, SGA, MABC (all evaluated on Scenario 1)
- **Dependencies**: none

## E02: Scenario 2 — PV outage with high electricity prices
- **Verifies**: [C03]
- **Evidence**: [figures/figure9.md](evidence/figures/figure9.md), [figures/figure10.md](evidence/figures/figure10.md), [figures/figure11.md](evidence/figures/figure11.md), [figures/figure12.md](evidence/figures/figure12.md), [tables/table1.md](evidence/tables/table1.md) (Scenario 2 columns)
- **Run**: Same IGA algorithm as E01, applied to modified load curves and rainy-day conditions (PV inoperable, higher electricity prices)
- **Setup**:
  - Same IES component parameters as E01
  - Modified: electrical and heat load curves (different from Scenario 1)
  - PV system inoperable due to rainy weather — power shortage condition
  - Higher-than-usual electricity prices
  - Same algorithm parameters as E01
- **Procedure**:
  1. Same evolutionary procedure as E01
  2. The algorithm must compensate for absent PV generation by adjusting CHP output, gas boiler operation, and grid purchases
- **Metrics**: o1 (total operating cost, CNY), o2 (total carbon emissions, m3), V (maximum constraint violation, kW)
- **Expected outcome**:
  - IGA maintains constraint violations below 0.3 kW despite the challenging conditions
  - The system avoids electricity purchases during peak price hours
  - Wind energy is efficiently utilized (no curtailment)
  - Stable electricity and heat supply is maintained
- **Baselines**: MGA, MPSO, SGA, MABC (all evaluated on Scenario 2)
- **Dependencies**: [E01]

## E03: Scenario 3 — PV outage with normal prices
- **Verifies**: [C03]
- **Evidence**: [figures/figure13.md](evidence/figures/figure13.md), [figures/figure14.md](evidence/figures/figure14.md), [figures/figure15.md](evidence/figures/figure15.md), [figures/figure16.md](evidence/figures/figure16.md), [tables/table1.md](evidence/tables/table1.md) (Scenario 3 columns)
- **Run**: Same IGA algorithm, with identical electricity load, heat load, and electricity price profiles as Scenario 1, but rainy weather makes PV inoperable
- **Setup**:
  - Same IES component parameters as E01
  - Same load and price profiles as Scenario 1
  - PV system inoperable (identical to Scenario 2 for PV, but otherwise same as Scenario 1)
  - Same algorithm parameters as E01
- **Procedure**:
  1. Same evolutionary procedure as E01
  2. The algorithm compensates for absent PV generation
  3. Reduced electricity purchases during peak price periods (15:00-17:00) by increasing CHP output
- **Metrics**: o1 (total operating cost, CNY), o2 (total carbon emissions, m3), V (maximum constraint violation, kW)
- **Expected outcome**:
  - IGA maintains all constraint violations within 0.3 kW
  - CHP output increases to meet electrical load demand during peak periods
  - The ESS returns to 50% SOC by the scheduling period's end
- **Baselines**: MGA, MPSO, SGA, MABC (all evaluated on Scenario 3)
- **Dependencies**: [E01]

## E04: Comparative evaluation — equality constraint handling
- **Verifies**: [C03, C05]
- **Evidence**: [tables/table1.md](evidence/tables/table1.md), [figures/figure8.md](evidence/figures/figure8.md), [figures/figure12.md](evidence/figures/figure12.md), [figures/figure16.md](evidence/figures/figure16.md)
- **Run**: Systematic comparison of IGA, MGA, MPSO, SGA, and MABC constraint violation results aggregated from E01, E02, E03
- **Setup**:
  - IGA, MGA, SGA: use the proposed constraint-prioritizing parent selection (Section 3.2, 3.5)
  - MPSO, MABC: use penalty function formulation (Eq. 38) with α1 = α2 = 1
  - All algorithms evaluated on identical IES problem instances
- **Procedure**:
  1. Run each algorithm on the three scenarios
  2. Record maximum constraint violation per algorithm per scenario
  3. Compare violations across algorithm groups (GA variants vs. penalty-function methods)
- **Metrics**: V (maximum equality constraint violation, kW) across all 49 constraints (24h electric + 24h thermal + initial SOC)
- **Expected outcome**:
  - All three GA variants (IGA, MGA, SGA) show constraint violations orders of magnitude lower than MPSO and MABC
  - The parent selection strategy is the common factor driving this gap
- **Baselines**: MGA, MPSO, SGA, MABC
- **Dependencies**: [E01, E02, E03]

## E05: Comparative evaluation — multi-objective performance
- **Verifies**: [C04, C05]
- **Evidence**: [tables/table1.md](evidence/tables/table1.md), [figures/figure17.md](evidence/figures/figure17.md)
- **Run**: Systematic comparison of IGA against four benchmarks (MGA, MPSO, SGA, MABC) across all three scenarios using operating cost (o1) and carbon emissions (o2) as metrics
- **Setup**:
  - Same IES problem instances as E01, E02, E03
  - Each algorithm runs to completion on each scenario
  - Single-objective SGA minimizes only operating cost (Eq. 26), with carbon cost included as part of operating cost
  - Multi-objective algorithms (IGA, MGA, MPSO, MABC) minimize both objectives (Eq. 26 and 27)
  - Weight-based selection (w1 = w2 = 1) applied to final Pareto front for multi-objective algorithms
- **Procedure**:
  1. Run each algorithm on each scenario
  2. Record o1 and o2 for the selected solution from each algorithm
  3. Compare IGA against each benchmark to quantify improvement
  4. Visualize Pareto front comparison (IGA vs MGA) for Scenario 1
- **Metrics**: o1 (total operating cost, CNY), o2 (total carbon emissions, m3)
- **Expected outcome**:
  - IGA achieves the lowest o1 and o2 values among all algorithms in all three scenarios
  - IGA's Pareto front dominates or lies to the lower-left of MGA's Pareto front
  - SGA (single-objective) achieves competitive o1 but higher o2 than multi-objective algorithms
- **Baselines**: MGA, MPSO, SGA, MABC
- **Dependencies**: [E01, E02, E03, E04]
