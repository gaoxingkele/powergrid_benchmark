# C2GES exploratory-v3 protocol freeze

- Frozen at: `2026-08-05T16:08:56+08:00` (Asia/Shanghai)
- Status: finite, post-primary exploratory comparison; not a prospective confirmatory experiment.
- Timing qualification: every prediction artifact covered here already existed before this freeze, and some individual source-mode results may previously have been inspected. The contribution of this freeze is that the complete extraction family, contrasts, multiplicity families, interval rules, and runtime boundary are fixed before outcome extraction for this package.

## Frozen design

- Seeds: `2026`, `2027`, `2028`, `2029`, `2030`.
- Role protocols: `label_blind`, `predicted`, `oracle`.
- Extraction modes (all and only): `bm25`, `full`, `lead_k`, `lexcue`, `no_graph`, `no_role`, `query_only`, `sbert`, `tfidf`.
- Evidence budgets: `K in {1, 3, 5, 10}`.
- Primary editorial cell: `label_blind`, `K=3`.
- Primary comparator: `full`; the eight frozen mode-minus-`full` contrasts are `bm25`, `lead_k`, `lexcue`, `no_graph`, `no_role`, `query_only`, `sbert`, and `tfidf`.
- Source scope: W4 seeds 2027--2030 plus the W3 seed-2026 run referenced by the W4 five-seed aggregate. No reruns, tuning, substitutions, or post-freeze modes are permitted.
- Explicitly absent: a new cross-encoder and a no-floor ablation were not run and must be reported as missing, not estimated or backfilled.

## Endpoints, uncertainty, and multiplicity

All outcome fields that are consistently present in every frozen cell will be extracted symmetrically. The existing primary evidence-quality metric is the ordering endpoint; other common metrics are secondary/resource diagnostics. Values may not be selected or suppressed by direction or significance.

- Family F1 (editorial extraction): the eight mode-minus-`full` contrasts in the primary cell, separately for each reported endpoint; two-sided exact paired sign-flip tests with Holm adjustment across the eight contrasts within endpoint.
- Family F2 (budget sensitivity): for each mode in `label_blind`, contrasts `K=1`, `K=5`, and `K=10` against `K=3`; Holm adjustment across 27 contrasts within endpoint.
- Family F3 (role protocol): at `K=3`, each mode under `predicted` and `oracle` versus the same mode under `label_blind`; Holm adjustment across 18 contrasts within endpoint.
- Family F4 (full finite grid): descriptive summaries for all 9 x 4 x 3 cells. Any additional inferential contrasts are clearly labeled descriptive/unadjusted and cannot be promoted into F1--F3.

Documents are the inferential clusters: paired document-level differences are formed before any test or interval. Exact sign-flip inference flips document-cluster mean differences, not individual repeated observations. Seeds are repeated training/decoding realizations, not independent documents. Report document-cluster bootstrap 95% intervals with the complete five-seed bundle retained within each resampled document; additionally report across-seed min--max or percentile summaries as stability diagnostics, never as a substitute for document-cluster uncertainty. For only five seed-level paired observations, an exact seed sign-flip test has minimum attainable two-sided p-value 0.0625 and is diagnostic only.

## Runtime boundary

Runtime is measured only from existing per-run timing/provenance fields with the same semantic definition across all cells. It excludes one-time corpus ingestion, embedding/index construction unless explicitly included by every compared source run, model training outside the recorded extraction run, manuscript/table/figure generation, and this re-analysis. Missing or semantically incomparable timing is reported as unavailable. Runtime is a resource diagnostic, not evidence of extraction quality or deployment readiness.

## Integrity and stopping rule

Inventory completeness is checked from paths, filenames, configuration/provenance identifiers, and hashes before outcomes are read. After inventory, one scripted symmetric extraction produces machine-readable long-form data, tables, and figures. A separate validator recomputes cell counts, identities, contrast directions, p-value adjustment, and artifact hashes. The package stops after the frozen grid and missing-mode statement; no favorable-result-driven extension is allowed.
