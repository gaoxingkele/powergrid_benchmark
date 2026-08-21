# C2GES Round 1 Response Matrix

> Current-status addendum (2026-08-06): the rows below preserve the Round-1
> evidence state. Author names, affiliations and correspondence have since been
> migrated from the paired CMC manuscript, and the bundle has expanded to the
> authoritative identity recorded in `round3_author_metadata_closure.json`.
> Remaining CRediT, funding, conflict, ethics/consent and AI-use statements still
> require author approval.

This matrix responds to `round1_methods_stats_review.md` and `round1_methods_stats_issue_matrix.json`. The review files themselves were not modified. Numerical additions are generated from frozen CSV/JSON or from hash-bound local audit records; no unavailable identifier or count was invented.

| ID | Status | Revision and evidence |
|---|---|---|
| R1-M01 | Resolved | Methods now discloses that seed 2026 began at 04:53 UTC, was inspected in W3, and was deliberately reused after the 05:12 UTC W4 freeze; only seeds 2027--2030 were frozen before execution. The five-seed study is called a frozen continuation/canonical aggregation, and unsupported prospective framing was removed. NO--GO decisions and the primary endpoint were retained. |
| R1-M02 | Resolved | The Holm citation and implementation claim were removed. Methods states what the aggregator actually produces: raw paired t/sign-flip p-values, while gates use a positive mean plus positive seed-t and hierarchical-CI lower bounds. No adjusted analysis was added. |
| R1-M03 | Resolved | Role-Provenance Protocols now specifies both TF--IDF channels, n-grams, casing/accent/sublinear settings, feature limits, class-balanced L2 logistic regression, liblinear, C, iterations, five-fold StratifiedGroupKFold, grouping, seeds, and serialization. It states that one ledger (SHA-256 `96c31a5f...`) is reused by all downstream seeds and that intervals exclude upstream refits/fold variation. |
| R1-M04 | Resolved | Added the total-loss equation and generated Table `tab:implementation`, covering head dimensions, dropout, encoder batch/snapshot, query/local channels, floors/init/epsilon, Adam and weight decay, instance-wise updates, epochs/checkpoint tie rule, RNGs, and normalization. `evidence/method_implementation_contract.json` is bound to exact executable-source hashes; `reproducibility/environment_lock.txt` records observed versions. |
| R1-M05 | Partially resolved (irrecoverable source-revision field disclosed) | Added the complete conversion algorithm, parsing/mapping/exclusion rules, dedup key, first-eight-byte SHA-256 80/10/10 assignment, whole-document capacity rule, converter hash, cache key/fingerprints, and generated conversion table. Offline replay recovered 32,900 source rows, 32,475 eligible rows, 425 `<2`-candidate exclusions, zero other eligibility exclusions, capacity exclusions, and final counts. The original converter passed no Hugging Face revision; this cannot be reconstructed retrospectively and is explicitly stated. Frozen converted-file hashes remain available. |
| R1-M06 | Partially resolved (human DOI/license action remains) | Created `reproducibility/bundle_manifest.json`, covering 11,230 retained local artifacts / 689,449,577 bytes: code, data/manifest, upstream ledger/model, all 15 checkpoints/configs/full prediction ledgers, W6 canonical release, environment record, and verifiers. `reproducibility/verify_bundle.ps1` is the one-command route and passes. A permanent repository DOI/URL, redistribution/license decision, and upload remain explicitly marked as human pre-submission blockers. |
| R1-M07 | Resolved by bounded attribution | Removed the statement attributing useful signal to shared components. Results now state only that role-provenance substitution did not reliably change the full reranker. It explains that source diagnostic modes were excluded because canonical v2 and its gates cover full/BM25 only; no selectively reported post-hoc ablation was introduced. |
| R1-m01 | Resolved | Methods and the main-table caption now use the same gate: positive mean plus both seed-level t-CI and hierarchical percentile-CI lower bounds above zero. The caption points to the complete canonical effects artifact for intervals omitted from the compact table. |
| R1-m02 | Resolved | Replaced “conditional upper-bound diagnostic” with “privileged-label conditional sensitivity diagnostic.” The superseded-claim audit rejects oracle/upper-bound phrasing in TeX and PDF. |
| R1-m03 | Resolved | Results now distinguish 810,000 source-ledger rows (54,000 per run, all modes) from 180,000 canonical v2 full/BM25 rows (12,000 per run). |
| R1-m04 | Resolved | Methods specifies seed-with-replacement then document-with-replacement sampling, duplicated-cluster behavior, pooled claim weighting (instance-weighted estimand), percentile endpoints, deterministic per-contrast RNG construction, seed-level t intervals, and the 2,000-draw endpoint-precision limitation. No retrospective 10,000-draw gate change was made. |
| R1-m05 | Partially resolved (author metadata requires authors) | Added head-height control and a PDF-string-safe C2GES macro; the reviewer-identified fancyhdr and hyperref PDF-string warnings are absent from the rebuilt log, with no undefined references/citations. Author/affiliation PDF metadata remains intentionally blocked rather than invented; W7 front-matter placeholders are preserved for human completion. |

## Added traceability artifacts

- `manuscript_applsci/evidence/conversion_audit.json`
- `manuscript_applsci/evidence/method_implementation_contract.json`
- `manuscript_applsci/generated/table_conversion_audit.tex`
- `manuscript_applsci/generated/table_implementation.tex`
- `manuscript_applsci/reproducibility/environment_lock.txt`
- `manuscript_applsci/reproducibility/bundle_manifest.json`
- `manuscript_applsci/reproducibility/create_bundle_manifest.py`
- `manuscript_applsci/reproducibility/verify_local_bundle.py`
- `manuscript_applsci/reproducibility/verify_bundle.ps1`
- `manuscript_applsci/scripts/audit_superseded_claims.py`

## Verification record

- Claim/source verifier: PASS (13 source hashes, 8 generated fragments, 8 figures, 27 citation keys).
- Frozen protocol/canonical unit tests: PASS (23 tests).
- Local bundle verifier: PASS (11,230 artifacts, 689,449,577 bytes, all SHA-256 hashes).
- LaTeX/BibTeX build: PASS; 20-page PDF; no undefined citations/references; reviewer-identified fancyhdr/hyperref warnings removed.
- Superseded-claim audit: PASS for TeX and extracted PDF across legacy split, legacy metrics, positive-role claim, unsupported prospective wording, removed Holm citation, and oracle-upper-bound wording.

## Human blockers carried forward

1. Select a repository, review FEVER/model/report licenses, upload the permitted bundle, mint a permanent DOI/URL, and replace the data-availability placeholder.
2. Supply author names, affiliations, corresponding author, CRediT roles, funding, conflicts, acknowledgments, and author-approved generative-AI declaration.
3. The unrecorded original Hugging Face source revision cannot be recreated; any clean future regeneration should pin and record a revision before execution.
