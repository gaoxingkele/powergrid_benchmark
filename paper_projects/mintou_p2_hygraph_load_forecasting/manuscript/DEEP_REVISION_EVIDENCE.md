# Deep-Revision Claim Contract

This document is the evidence contract for the current manuscript. It distinguishes the accepted rolling-origin experiment from fixed-split, proxy, and presentation assets. It does not infer author metadata, funding, deployment evidence, or unobserved experiment outcomes.

## Title-to-Evidence Map

The locked title is **“Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting.”** It is the immutable P4 identity, not a statement that the current implementation already satisfies the title-method claim. The current CSA-LoadNet is a baseline: it is neither a graph convolutional network (GCN) nor a hyperbolic graph convolutional network (HGCN). It uses dense cross-series attention with Poincaré-distance weighting and has no accepted adjacency-based graph convolution or hyperbolic graph message passing. No GCN or HGCN result exists in this stage.

The authoritative P4-C01--P4-C08 statuses and wording boundaries are registered in `checkpoints/2026-09-03_mdpi_wave0/CLAIM_EVIDENCE_REGISTER.md` and bound here to the manuscript contract:

| Claim ID | Bound status | Direct evidence and licensed scope | Excluded statement or next gate |
|---|---|---|---|
| P4-C01 | `SUPPORTED_CURRENT` | `experiments/p2_s3_identifiable_v1/config.json` and accepted outputs support scalar lead-24 forecasts over eight quarterly blocks and five common seeds, with seeds averaged within block. | Forecast positions, targets, countries, days, or seeds are not independent temporal replicates. |
| P4-C02 | `NOT_SUPPORTED` | The current implementation is the CSA/attention baseline, not a GCN. | A genuine adjacency-based Euclidean GCN must be implemented before describing the method as a graph convolutional network. |
| P4-C03 | `NOT_SUPPORTED` | Poincaré distance supplies attention weights; full hyperbolic mapping, convolution, and graph message passing are absent. | CSA-Poincaré must not be renamed or described as an HGCN. |
| P4-C04 | `UNRESOLVED` | The matched Poincaré-weighted CSA contrast is unresolved (MAPE 0.036640 versus 0.036894; Holm-adjusted p = 0.984). | No improvement, superiority, or equivalence claim is licensed. |
| P4-C05 | `NOT_SUPPORTED` | DLinear has lower error in the separately scoped exact-hierarchy comparison and remains a mandatory strong baseline. | The current approach must not be said to beat strong non-graph baselines. |
| P4-C06 | `FUTURE_HYPOTHESIS` | No accepted graph-data mapping has been frozen. | Graph provenance, node/edge, time-split, and leakage audits are required before a graph can be described as meaningful or leakage-free. |
| P4-C07 | `FUTURE_HYPOTHESIS` | No HGCN experiment or result exists. | A genuine HGCN and Euclidean GCN sanity baseline are required before testing or reporting an HGCN forecasting benefit. |
| P4-C08 | `SUPPORTED_WITH_SCOPE` | The target-route review and Electronics template support only a plausible scope route for a rebuilt graph-learning study. | Journal scope fit is not an acceptance-probability claim. |

The current manuscript evidence is therefore a bounded CSA baseline component evaluation, not evidence for the GCN/HGCN method named in the locked title and not a superiority paper. Until the title-method gate passes, the abstract, contributions, methods, results, discussion, limitations, and conclusion must keep that boundary explicit and give the matched rolling-origin family authority over the aggregation-existence claim. Fixed-split OPSD, SimBench, and Ausgrid results remain context and boundary evidence.

## Primary Estimand and Analysis Unit

For method $a$, quarterly evaluation block $o$, and seed $s$, the rolling-origin primary error is $e^{\mathrm{MAPE}}_{aos}$. A forecast origin is an individual processed index inside a block; it is not the outer analysis unit. The five seeds are averaged within method--block, and each contrast uses the eight paired differences

\[
d_o=\frac{1}{5}\sum_s e^{\mathrm{MAPE}}_{\mathrm{CSA},os}
    -\frac{1}{5}\sum_s e^{\mathrm{MAPE}}_{b,os}.
\]

The primary estimand is the mean of $d_o$ for CSA-Poincaré-Shared versus TargetSelfContext-Matched. WAPE is the frozen secondary metric; MAE, RMSE, and sMAPE are descriptive. The five-member primary MAPE family compares the proposed arm with target-self context, uniform cross-series context, Euclidean weighting, fixed scale, and the independent-encoder control. Exact two-sided sign-flip tests enumerate all $2^8$ block sign assignments, rely on sign-exchangeability under the no-effect null, and receive Holm adjustment across those five MAPE tests. Pointwise 95% intervals use 20,000 deterministic resamples of the eight block differences. Because the blocks share one record and nested training histories, the intervals are descriptive uncertainty summaries, not evidence of independent weather-year replication. No equivalence margin was specified.

The central observed contrast is:

| Metric | CSA-Poincaré-Shared | Target-self matched | Proposed minus control | Interval | Test scope |
|---|---:|---:|---:|---:|---|
| MAPE | 0.036640 | 0.036894 | -0.000253 (CSA mean is 0.69% lower; target-self mean is the denominator) | [-0.000669, 0.000232] | raw exact p = 0.328; Holm p = 0.984 |
| WAPE | 0.036775 | 0.037109 | -0.000334 (CSA mean is 0.90% lower; target-self mean is the denominator) | [-0.000778, 0.000153] | raw exact p = 0.227; secondary, not in the Holm family |

Six of eight MAPE block differences favor the proposed arm, but the corrected comparison is unresolved. The paper therefore does not claim an aggregation benefit. The eight 672-position test blocks are disjoint, as recorded by their processed-row anchor indices, but their expanding training histories are nested within one six-country record spanning 2017--2018. Disjoint test indices do not make them independent weather-year or system replications.

Fixed-split tests used seed-level scalars as their analysis units. Their standard deviations and tests quantify optimization variation conditional on one split, not uncertainty over temporal splits. They retain the favorable selected-MLP and smaller-head TemporalOnly cells but do not override the block-level matched null.

## Comparison Budget and Data Visibility

The rolling-origin confirmatory budget was frozen before outcome inspection:

- dataset/task: OPSD six-country scalar lead 24 only;
- methods: six component-identification arms;
- temporal blocks: eight quarterly UTC anchors from 2017-01-01 through 2018-10-01;
- seeds: {11, 23, 47, 59, 71} for every method--block cell;
- test exposure: 672 processed forecast origins per block, six targets per forecast origin, no test stride;
- training: stride 3, training targets strictly before each rolling origin, per-origin normalization, final 15% validation, eight completed epochs, common batch size and manual eager Adam;
- inference: block-level MAPE family; WAPE secondary.

This produces 240 raw run rows, 6,750 date-aggregated forecast-target audit rows, 48 seed-averaged block rows, six leaderboard rows, and ten metric-specific comparison rows. `run_manifest.json` records the exact command, environment, source/config/driver hashes, row counts, and output hashes. `results/run_results.completed_snapshot.csv` is byte-identical to the final raw table. On Windows checkout, the two Markdown reports have CRLF line endings while their manifest entries use canonical LF bytes; the artifact generator accepts them only when LF normalization reproduces the recorded digest. All CSV outputs match their recorded raw-byte hashes.

The proposed, target-self, uniform, Euclidean, and fixed-scale shared-encoder arms all instantiate 29,815 parameters and the same head. Target-self and uniform controls also execute the parameterized distance path as a zero-weight audit computation. The independent-encoder arm matches 29,815 total parameters and the same downstream head, but its six narrower encoders have an estimated 20,304 encoder multiply-accumulates per unique forecast origin versus 124,416 for the shared encoder. It is not a compute-matched isolation of sharing.

Baseline fairness is therefore tiered rather than global:

| Comparison | Matched dimensions | Unmatched dimensions | Licensed use |
|---|---|---|---|
| Proposed vs. target-self | Parameters, 100--64--1 head, 48-dimensional context slot, data, optimizer, batches, epochs, seeds, and executed parameterized path | Identical wall-clock timing is not asserted | Primary aggregation-existence comparison |
| Proposed vs. uniform, Euclidean, or fixed scale | Shared encoder, head, capacity, data, training budget, and seed/block cells | The controls implement different context or score rules by design | Combined family-level statement that no tested learned-weight advantage is established |
| Shared vs. independent encoder | Total parameters, downstream head, data, training budget, and seed/block cells | Per-series hidden widths, calibration allocation, and encoder arithmetic | Confounded boundary result; no causal sharing claim |
| Proposed vs. historical external architectures | Common task split and disclosed evaluation surface within each historical study | Capacity, epoch budget, and, on Ausgrid, training stride/exposure | Contextual ranking and adverse boundary evidence only |

The rolling-origin family deliberately excludes MLP, LSTM, TCN, DLinear, PatchTST-lite, SimBench, Ausgrid, and lead 1. This narrows confirmation instead of treating the three-seed screen or unmatched architectures as equal-strength controls. Fixed-split external comparisons retain their original seed and capacity limitations.

The hashed source is the local OPSD `time_series_60min_singleindex.csv`. The parser scanned 35,043 source rows, discarded 43 with a missing or nonnumeric selected-country value, and retained 35,000. Filtering occurs before all splits. Consequently, rolling windows and leads count retained positions and can cross UTC gaps. No interpolation or imputation is applied. The accepted outputs retain target dates aggregated within the audit table, not a complete list of discarded timestamps. The current run reconstructs only the discarded count before reaching its retained-row cap; it does not establish missingness robustness.

## Negative and Null Results

These findings must remain visible and retain their qualifiers:

| Finding | Evidence and correct scope | Prohibited upgrade |
|---|---|---|
| Matched aggregation null | Proposed MAPE 0.036640 versus target-self 0.036894; difference -0.000253, interval crosses zero, Holm p = 0.984. The ratio-of-means reduction is 0.69% using the target-self mean as denominator. WAPE is also unresolved (raw p = 0.227). | “Aggregation helps,” equivalence, or general cross-series superiority. |
| Uniform-context null | Proposed-minus-uniform MAPE -0.000066, Holm p = 0.984; WAPE raw p = 0.422. | Learned attention beats informative uniform cross-series pooling. |
| Euclidean-weight null | Proposed-minus-Euclidean MAPE -0.000009, Holm p = 0.984; four origins favor each arm. | Poincaré geometry is superior or equivalent. |
| Fixed-scale adverse trend | Fixed scale has lower mean MAPE and WAPE. Proposed-minus-fixed MAPE is +0.000041 with Holm p = 0.0625; WAPE is higher at all eight origins with raw p = 0.0078. | Learned scale helps; secondary WAPE cannot replace the corrected primary decision. |
| Independent-encoder adverse result with confounding | Shared is better at all eight origins; MAPE Holm p = 0.0391 and WAPE raw p = 0.0078. Hidden-width allocation and encoder arithmetic differ. | Parameter sharing causes the improvement or the control is compute-matched. |
| Fixed-split conflict | The OPSD lead-24 fixed split favored the proposed arm over selected MLP by 4.07% using the MLP mean as denominator and over smaller-head TemporalOnly by 6.49% using the TemporalOnly mean. Seed uncertainty is conditional on that split. | Treating optimization seeds on one split as temporal replication or ignoring the matched rolling-origin null. |
| Boundary results | OPSD lead 1 favors MLP; SimBench does not establish MLP superiority or parity at either lead; exact-hierarchy Ausgrid favors DLinear under unequal exposure. | General forecasting superiority, SimBench parity, or capacity-controlled Ausgrid causality. |
| Reconciliation result | Bottom-up, top-down, and OLS enforce exact hierarchy coherence. Under common OLS, DLinear mean hierarchy-weighted sMAPE is 0.280466 versus 0.289488 for CSA-LoadNet; CSA is 3.22% higher using DLinear as denominator (Holm p = 0.000985). Seed uncertainty is conditional on one split. | Coherence as evidence of forecasting accuracy or deployment value. |

The aggregation-existence conclusion comes only from the proposed-versus-target-self matched contrast. The uniform, Euclidean, and fixed-scale arms jointly support only the bounded conclusion that no tested learned weighting advantage is established by the frozen primary family. Combined ablations do not identify the best individual mechanism, allocate the unresolved family result among geometry and scale, or license equivalence. Proxy rolling tables remain proxy evidence and are not independent replicates of the accepted neural run.

## Shared Assets and Independent Contribution

`MANUSCRIPT.md`, the journal-submission TeX/PDF, submission previews, duplicated figure directories, and derived plotting tables are packaging or presentation variants, not independent evidence streams. `manuscript/ARTIFACT_STATUS.md` identifies the content master and records the current build status. Review files and changelogs are internal records. Storage labels and run namespaces map evidence files to the same scientific configurations but do not create independent replications.

The independent contribution is the matched-control rolling-origin experiment, including its frozen configuration, driver, raw results, date-aggregated forecast-target audit, block-level analysis, model audit, manifest, experiment report, and validation report. It repairs the fixed-split head mismatch, equalizes seed support within the narrowed comparison family, and uses the quarterly evaluation block as the outer unit. Its scientific contribution is the matched null and resulting claim correction, not a positive performance result, a new forecasting theory, or a state-of-the-art architecture claim.

Public OPSD, SimBench, and Ausgrid datasets remain provider-owned sources. Standard MAPE/WAPE/MAE/RMSE/sMAPE metrics, neural layers, Adam equations, exact sign-flip inference, Holm correction, and reconciliation transformations are not claimed as original. No companion Mintou project supplies an independent replicate for this paper.

## New or Rerun Experiments

One rolling-origin experiment namespace was executed once:

- namespace: `experiments/p2_s3_identifiable_v1/`;
- status: completed;
- exact command and environment: `run_manifest.json`;
- raw factorial: 6 methods × 8 quarterly blocks × 5 seeds = 240 rows;
- output reports: `EXPERIMENT_RESULT.md` and `VALIDATION_REPORT.md`;
- primary result: matched aggregation contrast unresolved after Holm correction (CSA mean 0.69% lower using target-self as denominator; Holm p = 0.984);
- secondary result: WAPE agrees that target-self context is unresolved;
- weighting result: no primary-family learned-weight advantage; fixed scale has an adverse nominal trend;
- sharing result: shared arm is lower-error than the parameter-matched independent arm, but the comparison is confounded by width allocation and compute.

The execution used Python 3.12.13 and PyTorch 2.13.0+cu130 on one RTX 3090. Fixed CPU/CUDA seeds, deterministic cuDNN, disabled cuDNN benchmarking, and the recorded CUBLAS workspace configuration were used. Global deterministic-algorithm enforcement was unavailable because the preserved environment lacks `sympy`; this degradation is recorded in the manifest. No run was retried, tuned after outcome inspection, or overwritten.

The deterministic artifact generator verifies the accepted manifest and its recorded outputs before rebuilding `p2_fixed_split_summary.csv`, `p2_rolling_origin_controls.csv`, `p2_reconciliation_summary.csv`, `p2_cross_setting_ranks.csv`, `p2_percentage_denominators.csv`, `p2_rolling_stability.csv`, `p2_runtime_accuracy.csv`, `p2_effect_summary.csv`, and all result figures. `p2_artifact_manifest.json` records the source and output hashes. This is an arithmetic and packaging audit, not an independent experiment rerun. Reproducibility status remains `UNVERIFIED`, and no byte-for-byte replay claim is made. The S5 closure independently recomputed the five raw sign-flip p-values and Holm adjustments from `origin_metrics.csv`; this checks arithmetic consistency, not experimental replication.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED -- CRediT:** assign verified contributor roles to Zheng Jieyun, Zhang Linyao, Zhang Zhanghuang, Chen Zhuolin, and Shi Ying, and obtain approval from every author. No roles were inferred.
- **AUTHOR INPUT REQUIRED -- funding:** provide the verified funder, grant number, and APC funder, or an author-confirmed no-external-funding statement. No funding status was inferred.
- **Author metadata confirmation:** the order is locked as Zheng Jieyun, Zhang Linyao, Zhang Zhanghuang, Chen Zhuolin, and Shi Ying, with Zheng Jieyun first and corresponding. Verify spelling, the single printed affiliation, the correspondence address, and rendered non-Latin names against author-approved records; do not alter the locked order while doing so.
- **Persistent archive:** no verified repository URL or DOI is present. Deposit and verify the final evidence package before making a persistent-public-archive claim.
- **Independent rerun:** a separate immutable rerun is required before changing the new namespace from `UNVERIFIED` to `VERIFIED`.
- **Bibliography and novelty:** the full bibliography, claim-to-source alignment, systematic novelty search, similarity screening, and external domain-expert review were not available in this isolated stage and remain `UNVERIFIED`.
- **Current PDF:** source regeneration reached the journal build helper, but the discovered MiKTeX installation required first-run setup and exited before producing a current PDF. Until a fresh build succeeds, the existing PDFs remain stale and are not evidence of current manuscript content.
- **Current quantitative-figure rebuild:** the retained P2 S4 tables and result figures match the checkout-normalized hashes recorded for unchanged scientific inputs, but the S5 generator invocation could not load Pillow's `_imaging` extension under the only available Python 3.14 runtime. A fresh S5 rebuild remains environment-blocked and is not claimed.
- **Final author approval:** acknowledgments, conflicts, AI-use disclosure, data-availability wording, and responsibility language require human confirmation.

These blockers are preserved rather than replaced with guessed metadata. They block submission-ready status but do not justify changing the scientific results.
