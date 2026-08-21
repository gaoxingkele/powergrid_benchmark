# Experiments

## E01: Comparative planning evaluation of collaborative vs single-device-type strategies
- **Verifies**: C01, C04
- **Evidence**: evidence/tables/table3.md; evidence/tables/table4.md; evidence/tables/table5.md; evidence/figures/figure4.md; evidence/figures/figure5.md; evidence/figures/figure6.md; evidence/figures/figure7.md
- **Run**: Not published as code; described in Section 5.2 (planning results), Section 5.3 (SOP operation impact). Solved via CPLEX for MISOCP on the Portugal 54-node system.
- **Setup**:
  - Model: MISOCP reformulation of the Wasserstein DRO planning model, solved by CPLEX.
  - Test system: Portugal 54-node, 4 substations, 54 source-load nodes, 9 DG nodes, 5 ESS nodes.
  - Cases: Case 1 (lines + SOPs + switches), Case 2 (lines + SOPs only), Case 3 (lines + switches only), Case 4 (Case 1 with SOPs replaced by switches).
  - Parameters: 20-year horizon, discount rate 0.03, line cost 150,000 CNY/km, SOP cost 1000 CNY/kW, switch cost 100,000 CNY each, DR incentive 0.3 CNY/kW, purchase price 0.5 CNY/kW, sale price 0.7 CNY/kW.
- **Procedure**:
  1. Formulate the three-stage MISOCP model for each case.
  2. Solve via CPLEX to obtain optimal planning decisions (line construction, SOP siting/sizing, switch placement).
  3. Compute annualized costs for each component (lines, SOPs, switches, ESS, DR, losses, DG penalties, electricity trading).
  4. Compute annual net profit = revenue - total costs for each case.
  5. Compare net profit and planning configurations across cases.
  6. For Case 4, compute operation-only comparison (fixed planning decisions from Case 1, replace SOPs with switches).
- **Metrics**: Annual net profit (CNY 10^4/year), device investment costs, DG penalty costs, network loss costs, DG accommodation rate, average line load rate.
- **Expected outcome**:
  - Collaborative planning (Case 1) achieves the highest net profit.
  - Case 3 (switches only) has the lowest net profit, with "nearly 5%" reduction vs Case 1.
  - Case 4 operation profit is "more than 6%" lower than Case 1 operation profit.
  - Case 1 requires fewer SOPs than Case 2 (3 vs 5), indicating more efficient deployment.
- **Baselines**: Case 2 (SOP-only), Case 3 (switch-only), Case 4 (SOPs replaced by switches).
- **Dependencies**: none

## E02: Uncertainty-handling method comparison — deterministic vs robust vs distributionally robust
- **Verifies**: C02, C04
- **Evidence**: evidence/tables/table6.md; evidence/figures/figure9.md
- **Run**: Section 5.5 Validity Analysis of Distributionally Robust Optimization Method. Same planning scenario solved under three different uncertainty models.
- **Setup**:
  - Model: Three formulations — (a) Deterministic (stochastic optimization with multiple scenarios, perfect distribution knowledge), (b) Traditional robust optimization (worst-case set-based), (c) Wasserstein-distance DRO (proposed).
  - Test system: Portugal 54-node system (Case 1 planning configuration).
  - Parameters: Same cost and system parameters across all three methods.
- **Procedure**:
  1. Solve the Case 1 planning problem under deterministic formulation (multiple scenarios, known probabilities).
  2. Solve under traditional robust optimization (worst-case uncertainty set).
  3. Solve under Wasserstein DRO (ambiguity set with radius epsilon).
  4. Compare annualized costs and net profit across the three solutions.
  5. Vary Wasserstein radius epsilon and observe impact on solution quality and maximum relative error (Figure 9).
- **Metrics**: Annual net profit (CNY 10^4/year), component costs, maximum relative error vs out-of-sample performance.
- **Expected outcome**:
  - Deterministic: Highest net profit (5089.49) but "too ideal" — does not hedge against distributional ambiguity.
  - Robust: Lowest net profit (4770.01) — overly conservative.
  - DRO: Intermediate net profit (4928.18) — improves by "more than 3%" vs robust optimization.
  - As Wasserstein radius increases, maximum relative error decreases (DRO becomes more robust).
- **Baselines**: Deterministic optimization; traditional robust optimization.
- **Dependencies**: E01

## E03: Solution method comparison — IPOPT vs Bilinear-Removed vs McCormick relaxation
- **Verifies**: C03, C05
- **Evidence**: evidence/tables/table7.md
- **Run**: Section 5.6 Validity Analysis of The McCormick Relaxation Method. Same planning problem solved via three alternative solution approaches.
- **Setup**:
  - Model: (a) IPOPT applied to the original nonconvex MINLP, (b) Bilinear-Removed method of reference [30], (c) Proposed McCormick relaxation method (MISOCP via CPLEX).
  - Test system: Portugal 54-node system (Case 1 planning configuration).
  - Hardware/Software: CPLEX solver for MISOCP; IPOPT for nonconvex NLP; unspecified for Bilinear-Removed.
- **Procedure**:
  1. Solve the original nonconvex MINLP via IPOPT with a 5-hour time limit.
  2. Solve via the Bilinear-Removed heuristic method.
  3. Solve via the proposed McCormick relaxation based MISOCP (CPLEX).
  4. Compare solution quality (annual net profit) and computation time.
- **Metrics**: Annual net profit (CNY 10^7), computing time (hours).
- **Expected outcome**:
  - IPOPT fails to obtain an optimal solution within 5 hours.
  - Bilinear-Removed is fastest (1.59 h) but achieves only 76% of the McCormick solution quality.
  - McCormick relaxation obtains a feasible optimal solution (4.93 x 10^7 CNY) at 2.52 h — demonstrating the best quality-time trade-off.
- **Baselines**: IPOPT (nonconvex); Bilinear-Removed heuristic.
- **Dependencies**: E01

## E04: Cost sensitivity analysis of SOP and interconnection switch investment
- **Verifies**: C01, C02
- **Evidence**: evidence/figures/figure8.md; evidence/tables/table4.md
- **Run**: Section 5.4 Impact of SOP and Interconnection Switch Costs on Planning Results. Varies device cost coefficients and observes changes in optimal planning configuration.
- **Setup**:
  - Model: Case 1 planning model with scaled SOP and switch unit costs.
  - Test system: Portugal 54-node system.
  - Parameters: SOP cost coefficient varied (e.g., 0.5x–1.5x nominal 1000 CNY/kW); interconnection switch cost varied (e.g., 0.5x–1.5x nominal 100,000 CNY each).
- **Procedure**:
  1. Fix all parameters except SOP unit cost.
  2. Solve planning model for each SOP cost level; record net profit and optimal device deployment.
  3. Repeat for interconnection switch cost variation.
  4. Identify cost thresholds where optimal device selection changes.
  5. Plot net profit vs cost coefficient for both device types (Figure 8).
- **Metrics**: Annual net profit (CNY 10^4/year), number and capacity of SOPs installed, number of switches installed.
- **Expected outcome**:
  - As SOP cost decreases, more SOP capacity is installed and net profit increases.
  - As switch cost increases, SOPs substitute for switches at interconnection positions.
  - Crossover point(s) exist where relative cost determines the optimal device choice.
- **Baselines**: Nominal cost coefficients.
- **Dependencies**: E01
