# Supplementary Note: Post-Unblinding Development-Only CF Calibration

## S1. Chronology and evidence boundary

The v0.3.1 formal test result was already known before this exploration began. The guarded development-only analysis started on 8 August 2026 at 17:29:45 Asia/Shanghai and completed at 17:43:04. It read only the 12-report development file (SHA-256 `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`) and the earlier development-decision record. The run manifest records `test_input_accessed=false` and `formal_output_accessed=false`. It did not alter the v0.3.1 freeze, configuration, predictions, aggregate results, or registered contrasts.

This chronology makes the analysis post-unblinding and post hoc even though its executable did not parse formal outputs. It can inform a new study design but cannot replace or rehabilitate the revealed 15-report test set.

## S2. Search space and selection procedure

The finite grid contained 147 semantically deduplicated configurations. CF weight was 0, 0.025, 0.05, 0.075, 0.10, 0.15, or 0.20. Removed CF mass was allocated to relevance, graph, or equally to both; path ranges were 2--3, 2--4, or 2--5 edges; graph distance and redundancy penalty remained fixed at 12 and 0.50. Three pre-coded gates (none, path coverage, and coverage plus adjacent-horizon stability) and strict-zero and coefficient-normalized no-CF comparisons were evaluated. Selection stability used 12 leave-one-report-out folds; each fold chose a configuration on the other 11 development reports. These folds are internal development diagnostics, not independent validation.

## S3. Complete selection result

All 12 leave-one-report-out folds selected the same zero-CF configuration, `C046` (relevance 0.55, role 0.20, graph 0.15, CF 0, position 0.10; 2--4-edge paths; no gate). Thus the winner frequency was 12/12 for zero CF and 0/12 for every nonzero-CF candidate. Its development ROUGE-L means were 0.12873 at $K=5$ and 0.15173 at $K=10$.

The highest full-development nonzero candidate under the specified tie-break was `C055` (CF 0.025, relevance-funded allocation, 2--5-edge paths, no gate), but it won no fold. Relative to strict zero, its mean ROUGE-L differences were -0.00131 at $K=5$ and -0.00091 at $K=10$; the descriptive 95% report-bootstrap intervals were [-0.00437, 0.00044] and [-0.00360, 0.00102]. It improved/harmed/tied 1/1/10 reports at $K=5$ and 1/3/8 at $K=10$. The machine label `robust_nonzero_cf` denotes only the deterministic tie-break among zero-frequency nonzero candidates; it is not evidence of empirical robustness.

The original formal development configuration, `C099` (CF 0.15, 2--4 edges, no gate), was below strict zero by -0.00567 at $K=5$ and -0.00257 at $K=10$. The corresponding descriptive intervals were [-0.01284, 0.00140] and [-0.00627, 0.00084]. The gates were non-discriminating because every development report passed them at every tested path horizon.

## S4. Interpretation and prohibition on reuse

The exploration shows that typed path scores were nonempty and stable across nearby path horizons, but no tested nonzero ranking weight produced a positive, stable development result. It therefore supports retaining the path-deletion quantity as an auditable structural diagnostic, not claiming an accuracy contribution. The result cannot justify choosing a favorable nonzero weight, rerunning `C046` or `C055` on the already revealed 15 reports, replacing the v0.3.1 primary table, selecting a subgroup from those reports, or calling any reuse confirmatory.

A later performance-oriented experiment would require a newly frozen method and a genuinely unseen holdout. If a nonzero CF ranking mechanism is retained, it should first satisfy a positive and stable development gate under a new integration rule; otherwise CF should remain auxiliary diagnostic output.

## S5. Bound artifacts

- `posthoc_dev_cf_calibration/artifacts/RUN_MANIFEST.json`: timeline, data boundary, code and output hashes.
- `posthoc_dev_cf_calibration/artifacts/CALIBRATION_DECISION.json`: 147-candidate and 12-fold decisions.
- `posthoc_dev_cf_calibration/artifacts/candidate_summary_ledger.jsonl`: 147 aggregate records.
- `posthoc_dev_cf_calibration/artifacts/loo_fold_ledger.jsonl`: 12 fold decisions.
- `posthoc_dev_cf_calibration/artifacts/per_report_ledger.jsonl`: 3,528 candidate-report-budget records.
- `posthoc_dev_cf_calibration/MECHANICAL_AUDIT.json`: mechanical audit.

No artifact in this supplement is a new formal test result.
