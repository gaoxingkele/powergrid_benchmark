# C²GES v0.3 Stage-1 Independent Re-audit — diagnostic_build_08

## Material Passport

- Artifact audited: `diagnostic_build_08`
- Audit date: 2026-08-08 (Asia/Shanghai)
- Audit role: fresh independent data/method auditor
- Access boundary: read-only inspection and deterministic recomputation
- Evaluation boundary: no development/test summarization scores, predictions, grid-search outcomes, or tuning decisions were opened
- Verification status: **VERIFIED**
- Overall decision: **PASS**

## 1. Decision and permitted next step

`diagnostic_build_08` passes the requested Stage-1 data, leakage, provenance, graph-role, work-limit, cache-equivalence, and regression-test gates.

**Authorization:** the team may use the 12-report development split for configuration selection. This decision does **not** freeze or authorize inspection of the 15-report test split, does not authorize test evaluation, and does not validate any downstream performance or causal-effect claim. A separate immutable development-selection record and subsequent test-freeze decision remain mandatory.

## 2. Audit scope and independence

The audit independently read the current builder and method sources, all eight build08 artifacts, the 40-row source manifest, and all 40 local source PDFs. It recomputed hashes, PDF page counts, inclusion/split/candidate inventories, reference/candidate boundaries, two leakage measures, registered contamination gates, rights-chain consistency, role-tie behavior, and cache values. The dataset was also reconstructed in memory from every included raw PDF and compared with the stored JSONL rows.

No file under `dev_selection_run*`, no prediction file, and no score or tuning result was inspected. The previously failed `diagnostic_build_07` was used only as historical context; it was not treated as evidence for build08.

## 3. Manifest and hash chain

The build manifest is internally consistent and its registered hashes match the current files:

| Item | Independently recomputed SHA-256 | Result |
|---|---|---|
| Current `build_full_pdf_dataset.py` | `817518DF71F16DA05F54E18A5505BD0639201082E5E846142EF74F64F1A1BA38` | matches manifest |
| Source manifest | `753939D6500320AD2E3DE1CED3E145399E90A9395E85A16DADE31D166C22BFE2` | matches manifest |
| Complete benchmark JSONL | `87F7F7545CE8116E161A88919483B4EEB0ACF7A9C8854981894947C326EDAA15` | matches manifest |
| Development JSONL | `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79` | matches manifest |
| Test JSONL | `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127` | matches manifest |
| Build manifest itself | `27CF2AD3C9114E92D967EBF524D94504B6E9BB13F9D643B6C486363C21611F51` | recorded by this audit |
| Per-report extraction audit | `FC533E5480B2849800B87E7424AB54790919C70DE7CA1BF8184DC392E5E590EC` | recorded by this audit |
| Rights ledger JSONL | `9B4F3F38CCC7DE306950700521B84B278143EE81629F1E74FEA459C528C6868E` | recorded by this audit |
| Rights ledger CSV | `01A02AFE10233345B7A4B7E98761586C814BD4C8CB7B07E016427D4C4AB5090F` | recorded by this audit |

All 40 PDF SHA-256 values are distinct. For every included report, the raw-PDF hash equals the hash stored in the dataset row, per-report audit, and rights ledger. A deterministic `doc_id<TAB>pdf_sha256<LF>` chain over the ordered 40-row rights ledger hashes to `3CF09E76946CF5459459EB7E839ED6BEBF59FC12F1BEDA21416C8FB78DBC6B70`.

## 4. PDF page counts and inventory

`pdfinfo` was run independently on all 40 source PDFs:

- source PDFs: 40;
- total declared pages: 3,200;
- page-count mismatches against the extraction audit: 0;
- missing PDFs: 0;
- included/excluded: 27/13;
- development/test: 12/15;
- total candidate sentences: 12,924;
- minimum/maximum candidates per included report: 51/1,898;
- reports above 80 candidates: 25;
- reports declaring truncation: 0 (`candidate_truncation` is `none` for all 27).

The development and test JSONLs are byte-content-equivalent, row for row, to filtering the complete benchmark by the registered split. No fixed 80-sentence cap is present.

## 5. The sole new exclusion relative to the former 28-report build

Relative to `diagnostic_build_06`, the only previously included report absent from build08 is:

- `nerc_034_2025_state_of_reliability_report_overview`: `missing_executive_summary_end`.

This is a conservative, fail-closed exclusion rather than performance-based selection. The raw 18-page PDF contains an `Executive Summary` heading on page 5 and an Executive Summary continuation/table on page 6, but no subsequent heading satisfying the pre-registered conservative end-boundary expression. The next content heading, `Severe Weather Responsible for the Most Severe Outages in 2024`, is intentionally not accepted by that expression. The builder therefore abstains instead of guessing a summary/body boundary.

The exclusion occurs inside `locate_summary`, before report-series split assignment and before any graph, selection, prediction, or evaluation operation. No score was available to this decision. The same rule is applied to all 40 PDFs; hence the exclusion is methodological fail-closure, not selective removal.

## 6. Summary boundary and leakage re-audit

The complete 27-row dataset was reconstructed in memory directly from the raw PDFs with the current builder functions. Stored references, body anchors, and candidate arrays were exactly reproduced; mismatched reports: 0.

Across all 27 included reports:

- reference/body page-interval overlaps: 0;
- candidates preceding the body-heading page: 0;
- exact normalized candidate/reference sentence matches: 0;
- residual normalized common substrings of at least 50 characters: 0.

The five mandatory cases and a seeded sample of five additional included reports were checked directly. The tuple below is `(reference-heading page, last retained reference page, body-heading page, first candidate page)`; the final two columns are exact-sentence leakage and `>=50`-character leakage.

| Report | Page tuple | Exact sentence | >=50 chars |
|---|---:|---:|---:|
| `nerc_001_november_13_wyoming_disturbance_report` | (2, 5, 8, 8) | 0 | 0 |
| `nerc_008_nerc_2021_california_solar_pv_disturbances` | (5, 7, 8, 8) | 0 | 0 |
| `nerc_011_san_fernando_disturbance_report` | (4, 9, 10, 10) | 0 | 0 |
| `nerc_028_ems_special_assessment` | (4, 6, 7, 7) | 0 | 0 |
| `nerc_040_2018_state_of_reliability_report` | (6, 11, 12, 12) | 0 | 0 |
| `nerc_041_2017_state_of_reliability_report` | (6, 7, 8, 8) | 0 | 0 |
| `nerc_030_winter_storm_elliott_recommendation_3_blac` | (5, 7, 8, 8) | 0 | 0 |
| `nerc_003_january_2025_arctic_events_a_system_perfor` | (4, 4, 5, 5) | 0 | 0 |
| `nerc_017_august_2017_hurricane_harvey_event_analysi` | (5, 6, 7, 7) | 0 | 0 |
| `nerc_042_2016_state_of_reliability_report` | (4, 5, 6, 6) | 0 | 0 |

The additional sample used deterministic seed `20260808` over the sorted included IDs after removing the five mandatory cases.

## 7. Registered pollution gates

Independent scanning of all 12,924 stored candidates produced zero for every registered class:

- `executive_summary_running_head`: 0;
- `section_table_fusion`: 0;
- `public_marker`: 0;
- `replacement_character`: 0;
- `common_mojibake`: 0;
- `page_marker`: 0;
- `dot_leader`: 0;
- `spaced_uppercase_running_title`: 0.

These counts agree with the build manifest. This result is limited to the registered deterministic pollution definitions; it is not a general semantic claim that every PDF sentence is stylistically clean.

## 8. Rights ledger and redistribution boundary

The rights ledger passes as a conservative provenance ledger:

- JSONL rows: 40; CSV rows: 40; ordering and field values are identical;
- all source URLs match the source manifest;
- `rights_holder = not_verified` for all reports;
- license locator and access date remain explicitly unrecorded;
- PDF and verbatim-text redistribution remain `not_authorized_pending_human_rights_review`;
- reviewer access remains conditional on third-party terms.

This is a fail-closed record, not a declaration of public-domain or redistribution permission. Source PDFs and verbatim benchmark text must not be placed in a submission package until a responsible human or institution resolves the applicable terms.

## 9. Role-tie, silver-label, and graph-edge checks

Rebuilding all 12 development graphs produced 111 positive top-score role ties. All 111 tied nodes have `dominant_role = None`, and there are zero directed edges incident to any tied node. Thus, the prior fixed-order tie advantage is removed and ambiguous nodes abstain.

Every build08 row has an empty `silver_role_evidence` object and `silver_label_provenance = none_in_v0.3_builder`. The v0.3 graph constructor accepts only sentence IDs/text and recomputes lexical role evidence; no silver role is consumed. No silver-label advantage was found.

## 10. Typed-path work guard and cache equivalence

The typed-path enumerator is stage-monotone, simple-path constrained, and depth bounded (`2 <= edges <= 4` in the registered use). It additionally defaults to `max_paths = 250,000` and `max_expansions = 2,000,000`, raising `PathEnumerationLimitError` before continuing when either limit is exceeded. The regression suite explicitly triggers both count and expansion fail-closed paths.

Cache equivalence passes at two levels:

- the unit test compares cached and uncached selection order and base-score dictionaries for both full and strict no-CF modes;
- independent all-pairs verification over the 12 development graphs compared 619,997 cached Jaccard values with the uncached function and found 0 float/value mismatches.

No downstream summarization score was computed or viewed in either check.

## 11. Regression test rerun

Command rerun from `R2_v0_3`:

```text
python -m unittest discover -s . -p 'test*.py' -v
```

Result: **20 tests run, 20 passed, 0 failures, 0 errors**. Coverage includes terminal-form-feed page counting, conservative summary boundaries and five real-PDF regression cases, reference leakage, no 80 cap, recurrent/running headers, pollution definitions, de-duplication, report-series grouping, typed-path identifiability/intervention equality/bounds/work limits, strict no-CF coefficient removal, role-tie abstention/no-edge behavior, and cached/uncached equivalence.

## 12. Final Stage-1 verdict

**PASS.** `diagnostic_build_08` may proceed to **development-only configuration selection** under an immutable run record. This is not a test freeze: the 15 test reports must remain unopened by the selection process, and any later test execution requires its own audited freeze artifact and authorization.

