# NERC Rule-Based External Consistency Backtest - P6 BiLo-NSGA

Status: `public_nerc_rule_backtest_v1`. First rung of the external-validity ladder
(NERC rule backtest -> MISO MTEP historical backtest -> expert labels).

Rule: priority(candidate) = NERC-topic kind weight x NERC-independent
stress percentile (raw candidate attributes BEFORE the pool's NERC
adjustment). Alignment measured against each method's selection
frequency over 10 seeded compromise portfolios (published-run seeds).

## Results

| experiment | method | role | priority capture | Kendall tau | p |
|---|---|---|---|---|---|
| budget_constrained_selection | AHP-TOPSIS | baseline | 2.314274 | 0.441372 | 2.26215e-08 |
| budget_constrained_selection | Ablation-NoForwardSearch | ablation | 1.742914 | 0.176308 | 0.0177575 |
| budget_constrained_selection | Ablation-ShallowLocalSearch | ablation | 1.671945 | 0.174575 | 0.0187098 |
| budget_constrained_selection | Ablation-RandomMutationOnly | ablation | 1.623138 | 0.043165 | 0.561095 |
| **budget_constrained_selection | BiLo-NSGA | proposed | 1.616590 | 0.109198 | 0.142573 |
| budget_constrained_selection | Ablation-LegacyDeletion | ablation | 1.607400 | 0.136551 | 0.0663526 |
| budget_constrained_selection | Ablation-NoBackwardSearch | ablation | 1.578274 | 0.070355 | 0.343647 |
| budget_constrained_selection | NSGA-II | baseline | 1.574740 | 0.058546 | 0.429176 |
| budget_constrained_selection | Ablation-LooseBudget | ablation | 1.571654 | 0.126553 | 0.0903842 |
| budget_constrained_selection | Ablation-LowDependencyDensity | ablation | 1.570698 | 0.101299 | 0.172919 |
| budget_constrained_selection | Ablation-NoFeasibilityRecovery | ablation | 1.536215 | 0.099577 | 0.180002 |
| budget_constrained_selection | Ablation-NoDependencyMoves | ablation | 1.533999 | 0.064709 | 0.382751 |
| budget_constrained_selection | NSGA-III | baseline | 1.492731 | 0.011861 | 0.872564 |
| budget_constrained_selection | Ablation-WeightedRankingOnly | ablation | 1.216178 | 0.027437 | 0.728193 |
| budget_constrained_selection | Pareto Local Search | baseline | 1.039933 | -0.068597 | 0.349858 |
| budget_constrained_selection | Random Feasible | baseline | 0.943514 | -0.003443 | 0.96345 |
| budget_constrained_selection | MOEA/D | baseline | 0.842903 | -0.034909 | 0.655717 |
| budget_constrained_selection | Greedy BCR | baseline | 0.226572 | -0.266846 | 0.000724802 |
| reliability_prioritized_review | AHP-TOPSIS | baseline | 1.597855 | 0.497232 | 4.84178e-07 |
| reliability_prioritized_review | NSGA-II | baseline | 1.403196 | 0.296324 | 0.00108727 |
| reliability_prioritized_review | Ablation-RandomMutationOnly | ablation | 1.361182 | 0.084286 | 0.353344 |
| reliability_prioritized_review | Ablation-LowDependencyDensity | ablation | 1.358136 | 0.229844 | 0.0115616 |
| reliability_prioritized_review | NSGA-III | baseline | 1.357023 | 0.259801 | 0.00412915 |
| reliability_prioritized_review | Ablation-LooseBudget | ablation | 1.347782 | 0.096848 | 0.286228 |
| reliability_prioritized_review | Ablation-NoBackwardSearch | ablation | 1.336575 | 0.160346 | 0.0758421 |
| reliability_prioritized_review | Ablation-NoForwardSearch | ablation | 1.326014 | 0.155060 | 0.0853634 |
| reliability_prioritized_review | Ablation-LegacyDeletion | ablation | 1.321351 | 0.097150 | 0.287563 |
| reliability_prioritized_review | Ablation-NoDependencyMoves | ablation | 1.317527 | 0.146806 | 0.104651 |
| **reliability_prioritized_review | BiLo-NSGA | proposed | 1.301273 | 0.072899 | 0.419248 |
| reliability_prioritized_review | Ablation-ShallowLocalSearch | ablation | 1.277172 | 0.133861 | 0.135496 |
| reliability_prioritized_review | Ablation-NoFeasibilityRecovery | ablation | 1.271615 | 0.136584 | 0.132383 |
| reliability_prioritized_review | Pareto Local Search | baseline | 1.027687 | -0.011780 | 0.896246 |
| reliability_prioritized_review | Random Feasible | baseline | 0.953811 | -0.129607 | 0.164782 |
| reliability_prioritized_review | Ablation-WeightedRankingOnly | ablation | 0.734584 | -0.099896 | 0.311992 |
| reliability_prioritized_review | Greedy BCR | baseline | 0.450402 | -0.406526 | 3.88116e-05 |
| reliability_prioritized_review | MOEA/D | baseline | nan | nan | nan |

## Boundary (read before citing)

- This is an external-CONSISTENCY check, not ground truth: it asks whether
  portfolios concentrate on candidates whose kind and physical stress match
  failure modes documented in the cached NERC reports.
- Residual construct overlap: the experiment pool's candidate attributes were
  NERC-adjusted at the kind level during construction, so kind weights are
  not fully independent of the pool. The stress-percentile component IS
  independent (raw RTS/SimBench physics). The MISO MTEP historical backtest
  remains the required true external anchor before manuscript validity
  claims.
- priority_capture > 1 means the method over-samples documented-risk
  candidates relative to a uniform pool draw.
