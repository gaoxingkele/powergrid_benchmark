# C2GES Round 2 Independent Review: Applied Sciences Fit and Research Integrity

## Review identity and recommendation

- **Role:** fresh independent *Applied Sciences* journal-fit and research-integrity reviewer, Round 2.
- **Frozen manuscript:** `paper_applsci.tex`, SHA-256 `36FF05A08809870E3493BAAF7F5F51191CAB20C00C1F521BE6477A55DD6A2A2D`.
- **Frozen PDF:** `build_r2/paper_applsci.pdf`, SHA-256 `F57B0C5D965450748A8CDE63D0442F3A6FBD08D872CEA1CC54C030F2DDA04CD8`, 10 pages.
- **Materials examined:** TeX and rendered pages; 3 tables and 4 figures; bibliography; round/structural/assembly audits; figure lineage; build08, pre-test, authorization, corrective-history, and post-run records; aggregate and six-contrast JSON; incident exclusions; and the completed 147-configuration post-unblinding development calibration.
- **Recommendation:** **Major Revision**.
- **Confidence:** **5/5** for journal-format, disclosure, artifact-traceability, and claim-alignment findings; **4/5** for statistical-reporting implications.

R2 is substantially more credible than R1. It uses complete PDFs, removes the registered Executive Summary leakage modes, replaces the algebraically redundant counterfactual score, includes a meaningful Semantic-MMR comparator, freezes one corrective test run, independently recomputes its output, and discloses the unfavorable no-CF ablation in every high-impact section. The 10-page PDF is compact but readable and follows the MDPI article structure. It is not yet a submission candidate, however. The chronology no longer matches the completed post-hoc calibration; the exact title remains materially broader than the evaluated corpus; the zero-tail bootstrap resolution is mislabeled in a Holm-adjusted column; the frozen round does not contain everything that the Supplementary Materials statement says is in the manuscript-bound package; and required citation/back-matter/manual submission fields remain open.

## Five most serious issues, ordered by decision impact

### 1. Completed post-unblinding calibration is omitted and described as future work

The manuscript says that development-only calibration “may be explored” (Discussion, Limitations; TeX line 239). It was already completed after the formal results were known. The retained exploratory package evaluates 147 configurations on the 12-report development split, records the post-unblinding chronology, passes an 11-check mechanical audit, and reports that all 12 leave-one-report-out folds select zero CF weight. The best nonzero candidate also remains below its no-CF comparison at both budgets. Leaving this completed analysis in future tense is an inaccurate chronology and creates avoidable selective-reporting risk.

- **Severity:** Major.
- **Evidence Anchor:** dataset: `posthoc_dev_cf_calibration/DEV_ONLY_EXPLORATORY_REPORT.md`, Sections 1--7; text: TeX line 239, “Development-only calibration may be explored”.
- **Required revision:** add a clearly separated “Post-Unblinding Development Sensitivity Analysis” subsection or supplementary note. State the start/end chronology, development-only hash, 147 configurations, 12/12 zero-CF LOO result, best-nonzero negative differences, non-discriminating gates, and prohibition on reuse of the 15 revealed test reports. Do not replace v0.3.1 or add C046/C055 to the primary result table.
- **R3 acceptance test:** the future-tense sentence is gone; the exploratory files are bound in the R3 audit/package; the abstract may mention the conclusion briefly but must not treat the calibration as confirmatory; formal predictions and six registered contrasts remain byte-identical.

### 2. The exact title and claimed application population are not concordant

The title says “for Power Grid Maintenance Reports”, whereas the measured material is 27 selected NERC reliability, disturbance, event-analysis, recommendation, and assessment reports, with 15 used for test. No maintenance work order, inspection record, utility maintenance log, site sample, or qualified maintenance-user evaluation is present. The Abstract, Introduction, Discussion, and Conclusion disclose this unusually clearly, which prevents a hidden overclaim but does not make the title empirically accurate. For *Applied Sciences*, the strongest current fit is applied computing/information processing on NERC technical reports, not validated maintenance engineering.

- **Severity:** Major editorial-fit risk; blocking for any title-concordant effectiveness claim.
- **Evidence Anchor:** text: Abstract and TeX lines 31--35, 231--243, and 247, including “maintenance-domain transfer remains untested”.
- **Required revision:** preferably use a minimal clarifying subtitle or title qualifier naming the NERC technical-report benchmark. If the exact title is retained by author instruction, the first abstract sentences, Featured Application, final Introduction paragraph, Discussion, and Conclusion must continue to state the evaluated population and untested transfer, and the cover letter must disclose the title risk. Do not describe the present work as demonstrating maintenance-workflow utility.
- **R3 acceptance test:** a claim scan finds no empirical maintenance-performance, operator-usefulness, safety, or deployment statement; the title risk is explicitly acknowledged in the cover letter and final audit. Full closure would require a new title-concordant corpus and qualified-domain evaluation, not wording alone.

### 3. Bootstrap resolution and Holm adjustment are conflated

Table 3 labels its final column “Holm p”. Two entries whose frozen raw estimator and computed Holm value are numerically `0.0` are rendered as `<0.0002`, with a note saying that this bound reflects 10,000-resample estimator resolution. The raw two-sided zero-tail estimator has a roughly `2/B` resolution statement, but a Holm-adjusted upper bound cannot simply reuse the raw-test bound: the ordered family multiplier can make the conservative adjusted bound larger. In addition, Methods does not state the exact sign-tail formula or explain that resampling observed paired deltas is not a conventional null-centered test. The current wording therefore gives the right qualitative direction but an inadequately defined and potentially anti-conservative adjusted number.

- **Severity:** Major.
- **Evidence Anchor:** table: Table 3, rows K=5 Semantic-MMR/TextRank and footnote; dataset: `primary_contrasts_holm.json`, where raw and Holm values are both stored as `0.0`; text: TeX lines 114--118 and 185--205.
- **Required revision:** preserve the frozen machine records, but specify the exact resampling/tail formula, resampling unit, seeds, family, and finite-simulation treatment. Either (a) report the registered quantity explicitly as a descriptive bootstrap sign-tail estimator and avoid conventional hypothesis-test language, or (b) add a separately identified, independently recomputed paired null-based sensitivity analysis from the immutable 210-row ledger. If bounds are shown for zero counts, propagate the finite-simulation correction through Holm rather than copying the raw bound into an adjusted column.
- **R3 acceptance test:** Table 3 terminology matches the implemented estimator; no adjusted p-value is reported as zero; any finite-resolution bound is arithmetically valid after multiplicity adjustment; the existing effect estimates and percentile intervals remain unchanged.

### 4. The claimed manuscript-bound verification package is not present in the frozen round

The Supplementary Materials statement says that the manuscript-bound package contains source/exclusion manifests, extraction and rights ledgers, development-search ledger, freeze and authorization records, dependency lock, regression-test report, the 210-row prediction ledger, all statistics, audits, and figure lineage. The frozen R2 round audit contains only six files under `evidence/`; it does not bind the prediction ledger, rights/extraction ledgers, freeze, authorization, dependency lock, regression output, or completed post-hoc calibration. These objects exist elsewhere in the workspace, but existence elsewhere is not proof that the frozen review/submission package contains them. `INCIDENT_EXCLUSION.md` also names only v0.1/v0.2 and does not enumerate failed diagnostic builds, partial dev runs, the terminated orphan run, or the failed v0.3 pre-test freeze. Figure lineage is global rather than per artifact and does not identify the source/transformation for Figures 1--2 or the supported manuscript claims for any figure.

- **Severity:** Major reproducibility and package-integrity defect.
- **Evidence Anchor:** absence: R2 `ROUND_AUDIT.json` and `evidence/` — expected every object claimed by the Supplementary Materials statement; checked the complete 38-file round inventory and `figures/FIGURE_LINEAGE.json`.
- **Required revision:** construct a rights-aware R3 supplementary/editor-review package and bind every included file by relative path, byte size, and SHA-256. Add a complete incident register with status and exclusion reason; never delete or overwrite accident directories. Expand figure/table lineage per artifact with source data, transformation script/hash, caption claim, supported manuscript claims, and limitations. If restricted PDFs/text cannot legally be transferred, remove them and state precisely what can actually be supplied.
- **R3 acceptance test:** package inventory and manuscript list are exact set-equals; every hash re-verifies; no excluded incident output is reachable as a scientific input; editor/reviewer material is permission-consistent; a fresh package verification script passes.

### 5. Submission metadata, core-method citations, and disclosure fields remain incomplete

The corresponding-author email is a literal placeholder. The Acknowledgments says tool-by-tool provider/model/version/date details “must be completed”; the Conflicts statement asks for later confirmation; no explicit funder-role sentence is present; the GitHub repository is not synchronized/tagged/fresh-clone verified; and third-party permissions remain conditional. Bibliographic metadata are much improved and the PDF has 20 rendered references with no unresolved citations, but the core evaluation/reporting still lacks direct references for ROUGE, Holm's procedure, and the particular TextRank/PageRank baseline. Cameron et al. alone does not document all aspects of the implemented percentile/sign-tail procedure. The current R2 round also does not carry a fresh item-level reference audit trail, so the filename `references_cited_verified.bib` is not itself verification evidence.

- **Severity:** Major as a submission-readiness bundle; these items do not invalidate the retained numerical ledger.
- **Evidence Anchor:** text: TeX lines 17 and 249--256; absence: Methods/References — expected primary citations for ROUGE, Holm, and TextRank plus a round-bound citation audit; checked TeX Sections 2--4, rendered References, BibTeX, and R2 round inventory.
- **Required revision:** obtain and verify Yang Yong's email; finalize CRediT/funder-role/conflict statements with author approval; replace the provisional AI sentence with tool/purpose/provider/model/version/date and author-responsibility details from the provenance ledger; add verified primary method citations without inventing metadata; synchronize/tag the repository and verify a fresh clone, or retain an explicit non-release state and label the package not ready for portal upload. Confirm all rights language against actual permissions.
- **R3 acceptance test:** no placeholder or “must be completed/confirmed” wording remains in a submission-candidate PDF except a separately labelled manual hold artifact; all in-text citations resolve and all rendered references are cited; an item-level reference audit accompanies R3; repository and license status are truthful and mechanically checked.

## Claim--evidence audit

| Location | Claim | Verdict | R3 action |
|---|---|---|---|
| Title; Abstract | Method is “for Power Grid Maintenance Reports” | **Overbroad population label.** Current evidence is NERC technical reports, not maintenance records | Qualify title minimally or retain exact title only with conspicuous untested-transfer language and cover-letter disclosure |
| Abstract; Methods 3.2; Table 1 | 40 PDFs/3200 pages, 27 retained, 12/15 split, 12,924 candidates, registered leakage counts zero | **Supported within registered deterministic gates** by build08 and independent audits | Retain the caveat that zero registered patterns do not prove semantic cleanliness |
| Introduction; Methods 3.4; Eq. (1)--(2) | Path deletion is mathematically distinct from weighted degree | **Supported** by construction, counterexample, tests, and nonzero execution diagnostics | Retain as structural/textual non-identity, never physical causal identification |
| Methods 3.6 | 144 configurations selected grid 60 on development; dev Full-minus-no-CF was negative | **Supported** by the frozen decision and ledger | Retain exactly; add the later exploratory calibration separately |
| Methods 3.7 | One authorized corrective run produced 210 rows; independent recomputation passed | **Supported mechanically** by registry, manifest, ledger, and post-run audit | Do not upgrade the evidence class beyond post-audit corrective descriptive |
| Abstract; Results; Table 3 | Full exceeds Semantic-MMR/TextRank “after Holm correction” | **Effect estimates and intervals supported; inferential label/bound incomplete** | Repair estimator terminology and finite-resolution/Holm handling |
| Abstract; Results; Discussion; Conclusion | Full is below strict no-CF by about 0.0033 and CF gain is not demonstrated | **Supported and appropriately prominent** | Preserve unchanged, including intervals crossing zero |
| Results 4.4 | CF channel executed and changed scores/selections | **Supported** by 9,774/19,008 nonzero score differences and 28/30 changed selections | Do not translate activity into usefulness |
| Limitations line 239 | Development-only calibration “may be explored” | **Contradicted by completed artifact** | Replace with factual post-unblinding disclosure |
| Supplementary Materials | Manuscript-bound package contains the listed evidence objects | **Not supported by frozen R2 inventory** | Assemble and hash-bind the actual R3 package or narrow the statement |
| Data Availability | Current GitHub is not asserted to reproduce R2; restricted data depend on permission | **Honest but not submission-ready** | Tag/fresh-clone verify; document precisely what editors/reviewers can receive |
| Acknowledgments | AI was not a qualified expert/author | **Appropriate boundary; tool provenance incomplete** | Retain boundary and fill the submission-time tool ledger |

## Experiment audit

### Required for R3

1. Do **not** rerun or retune the revealed 15-report formal test. Keep v0.3.1 immutable.
2. Recompute only the statistical sensitivity needed to correct the p-value interpretation, directly from the immutable prediction ledger, with an independent verifier and new hash-bound artifact.
3. Disclose the completed 147-configuration, development-only, post-unblinding calibration. It is exploratory evidence and cannot select a replacement model for the existing test.
4. Add a rights-safe sampling inventory covering all 40 reports: report ID/title metadata, genre/year, page count, inclusion/exclusion reason, split, summary boundary, reference length, and candidate count.
5. Add report-level sign counts and retain all paired points; clarify that ROUGE/redundancy are not factuality, engineering usefulness, unsafe omission, or causal-chain correctness metrics.

### Required for a future title-concordant confirmation

1. Freeze a new, never-inspected, license-cleared work-order/inspection/maintenance-report corpus with report/site grouping and a sealed external holdout.
2. Evaluate source faithfulness, cause/event/impact/mitigation coverage, usefulness, and unsafe omission with independent qualified power-grid reviewers; retain disagreement, adjudication, and inter-rater agreement.
3. Tune all tunable systems under comparable development budgets and add a contemporary long-document extractive comparator.
4. Test any new nonzero CF integration only after a positive and stable development gate; never select it from the current revealed test.

### Desirable, not required for the corrective R3 evidence class

- Runtime and memory scaling by candidate count and typed-path count.
- Rights-safe stratification by report genre, reference length, and candidate length, labelled exploratory.
- Channel correlations and selected-sentence overlap to explain why an active CF signal fails to improve ROUGE.

### Unjustified actions

- Retuning on, rerunning a selected method on, or selectively excluding any of the 15 revealed test reports.
- Replacing the adverse formal ablation with the post-hoc development result.
- Calling machine/LLM ratings qualified expert annotation or adjudication.
- Calling the corrective split fresh, preregistered, outcome-unseen, or generally representative.

## Figure and table audit

- **Figure 1 (dataset flow):** counts agree with the manifest, but the rendered boxes are small relative to surrounding whitespace. Enlarge it and add or point to the 13-report exclusion breakdown. Its lineage must identify the build manifest, transformation script/hash, and caption claim.
- **Figure 2 (algorithm):** readable and appropriately carries the proxy warning. The lower arrows visually imply a sequence `Q -> R -> G -> C`, whereas Equation (3) combines parallel channels and position `P` is absent. Redraw all five channels entering a weighted-combination node, then the redundancy-aware selector; show the strict no-CF switch explicitly.
- **Figure 3 (aggregate ROUGE-L):** values match the aggregate JSON and no uncertainty is implied in the caption. Keep it explicitly descriptive; direct value labels would improve the compact 10-page presentation.
- **Figure 4 (paired differences):** the strongest figure. It exposes every direction and the negative no-CF contrast. Add interval/sign-count annotations or a compact companion table, plus a rights-safe report-index mapping.
- **Table 1:** internally consistent. A supplement should expose the report-level inventory behind the aggregate counts.
- **Table 2:** numeric cells match the frozen JSON. The bolding rule is ambiguous for redundancy: lower is better and two K=5 values are bold. Define the visual convention explicitly or bold only the primary ROUGE-L metric.
- **Table 3:** numeric point estimates/intervals match the frozen JSON, but the “Holm p” header and `<0.0002` footnote must be repaired as described above. Include `n=15` and the exact estimator name in the caption.
- **Overall 10-page density:** acceptable for an *Applied Sciences* article and visually clean (0 overfull/underfull boxes), but Related Work is thin and Figures 1--2 use small labels. The abstract is approximately at/slightly above a 200-word target depending on tokenization; shorten it below 200 unambiguously.

## Citation, reproducibility, and ethics audit

### Verified strengths

- The MDPI `applsci` article class, complete front/back matter structure, author names/affiliations, grant number `521300250006`, CRediT roles, required all-authors sentence, IRB/consent statements, and conflict heading are present.
- The PDF compiles with no unresolved citation/reference, LaTeX warning, or overfull/underfull box; all 10 rendered pages were inspected.
- Twenty references render in citation order. The DOI/ACL/publisher metadata have a prior local remediation record, and no fabricated DOI was detected in the examined artifacts.
- The sole formal run is complete, hash-bound, non-resumable, and independently reaggregated with zero discrepancy. Prior invalid results are not used.
- The negative CF result and the causal/proxy boundary are unusually explicit.

### Remaining integrity and submission gates

- A fresh R2 item-level reference existence/context audit is not bundled; previous remediation should be imported and narrowed to the 20 rendered references, with current access dates for web sources.
- Add verified primary sources for ROUGE, Holm, and the exact TextRank/PageRank implementation; do not rely on an unrelated label or an inherited key.
- Expand the incident register to include every failed/partial diagnostic and dev selection run, the orphan process, and the failed predecessor freeze, with immutable exclusion status.
- Provide an actual rights-aware editor/reviewer package. “Available on request” cannot promise transfer that third-party permissions do not allow.
- Finalize corresponding-author email, AI tool provenance, funder role, CRediT confirmation, conflict confirmation, repository tag/fresh-clone receipt, and license decision before portal upload.
- No human participants are reported, so “Not applicable” IRB/consent wording is reasonable subject to institutional/author confirmation. LLM judgments must remain machine assistance and cannot satisfy the missing qualified-expert validation.

## Five questions for the authors

1. Will the authors minimally qualify the title with the evaluated NERC technical-report population, or explicitly accept and disclose that the exact title remains broader than the evidence?
2. Why does R2 describe development calibration as future work after the 147-configuration post-unblinding run was completed, and will the full negative 12/12 zero-CF result be bound into R3?
3. What exact inferential quantity do the authors intend the current bootstrap tail proportion to represent, and how will its finite-simulation bound be propagated through the six-test Holm family?
4. Which files can the corresponding author legally provide to editors/reviewers today, and which require third-party permission that has not yet been obtained?
5. What is the final claimed value of the counterfactual channel—auditable structural diagnosis, interpretability, or selection accuracy—given that both the formal ablation and the post-hoc development search do not support an accuracy gain?

## Round-3 acceptance checklist

- [ ] v0.3.1 predictions, aggregates, six registered contrasts, and negative no-CF result remain immutable.
- [ ] The 147-configuration post-unblinding calibration is disclosed in past tense, labelled exploratory, and package-bound; no current-test reuse occurs.
- [ ] Bootstrap/Holm terminology, formula, and zero-count resolution are corrected; any sensitivity recomputation is independently verified.
- [ ] Title, Abstract, Featured Application, Introduction, Discussion, Conclusion, and cover letter consistently distinguish NERC technical reports from untested maintenance records.
- [ ] The supplementary statement exactly matches a hash-bound, rights-aware package; every incident is registered and excluded.
- [ ] Figure/table lineage is per artifact and complete; Figure 2 shows parallel channels including `P`; Table 2/3 conventions are unambiguous.
- [ ] Primary citations for ROUGE, Holm, and TextRank/PageRank are verified and added; the 20-reference audit is round-bound.
- [ ] Corresponding email, detailed AI disclosure, funder role, CRediT/conflict confirmations, repository tag/fresh-clone receipt, and license status are complete or the deliverable remains explicitly held from submission.
- [ ] No claim asserts physical causal identification, CF accuracy gain, maintenance effectiveness, expert validation, or fresh confirmatory evidence.
- [ ] The final PDF compiles cleanly, is visually inspected page by page, and its SHA-256 appears in the R3 round audit.

## Bottom line

R2 is suitable for another revision round, not for portal upload. Its strongest publishable contribution is a transparent, auditable corrective benchmark and a mathematically distinct typed path-deletion diagnostic whose accuracy ablation is negative. R3 can close most integrity defects without rerunning the formal model experiment. It cannot close the title-concordant maintenance-validation gap without new data and qualified human evaluation; that limitation must remain explicit if the original title is retained.
