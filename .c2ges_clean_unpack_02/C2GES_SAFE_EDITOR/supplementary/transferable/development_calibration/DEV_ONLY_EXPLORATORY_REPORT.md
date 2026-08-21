## Material Passport

- Material ID: `C2GES-posthoc-dev-CF-calibration-v1`
- Material type: development-only exploratory experiment report
- Verification status: `ANALYZED`; post-run mechanical integrity audit `PASS`
- Evidence class: post-unblinding, post hoc, development-only
- Permitted use: sensitivity analysis and design of a future v0.4 protocol
- Prohibited use: replacement of v0.3.1, confirmation on the existing 15-report test set, or evidence that the CF channel improves accuracy
- Data boundary: SHA-256-pinned 12-report development file only

# Development-Only Exploratory Calibration of the C2GES Counterfactual Channel

## 1. Status and non-negotiable boundary

This analysis began after the frozen v0.3.1 formal result had already been
revealed. It is therefore post-unblinding and exploratory. The program did not
read or parse the held-out test JSONL, formal predictions, aggregate metrics, or
formal contrasts. It did not modify the v0.3.1 configuration, freeze, registry,
or outputs. The only data input was the 12-report development JSONL with
SHA-256 `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`;
the audited run04 development decision was read only to bind the prior setup.

The formal result's prior disclosure is recorded as a timeline fact rather than
concealed: formal v0.3.1 results were known before the exploration started at
2026-08-08 17:29:45 Asia/Shanghai; the exploratory run completed at 17:43:04.

## 2. Fixed exploratory design

The finite grid contained 147 semantically deduplicated configurations. The CF
weight was one of 0, 0.025, 0.05, 0.075, 0.10, 0.15, and 0.20. Relative to the
formal vector `(relevance=.40, role=.20, graph=.15, CF=.15, position=.10)`, the
difference `0.15-c` was assigned in one of three prespecified ways: entirely to
relevance, entirely to graph, or equally to relevance and graph. Thus every
full-model coefficient vector summed to one. The path range was 2--3, 2--4, or
2--5 edges; graph distance and redundancy penalty remained 12 and 0.50.

Three document-level gates were evaluated:

1. no gate;
2. coverage gate, active when at least two qualified paths existed and at least
   1% of sentence nodes had positive raw deletion loss; and
3. coverage-plus-stability gate, additionally requiring Spearman correlation of
   at least 0.75 between the current and immediately shorter path-horizon CF
   vectors.

Two no-CF comparisons were retained. `strict-zero` kept every coefficient and
set only the CF channel values to zero, matching the v0.3.1 strict ablation.
`normalized-no-CF` transferred the CF mass back to its prespecified donor(s), so
that both compared coefficient vectors summed to one. Results were calculated
at K=5 and K=10 for ROUGE-1 F1, ROUGE-L F1, pairwise lexical redundancy,
selected-sentence overlap, and changed sentence count.

Configuration stability was assessed with 12 report-level leave-one-report-out
(LOO) folds. Within each fold, the winner was chosen using only the other 11
reports by: mean of K=5 and K=10 ROUGE-L, then improvement over strict-zero,
then lower redundancy, lower CF weight, and stable identifier. These folds are
internal development diagnostics, not independent validation.

## 3. Main result: optimization did not support a nonzero CF weight

All 12 LOO folds selected the same zero-CF configuration: relevance 0.55, role
0.20, graph 0.15, CF 0, and position 0.10 (`C046`). Its mean development
ROUGE-L was 0.12873 at K=5 and 0.15173 at K=10. The 12/12 winner frequency is
strong evidence of development-set selection stability for zero CF, but it is
not external evidence.

No nonzero-CF configuration won any LOO fold. After the predetermined
tie-breaking among zero-frequency nonzero candidates, the highest full-
development candidate was `C055`: CF 0.025, relevance-funded allocation,
2--5-edge paths, and no gate. Its mean results were:

| Quantity | K=5 | K=10 |
|---|---:|---:|
| Full ROUGE-L | 0.12653 | 0.15097 |
| Full ROUGE-1 | 0.29432 | 0.38987 |
| Full redundancy | 0.08825 | 0.08392 |
| Full minus strict-zero ROUGE-L | -0.00131 | -0.00091 |
| 95% report-bootstrap interval for strict-zero difference | [-0.00437, 0.00044] | [-0.00360, 0.00102] |
| Full minus normalized-no-CF ROUGE-L | -0.00220 | -0.00075 |
| Mean strict-zero sentence-set changes | 0.33 | 0.67 |

At K=5, `C055` improved one report, harmed one, and left ten unchanged relative
to strict-zero. At K=10 it improved one, harmed three, and left eight unchanged.
Its label `robust_nonzero_cf` in the machine decision means only that it won the
prespecified tie-break among nonzero candidates; its LOO winner count is zero
and it is not empirically robust.

The original 0.15-CF, 2--4, ungated development configuration (`C099`) had mean
full ROUGE-L 0.11951 at K=5 and 0.15050 at K=10. Relative to strict-zero, the
differences were -0.00567 and -0.00257, with bootstrap intervals
[-0.01284, 0.00140] and [-0.00627, 0.00084]. It changed an average of 3.33 and
5.67 selected sentences. Relative to the coefficient-normalized no-CF
comparison, its differences were +0.00081 at K=5 and -0.00007 at K=10, and both
intervals crossed zero. Thus part of the strict-ablation gap reflects score-
scale interaction with the fixed redundancy penalty, but normalization still
does not establish a benefit.

## 4. Path and gate diagnostics

Typed paths were abundant rather than absent. Across 12 reports, the median
qualified-path counts were 1,356.5, 1,587.5, and 1,587.5 for maximum horizons
3, 4, and 5; ranges were 95--16,681, 96--26,025, and 96--26,025. Median node
coverage was 0.444 for every horizon, with a range of 0.268--0.853. Median
adjacent-horizon Spearman stability was 0.979, 0.996, and 1.000. Every report
passed both gate definitions at every horizon, so the explored gates were
non-discriminating and could not rescue accuracy.

This distinguishes two claims. The CF signal is identifiable, nonempty, and
stable under nearby path horizons on these development reports. However, those
properties did not translate into an observed ROUGE improvement when the signal
was used for selection.

## 5. Interpretation and statistical cautions

The analysis supports retaining the counterfactual path mechanism as an
algorithmic representation and diagnostic channel, provided the paper clearly
states that neither the formal test nor this post hoc development search showed
an accuracy gain attributable to it. It does not support choosing a smaller
nonzero weight merely because its negative mean is numerically closer to zero.

The intervals are percentile bootstrap intervals over only 12 reports and are
descriptive. Reports are heterogeneous, the grid is reused across folds, and
147 configurations create substantial selection multiplicity. No p-value or
interval here repairs the post-unblinding status. Zero changes in many reports
also make mean differences sparse and non-Gaussian. Accordingly, the exact
per-report ledger is more informative than a significance label.

## 6. v0.4 recommendation

The defensible performance-oriented v0.4 candidate is the zero-CF selector
`C046`, while retaining CF scores as an auxiliary diagnostic output rather than
as a ranking coefficient. This recommendation follows 12/12 LOO stability and
does not claim a CF accuracy contribution.

If the scientific objective requires testing a nonzero CF ranking term, no
nonzero configuration from this search currently satisfies a freeze gate. A
future nonzero v0.4 experiment should first specify a mechanistically different
integration rule on development data (for example, constraint or uncertainty
abstention rather than a linear additive weight), establish a positive and
stable development criterion, freeze code and hypotheses, and then evaluate
once on newly acquired NERC reports that have never been parsed, inspected, or
used here. The existing 15-report test set must not be reused to choose that
configuration.

## 7. Artifact inventory

- `run_dev_only_calibration.py`: guarded executable and complete analysis plan
- `test_dev_only_calibration.py`: 10 boundary and mathematical unit tests
- `code_snapshot/`: byte-identical copies of the three method modules bound in the run manifest
- `artifacts/per_report_ledger.jsonl`: 3,528 candidate-report-K records
- `artifacts/candidate_summary_ledger.jsonl`: 147 aggregate records
- `artifacts/loo_fold_ledger.jsonl`: 12 report-level LOO decisions
- `artifacts/path_gate_diagnostics.jsonl`: 36 report-horizon diagnostics
- `artifacts/CALIBRATION_DECISION.json`: machine-readable selection result
- `artifacts/RUN_MANIFEST.json`: data/code/output hashes and timeline
- `verify_calibration.py`: independent mechanical consistency verifier
- `MECHANICAL_AUDIT.json`: persisted 11-check post-run audit result

No artifact in this directory is a new formal test result.
