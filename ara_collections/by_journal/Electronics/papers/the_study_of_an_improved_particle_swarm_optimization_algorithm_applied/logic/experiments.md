# Experiments

Declarative verification plans reconstructed from the paper. Directional only; exact numbers live in `evidence/`.

## E01: Benchmark-function convergence test of SCMPSO
- **Verifies**: C01, C02
- **Evidence**: evidence/figures/figure5.md (per-function convergence), evidence/tables/table3.md (test parameters), evidence/figures/figure2.md, figure3.md, figure4.md (mechanism curves)
- **Run**: Not released as code; MATLAB 2020a implementation per Author Contributions. Procedure described in §4.2.5.
- **Setup**:
  - Model: SCMPSO optimizer
  - Hardware: Not specified in paper
  - Dataset: Five standard benchmark functions — Sum of Different Powers, Schwefel, Rastrigin, Rosenbrock, Levy
  - System: fixed population size, high-dimensional particles, and a fixed iteration budget (values in evidence/tables/table3.md and §4.2.5); per-function acceptance band and known optimum per Table 3
- **Procedure**:
  1. Configure each benchmark with the search domain and dimension of Table 3.
  2. Run SCMPSO for the fixed iteration budget.
  3. Record the objective ("Optimum") value vs iteration for each function.
  4. Check whether the value reaches the acceptance band and how fast.
- **Metrics**: convergence speed (iterations to acceptance band), final objective value, ability to escape local optima (unimodal vs multimodal functions)
- **Expected outcome**:
  - SCMPSO converges to the near-optimal acceptance band on all five functions within a small fraction of the budget.
  - It performs well on both unimodal (convergence-rate) and multimodal (local-optima-escape) benchmarks.
- **Baselines**: none (single-method characterization; comparison is E02)
- **Dependencies**: none

## E02: Comparative convergence of SCMPSO vs PSO/CPSO/QPSO
- **Verifies**: C01, C05
- **Evidence**: evidence/figures/figure6.md
- **Run**: MATLAB 2020a; §4.2.5, same-parameter comparison.
- **Setup**:
  - Model: SCMPSO vs traditional PSO, CPSO, QPSO
  - Hardware: Not specified in paper
  - Dataset: benchmark function(s) as in E01, under identical settings
  - System: identical population size, dimension, and iteration budget across all four algorithms (values in §4.2.5)
- **Procedure**:
  1. Run all four PSO variants under identical parameters.
  2. Overlay their objective-vs-iteration convergence curves.
  3. Compare descent speed and final settled value (including a zoomed view of late iterations).
  4. Note the iteration at which variants first approach the acceptance band, to justify the iteration budget.
- **Metrics**: convergence rate, final objective value, ranking of the four algorithms
- **Expected outcome**:
  - SCMPSO descends fastest and settles to the lowest final value; ordering SCMPSO best, then CPSO/QPSO, then PSO.
  - All variants approach the band well before the chosen budget, so the budget provides margin rather than accuracy.
- **Baselines**: PSO, CPSO, QPSO
- **Dependencies**: E01

## E03: 24-h microgrid dispatch simulation (case study)
- **Verifies**: C03
- **Evidence**: evidence/tables/table5.md (hourly dispatch), evidence/figures/figure13.md (power curves), figure14.md (grid exchange), figure8.md (topology), figures 9-12 (input profiles), table4.md (prices)
- **Run**: MATLAB 2020a; SCMPSO applied to the dispatch model of §3, procedure in §4.3 Steps 1-8.
- **Setup**:
  - Model: SCMPSO solving the economic-environmental dispatch (Min C_sun = C1 + C2)
  - Hardware: Not specified in paper
  - Dataset: typical summer day of a Jiangsu city — load, wind speed, temperature, irradiance profiles; time-of-use prices (Table 4); device parameters (Tables 1-2)
  - System: single-bus microgrid mixing multiple PV units, wind, one thermal generator, and storage units over a daily horizon at hourly resolution (device counts/ratings in evidence/tables/table1.md and §5.1)
- **Procedure**:
  1. Input load/price/weather/device data.
  2. Apply the merit-order scheduling strategy (renewables max, storage buffer, thermal slack, grid balance).
  3. Run SCMPSO to minimize total cost subject to all constraints.
  4. Extract hourly output of each source and the grid-interaction power.
  5. Classify the day into purchase / no-interaction / sale regimes.
- **Metrics**: hourly source outputs (kW), grid-interaction power (kW), regime classification, feasibility (power balance, limits)
- **Expected outcome**:
  - A feasible full-day dispatch where renewables are maximized, storage charges midday / discharges at night, thermal carries baseload, and the grid is bought-from at night and sold-to midday.
- **Baselines**: none (feasibility/behaviour demonstration)
- **Dependencies**: E01, E02

## E04: Cross-algorithm daily cost and emissions comparison
- **Verifies**: C04, C05
- **Evidence**: evidence/tables/table6.md (cost breakdown), evidence/tables/table7.md (emissions + treatment costs)
- **Run**: MATLAB 2020a; each of SCMPSO/CPSO/QPSO/PSO used to optimize the same dispatch model; §5.2.
- **Setup**:
  - Model: dispatch model solved by each of the four optimizers
  - Hardware: Not specified in paper
  - Dataset: same summer-day case as E03
  - System: identical microgrid and constraints across algorithms
- **Procedure**:
  1. Solve the dispatch with each algorithm.
  2. Record the daily cost breakdown (O&M, fuel, depreciation, grid interaction, environmental).
  3. Record pollutant emissions (CO2/SO2/NOX) and their treatment costs.
  4. Compare the four algorithms component-by-component.
- **Metrics**: per-component cost (RMB), pollutant emission mass (kg), treatment cost (RMB)
- **Expected outcome**:
  - The strongest optimizer yields the lowest O&M, fuel, depreciation, and environmental costs and the lowest emissions simultaneously; costs move together across the stack rather than trading off.
- **Baselines**: CPSO, QPSO, PSO (vs SCMPSO)
- **Dependencies**: E03

## E05: Iteration-budget adequacy analysis
- **Verifies**: C05
- **Evidence**: evidence/figures/figure6.md
- **Run**: MATLAB 2020a; reasoning stated in §4.2.5.
- **Setup**:
  - Model: the four PSO variants on the benchmark comparison
  - Hardware: Not specified in paper
  - Dataset: benchmark comparison of E02
  - System: the shared population size, dimension, and maximum iteration budget of the benchmark comparison (values in §4.2.5)
- **Procedure**:
  1. Observe the iteration at which the variants first approach the acceptance band.
  2. Set a minimum iteration floor from that observation.
  3. Choose a final budget with margin above the floor and justify it.
- **Metrics**: iteration-to-band, chosen budget, margin
- **Expected outcome**:
  - A budget set well above the first-approach point buys reliability margin, not additional final accuracy (curves are already flat past the floor).
- **Baselines**: PSO, CPSO, QPSO
- **Dependencies**: E02
