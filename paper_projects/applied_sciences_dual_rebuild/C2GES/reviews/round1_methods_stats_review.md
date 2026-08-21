# C2GES Review Round 1 — Methods, Statistics, and Reproducibility

## Review disposition

**Recommendation: MAJOR REVISION.**

This is an independent review of the newly assembled Applied Sciences manuscript, not a review of the superseded legacy draft. The reviewed snapshot is:

- TeX: `manuscript_applsci/paper_applsci.tex`, SHA-256 `82ff97765be219ea3f2400bfba2fecdfb75a0b5d8c6558921e797a7d982ba988`.
- PDF: `manuscript_applsci/build/paper_applsci.pdf`, SHA-256 `e1668847ea3a9ee8df2c9399373b283534e79c9c2add8b4aca0b2e241b4d5a51`.
- Canonical v2 manifest: `workspace/w6_c2_canonical_v2/canonical_manifest.json`, SHA-256 `989e91c60eb48220e92a8eac32047973fa0f7b5d407cc66af0489f6a51ca4783`.

The central numerical reconstruction is credible: the canonical validation passes, all 15 protocol–seed runs are indexed, the main K=3 predicted-label result is 0.4920, fixed BM25 is 0.4864, the hierarchical contrast is +0.0056 [0.0008, 0.0107], and predicted-label minus label-blind is +0.0010 with an interval crossing zero. The manuscript correctly retains the role-effect and blanket-superiority NO–GO conclusions. However, the paper currently overstates the prospective status of the five-seed study, asserts a Holm correction that is absent from code and artifacts, and omits implementation/data details needed for independent reproduction.

## Major issues

### R1-M01 — The complete five-seed experiment was not prospectively frozen

The manuscript calls the analysis a “confirmatory experiment,” says the families were “prespecified,” and says the decision rule was frozen before canonical aggregation (`paper_applsci.tex:135–144`). The last statement is narrowly true, but the broader confirmatory framing is not: `W4_FREEZE_MANIFEST.json:2–5` was created at 05:12 UTC after W3 started at 04:53 UTC, while `W3_C2_PILOT_REPORT.md:6,28–37,49–58` records the full test results for seed 2026 and explicitly calls them a one-seed pilot. The aggregation code deliberately sources seed 2026 from W3 rather than rerunning it (`aggregate_c2_w4_five_seed.py:35–38,114–115,268,275`), and the W4 report generator states that only seeds 2027–2030 were new (`aggregate_c2_w4_five_seed.py:303–311`).

Required revision: disclose that seed 2026 was an observed pilot reused in the five-seed aggregation and that only the remaining four seeds were frozen before execution. Replace “confirmatory” and “prespecified/preregistered” language with an accurate description such as “frozen continuation and canonical aggregation,” unless an independently timestamped protocol predating W3 can be produced. Preserve the NO–GO decisions; do not select a new primary endpoint after this disclosure.

### R1-M02 — Holm correction is claimed but not implemented or reported

`paper_applsci.tex:144` says that prespecified families and sequentially rejective Holm correction guard against searching over protocols and cutoffs. No family definition, raw-to-adjusted p-value table, or adjusted decision appears in the canonical v2 directory or generated manuscript fragments. The frozen aggregator computes paired t-test and exact sign-flip p-values only (`aggregate_c2_w4_five_seed.py:41–75,220–226`) and then constructs gates directly from unadjusted intervals (`aggregate_c2_w4_five_seed.py:237–255`). A repository-wide search of the canonical release and generated fragments found no Holm/adjusted-p implementation or result.

Required revision: either remove the Holm claim and describe the actual frozen gate, or define each multiplicity family and generate traceable Holm-adjusted p-values from the frozen contrast matrix. Any added adjusted analysis must be labeled retrospective unless a pre-W3 family specification is documented; it must not be used to rescue a failed gate.

### R1-M03 — The upstream role classifier is materially under-specified, and its uncertainty is not represented by the five downstream seeds

The manuscript describes only a “claim-text classifier” with grouped OOF predictions (`paper_applsci.tex:79–97`). The retained provenance shows five folds, seed 2026, 30,000 maximum features, `min_df=2`, and `C=1.0` (`upstream_labels/provenance.json:2–19,63–89`); the implementation is TF–IDF plus logistic regression. One ledger hash is frozen and reused by every predicted-label run (`W4_FREEZE_MANIFEST.json:33`; `aggregate_c2_w4_five_seed.py:156–162`). Consequently, the five-seed SD and hierarchical bootstrap vary the downstream selector, not the upstream classifier or its OOF partition.

Required revision: specify vectorizer, token/ngram settings, logistic-regression solver/penalty/C/max-iteration settings, grouping algorithm, shuffle/seed, fold count, class handling, and checkpoint/model serialization. Explicitly state that one upstream ledger was reused across all downstream seeds and that reported uncertainty does not include upstream-model refits. Ideally add an upstream-refit sensitivity analysis under a separately labeled exploratory protocol; otherwise bound the interpretation.

### R1-M04 — The downstream model/training description is insufficient to reproduce the registered model

The equations and high-level training loss are useful (`paper_applsci.tex:104–133`), but important frozen choices are absent. The code uses a 256-unit head, role embedding with encoder dimensionality, dropout 0.1, mixture floors `(0.35, 0.25, 0.05)`, raw initialization `(0.8, 0.7, 0.2)`, softplus epsilon `1e-3`, encoding batch size 64, per-document TF–IDF bigrams with `min_df=1`, Adam, one document-instance optimizer step at a time, and a 0.5 auxiliary-loss coefficient (`c2ges_learnable.py:185–221,275–300,318–355`). The manuscript merely calls the floors “registered” and does not give the auxiliary-loss formula or weight (`paper_applsci.tex:121,125–131`).

Required revision: add a complete hyperparameter/implementation table and the total-loss equation, including architecture dimensions, dropout, channel floors and initialization, local smoothing window/decay, normalization and tie behavior, optimizer defaults/weight decay, batching/gradient schedule, epoch/checkpoint selection, random sources, package versions, and exact encoder snapshot. Make the executable code and environment lock file part of the deposited supplement.

### R1-M05 — Dataset construction cannot be independently reconstructed from the manuscript

The data section states that SUPPORTS/REFUTES single-document instances are retained and that assignment is grouped (`paper_applsci.tex:62–75`), but it omits the precise source dataset revision/configuration, full eligibility rules, evidence-line mapping, handling of fewer than two candidates, missing evidence, duplicates, document-boundary limiting, and the deterministic hash split. These are consequential operations in `prepare_fever_benchmark.py:84–133,151–203,251–310`: the script loads `lukasellinger/filtered_fever-evidence_selection`, pools original splits, assigns by the first eight SHA-256 bytes of the document ID, discards several classes of rows, and skips a whole document if adding it would exceed a limit.

Required revision: provide an explicit conversion algorithm/pseudocode, source dataset revision or immutable snapshot hash, starting and excluded row counts by reason, split fractions, deterministic assignment rule, deduplication key, document-boundary limiting rule, and conversion-script hash. Deposit the exact split manifest and conversion code subject to FEVER licensing.

### R1-M06 — The claimed reproducibility package is not submission-ready

The manuscript says checkpoints and the per-instance ledger “should be deposited … if permitted” (`paper_applsci.tex:274`) and the data-availability statement still contains a required permanent repository placeholder (`paper_applsci.tex:279`). Local canonical artifacts are strong, but a reader cannot access the checkpoints, complete source prediction rows, executable code/environment, or immutable public DOI from the submitted document.

Required revision: before submission, deposit the permitted artifact bundle at a permanent URL/DOI; list licenses, hashes, code entry points, environment versions, split manifest, upstream ledger/model, all seed configurations/checkpoints, the full and canonical prediction ledgers, aggregation script, and a one-command verification route. If redistribution is restricted, give exact regeneration instructions and document every excluded artifact.

### R1-M07 — Existing component/baseline evidence is omitted while component attribution is discussed

The model is presented as a three-channel interpretable reranker (`paper_applsci.tex:104–131`), and the Results infer that useful signal “appears to come from the shared ranking components” (`paper_applsci.tex:173`). Yet the canonical ledger retains only `full` and `bm25` rows even though each indexed source run contains 54,000 rows and additional frozen modes; the canonical ledger retains 12,000 rows per run (`aggregate_c2_w4_five_seed.py:166–175`; `canonical_manifest.json`, source run index). The manuscript itself proposes query-only/no-role/no-floor work as future experiments (`paper_applsci.tex:249–254`) without presenting the already available frozen ablation modes.

Required revision: either report the existing frozen component/baseline modes in a clearly labeled exploratory ablation table with multiplicity caveats, or remove/soften attribution to the “shared ranking components” and explain why those frozen modes were excluded from canonical v2. Do not present post hoc ablations as confirmatory.

## Minor issues

### R1-m01 — Gate wording is internally inconsistent

The correct role gate requires a positive mean plus both seed-level and hierarchical intervals above zero (`paper_applsci.tex:138,142`). However, `paper_applsci.tex:146` says only the hierarchical interval is required, and the main-table caption (`paper_applsci.tex:165`) says hierarchical intervals determine the BM25 gate. The code applies both intervals to every positive-effect gate (`aggregate_c2_w4_five_seed.py:237–255`). Use one exact definition in Methods, captions, and Results; report both interval types or explicitly point readers to the artifact containing the omitted interval.

### R1-m02 — “Oracle upper bound” is not mathematically warranted

Figure 1 calls oracle-label a “conditional upper-bound diagnostic” (`paper_applsci.tex:89`). Privileged label access does not guarantee an upper bound for this constrained training procedure, and observed oracle performance is not uniformly greater. Call it a “privileged-label conditional sensitivity diagnostic.”

### R1-m03 — Clarify what the 180,000-row canonical ledger includes

`paper_applsci.tex:162` reports 180,000 canonical rows, while each of 15 source runs contains 54,000 rows (810,000 total). Canonical v2 intentionally retains 12,000 `full`/BM25 rows per run. State this scope explicitly and distinguish source-ledger audit coverage from the reduced canonical full-and-BM25 release.

### R1-m04 — Bootstrap estimand and Monte Carlo details need one more sentence

The code resamples seeds with replacement, then documents with replacement, pools all claims in sampled document clusters, takes percentile quantiles, and uses a deterministic RNG seed (`aggregate_c2_w4_five_seed.py:79–104`). This yields an instance-weighted cluster bootstrap rather than equal document weighting. Add the weighting/duplicate-cluster rule, interval type, RNG seed strategy, and the fact that 2,000 replicates limit endpoint precision. A 10,000-replicate stability check could be reported as sensitivity without changing the frozen gate.

### R1-m05 — The compiled artifact is readable but not clean

Visual inspection of Methods/Results pages found readable equations, tables, and figures. The latest 19-page PDF has no undefined citations/references, but the build log repeatedly reports `fancyhdr` head-height warnings and hyperref PDF-string warnings. PDF metadata still exposes `W7_FRONT_MATTER: AUTHOR NAMES REQUIRED`. These are not statistical faults but should be cleared before submission to ensure deterministic pagination and clean metadata.

## Explicit superseded-claim audit

**PASS for both TeX source and extracted PDF text.** The audit used boundary-aware searches plus manual context checks.

- Old split claim `4000/800/800` (including `4,000` variants): absent. The new manuscript consistently generates 8000/1500/1500. Standalone `800` occurrences in extracted PDF are the upstream accuracy `0.800` and a figure-axis tick, not an old split claim.
- Old one-seed/single-seed framing: absent from the new TeX and PDF. The manuscript says five seeds. The historical W3 artifact still correctly labels seed 2026 a one-seed pilot; this is evidence for R1-M01, not text leaked into the manuscript.
- Old point estimates `0.5066`, `0.5030`, `0.4967`, `0.4937`, `0.4837`, `0.4818`, `0.4414`, and old `+0.0099` role/system delta: absent.
- Positive-role claims such as “role conditioning improves,” a significant predicted-vs-blind effect, or “the role head drives the gain”: absent. The abstract, Results, Discussion, and Conclusion consistently state that predicted-label minus label-blind crosses zero and that the role claim is NO–GO (`paper_applsci.tex:18,29,183–189,249,271–272`).

## Verified strengths

- Canonical v2 validation reports 180,000 canonical rows, 15 indexed runs, 176 passed evidence checks, zero failures, and complete figure/table outputs.
- Generated TeX values are traceable through `generated/claim_source_map.json` to hashed canonical CSV/JSON sources.
- The manuscript cleanly separates the conditional oracle from deployed protocols and avoids treating FEVER as a power-grid corpus.
- The negative role result, cutoff dependence, deterministic nature of BM25, and limitations of the NERC silver material are stated prominently rather than buried.
- PDF inspection found no obvious clipped methods equations, unreadable main tables, or broken result figures.
- The cited-only bibliography is internally closed: 28 cited keys, 28 BibTeX entries, zero missing keys, and zero uncited entries.

## Round-2 verification gate

Round 2 should not close until R1-M01 and R1-M02 are resolved in text and artifacts, the exact upstream/downstream specifications and dataset conversion are supplied, and a permanent reproducibility package is identified. Re-run the superseded-claim audit after every numerical or narrative edit.
