# Experiments

Directional plans only — exact numbers live in `evidence/`.

## E01: Chaotic-map selection study for GWO initialization
- **Verifies**: C03, C04
- **Evidence**: evidence/tables/table4.md; evidence/figures/figure6.md
- **Run**: Not released as code (no public repo/log); reconstructed method in `logic/solution/algorithm.md` and `src/environment.md`. Author-run MATLAB-style simulation implied by runtimes in Table 4.
- **Setup**:
  - Model: GWO seeded by each of four chaotic maps (Tent, Sine, Chebyshev, Logistic), plus uniform-random traditional GWO
  - Hardware: Not specified in paper
  - Dataset: One MGC economic-dispatch instance — 3 microgrids, 24 hourly intervals, low-latitude coastal forecast (ECMWF meteorology + historical wind/solar/load)
  - System: Fitness = MGC objective (Eq. 8) with penalty terms
- **Procedure**:
  1. Replace GWO's uniform-random initial population with a chaotic sequence from each map (Table 3).
  2. Run each CGWO variant and traditional GWO on the same dispatch instance.
  3. Record convergence curves, final optimal fitness value, and runtime.
  4. Compare early-vs-late convergence behaviour and the accuracy/runtime trade-off; select a map.
- **Metrics**: Optimal fitness value (objective units); runtime (s); qualitative convergence speed/precision.
- **Expected outcome**:
  - Chaotic maps differ markedly in early convergence speed; one map converges fastest early, another reaches the most accurate final value.
  - The most-accurate map is not the fastest in runtime; when the accuracy gap is negligible the faster map is chosen.
- **Baselines**: Traditional (uniform-random) GWO.
- **Dependencies**: none

## E02: CDGWO vs. common intelligent optimization algorithms
- **Verifies**: C02, C04, C05, C06
- **Evidence**: evidence/tables/table5.md; evidence/figures/figure7.md
- **Run**: Not released as code; author-run simulation (runtimes/variance reported in Table 5).
- **Setup**:
  - Model: CDGWO (chosen chaotic map + dynamic opposition-based learning) vs FA, PSO, WOA, GWO, GA, SA
  - Hardware: Not specified in paper
  - Dataset: Same MGC dispatch instance as E01
  - System: Multiple runs per algorithm (convergence variance computed over runs, Eq. 21)
- **Procedure**:
  1. Apply each algorithm to the MGC economic-dispatch problem.
  2. Record optimal fitness value, runtime, iterations-to-convergence, and convergence variance over repeated runs.
  3. Compare convergence curves jointly with the tabulated indicators.
- **Metrics**: Optimal fitness value; runtime (s); number of iterations at convergence; convergence variance (Eq. 21).
- **Expected outcome**:
  - The proposed method reaches the best fitness with the shortest runtime and the lowest convergence variance.
  - Fewest-iterations-to-converge (a different algorithm) does not coincide with best runtime or best fitness.
- **Baselines**: FA, PSO, WOA, GWO, GA, SA.
- **Dependencies**: E01

## E03: Actual daily operating cost per algorithm
- **Verifies**: C01, C06
- **Evidence**: evidence/tables/tableA1.md
- **Run**: Not released as code; cost post-computed from each algorithm's dispatch solution.
- **Setup**:
  - Model: Dispatch solution from each of FA, PSO, WOA, GWO, CDGWO
  - Hardware: Not specified in paper
  - Dataset: Nominal MGC instance
  - System: Actual daily cost computed without penalty terms (distinct from fitness value)
- **Procedure**:
  1. Take each algorithm's optimized dispatch schedule.
  2. Compute the real daily monetary cost (operational + pollution + ESS loss), excluding penalty terms.
  3. Compare the actual-cost ranking against the fitness ranking from E02.
- **Metrics**: Actual daily cost (CNY).
- **Expected outcome**:
  - Fitness value and actual cost are not numerically equal (penalty decoupling).
  - The best-fitness algorithm also yields the lowest actual daily cost (ranking preserved).
- **Baselines**: FA, PSO, WOA, GWO.
- **Dependencies**: E02

## E04: Nominal economic dispatch of the MGC with CDGWO
- **Verifies**: C01, C07, C08
- **Evidence**: evidence/figures/figure8.md; evidence/figures/figure9.md; evidence/figures/figure10.md; evidence/tables/tableA2.md; evidence/tables/tableA4.md; evidence/figures/figure5.md
- **Run**: Not released as code; author-run CDGWO dispatch under nominal forecast.
- **Setup**:
  - Model: CDGWO solving the full penalized MGC dispatch model
  - Hardware: Not specified in paper
  - Dataset: Nominal typical-day forecast (wind/solar/load) for the coastal region; TOU tariff (Figure 5)
  - System: 3 MGs, 24 intervals, SOC ∈ [30%, 90%]
- **Procedure**:
  1. Solve the dispatch model under nominal inputs.
  2. Extract per-MG hourly power-balance schedules (PV/WT/ESS/MT-DG/exchange/grid).
  3. Tabulate per-MG grid purchase/sale and inter-MG exchange totals and per-MG costs.
  4. Inspect timing of purchases/sales/ESS cycling against the TOU price curve.
- **Metrics**: Per-hour power (kW) by source; per-MG grid purchase/sale and exchange totals (kW); per-MG operational/pollution/ESS-loss cost (CNY).
- **Expected outcome**:
  - Hourly supply + import exactly meets load in each MG (feasible balance).
  - Purchases concentrate in low-price hours; selling/discharging concentrate in high-price hours; ESS performs peak-shaving/valley-filling.
- **Baselines**: none (analysis of the proposed method's solution).
- **Dependencies**: E02

## E05: Robustness under ±10% random disturbance
- **Verifies**: C09
- **Evidence**: evidence/tables/tableA3.md; evidence/tables/tableA5.md; evidence/figures/figure8.md; evidence/figures/figure9.md; evidence/figures/figure10.md
- **Run**: Not released as code; author-run CDGWO dispatch under disturbed forecast.
- **Setup**:
  - Model: CDGWO solving the dispatch model with disturbed inputs
  - Hardware: Not specified in paper
  - Dataset: Nominal forecast with a ±10% random disturbance added to MG1 wind, MG2 PV, and MG3 load
  - System: Same as E04
- **Procedure**:
  1. Inject a ±10% random disturbance into the three specified quantities.
  2. Re-solve the dispatch model.
  3. Compare per-MG power balance, purchase/sale totals, and per-category costs against the nominal case.
- **Metrics**: Per-MG purchase/sale/exchange totals (kW); per-category and total cost (CNY); hourly power-balance satisfaction.
- **Expected outcome**:
  - Power balance is preserved at every hour under disturbance.
  - Operational, pollution, and total costs rise modestly relative to nominal; system performance stays stable.
- **Baselines**: The nominal-condition solution from E04.
- **Dependencies**: E04
