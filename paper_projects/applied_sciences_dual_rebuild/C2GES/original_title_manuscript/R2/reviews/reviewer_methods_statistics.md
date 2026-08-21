# C2GES Round 2 Independent Review: Methods and Statistics

## Review identity and recommendation

- Role: fresh independent methods/statistics/NLP reviewer, Round 2.
- Frozen manuscript reviewed: `paper_applsci.tex` (SHA-256 `36FF05A08809870E3493BAAF7F5F51191CAB20C00C1F521BE6477A55DD6A2A2D`) and `build/paper_applsci.pdf` (SHA-256 `F57B0C5D965450748A8CDE63D0442F3A6FBD08D872CEA1CC54C030F2DDA04CD8`).
- Evidence reviewed: the v0.3.1 freeze, development decision, 210-row prediction ledger, aggregate/contrast JSON, independent pre- and post-run audits, full-PDF build08 audit, incident history, figure lineage, and the later development-only CF calibration.
- Recommendation: **major revision**.
- Confidence: **5/5** for the statistical, experimental-design, and reproducibility findings.

R2 is a material scientific improvement over R1. The complete-PDF rebuild closes the registered Executive Summary leakage modes, the path-deletion variable is now mathematically and computationally distinct from weighted degree, the strict ablation changes only the CF coefficient, and the paper reports the adverse CF result prominently. The formal run and independent recomputation are unusually well documented. Nevertheless, the inferential p-value construction is not a valid null-calibrated paired test, the retained maintenance-report title is unsupported by the sampled population, and an already completed post-unblinding development search is described in the paper as merely future work. These issues require R3 correction. The existing v0.3.1 predictions must remain immutable; no favorable retuning on the 15 revealed reports is justified.

## Five most serious issues, ordered by decision impact

### 1. Blocking for the retained title: no maintenance-report population was evaluated

The title claims performance “for Power Grid Maintenance Reports,” while the measured population is 27 selected public NERC reliability, disturbance, event-analysis, recommendation, and assessment reports, with only 15 test reports. The manuscript discloses this clearly in the Abstract and at lines 31, 59, 233, 237, and 247, but disclosure does not create title-concordant evidence. There are no utility work orders, inspection reports, maintenance logs, site-level sampling frame, or qualified operator judgments. ROUGE against Executive Summaries cannot establish maintenance usefulness or unsafe-omission risk.

- **Severity:** Major and blocking for any title-concordant effectiveness claim.
- **Evidence anchor:** text: lines 31 and 233, “maintenance-domain transfer remains untested” and “does not establish effectiveness for operational maintenance reports.”
- **Required revision:** retain the exact title only if the Abstract, Introduction, Results, Discussion, and Conclusion consistently identify the study as a NERC technical-report benchmark and make maintenance an unvalidated intended application. Do not use “for maintenance reports” as an empirical population claim. A genuinely title-concordant claim requires a new license-cleared maintenance corpus and qualified human evaluation; that experiment cannot be manufactured from the current NERC split.
- **R3 acceptance test:** an automated claim scan finds no statement that the current experiment validates maintenance reports, and the title-risk boundary is visible in the first two Abstract sentences and final Conclusion paragraph. The limitations must state that title-concordant validation remains absent, not merely small.

### 2. Major: the registered bootstrap p-values are not generated under a null distribution

The runner resamples the observed paired deltas and computes `2*min(P(draw<=0), P(draw>=0))` (`run_test_v0_3_1.py`, lines 361--394). This bootstrap distribution is centered at the observed effect rather than at the null. Its tail proportion is useful as a descriptive bootstrap sign-tail, but it is not a calibrated hypothesis-test p-value. Holm adjustment cannot repair an invalid constituent p-value. Consequently, phrases such as “after Holm correction” in the Abstract and lines 187 and 223 overstate the inferential status.

I independently computed an exact two-sided report-level sign-flip sensitivity from the retained deltas; no model or test prediction was rerun. The unadjusted values were `0.43677`, `0.000305`, and `0.000122` at K=5 and `0.20068`, `0.006592`, and `0.009644` at K=10 for Full minus no-CF, Semantic-MMR, and TextRank, respectively. The qualitative finding remains the same after a six-test Holm correction: no evidence of a CF gain and positive baseline differences. These values are an unregistered sensitivity analysis, not a replacement confirmatory result.

- **Severity:** Major.
- **Evidence anchor:** equation/code: `run_test_v0_3_1.py`, lines 375--394; table: manuscript Table 3, lines 189--205.
- **Required revision:** preserve the registered percentile intervals and frozen machine values, but relabel the reported tail quantities as the registered bootstrap sign-tail estimator and remove calibrated-p-value language. Add a separately hash-bound post-run sensitivity artifact using a defensible paired null procedure (preferably exact sign-flip/permutation with an explicit symmetry/exchangeability assumption), apply Holm to its six values, and label it non-registered robustness evidence. If the authors decline this sensitivity analysis, report estimates and intervals descriptively and avoid significance claims.
- **R3 acceptance test:** the statistical section states the exact bootstrap construction and its limitation; Table 3 does not label the registered tail estimator simply as a conventional p-value; any added null-based analysis exactly regenerates from the immutable prediction ledger and is independently recomputed.

### 3. Major integrity issue: completed post-unblinding tuning is omitted and described in future tense

Line 239 says development-only calibration “may be explored.” It has already been completed after the formal result was known: 147 configurations, 12 leave-one-report-out folds, and 12/12 selection of a zero-CF winner. The best nonzero candidate (`CF=0.025`) remained below its no-CF comparison at both budgets. The calibration package properly prohibits access to the test JSONL and formal outputs, but the manuscript’s chronology is now inaccurate. Omitting it creates an avoidable selective-reporting concern, especially because the user explicitly considered tuning to make results look better.

- **Severity:** Major.
- **Evidence anchor:** dataset: `posthoc_dev_cf_calibration/DEV_ONLY_EXPLORATORY_REPORT.md`, Sections 1--6; text: manuscript line 239.
- **Required revision:** add a short, explicit post-unblinding exploratory-sensitivity subsection or supplementary note. State the chronology, 147 configurations, dev-only data hash, 12/12 zero-CF LOO outcome, absence of test access, and prohibition on replacing v0.3.1. Do not insert C046 or C055 into the primary table and do not rerun either on the revealed 15-report test set. Replace future tense with a factual record.
- **R3 acceptance test:** the formal v0.3.1 table and contrasts are unchanged; the exploration is visibly separated and labeled post hoc; its manifest shows `formal_output_accessed=false` and `test_input_accessed=false`; no abstract performance claim is based on C046/C055.

### 4. Major: the named causal/counterfactual contribution is identifiable but not validated as useful or causal

R2 fixes the R1 algebraic defect. Equations (1)--(2), the registered equal-degree counterexample, 29 tests, nonzero score differences in 9,774/19,008 comparisons, and different selections in 28/30 cells establish that the path-deletion channel is active and non-identical. This is a genuine software/mathematical contribution. However, the five roles and directed transitions are lexical heuristics without expert labels; deleting a sentence node is structural sensitivity, not an intervention on an event-generating process. Moreover, the Full model is below strict no-CF on development and both test budgets, and the post-hoc dev search selects zero CF in all 12 folds.

- **Severity:** Major for contribution framing; not a request to hide the negative result.
- **Evidence anchor:** equation: manuscript Equations (1)--(3), lines 85--106; table: Table 3, lines 196--201; dataset: `posthoc_dev_cf_calibration/artifacts/CALIBRATION_DECISION.json`.
- **Required revision:** define the contribution as an auditable typed-path structural diagnostic, not a demonstrated accuracy-enhancing counterfactual component. The Abstract and Conclusion already approach this boundary; tighten the Introduction contribution list and all uses of “causal” so that no reader can infer physical causal identification, causal-chain accuracy, or CF benefit. Add a concise operational definition of each lexical role and edge confidence, preferably in a supplementary table, so the graph is reproducible without reading code.
- **R3 acceptance test:** every causal/counterfactual claim is one of: proxy construction, mathematical non-identity, execution diagnostic, or explicitly negative ablation. No sentence attributes the Semantic-MMR/TextRank gains to the CF channel.

### 5. Major experimental-strength limitation: small selected sample, narrow metrics, and asymmetrically tuned comparator

The test unit is correctly the report, but `n=15` is small and selectively retained by summary-boundary/quality gates from 40 PDFs. The paper uses only one organization’s English public reports and two fixed sentence budgets. It measures ROUGE-1/2/L and lexical redundancy, not source faithfulness, role-chain coverage, factual sufficiency, expert preference, or unsafe omission. Semantic-MMR is a useful stronger baseline, but its lambda is fixed at 0.5 while C2GES receives a 144-configuration development search. This tuning asymmetry weakens a broad “superiority” narrative, even though the comparator is fully frozen and the paired differences are positive.

- **Severity:** Major for external validity and strength of comparative claims.
- **Evidence anchor:** text: lines 110--118 and 237--243; table: Tables 1--3.
- **Required revision:** present the baseline comparisons as results on the retained corrective split, not general method superiority. Report the inclusion/exclusion sampling frame and report genres in a supplementary table. Add report-level effect distributions (already shown in Figure 4) and sign counts to the results. A future new sealed holdout should tune all tunable baselines under the same development budget and add at least one competitive long-document extractive system. Qualified power-grid evaluation is required before claiming engineering usefulness; LLM ratings cannot be called expert validation.
- **R3 acceptance test:** the paper states the comparator-tuning asymmetry and n=15 precision limit; no population-wide or operational utility claim remains; every stronger-baseline or human-evaluation result, if added, has a new frozen protocol and unseen evaluation population.

## Claim--evidence audit

| Location | Claim | Audit finding | Required R3 action |
|---|---|---|---|
| Title; Abstract line 19 | C2GES is for power-grid maintenance reports | The corpus is public NERC reliability/disturbance/assessment reports; no maintenance records are evaluated | Keep the exact title only with an immediate explicit target-population disclaimer and no effectiveness claim; new maintenance evidence is required for title-concordant validation |
| Lines 33, 85--96 | CF is node-deletion typed-path utility distinct from degree | Supported mathematically and in code; the R1 identity defect is closed | Keep, but call it structural text-proxy sensitivity, not physical causal inference |
| Lines 63--71; Table 1 | Complete-PDF candidates and zero registered summary leakage | Independently rebuilt and audited: 40 PDFs, 27 retained, 12/15 split, 12,924 candidates, zero page/exact/50-character leakage | Supported within registered deterministic gates; retain the caveat that semantic cleanliness is not proven |
| Lines 75--77 | Role ties abstain and no silver labels enter v0.3 | Independent Stage-1 audit confirms 111 dev ties all abstain and zero silver-role evidence | Supported computationally; semantic validity of role labels remains untested |
| Lines 100--106 | Strict no-CF isolates only the CF channel | Config/code show only CF coefficient is set to zero with no renormalization | Supported as an implementation ablation; note that coefficient mass then sums to 0.85 and interacts with the fixed redundancy penalty |
| Lines 110--112 | 144-config dev choice and Semantic-MMR comparator | Development ledger supports grid 60; Semantic-MMR is complete but lambda 0.5 was not comparably tuned | Supported provenance, with comparator-strength/tuning asymmetry requiring disclosure |
| Lines 116--118 | Six-test Holm family and independent reproduction | Six records, hashes, row counts, and values independently match exactly | Mechanical reproducibility supported; conventional inferential interpretation of the bootstrap tail values is not |
| Lines 149--187; Tables 2--3 | Full exceeds Semantic-MMR/TextRank on this split | Mean deltas and percentile intervals match the frozen ledger; paired sign patterns are 14/1, 14/1 at K=5 and 11/4, 13/2 at K=10 | Retain as bounded descriptive evidence; repair the null-test terminology |
| Lines 185, 207, 217, 225, 247 | CF has no demonstrated ROUGE gain | Supported at dev and both test budgets; Full/no-CF signs are 7/7/1 and 6/8/1 | Strongly supported negative conclusion; retain prominently |
| Line 239 | Post-hoc calibration may be explored | Contradicted by completed 147-configuration dev-only analysis | Replace with accurate chronology and isolate from formal evidence |
| Lines 243, 255 | Future expert/LLM boundary | Correctly states that LLM judgment is not qualified expert validation | Retain; human validation remains absent, not “pending API authorization” |

## Experiment audit

### Required before R3 can be cleared

1. **Statistical sensitivity recomputation, not model rerun:** from the immutable 210-row ledger, produce and independently verify a paired null-based sensitivity analysis for the same six registered contrasts, or remove calibrated p-value language and retain descriptive intervals only.
2. **Post-unblinding chronology disclosure:** incorporate the completed 147-configuration development-only calibration as a clearly separated exploratory artifact. Do not alter the formal configuration, predictions, or primary results.
3. **Claim-strength revision:** constrain maintenance, causal, counterfactual, superiority, and engineering-usefulness language to what the 15-report corrective split supports.
4. **Sampling transparency:** provide the 40-report inventory with inclusion/exclusion reason, report genre/year, split, reference length, and candidate count, subject to rights-safe non-verbatim metadata.
5. **Metric transparency:** add report-level sign counts and clarify that ROUGE/redundancy do not measure causal-chain correctness, factuality, unsafe omission, or operator usefulness.

### Required for a future title-concordant confirmation, but not justifiable as a revision-time reuse of the current test

1. Acquire a new, never-inspected, license-cleared maintenance/work-order or inspection-report corpus with site/report grouping and an untouched external holdout.
2. Tune C2GES and tunable baselines under the same development budget, then freeze once before evaluation.
3. Add qualified, blinded power-grid reviewers using a frozen rubric for source faithfulness, cause/event/impact/mitigation coverage, usefulness, and unsafe omission; retain disagreements and report agreement/adjudication.
4. Include a competitive modern long-document extractive comparator and a length-matched extractive oracle or upper-bound diagnostic.
5. If a nonzero CF ranking term is tested again, require a positive, stable development gate before freezing and evaluate it once on the new holdout.

### Desirable analyses

- Report exploratory stratification by report genre, reference length, and candidate count, with no confirmatory language.
- Report correlations among Q, R, G, C, and P and the selected-sentence overlap between adjacent conditions.
- Add runtime/memory scaling by report length and path count.
- Provide a sensitivity analysis for word/token budgets in addition to K=5/10 sentence budgets on a future holdout.

### Unjustified reruns or reinterpretations

- Do not tune on the revealed 15 reports, rerun C046/C055 there, or choose a favorable CF weight from those outcomes.
- Do not replace the adverse formal CF ablation with a post-hoc development result.
- Do not call the current test fresh confirmatory, preregistered, or outcome-unseen.
- Do not use LLM/API ratings as expert labels or qualified adjudication.
- Do not infer maintenance safety, causal validity, or operator usefulness from ROUGE.

## Figure and table audit

### Figure 1: algorithm flow

The figure is legible and the bottom causal-boundary sentence is valuable. However, the lower arrows `Q -> R -> G -> C` visually imply a sequential computational dependence that the score does not have: Q, R, G, C, and P are score channels combined by Equation (3), and P is not shown. Revise the diagram so all five channels enter one weighted-combination node, then the redundancy-aware greedy selector. Show the strict no-CF switch at C and retain the proxy warning.

### Figure 2: dataset flow

The counts agree with the build manifest and Table 1. Add the 13-report exclusion breakdown or point to a supplementary inventory. The figure should continue to distinguish development selection from the one corrective test run.

### Figure 3: aggregate bars

The bar heights match `aggregate_metrics.json`, and Graph no-CF visibly exceeds Full. Because the data are paired and n=15, the bar figure should remain explicitly descriptive. Consider direct labels for values and avoid any visual significance notation.

### Figure 4: paired differences

This is the strongest result figure: it exposes all report-level directions and the adverse CF contrast. Replace anonymous “report index” with an accompanying rights-safe index-to-document metadata table. Add the 95% interval or sign count to each panel caption, while keeping the raw points visible.

### Tables 1--3

All checked values match the frozen JSON. Table 2’s caption says bold marks the observed maximum “within a budget and metric,” but redundancy is a lower-is-better metric and bold marks both Lead and Semantic-MMR at K=5. This is ambiguous: use a single defined rule, preferably bold only the best ROUGE values and mark minimum redundancy separately. Table 3 should replace `Holm p` with terminology that reflects the actual registered bootstrap sign-tail estimator unless a valid null-based sensitivity table is added. Every table should retain `n=15` in its caption.

## Reproducibility and ethics audit

### Verified strengths

- The v0.3.1 run is bound to one authorized physical attempt; 210/210 rows are complete and all 31 rehashed frozen files match.
- Independent post-run recomputation matches all 28 aggregate values and six contrast records with maximum absolute discrepancy zero.
- Development and test contain 12 and 15 disjoint reports, and the complete-PDF build has no fixed 80-sentence cap.
- Registered summary leakage checks, extraction-pollution checks, role-tie abstention, path work limits, and cache-equivalence tests pass.
- R1 v0.1/v0.2 results and failed/partial incidents remain preserved and excluded.
- The paper reports the unfavorable CF ablation in the Abstract, Results, Discussion, and Conclusion.

### Remaining reproducibility gaps

- The public GitHub repository is not yet asserted to reproduce this exact package; synchronization, immutable tag, and fresh-clone verification remain manual blockers.
- Source PDFs and verbatim derivatives are rights-restricted; editor/reviewer access must not be promised beyond actual third-party permissions.
- The paper needs a rights-safe report inventory and role/edge lexicon sufficient to reproduce the sampling and proxy graph without reverse-engineering code.
- The statistical p-value terminology must match the implemented estimator.
- Tool-by-tool AI provenance, corresponding-author email, author confirmation of CRediT/funder role/conflict statement, and permissions remain incomplete submission fields.

### Ethics boundary

No human-subject or animal experiment is reported, so the IRB/consent statements are appropriate for this computational study. The manuscript correctly states that AI tools were not qualified power-grid experts, annotators, adjudicators, or authors. This boundary must remain: an LLM-assisted annotation study can be described as machine evaluation, but cannot close the absent qualified-expert validation gate.

## Five questions for the authors

1. Will the authors accept that the exact maintenance-report title remains an aspirational application label rather than a tested population claim, and keep that limitation visible at every high-impact claim location?
2. What null hypothesis and exchangeability/symmetry assumptions do the authors intend the current bootstrap sign-tail estimator to test, given that its resampling distribution is centered at the observed empirical effect rather than the null?
3. Why was Semantic-MMR fixed at lambda 0.5 while C2GES received a 144-configuration development search, and how will the tuning-budget asymmetry be disclosed or corrected on a future unseen holdout?
4. Will the completed 147-configuration post-unblinding development analysis be formally registered in R3 as exploratory, including the 12/12 zero-CF LOO result, instead of remaining described in future tense?
5. Which concrete scientific contribution do the authors claim for the CF channel after both the formal test and post-hoc development search fail to show an accuracy gain: diagnostic interpretability, structural coverage, or something else that can be evaluated without implying causal validity?

## Round-3 acceptance checklist

- [ ] Exact R2 formal outputs, hashes, and adverse CF results remain unchanged.
- [ ] Bootstrap sign-tail values are not presented as conventional null-calibrated p-values; a defensible paired sensitivity recomputation is added or inferential language is removed.
- [ ] The already completed 147-configuration post-unblinding development analysis is disclosed, separated, and prohibited from replacing v0.3.1.
- [ ] Maintenance-domain effectiveness, physical causal identification, CF accuracy gain, and expert validation are not claimed.
- [ ] The contribution is framed as an auditable typed textual proxy/path-deletion mechanism with an honestly negative ranking ablation.
- [ ] Sampling inventory and inclusion/exclusion metadata are supplied without restricted verbatim text.
- [ ] Semantic-MMR tuning asymmetry, n=15, selected NERC population, fixed sentence budgets, and metric limitations are explicit.
- [ ] Figure 1 depicts five parallel score channels including P; Figure 4 remains paired and traceable; Table 3 terminology matches implementation.
- [ ] Repository tag/fresh-clone check, rights permissions, AI provenance, author confirmations, and corresponding email remain visible manual submission gates.
- [ ] Any future stronger experiment uses a newly frozen unseen holdout; the revealed 15-report test is never reused for method selection.

## Arithmetic recomputation note

The manuscript reports bootstrap intervals and resampling-tail quantities rather than t, z, F, chi-square, GRIM/GRIMMER, or df-to-N statistics covered by the bounded arithmetic procedures. I therefore did not invent an inapplicable arithmetic receipt. I independently reaggregated the report-level deltas and exact sign-flip sensitivities described above; those checks are reviewer calculations, not new registered evidence.
