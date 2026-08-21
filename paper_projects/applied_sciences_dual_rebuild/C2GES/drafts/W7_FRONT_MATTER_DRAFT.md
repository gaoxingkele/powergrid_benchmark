# W7 Staging Draft: C2GES Front Matter, Introduction, and Related Work

## Title

**C2GES: Interpretable Extractive Evidence Selection for Power Grid Reliability Reports**

<!-- CLAIM: C2-C09 | STATUS: TITLE-FROZEN-NARROWED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: claim_decisions.role_conditioning_primary_claim and manuscript_implication -->

## Abstract

Technical-report review requires concise evidence packets whose selected sentences remain inspectable. We present C2GES, an interpretable extractive reranker combining query relevance, a learnable role-compatibility channel, and local positional-chain consistency. Evaluation uses a FEVER-derived, document-conditioned evidence-selection corpus—not power-grid data—with train, development, and test partitions disjoint by underlying Wikipedia document. We compare oracle-label, leakage-controlled predicted-label, and label-blind protocols over five fixed training seeds. The oracle protocol is conditional rather than end-to-end; predicted training roles are generated out of fold by document, and development/test roles come from a train-only classifier. Results are evidence-budget dependent. BM25 is stronger at \(K=1\); at \(K=3\), oracle and predicted C2GES show only tiny advantages over BM25, while label-blind does not pass the positive-effect gate. Predicted-label versus label-blind intervals cross zero, making the primary role-conditioning claim NO-GO; blanket superiority over BM25 is also NO-GO. All runs pass the frozen evidence audit. Public NERC reliability reports illustrate the application workflow, but their current question/evidence labels are agent-verified silver rather than human gold and support qualitative cases only. C2GES is therefore positioned as a transparent, reproducible reranker with cutoff-specific behaviour, not as a demonstrated role-gain method.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Decision,Primary role effect,Relative to BM25,Claim guidance -->

## Keywords

evidence selection; extractive reranking; fact verification; interpretable information retrieval; document-grouped evaluation; power-grid reliability reports; FEVER

<!-- CLAIM: C2-C09 | STATUS: TITLE-FROZEN-NARROWED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: C2 task,application,role-title boundary -->

## 1. Introduction

Engineers and analysts reviewing reliability, disturbance, and lessons-learned reports need more than a topical document. They need the exact sentences that support a finding, expose a failure mechanism, describe an impact, or record a mitigation. Sentence-level evidence packets make the connection between a question and its documentary basis inspectable, quotable, and auditable. This need is related to evidence retrieval in fact verification and query-focused extractive summarization, where a system must identify support for a specific information need rather than merely estimate whole-document salience \cite{thorne2018fever,zhong2021qmsum,vig2022exploring}.

<!-- CLAIM: C2-C09 | STATUS: APPLICATION-MOTIVATION | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: thorne2018fever,zhong2021qmsum,vig2022exploring -->

The power-grid setting makes traceability especially important. Increasing digitalisation expands both the volume of operational information and the opportunity to apply data-driven methods, while reliability analysis still requires domain-aware interpretation and defensible provenance \cite{xie2022massively,srinivasan2023artificial,ranawaka2024leveraging}. A ranking system intended for this workflow should therefore expose sentence identifiers and component scores and should distinguish a reproducible retrieval result from an unverified application annotation.

<!-- CLAIM: C2-C07 | STATUS: APPLICATION-MOTIVATION | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: xie2022massively,srinivasan2023artificial,ranawaka2024leveraging -->

Evidence selection can be approached through lexical matching, sentence embeddings, graph-based salience, or learned reranking. Extractive models have framed sentence choice as text matching, heterogeneous or topic-aware graph learning, and rank fusion \cite{zhong2020extractive,wang2020heterogeneous,cui2020enhancing,jing2021multiplex,joshi2022ranksuman}. These methods motivate combining complementary signals, but they do not remove the need to test whether each added signal contributes beyond a strong query-relevance baseline.

<!-- CLAIM: C2-C04 | STATUS: LITERATURE-CONTEXT | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: zhong2020extractive,wang2020heterogeneous,cui2020enhancing,jing2021multiplex,joshi2022ranksuman -->

C2GES is an interpretable within-document evidence reranker. It combines a fixed query-relevance score, a learnable compatibility score conditioned on a selector role, and a proximity-smoothed local-chain score through a positive additive mixture. The architecture was designed to make each candidate’s score decomposable. However, interpretability of the score decomposition is distinct from proof that role conditioning improves retrieval; the role term must earn that claim through a paired ablation and protocol comparison.

<!-- CLAIM: C2-C08 | STATUS: METHOD-SCOPED | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py | KEYS: RoleHead,MixtureParams,local_chain_scores,prediction_rows -->

This distinction is critical because a veracity role can become a source of target leakage. In the oracle-label protocol, the selector receives the human FEVER SUPPORTS or REFUTES label, which would ordinarily be unknown before fact verification. We therefore treat oracle-label as a conditional sensitivity analysis with `end_to_end=false`. The primary deployable protocols are predicted-label, in which training roles are produced by document-grouped out-of-fold prediction and development/test roles by a train-only classifier, and label-blind, in which no gold or predicted veracity is exposed.

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED-END-TO-END | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/shared_evidence_audit.json | KEYS: upstream_oof_contract,protocol provenance and gold-role isolation -->

The quantitative study uses a FEVER-derived sentence-selection corpus. FEVER is a Wikipedia fact-verification resource with human-annotated evidence \cite{thorne2018fever}; it is not a collection of power-grid reports. We rebuild the conversion into 8000 training, 1500 development, and 1500 test instances grouped by underlying Wikipedia document, yielding 745, 141, and 145 documents with zero exact overlap. The grouping corrects the experimental unit for both partitioning and document-clustered uncertainty, while retaining an explicit limitation for redirects and semantic near-duplicates.

<!-- CLAIM: C2-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped/manifest.json | KEYS: source,counts,split_strategy,unique_documents,pairwise_overlap,notes -->

Five fixed training seeds provide the canonical result. The evidence does not support the hypothesised primary role gain: at \(K=3\), predicted-label minus label-blind has a near-zero mean difference and both the seed-level and hierarchical seed/document intervals cross zero. The role-conditioning decision is consequently NO-GO. This negative result is retained as a contribution to experimental clarity, because it prevents architectural intent from being mistaken for an empirically established effect.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: effects.predicted-label_minus_label-blind.3 and claim_decisions.role_conditioning_primary_claim -->

The comparison with BM25 is likewise not uniform. BM25 is stronger at \(K=1\). At \(K=3\), oracle-label and predicted-label C2GES have tiny positive hierarchical intervals relative to BM25, but the label-blind interval includes zero. Small positive differences occur at larger cutoffs, yet the mixed pattern makes blanket superiority NO-GO. We therefore interpret \(K\) as an evidence-reading budget and report cutoff-specific operating behaviour rather than declaring a universal winner.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Relative to BM25,Claim guidance -->

The original application theme is retained through public NERC reliability reports. The current NERC question and evidence records cover causal-role-oriented review cases, but their labels are agent-rewritten and agent-verified silver candidates. They have not undergone independent human adjudication and are not used as the source of the paper’s quantitative performance claims. NERC consequently demonstrates traceable case presentation and the intended workflow, not a human-gold power-grid leaderboard.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED-QUANTITATIVE | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc/manifest.json | KEYS: status,document_count,question_count,label_provenance -->

This study makes four scoped contributions. First, it presents C2GES as a decomposable evidence reranker whose candidate traces can be audited. Second, it establishes a document-disjoint FEVER conversion and a three-protocol contract that separates oracle, predicted, and absent role information. Third, it reports a complete five-seed evaluation with document-clustered inference and preserves the role and blanket-BM25 NO-GO decisions. Fourth, it defines an honest bridge to power-grid reliability-report analysis by separating quantitative human-annotated FEVER evidence from qualitative NERC silver cases.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/failure_and_evidence_audit.json | KEYS: complete five-seed audit; contribution boundaries in CLAIM_LEDGER -->

The remainder of the article reviews fact-verification retrieval, extractive ranking, and technical-report applications; defines the data and three role protocols; describes the C2GES mixture and training objective; reports the five-seed and cutoff-dependent results; and concludes with limitations, reproducibility artifacts, and requirements for future expert-adjudicated NERC evaluation.

<!-- CLAIM: C2-C09 | STATUS: MANUSCRIPT-STRUCTURE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MANUSCRIPT_BUDGETS.md | KEYS: C2GES section plan -->

## 2. Related Work

### 2.1. Fact Verification and Evidence Retrieval

FEVER formalised large-scale claim verification with Wikipedia evidence sentences, making evidence identification a measurable stage rather than an unobserved rationale \cite{thorne2018fever}. Later work has explored multi-step evidence retrieval for misinformation detection and question answering, reflecting the broader need to assemble support across retrieval stages \cite{liao2023muser,liang2020hammer}. C2GES operates in the narrower setting where the candidate document is supplied, so it should be compared as sentence reranking rather than open-corpus fact verification.

<!-- CLAIM: C2-C02 | STATUS: LITERATURE-SCOPE | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: thorne2018fever,liao2023muser,liang2020hammer -->

This task boundary also determines what “end-to-end” means. A full fact-verification pipeline may retrieve documents, select evidence, and predict veracity, whereas the present end-to-end claim covers upstream role prediction followed by evidence-sentence selection within a supplied document. The oracle-label protocol falls outside even that scoped definition because it consumes human veracity at selection time.

<!-- CLAIM: C2-C03 | STATUS: PROHIBITED-END-TO-END | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: C2-C02 and C2-C03 task boundary -->

### 2.2. Query-Focused Extractive Selection

Extractive summarization has been formulated as sentence–document or sentence–query matching, and query-focused benchmarks show that an explicit information need changes the desired evidence packet \cite{zhong2020extractive,zhong2021qmsum,vig2022exploring}. Sentence embeddings provide a transferable semantic relevance signal, including language-agnostic embedding approaches \cite{feng2022languageagnostic}. C2GES uses query relevance as one channel but evaluates exact evidence identifiers rather than summary fluency or coverage alone.

<!-- CLAIM: C2-C08 | STATUS: LITERATURE-CONTEXT | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: zhong2020extractive,zhong2021qmsum,vig2022exploring,feng2022languageagnostic -->

Graph-based extractive systems model sentence relations, topical structure, discourse, or multiplex connections \cite{wang2020heterogeneous,cui2020enhancing,jing2021multiplex,liu2021unsupervised}. C2GES uses a much lighter positional-neighbour smoothing term. It does not infer a physical causal graph, structural intervention, or event direction, and the term “local chain” should be read as a transparent ranking prior rather than a causal-identification claim.

<!-- CLAIM: C2-C08 | STATUS: METHOD-SCOPED | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: wang2020heterogeneous,cui2020enhancing,jing2021multiplex,liu2021unsupervised -->

### 2.3. Learned and Language-Model Reranking

Learned rerankers can model query–candidate interactions more directly than independent embedding similarity, while recent language-model work studies pairwise, setwise, and self-calibrated listwise ranking \cite{qin2024pairwise,zhuang2024setwise,ren2025selfcalibrated}. These approaches expand the accuracy–cost design space but also introduce model, endpoint, and prompting dependencies. The present study focuses on a lightweight decomposable reranker and treats comparisons with more complex rerankers as protocol-matched baselines, not as evidence that transparency automatically produces higher accuracy.

<!-- CLAIM: C2-C08 | STATUS: LITERATURE-CONTEXT | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: qin2024pairwise,zhuang2024setwise,ren2025selfcalibrated -->

BM25 remains an important lexical operating point because it is deterministic, inexpensive to reproduce, and often competitive when lexical overlap is informative. Our five-seed result reinforces the need to report it at every evidence budget: it leads at \(K=1\), while several C2GES comparisons become slightly positive at larger \(K\). This cutoff dependence argues for a Pareto-style or budget-specific presentation instead of using BM25 only as a baseline to be surpassed.

<!-- CLAIM: C2-C05 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/five_seed_aggregate.json | KEYS: effects against BM25 and blanket_superiority decision -->

### 2.4. Role Information, Causal Language, and Negative Evidence

Role or relation information is attractive when superficially similar sentences answer different questions. Causal-reasoning and explanation datasets also encourage explicit distinctions among causes, consequences, and supporting rationales \cite{feder2022causal,du2022ecare}. However, a role label can leak the target or duplicate cues already present in the query. C2GES therefore compares oracle, leakage-controlled predicted, and label-blind inputs and allows the role hypothesis to fail under a prespecified paired decision.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: feder2022causal,du2022ecare; experimental decision in W4 aggregate -->

Negative findings are particularly informative for additive architectures: a nonzero learned weight or a component’s intended semantic meaning does not demonstrate incremental utility. In the present experiment, the role-conditioned and role-blind variants are statistically unresolved at the primary cutoff. The contribution is therefore the controlled test and transparent NO-GO decision, not a post hoc reinterpretation of a tiny positive mean.

<!-- CLAIM: C2-C04 | STATUS: NO-GO-FROZEN | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/W4_C2_FIVE_SEED_REPORT.md | KEYS: Primary role effect at K=3 and Claim guidance -->

### 2.5. AI for Power-Grid Documentation

Power-grid digitalisation and AI research address forecasting, control, anomaly detection, cyber-physical risk, and decision support \cite{xie2022massively,srinivasan2023artificial,madabhushi2023survey}. Reliability-report evidence selection is complementary: it organises the documentary basis for engineering review rather than estimating system state or solving power flow. This narrower applied objective motivates inspectable sentence outputs and conservative claims about domain validation.

<!-- CLAIM: C2-C07 | STATUS: APPLICATION-MOTIVATION | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: xie2022massively,srinivasan2023artificial,madabhushi2023survey -->

Existing public NERC reports provide realistic language and report structure, but source authenticity does not make derived question–evidence labels expert gold. Our application cases retain official report provenance while disclosing that the current labels are silver. This separation between authentic documents and non-human annotations is necessary before C2GES can be evaluated as a quantitative power-grid-domain system.

<!-- CLAIM: C2-C07 | STATUS: PROHIBITED-QUANTITATIVE | ARTIFACT: data/public_datasets/reliability_reports/c2ges_nerc_reports/metadata/c2ges_nerc_report_manifest.json | KEYS: official report sources; label provenance in agent_audit manifest -->

### 2.6. Positioning of This Study

The study sits between fact-verification evidence selection, query-focused extraction, and technical-report review. Its differentiating elements are not a claimed universal ranking advantage or a confirmed role effect. They are the combination of an inspectable scoring interface, a true document-grouped conversion, explicit oracle/predicted/blind protocols, five-seed document-clustered evaluation, and a power-grid case-study boundary that does not promote silver labels to human gold.

<!-- CLAIM: C2-C06 | STATUS: ELIGIBLE-E4 | ARTIFACT: paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/failure_and_evidence_audit.json | KEYS: five-seed evidence completeness and claim boundaries -->

## Verified Citation Claim–Key Map

| Literature claim | Citation keys used | Verification artifact |
|---|---|---|
| FEVER supplies Wikipedia fact-verification claims with annotated evidence | `thorne2018fever` | `references_applsci.bib` DOI entry |
| Query-focused and extractive selection depend on the information need | `zhong2020extractive`, `zhong2021qmsum`, `vig2022exploring` | `references_applsci.bib` DOI entries |
| Graph-based extraction models sentence or topic relations | `wang2020heterogeneous`, `cui2020enhancing`, `jing2021multiplex`, `liu2021unsupervised` | `references_applsci.bib` DOI entries |
| Multi-step evidence retrieval is studied beyond single-stage ranking | `liao2023muser`, `liang2020hammer` | `references_applsci.bib` DOI entries |
| Recent LLM reranking includes pairwise, setwise, and self-calibrated listwise approaches | `qin2024pairwise`, `zhuang2024setwise`, `ren2025selfcalibrated` | `references_applsci.bib` verified DOI entries |
| Power-grid AI and digitalisation motivate traceable applied information systems | `xie2022massively`, `srinivasan2023artificial`, `ranawaka2024leveraging`, `madabhushi2023survey` | `references_applsci.bib` DOI entries |
| Causal NLP and explainable causal-reasoning datasets motivate careful role terminology | `feder2022causal`, `du2022ecare` | `references_applsci.bib` DOI entries |

<!-- CLAIM: C2-C06 | STATUS: CITATION-MAPPED | ARTIFACT: paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib | KEYS: all cited keys in W7 draft -->

## Assembly Boundary

The main manuscript must remove any older abstract, introduction, or related-work sentence that claims a supported role gain, universal superiority over BM25, quantitative NERC validation, or human-gold NERC annotations. It must also keep FEVER identified as Wikipedia fact-verification data rather than power-grid data. Citations should be copied only with the keys listed above and rechecked during final bibliography assembly.

<!-- CLAIM: C2-C09 | STATUS: TITLE-FROZEN-NARROWED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: C2-C03,C2-C04,C2-C05,C2-C07,C2-C09 -->
