# Round 1 Independent Review — Methods and Statistics

## Reviewer scope and independence

Role: methods and statistics reviewer for the Round 1 frozen manuscript only. I reviewed `paper_applsci.tex`, `build/paper_applsci.pdf`, `R1_ASSEMBLY_AUDIT.md`, and the cited local ledgers, manifests, reports, tables, implementation, and tests. I did not edit the manuscript or code and did not communicate with the other reviewers.

## Recommendation

**Major revision.** The paper is unusually explicit about negative results and about the retrospective replay not being an accuracy experiment. The reported point estimates that I sampled are traceable and numerically consistent. However, the current evidence does not test the framework named in the title: the five-role coordination core has no prospectively frozen, budget-matched execution-accuracy experiment, and its counterfactual channel has zero reference-free evidence in the only replay. In addition, “robust” is neither operationalized as a primary system-level estimand nor established by the inherited single-generation stress study. These are blocking scientific-positioning defects, not copy-editing issues.

## Five most serious issues

### 1. The main experimental unit never receives the title method — **blocking**

The title and abstract introduce a “Robust Multi-Agent Framework,” but the 1440 GridDB predictions and 5000 BIRD calls evaluate single-generation prompt procedures, not the five-role coordinator (`paper_applsci.tex`, lines 15, 22, 36, 140, 150). The 700-call component study tests presented values and a deterministic selector, while the replay only asks whether inherited candidates can populate interfaces. The authors themselves correctly acknowledge that the prospective coordination effect is unanswered (lines 38, 156, 254, 274, 278, 288). Consequently, the completed experiments cannot estimate the accuracy, abstention, cost, or robustness of MA-SQLGrid as an integrated system.

**Required resolution:** execute a hash-frozen prospective comparison in which the exact submitted coordinator is an experimental condition, or weaken the title and all system-level claims. If the original title must remain, this experiment is mandatory. The primary contrast must hold model snapshot, questions, decoding, candidate budget, physical calls or a predeclared resource budget, schema evidence, execution boundary, and evaluator constant.

**Acceptance test:** a new immutable run contains per-item blackboard digests sealed before gold loading, complete all-attempt ledgers, the direct/budget-matched coordinator conditions, predeclared primary and safety endpoints, and an independent recomputation that reproduces every manuscript number.

### 2. “Robust” is not operationalized, and the implemented counterfactual/safety logic is not yet robust — **blocking**

The 15-state result is inherited from predictions generated outside MA-SQLGrid and uses gold-relative equivalence; those labels are explicitly unavailable to the coordinator (`paper_applsci.tex`, lines 109, 148, 210, 274). The replay therefore has **0** questions with reference-free counterfactual evidence (`coverage_summary.json`). Moreover, the implemented `Adjudicator` ranks counterfactual pass rate before evaluated-state coverage and never uses `coverage_complete` (`ma_sqlgrid_agents.py`, lines 350–357 and 402–409). A candidate passing 1/1 state can outrank one passing 10/11 states, although the expected suite is incomplete. The validator is a lexical filter plus a caller-supplied executor (`ma_sqlgrid_agents.py`, lines 274–325), not by itself an SQLite authorizer, immutable/read-only connection, timeout, or resource-limit boundary. These details are acceptable for a skeleton, but not evidence of system robustness.

**Required resolution:** define robustness before running as named perturbation families and estimands (e.g., schema renaming/extension, value and ordering perturbations, empty/tied results, state invariants, malformed outputs, timeout/resource faults, abstention under missing evidence). Enforce a predeclared minimum/complete state-coverage rule or provide a justified missingness-aware score; add adversarial safety tests and executor-level read-only/timeout controls. Evaluate the integrated coordinator rather than reusing gold-relative labels at selection time.

**Acceptance test:** the protocol specifies the exact robustness denominator and failure treatment; all expected states are either evaluated or cause fail-closed abstention; adversarial tests cover multi-statements, comments, CTE writes, metadata access policy, timeouts, and executor exceptions; the Results report success and abstention jointly.

### 3. GridDB has development leakage and weak independent units — **major**

The 180-item evaluation partition was visible during development (`paper_applsci.tex`, lines 86 and 270). The sole domain database is synthetic, contains only 98 rows, and maps to 70 normalized-gold-SQL clusters, 58 of which are singletons. The cluster map is a dependence proxy, not an independently designed sampling unit. Therefore, the finite-set effects can be overfit through prompt, normalization, schema packaging, hint rules, selector weights, or manuscript-era analysis choices. This limits both causal attribution and external validity even when all 180 rows are retained.

**Required resolution:** keep these results as development/case-study evidence and add an untouched evaluation set or a transparent nested development/test design. For power-grid claims, use an independently held power-grid schema/question set whose references receive qualified review, or explicitly frame the domain contribution as software architecture rather than demonstrated domain performance. Pre-freeze grouping before outcome access and report sensitivity to question-level, structural-cluster, and database-level units where meaningful.

**Acceptance test:** the manuscript has a study-by-study chronology table (data visibility, intervention freeze, analysis freeze, outcome access, status); no visible-development result is called confirmatory or generalized to production; a new held-out set has an immutable split/hash and no authoring-time access.

### 4. BIRD comparisons are not resource-matched and do not benchmark MA-SQLGrid — **major**

The BIRD methods use one call for B0/B1/B2 but two mandatory calls for B3 (`BASELINE_PROTOCOL_FREEZE.md`, lines 11–14, 22; `BASELINE_PROTOCOL_FREEZE_v1_1.json`, method-call fields). The manuscript states only that each method has a fixed call pattern (line 150), which can be misread as a matched comparison. The comparison is valid as a comparison of four frozen workflows under a common maximum token envelope, but not as a clean causal estimate of repair or agentic coordination at equal physical calls. It also provides no MA-SQLGrid condition and no same-run strong learned Text-to-SQL baseline.

**Required resolution:** report calls, input/output tokens, latency status, failures, and final-prediction denominators for every method; label the existing BIRD contrast as workflow efficacy with unequal call counts. In the new experiment, include a call-matched multi-sample/control condition so gains cannot be attributed to additional samples or calls. Do not compare literature scores as if protocol-compatible.

**Acceptance test:** a resource table shows `n`, correct, accuracy, interval, calls/item, total calls, token totals, latency status, and failures for all eight model-method cells; the primary system contrast is budget matched and its estimand is stated explicitly.

### 5. Statistical reporting and adjudicator sensitivity are incomplete — **major**

Table 1 reports only proportions, although the underlying `V2_REANALYSIS.json` contains counts and composition-sensitivity intervals. BIRD results are prose-only and omit the full eight-cell table and uncertainty intervals even though `method_summary.csv` contains them. The multi-state section reports only a range and adjusted values, not all cell estimates/intervals. The fixed adjudicator weights (40/40/10/5/up to 5) have no derivation or sensitivity analysis (`paper_applsci.tex`, line 113; `ma_sqlgrid_agents.py`, lines 365–373). Among eligible candidates, the 80 safety/execution points are constant, so the actual choice is driven by shape/order/value signals and tie rules; these can be correlated with prompt-provided targets and are not semantic correctness measures.

The v3 execution/structural multiplicity hierarchy is explicitly a **post-review reanalysis**, not preregistration (`canonical_v3_inference_hierarchy/V3_INFERENCE_REPORT.md`). The manuscript should not let “registered” imply that this hierarchy was fixed before outcome access (lines 142, 148, 210). No reported *t*, *F*, chi-square, or degrees-of-freedom statistic supports a bounded arithmetic recomputation; sampled adjusted *p* values match the retained tables, but their chronology/status must be visible.

**Required resolution:** add complete count/denominator/interval tables; label intervals consistently as finite-corpus composition sensitivity; distinguish prospective freeze, post-review analysis freeze, and retrospective diagnostic; pre-register the new study’s primary family; and run adjudicator-weight/tie-rule/coverage-threshold sensitivity without selecting the best rule on the test outcomes.

**Acceptance test:** every quantitative statement maps to a row in an evidence ledger; every table shows its denominator and uncertainty/status; the chronology table prevents post hoc analyses from being described as preregistered; the selected adjudicator rule is frozen using development data only and survives a disclosed sensitivity grid.

## Claim–evidence audit

| Manuscript claim/location | Evidence checked | Verdict | Required action |
|---|---|---|---|
| 1440 predictions; 180 per GridDB cell (lines 22, 40, 138, 162–175) | `canonical_v2_reanalysis/V2_REANALYSIS.json`, `cell_summary` | **Supported.** Sampled counts are Qwen 76/129/78/108 and Granite 77/100/74/108; rates equal the manuscript values. | Add counts and composition-sensitivity intervals to Table 1. |
| Zero of nine execution effects survives Holm; selected raw/adjusted values (lines 191–193) | `canonical_v3_inference_hierarchy/V3_INFERENCE_REPORT.md` and `V3_INFERENCE_HIERARCHY.json` | **Numerically supported, status-sensitive.** The report says the hierarchy is post-review reanalysis, not preregistration. | State the chronology at first mention; reserve “preregistered” for genuinely pre-outcome plans. |
| Qwen E1 +0.1059, interval [0.0282, 0.2013], adjusted *p*=0.0310; Granite zero (lines 22, 197) | `component_canonical_release/table_primary_effects.csv` and `INDEPENDENT_AUDIT.md` | **Supported.** 170 questions/61 clusters; Qwen adjusted value is 0.0310397. | Report the denominator/clusters in the abstract or table and retain “composition-sensitivity,” not population CI. |
| Selector changes/rescues/harms and E2 effects (line 199) | `component_canonical_release/table_selection_descriptives.csv` and `table_primary_effects.csv` | **Supported.** Qwen 24/8/1 and Granite 36/10/0; neither passes the full rule. | Keep descriptive; add full table or supplement pointer. |
| 25,920 state rows, 1440/1440 T0 consistency, rates 0.6212–0.8182, all adjusted values 1 (lines 90, 210) | `semantic_reliability_experiment/formal_v5_analysis/ANALYSIS_SUMMARY.json`, `POST_SCORE_INDEPENDENT_AUDIT_A.md` | **Supported as a constructed-state diagnostic.** It does not test the submitted coordinator and is not human-certified robustness. | Present all cell rates and clarify that gold-relative state agreement cannot enter online adjudication. |
| 5000 BIRD calls, 4000 predictions, Qwen 0.394/0.378/0.348/0.302, Granite best 0.236, adjusted contrasts (lines 22, 88, 150, 221) | Raw `final_scores.jsonl` files, `method_summary.csv`, `cluster_contrasts_holm.csv`, post-run audit | **Supported.** Independent recount gives 2000 rows/backbone and exactly 500 rows/method; correct counts are 189/151/197/174 and 102/105/101/118. Adjusted values round to 0.0430 and 0.0117. | Disclose unequal calls/item and show all cells, counts, and intervals in a table. |
| Replay 180/173/172/7/1/0 and candidate distribution (lines 225–246) | `original_title_rebuild/retrospective_diagnostic/coverage_summary.json` and 180-row JSONL | **Supported as coverage only.** Status counts sum to 180 and distribution counts sum to 180. | Retain the current prohibition on accuracy or gain claims. |
| “robust multi-agent framework” (title, lines 15, 22, 284–288) | Coordination code/tests plus all experiments | **Not empirically supported as an integrated-system performance claim.** Implementation/unit tests exist, but no prospective MA-SQLGrid accuracy/robustness run exists. | Complete the blocking prospective experiment or weaken title/claim level. |

## Experiment audit

### Required reruns/new runs

1. **Prospective, budget-matched integrated-system experiment:** direct single candidate; staged single-candidate handoffs; fixed multi-candidate validation/adjudication without counterfactual evidence; same pool with a frozen reference-free invariant/state suite. Include a multi-sample non-agent control.
2. **System ablations:** Analyst/Cartographer handoffs, validation, adjudication, abstention, and counterfactual channel. Each ablation must change one factor or be labeled as a package contrast.
3. **Robustness suite:** schema/value/order/tie/empty-result perturbations, malformed SQL, missing evidence, timeouts, and executor faults, with complete-state denominators and abstention counted.
4. **Held-out power-grid evaluation:** at minimum one untouched database/question set; expert-reviewed gold is preferable. Machine-adjudicated silver can be used for diagnostics but not promoted to expert gold.
5. **Independent recomputation:** regenerate all aggregate tables and digests from immutable item-level ledgers in a clean directory/runtime.

### Desirable analyses

- Stratify held-out results by join count, aggregation, nesting, ordering/ties, and schema size, with the family and exploratory status declared in advance.
- Report calibration/coverage trade-offs for abstention and failure taxonomy by method.
- Provide a prespecified adjudicator sensitivity grid and a “first eligible candidate” baseline.
- Report paired effect estimates and cluster-aware intervals, not only adjusted *p* values.

### Unjustified reruns or relabeling

- Do **not** score the retrospective replay with gold and present it as prospective coordination accuracy.
- Do **not** feed formal-v5 gold-relative agreement into the Critic or selector.
- Do **not** resume, overwrite, delete, or include the two BIRD incident runs.
- Do **not** rerun existing studies selectively until a desired *p* value appears or merge their multiplicity families after seeing outcomes.
- Do **not** relabel GridDB/BIRD prompting workflows as five-agent baselines.

## Figure and table audit

- **Figure 1 (framework): pass with major scientific caveat.** It visibly marks external candidates and the gold boundary, which prevents a common misleading architecture claim. Add the exact eligibility/coverage rule and distinguish the five specialist roles from the deterministic controller. If the final system uses an executor-level authorizer/timeout, show that boundary.
- **Algorithm 1: major.** It says “available reference-free state evidence” but does not expose incomplete-coverage behavior or the fact that `coverage_complete` is unused. Revise after the algorithm is fixed; specify how missing states affect eligibility, abstention, and ranking.
- **Table 1: major reporting omission.** Add correct/180 and composition-sensitivity intervals; identify F00–F11 as bundled package conditions.
- **Component Figure: adequate but incomplete alone.** Its caption correctly says composition sensitivity and multiplicity, but a numeric table should accompany it.
- **Multi-state Figure: major reporting omission.** Provide all eight cell rates, denominators, intervals/status, and the exact 15-state suite definition in a table or supplement.
- **BIRD: blocking presentation gap.** There is no result table. Add all eight model-method cells with correct/500, accuracy, database-cluster interval, calls/item, total calls, failures, and adjusted contrasts. Reporting only the best values in prose invites selective-reading bias even though all values exist locally.
- The PDF builds cleanly and the sampled text has no unresolved citation/cross-reference. The build log has only two `hyperref` PDF-string warnings, not fatal errors.

## Reproducibility and ethics findings

### Strengths

- Raw BIRD recount, component tables, GridDB v2 products, and replay counts agree with the manuscript samples.
- All-attempt denominators, zero-retry policy, incident retention, and independent re-execution are strong practices.
- The replay is correctly labeled diagnostic and explicitly forbids an accuracy claim.
- Gold isolation is a stated software boundary, and unit tests check abstention, multi-statement/write rejection, unknown counterfactual evidence, and tie order.
- The manuscript appropriately labels RTS-GMLC, SimBench, and NERC-derived question–SQL data as machine-adjudicated silver rather than expert gold.
- The human/animal ethics “not applicable” statement and AI-assistance disclosure are appropriate for the described work.

### Problems and required controls

- The submitted coordination implementation is not bound to a released prospective run manifest; unit tests are not performance validation.
- Ledger sealing is software evidence, not an external timestamp. The manuscript already says this for the component selection audit; apply the same epistemic standard to all seals.
- The data-availability statement promises a public repository and restricted verification package, but Round 1 does not demonstrate that the public repository is synchronized to the manuscript hashes. Add a release tag/commit and manifest before submission.
- Third-party BIRD and derived power-system assets must retain their licenses and redistribution restrictions. “Available on request” cannot override upstream permission.
- The corresponding-author email placeholder is intentionally unresolved and blocks portal upload, although it is not a methods defect.

## Concrete revision checklist and verification tests

| ID | Severity | Revision requirement | Verification |
|---|---|---|---|
| M1 | **blocking** | Run the prospective budget-matched integrated MA-SQLGrid experiment, or weaken the title/system claims. | Frozen protocol predates calls; immutable ledgers include every item; independent recomputation matches tables. |
| M2 | **blocking** | Define and test system robustness with reference-free states/invariants and fail-closed missing-evidence handling. | Expected-state coverage appears in item ledgers; incomplete coverage cannot silently outrank complete evidence; robustness denominators are complete. |
| M3 | **major** | Add held-out domain evaluation and a study chronology/data-visibility table. | Hash manifest shows untouched split; manuscript labels visible-development and post-review analyses correctly. |
| M4 | **major** | Add call-matched controls and complete resource accounting. | Calls/item, tokens, failures, latency status, and all-attempt denominators reconcile with raw ledgers. |
| M5 | **major** | Validate/freeze adjudicator rule and conduct sensitivity/ablation analysis. | Rule selected without test-outcome access; sensitivity grid and first-candidate baseline are retained, including negative results. |
| M6 | **major** | Add full GridDB, component, multi-state, and BIRD numeric tables with counts and intervals. | Automated table-to-ledger check reproduces every cell and caption denominator. |
| M7 | **major** | Separate preregistration, prospective freeze, post-review reanalysis, and retrospective diagnostic terminology. | Search/audit finds no stronger chronology label than supported by the dated manifests. |
| M8 | **major** | Strengthen validator/executor security and adversarial tests. | SQLite authorizer/read-only mode, timeout/resource policy, and negative tests pass; failures are retained, not retried away. |
| M9 | **minor** | Clarify that two backbones are sensitivity analyses, not independent replications, wherever results are summarized. | Abstract, Results, and Conclusions use consistent wording. |
| M10 | **minor/manual** | Bind the public code release and fill the correspondence email before submission. | Release commit/tag and package SHA are cited; no manual placeholder remains in portal-ready package. |

## Final methodological judgement

The manuscript is honest about what the inherited experiments do not prove, and its sampled numbers are substantially better documented than the original-title claim would suggest. That honesty does not solve the central design gap: the integrated multi-agent framework and its claimed robustness are not the treatment in any prospective accuracy experiment. Round 2 should treat M1–M2 as blocking and M3–M8 as major. Reformatting or additional prose alone cannot close them.
