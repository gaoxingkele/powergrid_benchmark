# Deep-Revision Claim Contract

This document is the evidence contract for the current manuscript. It distinguishes the new immutable rolling-origin experiment from historical fixed-split, proxy, and presentation assets. It does not infer author metadata, funding, deployment evidence, or unobserved experiment outcomes.

## Title-to-Evidence Map

The current title is **“Cross-Series Context for 24-Step-Ahead Point Forecasting of Multi-Region Power Load: A Matched Rolling-Origin Component Evaluation.”** “Step” means a processed OPSD position, not necessarily one elapsed UTC hour after complete-row filtering.

| Title or contribution element | Direct evidence | Licensed statement | Excluded statement |
|---|---|---|---|
| Cross-series context | `experiments/p2_s3_identifiable_v1/config.json`, driver, model audit, and run rows define learned Poincaré, uniform-neighbor, Euclidean, fixed-scale, and target-self contexts with a common 48-dimensional context slot. | Cross-series content and weight form are controlled components. | Cross-series aggregation improves forecasting error. |
| 24-step-ahead point forecasting | The frozen horizon is 24 processed positions and each sample predicts one scalar target per series. The new run retains target UTC dates and records 43 discarded source rows before the 35,000-row cap. | Results concern scalar lead-24 prediction on the retained-row sequence. | A 24-value next-day trajectory or an uninterrupted 24-elapsed-hour lead at every sample. |
| Matched control | `results/model_audit.csv` records 29,815 parameters, a 100--64--1 head, 48-dimensional context, and the executed distance path for the proposed, target-self, and uniform-context arms. The frozen run uses common seeds, origins, optimizer, batches, epochs, and training exposure. | The proposed-versus-target-self and proposed-versus-uniform comparisons remove the historical smaller-head defect. | Identical wall-clock timing or full capacity matching to the historical external architecture roster. |
| Rolling-origin component evaluation | Eight frozen quarterly origins and five common seeds yield 240 method--origin--seed rows. Seeds are averaged within origin before exact paired inference. | The rolling origin is the outer analysis unit for the new component claims. | Treating hourly targets, countries, days, or seeds as independent temporal replications. |
| Component-level result | Table 4 and `paired_comparisons.csv` preserve the matched aggregation null, weighting-form nulls, adverse fixed-scale trend, and confounded independent-encoder result. | The fixed-split aggregation attribution does not replicate under the new estimand. | Upgrading a null to equivalence, claiming a best weighting form, or attributing the independent-encoder gap to sharing alone. |

The manuscript story is therefore a bounded component evaluation, not a superiority paper. The abstract, contributions, methods, results, discussion, limitations, and conclusion all give the new matched rolling-origin family authority over the aggregation-existence claim. Historical OPSD, SimBench, and Ausgrid results remain context and boundary evidence.

## Primary Estimand and Analysis Unit

For method $a$, rolling origin $o$, and seed $s$, the new primary error is $e^{\mathrm{MAPE}}_{aos}$. The five seeds are averaged within method--origin, and each contrast uses the eight paired differences

\[
d_o=\frac{1}{5}\sum_s e^{\mathrm{MAPE}}_{\mathrm{CSA},os}
    -\frac{1}{5}\sum_s e^{\mathrm{MAPE}}_{b,os}.
\]

The primary estimand is the mean of $d_o$ for CSA-Poincaré-Shared versus TargetSelfContext-Matched. WAPE is the frozen secondary metric; MAE, RMSE, and sMAPE are descriptive. The five-member primary MAPE family compares the proposed arm with target-self context, uniform cross-series context, Euclidean weighting, fixed scale, and the independent-encoder control. Exact two-sided sign-flip tests enumerate all $2^8$ origin sign assignments, and Holm adjustment covers those five MAPE tests. Pointwise 95% intervals bootstrap the eight origins with 20,000 deterministic resamples. No equivalence margin was specified.

The central observed contrast is:

| Metric | CSA-Poincaré-Shared | Target-self matched | Proposed minus control | Interval | Test scope |
|---|---:|---:|---:|---:|---|
| MAPE | 0.036640 | 0.036894 | -0.000253 (-0.69%) | [-0.000669, 0.000232] | raw exact p = 0.328; Holm p = 0.984 |
| WAPE | 0.036775 | 0.037109 | -0.000334 (-0.90%) | [-0.000778, 0.000153] | raw exact p = 0.227; secondary, not in the Holm family |

Six of eight MAPE origin differences favor the proposed arm, but the corrected comparison is unresolved. The paper therefore does not claim an aggregation benefit. The eight origins are adjacent portions of one six-country record spanning 2017--2018; quarterly spacing reduces test-block overlap but does not make them independent weather-year or system replications.

Historical fixed-split tests used seed-level scalars as their analysis units. They remain accurately reported as historical results, including the favorable selected-MLP and smaller-head TemporalOnly cells, but they do not override the new origin-level matched null.

## Comparison Budget and Data Visibility

The new confirmatory budget was frozen before outcome inspection:

- dataset/task: OPSD six-country scalar lead 24 only;
- methods: six component-identification arms;
- temporal origins: eight quarterly UTC anchors from 2017-01-01 through 2018-10-01;
- seeds: {11, 23, 47, 59, 71} for every method--origin cell;
- test exposure: 672 processed origins per rolling origin, six targets per processed origin, no test stride;
- training: stride 3, training targets strictly before each rolling origin, per-origin normalization, final 15% validation, eight completed epochs, common batch size and manual eager Adam;
- inference: origin-level MAPE family; WAPE secondary.

This produces 240 raw run rows, 6,750 forecast-target-date audit rows, 48 seed-averaged origin rows, six leaderboard rows, and ten metric-specific comparison rows. `run_manifest.json` records the exact command, environment, source/config/driver hashes, row counts, and output hashes. `results/run_results.completed_snapshot.csv` is byte-identical to the final raw table.

The proposed, target-self, uniform, Euclidean, and fixed-scale shared-encoder arms all instantiate 29,815 parameters and the same head. Target-self and uniform controls also execute the parameterized distance path as a zero-weight audit computation. The independent-encoder arm matches 29,815 total parameters and the same downstream head, but its six narrower encoders have an estimated 20,304 encoder multiply-accumulates per unique origin versus 124,416 for the shared encoder. It is not a compute-matched isolation of sharing.

The new family deliberately excludes MLP, LSTM, TCN, DLinear, PatchTST-lite, SimBench, Ausgrid, and lead 1. This narrows confirmation instead of treating historical three-seed screens or unmatched architectures as equal-strength controls. Historical external comparisons retain their original seed and capacity limitations.

The hashed source is the local OPSD `time_series_60min_singleindex.csv`. The parser scanned 35,043 source rows, discarded 43 with a missing or nonnumeric selected-country value, and retained 35,000. Filtering occurs before all splits. Consequently, rolling windows and leads count retained positions and can cross UTC gaps. No interpolation or imputation is applied. The current run reconstructs only the discarded count before reaching its retained-row cap; it does not establish missingness robustness.

## Negative and Null Results

These findings must remain visible and retain their qualifiers:

| Finding | Evidence and correct scope | Prohibited upgrade |
|---|---|---|
| Matched aggregation null | Proposed MAPE 0.036640 versus target-self 0.036894; difference -0.000253, interval crosses zero, Holm p = 0.984. WAPE is also unresolved (raw p = 0.227). | “Aggregation helps,” equivalence, or general cross-series superiority. |
| Uniform-context null | Proposed-minus-uniform MAPE -0.000066, Holm p = 0.984; WAPE raw p = 0.422. | Learned attention beats informative uniform cross-series pooling. |
| Euclidean-weight null | Proposed-minus-Euclidean MAPE -0.000009, Holm p = 0.984; four origins favor each arm. | Poincaré geometry is superior or equivalent. |
| Fixed-scale adverse trend | Fixed scale has lower mean MAPE and WAPE. Proposed-minus-fixed MAPE is +0.000041 with Holm p = 0.0625; WAPE is higher at all eight origins with raw p = 0.0078. | Learned scale helps; secondary WAPE cannot replace the corrected primary decision. |
| Independent-encoder adverse result with confounding | Shared is better at all eight origins; MAPE Holm p = 0.0391 and WAPE raw p = 0.0078. Hidden-width allocation and encoder arithmetic differ. | Parameter sharing causes the improvement or the control is compute-matched. |
| Historical fixed-split conflict | The earlier fixed split favored the proposed arm over selected MLP and smaller-head TemporalOnly. | Treating optimization seeds on one split as temporal replication or ignoring the new matched null. |
| Historical boundary results | OPSD lead 1 favors MLP; SimBench does not establish MLP superiority or parity at either lead; exact-hierarchy Ausgrid favors DLinear under unequal exposure. | General forecasting superiority, SimBench parity, or capacity-controlled Ausgrid causality. |
| Reconciliation result | Bottom-up, top-down, and OLS enforce exact hierarchy coherence. | Coherence as evidence of forecasting accuracy or deployment value. |

The uniform, Euclidean, and fixed-scale arms jointly support only the bounded conclusion that no learned weighting advantage is established by the frozen primary family. Combined ablations do not identify the best individual mechanism. Historical proxy rolling tables remain proxy evidence and are not independent replicates of the new neural run.

## Shared Assets and Independent Contribution

`MANUSCRIPT.md`, the journal-submission TeX/PDF, submission previews, duplicated figure directories, and derived plotting tables are packaging or presentation variants, not independent evidence streams. `manuscript/ARTIFACT_STATUS.md` identifies the content master and records that the TeX was regenerated while the PDF and older submission preview could not be rebuilt in the current environment. Historical review files and changelogs are internal records. The historical `HyG-LoadFormer (neural)` label maps to the same full CSA configuration but does not make a prior run an independent replicate of `p2_s3_identifiable_v1`.

The new independent contribution is the immutable matched-control namespace, including its frozen configuration, driver, raw results, forecast-date audit, origin-level analysis, model audit, manifest, experiment report, and validation report. It repairs the historical head mismatch, equalizes seed support within the narrowed comparison family, and uses rolling origin as the outer unit. Its scientific contribution is the matched null and the resulting claim correction, not a new positive performance result.

Public OPSD, SimBench, and Ausgrid datasets remain provider-owned sources. Standard MAPE/WAPE/MAE/RMSE/sMAPE metrics, neural layers, Adam equations, exact sign-flip inference, Holm correction, and reconciliation transformations are not claimed as original. No companion Mintou project supplies an independent replicate for this paper.

## New or Rerun Experiments

One new experiment namespace was executed once:

- namespace: `experiments/p2_s3_identifiable_v1/`;
- status: completed;
- exact command and environment: `run_manifest.json`;
- raw factorial: 6 methods × 8 origins × 5 seeds = 240 rows;
- output reports: `EXPERIMENT_RESULT.md` and `VALIDATION_REPORT.md`;
- primary result: matched aggregation contrast unresolved after Holm correction;
- secondary result: WAPE agrees that target-self context is unresolved;
- weighting result: no primary-family learned-weight advantage; fixed scale has an adverse nominal trend;
- sharing result: shared arm is lower-error than the capacity-matched independent arm, but the comparison is confounded by width allocation and compute.

The execution used Python 3.12.13 and PyTorch 2.13.0+cu130 on one RTX 3090. Fixed CPU/CUDA seeds, deterministic cuDNN, disabled cuDNN benchmarking, and the recorded CUBLAS workspace configuration were used. Global deterministic-algorithm enforcement was unavailable because the preserved environment lacks `sympy`; this degradation is recorded in the manifest. No run was retried, tuned after outcome inspection, or overwritten.

An independent arithmetic audit rechecked output hashes, the 240-cell factorial, parameter counts, seed-to-origin aggregation, exact sign-flip p-values, and daily-to-run MAPE reconstruction without error. This is an analysis audit, not an independent experiment rerun. Reproducibility status remains `UNVERIFIED`, and no byte-for-byte replay claim is made.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED -- CRediT:** assign verified contributor roles to Jieyun Zheng, Linyao Zhang, Zhanghuang Zhang, Zhuolin Chen, and Ying Shi, and obtain approval from every author. No roles were inferred.
- **AUTHOR INPUT REQUIRED -- funding:** provide the verified funder, grant number, and APC funder, or an author-confirmed no-external-funding statement. No funding status was inferred.
- **Author metadata confirmation:** verify author spelling and order, the single printed affiliation, correspondence details, and rendered non-Latin names against author-approved records.
- **Persistent archive:** no verified repository URL or DOI is present. Deposit and verify the final evidence package before making a persistent-public-archive claim.
- **Independent rerun:** a separate immutable rerun is required before changing the new namespace from `UNVERIFIED` to `VERIFIED`.
- **Final author approval:** acknowledgments, conflicts, AI-use disclosure, data-availability wording, and responsibility language require human confirmation.

These blockers are preserved rather than replaced with guessed metadata. They block submission-ready status but do not justify changing the scientific results.
