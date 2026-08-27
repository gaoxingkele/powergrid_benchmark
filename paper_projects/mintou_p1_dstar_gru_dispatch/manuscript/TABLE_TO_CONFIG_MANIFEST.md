# Table-to-Config Manifest

## Stage-5 v2 binding

The paper-facing statistics tables and figures derive only from the accepted,
protocol-valid `p1_ieee_access_upgrade_v2` execution manifest. The derivation
does not mix values from `p1_s3_fair_v1`, legacy v5/v6 runs, historical
ablations, or an additional experiment. Stage 5 integrates these replacements
into `MANUSCRIPT.md` and the exact IEEE Access source.

| Item | Binding |
|---|---|
| Accepted source commit | `cffe8fdb80a022978cc3715bd1fb014647bd1617` |
| Run namespace | `p1_ieee_access_upgrade_v2` |
| Source manifest | `../experiments/p1_ieee_access_upgrade_v2/run_manifest.json` |
| Normative contract | `../experiments/p1_ieee_access_upgrade_v2/upgrade_contract.json` |
| Derivation/check | `../experiments/p1_ieee_access_upgrade_v2/derive_statistics.py` |
| Provenance record | `../experiments/p1_ieee_access_upgrade_v2/statistics_provenance.json` |
| Completed result rows | 2310 |
| Training trajectories | 240 |
| Primary cap / k | 0.70 / 8 |
| Common seeds | 11, 23, 47, 59, 71, 83, 97, 109, 127, 139 |
| Paired inference | 30 contrasts; exact two-sided sign flip; Holm within each frozen family and horizon |
| Seed interval | Predeclared 95% t interval with critical value 2.2621571627409915; seed-conditional only |
| Moving-block sensitivity | 36 cells; block lengths 24/168; 5000 PCG64 replicates; conditional/descriptive only |

## Paper-facing table bindings

| Candidate paper table | Direct sealed source | Derivation | Mandatory scope |
|---|---|---|---|
| `derived_tables/v2_paired_seed_effects.csv` | `results/run_results.csv`; checked against `results/paired_effects.csv` | Independently derives all ten-pair differences, effect summaries, 1024-assignment exact tests, within-family/horizon Holm adjustments, and seed intervals | Cap 0.70; training-seed conditional; onset family diagnostic when pre-test support is absent |
| `derived_tables/v2_moving_block_sensitivity.csv` | `results/test_predictions_primary_mae.npz`; checked against `results/moving_block_supplement.csv` | Paired hourly absolute-loss differences, averaged across ten seeds, then ordinary overlapping non-circular moving-block resampling | Conditional descriptive sensitivity on one observed sequence; excluded from Holm; not uncertainty across years/systems |
| `derived_tables/v2_deterministic_references.csv` | `results/run_results.csv` | Selects the ten cap-0.70 Persistence, Seasonal-24h, objective-specific Ridge, and privileged-control rows | Deterministic descriptive references; no seed-based p-value; privileged control is not a forecaster |
| `derived_tables/v2_cross_cap_descriptive.csv` | `results/run_results.csv` | Computes six selected-learned mean/SD versus Persistence readouts | Same-sequence descriptive comparison; no cross-cap inference |
| `derived_tables/v2_claim_wording_router.csv` | Frozen claim gates plus the four numerical tables above | Applies learned-space, method-specific, null/adverse, Persistence, and onset-inapplicable routes | Cannot broaden a contrast, promote non-significance to no effect, or cure absent onset support |

All five table hashes and byte counts are recorded in
`statistics_provenance.json`. `validate_upgrade.py --phase statistics` rebuilds
the expected bytes in memory and fails if a table is missing, stale, or altered.

## Paper-facing figure bindings

`figures/make_figures.py` verifies every execution-manifest output and every
Stage-3 paper-table hash before rendering. `figures/artifact_manifest.json`
records the generator, source manifests, validated inputs, and hashes for the
PNG/PDF pairs consumed by or delivered with the paper.

| Figure | Direct paper-table/contract binding | Scientific role |
|---|---|---|
| `fig_benchmark_overview` | `upgrade_contract.json`; repeated support fields in sealed `run_results.csv` | temporal gate, analysis-unit counts, and zero pre-test onset support |
| `fig_architecture` | normative retrieval/control catalog in `upgrade_contract.json` | separates target, fitted paths, attribution controls, external references, and privileged audit |
| `fig_primary_effects` | `v2_paired_seed_effects.csv` | three primary contrasts at each lag with seed-conditional intervals and Holm values |
| `fig_cap_profile` | `v2_cross_cap_descriptive.csv` | same-sequence selected-minus-Persistence ordering across caps |

## Frozen statistical families

| Family | Metric / direction | Contrasts per horizon | Holm partition |
|---|---|---:|---|
| `primary_mae_mechanism_attribution` | MAE / lower is favorable | 6 | This family and horizon only |
| `architecture_head_mae` | MAE / lower is favorable | 3 | This family and horizon only |
| `onset_f1_diagnostic` | onset F1 / higher is favorable | 6 | This family and horizon only; diagnostic under absent support |

Caps, objectives, horizons, and families are never pooled for adjustment.
Deterministic references, cross-cap comparisons, and k=4/16/32 sensitivity do
not receive seed-based inference.

## Wording-router outcomes

| Route | Gate | Paper-facing consequence |
|---|---|---|
| learned-space | Both named k=8 controls and paired contrasts must be complete; wording follows both observed directions and adjusted results | Favorable against both controls at 1 h; no learned-space advantage at 24 h because the raw contrast is adverse and the randomized contrast is Holm-unresolved |
| method-specific | Exact condition, control, cap, horizon, metric, and family are named | Favorable results do not license an overall architecture or forecasting winner |
| null/adverse | Adverse directions and Holm-unresolved results remain valid outcomes | Report the adverse result or unresolved contrast; do not call the protocol invalid or infer no effect from non-significance |
| Persistence | One deterministic row per cap/horizon | Report orderings descriptively without a seed-based p-value or general dominance claim |
| onset-inapplicable | Positive onset support is absent in both selection and calibration | All onset-family values remain diagnostics; exact/Holm values cannot license an onset-benefit claim |

## Executable provenance boundary

The execution manifest records runner SHA-256
`d4f0e14dd010e4f429e2d61771d781b169a673b73156dac5236113f0e3f34e28`.
That hash exactly matches the committed Git blob and the canonical-LF working
content. The Windows checkout renders the same content with CRLF and therefore
has raw SHA-256
`da2e1f1ec024d2493e776a1b63b23bfee99b05971752a1ec59f74a2a4dabb225`.
Both representations are recorded; the CRLF rendering is not classified as a
scientific source mismatch. A mismatch between the manifest hash and the
committed blob fails closed.

## Version-scope handoff

The current manuscript narrative and generated figures use the v2 result
family and the Stage-4 citation boundary. The legacy v1 figures and tables may
remain as historical supplementary records but are not cited or copied into
the paper-facing artifact manifest. No title, contribution, method, result,
discussion, or conclusion claim may be broadened beyond the routes above.
