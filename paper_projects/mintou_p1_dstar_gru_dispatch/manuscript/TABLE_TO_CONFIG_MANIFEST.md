# Table-to-Config Manifest

This manifest binds the manuscript's tables and information claims to the frozen executable assets. Paths beginning with `../../` are relative to this project directory. All reported model results use v6 (`public_rts_curtailment_v6_modern_temporal_controls`). The v5 files are provenance records only.

## Information-time contract

| Contract field | Executed definition | Source/config binding | Manuscript use |
|---|---|---|---|
| Source row time | `Year`, `Month`, `Day`, and `Period` are joined into one row key by `sum_timeseries`. | `../../src/powergrid_benchmark/mintou_real_dispatch.py`, `sum_timeseries`. | Delivery-row index; not an issue timestamp. |
| Benchmark issue index | Query window ends at row $s$ and includes rows $s-47:s$. | `mintou_real_curtailment.py`, `build_task`: `starts` and `windows`. | Called benchmark issue index, not operational issue time. |
| Delivery row | $t=s+h$, with $h=1$ or $24$. | `build_task`: `target_t = starts + horizon`; v6 config `horizons`. | Retrospective 1 h and 24 h lag tasks. |
| Data vintage | No issue timestamp, as-of mapping, release identifier, or revision field is recorded in the config or result rows. | v6 config and run schema inspected; no such field. | Exact source vintage is unresolved; no operational day-ahead claim. |
| Common raw query features | Load, wind, PV, net load, load ramp, renewable share, static topology-stress proxy for rows $s-47:s$. | `build_series`, `build_task`; v6 config `window=48`. | Same raw query window for all methods, except NoTopology drops the last feature. |
| Shared normalization | Mean/SD from feature rows 0--6131. | `build_task`: `mu = features[:train_end]`, `sd = features[:train_end]`. | For the first 23 targets of the 24 h test, scaling includes pre-test feature rows later than $s$. |
| Temporal partitions | First 70% of delivery target rows is training; its last 15% is validation; final 30% is test. | v6 config `train_ratio=0.7`; source `VAL_RATIO=0.15`. | Delivery-row split, no shuffling; not a per-issue as-of split. |

## Paper-facing name mapping

| Paper-facing term | Frozen artifact identifier | Rationale |
|---|---|---|
| GRU learned-space retrieval (GRU-LSR) | `DSTAR-GRU` | Preserves joins to the immutable archive while removing the unsupported digital-twin/Siamese expansion. |
| Shared-encoder learned-space retrieval | Source/config descriptions containing “Siamese retrieval” | The same fitted encoder maps bank and query windows; no contrastive or pairwise loss is implemented. |
| Retrospective 24 h lag onset detection | Some historical prose calls this “day-ahead warning.” | No issue timestamp or forecast vintage exists in the executed assets. |

## Manuscript table bindings

| Manuscript table | Values and configuration | Frozen result source | Scope and consistency note |
|---|---|---|---|
| **Table 1: cap sensitivity** | Caps 0.60/0.70/0.80, onset threshold 0.02, final-30% test. `manuscript/figures/cap_sensitivity.json`. | Series statistics derived from the same `build_series` construction. | Series-level only. The v6 model config fixes cap 0.70; there are no 0.60/0.80 model reruns. |
| **Table 2: methods** | `../../papers/mintou/mintou_p1_dstar_gru_dispatch/src/configs/real_curtailment_config.json`, `methods`; source `METHODS`. | v6 run archive method/role columns. | 14 methods: GRU-LSR/archive DSTAR-GRU, eight baselines, five ablations. |
| **Table 3: hyperparameters** | v6 config: hours, window, horizons, train ratio, seeds, epochs, $k$; source constants/model constructors: validation ratio, batch, learning rate, hidden size, blend grid, Ridge penalty, thresholds, DLinear window 25, TCN channels/dilations. | Not a result table. | The JSON config is incomplete for several source-only constants. Its `statistics` string mentions curtailment MAE only; the source loop and `primary_inference_v2` table contain the recorded three-metric family. |
| **Table 4: leaderboards** | v6 config task, horizons, methods, seeds. | `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/tables/real_curtailment_leaderboard.csv` (28 rows). | Means over ten seeds for stochastic methods and one row for deterministic methods. GRU-LSR maps to source label DSTAR-GRU. |
| **Table 5: compute--error** | v6 config task/horizons/seeds; source timing wraps each `run_method` call. | `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/runs/real_curtailment_results.csv` (208 rows), fields `runtime_s` and `curtailment_mae`. | Descriptive wall-clock measurements from the recorded environment; not an asymptotic or deployment benchmark. |

## Inference and figure bindings

| Claim/artifact | Source | Binding |
|---|---|---|
| Primary 27-test family per horizon | `real_curtailment_primary_inference_v2.csv` | Archive-label DSTAR-GRU versus nine seeded opponents on curtailment MAE, onset MAE, and onset F1; Holm within horizon. |
| Paired sensitivity | `real_curtailment_paired_sensitivity_v2.csv` | Exact sign-flip sensitivity using common seed indices; does not replace primary Mann--Whitney inference. |
| Figures 3--8 | v6 run/leaderboard/inference tables | Existing graphics display the frozen DSTAR-GRU label; captions map it to GRU-LSR. |
| Figure 1/task counts | `manuscript/figures/series_stats.json` and `cap_sensitivity.json` | Series/task description only; no extra model run. |
| NREL-118 applicability | `nrel118_transportability_config.json` and `nrel118_transportability_summary.csv` | Zero positive rows at cap 0.70; no model ranking. |

## Method information availability

| Method family | Fit/reference rows | Validation/selection rows | Boundary at a test query ending at $s$ |
|---|---|---|---|
| Persistence | None | None | Uses $y_s$ only. |
| Seasonal-24h | None | None | Uses $y_{t-24}$; equals $y_s$ at $h=24$. |
| Ridge, kNN-RawFeature | Fit + validation targets through delivery row 6131 | Fixed penalty or $k$ | Model/bank is frozen by delivery split, not per issue index. |
| MLP, LSTM, DLinear, TCN | Fit targets | Validation targets through row 6131 select checkpoint | Raw query ends at $s$; checkpoint may use later pre-test rows for the first 23 $h=24$ samples. |
| GRU-LSR and retrieval controls | Fit targets; retrieval bank is fit-only | Validation targets through row 6131 select checkpoint/blend | Raw query ends at $s$; fitted artifacts may cross the issue index for the first 23 $h=24$ samples. |
| Onset classification for every method | Fit + validation predictions/labels through row 6131 | 40-quantile F1 grid | Threshold may cross the issue index for the first 23 $h=24$ samples. |

## v5/v6 provenance

| Version | Repository state | Methods / run rows | Role in paper |
|---|---|---:|---|
| v5 `public_rts_curtailment_v5_onset_eval` | `3f0371eb5d775f5967ad59120e937d4804bd5a21` (2026-07-26) | 12 / 168 | Historical archive only. Current `*_v5_pre_above_mean.csv` copies have the same Git blob IDs as the v5 current-name files at this revision. |
| v6 `public_rts_curtailment_v6_modern_temporal_controls` | `a728800bd48b11bc8f07647f82e4c9c2841a3e45` (2026-08-13) | 14 / 208 | Sole source for manuscript model results; adds DLinear and TCN. |

All 15 scientific metric fields in the 168 shared method--horizon--seed rows are identical between archived v5 and v6. Runtime and source-status strings are excluded from that scientific-field comparison. Thus v6 extends rather than numerically revises the shared v5 results.

## Frozen artifact checksums

SHA-256 values below identify the inspected supplementary assets. They are reproducibility metadata, not scientific outcomes.

| Asset | SHA-256 |
|---|---|
| `../../src/powergrid_benchmark/mintou_real_curtailment.py` | `c918466cb2119096190566fe7cc814a5233554406c0473c9caced47ce4cbc294` |
| `../../papers/mintou/mintou_p1_dstar_gru_dispatch/src/configs/real_curtailment_config.json` | `1f6b81676d5c3e85386c344cef5fe735dd440a095ff74234b92a7210907436c2` |
| v6 `evidence/runs/real_curtailment_results.csv` | `19d5bc93d96c5b4c094b828fd119d3401a30e41ba44317f681b255bbc3469a75` |
| v6 `evidence/tables/real_curtailment_leaderboard.csv` | `4cd40a7eb2666824e816305b0cc7b0dcf12a9e73a275e9d22e5c25acea31a246` |
| v6 `evidence/tables/real_curtailment_primary_inference_v2.csv` | `be28954a19bdd4abe59cba3c0089ec7f3c4b35f33863fcc41bfa287b059bac63` |
| v6 `evidence/tables/real_curtailment_paired_sensitivity_v2.csv` | `c7f96bed52088d34e8e4e1430c32e8a88b10d4edb6632ef44904eacbbfa9d815` |
| v5 `evidence/runs/real_curtailment_results_v5_pre_above_mean.csv` | `2fc3caad1b0f628a3dce0c5fc5143429e809c02079011db62389973b7577120e` |
| v5 `evidence/tables/real_curtailment_leaderboard_v5_pre_above_mean.csv` | `aa893c768b24ce8f439b0039b3243845fc038f36d532a4384a8b5e7eadbaa1f9` |
| `manuscript/figures/series_stats.json` | `78445c4551421ca1b10fd984eb550ab4f946492c33afc9fb34d830e34c1d259c` |
| `manuscript/figures/cap_sensitivity.json` | `4769b69611262706a55ed0d701e859515854ff20d65f32d6bf41894c095aa10a` |

## Known manifest boundaries

- `experiment_manifest.json` and `method_manifest.csv` describe the deprecated synthetic/dispatch concept and are not configurations for manuscript Tables 2--5.
- `real_curtailment_config.json` is the governing v6 JSON, but source code remains necessary for constants absent from the JSON.
- The exact RTS-GMLC source release/vintage is not recorded in these assets; no source-file checksum can be published from the inspected worktree.
- The delivery-row split does not enforce a per-issue cutoff. For 24 h delivery rows 6132--6154 (issue indices 6108--6130), scaling and validation-selected artifacts can use later pre-test rows through 6131.
- Selected retrieval blend coefficients are not stored in the run rows.
- `p1_method_diagnostics.csv` omits DLinear and TCN and must not replace the v6 leaderboard.
