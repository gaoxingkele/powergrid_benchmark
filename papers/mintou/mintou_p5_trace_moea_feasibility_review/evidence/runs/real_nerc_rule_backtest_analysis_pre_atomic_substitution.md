# NERC Rule-Based External Consistency Backtest - P5 TRACE-MOEA

Status: `public_nerc_rule_backtest_v1`. First rung of the external-validity ladder
(NERC rule backtest -> MISO MTEP historical backtest -> expert labels).

Rule: priority(candidate) = NERC-topic kind weight x NERC-independent
stress percentile (raw candidate attributes BEFORE the pool's NERC
adjustment). Alignment measured against each method's selection
frequency over 10 seeded compromise portfolios (published-run seeds).

## Results

| experiment | method | role | priority capture | Kendall tau | p |
|---|---|---|---|---|---|
| benchmark_portfolio_optimization | AHP-TOPSIS | baseline | 2.291668 | 0.450425 | 1.16119e-08 |
| benchmark_portfolio_optimization | Ablation-NoRenewableFeatures | ablation | 1.684919 | 0.069897 | 0.341597 |
| benchmark_portfolio_optimization | Weighted Sum | baseline | 1.681310 | 0.102386 | 0.194673 |
| benchmark_portfolio_optimization | Ablation-NSGA2Only | ablation | 1.590639 | 0.044170 | 0.548735 |
| benchmark_portfolio_optimization | NSGA-II | baseline | 1.584589 | 0.084231 | 0.250056 |
| **benchmark_portfolio_optimization | TRACE-MOEA | proposed | 1.550030 | 0.010955 | 0.881115 |
| benchmark_portfolio_optimization | Ablation-NoPreferenceRanking | ablation | 1.514015 | -0.010529 | 0.885573 |
| benchmark_portfolio_optimization | Ablation-NoScheduleRisk | ablation | 1.493551 | 0.006176 | 0.933116 |
| benchmark_portfolio_optimization | Ablation-NoFeasibilityRepair | ablation | 1.457017 | -0.012004 | 0.86965 |
| benchmark_portfolio_optimization | Ablation-SingleObjective | ablation | 1.107951 | 0.162735 | 0.0277619 |
| benchmark_portfolio_optimization | Ablation-SmallProjectPool | ablation | 1.034828 | -0.055145 | 0.465512 |
| benchmark_portfolio_optimization | Ablation-NoReliabilityFeatures | ablation | 1.024520 | 0.027392 | 0.712551 |
| benchmark_portfolio_optimization | Random Feasible | baseline | 0.891288 | -0.069526 | 0.347738 |
| benchmark_portfolio_optimization | MOEA/D | baseline | 0.597327 | -0.045654 | 0.560112 |
| benchmark_portfolio_optimization | Greedy BCR | baseline | 0.226572 | -0.305273 | 0.00011029 |
| reliability_driven_review | AHP-TOPSIS | baseline | 1.628495 | 0.524609 | 1.09893e-07 |
| reliability_driven_review | NSGA-II | baseline | 1.383713 | 0.261055 | 0.00398131 |
| reliability_driven_review | Ablation-NoFeasibilityRepair | ablation | 1.361194 | 0.192080 | 0.0334733 |
| reliability_driven_review | Ablation-NoScheduleRisk | ablation | 1.343222 | 0.208088 | 0.0204789 |
| reliability_driven_review | Ablation-NoPreferenceRanking | ablation | 1.341015 | 0.149776 | 0.0958362 |
| reliability_driven_review | Ablation-NoRenewableFeatures | ablation | 1.340772 | 0.217509 | 0.0154462 |
| **reliability_driven_review | TRACE-MOEA | proposed | 1.338031 | 0.146437 | 0.104422 |
| reliability_driven_review | Ablation-NSGA2Only | ablation | 1.289209 | 0.060553 | 0.500055 |
| reliability_driven_review | Random Feasible | baseline | 1.023574 | 0.073651 | 0.420889 |
| reliability_driven_review | Ablation-NoReliabilityFeatures | ablation | 0.993940 | -0.007161 | 0.937932 |
| reliability_driven_review | Weighted Sum | baseline | 0.986595 | 0.042020 | 0.670633 |
| reliability_driven_review | Ablation-SingleObjective | ablation | 0.973754 | 0.054893 | 0.547867 |
| reliability_driven_review | Ablation-SmallProjectPool | ablation | 0.799643 | -0.313718 | 0.000789096 |
| reliability_driven_review | Greedy BCR | baseline | 0.532293 | -0.389867 | 7.95221e-05 |
| reliability_driven_review | MOEA/D | baseline | nan | nan | nan |

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
