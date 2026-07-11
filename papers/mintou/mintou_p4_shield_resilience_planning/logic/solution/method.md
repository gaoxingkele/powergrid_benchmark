# Method

## Main Algorithm

`SHIELD-MOEA`: Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience

## Innovation Handles

- Combines scenario screening with resilience-aware Pareto optimization.
- Uses local repair to recover feasibility under outage and DER uncertainty.
- Preserves stress-test and failed-scenario evidence in ARA traces.

## Baseline Coverage

- NSGA-II
- MOEA/D
- GA
- Weighted Sum
- Stochastic MILP-small

## Ablation Coverage

- no_scenario_screening
- no_local_repair
- no_resilience_objective
- no_der_uncertainty
- no_outage_uncertainty
- low_scenario_count
- weighted_sum_only
