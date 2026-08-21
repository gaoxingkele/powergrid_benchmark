# C²GES v0.3 Stage-1 Independent Audit

**Audit date:** 2026-08-08 (Asia/Shanghai)  
**Auditor role:** independent data/method auditor; no implementation changes and no downstream test-result or weight inspection  
**Latest diagnostic designated by the implementer:** `diagnostic_build_06`  
**Overall decision:** **FAIL — v0.3 must not be frozen yet**

`diagnostic_build_03` was superseded during this audit by the implementer's explicit latest diagnostic, `diagnostic_build_06`. All freeze findings below therefore apply to build06 and the current source files. Historical build03 is not used as a freeze candidate.

## 1. Scope and independence boundary

The audit covered the current `build_full_pdf_dataset.py`, `test_full_pdf_builder.py`, all build06 dataset/audit/rights/manifest artifacts, `counterfactual_paths.py`, `test_counterfactual_paths.py`, `CF_IDENTIFIABILITY_NOTE.md`, the 40-row source manifest, and all 40 local raw PDFs. The v0.3 method wiring and its tests were consulted only to determine whether the typed-path channel is actually callable. No files under `dev_selection_run01` and no downstream test predictions, scores, comparisons, or tuning decisions were inspected.

## 2. Recomputed inventory, hashes, and split

The following items pass:

- source manifest: 40 rows;
- local raw PDFs: 40 files, 40 distinct SHA-256 values, no missing file;
- each PDF SHA-256 agrees across the raw file, per-report extraction audit, benchmark row, and rights ledger;
- included/excluded: 28/12;
- included split: 12 development and 16 test reports;
- current builder SHA-256: `30ED1981A2A0BBB2DB3D737A2AD1112B274B2AD25B571EA67AD7F7F684FC19E8`, exactly matching build06;
- benchmark SHA-256: `4139777B9F11AAF0FD52A5B1FFB9C11121572C3375075391368DB6500D4F7570`, exactly matching build06;
- benchmark/dev/test file hashes all agree with `build_manifest.json`.

The page-count field fails. `pdfinfo` reports 3,200 pages across the 40 PDFs, while build06 records 3,240. Every one of the 40 reports is over-counted by exactly one page. The cause is deterministic: `pdf_pages()` applies `split("\f")` but retains the final empty element emitted after the terminal form feed. This is not only cosmetic because `len(pages)` also enters the recurrent-header threshold.

## 3. Candidate population, fixed-cap gate, and reference overlap

Independent recomputation from the JSONL rows gives:

- total candidates: 13,561;
- minimum/maximum candidates per included report: 54/1,963;
- reports with more than 80 candidates: 26;
- reports with exactly 80 candidates: 0;
- every row declares `candidate_truncation = "none"` and its stored count equals its actual candidate-list length;
- candidates preceding the stored body boundary: 0;
- residual exact normalized reference substring of at least 50 characters: 0;
- the six declared pollution-pattern totals are all 0.

Thus, there is no hidden 80-sentence cap and the implemented 50-character gate works against the *stored* reference. However, these checks do not establish a clean benchmark because the stored reference is truncated too early for several reports.

## 4. Blocking Executive Summary boundary and header contamination

The real-PDF boundary audit fails. `END_RE` accepts generic headings such as `Key Findings`, `Recommendations`, and any line beginning `Chapter 1`, even when those lines are still inside the Executive Summary. Consequently, part of the official summary is moved into the candidate pool and is no longer visible to the 50-character leakage check.

Concrete reproduced cases include:

- `nerc_028_ems_special_assessment`: the boundary is set at `Key Findings` on PDF page 4, but page 4 and the following page are explicitly headed `Executive Summary`; candidate `s00001` is the first key finding from that summary.
- `nerc_040_2018_state_of_reliability_report`: the boundary is set at the first `Recommendations` block on PDF page 7, while pages 7–8 are explicitly headed `Executive Summary`; candidate `s00001` is recommendation 1-1 from that summary.
- `nerc_008_nerc_2021_california_solar_pv_disturbances`: the boundary matches the narrative sentence beginning `Chapter 1 provides ...` on page 5; the sentence continues into the candidates and the Executive Summary continues on page 6.
- `nerc_011_san_fernando_disturbance_report`: the same narrative `Chapter 1 provides ...` failure occurs, and multiple candidates retain the running `Executive Summary` header.
- `nerc_001_november_13_wyoming_disturbance_report`: `Key Contributors` is treated as the body boundary although it is part of the Executive Summary material.

A seeded random audit (`seed=20260808`) selected `nerc_028`, `nerc_021`, `nerc_002`, `nerc_040`, and `nerc_014`. First/middle/last candidate anchors were checked against their complete raw PDFs. The page anchors and extracted wording were genuine, and no replacement-character, dot-leader TOC, or CJK mojibake was found. Three reports had a defensible post-summary boundary (`nerc_021`, `nerc_002`, `nerc_014`), but two of five failed because their candidates began inside the Executive Summary (`nerc_028`, `nerc_040`). Therefore the required random-sample criterion does not pass.

The declared pollution gate also misses generic running heads. Eighteen candidates contain the literal string `Executive Summary`; repeated examples in `nerc_011` are clearly page headers fused to candidate text. Other candidates fuse section running heads with tables (for example `Introduction Table I.1 ...`). The manifest's zero pollution total is correct only for its six narrow regex categories, not for the broader no-header requirement.

## 5. Rights ledger

The rights ledger passes as a conservative provenance record and does not invent a license:

- 40 JSONL rows and 40 CSV rows with identical document ordering;
- all source URLs are present and inherited from the source manifest;
- `rights_holder = not_verified`;
- `license_or_terms_locator = not_recorded_in_source_manifest`;
- access date is explicitly not recorded;
- PDF and verbatim-text redistribution are explicitly not authorized pending responsible human review;
- reviewer access is conditional on third-party terms.

These entries document uncertainty; they do not constitute permission. A responsible human or institution still must resolve any distribution or reviewer-access mechanism before packaging source PDFs or verbatim benchmark text.

## 6. Typed-path counterfactual mathematics and numerical check

The new quantity is not algebraically the weighted-degree signal. For the registered synthetic graph, nodes `r` and `x` have the same weighted-degree signal (both 0 after scaling), but raw typed-path losses are 0.75 and 0. The full scaled vectors also differ:

- weighted degree: `r=0, t=1, p=1, i=0, x=0, m=0`;
- typed-path counterfactual: `r=0.6, t=1, p=1, i=1, x=0, m=0`.

The intervention identity is valid for the induced-node-deletion operation: deleting a node removes exactly the pre-existing simple qualified paths containing it, so `U(G)-U(G_-i)` equals the sum of their strengths. The implementation is wired into the v0.3 score channel through `v03_methods.score_channels`; it is not merely an unused proof helper.

Path enumeration is depth-bounded (`2 <= edges <= 4`) and stage-monotone, so it cannot be unbounded. Its worst-case work is approximately `O(S·Δ^L)` and it materializes every qualified path before aggregation, where `S` is the number of start-role nodes, `Δ` is eligible out-degree, and `L <= 4`. On the largest development report (762 nodes, 2,814 edges), 21,507 qualified paths were materialized; this completed quickly in the audited environment. The cap makes current use plausible, but the freeze should retain a path-count/runtime guard because the full corpus contains reports up to 1,963 candidates and the implementation has no explicit maximum-path fail-closed gate.

Exact unknown roles are skipped in typed-path construction, which is fail-closed at that layer. The upstream dominant-role mapping is **not** fail-closed for ambiguity: when multiple roles share the positive maximum score, `CausalEventGraph.from_sentences()` chooses the first role in the fixed `ROLES` order. Across the 12 development reports, 117 of 3,592 nodes had such maximum-score ties. This can manufacture a path stage rather than abstain, so the role-mapping requirement is not satisfied.

## 7. Test rerun

`python -m unittest discover -s . -p 'test*.py' -v` was rerun from `R2_v0_3`:

- 15 tests run;
- 15 passed;
- 0 failures/errors.

The suite validates synthetic boundaries, no fixed 80 cap, declared pollution patterns, de-duplication, series grouping, typed-path identifiability/intervention equality, bounded scaling, and strict no-CF coefficient removal. It does not test terminal-form-feed page counting, full Executive Summary continuation across pages, generic running heads, or ambiguous role ties. Passing tests therefore do not clear the blocking data/protocol findings above.

## 8. Freeze decision and required closure

**Freeze authorization: denied for the current v0.3 candidate.** The following items are blocking:

1. discard the terminal empty page and regenerate truthful page-count metadata;
2. replace the generic first-match summary end rule with a boundary rule that demonstrably reaches the end of the complete Executive Summary, including continuation pages and internal `Key Findings`/`Recommendations` subsections;
3. extend header/footer cleaning and regression tests to catch generic running heads such as `Executive Summary` and section-title fusion;
4. make ambiguous dominant-role assignment fail closed (or register and justify an explicit deterministic ambiguity policy before inspecting evaluation results);
5. add real-PDF regression fixtures/checks for the reproduced boundary cases and a path-count/runtime fail-closed guard;
6. rebuild into a new immutable diagnostic directory and obtain a fresh independent audit before freezing.

No conclusion about downstream summarization quality or causal validity is made by this Stage-1 audit.
