# MA-SQLGrid Round 3 Claims, Evidence-Chain, and Submission-Compliance Review

## Decision

**MAJOR_REVISION**

The scientific result chain is internally coherent and independently reproducible, and I found no numerical contradiction in the factorial, component, or semantic-v5 claims. The manuscript also consistently limits the new experiment to an automated retrospective multi-state agreement stress test rather than a human semantic validation. The major-revision decision is instead driven by hard submission-compliance gates: visible author/declaration placeholders, unresolved redistribution/license review, and no permanent repository DOI/URL. One additional traceability defect is present: the Round-2 response and assembly report identify an older PDF, not the current compiled manuscript.

## Snapshot Audited

- TeX: `../manuscript_applsci/paper_applsci.tex`, 69,693 bytes, SHA-256 `2206ADAEC37BA3C89F5177C1D32AB8519967BA1C688C96E134F754769FE29067`.
- PDF: `../manuscript_applsci/build/paper_applsci.pdf`, 24 pages, 662,457 bytes, SHA-256 `441494CF65860CB7ECDC25F8638DE2BF12D3A06E066DE4D0B677A4B2383E6C44`.
- Build log: SHA-256 `86B23A9F8E12F522022F771C278EA6DA9C2EBDC0F068D2F59FC95A023C40C630`.
- `scripts/verify_manuscript.py`: PASS; 26 v2 outputs, 15 v3 outputs, four component-analysis outputs, nine figures, and 23 citation keys verified.
- PDF/build diagnostics: no LaTeX errors, undefined references, or overfull boxes; two harmless hyperref PDF-string warnings and four underfull-box warnings remain.

## Findings

### R3-CC-01 — Submission metadata and declarations remain placeholders (major; human action required)

The PDF visibly prints `W10_FRONT_MATTER` in the author, affiliation, correspondence, supplementary-material, CRediT, funding, ethics-confirmation, consent-confirmation, data-availability, acknowledgments, conflict-of-interest, and generative-AI fields. The TeX contains 13 such markers. The required MDPI declaration commands are present, so no declaration category was silently omitted, but their content has not been author-approved. This prevents submission and must not be closed by an agent.

Evidence: TeX lines 15--18 and 435--445; PDF-extracted text; `round2_author_response.json` correctly reports `author_metadata_complete=false` and `submission_ready=false`.

Required action: authors supply identities/affiliations/correspondence and approve CRediT, funding, ethics/consent applicability, acknowledgments, COI, and AI-use wording; then recompile and re-audit the PDF.

### R3-CC-02 — Data/license/DOI gate is explicitly unresolved (major; human/legal/repository action required)

The manuscript correctly says that GridDB redistribution permission is unresolved and that RTS-GMLC/SimBench derivatives carry source-specific obligations. The supplementary-material and data-availability statements still request a license-reviewed public repository URL/DOI. No license or DOI has been fabricated or implicitly filled. This is honest claim discipline, but it remains a submission/reproducibility blocker under the project plan.

Evidence: TeX lines 129, 419, 435, and 440; `round2_author_response.json` reports `license_and_doi_complete=false`; the Round-2 response labels the relevant items `deferred_human`.

Required action: complete source-by-source legal review, decide what may be redistributed, deposit the permitted package, insert the permanent DOI/URL, and hash-bind the deposited package.

### R3-CC-03 — Round-2 PDF identity is stale (minor traceability defect)

The current PDF is 662,457 bytes with SHA-256 `441494...E6C44`. Both `round2_author_response.md/json` and `W10_ASSEMBLY_REPORT.md` claim that the current 24-page PDF is 663,736 bytes with SHA-256 `81A945...A98F`. Page count is unchanged, but the byte/hash identity is false after semantic-v5 integration edits and recompilation. The response item `MA-R2-m07` therefore overstates synchronization.

Required action: update the response Markdown/JSON and assembly report to the final frozen TeX/PDF identities after all Round-3 revisions; add the TeX hash as well as the PDF hash.

### R3-CC-04 — Automated stress-test boundary is sound, with one wording refinement recommended (minor)

The manuscript repeatedly calls the v5 result a retrospective automated multi-state agreement/reliability stress test, excludes all 114 order-sensitive questions from the claim-promoting endpoint, and explicitly says it is not a human semantic audit or certification. The exact denominators are consistent across TeX, release, and both post-score audits: 25,920 atomic rows; 7,920 primary semantic rows; 528 primary predictions; 16,416 held diagnostic rows; 912 held predictions; 66 eligible and 114 held questions. T0 continuity is 1,440/1,440, and all nine Holm-adjusted suite values are 1.0000. Cell rates and the largest modifier (+0.3030, interval [-0.1714, +0.8780]) match the frozen analysis.

However, the abstract says “Two blinded technical reviewers” without immediately identifying them as agents. The Methods later says “This agent review,” and the abstract later says the test is not a human semantic audit, so this is not a false claim; nevertheless, “two blinded agent technical reviewers” would remove avoidable ambiguity.

Evidence: `formal_v5_results/RUN_SUMMARY.json`; `formal_v5_analysis/ANALYSIS_SUMMARY.json`; `formal_v5_release/release_manifest.json`; `POST_SCORE_INDEPENDENT_AUDIT_A.json`; `POST_SCORE_INDEPENDENT_AUDIT_B.json`; `semantic_order_review/adjudication.json` identifies the adjudication as agent technical review, not human domain review.

### R3-CC-05 — Semantic-v5 artifact lineage passes (no revision required)

The release binds nine artifacts, including the 25,920-row atomic ledger, 1,440 suite rows, nine contrasts, freeze, tables, and figure source. All release hashes and byte sizes pass the verifier. Two post-score audits independently reconstruct the suite and all nine contrasts; the second reports 29,160 independent read-only SQL executions with zero atomic-field mismatch. Manuscript semantic tables/figure are bound by `MANUSCRIPT_FIGURE_LINEAGE.json`, and their values agree with the release.

### R3-CC-06 — Factorial and component claims match canonical evidence (no revision required)

The manuscript preserves the primary 0/9 Holm outcome, labels the two structural hint effects as direct adherence/manipulation checks, and does not promote them as semantic benefit. The 700-call component claims match `CANONICAL_RESULTS.json`: Qwen E1 +0.1059 with composition-sensitivity interval [0.0282, 0.2013] and adjusted p=0.0310; Granite E1 is 0; neither E2 effect is promoted; cross-backbone replication is not claimed; latency remains diagnostic.

### R3-CC-07 — BIRD status is consistent and uninflated (no revision required)

The manuscript, Round-2 response, prompt audit, freeze, and independent technical audit all agree: gold preflight 500/500 under SQLite 3.40.1; expected future generation calls 5,000; formal model calls zero; freeze status `FROZEN_NOT_RUN`; human launch approval/signature absent. No BIRD score enters the manuscript and no DKASQL reproduction or numerical comparison is claimed. The current freeze file SHA-256 is `29C780C63A2DC2BAAE221CFCE52252C716D8720DBEECDC2F7A2FDD5756B42AF5`.

### R3-CC-08 — Abstract is slightly above the target length (minor)

A mechanical count gives approximately 207 words. The Applied Sciences profile targets about 200 words, so this is not a structural failure, but trimming roughly 7--15 words would improve compliance and readability without deleting limitations.

## Acceptance Gates for the Revision

1. Replace every `W10_FRONT_MATTER` marker with author-approved content; zero markers may remain in the submission PDF.
2. Complete the license/repository decision and insert the permitted permanent DOI/URL, or provide journal-compliant availability wording approved by the authors and repository/legal owner.
3. Synchronize the Round-2 response and assembly report to the final TeX/PDF hashes and byte/page counts.
4. Prefer “agent technical reviewers” in the abstract and trim the abstract to approximately 200 words.
5. Re-run the manuscript verifier and record a final clean compile, PDF text scan, and stable hash snapshot after all human metadata changes.

## Overall Assessment

Within its bounded evidence domain, MA-SQLGrid is scientifically auditable and claim-disciplined. The current deficiencies do not require a new scientific experiment, and BIRD must remain unexecuted until the separately frozen human-authorization gate is satisfied. The manuscript is not submission-ready until the major human/compliance gates above are closed.
