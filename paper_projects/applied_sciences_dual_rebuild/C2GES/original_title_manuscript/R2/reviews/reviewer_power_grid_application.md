# C2GES Round 2 Independent Review: Power-Grid Application and Engineering Safety

## Review identity and recommendation

- Role: fresh independent power-system application and engineering-safety reviewer, Round 2.
- Frozen manuscript reviewed: `paper_applsci.tex` (SHA-256 `36FF05A08809870E3493BAAF7F5F51191CAB20C00C1F521BE6477A55DD6A2A2D`) and `build/paper_applsci.pdf` (SHA-256 `F57B0C5D965450748A8CDE63D0442F3A6FBD08D872CEA1CC54C030F2DDA04CD8`).
- Evidence reviewed: the v0.3.1 freeze and authorization, complete-PDF build08 manifest and extraction audit, rights ledger, development decision, prediction and aggregate ledgers, independent pre-test and post-run audits, figures, R2 assembly audit, and the development-only post-unblinding CF calibration report.
- Recommendation: **major revision**.
- Confidence: **5/5** for the population, operational-scope, domain-validity, safety, and rights findings; **4/5** for the likely consequences of the reference-summary design because no qualified-user study is available.

R2 is substantially more credible than R1. It openly withdraws the leaked and algebraically defective earlier results, evaluates complete PDFs, retains the adverse counterfactual ablation, and repeatedly distinguishes textual proxy structure from grid physics. Those are material strengths. The paper is nevertheless not ready for submission under its exact title. The observed population is a heterogeneous set of public NERC reliability and disturbance publications, not maintenance reports, and neither the role/edge taxonomy nor the summaries have been evaluated by qualified power-grid personnel. The current evidence supports a reproducible benchmark of source-text overlap on retained NERC reports. It does not establish maintenance-workflow value, causal-chain correctness, or safe use in power-grid maintenance.

## Five most serious issues, ordered by decision impact

### 1. The title names a population that the study did not evaluate

The title states “for Power Grid Maintenance Reports,” but the corpus consists of public NERC disturbance reports, event analyses, reliability assessments, recommendation documents, and performance reviews. The manuscript correctly concedes that it contains no utility work orders or inspection logs (Abstract and Section 1, lines 19 and 31) and that operational-maintenance effectiveness is untested (Section 5.3, line 233). Disclosure is necessary, but it does not supply title-concordant evidence. NERC publications differ from maintenance records in authorship, audience, approval process, asset granularity, temporal density, vocabulary, confidentiality, and whether an Executive Summary exists.

- **Severity:** Major; blocking for any claim that current results validate the title population.
- **Evidence anchor:** text: `paper_applsci.tex`, line 31, “it contains maintenance-relevant lessons and corrective actions but not utility work orders or inspection logs.”
- **Required revision:** If the exact title must remain, introduce a formal title-scope convention in the Abstract and Introduction: “maintenance” is the intended downstream use, while the measured population is a NERC technical-report proxy corpus. Use “NERC technical reports” for every empirical result. Do not call the 27 reports maintenance reports, a maintenance benchmark, or evidence of operational deployment. A title-concordant effectiveness claim requires a new, license-cleared corpus of actual work orders, inspection reports, or maintenance narratives with a genuinely unseen evaluation split.
- **R3 acceptance test:** A case-insensitive claim scan plus manual reading of the Title, Abstract, Featured Application, Introduction, Results, Discussion, and Conclusion finds no sentence that treats the current corpus as maintenance records or generalizes current ROUGE results to maintenance performance. The first Abstract paragraph and final Conclusion paragraph retain an explicit population disclaimer.

### 2. The causal-role and counterfactual vocabulary lacks power-system semantic validation

The algorithm assigns root-cause, trigger, propagation/response, impact, and mitigation roles from lexical evidence, permits fixed stage-monotone transitions within 12 sentence positions, and interprets node deletion as path-utility sensitivity (Sections 3.3--3.4, lines 75--96). This is computationally well specified, but it has not been shown that the roles match NERC event-analysis practice, that the direction of a rhetorical transition matches the direction of a physical or operational dependency, or that a 12-sentence window preserves a true event chain. Power-system reports commonly distinguish initiating event, contributing cause, protection/control response, cascading sequence, consequence, restoration, recommendation, responsible entity, and implementation status. Collapsing these into five lexical stages may confound cause with observation, response with propagation, and mitigation with a recommendation that has not been implemented.

The manuscript appropriately says the graph is a textual proxy, and the negative ablation makes the limitation empirically important: Full is below strict no-CF at both development and test budgets, and all 12 development leave-one-report-out folds selected a zero-CF winner in the later exploratory calibration. Mathematical non-identity is therefore a valid algorithm property, not evidence of domain-valid causal reasoning or useful counterfactual inference.

- **Severity:** Major for the named contribution and domain interpretation.
- **Evidence anchor:** text: `paper_applsci.tex`, lines 75--77 and 229, “Direction and path score are reproducible hypotheses, not validated relations in grid physics.”
- **Required revision:** Add a rights-safe supplementary taxonomy table defining every role, lexical evidence family, allowed transition, ambiguity rule, and a positive and negative paraphrased example. Label the output consistently as a “typed event-narrative proxy graph” or equivalent. Reserve “causal” and “counterfactual” for the exact textual-proxy and node-deletion definitions, never for physical mechanisms, potential outcomes, root-cause identification, or event prevention. Incorporate the completed development-only calibration chronology and its zero-CF result rather than describing it as future work.
- **R3 acceptance test:** Every causal/counterfactual statement falls into one of four supported categories: proxy definition, mathematical non-identity, execution diagnostic, or explicitly adverse ablation. A supplementary taxonomy makes the implemented stages reproducible without source-code archaeology. No result attributes the advantages over Semantic-MMR or TextRank to the counterfactual term.

### 3. Official Executive Summaries are not a validated engineering gold standard

The official Executive Summary is used as the sole reference, while the system outputs five or ten body sentences (Section 3.1, line 57). Across the retained reports, the extraction audit records reference lengths from 256 to 3578 words (median 1106), whereas each system output has a fixed sentence count. The summaries are authoritative editorial products, but they are not independent expert annotations of the best extractive sentences. They may paraphrase, synthesize tables, include recommendations, or emphasize regulatory and organizational context absent from any one body sentence. Consequently, low ROUGE can reflect the extractive/abstractive and length mismatch, and higher ROUGE cannot establish engineering completeness, correctness, or safe omission behavior.

- **Severity:** Major for interpretation of accuracy and practical value.
- **Evidence anchor:** dataset: `diagnostic_build_08/per_report_extraction_audit.jsonl` — 27 retained references, 256--3578 reference words (median 1106); text: `paper_applsci.tex`, line 57.
- **Required revision:** Rename the measured endpoint precisely as lexical overlap with each document’s official Executive Summary. Add a rights-safe per-report metadata table containing report code, genre, split, declared pages, reference pages/word count, candidate count, and inclusion status. Explain that the reference was not designed as an extractive gold summary. Do not use “accuracy,” “faithfulness,” “coverage,” or “quality” without a separate validated endpoint. A future human study should judge source faithfulness, event-chain coverage, action/recommendation coverage, and unsafe omissions independently of ROUGE.
- **R3 acceptance test:** Abstract, Results, Discussion, figure captions, and Conclusion describe ROUGE as Executive-Summary lexical overlap, not engineering correctness. The metadata table exposes reference-length and genre heterogeneity, and the limitations explain the extractive-reference mismatch.

### 4. Structural eligibility creates a narrow, selected, and heterogeneous sample

Only 27 of 40 PDFs were retained; 11 were excluded because an Executive Summary heading was not detected and two because a reliable summary endpoint was unavailable. The exclusions include operationally important cold-weather, blackout, outage, and storm reports. Thus eligibility depends on document layout and summary structure, not a power-system sampling frame. The retained set combines individual disturbances, broad annual reliability assessments, recommendations, and EMS-related assessments. All documents are English-language public reports associated with NERC or related North American bodies. The 15-report test split is therefore too small and structurally selected to represent maintenance reporting across utilities, asset classes, regions, languages, or operating organizations.

The series-level hash split is preferable to naive random sentence splitting, but the manuscript does not show genre/year/asset balance between the 12-report development and 15-report test partitions. Similar series and topics also remain a legitimate dependence concern even when explicit series identifiers do not cross splits.

- **Severity:** Major for external validity and comparative generalization.
- **Evidence anchor:** dataset: `diagnostic_build_08/per_report_extraction_audit.jsonl` — 27 included, 11 `missing_executive_summary_heading`, and 2 `missing_executive_summary_end`; table: manuscript Table 1, 27/13 and 12/15.
- **Required revision:** Add the full 40-document, rights-safe inventory and an exclusion-flow breakdown. Report genre, year where verified, topic/asset family, series group, split, and exclusion reason. State that this is a deterministic convenience/eligibility sample rather than a representative sample. Add descriptive, clearly exploratory results by broad document genre only if group sizes and all cells are shown; do not create a favorable subgroup claim from n=15.
- **R3 acceptance test:** Figure 1 branches 40 PDFs into 27 retained and 13 excluded instead of visually placing exclusion as an intermediate step. A supplementary inventory accounts for all 40 records, and every comparative statement is bounded to the retained corrective split.

### 5. The Featured Application is not yet supported by a qualified-user or safety evaluation

The Featured Application proposes source-traceable engineering-report navigation and correctly denies autonomous root-cause analysis (line 21). However, no qualified operator, protection engineer, maintenance engineer, reliability analyst, or report author assessed the extracted summaries. The study does not measure whether selected sentences preserve units, equipment identity, temporal order, negation, uncertainty, recommendation status, or the distinction between observed cause and suspected cause. It also does not test whether a K=5 or K=10 extract omits a safety-critical qualifier or recommendation. Source linking is useful, but traceability alone does not make an incomplete extract operationally safe.

- **Severity:** Major for the claimed application and engineering value.
- **Evidence anchor:** absence: evaluation protocol — expected qualified power-grid assessment of usefulness and unsafe omissions; checked Sections 3.1--3.7, 4.1--4.4, 5.3--5.5, Supplementary Materials, and the v0.3.1 evidence package.
- **Required revision:** Reframe the Featured Application as a prototype navigation aid requiring review of the linked source passage and surrounding context. Add an explicit “not for operational decision-making, protection setting, dispatch, compliance determination, or autonomous root-cause analysis” boundary. Preserve qualified-human validation as an unresolved future requirement; an LLM API may assist annotation preparation but cannot be represented as a qualified expert or adjudicator.
- **R3 acceptance test:** The Featured Application and Discussion identify the user, permitted task, mandatory source review, prohibited decisions, and failure modes. No “deployment,” “decision support,” “safety,” or “engineering usefulness” claim is made from ROUGE alone. Any expert result added later includes real qualifications, blinded protocol, disagreement retention, adjudication, and inter-rater agreement.

## Five questions for the authors

1. What exact operational document classes do the authors intend “power grid maintenance reports” to denote: work orders, inspection records, defect reports, outage/event analyses, reliability assessments, or a specified subset? Which of those classes is represented by each of the 27 retained documents?
2. Who defined the five role categories and allowed transitions, and against which NERC or utility event-analysis/maintenance taxonomy were they checked? Were any ambiguous, negated, hypothetical, or recommendation-only sentences examined by a qualified engineer?
3. In the proposed navigation workflow, what does the user receive besides the selected sentence: report identifier, page, surrounding paragraph, table/figure link, confidence, and an explicit omission warning? How is an unsafe or misleading extract escalated?
4. Why are K=5 and K=10 operationally meaningful across reports whose official summaries range from 256 to 3578 words and whose bodies range from 51 to 1898 candidates? Would a word/token budget or reference-length-normalized budget better reflect use?
5. What documented permission or terms permit local computational use and editor/reviewer access for each source PDF and verbatim derivative, and who will make the required institutional/legal determination before submission?

## Claim--evidence audit

| Location | Manuscript claim | Domain judgment | Required R3 action |
|---|---|---|---|
| Title; Abstract line 19 | C2GES is “for Power Grid Maintenance Reports” | Not demonstrated by the NERC reliability/disturbance/assessment sample | Retain the exact title only with an immediate proxy-population disclaimer and no title-concordant effectiveness claim |
| Featured Application, line 21 | Source-traceable extract for engineering-report navigation | Source identifiers/pages are mechanically traceable; user usefulness and safe omission are untested | Define the prototype workflow and prohibit consequential use without source-linked qualified review |
| Introduction, line 31 | NERC reports contain maintenance-relevant lessons and corrective actions | Plausible and often true for event reports, but not quantified or mapped to the 27 records | Provide genre/document mapping; describe “maintenance-relevant” as rationale, not validation |
| Introduction, lines 33--35 | Typed path deletion is distinct from degree and transparently reports adverse evidence | Supported by equations, tests, and frozen adverse ablation | Retain as a methodological/auditability contribution; do not imply domain causal validity |
| Related Work, lines 47 and 51 | Directed edges are textual proxies and maintenance-workflow utility is not validated | Appropriately bounded | Retain and make terminology consistent in title-facing sections and captions |
| Methods, lines 57 and 71 | Executive Summary is the reference; registered leakage modes are zero | Mechanical boundary/exact/substring checks pass; semantic independence and reference suitability remain unvalidated | Call it an official-reference overlap task and disclose reference heterogeneity |
| Methods, lines 75--96 | Five roles and stage-monotone paths encode a causal/event narrative | Computational definition is supported; power-system semantic validity is absent | Add taxonomy, lexical rules, ambiguity examples, and a strict proxy-only interpretation |
| Methods, lines 110--112 | One of 144 configurations is selected and seven baselines share the candidate space | Provenance is supported; the selected Full configuration was already worse than no-CF on development | Keep adverse development result and report the completed post-unblinding calibration accurately |
| Tables 2--3; lines 149 and 185 | Full exceeds Semantic-MMR/TextRank but not strict no-CF on 15 reports | Numeric statement is supported for this retained split | Use “on the retained NERC corrective split”; do not claim general superiority or maintenance benefit |
| Discussion, lines 225 and 229 | CF has no demonstrated accuracy value and no physical causal effect is identified | Strong and appropriately conservative | Retain prominently in Abstract, Discussion, and Conclusion |
| Discussion, line 233 | Current evidence supports NERC technical-report summarization and a proposed maintenance use case | First clause is supported only as Executive-Summary overlap; second is a proposal, not evaluation | Replace “supports summarization” with the exact endpoint and keep the use case explicitly unvalidated |
| Limitations/Future Validation, lines 237--243 | Human expertise, safety endpoints, and title-concordant corpus are absent | Correct and important | Convert these into explicit submission/claim gates; do not let LLM review close them |
| Data Availability, lines 249 and 254 | Verification materials may be requested subject to permission | Rights ledger records `rights_holder=not_verified`, no terms locator, and redistribution pending human review for all 40 PDFs | Resolve rights/terms per file or restrict the package to hashes and non-verbatim metadata; do not promise access that cannot lawfully be supplied |

## Experiment audit

### Required for R3 using existing immutable evidence

1. **Do not rerun or tune on the revealed 15 reports.** Preserve the v0.3.1 predictions and adverse CF contrast. Record the completed 147-configuration development-only calibration as post-unblinding exploratory evidence, including the 12/12 zero-CF leave-one-out result and the prohibition on substituting it for the frozen model.
2. **Add a rights-safe 40-report inventory.** Include title or stable code, document genre, verified year, source organization, page count, reference length, candidate count, series group, split, inclusion/exclusion reason, and permission status.
3. **Audit the claimed role semantics without fabricating expert labels.** At minimum, publish the deterministic dictionary/transition taxonomy and a blinded-to-outcome, rights-safe error taxonomy of ambiguous/negated/hypothetical/recommendation sentences. If no real qualified review is available, label semantic validity as absent.
4. **Report endpoint limitations quantitatively.** Show reference-length and candidate-count distributions and state that K=5/10 are research budgets, not validated operational limits. Add report-level direction/sign counts already derivable from the immutable ledger.
5. **Repair claim scope.** Treat all current results as descriptive Executive-Summary-overlap results on the retained NERC corrective split.

### Required for future title-concordant validation

1. Build a new, genuinely unseen, license-cleared multi-utility or multi-site corpus of actual maintenance/work-order/inspection narratives, split by site or report family before any outcome access.
2. Freeze a task definition that identifies target users and distinguishes event review, maintenance planning, defect triage, compliance, and root-cause analysis.
3. Recruit qualified power-grid personnel with recorded expertise. Use independent blinded ratings for source faithfulness, equipment/action coverage, temporal and causal-chain coherence, engineering usefulness, and unsafe omission; retain disagreements, predefine adjudication, and report agreement.
4. Compare C2GES and tunable baselines under equal development budgets. Include at least one competitive long-document extractor and a simple source-position baseline.
5. Evaluate abstention and failure behavior, including negation, uncertain/suspected causes, conflicting evidence, table-dependent facts, units, asset identifiers, and recommendations not yet implemented.

### Desirable analyses

- Rights-safe qualitative error cases stratified by disturbance, annual assessment, recommendation, and EMS/cyber-related documents.
- Coverage of each role and complete role paths among selected sentences, explicitly described as proxy diagnostics until expert-validated.
- Runtime and memory by candidate count and path count, relevant to long operational reports.
- Word/token-budget sensitivity and report-length-normalized budgets on a future holdout.
- A user-interface mock-up showing source page, surrounding context, uncertainty, and omission warning; this is design evidence, not a usability result.

### Unjustified reruns or interpretations

- No hyperparameter search, model selection, or favorable subgroup selection on the revealed 15-report test set.
- No replacement of Full C2GES by strict no-CF while retaining the same algorithmic performance narrative without a new sealed evaluation.
- No assertion that lexical roles reveal physical causes or that deleting a sentence simulates a grid intervention.
- No inference of safety, operator usefulness, maintenance value, or factual completeness from ROUGE/redundancy.
- No use of an LLM/API panel as a substitute for qualified power-grid experts or genuine human adjudication.

## Figure and table audit

### Figure 1: dataset construction

The displayed counts are consistent with the manifest, but the visual flow `40 complete PDFs -> 13 excluded -> 27 retained` is logically wrong: the excluded reports are drawn as an intermediate population leading to retained reports. Branch the 40 PDFs into 27 retained and 13 excluded, show the exclusion breakdown (11 missing summary heading; 2 missing summary endpoint), and then branch the retained set into development and test. Add “NERC public technical reports; not maintenance work orders” inside the figure or caption.

### Figure 2: algorithm flow

The proxy warning is valuable and should remain. The lower arrows visually imply a sequential chain `Q -> R -> G -> C`, although Equation (3) combines Q, R, G, C, and P as score channels; P is absent. Redraw the five channels as parallel inputs to a weighted-combination node, show the strict no-CF switch on C, and then show redundancy-aware greedy selection. Also make clear that roles feed graph construction while Q and P need not. This correction is important because the current drawing can be mistaken for a physical causal pipeline.

### Figure 3: aggregate ROUGE-L

The graph-no-CF bars correctly appear above Full at both budgets. Retain this visible negative result. Add `n=15`, label the endpoint as overlap with official Executive Summaries, and avoid any wording that implies operational superiority. Direct value labels would improve auditability.

### Figure 4: paired differences

This is the most informative result figure because it shows heterogeneity and the adverse CF contrast. Replace anonymous indices with rights-safe report codes and provide an adjacent mapping to genre/year/length. Add sign counts and confidence intervals to the caption. Do not add a favorable subgroup overlay selected after inspection.

### Tables 1--3 and required supplementary table

Table 1 needs the 13-report exclusion breakdown, report genres, and reference-length range. Table 2 should say `n=15 selected NERC reports` and define redundancy direction; bolding should not suggest that the Full model is the best condition. Table 3 should retain the negative Full-minus-no-CF estimates. A new supplementary inventory should account for all 40 PDFs without redistributing protected text.

## Reproducibility, rights, ethics, and engineering-safety audit

### Verified strengths

- The independent post-run audit validates one complete 210-row run, 31/31 current rehashes, all aggregate values, and all six contrast records.
- Development and test contain disjoint report series under the registered grouping, and no fixed 80-sentence cap remains.
- Page-boundary, exact-match, 50-character-substring, and extraction-pollution gates report zero registered leakage; the paper correctly avoids claiming universal semantic cleanliness.
- Selected sentences retain source identifiers and pages, creating a useful traceability substrate.
- The adverse CF result is visible in the Abstract, Results, Discussion, and Conclusion.
- The manuscript explicitly denies physical causal identification, autonomous root-cause analysis, and LLM-as-expert substitution.

### Remaining reproducibility and rights defects

- Every rights-ledger row records `rights_holder=not_verified`, `license_or_terms_locator=not_recorded_in_source_manifest`, and PDF/verbatim redistribution as not authorized pending human review. The R2 package therefore cannot promise the underlying PDFs or verbatim dataset to editors or reviewers without an actual terms/permission determination.
- Source-manifest access dates are not recorded. Add verified access dates and stable source locators without altering frozen experimental content.
- The public GitHub repository is not yet asserted to match the manuscript-bound package. A repository owner must synchronize, tag, archive, and verify a fresh clone before submission.
- The candidate extractor is deterministic, but the source PDFs and verbatim candidate/reference files are restricted. A clean reproducibility path should separate redistributable code, hashes, synthetic tests, and non-verbatim metadata from controlled source-dependent artifacts.

### Ethics and safety boundaries

No human-subject experiment is reported, so the current IRB “not applicable” statement is consistent with the machine-only study. If qualified personnel are later recruited for scientific evaluation, the authors/institution must determine whether ethics or organizational review is required and document consent, confidentiality, data access, and retention. Reviewer agents or LLM APIs cannot fabricate qualifications, approvals, consent, adjudication, or inter-rater agreement.

The system must not be described as safe for consequential use merely because it is extractive. Extractive summaries can omit qualifiers, select stale recommendations, detach values from units or tables, or preserve a sentence whose meaning depends on surrounding context. The submission should explicitly require inspection of the linked source and prohibit autonomous maintenance, protection, dispatch, compliance, or root-cause decisions.

### Manual blockers no AI agent can close

1. A genuine qualified power-grid review with real identities/qualifications, consent where applicable, independent ratings, disagreement records, and adjudication.
2. File-by-file legal/institutional determination of the NERC and related report terms, including whether editor/reviewer access and verbatim derivatives may be supplied.
3. Yang Yong’s corresponding-author email and author verification of names, affiliations, contribution statement, funding/funder role, conflict statement, and AI-use disclosure.
4. Repository-owner synchronization, immutable release/tag, archive decision, and fresh-clone verification.
5. A new untouched title-concordant dataset if the authors wish to claim maintenance-report effectiveness rather than an intended transfer use.

## Concrete R3 acceptance conditions

R3 may advance to the final review round only if all of the following are satisfied:

1. **Population/title boundary:** the exact title is retained only alongside an immediate, repeated statement that the measured population is selected public NERC technical reports and maintenance transfer is untested.
2. **Causal-language boundary:** every causal/counterfactual claim is restricted to typed textual proxies and node-deletion structural sensitivity; no physical mechanism, causal identification, or counterfactual accuracy is implied.
3. **Negative evidence:** the formal v0.3.1 Full-minus-no-CF results remain unchanged and prominent, and the completed post-unblinding development-only calibration is accurately disclosed with its 12/12 zero-CF outcome.
4. **Reference/metric boundary:** ROUGE is described as overlap with official Executive Summaries, not expert accuracy, factual sufficiency, engineering usefulness, or safety.
5. **Sampling transparency:** a rights-safe inventory accounts for all 40 PDFs, all 13 exclusions, report genres/years/series, split, lengths, and permission status; the sample is called selected rather than representative.
6. **Engineering-safety boundary:** the Featured Application identifies source review and qualified human judgment as mandatory and explicitly prohibits consequential autonomous use.
7. **Figures/tables:** the dataset flow branches correctly, the algorithm figure displays Q/R/G/C/P channels without a false sequential implication, and captions show `n=15`, the NERC population, and the adverse CF result.
8. **Reproducibility and rights:** code, non-verbatim metadata, hashes, and controlled artifacts are separated; repository and rights actions remain visibly unresolved unless real records close them.
9. **Human-evidence integrity:** no LLM, reviewer agent, or API output is labeled qualified expert annotation or human adjudication.
10. **Submission status:** the manuscript remains “not ready for portal upload” while correspondence, author/funder confirmation, rights, repository release, and any claimed human validation remain incomplete.

With these revisions, the paper could be a transparent methodological study of deterministic event-narrative summarization on selected NERC reports while preserving the original title as an explicitly aspirational application target. Without them, the title and causal terminology would invite a stronger engineering interpretation than the evidence supports.
