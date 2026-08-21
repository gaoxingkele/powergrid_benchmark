# C2GES Round 3 Independent Review: Applied Sciences Fit and Research Integrity

## Review identity, frozen object, and recommendation

- **Role:** fresh Round-3 *Applied Sciences* and research-integrity reviewer.
- **Review mode:** read-only re-review of the frozen R3 manuscript, PDF, audits,
  figures, lineage, and supplementary compartments. I did not edit or rerun the
  manuscript, summarization method, or formal test.
- **Frozen TeX:** `paper_applsci.tex`, SHA-256
  `5C56F9751515F03E5FEBA7C4DFF380CF57280121B5592CD306046322929A03D6`.
- **Frozen PDF:** `build_r3/paper_applsci.pdf`, SHA-256
  `3CB2613E9EFA530602DAFB4A165E771E3F7C231AC7C92E8624B209A80F19EBC3`,
  14 pages.
- **Supplement allowlist:** SHA-256
  `9318AC2C159D3D86AE6BA6225F5B167B059BBC55854304847AB3A504A711B097`.
- **Recommendation:** **Major Revision**.
- **Confidence:** **5/5** for package, build, declaration, and claim--artifact
  findings; **4/5** for editorial fit because the editor may differ on whether
  the exact aspirational title is acceptable.

The 14-page manuscript is a substantial and scientifically more candid repair
of R2. Its title, first abstract sentence, Results, Limitations, and Conclusion
now agree that the evaluated population is a selected NERC technical-report
proxy corpus and that the counterfactual channel did not improve ROUGE. I
independently recomputed the six exact sign-flip values, six-item Holm values,
sign counts, and all 14 method--budget aggregate rows from the immutable
210-row prediction ledger; they match the paper. The 40-row inventory also
reaggregates to 27 included and 13 excluded reports. These are important
strengths.

R3 nevertheless fails the protocol's submission-candidate gate. The exact-set
allowlist verifies the files that happen to be present, but the package omits
several artifacts that its own development-calibration supplement says are
bound. Its figure lineage is not yet per-artifact reproducibility evidence, the
R3 citation audit is not the item-level/context audit required by R2, and all
manual author, funder, AI, rights, and repository holds remain open. The title
continues to name a population that was not evaluated. These are not reasons
to alter the immutable formal result; they are reasons not to call this frozen
round submission-ready.

## Closure audit of the Round-2 blockers

| R2 blocker | R3 verdict | Evidence |
|---|---|---|
| Completed 147-configuration calibration omitted/future-tense | **Closed in the manuscript; package closure failed** | TeX lines 157--159, 280, 302, and 310 disclose the chronology, 147 candidates, 12 LOO folds, 12/12 zero-CF outcome, and no-reuse boundary. The package omits the underlying candidate, fold, and report ledgers named by its own supplementary note. |
| Maintenance title versus evaluated population | **Partially closed by disclosure, not empirically closed** | TeX lines 19, 21, 31, 296, 300, and 310 consistently identify the NERC proxy population and untested transfer. No maintenance work-order/inspection corpus or qualified-user evidence exists. |
| Registered bootstrap quantity mislabeled as a conventional p-value | **Closed** | TeX lines 145--151 and Table 4 label it a descriptive observed-delta sign-tail estimator. No significance claim is based on it. |
| Need a defensible null sensitivity | **Closed as unregistered post-run sensitivity** | Six exact paired sign-flip enumerations use 32,768 assignments each and one six-item Holm family. Fresh recomputation from ledger SHA `AAE2...338F` matched every raw and adjusted value. This is correctly not called confirmatory. |
| Hidden report heterogeneity / unclear 40-report accounting | **Closed** | Figure 4 and Table 5 expose signs; the rights-safe JSON has 40 unique rows, 27 included, 13 excluded, 3,200 pages, 12,924 included candidates, and a 12/15 split. Exclusions are 11 missing-summary-heading and 2 missing-summary-end records. |
| Supplementary statement exceeded actual package | **Not closed** | The 49-file allowlist is internally exact, but it is not complete relative to the supplement's own bound-artifact list; details appear in Issue 1. |
| Figure 2 channel topology and Figure 4 sign annotation | **Closed visually** | The algorithm figure shows five parallel inputs and the strict no-CF switch; Figure 4 shows all points and `+/-/0` counts. |
| Per-artifact figure lineage | **Not closed** | Current lineage lacks output hashes and manuscript figure/caption anchors and does not bind all stated sources; Figure 1's counts are hard-coded rather than read from the named inventory. |
| Missing primary ROUGE, TextRank, and Holm citations | **Closed for presence; final reference audit remains open** | All three primary references are cited and render. The R3 audit verifies only the set plus metadata for these three, not all 23 contextual uses. |
| Email, funder, CRediT/COI, AI provenance, rights, and repository | **Open manual** | TeX lines 17 and 313--319 and `SUBMISSION_HOLDS.md` explicitly retain the holds. |

## Five most serious issues, ordered by decision impact

### 1. The supplementary allowlist is exact but scientifically incomplete

The verifier compares `SUPPLEMENT_ALLOWLIST.json` with the files already placed
under `supplementary/`; it has no completeness contract against all artifacts
claimed by the paper and supplementary notes. Consequently, `PASS 49/49`
cannot establish that the evidence package is complete.

The bound-artifact list in
`POST_UNBLINDING_DEV_CALIBRATION_SUPPLEMENT.md`, Section S5, explicitly names
`candidate_summary_ledger.jsonl` (147 rows), `loo_fold_ledger.jsonl` (12 rows),
and `per_report_ledger.jsonl` (3,528 rows). None appears in the allowlist.
`RUN_MANIFEST.json` additionally hash-binds `path_gate_diagnostics.jsonl` (36
rows), which is also absent. The executable, its test and verifier, its frozen
code snapshots, and `RUN_STATE.json` are absent too. The four omitted ledgers
exist in the retained workspace with hashes
`0F0E...562D`, `B22D...955B`, `73C9...3FB`, and `B9BA...B0EC`, respectively,
but existence outside the frozen package does not satisfy the R2 acceptance
test.

There is also stale-package contamination: the transferable set contains
`R2_TO_R3_RESPONSE_MATRIX_DRAFT.md` alongside the final matrix. It is a
different, obsolete draft and has no scientific or editorial purpose in the
submission package. No withdrawn v0.1/v0.2 numerical output was found in the
transferable scientific inputs, so this is package-hygiene pollution rather
than evidence contamination.

- **Severity:** Major, blocking final audit.
- **Required revision:** define a semantic completeness schema, not only a
  directory set-equality check. Include every calibration artifact claimed as
  bound, plus sufficient code/tests/snapshots to reproduce and verify it, or
  narrow the manuscript and supplement statements to the smaller evidence
  class actually delivered. Remove the obsolete draft response matrix.
- **Acceptance test:** a clean-room unpack receives one authoritative response
  matrix; every file named in Sections S1--S5 resolves within the package;
  all hash edges resolve; the calibration verifier and tests run using only
  packaged permitted inputs; exact-set, required-role, and forbidden-file
  checks all pass.

### 2. Figure lineage remains incomplete and Figure 1 is generated from hard-coded counts

The four figures are legible and their displayed values match the manuscript.
However, `FIGURE_LINEAGE.json` gives only a global generation-script hash and
four prose records. It does not record output PDF/PNG hashes, manuscript figure
numbers and caption anchors, source-file hashes per artifact, or the exact
supported claim locations requested in R2. More importantly,
`generate_figures.py::dataset_flow()` hard-codes 40, 13, 27, 12, 15, 3,200,
12,924, and 144; it never reads the build manifest or rights-safe inventory that
the lineage calls its source. The algorithm diagram likewise cites TeX
Equations (1)--(3) without binding the TeX hash as that artifact's input. The
script reads aggregate/prediction files from an external workspace path rather
than the packaged copies, so a clean package cannot regenerate all figures.

- **Severity:** Major reproducibility defect; the rendered figures themselves
  contain no detected numeric error.
- **Required revision:** make each data-driven figure read its packaged source,
  assert source hashes and expected row/count invariants, and generate from a
  clean unpack. Expand lineage per artifact to include manuscript figure ID,
  caption/claim anchors, input paths and hashes, script/function/hash, output
  hashes, and limitations.
- **Acceptance test:** remove access to the parent workspace, regenerate all
  four figures from the unpacked package, obtain the declared hashes, and have
  an independent script rederive every displayed number and sign label.

### 3. The R3 citation audit is not the required item-level final audit

`R3_CITATION_AUDIT.json` proves that 23 cited keys exist and render and provides
fresh metadata checks for ROUGE, TextRank, and Holm. It explicitly states that
all other contextual claims merely “inherit the local remediation record.” The
record is not bound in R3, and the audit has no 23-row bibliographic verdict,
claim-location mapping, source locator, contextual-support verdict, or search
trail. The R2 reviewer required an item-level audit accompanying R3. A clean
set/bibliography check is not equivalent to final claim--citation verification.

- **Severity:** Major final-integrity gap; no specific fabricated citation was
  identified in this review.
- **Required revision:** bind an item-level audit for all 23 cited references,
  with authoritative metadata locators and each in-text use mapped to the
  supporting source. Mark inaccessible or not-human-read full text explicitly;
  do not infer contextual support from a DOI match.
- **Acceptance test:** 23/23 references have explicit existence and metadata
  verdicts; every citation occurrence has a context verdict; zero orphan,
  dangling, not-found, or major-distortion records remain.

### 4. The exact title remains broader than the evidence class

The disclosure is now unusually clear and internally consistent: the first
abstract sentence, Featured Application, Introduction, Discussion, Conclusion,
cover letter, and holds all say that “maintenance” is aspirational and that the
evaluated population is selected NERC reliability/disturbance technical
reports. This avoids a hidden claim. It does not make the title empirically
concordant. The paper contains no utility maintenance work orders, inspection
records, site grouping, qualified maintenance-user evaluation, safety endpoint,
or evidence that the extraction regime transfers to those records. A title
that requires its first sentence to disclaim its population is a material
desk-review risk for *Applied Sciences*.

- **Severity:** Major editorial-fit risk and a blocker to any title-concordant
  effectiveness interpretation.
- **Required revision:** either minimally qualify the title with the NERC
  technical-report benchmark, or obtain a license-cleared, untouched,
  title-concordant corpus and qualified validation. If the authors retain the
  exact title, the current conspicuous scope language and cover-letter warning
  must remain and the submission must accept this desk-rejection risk.
- **Acceptance test:** no statement implies demonstrated maintenance-record
  effectiveness, safety, operator utility, or physical causal identification;
  editor-facing materials disclose the mismatch; any stronger claim is backed
  by genuinely new title-concordant evidence.

### 5. Required submission declarations and transfer permissions remain unresolved

The PDF still says that Yang Yong's email is to be provided, the exact funder
name and role must be confirmed, the conflict declaration requires author
confirmation, and AI provider/model/version/purpose/date fields remain a manual
hold. Repository synchronization, license, release tag, archival receipt, and
fresh-clone verification are also absent. All 40 rights rows say PDF and
verbatim-text redistribution is not authorized pending human review; reviewer
access is only “by corresponding author subject to third-party terms.” The
restricted prediction ledger contains verbatim derived text and therefore
cannot currently be sent to an editor/reviewer under the package's own rule.

- **Severity:** Major submission-readiness bundle; it does not alter the
  numerical findings.
- **Required revision:** obtain author/institutional confirmations and record
  file-by-file rights decisions; fill the verified email, exact funder and role,
  final CRediT/COI, and complete AI-use provenance; synchronize and archive a
  licensed code release; make data-access wording match what can legally be
  delivered.
- **Acceptance test:** no “to be provided,” “must confirm,” or “manual hold”
  remains in a portal candidate; a fresh-clone receipt matches the package;
  every transmitted file has an affirmative permission basis. If permissions
  remain unavailable, remove restricted content from the transfer ZIP and state
  the resulting verification limitation rather than promising access.

## Claim--evidence audit

| Location | Claim | Verdict and evidence |
|---|---|---|
| Title; Abstract; Featured Application | Framework is “for Power Grid Maintenance Reports” | **Population-overbroad but conspicuously bounded.** The evaluated set is NERC technical reports, not maintenance records. |
| Abstract; Section 3.2; Table 2 | 40 PDFs, 3,200 pages, 27 retained, 13 excluded, 12/15 split, 12,924 candidates | **Verified.** Fresh reaggregation of the 40-row rights-safe JSON matched all counts; exclusion reasons are 11+2. Rights and independent year/genre verification remain unresolved. |
| Sections 3.3--3.5; Equations (1)--(3) | Typed path deletion is distinct from degree and executed as specified | **Supported as a deterministic structural-text mechanism.** The paper properly excludes physical causal identification and semantic validity. Expert role/edge validation is absent. |
| Sections 3.7--3.8; Tables 3--5 | Seven methods, two budgets, 210 rows; Full exceeds Semantic-MMR/TextRank but trails strict no-CF | **Verified numerically.** Fresh ledger aggregation matched every mean and paired contrast. This is evidence only on the selected corrective split. |
| Abstract; Section 3.8; Table 4 | Registered bootstrap intervals and descriptive sign-tail records | **Supported with corrected terminology.** No conventional p-value/significance claim remains. |
| Abstract; Section 3.8; Table 5; Conclusion | Exact sign-flip sensitivity preserves Semantic-MMR/TextRank directions after six-item Holm adjustment | **Verified conditionally.** Independent enumeration reproduced raw values `0.436768, 0.000305, 0.000122, 0.200684, 0.006592, 0.009644` and Holm values `0.436768, 0.001526, 0.000732, 0.401367, 0.026367, 0.028931`. The sign-symmetry assumption and post-run status are stated. |
| Sections 3.9 and 4.5; Abstract; Conclusion | 147 development-only configurations and 12/12 LOO zero-CF winners | **Numerically corroborated but incompletely packaged.** Source ledgers have 147 candidate rows, 12 fold rows, 3,528 candidate-report-budget rows, and 12 C046 winners; those ledgers are absent from R3 supplement. |
| Section 4.4 | Channel changed 9,774/19,008 scores and 28/30 selections | **Supported by the retained formal evidence and appropriately interpreted only as execution, not utility.** |
| Supplementary Materials | Transferable package contains the described evidence and is exact | **Misleading by omission.** Exact for the 49 present files, not complete against the supplement's own claimed calibration artifacts. |
| Data Availability | Restricted verification material may be requested subject to permission | **Truthful conditional statement, but presently non-operational.** No affirmative transfer permission is recorded. |
| Acknowledgments / declarations | AI was not an expert/author; authors retain responsibility | **Appropriate boundary; provenance incomplete and author confirmation open.** |

## Experiment audit

### Required before a revised final audit

1. **No formal-test rerun is required or justified.** Preserve v0.3.1 and ledger
   SHA `AAE2...338F` unchanged.
2. Complete and clean the package for the already completed 147-configuration
   development calibration; do not run C046, C055, or any new configuration on
   the revealed 15-report test set.
3. Regenerate figures from packaged sources in a clean environment and verify
   the declared outputs independently.
4. Run the final item-level reference/context audit and a fresh package audit
   after the above changes.

### Required only for a title-concordant effectiveness claim

1. Freeze a new, license-cleared maintenance-work-order/inspection corpus with
   report/site grouping and an untouched external holdout.
2. Use qualified power-grid personnel to evaluate source faithfulness,
   cause/event/impact/mitigation coverage, engineering usefulness, and unsafe
   omission; retain independent ratings, disagreement, adjudication, and
   agreement statistics.
3. Give tunable baselines comparable development budgets and register the
   integration and analysis before revealing the new holdout.

### Desirable but not required for the present bounded paper

- Runtime/memory scaling by candidate count and typed-path count.
- A clean-room reproduction on a rights-cleared subset.
- Rights-safe exploratory channel-correlation and selection-overlap diagnostics.

### Unjustified reruns or relabeling

- Any tuning, subgroup selection, exclusion, or selected-method rerun on the 15
  revealed test reports.
- Replacing the negative formal ablation with post-unblinding development
  exploration or calling that exploration prospective/confirmatory.
- Calling LLM or agent ratings qualified expert annotation or adjudication.
- Treating sign-flip sensitivity as registered, assumption-free, or a cure for
  the selected corrective evidence class.

## Figure and table audit

| Artifact | Verdict |
|---|---|
| Figure 1, dataset flow | **Visually pass; lineage fail.** Counts match the inventory, but the generator hard-codes them and does not read the claimed source. Labels are legible in the 14-page PDF. |
| Figure 2, algorithm | **Visual/content pass; lineage partial.** All Q/R/G/C/P channels enter in parallel and strict no-CF is shown. Bind the TeX/method source hash and output hashes. |
| Figure 3, aggregate ROUGE-L | **Pass numerically.** Fresh ledger means match the bars. Caption correctly calls them descriptive. Clean-package input is still missing. |
| Figure 4, paired differences | **Pass numerically and visually.** All 15 points per panel and the six sign counts match fresh computation. |
| Table 1 | **Pass as executable taxonomy, not validation evidence.** The no-expert-label boundary is explicit. |
| Table 2 | **Pass.** Counts and audit denominators are internally consistent. |
| Table 3 | **Pass.** Seven conditions, two budgets, four metrics match the ledger; bold/underline conventions are clear. |
| Table 4 | **Pass after R2 correction.** Registered quantity is no longer called a hypothesis-test p-value. |
| Table 5 | **Pass numerically.** Exact and Holm values, assignment count, and sign counts match independent recomputation. |
| Overall layout | **Journal-fit pass.** Four figures, five tables, four displayed equations, six top-level sections, and 23 references fit a readable 14-page MDPI draft. All pages were inspected; no clipping, overlap, missing glyph, unresolved reference, or illegible figure was observed. The sparse final bibliography page is cosmetic, not a defect. |

## Reproducibility, rights, and ethics findings

### Strengths

- Formal predictions are immutable, separately restricted, and hash-bound.
- Registered, corrective, exploratory, and post-run evidence classes are not
  conflated in the manuscript.
- Negative Full-minus-no-CF results are prominent in the Abstract, Results,
  Discussion, and Conclusion.
- The paper does not substitute AI review for qualified power-grid personnel.
- Source PDFs and full extracted datasets are absent from the transferable set;
  every current rights record fails closed.
- The incident register preserves and excludes v0.1/v0.2, failed builds,
  partial development runs, the orphan run, and the failed freeze.

### Blocking or manual findings

- The scientific supplement is not complete enough for clean-room
  reproduction of the calibration or figures.
- The restricted ledger cannot presently be transmitted, so an editor cannot
  reproduce the exact statistics unless rights are affirmatively resolved.
- Repository code is intended, not frozen/released/fresh-clone verified.
- Qualified human validation and title-concordant data do not exist.
- Corresponding email, exact funder/role, author CRediT/COI confirmation, and
  complete AI-use provenance remain author-owned manual gates.
- The current citation audit is mechanical/set-level rather than final
  item-level/context verification.

## Concrete revision instructions and acceptance tests

1. **Rebuild the supplement manifest around required artifact roles.** A schema
   must require the calibration executable, frozen code snapshots, tests,
   verifier, state, four machine ledgers, decision, report, and manifest. Test
   both missing-required and forbidden-extra cases.
2. **Remove stale content.** Exclude
   `R2_TO_R3_RESPONSE_MATRIX_DRAFT.md`; retain one final response matrix and one
   immutable incident register.
3. **Repair figure provenance.** Generate from packaged files only; add per-file
   input/output hashes and manuscript anchors; verify counts/labels by parsing
   sources rather than embedding constants.
4. **Produce a 23-item citation/context audit.** Bind it into R3 and verify all
   rendered uses, not merely BibTeX key presence.
5. **Close or explicitly preserve the title decision.** A minimally qualified
   title is preferable; if the exact title is retained, keep the current first-
   sentence and cover-letter disclosures and make no stronger claim.
6. **Complete author-controlled declarations and rights.** The final package
   may advance only after email, funder, CRediT/COI, AI provenance, repository,
   and file-by-file transfer decisions are evidenced.
7. **Re-freeze and re-audit.** Produce a new TeX/PDF/figure/supplement hash set,
   clean-unpack build receipt, clean-unpack reproduction receipt, and final
   response matrix closing every Round-3 item.

## Final acceptance decision

**Not ready for final audit or portal submission; Major Revision.** The core
numerical claims in this frozen R3 draft are internally consistent and unusually
well bounded, and no test rerun is requested. Final acceptance is withheld
because the package-completeness and figure-lineage blockers are genuine
research-integrity defects, the required item-level citation audit is absent,
and all author/rights/repository gates remain open. A repaired R3.1/R4 package
can be reconsidered without changing the immutable v0.3.1 predictions or
improving the negative counterfactual ablation.

