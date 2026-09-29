# Real Project Review Analysis - P6 BiLo-NSGA (v2, real algorithms)

Status: `public_rts_simbench_nerc_project_review_v3_direct_family_controls`.

## Why v2 exists

The v1 experiment was **invalidated and deprecated**: methods were hand-parameterized
proxies and the composite metric consumed method-owned constants (circular).
v2 re-runs the task with real algorithm implementations (pymoo NSGA-II/NSGA-III/MOEA/D,
classic AHP-TOPSIS/greedy/weighted-sum baselines, self-contained proposed methods),
a method-independent evaluation (standard hypervolume, fixed normalization bounds),
30 seeded runs per method/experiment, and Mann-Whitney U tests with Holm correction.
Trace/move statistics are descriptive only and never enter the ranking.

Task: budget-constrained project review over 8 experiments on RTS-GMLC + SimBench + NERC-report-derived candidates.

## Headline results (pooled across experiments and seeds)

- Proposed method: `BiLo-NSGA`
- Proposed mean hypervolume: `0.17189867` (std `0.00860517`)
- Best baseline: `NSGA-II` with `0.17000297`
- Best ablation: `Ablation-NoBackwardSearch` with `0.17294302`
- Relative gain over best baseline: `1.12%`
- Relative gain over best ablation: `-0.60%`
- Holm-significant wins vs baselines: `52/56` (per-experiment comparisons)
- Holm-significant losses (any opponent): `0`
- Current value signal: `significant_public_signal`

## Leaderboard (mean hypervolume, descending)

| method | role | mean HV | std | mean runtime (s) |
|---|---|---|---|---|
| Ablation-NoBackwardSearch | ablation | 0.17294302 | 0.00797087 | 0.161583 |
| Ablation-NoForwardSearch | ablation | 0.17256956 | 0.00679423 | 0.113853 |
| Ablation-ShallowLocalSearch | ablation | 0.17235875 | 0.00828795 | 0.151955 |
| Ablation-LowDependencyDensity | ablation | 0.17235789 | 0.00848525 | 0.218093 |
| Ablation-LegacyDeletion | ablation | 0.17228212 | 0.00844450 | 0.193346 |
| Ablation-NoDependencyMoves | ablation | 0.17197839 | 0.00927082 | 0.182324 |
| BiLo-NSGA | proposed | 0.17189867 | 0.00860517 | 0.218849 |
| Ablation-RandomMutationOnly | ablation | 0.17172917 | 0.00700738 | 0.049611 |
| NSGA-II | baseline | 0.17000297 | 0.00739137 | 0.079756 |
| Ablation-NoFeasibilityRecovery | ablation | 0.16810627 | 0.01271869 | 0.192076 |
| NSGA-III | baseline | 0.16236232 | 0.01331321 | 0.099305 |
| Ablation-LooseBudget | ablation | 0.16097970 | 0.01350719 | 0.239613 |
| AHP-TOPSIS | baseline | 0.13874738 | 0.00152281 | 0.000405 |
| Pareto Local Search | baseline | 0.11636321 | 0.01487674 | 1.415579 |
| Random Feasible | baseline | 0.07025532 | 0.02089243 | 0.000332 |
| Greedy BCR | baseline | 0.04097955 | 0.00766583 | 0.000300 |
| Ablation-WeightedRankingOnly | ablation | 0.03559022 | 0.00892416 | 0.000318 |
| MOEA/D | baseline | 0.02529045 | 0.01403781 | 0.303851 |

## Interpretation Boundary

Candidates are derived from public grid case statistics and public reliability-report
metadata; portfolio objectives are engineering proxies. The experiment validates
algorithmic performance on a reproducible public benchmark. It does not establish
real-world review validity: expert-labeled outcomes and calibrated engineering
economics remain open requirements before manuscript claims about actual utility
project review. Trace/decision-coverage columns are explainability descriptors, not
performance evidence.

## Remaining Compliant Optimization Path

- Add expert-labeled feasibility-review outcomes (or historical project outcome data,
  e.g. LBNL Queued Up / EIA-860 retirements) as external ground truth.
- Calibrate cost coefficients against published utility investment figures.
- Keep v1 deprecated artifacts and all weak seeds in the evidence trail.
