# Experiments

## E01: Year-Long Sequential DAM-ASM Simulation on NREL-118 System
- **Verifies**: C01
- **Evidence**: evidence/tables/table1.md through evidence/tables/table8.md; evidence/figures/figure1.md through evidence/figures/figure19.md
- **Run**: NCUCER MILP solved daily for 366 days (leap year); Python/Pyomo/Gurobi; DIgSILENT PowerFactory for DCLF
- **Setup**:
  - System: NREL 118-Bus, 327 units (40.5 GW), 89 DT, 15 DH
  - Horizon: 8784 h (366 days × 24 h)
  - ASM optimization: daily MILP with 24 h horizon
- **Procedure**:
  1. Solve DAM for each daily time step (zonal LP, no UC)
  2. Perform bid adjustment (5-case logic) based on DAM schedules
  3. Run DCLF + PTDF computation (PowerFactory)
  4. Solve NCUCER ASM MILP for the full day
  5. Enforce MUT/MDT continuity between days (Algorithms 1–2)
- **Metrics**: Yearly TSO disbursement, RES curtailment, load shedding, SRR compliance, branch overload resolution
- **Expected outcome**: All network overloads resolved, SRR met year-round, zero curtailment/shedding, feasible unit states every day.
- **Baselines**: None (operational run)
- **Dependencies**: none

## E02: Bid Adjustment Case Validation per Technology
- **Verifies**: C01, C02
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure3.md
- **Run**: Analysis of yearly SU/SD occurrences from ASM solution
- **Setup**:
  - 89 DT units across 5 technology groups (CC NG, CT NG, CT Oil, Geo, ST NG)
  - Bid adjustment cases (a)–(e) per Figure 3
- **Procedure**:
  1. Aggregate ASM yearly results by technology
  2. Count occurrences of constraint (31) activation (unit below P^min, forced SU or SD)
  3. Count total SU and SD clearances per technology
- **Metrics**: SU/SD occurrence counts, constraint (31) activation frequency, technology breakdown
- **Expected outcome**: CC NG shows most SU because it is the most frequent marginal technology; ST NG shows more SD than SU due to higher costs.
- **Baselines**: None
- **Dependencies**: E01

## E03: USC/DSM Adequacy and SRR Compliance
- **Verifies**: C01, C04, C05
- **Evidence**: evidence/figures/figure10.md; evidence/tables/table5.md
- **Run**: Analysis of ASM USM/DSM before and after redispatch
- **Setup**:
  - USM/DSM computed after DAM and after ASM
  - SRR values from 94.4 MW to 302.5 MW
- **Procedure**:
  1. Compute USM after DAM = sum(min(SRH, upward margin)) for cleared DT units
  2. Compute USM after ASM similarly
  3. Identify hours where DAM USM < SRR
  4. Verify ASM resolves deficiency
- **Metrics**: USM deficit hours (741), technology contributing to SU/DR resolution
- **Expected outcome**: DSM always sufficient; USM deficient for 741 h; ASM resolves all via SU and DR clearance.
- **Baselines**: Baseline DAM-only case
- **Dependencies**: E01

## E04: Technology Contribution to ASM Service Provision
- **Verifies**: C04
- **Evidence**: evidence/figures/figure9.md; evidence/tables/table5.md
- **Run**: Yearly ASM results breakdown by technology
- **Setup**:
  - Services: UR, DR, SU, SD, SRU, SRD
  - Technologies: CC NG, CT NG, CT Oil, ST NG, DH, Geo
- **Procedure**:
  1. Aggregate yearly MWh of each service per technology from NCUCER results
  2. Rank technologies by contribution to each service
- **Metrics**: Relative contribution (%) of each technology to each service
- **Expected outcome**: CC NG is most used overall; DH provides UR and DR; CT NG provides SRU; ST NG provides SU/SD.
- **Baselines**: None
- **Dependencies**: E01

## E05: Sensitivity Analysis on Bid Factors and DH Strategy
- **Verifies**: C06, C07
- **Evidence**: evidence/tables/table6.md, evidence/tables/table7.md; evidence/figures/figure15.md, evidence/figures/figure16.md
- **Run**: Two sensitivity sets on base case
- **Setup**:
  - Bid factors: narrower prices (selling +10%, buying −10%) and larger prices (opposite)
  - DH allocation: 85% DAM (vs 90% base)
- **Procedure**:
  1. Re-run yearly simulation with modified parameters
  2. Compare ASM service quantities and costs (Table 6 for bid factors, Figure 15/16 for DH strategy)
  3. Compare DAM zonal prices for DH sensitivity (Table 7)
- **Metrics**: Service quantity variation (%), cost variation (%), zonal price variation, overload occurrence change
- **Expected outcome**: UR inelastic; DR/SU/SD elastic. DH strategy change increases costs by ~$1.72M.
- **Baselines**: Base case (90% DH allocation, nominal bid factors)
- **Dependencies**: E01

## E06: Benchmark Comparison with DAM-UC-Reserve Model
- **Verifies**: C03
- **Evidence**: evidence/tables/table8.md; evidence/figures/figure17.md, evidence/figures/figure18.md, evidence/figures/figure19.md
- **Run**: Benchmark DAM model with UC and reserve (Appendix A) vs proposed sequential approach
- **Setup**:
  - Benchmark: zonal market with MUT/MDT and SR constraints per [32,33]
  - Same NREL-118 system, yearly horizon
  - Benchmark excludes forecast updates and nodal redispatch
- **Procedure**:
  1. Run benchmark DAM-UC-Reserve yearly simulation
  2. Compare zonal prices, dispatched energy, and SU/SD/SRU/SRD costs
  3. Compare total cost (energy + services)
  4. Evaluate residual overloads after benchmark DAM via DCLF
- **Metrics**: Zonal prices, total cost, dispatched energy variation, service cost variation, branch overloads
- **Expected outcome**: Proposed approach yields 5.6× lower total cost ($3.49B vs $19.50B). Benchmark has 2–6× higher zonal prices.
- **Baselines**: Proposed sequential approach (base case from E01)
- **Dependencies**: E01
