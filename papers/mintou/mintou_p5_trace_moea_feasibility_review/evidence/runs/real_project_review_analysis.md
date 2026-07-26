# Real Project Review Analysis - P5 TRACE-MOEA (v2, real algorithms)

Status: `public_rts_simbench_nerc_project_review_v2_real_algorithms`.

## Why v2 exists

The v1 experiment was **invalidated and deprecated**: methods were hand-parameterized
proxies and the composite metric consumed method-owned constants (circular).
v2 re-runs the task with real algorithm implementations (pymoo NSGA-II/NSGA-III/MOEA/D,
classic AHP-TOPSIS/greedy/weighted-sum baselines, self-contained proposed methods),
a method-independent evaluation (standard hypervolume, fixed normalization bounds),
30 seeded runs per method/experiment, and Mann-Whitney U tests with Holm correction.
Trace/move statistics are descriptive only and never enter the ranking.

Task: traceable feasibility review over 7 experiments on RTS-GMLC + SimBench + NERC-report-derived candidates.

## Headline results (pooled across experiments and seeds)

- Proposed method: `TRACE-MOEA`
- Proposed mean hypervolume: `0.17424740` (std `0.00634763`)
- Best baseline: `NSGA-II` with `0.17270385`
- Best ablation: `Ablation-NoScheduleRisk` with `0.17402541`
- Relative gain over best baseline: `0.89%`
- Relative gain over best ablation: `0.13%`
- Holm-significant wins vs baselines: `38/42` (per-experiment comparisons)
- Holm-significant losses (any opponent): `1`
- Current value signal: `positive_but_partially_significant`

## Leaderboard (mean hypervolume, descending)

| method | role | mean HV | std | mean runtime (s) |
|---|---|---|---|---|
| TRACE-MOEA | proposed | 0.17424740 | 0.00634763 | 0.047997 |
| Ablation-NoScheduleRisk | ablation | 0.17402541 | 0.00701730 | 0.042531 |
| Ablation-NoPreferenceRanking | ablation | 0.17395616 | 0.00563757 | 0.044389 |
| Ablation-NoFeasibilityRepair | ablation | 0.17300434 | 0.00652491 | 0.041066 |
| NSGA-II | baseline | 0.17270385 | 0.00642322 | 0.080394 |
| Ablation-NSGA2Only | ablation | 0.17249235 | 0.00651955 | 0.037266 |
| Ablation-NoRenewableFeatures | ablation | 0.16929588 | 0.00374682 | 0.041440 |
| AHP-TOPSIS | baseline | 0.13467830 | 0.00268779 | 0.000394 |
| Ablation-SingleObjective | ablation | 0.11616713 | 0.02636519 | 0.047783 |
| Ablation-NoReliabilityFeatures | ablation | 0.09081027 | 0.02123886 | 0.041556 |
| Random Feasible | baseline | 0.08064060 | 0.02261091 | 0.000321 |
| Ablation-SmallProjectPool | ablation | 0.06919518 | 0.01279698 | 0.044441 |
| Greedy BCR | baseline | 0.05575570 | 0.03247700 | 0.000295 |
| Weighted Sum | baseline | 0.04104791 | 0.01991111 | 0.000291 |
| MOEA/D | baseline | 0.01954232 | 0.01379150 | 0.315039 |

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
