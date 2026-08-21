# W6 Staging Draft: C2GES Results, Discussion, Limitations, and Conclusions

**Status.** This staging text reports only the frozen five-seed, document-grouped FEVER experiment and the audited NERC evidence boundary. The primary role-conditioning claim is a frozen **NO-GO**, and blanket superiority over BM25 is also **NO-GO**. The draft does not modify the main manuscript and must replace, rather than coexist with, results derived from the superseded split.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Decision -->

## 5. Results

### 5.1. Execution Completeness and Evidence Audit

All five training seeds—2026 through 2030—completed for the oracle-label, predicted-label, and label-blind protocols. Seed 2026 was the frozen W3 run and was not rerun; the other four seeds were executed after the W4 configuration freeze. The combined evidence and failure audit passed 176 checks with zero failures, covering protocol identity, seeds, data counts, cutoffs, leakage controls, required files, hashes, prediction coverage, and resource records.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/failure_and_evidence_audit.json | KEYS: passed,check_count,failure_count,checks -->

The experiment retained the document-grouped corpus of 8000 training, 1500 development, and 1500 test instances, with 745, 141, and 145 underlying Wikipedia documents, respectively, and no exact document overlap. Thus the five-seed results use the original Wikipedia document—not a claim identifier—as both the split group and the inner bootstrap cluster.

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/failure_and_evidence_audit.json | KEYS: counts,leakage grouping_key,unique_documents,pairwise_overlap -->

### 5.2. Five-Seed Evidence Selection

Table 1 summarizes macro mean instance-level evidence F1. At \(K=1\), BM25 obtained 0.6994, whereas the oracle-label, predicted-label, and label-blind C2GES variants obtained five-seed means of 0.6705, 0.6688, and 0.6677. At \(K=3\), the corresponding C2GES means were 0.4926, 0.4920, and 0.4910, compared with 0.4864 for fixed BM25. Differences became numerically smaller as the returned-sentence budget increased.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Five-seed evidence F1 -->

#### Table 1. Five-seed evidence F1, reported as mean ± sample standard deviation; BM25 is fixed.

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| Oracle-label C2GES | 0.6705 ± 0.0050 | 0.4926 ± 0.0015 | 0.4160 ± 0.0009 | 0.3563 ± 0.0001 |
| Predicted-label C2GES | 0.6688 ± 0.0051 | 0.4920 ± 0.0021 | 0.4150 ± 0.0007 | 0.3563 ± 0.0002 |
| Label-blind C2GES | 0.6677 ± 0.0021 | 0.4910 ± 0.0021 | 0.4154 ± 0.0006 | 0.3560 ± 0.0003 |
| BM25 | 0.6994 | 0.4864 | 0.4109 | 0.3530 |

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: metric,metric_summary -->

The standard deviations across five seeds were small in absolute terms, particularly at the larger cutoffs, but this stability must not be interpreted as evidence for the role mechanism. Overall C2GES F1 can be stable while the difference between role-aware and role-blind variants remains small, sign-changing, or uncertain. The prespecified decision therefore rests on paired effects rather than on overlap or non-overlap of separate method-level intervals.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: metric_summary,effects,claim_decisions -->

### 5.3. Primary Role-Conditioning Decision

At the primary cutoff \(K=3\), predicted-label minus label-blind had a mean F1 difference of 0.00097. Its seed-level t interval was [−0.00165, 0.00359], and its hierarchical seed/document bootstrap interval was [−0.00119, 0.00307]. Both intervals crossed zero, so the prespecified positive-effect gate failed and the primary role-conditioning claim is **NO-GO**.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: predicted-label_minus_label-blind at K=3 -->

The two oracle sensitivity contrasts reached the same decision. Oracle-label minus label-blind was 0.00157 at \(K=3\), with seed-level interval [−0.00167, 0.00482] and hierarchical interval [−0.00093, 0.00440]. Oracle-label minus predicted-label was 0.00060, with intervals [−0.00117, 0.00237] and [−0.00121, 0.00228]. Neither contrast passed the positive gate.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: oracle sensitivity contrasts at K=3 -->

This result rejects a reliable role-gain claim under the implemented architecture and protocol; it does not prove that role information is universally useless. The observed mean differences are close to zero relative to the absolute F1 scale, and their uncertainty includes small effects in both directions. Accordingly, role conditioning may remain an inspectable input or an exploratory design element, but it cannot be the article’s demonstrated primary contribution.

<!-- CLAIM: C2-C09 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: claim_decisions.role_conditioning_primary_claim,manuscript_implication -->

### 5.4. Cutoff-Dependent Comparison with BM25

BM25 was clearly stronger at \(K=1\). Relative to BM25, the hierarchical mean differences were −0.0289 for oracle-label, −0.0306 for predicted-label, and −0.0317 for label-blind C2GES. Their 95% hierarchical intervals—[−0.0435, −0.0141], [−0.0465, −0.0157], and [−0.0456, −0.0173]—were wholly negative. Therefore, a one-sentence retrieval budget favoured BM25 for every C2GES protocol.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Relative to BM25,K=1 -->

At \(K=3\), oracle-label and predicted-label C2GES had tiny positive differences over BM25: 0.0062 with hierarchical interval [0.0017, 0.0109], and 0.0056 with [0.0008, 0.0107], respectively. The protocol-specific positive-effect gates passed. These advantages are cutoff-specific and small; moreover, the oracle comparison is conditional rather than end-to-end because it consumes the human FEVER veracity label.

<!-- CLAIM: C2-C03 | STATUS: CONDITIONAL-ORACLE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: oracle/predicted K=3 BM25 contrasts and oracle boundary -->

The label-blind comparison did not pass at \(K=3\). Its mean difference from BM25 was 0.0046, but the hierarchical interval was [−0.0000, 0.0092] and included zero at the stored numerical precision. The gate was therefore **NO-GO**, even though the seed-level mean was positive. This distinction prevents a positive point estimate from being reported as a confirmed end-to-end advantage.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: effects.label-blind_minus_bm25.3,positive_effect_gate -->

At \(K=5\) and \(K=10\), all three protocols had small positive hierarchical intervals relative to BM25, with mean differences ranging from 0.0031 to 0.0051. However, the negative results at \(K=1\), the label-blind failure at \(K=3\), and the conditional nature of oracle-label make blanket superiority untenable. The frozen decision for “C2GES broadly outperforms BM25” is **NO-GO**.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: effects against BM25,claim_decisions.blanket_superiority_over_bm25 -->

#### Table 2. Frozen protocol-specific decisions relative to BM25.

| Protocol | K=1 | K=3 | K=5 | K=10 | End-to-end interpretation |
|---|---|---|---|---|---|
| Oracle-label | BM25 stronger | Tiny C2GES advantage | Tiny C2GES advantage | Tiny C2GES advantage | No; conditional oracle |
| Predicted-label | BM25 stronger | Tiny C2GES advantage | Tiny C2GES advantage | Tiny C2GES advantage | Yes, including upstream errors |
| Label-blind | BM25 stronger | NO-GO | Tiny C2GES advantage | Tiny C2GES advantage | Yes |

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Relative to BM25 and claim guidance -->

### 5.5. Runtime and Resource Observations

Mean wall time was 200.40 s for oracle-label, 204.99 s for predicted-label, and 200.40 s for label-blind, with all five runs successful in each protocol. Mean sampled peak resident memory was 1.280, 1.270, and 1.274 GiB, respectively. These measurements show comparable recorded execution footprints across protocols, not an efficiency advantage over external rerankers or BM25.

<!-- CLAIM: C2-C08 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Runtime and failures -->

Memory was sampled over the process tree every 0.2 s and may miss shorter peaks; GPU memory was not part of this CPU run. The predicted-label wall time also does not, by itself, establish the full lifecycle cost of generating and maintaining the upstream role classifier. Consequently, the evidence supports transparent resource reporting but not a general low-cost claim.

<!-- CLAIM: C2-C08 | STATUS: PENDING-SCOPE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: RSS measurement limitation and manuscript implication -->

## 6. Discussion

### 6.1. Main Interpretation

The central finding is budget-dependent retrieval behaviour rather than a stable role-conditioning benefit. BM25 was strongest when only one sentence could be returned, while C2GES variants produced small advantages at several larger cutoffs. This pattern is consistent with different ranking objectives: a lexical method can place a highly matching sentence first, whereas a learned mixture can distribute evidence-relevant sentences more favourably deeper in the short list. The current experiment establishes the pattern but does not isolate its mechanism.

<!-- CLAIM: C2-C05 | STATUS: SCOPED-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: cutoff-specific effects; mechanism is interpretation -->

The most operationally defensible end-to-end result is the predicted-label protocol, because its training roles are document-grouped out-of-fold predictions and its development/test roles come from a classifier fitted only on training documents. At \(K=3\), this workflow had a small positive interval relative to BM25. Nevertheless, it was not reliably better than label-blind C2GES, so the gain cannot be attributed to role information.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: predicted-label BM25 and predicted-minus-blind decisions -->

Oracle-label remains useful as a conditional sensitivity analysis: it asks what the selector would do if veracity were supplied correctly. Its results cannot be described as end-to-end evidence selection, because human FEVER veracity is exposed at inference time. The small oracle advantage over predicted-label at \(K=3\) also failed its paired gate, providing no basis to argue that access to correct roles materially changed selection.

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED-END-TO-END | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: oracle-label_minus_predicted-label.3 and oracle protocol boundary -->

### 6.2. Why the Role Claim Failed

One explanation is that query relevance already captures most of the distinction associated with SUPPORTS and REFUTES in the document-conditioned candidate pool. Another is that a two-class veracity role is too coarse to guide sentence selection beyond what the claim text provides. A third is architectural: positive mixture floors force the role channel to remain present, but presence does not ensure that it encodes information complementary to query and local-chain scores. These are hypotheses for follow-up ablation, not conclusions demonstrated by the five-seed comparison.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: RoleHead,MixtureParams; explanatory hypotheses -->

The appropriate scientific response to the failed gate is to narrow the contribution. C2GES can still be described as an auditable mixture reranker evaluated under leakage-controlled role protocols, but the manuscript should not say that causal-role conditioning improves evidence selection. Future variants should be compared against the present label-blind model and should earn a role claim through a new preregistered evaluation rather than reinterpret the current near-zero effects.

<!-- CLAIM: C2-C09 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Claim guidance -->

### 6.3. Practical Meaning of K

The cutoff \(K\) represents a reading budget. A user who needs one sentence receives the clearest support from BM25 in this experiment. When a short evidence packet of three or more sentences is acceptable, the learned reranker can provide slightly higher evidence F1 under some protocols and cutoffs. Because these differences are only a few thousandths of F1 at larger \(K\), deployment choice should also consider implementation complexity, latency, traceability, and the cost of the upstream classifier.

<!-- CLAIM: C2-C05 | STATUS: SCOPED-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Five-seed F1 and Relative to BM25 -->

This framing makes BM25 a strong operating point rather than a weak baseline. The five-seed study does not justify replacing it universally. A practical system could expose both a lexical top-1 answer and a C2GES-expanded evidence packet, but that hybrid workflow is a proposed application design and requires a separate user or task-level evaluation.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: blanket superiority NO-GO; hybrid is prospective -->

### 6.4. Statistical Resolution with Five Seeds

Five seeds are sufficient to expose instability and prevent single-seed selection, but they provide limited resolution for seed-level randomisation inference. With \(n=5\), an exact two-sided sign-flip test has only \(2^5=32\) assignments; even five effects with the same sign yield a minimum attainable two-sided p-value of \(2/32=0.0625\). Therefore, the stored sign-flip p-values cannot cross a conventional 0.05 threshold solely because of their discrete resolution.

<!-- CLAIM: C2-C04 | STATUS: POWER-LIMITATION | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_effects.csv | KEYS: n=5 exact_sign_flip_p and minimum 0.0625 -->

For that reason, the analysis reports both seed-level t intervals and hierarchical bootstrap intervals that resample training seeds and underlying Wikipedia documents. Agreement between these intervals is informative, but neither creates additional independent seeds. The role gate failed because both interval families crossed zero, not because the underpowered sign-flip test was treated as decisive.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Claim guidance and primary role effect -->

### 6.5. Power-Grid Application Boundary

The NERC collection remains an application case comprising public source reports and agent-rewritten, agent-verified silver questions and evidence identifiers. It can illustrate inspectable score traces and the types of trigger, root-cause, propagation, impact, and mitigation evidence that engineers may seek. It cannot establish quantitative power-grid-domain superiority, expert agreement, or a human gold benchmark.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED-QUANTITATIVE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: status,label_provenance,role_counts -->

Accordingly, the main quantitative evidence should remain the human-annotated FEVER sentence-selection experiment, with NERC presented in a separate qualitative case-study section. Any NERC examples must retain their report URL, document identifier, sentence identifier, agent-label provenance, and non-human status. A future expert-adjudicated NERC set would constitute new evidence rather than a relabelling of the existing silver corpus.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED-QUANTITATIVE | ARTIFACT: data/public_datasets/reliability_reports/c2ges_nerc_reports/metadata/c2ges_nerc_report_manifest.json | KEYS: official report mapping and local provenance -->

## 7. Limitations

First, exact normalized-title disjointness does not rule out Wikipedia redirects, repeated passages, content-level overlap, entity aliases, or semantic near-duplicates. The title audit screened and reviewed high-similarity names, but its documented scope is lexical title identity. The reported generalisation is therefore across exact document groups under this conversion, not across every notion of semantic document independence.

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/W3_C2_PILOT_REPORT.md | KEYS: title audit limitation -->

Second, the FEVER task is document-conditioned evidence selection. Candidate Wikipedia documents are supplied, so the experiment does not measure open-corpus retrieval, page selection, complete fact-verification accuracy, or power-grid report search across a repository. The predicted-label protocol is end-to-end only with respect to role prediction plus within-document sentence selection.

<!-- CLAIM: C2-C02 | STATUS: SCOPED-END-TO-END | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: build_examples and per-document candidate ranking -->

Third, oracle-label is not an end-to-end system. Its human FEVER veracity input is unavailable before verification in an ordinary deployment, so oracle results are a conditional sensitivity bound. They must not be merged with predicted-label or label-blind results to imply a deployable average.

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED-END-TO-END | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: oracle consumes human FEVER veracity,end_to_end=false -->

Fourth, five training seeds remain a small algorithmic-repeat sample. The exact sign-flip test is discretely underpowered, while hierarchical document resampling characterises within-corpus uncertainty rather than new datasets or independent research sites. More seeds could sharpen algorithmic variability but would not remedy dataset shift or task-scope limitations.

<!-- CLAIM: C2-C04 | STATUS: POWER-LIMITATION | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: five-seed limitation and retained sign-flip values -->

Fifth, BM25 was fixed while learned systems varied over seeds. The paired hierarchical analysis accounts for method differences over common documents and learned repeats, but it does not turn BM25 into a stochastic training distribution. Results should therefore be read as comparisons with one frozen BM25 configuration, not every possible tokenizer, parameterisation, or retrieval implementation.

<!-- CLAIM: C2-C05 | STATUS: SCOPED-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: BM25 fixed metric_summary and effects -->

Sixth, runtime and RSS measurements are incomplete cost indicators. The 0.2-second sampler can miss short memory spikes, and the study does not provide matched energy use, GPU memory, engineering labour, or external reranker cost. Component transparency is directly inspectable, but claims of interpretability benefit or low-cost deployment still require user-centred case audit and broader resource comparison.

<!-- CLAIM: C2-C08 | STATUS: PENDING-SCOPE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Runtime limitations -->

Finally, the NERC annotations are silver, agent-generated candidates rather than independent expert judgements. They cannot support quantitative domain conclusions, clinical-style ground-truth language, or claims about engineer utility. A credible next stage requires blinded domain review, adjudication, agreement measurement, and a held-out application subset.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED-QUANTITATIVE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: agent_verified_candidate,not human gold -->

## 8. Conclusions

Under a document-grouped five-seed evaluation, C2GES did not demonstrate a reliable role-conditioning gain. Predicted-label, oracle-label, and label-blind differences at the primary \(K=3\) cutoff were small and their seed-level and hierarchical intervals crossed zero. The role claim is therefore **NO-GO**, and role awareness should not be presented as the method’s established central contribution.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Primary role effect at K=3 -->

The comparison with BM25 was cutoff dependent. BM25 was stronger at \(K=1\); oracle-label and predicted-label C2GES had tiny positive advantages at \(K=3\), while label-blind did not pass there; all variants had small positive intervals at \(K=5\) and \(K=10\). These findings support a budget-aware comparison, not blanket C2GES superiority.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: BM25 effects and claim decisions -->

The defensible contribution is a reproducible and auditable study of an interpretable mixture reranker under oracle, leakage-controlled predicted-label, and label-blind protocols. The predicted-label branch is end-to-end within the document-conditioned task; the oracle branch is not. NERC remains a silver-labelled qualitative application case pending genuine domain-expert annotation.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/failure_and_evidence_audit.json | KEYS: reproducibility audit; protocol and NERC boundaries from claim ledger -->

## 9. Title Adjustment Options

**Preferred option:** *C2GES: Interpretable Extractive Evidence Selection for Power Grid Reliability Reports*. This is the smallest honest change to the current application-centred title: it preserves the method name, evidence-selection task, and power-grid setting while removing “Causal-Role-Aware” as a demonstrated title-level promise.

<!-- CLAIM: C2-C09 | STATUS: TITLE-NARROWED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: role claim NO-GO and manuscript implication -->

**Alternative option:** *C2GES: Budget-Aware Evidence Reranking for Power Grid Reliability Reports*. This option foregrounds the empirically supported cutoff dependence and retains the original application theme. “Budget-aware” refers to the observed \(K\)-dependent operating trade-off, not to an adaptive budget-allocation algorithm.

<!-- CLAIM: C2-C05 | STATUS: TITLE-SCOPED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: cutoff-dependent BM25 results and blanket NO-GO -->

Neither title should add “superior,” “role-enhanced,” “expert-validated,” or “human-gold power-grid benchmark.” The preferred manuscript framing is transparent evidence reranking, leakage-controlled protocol comparison, and evidence-budget behaviour, with role conditioning retained as a falsified or unsupported primary hypothesis rather than a success claim.

<!-- CLAIM: C2-C09 | STATUS: TITLE-NARROWED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: C2-C04,C2-C05,C2-C07,C2-C09 boundaries -->

## Assembly Notes and Claim Decisions

- **C2-C01:** retain the exact-title grouping result and semantic/redirect limitation.
- **C2-C02:** predicted-label is end-to-end only because training roles are grouped OOF and dev/test roles are train-only predictions.
- **C2-C03:** oracle is conditional and must carry `end_to_end=false`.
- **C2-C04:** frozen **NO-GO**; no reliable role-conditioning gain.
- **C2-C05:** frozen **NO-GO** for blanket BM25 superiority; use cutoff-specific wording.
- **C2-C06:** five-seed execution is reproducible, with 176/176 checks passed and zero failures.
- **C2-C07:** NERC remains a silver qualitative case; no quantitative domain superiority.
- **C2-C08:** resource traces exist, but general low-cost and interpretability-benefit claims remain scoped.
- **C2-C09:** remove role gain from the title-level contribution and use one of the two narrowed titles.

<!-- CLAIM: C2-C09 | STATUS: TITLE-NARROWED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: claim_decisions and manuscript_implication -->
