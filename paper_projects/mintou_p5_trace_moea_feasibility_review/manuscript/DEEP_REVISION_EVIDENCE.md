# Deep Revision Evidence Contract

This contract fixes the claim boundary for TRACE-MOEA. It treats the released
run tables, configuration files, and implementation as evidence of constrained
proxy-benchmark search and run-level event co-occurrence summaries. It does not
treat them as evidence of real utility-review accuracy, electrical feasibility,
or human value.

## Title-to-Evidence Map

Manuscript title: **TRACE-MOEA: Constrained Power-Grid Portfolio Search with Adaptive Preference Elitism, Budget Repair, and Run-Level Event Co-Occurrence Summaries**.

| Title element | What is measured or implemented | Evidence of record | Claim boundary |
|---|---|---|---|
| Constrained power-grid portfolio search | Binary selection from a 120-candidate public proxy under a hard cost budget and five proxy objectives; feasible-front hypervolume is recorded for each run. | `manuscript/MANUSCRIPT.md` Sections 3 and 5; `papers/mintou/mintou_p5_trace_moea_feasibility_review/src/configs/real_project_review_config.json`; `evidence/runs/real_project_review_results.csv` | “Constrained” means budget-constrained. It does not mean AC power-flow, OPF, or engineering-economic feasibility. |
| Adaptive preference elitism | Eight weight vectors score generation-locally normalized parent--offspring rows with a dimensionless violation penalty of 10; absent best-response row indices replace seeded-random selected slots. The vectors are perturbed and greedily reselected every five generations. | `src/powergrid_benchmark/mintou_real_project_review.py`; NoPreferenceRanking rows in `evidence/tables/real_project_review_leaderboard.csv` and `real_project_review_inference_v2.csv` | The payload is emitted even when no replacement occurs, and replacement/eviction is not counted. The mechanism's isolated pooled hypervolume difference is only 0.17% and its direct effect is unresolved after cross-scenario correction. |
| Budget repair | Over-budget portfolios deterministically drop the selected candidate with the lowest raw `(reliability + renewable + load_support + quality) / max(cost, 1)` score; exact ties take the smallest pool-local index. | `src/powergrid_benchmark/mintou_real_project_review.py`; NoFeasibilityRepair rows in the main run and aggregate tables | Repair supports budget fundability in synthetic cost units. The mixed-scale score is a proxy heuristic and does not establish network feasibility, economic optimality, or a unit-invariant benefit-cost ranking. |
| Run-level event co-occurrence summaries | Each released main-run row contains `trace_event_count` and `decision_coverage`. The latter is the set overlap between pool-local positions occurring in generated `repair_drop`/`preference_elite` payloads and positions represented in the deduplicated final feasible front. | `evidence/runs/real_project_review_results.csv`; `evidence/tables/real_project_review_leaderboard.csv`; `src/powergrid_benchmark/mintou_real_project_review.py` | The release preserves only count and overlap. Payloads use local positions rather than stable `cid` values; order, replacement flags, evictions, and state snapshots are absent. The evidence therefore supports event production and co-occurrence only, not chronology, replay, an audit trail, or human utility. |

The power-grid setting is a reproducible proxy derived from RTS-GMLC,
SimBench, and public reliability-report metadata. No expert-labeled utility
review dataset is present.

## Primary Estimand and Analysis Unit

The main optimization estimand is the difference in standard feasible-front
hypervolume between TRACE-MOEA and a named comparator within a named review
scenario under the fixed configuration. The analysis unit for a stochastic
comparison is one seeded method-scenario run. Each stochastic method has 30
runs per scenario. Pooled means over seven scenarios are descriptive summaries
across heterogeneous scenarios; the manuscript reports the per-scenario
Mann-Whitney U tests and their within-scenario Holm corrections separately.

Deterministic ranking rules produce one unique output per scenario. Their 30
rows are repeated provenance rows and are used only for descriptive gaps, not
as 30 independent observations. The matched-budget study has a separate unit:
one seeded method-budget run in the preference-aware scenario (three methods,
three budgets, 30 seeds; 270 run rows).

Trace evidence has a different estimand and unit. For each TRACE-MOEA run, the
released record reports the number of generated records and the fraction of
pool-local candidate positions represented in the deduplicated final feasible
front that also occur somewhere in the run's generated event-position set.
Across the 210 main TRACE-MOEA runs, the observed mean is 1126.25 records per
run (sample standard deviation 134.86) and mean position co-occurrence is
0.985688. The count comprises a mean 806.25 repair-drop records and exactly 320
`preference_elite` best-response records per run. Because the implementation
emits one such record for each of eight weight vectors in each of 40 generations
whether or not population replacement was needed, 320 is not an injection,
replacement, or eviction count.

## Comparison Budget and Data Visibility

TRACE-MOEA, NSGA-II, and R-NSGA-II use the disclosed population size of 40,
40 generation labels, and 30 seeds per method-scenario. MOEA/D instead uses 35
five-objective Das--Dennis directions; the run archive does not retain `n_eval`,
so identical objective-call budgets are not claimed. Methods receive the same
scenario candidate pool and budget, except for the explicitly labeled
SmallProjectPool ablation. Other ablations deliberately hide or disable the
component named in the ablation while evaluation remains on the full fixed
objective space. R-NSGA-II is the direct implemented preference-family control.
The three-budget control keeps the nominal population, generation limit,
scenario weights, and seed count fixed while changing budget multiplier and
method. Its raw R-NSGA-II reference point is recomputed from each budget's
frozen bounds.

The generated JSON records population, generations, methods, and evaluation but
omits preference count, penalty, operator rates, adaptation constants, eviction,
ties, and trace schema. R-NSGA-II receives the disclosed raw reference point and
`epsilon=0.01`, but the pymoo version, operator-default probabilities, internal
normalization mode, and per-generation ideal/nadir values were not serialized.
The fixed empirical bounds construct the reference point and evaluation metric;
they are not claimed as the comparator's internal survival bounds. The JSON's
legacy phrases "preference coevolution" and "decision trace archive" name the
weight-update mechanism and ephemeral in-memory list; they do not establish a
separate coevolving solution population or a released event archive.

The deterministic MCDA and greedy methods do not share a stochastic
function-evaluation budget, so their results remain descriptive. Runtime is
implementation- and machine-specific and is not a cross-platform efficiency
claim.

All methods see attributes from the same public proxy construction. Those
attributes include synthetic cost units and engineering proxies; they do not
include confidential utility dossiers, expert feasibility labels, calibrated
utility expenditures, or AC power-flow outcomes. The NERC rule check reuses a
source family involved in proxy construction, and the MTEP16 check has
portfolio dependence and label-imbalance limitations. Both remain descriptive
external-consistency checks.

## Negative and Null Results

- Removing preference adaptation changes pooled hypervolume from 0.174247 to
  0.173956, a 0.17% difference. No preference-ablation contrast survives the
  second Holm correction across seven scenarios; the smallest reported
  cross-scenario-adjusted value is 0.0722. This does not establish a distinct
  optimization gain from adaptive preference elitism.
- TRACE-MOEA is not significantly different from NSGA-II in four of seven main
  scenarios. In `distribution_project_review`, its mean difference is nominally
  negative (-0.00022; Holm-adjusted p = 1.0).
- The NoScheduleRisk ablation has a slightly lower pooled mean overall but is
  higher in `traceability_evaluation` under the within-scenario family. That
  adverse full-method contrast does not survive the second correction
  (cross-scenario-adjusted p = 0.0510).
- The 98.6% value is a software-level set overlap between final-front pool-local
  positions and generated event positions. It is not evidence of explanation
  quality, faster review, more consistent decisions, contestability, or
  regulatory compliance.
- Event payloads, stable candidate identifiers, replacement/eviction flags, and
  population snapshots are not present in the released run table. The package
  therefore cannot support chronology or replay claims.
- The public-record checks do not establish above-chance portfolio performance,
  engineering-economic effectiveness, or expert-validated review correctness.

## Shared Assets and Independent Contribution

The named companion project is `mintou_p6_bilonsga_project_review`. The two
projects share benchmark infrastructure: the public candidate-generation code,
RTS-GMLC/SimBench/NERC source inputs, common execution and evaluation utilities,
and public-record backtest code and source records. Shared infrastructure is
not claimed as TRACE-MOEA's independent contribution.

TRACE-MOEA's independent question is restricted to the p5 configuration and
outputs: how a five-objective, hard-budget portfolio search behaves when a
constrained non-dominated sorting kernel is combined with adaptive preference
elitism, deterministic repair, and quarantined run-level event co-occurrence
summaries. The p5 method configuration, scenario definitions, executions,
run rows, selected fronts, statistical comparisons, and resulting claims are
paper-specific. No result from `mintou_p6_bilonsga_project_review` is used to
support a TRACE-MOEA effect, and no TRACE-MOEA result is evidence for the
companion's independent mechanism question.

## New or Rerun Experiments

No experiment was added or rerun in this narrative stage. The revision consumes
the existing 3360-row main run file, the existing 270-row matched-budget file,
their aggregate/inference tables, and the existing descriptive backtests. No
numerical result was tuned or replaced.

A claim about a replayable intervention archive would require stable candidate
identifiers, ordered payloads, replacement/eviction flags, sufficient state
snapshots, and replay tests, followed by a controlled rerun or a verified export
from preserved runs. A claim about human review
benefit would require a separately approved human evaluation. Electrical
feasibility would require separately approved network-model checks. None of
those studies is part of this stage.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** confirm the CRediT roles and approval of every
  named author. This stage does not assign roles.
- **AUTHOR INPUT REQUIRED:** confirm the funder, grant number, and APC funder,
  or confirm that the no-external-funding statement is correct.
- **AUTHOR INPUT REQUIRED:** provide and approve a persistent repository URL or
  DOI for the paper-specific evidence package, including a decision on whether
  stable-ID ordered payloads, replacement/eviction flags, and replay state will
  be released.
- **AUTHOR INPUT REQUIRED:** confirm ORCID identifiers, correspondence details,
  and the submission-time bibliographic status of the companion manuscript.
- Expert labels, a human trace-utility study, calibrated utility costs, and
  AC/OPF checks remain scientific blockers for stronger deployment, review-
  effectiveness, economic, or electrical-feasibility claims.
