# Figure and Table Trace

This internal map records the accepted evidence and deterministic transformation behind every manuscript table and figure. Source paths and SHA-256 digests are fixed in `RESULTS_ARTIFACT_MANIFEST.json`; `figures/make_figures.py` verifies every digest before writing an artifact. The map is file lineage for the supplementary/internal record and is intentionally absent from the reader-facing results narrative.

| Manuscript item | Regenerated artifact | Accepted evidence used | Comparison scope |
|---|---|---|---|
| Table 1 | `derived_tables/p6_candidate_pool_composition.csv` | Public-source profile | Descriptive candidate derivation |
| Table 2 | `derived_tables/p6_scenario_contract.csv` | Legacy and matched configuration snapshots | Design contract; no outcome comparison |
| Figure 1 | `figures/fig_architecture.{svg,png,pdf}` | Method fields in the two configuration snapshots | Method schematic; no performance claim |
| Table 3 | `derived_tables/p6_method_contract.csv` | Legacy method list plus matched stage-local comparator definitions | Method disclosure |
| Table 4 | `derived_tables/p6_legacy_leaderboard.csv` | Legacy fixed-generation run rows | Pooled descriptive summary; deterministic rows have one unique output per scenario |
| Figure 2 | `figures/fig_hv_boxplot.{svg,png,pdf}` | Legacy fixed-generation run rows | Seed distributions; deterministic methods shown descriptively |
| Table 5 | `derived_tables/p6_legacy_nsga2_scenarios.csv` | Legacy inference rows | Mann--Whitney U; Holm across 14 stochastic opponents within scenario |
| Figure 3 | `figures/fig_budget_sensitivity.{svg,png,pdf}` | Legacy fixed-generation run rows | Budget-indexed cross-scenario diagnostic, not a budget-only intervention |
| Figure 4 | `figures/fig_ablation.{svg,png,pdf}` | Legacy fixed-generation run rows | Pooled effects descriptive; decisions remain scenario-specific |
| Figure 5 | `figures/fig_move_diagnostics.{svg,png,pdf}` | Legacy full/no-forward/no-backward/legacy-deletion rows | Event production and hypervolume kept in separate panels |
| Figure 6 | `figures/fig_nerc_backtest.{svg,png,pdf}` | Accepted NERC backtest | Descriptive external consistency |
| Table 6 | `derived_tables/p6_mtep_outcome_summary.csv` | Accepted MTEP16 backtest | Descriptive project-level outcome consistency; portfolio dependence not preserved |
| Figure 7 | `figures/fig_search_audit_efficiency.{svg,png,pdf}` | Legacy fixed-generation run rows | Native-unit quality, runtime, event-count, and co-occurrence panels; no composite score |
| Table 7 | `derived_tables/p6_quality_effort_tradeoff.csv` | Legacy run and inference rows | The 1.12% hypervolume difference and 2.74-times runtime factor form an unmatched quality--compute tradeoff |
| Figure 8 | `figures/fig_mtep_outcome_backtest.{svg,png,pdf}` | Accepted MTEP16 backtest | Broad and strict outcome definitions shown separately |
| Figure 9 | `figures/fig_atomic_substitution_controls.{svg,png,pdf}` | Legacy run and inference rows | PLS resolves in eight scenarios; forward insertion resolves only in three named scenarios; substitution comparisons remain unresolved |
| Table 8 | `derived_tables/p6_matched_evaluation_summary.csv` | Matched summary and inference rows | Primary 16-contrast paired family at exactly 3200 units |

Auxiliary regenerated tables are `p6_search_audit_efficiency.csv`, `p6_matched_time_summary.csv`, `p6_forward_substitution_resolution.csv`, `p6_hypervolume_sensitivity.csv`, and `p6_local_sensitivity_effects.csv`. They preserve the full legacy search/event readout, the separately corrected matched-time family, and the descriptive sensitivity scopes; they are not additional experiments.
