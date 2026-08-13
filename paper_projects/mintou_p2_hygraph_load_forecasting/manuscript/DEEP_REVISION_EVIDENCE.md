# Deep-Revision Claim Contract

This document is the narrative evidence contract for the current manuscript. It records what the observable files in this isolated worktree do and do not support. It does not promote manuscript statements or rendered figures to independent experimental evidence, and it does not fill human-owned metadata by inference.

## Title-to-Evidence Map

The stabilized title is **“Cross-Series Aggregation for 24-Hour-Ahead Point Forecasting of Multi-Region Power Load: A Component-Level Evaluation.”** It is deliberately neutral about superiority and names the implemented scalar-target task.

| Title or story element | Observable anchor | Licensed statement | Excluded statement |
|---|---|---|---|
| Cross-series aggregation | `MANUSCRIPT.md`, Sections 4.2 and 4.4, defines the context vector and the TemporalOnly switch that removes it; Sections 6.1–6.3 report the associated comparison. | Aggregation existence is an independently switched component, and the full model separates from TemporalOnly on OPSD at lead 24 under the reported protocol. | A particular attention, distance, or inverse-temperature parameterization is superior. |
| 24-hour-ahead point forecasting | `MANUSCRIPT.md`, Table 1 and Section 3.1, defines each target as one scalar $y_{i,t+24}$; Sections 6.1, 8, and 9 confine the positive claim to that OPSD task. | The positive result is setting-specific to one scalar target 24 hours after each origin. | Calling the experiment a 24-point next-day trajectory forecast or claiming general short-horizon/all-horizon superiority. |
| Multi-region | `MANUSCRIPT.md`, Table 1, lists the six-country OPSD pool and eight-profile SimBench pool. | The method is evaluated on pools of related load series. | A universal result over arbitrary regions, grids, or customer hierarchies. |
| Component-level evaluation | `MANUSCRIPT.md`, Section 4.4, separates aggregation existence, weight form, inverse-temperature, and sequence-phase switches; Figure 3 and Sections 6.2–6.3 report their distinct outcomes. | The evaluation distinguishes the aggregation-existence question from the weight-form question. | Treating the combined ablation block as proof that every individual mechanism helps. |
| Exact hierarchy as a boundary study | `MANUSCRIPT.md`, Sections 3.2 and 6.4, separates forecast error from coherence under common reconciliation. | The Ausgrid study supplies a negative transfer boundary and a coherence comparison. | Hierarchical forecasting superiority, dispatch performance, or deployment evidence. |

The three manuscript contributions follow the same contract: (1) the method contribution is a component-identifiable forecaster, not a new geometry claimed superior; (2) the experiment contribution is a multi-setting, temporally split component evaluation; and (3) the result contribution is a bounded map containing one supported OPSD 24-hour-ahead point aggregation result plus unresolved and adverse settings. The abstract, Contributions list, Results, Discussion, Limitations, and Conclusion must retain these same qualifiers.

## Primary Estimand and Analysis Unit

The component estimand that carries the paper's central scientific story is the difference in OPSD lead-24 MAPE between the full CSA-LoadNet configuration and TemporalOnly, which removes cross-series aggregation while retaining the temporal path. Every origin contributes one $t+24$ scalar target per series; no next-day trajectory estimand exists. The targeted external benchmark contrast is CSA-LoadNet versus MLP on the same dataset, lead, origin split, primary metric, and ten-seed set. It is not a capacity-matched estimand: CSA-LoadNet has 29,815 instantiated parameters on OPSD and MLP has 30,465, with different maximum epoch counts.

The reported inferential unit is one seed-level scalar primary-error summary on a fixed chronological test-target sequence. `MANUSCRIPT.md`, Sections 5.2–5.3, states ten common seeds for the decision set and uses two-sided Mann–Whitney U tests with Holm correction; paired sign-flip tests are sensitivity analyses. Hourly targets are not treated as independent experimental replications. The design therefore supports variation across the reported training seeds on one split, not variation across independently sampled datasets, regions, or weather years.

Metric roles are fixed before cross-setting interpretation:

| Dataset/task | Primary metric | Permitted use |
|---|---|---|
| OPSD, 1 h and 24 h point leads | MAPE | The OPSD lead-24 component and MLP contrasts carry the positive claim; OPSD 1 h is a negative boundary. |
| SimBench, 1 h and 24 h point leads | normalized MAE | Near-zero profile values make MAPE descriptive rather than rank-determining; no MLP superiority or parity claim is licensed. |
| Exact Ausgrid hierarchy, 24 h point lead | hierarchy-weighted sMAPE | Compares forecasting accuracy while giving leaf, region, and root levels equal weight; coherence violation is a separate structural outcome. |

No cross-dataset pooled error or average rank is a primary estimand because MAPE, normalized MAE, and hierarchy-weighted sMAPE have different denominators and meanings. The title is therefore task-descriptive, not a claim of overall dominance.

## Comparison Budget and Data Visibility

The comparison budget stated in `MANUSCRIPT.md` is: ten seeds for CSA-LoadNet, five single-switch ablations, and the targeted MLP comparator on OPSD and SimBench; a separate preliminary three-seed screen for four compact neural families; and ten seeds per model and reconciliation regime in the exact Ausgrid study. The preliminary screen used the same fixed test trajectory to select MLP for confirmation. It is supporting model-selection evidence only, creates test visibility for comparator choice, and must not be described as equal-strength or preregistered confirmation.

The inspected model source fixes the exact capacities and maximum epochs reported in Manuscript Table 2. OPSD and SimBench use training-origin stride 3 for every trained model. In the v8 hierarchy driver, CSA variants receive stride 6, but the external baseline routine retains its module-level stride 3; the results writer nevertheless records the stride-6 sample count for every row. Consequently, the Ausgrid result is not an equal-exposure comparison, and the CSV `train_samples` column is not authoritative for baseline exposure.

Data visibility is also asymmetric across operations. Per-series normalization and top-down reconciliation proportions use the pre-test segment only. OPSD/SimBench row-validity filters run before splitting. Ausgrid completeness and top-energy leaf selection use all three years, including the eventual test period; this is not a train-only structural filter. The raw public dataset cache is not present in this isolated worktree, so discarded-row counts and independent reruns cannot be reconstructed here.

The authoritative source and evidence scaffold is visible read-only at `../../papers/mintou/mintou_p2_hygraph_load_forecasting/`. The files below were inspected for this contract. Files under `manuscript/derived_tables/` are convenient presentation derivatives; the `../../papers/.../evidence/` files are the claim anchors.

| Asset | Visible here | Evidential scope |
|---|---|---|
| `../../papers/.../evidence/runs/real_{opsd,simbench}_hyg_neural_results.csv`, `real_{opsd,simbench}_v7_extra_seed_results.csv`, and the MLP rows in `real_{opsd,simbench}_neural_results.csv` | Yes; together they contain 280 decision-set rows: 7 methods × 2 horizons × 10 seeds × 2 datasets. | Direct run-level support for the non-hierarchical decision set. The manuscript's earlier count of 420 was not supported by this arithmetic and has been corrected to 280. |
| `../../papers/.../evidence/runs/real_ausgrid_exact_hierarchy_v8_results.csv` | Yes; 440 rows: 11 methods × 4 reconciliation regimes × 10 seeds. | Direct run-level support for the exact-hierarchy comparison budget. The identically sized `_partial.csv` copy is not a second experiment. |
| `../../papers/.../evidence/tables/real_opsd_v7_leaderboard.csv`, `real_simbench_v7_leaderboard.csv`, `real_p2_primary_inference_v2.csv`, `real_p2_paired_sensitivity_v2.csv`, and the v8 Ausgrid leaderboard/significance tables | Yes. | Direct table-level anchors for the reported means, corrected decisions, effect summaries, and sensitivity analyses. |
| `../../papers/.../src/configs/real_p2_v7_config.json` and `real_ausgrid_exact_hierarchy_v8_config.json` | Yes. | Machine-readable support for the ten-seed lists, model sets, primary metrics, exact hierarchy, and reconciliation labels. The older `real_hyg_neural_config.json` records only the initial three-seed v6 configuration and uses the historical curvature terminology. |
| `../../papers/.../evidence/source/real_opsd_source_profile.csv` and `real_simbench_source_profile.csv` | Yes. | Direct provenance for source files, row counts, series pools, and chronological boundaries. Their historical dependency-policy labels describe the earlier data preparation records, not the later neural execution environment. |
| `../../src/powergrid_benchmark/mintou_real_load_forecasting.py`, `mintou_hyg_neural.py`, `mintou_neural_forecasting.py`, and `mintou_hierarchy_reconciliation.py` | Yes. | Direct source anchors for scalar targets, row filtering, hourly aggregation, sequence-index phase features, model capacities, training strides, full-record Ausgrid selection, and the four reconciliation transformations. |
| `derived_tables/p2_runtime_accuracy.csv`, `p2_cross_setting_ranks.csv`, and `p2_rolling_stability.csv` | Yes. | Presentation summaries only. The rolling table is historical/proxy robustness evidence and is not the current ten-seed decision set. |
| Figures and generated TeX/PDF copies | Yes. | Presentation and build artifacts, not independent replications of the source results. |

The narrative acceptance phase checks this contract and the manuscript story; it does not by itself re-establish every numerical result. Public source URLs establish dataset provenance at the citation level, while the source profiles, configurations, and run tables establish the processed-series, split, and result record used here. The run-level and table-level files are related layers of one evidence chain and are not independent replications.

## Negative and Null Results

These findings are part of the contribution and must remain visible:

| Finding recorded in `MANUSCRIPT.md` | Correct scope | Prohibited upgrade |
|---|---|---|
| Poincaré-distance, Euclidean-distance, equal-weight, and fixed-distance-scale variants do not separate after the reported correction in any tested setting (Section 6.3). | No weighting-form difference was resolved at the available precision and budget. The historical FixedCurvature key sets inverse-temperature $\tau_i=1$; it does not change metric curvature. | Poincaré, learned scale, fixed scale, or equal weighting is superior; or the variants are equivalent. No equivalence margin was prespecified. |
| The no-sequence-phase control (historical label NoCalendar) has the best nominal OPSD 24 h mean but is not separated from the full model (Section 6.1). | Sequence-phase contribution is unresolved. | Row-index phase features help, hurt, or are unnecessary. |
| OPSD 1 h significantly favors MLP (Sections 6.5 and 8). | A short-horizon negative boundary. | General load-forecasting superiority. |
| SimBench does not separate CSA-LoadNet from MLP at either horizon, with the MLP mean ahead at 24 h (Sections 6.5 and 8). | No superiority or parity claim. | Treating non-significance as equality or successful transfer. |
| Exact-hierarchy Ausgrid favors DLinear under the reported comparison while bottom-up, top-down, and OLS achieve coherence (Sections 6.4 and 8). | Coherence can be enforced without making CSA-LoadNet the most accurate forecaster; the ranking is qualified by unequal capacity, epochs, and training-origin strides. | Hierarchical accuracy superiority, a capacity-controlled DLinear claim, or reconciliation as evidence of model accuracy. |
| Full-record Ausgrid leaf selection, unspecified SimBench/Ausgrid timezones, row-index phase features, and unrecorded discard counts remain part of the processed-data contract. | Explicit data-visibility and preprocessing limitations. | Claiming a train-only Ausgrid filter, localized civil-time/DST handling, or missingness robustness. |
| Alternative weather years, split positions, larger pools, MinT, exogenous weather, and architecture-specific tuning are untested (Section 8). | Explicit external-validity and budget limitations. | Robustness, deployment readiness, or universal mechanism claims. |

The weight-form ablations are combined evidence for the joint bounded conclusion that no tested form separated here. They do not identify which form is best, and historical rolling results do not broaden that conclusion.

## Shared Assets and Independent Contribution

The master manuscript, journal-submission copy, submission-preview copy, duplicated figure scripts, and rendered figures are packaging variants of shared assets. They must not be counted as independent evidence streams. The historical reviews and changelog document the revision path but are internal records rather than experimental observations. The read-only scaffold file `../../papers/mintou/mintou_p2_hygraph_load_forecasting/PAPER.md` still carries the earlier “Cross-Series Attention” title; its aggregation-centered claim boundary remains useful, but that legacy title is not the current manuscript title.

OPSD, SimBench, and Ausgrid are public source datasets credited to their providers. Baseline architectures, reconciliation methods, and standard error metrics are prior work. The manuscript's independent scientific contribution is limited to the component-identifiable CSA-LoadNet testbed, the scoped comparison design that separates aggregation existence from aggregation-weight form, and the resulting bounded empirical map. The exact-hierarchy construction and common reconciliation comparison are an additional study-specific evaluation asset, not evidence of cross-project or field-wide superiority.

No companion Mintou project supplies an independent replicate for this paper in the current contract. Reuse of datasets, scripts, formatting assets, or historical labels must remain disclosed as reuse rather than described as an independent contribution.

## New or Rerun Experiments

No experiment was newly run or rerun in this stage, and no experimental outcome, p-value, interval, dataset record, expert label, or deployment claim was newly generated. No reported error or inferential value was changed. Exact parameter counts were added by deterministic arithmetic over the inspected layer definitions, not by fitting models. The stage corrects the task label, temperature/scale semantics, preprocessing/time contract, capacity disclosure, training-exposure disclosure, and reconciliation specification.

The raw OPSD, SimBench, and Ausgrid dataset cache referenced by the source code is absent from this isolated worktree. Independent preprocessing counts and experiment reruns were therefore not possible here. Future evidence tasks include reconstructing discard/imputation counts from the raw sources, rerunning Ausgrid with train-only leaf selection and matched training-origin exposure, repeating the primary analysis across additional chronological/weather-year splits, predeclaring an equivalence margin if equivalence among weight forms is scientifically important, and evaluating untested reconciliation or exogenous-input variants. Until those tasks are performed, the current limitations remain binding.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED — CRediT:** `MANUSCRIPT.md`, Author Contributions, still requires assignment of verified roles and approval from every listed author. No roles were inferred in this stage.
- **AUTHOR INPUT REQUIRED — funding:** `MANUSCRIPT.md`, Funding, still requires a verified funder, grant number, and APC funder, or an author-confirmed no-external-funding statement. No funding status was inferred.
- **Author metadata confirmation:** the master currently prints an author roster, one affiliation, and correspondence details, but this isolated worktree contains no documentary source or approval record for them. The corresponding authors must verify spelling, ordering, affiliation coverage, correspondence, and the rendered non-Latin names before submission.
- **Persistent archive:** the Data Availability Statement says the supplementary package is available from the corresponding author and that a persistent archive can be supplied. No repository URL or DOI is visible here; authors must deposit and verify the final evidence package before making a public-archive claim.
- **Final author approval:** the acknowledgments, conflicts statement, AI-use disclosure, and responsibility language require confirmation by the authors; this narrative stage cannot provide that human attestation.

These blockers are preserved rather than replaced with guessed metadata. They block submission-ready status but do not justify changing the scientific result.
