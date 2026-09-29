# Method

## Main Algorithm

`CARS-MODE`: Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution

## Innovation Handles

- Adapts mutation, crossover, and repair intensity from diversity and violation signals.
- Represents planning decisions as engineering portfolios.
- Reports Pareto quality and electrical feasibility together.

## Baseline Coverage

- Standard DE
- NSGA-II
- MOEA/D
- PSO
- GA
- Weighted Sum

## Ablation Coverage

- fixed_parameters
- no_strategy_adaptation
- no_constraint_repair
- no_diversity_preservation
- weighted_sum_only
- no_storage_candidates
- no_der_candidates
- low_scenario_count
