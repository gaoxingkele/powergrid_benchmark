# C2GES Round 1 Independent Review: Methods, Statistics, and NLP Experiments

## Review identity and recommendation

- Role: independent methods/statistics/NLP reviewer, Round 1.
- Frozen object reviewed: `paper_applsci.tex` (SHA-256 `F15071AE56BD88DBDB303D277F93C42053E3002EA29DE1FC556DB84A5933F15B`), `build/paper_applsci.pdf` (SHA-256 `E192A812ED513E8A6452AEA5371B3E5E1091E6889033D3C9B93C1F324B14CF5D`), `ASSEMBLY_AUDIT_R1.md`, `ROUND_AUDIT.json`, protocol-v0.1/v0.2 code, frozen data, 224-row prediction ledger, bootstrap output, NERC builder, and auxiliary FEVER assets.
- Recommendation: **reject in the present form**. This is not a request for cosmetic rewriting. Two blocking defects invalidate the central counterfactual interpretation and the reported benchmark estimates. A newly frozen dataset and a functionally identifiable counterfactual method could support reconsideration as a new round.

The manuscript is unusually candid about negative results, silver labels, and the absence of a GNN. The files compile, the principal hashes match the manifests, and the two formal executions are byte-identical. Those strengths do not cure the two foundational defects below.

## Five most serious issues, ordered by decision impact

### 1. Blocking: the counterfactual score is mathematically the same signal as graph salience

The paper defines graph salience as normalized weighted degree (lines 73--79) and counterfactual sensitivity as the normalized loss of total edge weight after deleting a node and its incident edges (lines 91--99). For this graph,

`F(G) - F(G_-i) = sum of weights of all edges incident to i`,

which is exactly the weighted degree used for graph salience. The implementation confirms this identity: `graph_signal()` accumulates each incident edge weight at lines 264--270 of `c2ges_offline.py`, while `counterfactual_sensitivity()` deletes the node, measures the same incident-weight loss, and applies the same min--max transform at lines 272--279. I independently recomputed both arrays for all 781 candidate nodes in the 16 test reports; the maximum absolute difference was `1.9984e-15`, i.e., floating-point noise.

Consequences:

- The nominal Full score at manuscript lines 103--107 is functionally `0.30 Q + 0.20 R + 0.45 G + 0.05 P`, not a five-channel model with an independent counterfactual variable.
- The strict no-CF condition at lines 115--117 changes every retained coefficient through renormalization and changes the effective graph coefficient from 0.45 to 0.2667. Its contrast is therefore a mixture-weight contrast, not an identifiable test of a counterfactual component.
- The negative ablation is honestly reported, but it cannot validate that a distinct counterfactual algorithm was implemented or tested. The word **Counterfactual** in the title is not supported by the present scoring construction.

Acceptance test: before another test-set run, define a counterfactual quantity that is not algebraically reducible to graph degree or any other included channel. Add a unit test requiring non-identity on registered synthetic graphs, document the estimand, register the development-only selection rule, freeze code/config/data, and perform one untouched-test evaluation. If no non-redundant counterfactual definition is justified, remove “Counterfactual” from the title and treat node deletion only as an audit visualization, not a contribution.

### 2. Blocking: official Executive Summary text remains in the candidate pool

The manuscript says that candidates are the body after removal of the detected summary prefix (lines 61--65). The builder does not locate the end of the Executive Summary in the segmented sentence sequence. Instead, it searches only the first `min(40, max(8, len(sentences)//3))` sentences for high containment and cuts after the last match (`build_nerc_summary_dataset.py`, lines 126--135). Long summaries therefore continue past the cut.

My audit normalized case/punctuation and required a candidate of at least 50 characters to occur verbatim in its official reference. It found:

- 116 candidate sentences copied verbatim from their reference across the 28 retained reports;
- 57 such candidates in five test reports (`nerc_001`, `nerc_009`, `nerc_011`, `nerc_014`, and `nerc_032`);
- leaked selections in the frozen ledger, including 2/80 Full selections at K=5 and 6/160 at K=10; Lead selected 16/80 and 28/160 leaked sentences, respectively.

For example, the first test record cuts after sentence 26, yet candidates `s027`--`s030` occur verbatim in the reference. Lead selects all four at K=5. Thus, the headline Full-versus-Lead/TextRank intervals are computed on a contaminated candidate benchmark. The current tests pass but do not test reference-prefix exclusion; `ASSET_MAPPING_ROUND1.md` had already identified this missing assertion.

Acceptance test: rebuild into a new immutable directory using a boundary mapping that aligns the PDF Executive Summary end with segmented sentence IDs. Fail closed if alignment is ambiguous. For every report, record the end SID and a normalized exact/near-duplicate audit. Require zero residual reference-prefix sentences; manually inspect all exceptions attributable to legitimate repetition later in the body. Re-freeze the dataset, rerun all methods, reproduce in a second directory, and withdraw every current ROUGE/contrast value from the next manuscript.

### 3. Blocking for the retained title: the experimental corpus does not establish performance on “maintenance reports” or causal fidelity

Lines 63 and 217 acknowledge that the 28 included documents are heterogeneous NERC disturbance, reliability, storm, recommendation, and assessment reports, not utility maintenance work orders. Only 16 reports are in the test set. The references are very long official Executive Summaries (279--2298 words; median 790.5), whereas outputs contain five or ten sentences. ROUGE consequently rewards length, as the manuscript itself notes at line 189. No domain expert evaluates causal-chain completeness, factual sufficiency, engineering usefulness, or whether a typed edge is causally correct.

The title nevertheless makes a domain-wide “Power Grid Maintenance Reports” claim and foregrounds causal/counterfactual capability. The careful limitations do not make the measured population representative of that title.

Acceptance test: either (a) add a license-cleared maintenance/work-order corpus with report-level split, a frozen sampling frame, and blinded qualified-domain evaluation, or (b) revise the title and abstract to the actually measured NERC reliability/disturbance corpus. If the title must remain unchanged, the additional maintenance-domain evaluation is required, not optional.

### 4. Major: the statistical family and primary-outcome narrative are inconsistent

The registered primary outcome is ROUGE-L at K=5 (lines 119--123 and `formal_config_v0.2.json`). Full does not lead on that outcome: Centroid is higher by 0.0082 and the paired interval crosses zero. The abstract instead foregrounds two positive ROUGE-1 intervals, a secondary metric. This is transparent but still risks outcome switching in emphasis.

The manuscript states that there are 15 comparisons per budget (line 225). The frozen bootstrap file contains 18 per budget: six Full-minus-baseline contrasts times three ROUGE metrics. Across two budgets there are 36 emitted tests/intervals. None is multiplicity-adjusted. With only 16 resampling units, percentile intervals are unstable and the discrete bootstrap distribution does not support strong inferential language. The phrase “improves ROUGE-1” at line 203 should be “has a positive unadjusted exploratory mean difference” unless a confirmatory family is registered and controlled.

Acceptance test: define one confirmatory primary contrast and metric before rerun, report its paired per-report effect and uncertainty, and label all other 35 contrasts exploratory. Correct the comparison count. If inferential claims are retained for a family, apply a registered multiplicity procedure and report adjusted results; otherwise remove significance-style language and present intervals descriptively. Provide per-report paired plots and a robustness analysis suitable for n=16 (e.g., exact paired randomization/sign-based sensitivity in addition to bootstrap), without treating any post-hoc result as confirmatory.

### 5. Major: baseline, development, and silver-label evidence are insufficient for the algorithmic claim

The seven conditions include useful transparent baselines, but the strongest neural comparator is only an all-MiniLM centroid. There is no modern extractive summarizer adapted or prompted for long technical reports, no upper-bound/oracle extract, and no length-matched domain baseline beyond simple ranking. Centroid has the best observed primary metric at both budgets; strict no-CF has the best observed ROUGE-1 at both budgets and ROUGE-2 at K=10.

The protocol says weights are selected on development documents, while the paper calls them “frozen defaults” (line 107). No development-search ledger, objective values, candidate grid, or selection decision is supplied. Therefore, absence of test tuning is asserted but the origin of 0.30/0.20/0.20/0.25/0.05 and 0.35 is not evidenced.

Silver role evidence directly changes test-time graph roles and selection (lines 67--73), yet its creation provenance is only `agent_verified_candidate_not_human_gold`. It is not shown whether the machine workflow saw the Executive Summary or other target-derived material. The coverage metric is correctly called circular/diagnostic, but possible target leakage into the selector itself is not ruled out.

Acceptance test: publish a development-only model-selection ledger or relabel coefficients as unselected heuristics and avoid performance optimization claims. Freeze and document the silver-generation inputs, prompts/code/model hashes, and prove that references were inaccessible. Add a lexical-only Full condition with no silver input. Add at least one competitive length-matched technical-document extractive baseline and an oracle extract to contextualize headroom. Do not promote FEVER results as evidence for NERC summarization or causal modeling.

## Claim--evidence audit

| Manuscript location | Claim | Evidence finding | Severity / required action |
|---|---|---|---|
| Title; abstract line 19 | Causal and counterfactual graph-enhanced summarization | Proxy roles are not validated causality; CF equals graph degree at all audited nodes | **Blocking**. Redesign and freeze an identifiable CF signal or change title/claim. |
| Lines 31, 49--51, 79, 99, 209--211 | Graph is a causal proxy; intervention is not physical causality | Boundary language is appropriate, but “causal” remains based on hand-written role transitions and machine silver | Major. Use “role-transition proxy graph” consistently unless independently validated. |
| Lines 61--65 | Candidate body excludes the Executive Summary prefix | Contradicted by 57 verbatim reference candidates in five test reports | **Blocking**. Rebuild and rerun; current results are not usable. |
| Abstract line 19; lines 129--156, 178--184, 235 | Aggregate ROUGE and paired intervals | Values checked against `aggregate_metrics.json` and `paired_bootstrap.json`; values/hashes match, but inputs are contaminated | **Blocking**. Numerically traceable does not mean scientifically valid. Withdraw after clean rerun. |
| Lines 115--117, 152--156, 203--205 | Strict no-CF isolates the counterfactual contribution | False functional isolation because C=G and other coefficients are renormalized | **Blocking**. Replace ablation design. |
| Lines 119--123 | ROUGE-L is primary; 10,000 report-level resamples | Supported by config/code | Major interpretation issue: abstract foregrounds secondary ROUGE-1; multiplicity unadjusted. |
| Line 150 | “only v0.2 five-sentence ROUGE intervals excluding zero” are R1 vs Lead/TextRank | Matches raw v0.2 bootstrap family | Descriptively correct, but contaminated and unadjusted. |
| Lines 191--193 | Two executions are byte-identical, 224 cells complete | Verified hashes: predictions `1F8296...43BE1`, aggregates `B26D43...82F71`, bootstrap `4CA4AA...B5AB8` | Supported. Keep as computational reproducibility only. |
| Lines 195--197 | FEVER auxiliary evidence selection, not domain result | Boundary is explicit; local generated artifacts were not re-derived in this review | Minor. Consider moving to supplement because it distracts from the NERC experiment. |
| Lines 203--205 | Full “improves” R1 over Lead/TextRank | Positive unadjusted intervals exist, but primary metric is R-L and data are contaminated | **Blocking** for current numeric claim; after rerun use exploratory wording unless preregistered. |
| Lines 221--227 | n=16, silver limitations, 15 comparisons, no test tuning | n/silver limits stated; comparison count is wrong (18 per budget); no development ledger proves coefficient selection | Major. Correct and supply ledger. |
| Lines 233--237 | Supported contribution includes counterfactual ablation | A negative execution exists but does not isolate a distinct CF variable | Major/blocking depending on retained title. |

## Experiment audit

### Required reruns

1. **Clean benchmark rerun** after deterministic Executive Summary boundary alignment and a zero-prefix-leakage gate. This must receive a new dataset hash and protocol version; v0.2 must remain retained but excluded.
2. **Identifiable counterfactual rerun** only after a development-only redesign whose signal is demonstrably non-collinear/non-identical with graph salience and whose selection rule is frozen before touching test data.
3. **No-silver condition** to show performance without precomputed machine role evidence and to rule out reference-aware silver leakage.
4. **Length-controlled evaluation**: keep fixed sentence budgets if desired, but add word/token-matched budgets because sentence lengths vary and references are very long.
5. **Primary statistical analysis** with one preregistered K=5 ROUGE-L contrast, per-report paired values, and appropriate n=16 sensitivity analysis. Treat remaining contrasts as exploratory.

### Required new evidence if the original title is retained

1. A representative, license-cleared sample of actual maintenance/work-order reports or a defensible mapping from the NERC sampling frame to that target population.
2. Blinded assessment by multiple qualified human power-grid reviewers of causal-chain completeness, factual support, and operational usefulness, with a frozen rubric, independent labels, retained disagreements, and human adjudication. An LLM-only panel is not expert validation.
3. At least one competitive long-document/technical-report extractive comparator and an extractive oracle.

### Desirable analyses

- Stratify results by report genre and reference length, while labeling all subgroup analyses exploratory.
- Report edge counts, isolated-node rates, role distributions, and the fraction of selections forced by each coverage reservation.
- Quantify graph/role/position channel correlations on development and test sets. This would have exposed C=G immediately.
- Evaluate summary factuality only with source-grounded human criteria; do not infer factuality from ROUGE.
- Group related report series before split and audit cross-split near duplicates. Hashing `doc_id` alone does not prevent series-level leakage; the top dev/test reference-token Jaccard observed in my audit was 0.701.

### Unjustified reruns or claims

- Do not tune a revised counterfactual formula or weights on the current 16 test reports.
- Do not repeatedly rerun alternative methods against the same test set and select the most favorable title narrative.
- Do not call machine or LLM labels “expert adjudication,” “ground truth,” or “causal fidelity.”
- Do not use the FEVER experiment to compensate for missing domain validation.
- Do not describe higher K=10 ROUGE as better precision, causal validity, or engineering usefulness.

## Figure and table audit

### Figure 1

The architecture is legible in the PDF and its caveats about no GNN/API/physical causality are useful. However, it visually presents “weighted-degree graph signal” and “node-deletion sensitivity” as distinct channels. They are the same normalized vector under the implemented definitions. The figure is therefore materially misleading even though the code path is drawn correctly. Replace it only after the method is redesigned, or merge both boxes/signals and state the algebraic equivalence. Prefer the vector SVG/PDF source over the QA PNG for submission.

### Figure 2

The bars match the aggregate JSON and clearly show no dominant Full model. The figure omits uncertainty and paired structure. Replace or supplement it with per-report paired-difference plots and intervals for the registered primary contrast. Do not use bar height alone for inferential interpretation.

### Tables 1 and 2

The displayed means match `aggregate_metrics.json`. The captions say bold marks the column maximum, but redundancy bolding marks the minimum (Lead: 0.0539 at K=5 and 0.0516 at K=10). Change the caption to “best observed direction: maximum for ROUGE/coverage and minimum for redundancy,” or avoid bolding. Add `n=16` explicitly in each caption and distinguish primary versus exploratory metrics. All current values must be replaced after the leakage-corrected rerun.

### Evidence-package clutter

`ROUND_AUDIT.json` includes a literal `$outputDir/paper_applsci.pdf`, failed build outputs, unused legacy FEVER figures/tables, and multiple PDFs. This does not change the authoritative PDF hash, but a submission package should contain a single canonical manuscript/PDF plus clearly separated retained-failure and auxiliary directories. A file-inventory PASS is not a scientific-validity gate.

## Reproducibility audit

### Verified strengths

- Recomputed SHA-256 values match the manuscript audit for TeX, PDF, frozen dataset, predictions, aggregate metrics, and bootstrap output.
- Run 01 and Run 02 core output hashes match.
- All 14 local unit tests pass.
- The formal runner refuses an existing output directory and verifies frozen code/config/data/runtime/model hashes.
- The 224-row count is consistent with 16 reports x 7 conditions x 2 budgets.

### Blocking gaps

- No test asserts complete removal of the Executive Summary from candidate prefixes.
- No test checks that counterfactual sensitivity differs from graph salience; in fact, a correct such audit currently proves identity.
- The reported “independent reproduction” is computationally independent only in directory/execution, not an independent implementation or analyst recomputation.
- Absolute local model paths reduce portability even though revision/tree hashes are supplied.
- No provenance record establishes that silver-role generation could not access the reference.

Acceptance test: add explicit leakage, channel-identity, silver-provenance, split-near-duplicate, and canonical-package tests. Have a separate script recompute tables directly from the clean prediction ledger without importing the experiment runner.

## Ethics, licensing, and governance audit

- The manuscript correctly states that no human/animal participants were involved in the current computational study and discloses AI-assisted drafting/code review.
- It correctly refuses to call machine silver labels human/expert gold.
- The proposed future human study appropriately requires qualified independent reviewers and retained disagreements; this must be implemented before any expert-validity claim.
- Data availability appropriately conditions NERC materials on third-party permissions. Before submission, provide the editor with source URLs/hashes and a permission/redistribution matrix. “Available on request” cannot promise redistribution that the authors are not licensed to provide.
- The corresponding-author email is still a manual placeholder, correctly blocking portal upload but not scientific review.
- Because some candidate text is copied from the reference by a parsing failure, the current paper must not present the benchmark as leakage-controlled or its ROUGE estimates as valid evidence.

## Blocking, major, and minor revision ledger

### Blocking

1. Counterfactual score is algebraically identical to graph salience; title/component claim is unsupported.
2. Reference-prefix leakage contaminates candidates and selected outputs; all domain metrics must be rerun.
3. Original “maintenance reports” title requires actual maintenance-domain evidence or must be narrowed.

### Major

1. Register and control the statistical family; correct 15 to 18 comparisons per budget.
2. Supply coefficient-development provenance and a no-silver condition.
3. Add stronger, length-matched baselines, an oracle, and qualified human domain evaluation for causal usefulness.
4. Revise Figure 1 and add paired uncertainty visualization.
5. Audit series-level split similarity, not only exact report hashes.

### Minor

1. Correct table bolding captions for redundancy.
2. Move the auxiliary FEVER paragraph/results to the supplement or shorten it.
3. Replace QA raster architecture art with vector output in the submission source.
4. Clean the canonical round/package inventory while retaining failures outside the submission bundle.

## Round-2 acceptance checklist

A methods reviewer should not clear Round 2 until every item below is machine- or artifact-verifiable:

- [ ] New dataset directory/hash; old v0.2 preserved and explicitly excluded.
- [ ] Zero unresolved Executive Summary prefix sentences in candidates, with per-report alignment audit.
- [ ] Counterfactual signal is formally distinct from graph salience and passes a registered non-identity test.
- [ ] Development-only choice ledger predates the new test run; test set executed once after freeze.
- [ ] No-silver and stronger length-matched baselines are present.
- [ ] One primary contrast/metric is declared; the complete exploratory family is counted and labeled.
- [ ] Tables and claims regenerate from the clean ledger and an independent recomputation matches.
- [ ] Figure 1 reflects actual distinct computations; result plots show paired uncertainty.
- [ ] Title population is supported by a maintenance corpus and qualified reviewers, or the title is narrowed.
- [ ] Licensing/redistribution matrix and editor-only verification package are complete.

