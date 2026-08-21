# Round 1 Methodology and Statistics Review: C²GES

## Recommendation

**Major Revision**. Confidence: **5/5**. Statistical-reporting status: **Adequate for a corrective descriptive study, but not for a confirmatory effectiveness claim**.

The manuscript is unusually candid about its negative ablation, post-unblinding chronology, unequal output lengths, and lack of maintenance-domain validation. The central methodological problem is therefore not concealed misconduct or selective reporting; it is a mismatch between the breadth suggested by RQ1/title language and what the selected, outcome-exposed, equal-sentence proxy study can estimate.

## Strengths

1. **RQ-to-evidence separation is explicit.** Section 3.1 and Table `tab:claim-evidence-map` distinguish system comparison, component attribution, and transfer. The report, rather than the 12,924 nested candidate units, is correctly designated as the inferential unit (Section 3.1, paragraph beginning “The unit of analysis is the report”).
2. **The component ablation is well controlled.** Section 3.5 states that strict no-CF changes only the coefficient of `C_i`, without renormalizing other weights or changing candidates, graph construction, redundancy, tie rules, or budgets. This is the strongest design element for RQ2.
3. **Adverse evidence is retained.** Sections 3.7, 3.8, 4.4, 5.1, and 6 report the unfavorable Full-minus-no-CF estimates, intervals crossing zero, and the post-unblinding development search that selected zero CF in all 12 folds.
4. **Multiplicity and chronology are visible.** Table `tab:signflip` adjusts all six post-run exact values as one Holm family, while the manuscript labels this analysis unregistered and post-run. Earlier contaminated versions are explicitly withdrawn.
5. **Reproducibility and leakage controls are layered.** Sections 3.2 and 3.7 identify hashes, partitions, page-boundary checks, candidate/reference matching, row-set checks, and immutable ledgers without treating audit success as algorithmic accuracy.

## Major findings

### M1. RQ1 is not answered as a fair effectiveness comparison

- **Severity:** Major
- **Evidence anchors:** Introduction, RQ1 paragraph; Section 3.5 “Sentence-count budgets”; Section 4.2, Table `tab:length-audit`; Section 4.6, RQ1 answer.
- **Evidence:** Full uses 287.7/568.9 mean words, versus 184.7/354.5 for Semantic-MMR and 177.0/369.0 for TextRank. Full is therefore about 56%/60% longer than Semantic-MMR and 63%/54% longer than TextRank at K=5/10. Long and table-fused extraction units are frequent.
- **Why it matters:** The primary endpoint rewards recovered reference tokens. Equal sentence counts do not control the amount of evaluated text, so the observed Full-baseline ROUGE differences cannot identify ranking quality independently of output volume.
- **Actionable fix without new experiments:** Rewrite RQ1 and every corresponding answer as a **descriptive equal-extraction-unit comparison**. Do not use unqualified “higher performance” or “superiority.” Make Table `tab:length-audit` part of the RQ1 answer, and state that the experiment cannot rank the systems under equal information budgets.

### M2. The uncertainty intervals do not license population inference

- **Severity:** Major
- **Evidence anchors:** Section 3.1, paragraph beginning “This is a post-audit corrective evaluation”; Sections 3.2 and 3.7; Table `tab:contrasts`.
- **Evidence:** The 15 reports are a selected subset from one organization; the population was inspected during corrective reconstruction; inclusion depends on readable PDFs and detectable summaries; the formal split is not outcome-unseen. The percentile bootstrap resamples only these observed reports.
- **Why it matters:** “95% CI” can be read as sampling uncertainty for a target population, but neither random sampling nor an outcome-unseen holdout supports that interpretation.
- **Actionable fix:** Rename these throughout as **95% report-composition bootstrap intervals** (or explicitly define them as sensitivity intervals). State the finite-set estimand immediately before Table `tab:contrasts`: mean paired difference over these 15 retained reports. Avoid “test-set confirmation.”

### M3. No practical-significance threshold is defined

- **Severity:** Major
- **Evidence anchors:** Section 3.7 metric hierarchy; Tables `tab:all-results` and `tab:contrasts`; Sections 4.6 and 5.1.
- **Evidence:** Raw paired ROUGE-L differences and intervals are reported, but there is no predeclared minimum meaningful ROUGE change, word-normalized endpoint, expert judgment, or safety/coverage threshold.
- **Why it matters:** Small exact or interval-separated lexical-overlap differences are not automatically meaningful for engineering review, especially with unequal length.
- **Actionable fix:** Add an explicit statement that **practical significance is not identifiable in this study** because no minimally important difference or human-centered criterion was registered. Interpret raw differences as lexical-overlap effect estimates only; do not retrofit a threshold.

### M4. Hyperparameter opportunity and selection uncertainty are asymmetric

- **Severity:** Major
- **Evidence anchors:** Section 3.6, paragraphs reporting 144 configurations and comparator opportunity; Section 3.8.
- **Evidence:** Full receives a 144-configuration development search on 12 reports, while Semantic-MMR is fixed at 0.5 and TextRank uses a frozen implementation. The post-unblinding 147-configuration search is diagnostic, not validation.
- **Why it matters:** RQ1 mixes algorithm differences with unequal tuning effort, while the small development set creates considerable selection uncertainty not propagated into Table `tab:contrasts`.
- **Actionable fix:** Establish strict no-CF as the primary mechanism comparator and label Semantic-MMR/TextRank comparisons exploratory. Add one compact table listing tuning dimensions and number of tried configurations for every method. State that the reported intervals condition on the selected configuration and omit model-selection uncertainty.

### M5. The theoretical contribution is path participation, not causal or counterfactual identification

- **Severity:** Major
- **Evidence anchors:** Section 2.2; Section 3.4, Equations defining `U(G)` and `C_i`; Section 5.2.
- **Evidence:** `C_i` equals the sum of strengths of registered textual paths containing node i. Node deletion does not change edge weights or model predictions and does not identify interventions, potential outcomes, or physical relations. Roles and edges also lack expert validation.
- **Why it matters:** The mathematics supports a deterministic weighted path-participation sensitivity, but not the stronger causal semantics readers may infer from the title and terminology.
- **Actionable fix:** Present a short proposition naming `C_i` as a **weighted qualified-path participation functional** and state its assumptions (fixed graph, unchanged remaining path weights). Keep “counterfactual” only as the implementation label and use “structural deletion sensitivity” for claims.

### M6. Dependence and cross-document leakage limitations are incomplete

- **Severity:** Major
- **Evidence anchors:** Section 3.2 leakage gates; Section 3.7 sign-flip assumptions; Section 5.4 limitations.
- **Evidence:** Within-report summary/body leakage is carefully checked, but no audit is reported for cross-report near-duplicate language, revised editions, or repeated organizational boilerplate across development and test. The sign-flip analysis assumes report independence and symmetric paired errors with only 15 reports.
- **Why it matters:** Unique PDF hashes do not imply independent textual evidence; related NERC reports can share language and event material. Dependence would make report-level resampling and sign flipping optimistic.
- **Actionable fix:** Add this as an explicit unresolved leakage/dependence limitation. If an existing metadata ledger already records report series or event families, report a sensitivity grouping from it; otherwise do not claim the split is cross-report-content independent.

## Minor findings

1. **Synthetic arithmetic discrepancy.** Section 3.4/Table `tab:toy-path` gives rounded path strengths 0.567, 0.741, 0.367, 0.542 and states `U(G)≈2.217`. Direct evaluation from the displayed edge weights gives 0.566964, 0.741559, 0.367423, 0.542282, hence **`U(G)=2.218228≈2.218`**; the root-node subtotal 1.308523≈1.309 is correct. Correct the narrative or say 2.217 is the sum of already rounded table entries.
2. **Overstrong heterogeneity sentence.** Section 4.4 says the paired analysis “rules out” a few-extreme-reports explanation. Sign counts show that direction is widespread for some contrasts, but they do not rule out magnitude influence. Replace with “shows that the sign was not confined to a few reports.”
3. **Registered-tail table clarity.** Table `tab:contrasts` displays the unadjusted descriptive bootstrap tail values, whereas the prose mentions a stored Holm transformation. Label the column “unadjusted descriptive tail quantity” and point to the preserved adjusted artifact; do not make it resemble a conventional p-value.
4. **Post hoc effect descriptors.** If standardized paired effects are added, label them descriptive and derived from the immutable ledger; raw ROUGE differences remain more interpretable than standardized values.

## Arithmetic and statistical audit receipt

All six exact sign-flip values were independently recomputed from `predictions.jsonl` by enumerating all `2^15=32,768` sign assignments. They match Table `tab:signflip`: 0.436768, 0.000305, 0.000122, 0.200684, 0.006592, and 0.009644. Holm adjustment over the six-value family reproduces 0.436768, 0.001526, 0.000732, 0.401367, 0.026367, and 0.028931.

The paired ledger also reproduces the six mean differences in Table `tab:contrasts`. Descriptive paired SDs are 0.01419, 0.01581, 0.01656, 0.00958, 0.01660, and 0.01513 in table order. No conventional test statistic/df pair is reported for a bounded `p_from_test_statistic` recomputation; the bootstrap and exact randomization procedures are nonstandard resampling procedures and were checked against their retained ledgers instead.

## Conclusion-following-evidence verdict

The negative RQ2 conclusion follows from the controlled ablation. The auditability conclusion follows from the retained records. The RQ1 baseline observations follow only as finite, equal-sentence, unequal-word descriptions. Maintenance usefulness, semantic quality, physical causality, and population-level superiority do not follow; the manuscript generally admits this, but the RQ wording and interval labels should be tightened so readers cannot miss it.
