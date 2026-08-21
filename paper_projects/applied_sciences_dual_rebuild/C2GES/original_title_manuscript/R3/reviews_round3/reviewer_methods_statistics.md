# C2GES Round 3 Independent Final Review: Methods and Statistics

## Review identity, frozen inputs, and recommendation

- Role: fresh Round-3 methods/statistics/NLP reviewer. I did not participate in
  manuscript revision and did not edit the manuscript, figures, evidence, or
  experiment outputs.
- Frozen source reviewed: `paper_applsci.tex`, SHA-256
  `5C56F9751515F03E5FEBA7C4DFF380CF57280121B5592CD306046322929A03D6`.
- Frozen PDF reviewed: `build_r3/paper_applsci.pdf`, SHA-256
  `3CB2613E9EFA530602DAFB4A165E771E3F7C231AC7C92E8624B209A80F19EBC3`
  (14 pages).
- Immutable prediction ledger checked locally: 210 rows, SHA-256
  `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`.
- Evidence reviewed: R2 methods review; R2-to-R3 response matrix; formal
  configuration/freeze/authorization; independent pre- and post-run audits;
  aggregate and registered-contrast JSON; exact sign-flip code/results/tests;
  rights-safe 40-report inventory; development-calibration decision, report,
  manifest, local ledgers, and mechanical audit; supplement allowlist; figure
  lineage; structural/build/visual audits; and submission holds.
- Recommendation: **minor revision; not yet ready for final audit**.
- Confidence: **5/5** for the numerical, experimental-design, and package-
  reproducibility findings.

The scientific R2 methods blockers are substantially closed. The registered
bootstrap tail quantity is now correctly described as a descriptive sign-tail
summary rather than a null-calibrated p-value. The exact sign-flip analysis is
clearly post-run and conditional on sign symmetry. The completed
147-configuration search is disclosed with the correct post-unblinding
chronology, and its adverse result is not used to replace the frozen test.
The manuscript consistently reports that the counterfactual channel has no
demonstrated ROUGE benefit. My independent enumeration reproduced all six
exact p-values, Holm adjustments, sign counts, and mean differences.

The remaining repairable blocker is package completeness: the R3 supplement
describes and hash-binds development-calibration ledgers and executable code
that are not present in the 49-file allowlist, while the public repository is
explicitly unsynchronized. The rights and author-controlled release gates also
remain open. These defects do not justify rerunning the revealed test set or
changing any result, but they prevent a “ready for final audit” recommendation.

## R2 methods-blocker verification

| R2 blocker | R3 verdict | Evidence |
|---|---|---|
| Registered bootstrap quantity mislabeled as a conventional p-value | **Closed** | TeX lines 145--151 define the estimator, explain observed-distribution centering, deny null calibration, and separate the exact sensitivity. Table 4 uses `Registered t_boot`; no significance claim is based on it. |
| Need a defensible paired null sensitivity with multiplicity control | **Closed as unregistered sensitivity, not confirmation** | TeX lines 151 and 247--261 state all assumptions and the six-item Holm family. Independent enumeration from the 210-row ledger exactly reproduced 32,768 assignments per contrast and every displayed value. |
| Completed 147-configuration search described as future work | **Closed for chronology and interpretation** | TeX lines 155--159, 278--280, and 300--302 report post-unblinding timing, 147 configurations, 12 LOO folds, 12/12 zero-CF winners, 0/12 for the best nonzero candidate, and non-reuse. |
| Named CF contribution framed as causal or accuracy-enhancing | **Closed for claim strength** | TeX lines 33--35, 47, 108--119, 276--288, and 310 define a textual structural perturbation and preserve the negative ablation. |
| Selected n=15 sample, ROUGE-only endpoint, comparator-tuning asymmetry, and title/population mismatch | **Closed for disclosure; not solved as external validity** | TeX lines 19, 31, 59--67, 247, 296--306, and 310 state the selected NERC proxy population, n=15, endpoint boundary, asymmetric tuning, and untested maintenance transfer. New data remain necessary for broader claims. |

## Five most serious residual issues, ordered by decision impact

### 1. Repairable final-gate blocker: the advertised development-calibration evidence set is incomplete in the R3 package

The development report's Artifact Inventory and Supplementary Note S5 name
`run_dev_only_calibration.py`, `test_dev_only_calibration.py`,
`verify_calibration.py`, `candidate_summary_ledger.jsonl`,
`loo_fold_ledger.jsonl`, `per_report_ledger.jsonl`, and
`path_gate_diagnostics.jsonl`. None is present under R3
`supplementary/`, and none appears in `SUPPLEMENT_ALLOWLIST.json`.
`RUN_MANIFEST.json` contains hashes for the missing ledgers and absolute
local paths for code, but a hash is not an executable or a result ledger. This
matters because the 147-configuration and 12/12 LOO result appears in the
Abstract and Conclusion.

- **Severity:** Major for final-package reproducibility; repairable without new
  data or experiment reruns.
- **Evidence anchor:** absence: R3 `supplementary/` and
  `SUPPLEMENT_ALLOWLIST.json` — expected the artifacts named in
  `DEV_ONLY_EXPLORATORY_REPORT.md` Section 7 and
  `POST_UNBLINDING_DEV_CALIBRATION_SUPPLEMENT.md` Section S5; checked the
  exact 49-file allowlist and recursive file set.
- **Required action:** copy byte-identical, hash-verified code and non-verbatim
  ledgers into an appropriate transferable compartment; place any
  rights-sensitive development ledger in a clearly named restricted
  compartment. Rebuild the allowlist, rerun exact-set verification, and replace
  absolute machine paths with package-relative locators. If redistribution is
  not permitted, revise S5 to distinguish “locally retained and hash-bound”
  from “included supplementary material.”
- **Acceptance test:** every artifact claimed as included resolves to exactly
  one allowlisted path; its SHA-256 matches the run manifest; a fresh
  environment can rerun the calibration audit without relying on
  `D:\aicoding\...`.

### 2. Repairable/manual final-gate blocker: the reported method itself is not yet available in a synchronized release

The package contains formal configuration and hash records, but not the complete
frozen C2GES implementation/runner/evaluator dependency tree needed to
regenerate the 210 rows. The Data Availability Statement correctly says that
the GitHub repository is not yet asserted to match R3. This is honest, but it
means computational reproducibility is currently local rather than
editor/reviewer-executable.

- **Severity:** Major for final audit; repairable repository-owner action.
- **Evidence anchor:** text: TeX line 317, “must be synchronized, licensed,
  tagged, archived, and verified from a fresh clone”.
- **Required action:** create an immutable release containing the exact
  hash-bound implementation, environment lock, tests, and rights-safe
  reproduction entry points; archive it and retain a clean-clone execution
  receipt. Do not silently substitute the repository's current branch for the
  frozen implementation.
- **Acceptance test:** a fresh clone at the cited tag matches the manuscript-
  bound code hashes and reproduces all rights-permitted mechanical checks.

### 3. Manual rights blocker: independent external reaggregation is conditional on unresolved third-party permission

All 40 rights records remain fail-closed: rights holder and terms locator are
unverified, and PDF/verbatim redistribution is not authorized. The 210-row
prediction ledger is correctly placed in `restricted_local_only`, but exact
external recomputation of Tables 3--5 and Figure 4 depends on access to that
ledger. The manuscript does not overpromise access; nevertheless, final
editor/reviewer verification cannot currently be guaranteed.

- **Severity:** Major for submission logistics and external reproducibility;
  manual/institutional, not an algorithmic defect.
- **Evidence anchor:** dataset:
  `rights_safe_report_metadata.json`, 40/40 rows with
  `rights_holder=not_verified` and
  `pdf_redistribution_status=not_authorized_pending_human_rights_review`;
  TeX lines 312 and 317.
- **Required action:** obtain a file-by-file rights/terms determination. Give
  the editor only material that may legally be transferred. If the ledger
  cannot be shared, say so unambiguously and provide the maximum lawful
  non-verbatim aggregate verification surface.
- **Acceptance test:** a human-approved rights matrix identifies what may be
  sent to editors/reviewers and the final archive contains no file whose
  transfer status is unresolved.

### 4. New-data boundary: the retained maintenance-report title still exceeds the evaluated population

R3 handles this issue responsibly: the first Abstract sentence, Introduction,
Featured Application, Discussion, and Conclusion all state that maintenance is
aspirational and the data are selected public NERC technical reports. Therefore
the manuscript no longer makes an unsupported maintenance-effectiveness claim.
However, wording cannot make the current evaluation title-concordant. An editor
may still regard the title/population mismatch as material.

- **Severity:** Major only for any title-concordant effectiveness or
  generalization claim; not a numerical defect in the bounded NERC study.
- **Evidence anchor:** text: TeX line 31, “Effectiveness, safety, and usefulness
  on title-concordant maintenance records remain untested.”
- **Required action:** preserve all present boundary language. To remove the
  underlying limitation rather than merely disclose it, collect a new,
  license-cleared maintenance/work-order corpus with a sealed report- or
  site-level holdout.
- **Acceptance test:** absent new data, no maintenance effectiveness, safety,
  or operator-utility claim appears anywhere. With new data, the protocol must
  be frozen before holdout access.

### 5. New-data/human-validation boundary: n=15, ROUGE-only evaluation, lexical proxy semantics, and tuning asymmetry limit inference

The paper now states all four limitations. The 15 reports come from one
organization and a conservatively selected 40-report inventory; ROUGE measures
Executive-Summary overlap only; Semantic-MMR's 0.5 coefficient was fixed while
C2GES received 144 development configurations; and the role/edge taxonomy has
no qualified-expert gold labels. These limitations do not invalidate the
descriptive corrective benchmark, but they prevent claims of semantic causal
validity, general superiority, safety, or operational usefulness.

- **Severity:** Major for broader scientific claims; requires new data and
  qualified humans to close, not another analysis of the revealed 15 reports.
- **Evidence anchor:** text: TeX lines 300--306.
- **Required action:** keep current claims bounded. A future study should use a
  newly sealed holdout, equal tuning budgets for tunable comparators, at least
  one modern long-document extractor, and blinded qualified power-grid ratings
  for faithfulness, role-chain coverage, unsafe omission, and usefulness, with
  disagreements, adjudication, and inter-rater agreement retained.
- **Acceptance test:** no current claim exceeds Executive-Summary lexical
  overlap on the selected NERC split; any stronger claim traces to a new frozen
  protocol and genuinely unseen data.

## Claim--evidence audit

| Manuscript claim | Verdict | Exact evidence / boundary |
|---|---|---|
| 27 of 40 reports retained; 12 development, 15 test; 12,924 candidates | **Supported** | Rights-safe metadata independently reaggregates to 40 rows, 27 included, 13 excluded (11 missing summary heading; 2 missing generic endpoint). TeX lines 65--75 and Table 2 agree. |
| One formal run yielded 210 rows and all registered outputs were independently recomputed | **Supported locally** | 15 x 7 x 2 = 210; prediction hash and post-run audit agree. External recomputation remains rights/release constrained. |
| The bootstrap tail is descriptive, not a conventional p-value | **Supported and correctly framed** | Equation (4), TeX lines 145--149, implements twice the smaller observed-bootstrap sign tail and states the null-calibration defect. |
| Exact sign-flip p-values and Holm-adjusted values in Table 5 | **Numerically verified** | Independent product enumeration from the immutable ledger reproduced all six values exactly: 0.436768/0.436768, 0.000305/0.001526, 0.000122/0.000732, 0.200684/0.401367, 0.006592/0.026367, and 0.009644/0.028931 (raw/Holm). |
| Sign counts 7/7/1, 14/1/0, 14/1/0, 6/8/1, 11/4/0, 13/2/0 | **Verified** | Independently reaggregated from the 210 rows; Figure 4 and Table 5 match. |
| Full-minus-no-CF equals about -0.0033 at both budgets and intervals cross zero | **Supported** | Independent means are -0.003332269 and -0.003360435; registered intervals [-0.010889, 0.002826] and [-0.008306, 0.001040]. |
| Full exceeds Semantic-MMR and TextRank on this retained split | **Supported as a bounded descriptive comparison** | Means and paired differences agree with the ledger; exact sensitivity is assumption-conditional and post-run, and the paper avoids population-wide superiority. |
| 147 post-unblinding configurations; zero CF selected in 12/12 LOO folds | **Supported by local retained evidence; frozen package incomplete** | Local ledgers have 147 summary rows, 12 fold rows, 3,528 per-report-budget rows, and hashes matching `RUN_MANIFEST.json`; the decision says C046 won 12/12 and C055 0/12. Those ledgers/code are absent from R3's allowlist. |
| No retuning or rerun on the 15 revealed test reports | **Supported by chronology, code inspection, and unchanged formal hash; not an OS-level access proof** | Calibration executable binds only the development file and prior development decision; manifest says both forbidden-access flags are false; formal ledger hash is unchanged. The manuscript correctly calls the activity post-unblinding despite the file boundary. |
| CF is an active, non-degree-equivalent structural diagnostic but has no demonstrated ROUGE gain | **Supported within the computational definition** | Equations (1)--(3), unit/audit evidence, 28/30 changed selections, and 9,774/19,008 nonzero score comparisons support activity/non-identity. Formal and exploratory ablations do not support a gain. |
| The study validates maintenance reports, physical causal relations, safety, or expert usefulness | **Not claimed** | High-impact sections explicitly deny these interpretations. New data/human evaluation would be required. |

## Experiment audit

### Required before final audit; no model/test rerun needed

1. Complete the supplementary evidence set for the 147-configuration analysis
   or correct every inventory statement so it names local-only artifacts
   honestly.
2. Synchronize and archive the exact code release, then retain a clean-clone
   hash/test receipt.
3. Complete the human rights determination and generate the final transfer
   allowlist.
4. Re-run only mechanical package, manifest, build, and fresh-clone checks after
   packaging. These are not scientific reruns.

### Desirable for a future new-data study

- Use a newly acquired, never-inspected maintenance-report or work-order
  corpus, grouped at report/site level with a sealed external holdout.
- Give tunable comparators equal development-search budgets and add a modern
  long-document extractive comparator.
- Add qualified, blinded human assessment of source faithfulness,
  cause/event/impact/mitigation coverage, unsafe omission, and engineering
  usefulness; retain raw ratings, disagreement, adjudication, and agreement.
- Predefine a minimum effect of practical interest or precision target at the
  report level rather than interpreting non-significance at n=15 as
  equivalence.
- If a nonzero CF ranking channel is studied again, require a positive and
  stable development gate before a one-time new-holdout evaluation. Otherwise
  retain CF as auxiliary diagnostic output.

### Unjustified reruns or reinterpretations

- Do not tune any weight, gate, endpoint, subgroup, comparator, or wording from
  favorable patterns in the revealed 15 reports.
- Do not evaluate C046, C055, or another post-unblinding configuration on the
  existing test split.
- Do not replace the adverse frozen ablation with the 147-configuration
  exploration or call that exploration prospective, confirmatory, or
  outcome-unseen.
- Do not describe the registered bootstrap sign-tail as a conventional p-value
  or the exact sign-flip sensitivity as assumption-free.
- Do not use an LLM/API panel as qualified human expert validation or
  adjudication.

## Figure and table audit

- **Figure 1 / dataset flow:** counts and branches match the 40-row inventory.
  The development/test separation and single corrective run are visible.
- **Figure 2 / algorithm:** the R2 visual defect is closed. Q, R, G, C, and P
  enter the weighted combination in parallel, and the strict no-CF switch and
  proxy boundary are visible.
- **Figure 3 / aggregate ROUGE-L:** values match Table 3 and the aggregate JSON.
  It is explicitly descriptive; Figure 4 supplies the paired view.
- **Figure 4 / paired differences:** all 90 points and six sign-count labels
  match independent ledger reaggregation. Rights-safe indices are linked to
  Supplementary Table S1.
- **Tables 2--5:** n=15 is stated; bold is restricted to maximum ROUGE-L,
  underline to minimum redundancy; registered sign-tail and unregistered exact
  sensitivity are separated. All checked values match retained artifacts.
- **Visual quality:** all 14 rendered pages were reviewed. Figures, equations,
  tables, captions, and references are legible; no clipping or statistical
  symbol ambiguity was observed.

No figure or table repair is required from the methods/statistics perspective.
If package paths change, only supplementary locators and their hashes should be
updated; plotted scientific values must remain unchanged.

## Reproducibility and ethics findings

### Verified strengths

- Formal predictions, means, intervals, contrasts, and adverse CF results are
  immutable and internally consistent.
- Registered and post-run evidence classes are visibly separated.
- The exact sensitivity states report independence/sign-exchangeability,
  inclusive two-sided enumeration, zero-delta treatment, and one six-test Holm
  family. Holm remains valid under dependence among contrasts.
- The complete 40-report sampling frame and all 13 exclusions are accounted
  for without transferring report prose.
- R1/v0.1/v0.2 incidents remain excluded, and current text does not silently
  rehabilitate them.
- Test-set retuning is explicitly prohibited in Methods, Limitations,
  Conclusion, and the supplementary note.

### Residual reproducibility limits

- The R3 calibration package is summary-complete but not execution-complete.
- The public repository is not a verified release of the frozen implementation.
- Rights restrictions prevent an unqualified promise of editor/reviewer access
  to the prediction ledger and source-derived text.
- The selected corpus and n=15 design do not support broad population
  generalization; the exact sensitivity's assumptions cannot be established
  from this sample.

### Ethics boundary

No human participants or animals were used in the reported computational
experiment, so the not-applicable IRB and consent statements are coherent.
The paper correctly states that AI systems were used as tools rather than
authors, qualified grid experts, annotators, or adjudicators. Qualified-human
validation remains absent and must not be replaced by LLM labeling. Rights,
AI-use provenance, CRediT, funder role, conflict declaration, and corresponding
email require responsible human confirmation before portal upload.

## Five questions for the authors

1. Will the authors include the calibration executable, tests, and all four
   hash-bound ledgers in the final package, or revise Supplementary Note S5 to
   label them explicitly as local-only retained evidence?
2. Which immutable repository tag/archive will bind the exact formal runner,
   method modules, model tree, evaluator, and dependency lock, and what
   fresh-clone receipt will demonstrate equivalence?
3. What file-by-file legal basis will permit the editor or reviewers to inspect
   the restricted prediction ledger and, if needed, source PDFs or derived
   text?
4. Do the authors accept that retaining the current title leaves an irreducible
   title/population limitation until a new maintenance-record corpus is
   evaluated, even though R3 now discloses it correctly?
5. Is the intended final scientific contribution explicitly limited to an
   auditable structural diagnostic plus bounded NERC lexical-overlap results,
   with no claimed CF accuracy gain, physical causal validity, safety, or
   maintenance-workflow effectiveness?

## Final acceptance decision and tests

### Decision

**Minor revision; not ready for final audit.** No new model experiment on the
current test set is required or justified. The R2 scientific-statistical
blockers are closed at the manuscript level. Final clearance is withheld for
the repairable evidence-package/repository defects and the unresolved manual
rights/author fields. The new-data limitations do not require fabrication or a
revision-time test reuse; they require continued claim boundaries unless the
authors conduct a genuinely new study.

### Acceptance tests

- [x] Bootstrap tail is relabeled and no calibrated-p-value claim remains.
- [x] Exact 2^15 sign-flip values, six-item Holm adjustment, assumptions, and
  post-run status are correct.
- [x] The 147-configuration chronology, 12/12 zero-CF result, and non-reuse
  prohibition are explicit.
- [x] CF negative results appear in Abstract, Results, Discussion, and
  Conclusion.
- [x] The 40-report inventory, 27/13 accounting, n=15, ROUGE boundary,
  comparator-tuning asymmetry, and title-domain boundary are explicit.
- [x] No evidence of test-set hyperparameter retuning or formal-output
  replacement was found.
- [ ] Calibration code and all claimed ledgers are present in, or accurately
  excluded from, the final package with package-relative locators.
- [ ] Exact frozen implementation is synchronized, tagged, archived, and
  verified by a fresh-clone receipt.
- [ ] Human rights review establishes the lawful editor/reviewer transfer set.
- [ ] Corresponding email, funder wording/role, CRediT, conflicts, and AI-use
  provenance are confirmed by responsible humans.

## Arithmetic recomputation note

The manuscript reports bootstrap intervals and exact randomization values, not
t, z, F, chi-square, GRIM/GRIMMER, or df-to-N statistics covered by the ARS
bounded arithmetic procedures. I therefore did not invent an inapplicable
receipt. I independently recomputed the report-level means, signs, complete
2^15 product enumeration, and Holm step-down values directly from the frozen
ledger; these calculations matched every Table 5 value exactly.
