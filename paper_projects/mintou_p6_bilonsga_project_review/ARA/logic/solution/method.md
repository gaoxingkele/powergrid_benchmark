# Method

## Main Algorithm

`BiLo-NSGA`: Bidirectional Local-search Non-dominated Sorting Genetic Algorithm

## Innovation Handles

- Defines local-search moves in project-review terms.
- Produces an audit trail for added, removed, and substituted projects.
- Separates the algorithmic contribution from broader feasibility-review framing.

## Baseline Coverage

- NSGA-II
- NSGA-III
- MOEA/D
- Greedy BCR
- AHP/TOPSIS
- Random Feasible

## Ablation Coverage

- no_forward_search
- no_backward_search
- random_mutation_only
- no_dependency_moves
- no_feasibility_recovery
- weighted_ranking_only
- shallow_local_search
- low_dependency_density
- loose_budget
