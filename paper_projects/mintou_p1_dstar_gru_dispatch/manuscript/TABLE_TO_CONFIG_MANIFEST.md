# Table-to-Config Manifest

This manifest binds the paper's scientific tables and figures to the completed
fair run at `../experiments/p1_s3_fair_v1/run_manifest.json`. The main
manuscript does not mix the legacy v5/v6 leaderboard with the fair-run result
family. Runtime, environment, hashes, legacy version history, and incident
details are retained in `SUPPLEMENTARY_METHODS_AND_AUDIT.md`.

## Governing evidence

| Item | Binding |
|---|---|
| Run namespace | `p1_s3_fair_v1` |
| Completed result rows | 510 |
| Primary cap | 0.70 |
| Sensitivity caps | 0.60 and 0.80, descriptive on the same system-year |
| Retrospective lags | 1 h and 24 h |
| Seeded unit | Paired GRU method-seed run; ten common seeds |
| Primary test | Two-sided exact paired sign-flip test |
| Multiplicity | Holm over six frozen GRU contrasts separately within each lag |
| Information boundary | Delivery-row data; forecast issue time and source vintage unavailable |
| Independent execution check | All 510 non-timing fields identical; four scientific derived tables byte-identical |

The run manifest validates the exact configuration, script, four RTS-GMLC
input files, and six output files. `manuscript/figures/make_figures.py` repeats
the output hash/byte checks before regenerating figures or derived tables.

## Information-time contract

| Phase | Executed rule | Allowed use | Main-text binding |
|---|---|---|---|
| Fit | Targets below delivery row 4380, with the horizon embargo applied to constructed samples | Feature normalization, Ridge coefficients, GRU parameters, retrieval bank | Sections III-B and V-A |
| Selection | Targets from `4380+h` to 5255 | Ridge penalty, GRU checkpoint, selected head weight | Sections III-B/C and IV |
| Calibration | Targets from `5256+h` to 6131 | Detection threshold only | Sections III-B/C |
| Test | Targets at or after `6132+h` | Scoring only | Sections V-B and VI |

The source files expose calendar delivery rows but not forecast issue
timestamps, an as-of mapping, release identifiers, or data-vintage fields.
Every result is therefore a retrospective delivery-row lag result.

## Manuscript table bindings

| Manuscript table | Values | Direct source | Scope note |
|---|---|---|---|
| Table 1: phase/onset counts | Horizon-specific fit, selection, calibration, test, and onset counts | `derived_tables/fair_onset_support.csv`, derived from `results/run_results.csv` | Delivery-target counts; not independent inferential units |
| Table 2: fair conditions | GRU selected/fixed blends, deterministic baselines, privileged control | `experiments/p1_s3_fair_v1/config.json` and `results/run_results.csv` | Fair subset only; not the legacy 14-method roster |
| Table 3: hyperparameters/statistics | Frozen data split, GRU, retrieval, objective, and test settings | `experiments/p1_s3_fair_v1/config.json` | Runtime/environment omitted from main text |
| Table 4: primary-cap MAE | Mean/SD, head weight, seed count | `derived_tables/fair_primary_cap_summary.csv`, derived from `results/leaderboard.csv` | Deterministic rows are descriptive and have no seed p-value |
| Table 5: onset diagnostics | Six paired onset-F1 contrasts | `derived_tables/fair_paired_contrasts.csv` / `results/paired_primary.csv` | Qualified by zero selection/calibration onsets |
| Table 6: cap sensitivity | Selected GRU-LSR and Persistence MAE in six cap-by-lag cells | `derived_tables/fair_cap_selected_vs_persistence.csv` / `results/cap_sensitivity.csv` | Same system/year; no cross-cap inference |

## Figure bindings

| Figure | Scientific content | Source fields |
|---|---|---|
| Fig. 1: fair temporal gate and onset support | Frozen phase proportions and positive-onset counts by cap/lag/phase | `config.json` partitions; `run_results.csv` count fields |
| Fig. 2: evaluation architecture | Fit-only encoder/bank, selected/fixed blends, separated selection/calibration/test, privileged control | `config.json`; `run_manifest.json` evidence boundary |
| Fig. 3: primary-cap MAE | Direct control, deterministic references, selected/fixed GRU controls | `leaderboard.csv`, cap 0.70 and MAE-selection rows |
| Fig. 4: paired mechanism contrasts | Mean treatment-minus-control differences and within-lag Holm p-values | `paired_primary.csv` |
| Fig. 5: cap sensitivity | Selected GRU-LSR minus Persistence MAE | `cap_sensitivity.csv` |

Every displayed figure has PNG, PDF, and SVG-wrapper forms. Their generated
hashes and the validated input hashes are recorded in
`manuscript/figures/artifact_manifest.json`.

## Negative and null-result bindings

| Finding | Evidence | Required qualification |
|---|---|---|
| Persistence is lower-MAE than selected GRU-LSR at cap 0.70 at both lags | `leaderboard.csv` | Descriptive deterministic comparison; no seed p-value |
| Selected MAE condition uses head weight zero for every seed | `run_results.csv` | Supports retrieval-only, not blend synergy |
| Selection and calibration have zero positive onsets at every cap/lag | `run_results.csv` | Onset-targeted selection and calibration are inapplicable |
| Selected onset condition equals the head | `paired_primary.csv`: difference 0, ten ties, Holm p=1 | Inapplicability evidence, not proof of no onset effect |
| Fixed 0.5 onset-F1 effect is positive at 1 h and null at 24 h | `paired_primary.csv` | Diagnostic under the unsupported onset arm |
| Direct transform has zero continuous error but onset F1 below one | `policy_transform_audit.csv` and `leaderboard.csv` | Metric-definition limitation; direct condition is privileged |
| Cap ordering crosses in two of six cells | `fair_cap_selected_vs_persistence.csv` | Same-series descriptive sensitivity only |

## Legacy evidence boundary

The legacy v5/v6 archives retain historical full-roster results, including
methods not rerun under the fair temporal gate. They remain useful for audit
history but do not support current main-text result, ranking, or inferential
claims. Their hashes and chronology are recorded only in the supplement.
