# Experiments

## E01: DDU vs Single-Level Hardening Comparison (Case 1 vs Case 2)

- **Verifies**: C01 — DDU-based multi-level hardening reduces cost compared to single-level (binary) hardening.
- **Evidence**: Table 2, Figure 4, Table 9.
- **Run**: 1 (base case in Table 2).
- **Setup**: IEEE 33-bus test system. Three wind-speed scenarios, six fault states per scenario. Hardening budget CNY 1.2 million. Three hardening levels (costs: 200k/300k/500k CNY; coefficients: 2/4/6). Case 1: traditional single-level hardening (binary, no DDU). Case 2: proposed multi-level DDU model. MEG at node 11. EV stations at nodes 14, 30. DGs at nodes 14, 21, 24.
- **Procedure**:
  1. Solve Case 1 (single-level hardening model, no DDU: lines either hardened or not).
  2. Solve Case 2 (multi-level DDU model with graduated hardening levels).
  3. Compare total costs, considering both the case where hardened lines do not fail and the case where they still have residual failure probability.
  4. Re-evaluate with three most probable fault scenarios for comparison (Figure 4).
- **Metrics**: Total system cost (CNY 10^4) including load shedding, generation, and purchased electricity. Reinforcement strategy (which lines hardened to which levels).
- **Expected outcome**: Case 2 total cost is lower than Case 1 when line failure probability is considered, because the DDU model allocates hardening resources more flexibly across graduated levels, avoiding over-investment in low-priority lines. Without considering failure, Case 2 cost may be higher because more sophisticated modeling does not provide benefit. DDU model enables more flexible reinforcement combinations.
- **Baselines**: Case 1 (traditional single-level hardening).
- **Dependencies**: E02, E06.

## E02: Five-Case Comparative Analysis of Resilience Measures

- **Verifies**: C02 — coordinated optimization of multiple resilience measures reduces loss-of-load cost.
- **Evidence**: Table 2, Table 3, Table 9.
- **Run**: 2 (comprehensive comparative analysis in Section 5.2).
- **Setup**: IEEE 33-bus and IEEE 123-bus systems with five planning schemes:
  - Case 1: Traditional single-level hardening, no DDU, no reconfiguration, no DR, no EV, no MEG.
  - Case 2: DDU multi-level hardening only.
  - Case 3: DDU + network reconfiguration (tie-line switching).
  - Case 4: DDU + reconfiguration + DR + EV + MEG.
  - Case 5: DDU + all measures + distributionally robust optimization (worst-case scenarios).
- **Procedure**:
  1. Configure each case according to Table 1.
  2. Solve each case under same 33-bus test system parameters.
  3. Compare total costs, reinforcement strategies, and MEG deployment.
  4. Repeat on IEEE 123-bus system (94 nodes) for scalability verification (Table 9).
  5. Track simulation time for each case.
- **Metrics**: Total cost (CNY 10^4), load loss rate (%), MEG deployment nodes, simulation time.
- **Expected outcome**: Cost decreases from Case 2 to Case 4 as more resilience measures are added. Case 5 has slightly higher nominal cost than Case 4 but lower worst-case cost, demonstrating the DRO insurance effect. Simulation time increases with model complexity (Case 5 is slowest). Adding demand response, EV-V2G, and MEG reduces load shedding most significantly. The same cost trends replicate on the larger IEEE 123-bus system, confirming scalability.
- **Baselines**: Case 1 and Case 2 serve as baselines for evaluating incremental benefit of each resilience measure.
- **Dependencies**: E01, E04.

## E03: Sobol' Global Sensitivity Analysis of Reinforcement Decisions

- **Verifies**: C04 — Sobol' first-order indices identify the highest-priority reinforcement targets.
- **Evidence**: Figure 6, Table 7.
- **Run**: 3 (Section 5.3).
- **Setup**: IEEE 33-bus system. Eight candidate reinforcement lines (1-2, 2-3, 3-23, 23-24, 31-32, 32-33, 3-4, 5-6) covering different functional roles (feeders, tie lines, secondary branches). Resilience index R = f(x_1, ..., x_8) where x_i are decision variables indicating hardening levels.
- **Procedure**:
  1. Define input variables: eight reinforcement decision variables (hardening level of each candidate line).
  2. Establish resilience evaluation model: R = f(x_1, ..., x_n) measuring system resilience (e.g., expected load recovery).
  3. Generate N random samples of reinforcement variables within feasible budgets using Monte Carlo or Latin Hypercube Sampling.
  4. Evaluate resilience index for each sample.
  5. Calculate first-order Sobol' indices (Si) and total-effect indices (STi).
  6. Compute across four budget levels: 12, 15, 18, 21, 24 (x 10^4 CNY).
- **Metrics**: First-order Sobol' index (Si) per line per budget level. Total-effect index (STi) at budget CNY 24 x 10^4. Difference STi - Si indicating interaction strength.
- **Expected outcome**: At low budgets, main feeder lines and key tie lines to critical load clusters exhibit the highest Si values. At higher budgets, contributions expand to secondary lines near critical loads. Lines near critical loads with MEG/DG support show STi values significantly exceeding their Si values, indicating strong interaction effects. Lines with consistently low Si and STi across budgets can be deprioritized.
- **Baselines**: No baseline method explicitly compared; analysis is self-referential to the model.
- **Dependencies**: E01, E02 (the sensitivity analysis relies on the same system configuration).

## E04: DRO vs Deterministic Optimization Comparison (Case 4 vs Case 5)

- **Verifies**: C03 — DRO provides insurance against worst-case scenarios.
- **Evidence**: Table 3.
- **Run**: 4 (Section 5.3).
- **Setup**: IEEE 33-bus system. Four reinforcement cost levels: 12, 15, 18, 24 (x 10^4 CNY). Case 4: deterministic model (fixed scenario probabilities). Case 5: DRO model (worst-case distribution in ambiguity set).
- **Procedure**:
  1. Solve Case 4 (deterministic) with scenario probabilities p_k = p_{k,0}.
  2. Solve Case 5 (DRO) where the solver identifies the worst-case probability distribution within the norm-bounded ambiguity set.
  3. Compare total costs for both cases under nominal conditions.
  4. Compute worst-case costs by forcing the worst-case scenario scenario into both models.
  5. Repeat at four reinforcement cost levels.
- **Metrics**: Total cost (CNY 10^4) for nominal and worst-case conditions for both Case 4 and Case 5.
- **Expected outcome**: Case 5 nominal cost is slightly higher than Case 4 due to the DRO premium (bias toward worst-case distribution). However, Case 5 worst-case cost is lower than Case 4 worst-case cost, confirming the DRO insurance effect. As reinforcement cost increases, the gap narrows because critical lines become hardened in both cases, making the worst-case scenarios more similar. The DRO premium is the price paid for guaranteed worst-case protection.
- **Baselines**: Case 4 (deterministic model).
- **Dependencies**: E02 (Cases 4 and 5 as defined in the five-case analysis).

## E05: Confidence Set Parameter Sensitivity Analysis

- **Verifies**: C03 — higher confidence levels (larger ambiguity sets) increase total cost.
- **Evidence**: Table 6.
- **Run**: 5 (Section 5.3, Table 6).
- **Setup**: IEEE 33-bus system. Varying combinations of confidence parameters alpha_1 and alpha_infinity for the l1-norm and l-infinity-norm ambiguity sets.
- **Procedure**:
  1. Set alpha_1 values: 0.2, 0.5, 0.9.
  2. Set alpha_infinity values: 0.5, 0.9, 0.99.
  3. For each of the 9 combinations, solve the DRO model and record total cost.
- **Metrics**: Total cost (CNY 10^4) for each (alpha_1, alpha_infinity) combination.
- **Expected outcome**: As either alpha_1 or alpha_infinity increases (larger ambiguity set), total cost increases. alpha_infinity has a stronger effect on total cost than alpha_1, because the l-infinity-norm constrains the maximum per-scenario deviation and is the binding constraint. The cost increase is monotonic but not linear.
- **Baselines**: alpha_1 = alpha_infinity = 0 (would be deterministic case, not explicitly computed).
- **Dependencies**: E04.

## E06: Fault-State Pruning Computational Efficiency

- **Verifies**: C05 — scenario pruning reduces computation time while incurring minimal accuracy loss.
- **Evidence**: Table 8.
- **Run**: 6 (Section 5.4).
- **Setup**: IEEE 33-bus system. Three wind-speed scenarios (probabilities 0.11, 0.58, 0.31), each generating three failure states, total nine initial fault states. Hardening cost CNY 1.2 x 10^5. Pruning ratio alpha_cut = 0.95.
- **Procedure**:
  1. Solve without reduction (all 9 states) to obtain baseline cost and solve time.
  2. Reduce 2 fault states (keep 7). Record total cost, error, and solve time.
  3. Reduce 3 fault states (keep 6). Record same metrics.
  4. Reduce 4 fault states (keep 5). Record same metrics.
- **Metrics**: Total cost (CNY 10^4), percentage error relative to no-reduction case, solve time (seconds).
- **Expected outcome**: Reducing a moderate number of lowest-weighted fault states yields a large reduction in solve time with minimal cost error (< 1%) because low-impact states have negligible influence on the optimal hardening decision. Reducing too many states degrades accuracy rapidly as important scenarios are dropped. The trade-off curve is nonlinear: the first few reductions are nearly lossless, but aggressive reduction is unacceptable.
- **Baselines**: No-reduction case (all fault states retained).
- **Dependencies**: E01, E02 (same system configuration).
