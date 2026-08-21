# W5 Staging Draft: C2GES Materials, Data, Methods, Protocol, and Statistics

**Status.** This evidence-bound draft is intended for later assembly into an *Applied Sciences* manuscript. It uses only the rebuilt document-grouped protocol and does not transfer sample counts, confidence intervals, or performance claims from the superseded leakage-prone evaluation. Role-effect, BM25-comparison, efficiency, and title claims remain conditional on the frozen five-seed decision.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: five-seed role-effect gate -->

## 2. Materials and Data

### 2.1. Study Design and Evidence Boundary

We evaluate C2GES as a sentence-level evidence selector under three parallel role-information protocols: oracle-label, predicted-label, and label-blind. All protocols use the same claims, candidate sentences, split assignments, selector architecture, metric definitions, and evaluation cutoffs. Their only intended difference is the provenance of the role supplied to the selector. This alignment permits paired comparisons without changing the candidate pool.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: PROTOCOLS and shared selector implementation -->

The oracle-label protocol exposes the human FEVER veracity label to the selector. It is therefore a conditional role-information experiment and an upper-bound diagnostic, with `end_to_end=false`; it is not a standard end-to-end evidence-selection result. The predicted-label and label-blind protocols are the two end-to-end variants: the former consumes a leakage-controlled upstream prediction, whereas the latter supplies a constant unknown role and exposes neither gold nor predicted veracity.

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: oracle reporting constraint and end_to_end=false -->

The complete FEVER conversion contains 8000 training, 1500 development, and 1500 test instances. The split is grouped by normalized underlying Wikipedia title/document identifier, yielding 745, 141, and 145 unique documents in the three partitions, respectively, with zero exact document overlap. These document groups replace claim identifiers as the unit of partitioning and inference.

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped/manifest.json | KEYS: counts,split_grouping_key,unique_documents,pairwise_overlap -->

Exact document disjointness does not prove semantic independence. The title audit normalizes URL encoding, Unicode, case, underscores, spaces, punctuation, leading articles, and one trailing disambiguator; it screened 233,515 cross-split title pairs, found no exact normalized alias, and resolved the sole high-similarity candidate as a distinct entity. Redirect aliases, shared passages, semantic near-duplicates, and entity-level relationships may remain and are retained as limitations.

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/shared_evidence_audit.json | KEYS: title_alias_review_complete and scope caveat -->

### 2.2. FEVER Evidence-Selection Corpus

Each converted instance comprises a claim, an underlying Wikipedia document, an ordered candidate-sentence list, a FEVER veracity label in `{SUPPORTS, REFUTES}`, and one or more annotated evidence-sentence identifiers. The selector ranks sentences within the supplied document; it does not perform open-corpus page retrieval or predict final claim veracity. Consequently, the primary task is document-conditioned evidence selection rather than complete fact verification.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: load_docs,build_examples,evidence_sentence_ids -->

FEVER evidence annotations remain evaluation targets in all three protocols. Gold evidence is never used as an input feature, role-prediction feature, candidate-score feature, or inference-time stopping signal. Gold veracity enters the selector only in the explicitly labelled oracle protocol and is otherwise reserved for upstream-label evaluation and post hoc role-stratified analysis.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/shared_evidence_audit.json | KEYS: upstream_oof_contract and protocol isolation checks -->

### 2.3. Predicted-Role Construction

The predicted-label workflow uses claim text as the upstream classifier input. Training-role predictions follow a document-grouped OOF scheme implemented with `StratifiedGroupKFold`, grouping every fold by the underlying Wikipedia document. Thus each training instance receives a role prediction from a classifier that was not fitted on any claim from its document. A final upstream classifier fitted only on the training partition produces roles for development and test.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/upstream_labels/provenance.json | KEYS: features,folds,train_predictions,dev_test_predictions -->

The upstream stage is part of the predicted-label system rather than an external convenience input. Its accuracy, balanced accuracy, macro-F1, confusion matrix, and per-instance predicted roles must accompany downstream selector results. Prediction errors are preserved through the pipeline instead of being replaced with oracle labels, so the resulting score represents the deployed two-stage workflow.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/upstream_labels/metrics.json | KEYS: upstream metrics and train_prediction_protocol -->

### 2.4. NERC Application Material

The local NERC collection contains 40 public reliability and event-report PDFs with a manifest linking document identifiers, report titles, official source pages, URLs, and local files. A separate candidate annotation set contains five causal-role questions per document—trigger event, root cause, propagation or response, impact, and mitigation—for 200 questions and 608 referenced evidence identifiers.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: document_count,questions_per_document,question_count,evidence_id_count,role_counts -->

The NERC question and evidence labels are agent-rewritten and agent-verified silver candidates. They have not been converted into an independently human-adjudicated test set, even when an automated verifier repaired unsupported wording or evidence identifiers. Accordingly, NERC is restricted to qualitative case analysis, trace inspection, and annotation-workflow demonstration; it cannot support quantitative domain-superiority or human-gold claims.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: status,label_provenance,independent_verifier_summary -->

Any future quantitative NERC experiment requires a frozen annotation manual, independent domain reviewers, recorded disagreements, adjudication, agreement statistics, and a sealed evaluation subset not used during method development. Until those artifacts exist, numerical NERC outputs must remain supplementary diagnostics and must not determine model selection, the primary abstract claim, or the article title.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: NERC human-review gate -->

## 3. Proposed C2GES Method

### 3.1. Task Formulation

For claim \(q_i\) and its candidate sentences \(D_i=\{s_{ij}\}_{j=1}^{n_i}\), C2GES assigns each sentence a scalar score and returns the \(K\) highest-ranked sentence identifiers. Let \(E_i\subseteq D_i\) be the annotated evidence set and \(r_i\) the selector role obtained under one of the three protocols. The role is an intervention input; \(E_i\) is used only by the training objective and offline evaluator.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: build_examples,prediction_rows,evidence_f1 -->

The sentence and claim encoder produces \(h_{ij}=f(s_{ij})\) and \(h_i^q=f(q_i)\). The frozen pilot uses `sentence-transformers/all-MiniLM-L6-v2`, whose snapshot and file hash are recorded in the execution manifest. Model identity is treated as configuration rather than an unreported implementation detail.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_FREEZE_MANIFEST.json | KEYS: encoder.model_id,snapshot_ref,sha256 -->

### 3.2. Query-Relevance Component

The query score combines normalized semantic cosine similarity and normalized within-document TF–IDF cosine similarity:

\[
Q_{ij}=\operatorname{norm}\!\left[
\tfrac{1}{2}\operatorname{norm}(\cos(h_{ij},h_i^q))+
\tfrac{1}{2}\operatorname{norm}(\operatorname{tfidf}(s_{ij},q_i))
\right],
\]

where `norm` is min–max normalization within the candidate document and maps a constant vector to zeros. The fixed one-half coefficients define the implemented query channel and are not tuned on the test partition.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: build_examples Q and minmax -->

### 3.3. Learnable Role-Compatibility Component

For role embedding \(e(r_i)\), the role head concatenates sentence, claim, and role representations and applies a two-layer multilayer perceptron:

\[
R_{ij}=\sigma\!\left(
W_2\,\operatorname{ReLU}\left[W_1(h_{ij}\oplus h_i^q\oplus e(r_i))+b_1\right]+b_2
\right).
\]

The implementation uses a 256-unit hidden layer and dropout of 0.1. In the label-blind protocol, \(r_i\) is the constant unknown role; in the predicted-label protocol it is the OOF or train-only upstream output; and only the conditional oracle protocol uses FEVER veracity.

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: RoleHead,protocol_role,PROTOCOLS -->

The existence of this role head does not demonstrate a useful role effect. The single-seed pilot produced paired document-cluster confidence intervals that crossed zero for cross-protocol comparisons at every evaluated \(K\). The role contribution therefore remains `PENDING-EVIDENCE` until all five frozen seeds are complete and jointly analysed; if the null pattern persists, the role novelty must be subordinated or removed.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/W3_C2_PILOT_REPORT.md | KEYS: cross-protocol bootstrap and five-seed gate -->

### 3.4. Local-Chain Component

The local-chain score smooths query salience over sentence position. With \(u_{i\ell}=\operatorname{norm}(\cos(h_{i\ell},h_i^q))\), it is

\[
G_{ij}=\operatorname{norm}\!\left[
\frac{\sum_{\ell\ne j}\exp(-|j-\ell|/3)u_{i\ell}}
{\sum_{\ell\ne j}\exp(-|j-\ell|/3)}
\right].
\]

This component represents proximity-smoothed salience rather than an identified causal graph. Calling it a local chain describes its positional consistency prior; it does not imply that causal direction or event links were recovered from text.

<!-- CLAIM: C2-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: local_chain_scores -->

### 3.5. Positive Mixture and Learning Objective

The final sentence score is

\[
S_{ij}=w_QQ_{ij}+w_RR_{ij}+w_GG_{ij},\qquad
w_m\ge 0,\quad \sum_m w_m=1.
\]

Mixture parameters are obtained by softplus transformation, normalization, and blending with registered floors \((0.35,0.25,0.05)\) for the query, role, and local-chain channels. The resulting weights are renormalized. These floors make component presence explicit but can constrain the learned optimum, so a no-floor sensitivity analysis is required before interpreting the fitted weights.

<!-- CLAIM: C2-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: MixtureParams,floors,weights -->

For positive evidence sentences \(P_i\) and remaining candidates \(N_i\), define the pairwise softplus loss

\[
\mathcal{L}_{\mathrm{rank},i}=
\frac{1}{|P_i||N_i|}\sum_{p\in P_i}\sum_{n\in N_i}
\log\!\left(1+\exp(S_{in}-S_{ip})\right).
\]

The implemented objective adds direct role-head contrast supervision:

\[
\mathcal{L}_i=\mathcal{L}_{\mathrm{rank},i}+0.5\,
\mathcal{L}_{\mathrm{rank},i}^{(R)}.
\]

The second term applies the same positive–negative ranking loss to \(R_{ij}\). A no-role ablation, no-chain ablation, no-floor variant, pointwise-loss alternative, and frozen-encoder comparison should be evaluated under identical document groups and five training seeds.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: pairwise_loss,role_contrast_loss,train_model -->

### 3.6. Inference and Interpretability

At inference time, component scores and their weighted sum are computed for every candidate sentence, sorted in descending order, and truncated at \(K\). The prediction ledger retains selected identifiers, gold identifiers for evaluator-only use, selector-role provenance, candidate-level scores, and configuration identifiers. Because each channel and mixture weight is inspectable, the system can expose why a sentence was promoted; whether this constitutes a stable low-cost interpretability advantage remains a five-seed and case-audit question.

<!-- CLAIM: C2-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: prediction_rows,candidate_scores,mixture_weights -->

#### Proposed Algorithm 1. Leakage-Controlled C2GES Training and Evaluation

```text
Input: document-grouped train/dev/test; protocol p; seed z; cutoffs K
Audit that no underlying Wikipedia document crosses a split.
If p is predicted-label:
    partition training documents into grouped folds;
    predict each held-out training fold from all other training folds;
    fit the final upstream classifier on training documents only;
    predict development and test roles; freeze role predictions and hash.
Else if p is label-blind:
    assign the constant unknown role to every instance.
Else:
    expose FEVER veracity and mark the run oracle/conditional/end_to_end=false.
Encode claims and candidate sentences; construct Q, R, and G components.
Train the role head and positive mixture on training data only.
Select the checkpoint by the frozen development criterion.
For every test instance and K, store ranked IDs and component traces.
Audit complete protocol × seed × item × K coverage and immutable hashes.
Compute metrics and paired bootstrap intervals clustered by source document.
Output: predictions, upstream metrics, resources, provenance, and audit report.
```

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/shared_evidence_audit.json | KEYS: 47-check execution and OOF contract -->

## 4. Experimental Protocol

### 4.1. Frozen Runs and Comparators

The confirmatory protocol uses five fixed training seeds and reports \(K\in\{1,3,5,10\}\). Learned systems are trained independently per seed; deterministic baselines receive one frozen run plus a reproducibility rerun. All methods must rank the same per-instance candidate sentences and be evaluated over the same 1500 test instances and 145 source-document clusters.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: C2-M01 replication,eval K,cluster_unit -->

The main comparator interface includes Lead-\(K\), TF–IDF, BM25, TextRank or LexRank, SBERT similarity, a cross-encoder MiniLM reranker, a BGE reranker, a query-only learned selector, and C2GES. Baseline additions must not change the candidate pool, split, evidence targets, or metric implementation. Model snapshots, retrieval parameters, and hardware must be recorded for every result-bearing run.

<!-- CLAIM: C2-C05 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: C2-M02 conditions and reproducibility requirements -->

BM25 is a prespecified primary baseline, but the manuscript will not claim broad superiority. The one-seed diagnostic showed a \(K\)-dependent pattern, including a significant BM25 advantage at \(K=1\) and nonsignificant differences at \(K=3\) and \(K=5\). Canonical conclusions must use the completed five-seed aggregation and be phrased as cutoff-specific comparisons or a Pareto diagnosis.

<!-- CLAIM: C2-C05 | STATUS: PROHIBITED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/W3_C2_PILOT_REPORT.md | KEYS: BM25 comparison boundary -->

### 4.2. Metrics

For predicted set \(\hat E_i^{(K)}\) and annotated evidence \(E_i\), per-instance precision, recall, and F1 are

\[
P_i@K=\frac{|\hat E_i^{(K)}\cap E_i|}{K},\quad
R_i@K=\frac{|\hat E_i^{(K)}\cap E_i|}{|E_i|},\quad
F_{1,i}@K=\frac{2P_i@K R_i@K}{P_i@K+R_i@K},
\]

with zero assigned when the denominator is zero. We report macro evidence F1 and recall at each \(K\), plus MRR and nDCG where their relevance and tie conventions are frozen. Role-stratified results use the gold label only as an analysis stratum, never as selector input outside the oracle protocol.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: C2-M01 primary_metrics and K protocol -->

Efficiency fields include training wall time, inference wall time, peak resident memory, model size, encoder calls, throughput, and hardware. The existing pilot sampled process-tree RSS at 0.2-second intervals and did not measure sub-interval peaks or GPU memory. Final efficiency aggregation must retain those measurement limitations and must not infer a low-cost advantage from one seed.

<!-- CLAIM: C2-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/W3_C2_PILOT_REPORT.md | KEYS: runtime,resource measurement limitations,five-seed gate -->

### 4.3. Statistical Analysis

All resampling and paired tests use the underlying Wikipedia document as the cluster unit. For methods \(A\) and \(B\), define the cutoff-specific mean difference

\[
\Delta_{A-B}(K)=\frac{1}{N}\sum_{i=1}^{N}
\left[F_{1,i}^{A}@K-F_{1,i}^{B}@K\right].
\]

Bootstrap replicates sample the 145 test documents with replacement and include all instances belonging to each sampled document. The 2.5th and 97.5th percentiles form the paired document-cluster 95% confidence interval.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: bootstrap_delta cluster_unit and CI quantiles -->

Prespecified families cover the three role-information protocols, C2GES versus the primary baseline, and component ablations across \(K\). The final analysis reports effect sizes, paired cluster intervals, raw paired-test p-values, Holm-adjusted p-values, cluster counts, and seed-level values. Seed selection based on test performance is prohibited; missing runs remain visible and block the canonical table unless a documented infrastructure-wide rerun is applied uniformly.

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: C2-M01/C2-M02 tests,Holm,five seeds -->

The role-effect decision is made from the complete five-seed result, not from a favourable seed or cutoff. A role-related conclusion requires directionally stable effects and uncertainty compatible with the preregistered threshold; otherwise, the paper will present role conditioning as a tested but unsupported mechanism and shift the contribution toward leakage-controlled protocol design, traceability, or efficiency only where evidence permits.

<!-- CLAIM: C2-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: C2GES go/no-go and title decision -->

## 5. Reproducibility and Data Governance

The one-seed full-corpus pilot completed the oracle-label, predicted-label, and label-blind protocols with zero recorded failures and passed 47 of 47 shared evidence checks. This establishes execution and audit readiness for seed 2026, not a five-seed scientific conclusion. The remaining frozen seeds must complete before result tables or title claims are released.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/W3_C2_PILOT_REPORT.md | KEYS: scope,47 checks,zero failures,one-seed boundary -->

The frozen run configuration specifies the document-grouped corpus, 8000/1500/1500 limits, four epochs, learning rate 0.001, CPU execution, training cutoff 3, evaluation cutoffs 1/3/5/10, 2000 bootstrap samples, document-overlap rejection, and overwrite protection. The corpus SHA-256 is `683694b87a9842e54eb48aad1aaff85f1105e150f10e9e43fa7efe915a36af20`, and the predicted-role ledger is separately hashed.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_FREEZE_MANIFEST.json | KEYS: base_run_config,dataset_corpus_sha256,predicted_labels_sha256 -->

Each releaseable run must preserve the seed, protocol, split and data hashes, code hashes, encoder snapshot, upstream-role hash, configuration, environment, checkpoint, prediction ledger, component traces, metric tables, resource usage, stdout/stderr, and audit status. Resume operations must not overwrite completed evidence, and a canonical aggregation must verify complete protocol-by-seed-by-instance-by-cutoff coverage.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/shared_evidence_audit.json | KEYS: provenance completeness,hash inventory,Cartesian checks -->

The Data Availability Statement should distinguish the FEVER-derived document-grouped conversion, reproducible split and role-prediction metadata, model artifacts, public NERC source PDFs, and non-publication-grade silver annotations. Source licenses and attribution obligations must be checked before redistributing text or derived records. NERC silver labels should be released only with their agent provenance and explicit non-human status.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED | ARTIFACT: data/public_datasets/reliability_reports/c2ges_nerc_reports/metadata/c2ges_nerc_report_manifest.json | KEYS: official source mapping and local PDF provenance -->

## Proposed Table Interfaces

### Table 1. Corpus and Split Audit

| Partition | Instances | Underlying documents | Grouping key | Cross-partition overlap | Evidence role |
|---|---:|---:|---|---:|---|
| Train | 8000 | 745 | Normalized underlying Wikipedia title/document ID | 0 | Training and grouped OOF roles |
| Development | 1500 | 141 | Same | 0 | Checkpoint selection; roles from train-only classifier |
| Test | 1500 | 145 | Same | 0 | Frozen evaluation; roles from train-only classifier |

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped/manifest.json | KEYS: split audit -->

### Table 2. Three-Protocol Contract

| Protocol | Selector role input | Train-role provenance | Dev/test provenance | End-to-end | Reporting label |
|---|---|---|---|---|---|
| Oracle-label | FEVER veracity | Gold | Gold | No | Conditional oracle upper bound |
| Predicted-label | Upstream prediction | Document-grouped OOF | Train-only classifier | Yes | Primary deployed workflow |
| Label-blind | Constant unknown | Constant unknown | Constant unknown | Yes | Primary role-free workflow |

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/C2GES/figures/frameworks/captions.md | KEYS: c2_f01_three_protocols contract -->

### Table 3. Main Five-Seed Results — Reserved Interface

| Method/protocol | Seeds complete | F1@1 | F1@3 | F1@5 | F1@10 | Recall@K | MRR | nDCG@K |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C2GES oracle-label | **PENDING FIVE SEEDS** | — | — | — | — | — | — | — |
| C2GES predicted-label | **PENDING FIVE SEEDS** | — | — | — | — | — | — | — |
| C2GES label-blind | **PENDING FIVE SEEDS** | — | — | — | — | — | — | — |
| BM25 | Frozen reruns pending aggregation | — | — | — | — | — | — | — |

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: C2-M01 canonical table gate -->

### Table 4. Upstream Predicted-Role Interface

| Split | Prediction scheme | Accuracy | Balanced accuracy | Macro-F1 | Confusion matrix artifact |
|---|---|---:|---:|---:|---|
| Train | Document-grouped OOF | From immutable artifact | From immutable artifact | From immutable artifact | Required |
| Development | Classifier fitted on train only | From immutable artifact | From immutable artifact | From immutable artifact | Required |
| Test | Classifier fitted on train only | From immutable artifact | From immutable artifact | From immutable artifact | Required |

<!-- CLAIM: C2-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/upstream_labels/metrics.json | KEYS: upstream reporting interface -->

### Table 5. Paired Statistical Contrasts

| Family | Contrast | K | Five-seed mean delta | Document-cluster 95% CI | Raw p | Holm p | Decision |
|---|---|---:|---:|---|---:|---:|---|
| Role source | Oracle − predicted | 1/3/5/10 | — | — | — | — | Pending |
| Role source | Predicted − blind | 1/3/5/10 | — | — | — | — | Pending |
| Baseline | Predicted − BM25 | 1/3/5/10 | — | — | — | — | Pending |
| Ablation | Full − no-role | 1/3/5/10 | — | — | — | — | Pending |

<!-- CLAIM: C2-C04 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/experiment_registry.json | KEYS: paired cluster tests and Holm interface -->

### Table 6. NERC Evidence Status

| Material | Count | Provenance | Permitted use | Prohibited use | Human-review gate |
|---|---:|---|---|---|---|
| Public source reports | 40 documents | Official NERC PDFs and manifest | Application context and traceable source inspection | Copyright-unchecked redistribution | Source/license review |
| Causal-role candidates | 200 questions; 608 evidence IDs | Agent-rewritten and agent-verified silver | Qualitative cases and annotation workflow | Human-gold benchmark or quantitative superiority | Independent domain review and adjudication |

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: NERC evidence status -->

## Figure and Diagram Interfaces

1. **Figure 1, three-protocol flow:** reuse the existing protocol diagram and caption; visually mark oracle as conditional and the other two branches as end-to-end.
2. **Figure 2, grouped split and OOF roles:** show atomic document assignment, grouped training folds, and train-only development/test prediction.
3. **Figure 3, C2GES mixture:** claim/sentence encoder feeding query, role, and local-chain channels; gold evidence enters only the loss/evaluator.
4. **Figure 4, audit and statistics:** prediction ledger → completeness/hash audit → document-cluster resampling → corrected decisions.
5. **Figure 5, five-seed role effects:** reserved forest or seed-distribution plot; render only after all frozen seeds pass audit.
6. **Figure 6, cutoff-specific baseline trade-off:** reserved \(K\)-sensitivity and efficiency Pareto plot; do not title it “superiority.”

<!-- CLAIM: C2-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/C2GES/figures/frameworks/artifact_manifest.json | KEYS: existing framework figure provenance and pending result figures -->

## Reference Placeholders (Metadata Must Be Verified)

- `[REF-FEVER]`: canonical FEVER dataset paper and dataset license/source page.
- `[REF-EVIDENCE-SELECTION]`: primary evidence-sentence selection or fact-verification retrieval work.
- `[REF-BM25]`: original or authoritative BM25 reference.
- `[REF-SBERT]`: canonical Sentence-BERT paper for the frozen encoder family.
- `[REF-CROSS-ENCODER]`: primary cross-encoder reranking reference.
- `[REF-BGE]`: official BGE reranker paper or model report.
- `[REF-OOF-GROUPED]`: methodological reference for grouped cross-fitting/out-of-fold prediction.
- `[REF-CLUSTER-BOOTSTRAP]`: statistical reference for paired cluster bootstrap inference.
- `[REF-HOLM]`: original Holm family-wise correction.
- `[REF-NERC-SOURCES]`: official NERC reports and use/attribution terms.
- `[REF-MDPI-DATA]`: current MDPI/*Applied Sciences* data-availability guidance.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: reference acquisition and reproducibility plan -->

## Pending-Evidence and Prohibited-Claim Register

- **C2-C01 — ELIGIBLE-DIAGNOSTIC:** Report exact-title document disjointness with the redirect/content/semantic-near-duplicate limitation.
- **C2-C02 — ELIGIBLE-DIAGNOSTIC:** Treat OOF/train-only predicted roles and upstream errors as part of the end-to-end workflow.
- **C2-C03 — PROHIBITED:** Never present oracle-label as end-to-end; label it conditional with `end_to_end=false`.
- **C2-C04 — PENDING-EVIDENCE:** Role effects require the complete five-seed decision at all registered cutoffs.
- **C2-C05 — PROHIBITED:** Do not claim broad superiority over BM25; report cutoff-specific evidence after five-seed aggregation.
- **C2-C06 — ELIGIBLE-DIAGNOSTIC:** The 47-check seed-2026 run establishes reproducible pilot execution only.
- **C2-C07 — PROHIBITED:** NERC agent-verified silver cannot be represented as a human gold standard or quantitative domain proof.
- **C2-C08 — PENDING-EVIDENCE:** Interpretability and low-cost trade-off claims require five-seed resources, stable weights, and case audit.
- **C2-C09 — PENDING-EVIDENCE:** Freeze the final role-related title only after the five-seed role-effect decision.

<!-- CLAIM: C2-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: complete C2 claim boundary -->
