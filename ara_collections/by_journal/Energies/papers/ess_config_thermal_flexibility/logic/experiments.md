# Experiments

## E01: Three-scenario comparative economic analysis of ESS with and without TCL flexibility
- **Verifies**: C01, C03
- **Evidence**: [evidence/tables/table1.md](evidence/tables/table1.md), [evidence/figures/figure5.md](evidence/figures/figure5.md), [evidence/figures/figure6.md](evidence/figures/figure6.md)
- **Run**: Case study in Section 6.2 — the paper's main empirical validation
- **Setup**:
  - Model: Multi-objective ESS optimization model (Eq. 27), solved via POA-GWO-CSO
  - Hardware: Not specified in paper
  - Dataset: Typical summer day data from a selected region of Shanxi Province [26]; outdoor solar irradiance, ambient temperature (Figure 3), PV and wind maximum forecasted output, conventional load profile (Figure 4)
  - System: Distribution network with PV, wind, ESS, micro-gas turbines, and temperature-controlled building loads
  - ESS parameters: Lifetime 10.5 years, AC rated power 1.6 kW, AC EER 3.0
- **Procedure**:
  1. Define three scenarios: S1 (no ESS, no TCL flexibility), S2 (ESS configured, no TCL flexibility), S3 (ESS configured with TCL flexibility)
  2. Run the multi-objective optimization for each scenario
  3. Record annual load operating costs, ESS annual net income, and RE consumption rate for each scenario
  4. Compare results across scenarios
- **Metrics**: Load annual operating costs (CNY), ESS annual net income (CNY), RE consumption rate (%)
- **Expected outcome**: S3 achieves the lowest operating cost and highest ESS net income; S2 substantially improves over S1; S3 improves marginally over S2
- **Baselines**: S1 (no ESS), S2 (ESS without TCL flexibility)
- **Dependencies**: None

## E02: Algorithm convergence comparison (POA-GWO-CSO vs. component algorithms)
- **Verifies**: C02
- **Evidence**: [evidence/figures/figure9.md](evidence/figures/figure9.md)
- **Run**: Algorithm comparison in Section 6.2
- **Setup**:
  - Model: Same multi-objective ESS optimization model as E01
  - Hardware: Not specified in paper
  - Dataset: Same as E01 (Shanxi Province summer day)
  - System: Four methods compared: M1 = POA-GWO-CSO (proposed), M2 = standalone POA, M3 = standalone GWO, M4 = POA-GWO without CSO
- **Procedure**:
  1. Run each of the four algorithms on the same ESS optimization problem
  2. Record the scaled fitness value at each iteration (up to 500 iterations)
  3. Plot fitness value vs. iteration count for all four methods
  4. Compare convergence speed and final fitness value
- **Metrics**: Scaled fitness value (normalized), iteration count to convergence
- **Expected outcome**: Method 1 achieves higher fitness values than all other methods at every iteration count
- **Baselines**: Standalone POA, standalone GWO, POA-GWO without CSO
- **Dependencies**: E01 (uses the same problem formulation)

## E03: Qualitative analysis of pre-cooling behavior with and without TCL flexibility
- **Verifies**: C04
- **Evidence**: [evidence/figures/figure7.md](evidence/figures/figure7.md), [evidence/figures/figure8.md](evidence/figures/figure8.md)
- **Run**: Scenario 2 and Scenario 3 analysis in Section 6.2
- **Setup**:
  - Model: Same as E01
  - Hardware: Not specified in paper
  - Dataset: Same as E01
  - System: A single building's air conditioning system under Scenarios 2 (fixed setpoint) and 3 (comfort range)
- **Procedure**:
  1. Record air conditioning power consumption and indoor temperature over 24 hours for Scenario 2 (fixed indoor temperature setpoint)
  2. Record same quantities for Scenario 3 (temperature-controlled load flexibility with comfort range)
  3. Compare the operating patterns and temperature profiles
- **Metrics**: AC power (kW), indoor temperature (°C), electricity cost contribution from AC
- **Expected outcome**: Scenario 3 shows pre-cooling before peak tariff periods with corresponding temperature drops; Scenario 2 shows AC power tracking outdoor temperature
- **Baselines**: Scenario 2 (fixed setpoint, no flexibility)
- **Dependencies**: E01 (uses Scenarios 2 and 3 from the case study)
