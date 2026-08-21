# Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports

## Material Passport and Round-1 Boundary

- Draft purpose: section-complete evidence-aligned manuscript draft for MDPI *Applied Sciences*.
- Primary quantitative source: frozen offline run `C2GES-NERC-FORMAL-v0.1-20260808`, Run 01 and byte-identical Run 02 reproduction.
- Primary domain corpus: 40 locally registered public NERC PDFs; 28 included after deterministic section-boundary screening, with 12 development and 16 test reports.
- Primary reference: the official Executive Summary extracted from each included report.
- Main operating point: five extracted sentences per report.
- Machine-label boundary: five-role evidence records are machine-verified silver candidates. They are neither human nor domain-expert gold.
- Implementation boundary: the current method uses a deterministic typed sentence graph, weighted-degree graph signal, leave-one-node-out graph intervention, and constrained extractive selection. It does not implement a GNN, T5 counterfactual generator, structural causal model, or physical power-system simulator.
- Citation boundary: citation keys below already occur in the verified bibliography of the current Applied Sciences manuscript. No new bibliography entry is proposed in this round.

## Abstract

Power-grid reliability reports contain event descriptions, causes, propagation paths, impacts, and mitigation actions that are difficult to retain in a short extractive summary. This study presents C²GES, an offline causal- and counterfactual-graph-enhanced extractive summarization method for public power-grid reliability reports. The implemented method assigns sentence-level causal-role scores, constructs a typed directed proxy graph, measures deterministic counterfactual sensitivity as the loss of graph causal flow after removing a sentence node, and selects sentences under length, causal-function coverage, redundancy, and source-order constraints. A leakage-controlled benchmark was constructed from 40 public North American Electric Reliability Corporation reports. Twenty-eight reports with extractable official Executive Summaries were retained and split by document hash into 12 development and 16 test reports. Six methods were evaluated on identical candidate sentences and a five-sentence budget: Lead, Centroid, TextRank, Role, Graph without counterfactual sensitivity, and full C²GES. Full C²GES obtained ROUGE-1/2/L F1 scores of 0.2608/0.0934/0.1323. Its ROUGE-1 difference was +0.0388 over Lead (95% report-level bootstrap interval [0.0136, 0.0663]) and +0.0390 over TextRank ([0.0070, 0.0782]). However, Centroid achieved the highest observed ROUGE-2 and ROUGE-L, while Graph without counterfactual sensitivity achieved the highest observed ROUGE-1. Thus, the experiment supports a limited improvement over two lightweight baselines on ROUGE-1, but it does not establish that the counterfactual component is effective or that C²GES is broadly superior. Two independent executions produced byte-identical predictions, aggregate metrics, and bootstrap outputs. The results define a reproducible domain benchmark and an auditable method baseline while leaving semantic baselines, strict one-factor counterfactual ablation, and expert validation as necessary next steps.

**Keywords:** extractive summarization; causal event graph; counterfactual intervention; power-grid reliability reports; NERC; reproducible evaluation

## 1. Introduction

Power-grid incident, disturbance, maintenance, and lessons-learned reports record more than isolated facts. Engineers often need the sequence that connects a condition or root cause to an initiating event, propagation or system response, operational impact, and corrective action. A short summary that retains equipment names and impact quantities but breaks those connections may be lexically relevant while remaining of limited use for root-cause review. This motivates an extractive setting in which selected sentences remain traceable to stable source identifiers and can be inspected against the official report.

Evidence selection and query-focused summarization provide useful foundations for this setting. FEVER established sentence-level evidence retrieval as an independently assessable task 
\cite{thorne2018fever}; query-focused summarization similarly conditions selection on a specified information need rather than only global topical salience \cite{zhong2021qmsum,vig2022exploring,zhong2020extractive}. These lines of work show the value of an explicit selection ledger. They do not, by themselves, guarantee coverage of a technical report's cause--event--impact--mitigation structure.

Graph-based extractive methods address document structure by representing sentences and their relations before ranking \cite{wang2020heterogeneous,cui2020enhancing,jing2021multiplex}. Causal NLP provides a distinct perspective by asking whether textual evidence encodes directional or intervention-relevant relations rather than association alone \cite{feder2022causal,du2022ecare}. Combining the two ideas is attractive for reliability-report summarization, but the strength of the resulting claim must follow the implementation. The method evaluated here uses an explicit typed proxy graph and deterministic graph intervention. It does not infer a structural causal model, estimate physical causal effects, or learn graph representations with a GNN.

The original C²GES concept proposed a substantially broader neural architecture and a new manually annotated power-grid corpus. Those claims are not carried into this study because the corresponding dataset, GNN/T5 implementation, expert adjudication, and reported performance values are not present in the audited assets. Instead, the present article retains the original application question and title while grounding the method in executable code, frozen public data, complete prediction ledgers, and reproduced outputs. This changes the contribution from a claimed neural state of the art to an auditable first benchmark of deterministic causal-graph constraints for domain extractive summarization.

The domain evaluation uses public NERC reports as authentic technical documents \cite{nercEventAnalysis,nerc2015qualityreport}. Reports are included only when an official Executive Summary can be separated from the candidate body using recorded section-boundary rules. The official summary is the reference; machine-produced five-role evidence records are used only as silver graph input and a role-coverage diagnostic. They are never described as independent expert annotations. This separation is important because machine agreement cannot validate the same causal structure supplied to the selector.

This work makes four scoped contributions:

1. It constructs a hash-defined extractive-summarization benchmark from public NERC reports, retaining every inclusion or exclusion reason and identifying the official Executive Summary as the reference provenance.
2. It implements a deterministic C²GES method core comprising a typed sentence-level causal proxy graph, structural node/edge interventions, graph-flow counterfactual sensitivity, and constrained selection with causal-function coverage and redundancy control.
3. It evaluates six offline conditions on the same 16 frozen test reports and five-sentence budget, with report-level paired bootstrap uncertainty, full prediction ledgers, code/data/runtime hashes, and an independent identical reproduction.
4. It reports both favorable and unfavorable results: full C²GES improves observed ROUGE-1 over Lead and TextRank, but does not exceed Centroid on ROUGE-2/ROUGE-L or Graph without counterfactual sensitivity on ROUGE-1.

The remainder of the article reviews related work, defines the benchmark and implemented method, presents the frozen evaluation, and discusses what the current results do and do not establish.

## 2. Related Work

### 2.1. Extractive and Query-Focused Summarization

Extractive summarization selects source sentences rather than generating new text, retaining a direct link between output and source evidence. Matching-based methods, iterative ranking, and unsupervised graph objectives offer transparent baselines for this task \cite{zhong2020extractive,bi2021aredsum,liu2021unsupervised}. Query-focused work further shows that the usefulness of a sentence depends on the requested information, not only its global centrality \cite{zhong2021qmsum,vig2022exploring}. The present task is document-focused rather than open-corpus retrieval: each method receives the same candidate sentences from one report and returns a fixed-size extract.

Lead, centroid, and graph-centrality baselines remain informative in technical reports. Lead exploits the tendency of reports to introduce major findings early. Centroid ranking favors sentences sharing vocabulary with the document as a whole. TextRank represents sentences as an undirected similarity graph and applies PageRank. These baselines test whether a causal-role mechanism adds value beyond document position, lexical centrality, or generic graph centrality.

### 2.2. Evidence Retrieval and Semantic Ranking

Sentence evidence retrieval has been evaluated extensively in fact verification, including human-annotated FEVER evidence \cite{thorne2018fever}. Lexical BM25 and dense sentence encoders offer strong comparators \cite{robertson2009probabilistic,reimers2019sentencebert}. The existing C²GES asset base contains a separate document-grouped FEVER study with BM25, MiniLM, and BGE comparisons. That study is useful as auxiliary evidence about sentence-ranking behavior, but it is not a power-grid summarization result and does not replace the NERC evaluation in this article.

### 2.3. Graph Structure in Summarization

Graph summarization methods connect sentences, topics, entities, or discourse units and then propagate or rank salience \cite{wang2020heterogeneous,cui2020enhancing,jing2021multiplex}. Many such systems learn graph representations. In contrast, the implemented C²GES graph is deterministic: role cues and optional silver role evidence assign a dominant sentence role; allowed role transitions create typed edges; and a weighted-degree statistic supplies graph salience. This design sacrifices representational capacity for transparent edge construction and reproducible interventions. It should therefore be compared with lightweight graph ranking, not described as a GNN model.

### 2.4. Causal and Counterfactual NLP

Causal NLP spans causal relation extraction, causal inference over text-derived variables, robustness analysis, and counterfactual data construction \cite{feder2022causal,du2022ecare}. The word *counterfactual* is used narrowly here. For each sentence node, the method constructs a graph with that node removed and measures the reduction in total typed edge weight. This is an operational structural perturbation of the proxy graph. It is not a Pearl-style intervention on an identified physical data-generating process, and the resulting score should be interpreted as graph sensitivity rather than an estimated causal effect.

### 2.5. NLP for Power-Grid Technical Reports

AI and language technologies are increasingly considered for grid models, operational records, and infrastructure analysis \cite{xie2022massively,hamann2024foundation,madabhushi2023survey,srinivasan2023artificial}. Verified prior work in *Applied Sciences* includes supervised entity--relation extraction from a purpose-built grid-field corpus \cite{meng2023gridfield}. Its target and supervision differ from the present task: entity--relation extraction predicts labelled relations, whereas C²GES selects a short traceable extract from a supplied report. The current study does not claim superior relation extraction or validated physical causality; it evaluates report-level summary overlap and diagnostic role coverage.

## 3. Task Definition and Data

### 3.1. Extractive Summarization Task

Let a report be a sequence of candidate sentences

\[
D = \{s_1,\ldots,s_n\},
\]

where every sentence has a stable identifier and source position. Given a sentence budget (K), a method returns an ordered subset 

\[
\hat{Y}_K \subseteq D, \qquad |\hat{Y}_K|=\min(K,n).
\]

The selected sentences are restored to source order before concatenation. The primary frozen operating point is (K=5). The reference (Y) is the report's official Executive Summary, and overlap is evaluated with ROUGE-1, ROUGE-2, and ROUGE-L F1.

The benchmark is global rather than query-specific: it asks for a short report summary. Causal roles enter as content-coverage signals, not as an externally supplied user query. This differs from the existing FEVER evidence-selection task, where a claim acts as a query and SUPPORTS/REFUTES is an optional role input.

### 3.2. Public NERC Source Reports

The local registered source comprises 40 public NERC PDF reports covering disturbances, reliability reviews, storm analyses, recommendations, and related technical assessments. This set supplies authentic power-grid report language, although not every document is literally a maintenance work order. The phrase *maintenance reports* in the retained title therefore denotes the intended engineering-review use, while the measured corpus should be described precisely as public NERC reliability and disturbance reports.

For each PDF, `pdftotext` produces layout-preserving text. A report is eligible when an `Executive Summary` heading and a deterministic end boundary can be identified and the cleaned section contains at least 80 alphanumeric words. Candidate sentences come from the previously segmented report JSON after removal of the detected executive-summary prefix. Each retained row records the source URL, PDF hash, segmented JSON hash, number of removed prefix sentences, reference provenance, and any optional silver role evidence.

An initial build revealed a boundary failure: one Executive Summary extended to 25,209 words because the report transitioned to `Chapter 1` rather than an older registered end heading. That directory was retained as a failed diagnostic and excluded. The builder was revised to recognize a `Chapter 1` heading, a regression test was added, and a new dataset was constructed. The corrected frozen dataset contains 28 reports, with 12 development and 16 test reports; 12 reports are excluded with explicit reasons. In the test set, official reference summaries contain 279--2298 words (median 790.5), and candidate pools contain 20--60 sentences (median 54).

### 3.3. Hash-Defined Split and Leakage Boundary

Each document ID is mapped to a split by SHA-256. Buckets 0--2 form development and buckets 3--9 form test. No report appears in both partitions. The complete JSONL dataset SHA-256 is `3B74CA2EE3D2DD207341BC870B8B5319AB935566670B2FD7C192E7BB725A7C48`. The development set was not used to optimize v0.1 weights; the executed configuration uses preregistered default weights. Therefore, these weights must not be called tuned or optimal.

### 3.4. Silver Causal-Role Evidence

Each segmented report may contain candidate evidence for five functions: trigger event, root cause, propagation or response, impact, and mitigation. These records were created and checked by machine workflows. During graph construction, a supplied silver role takes precedence over a lexical tie for that sentence. During evaluation, silver role coverage is the fraction of roles with available evidence for which at least one registered sentence is selected.

This metric is diagnostic. It tests consistency with the machine-produced role layer, not agreement with independent engineers. It is especially inappropriate to label it expert causal fidelity, because the silver role layer can also influence graph construction. The official Executive Summary, rather than the silver role record, supplies the ROUGE reference.

## 4. Proposed C²GES Method

### 4.1. Overview

C²GES contains four deterministic stages: role scoring, typed graph construction, structural counterfactual sensitivity, and constrained extractive selection. Figure 1 should depict the auditable data flow

`candidate sentences -> lexical/silver role scores -> typed directed proxy graph -> graph and intervention scores -> constrained five-sentence extract`.

The figure must not show a trained GNN, T5 generator, or physical-grid simulator because those components are absent from the executable method.

### 4.2. Sentence-Level Role Scores

For each sentence (s_i) and role (r), a transparent cue function counts registered domain phrases. Longer phrases receive a small additional weight, and engineering quantities such as MW, GW, kV, Hz, and percentages add an impact cue. Raw non-negative scores are divided by the maximum score for that role within the document. If a sentence ID occurs in the optional silver evidence for role (r), its score is set to at least one. The dominant role is the highest-scoring role, with explicit silver evidence taking precedence over lexical ties.

This mechanism is a deterministic weak signal. It does not constitute trained causal relation extraction. A Role-only condition ranks sentences by their maximum role score to expose the behavior of this channel without graph or counterfactual terms.

### 4.3. Typed Causal Proxy Graph

Every candidate sentence becomes a graph node containing its identifier, text, position, five role scores, and dominant role. Directed edges are permitted only for registered role transitions:

- root cause → trigger event (`causes`);
- root cause → propagation/response (`enables_propagation`);
- trigger event → propagation/response (`propagates_to`);
- trigger event or propagation/response → impact (`results_in`);
- impact → mitigation (`motivates_mitigation`);
- root cause → mitigation (`addressed_by`).

For an allowed pair within 12 sentence positions, edge weight is

\[
w_{ij}=0.45\exp(-d_{ij}/5)+0.30J(s_i,s_j)+0.25\min(R_i,R_j),
\]

where (d_{ij}) is absolute sentence distance, (J) is token-set Jaccard similarity, and (R_i,R_j) are the dominant-role scores. Edge direction follows role semantics rather than narrative order because technical reports may state an impact before explaining its cause. Sentence graph salience (G_i) is the min--max normalized sum of incoming and outgoing edge weights.

The resulting object is called a causal *proxy* graph throughout the paper. Its edges encode registered role compatibility and local textual support. They have not been independently verified as physical causal relations.

### 4.4. Deterministic Counterfactual Intervention

Let total graph causal flow be

\[
F(G)=\sum_{e\in E(G)}w_e.
\]

For each sentence node (i), the method constructs a new graph (G_{-i}) by removing the node and every incident edge. Raw sensitivity is

\[
\Delta_i^{\mathrm{cf}}=\max\{0,F(G)-F(G_{-i})\},
\]

and the document-level values are min--max normalized to form (C_i). The graph object is immutable under intervention: the original graph remains available, unknown node IDs fail closed, and node and edge removal are separately testable.

This operation answers a limited computational question: how much registered typed graph flow depends on one sentence? It does not generate alternative event text and does not model how the physical grid would have behaved had an event not occurred.

### 4.5. Sentence Score and Constrained Selection

For full C²GES, base sentence score is

\[
S_i=0.30Q_i+0.20R_i+0.20G_i+0.25C_i+0.05P_i,
\]

where (Q_i) is offline document-centroid relevance, (R_i) is maximum role compatibility, (G_i) is graph salience, (C_i) is counterfactual graph sensitivity, and (P_i=1/(1+\mathrm{position}_i)) is a position prior. These are frozen default weights, not development-optimized estimates.

Selection first reserves one sentence for each available causal-function group when (K\geq3): cause or trigger, propagation or impact, and mitigation. Remaining slots maximize

\[
S_i-0.35\max_{j\in A}J(s_i,s_j),
\]

where (A) is the set already selected. Ties are broken by earlier source position and then sentence ID. The final extract is sorted back into document order.

### 4.6. Registered Conditions

All six methods use the same candidate pool and five-sentence budget.

1. **Lead:** the first five candidate sentences.
2. **Centroid:** top sentences by offline document-centroid lexical relevance.
3. **TextRank:** PageRank over an undirected sentence Jaccard graph using NetworkX 3.6.1.
4. **Role:** top sentences by maximum five-role score.
5. **Graph without CF:** the constrained summarizer with weights 0.40 relevance, 0.25 role, 0.25 graph, 0 counterfactual, and 0.10 position.
6. **C²GES Full:** the complete score and constraints described above.

The Graph-without-CF condition is not a strict single-factor ablation because its four retained weights are independently registered rather than being the exact proportional renormalization of the full model. It provides a practical comparison, but cannot isolate the counterfactual channel by itself.

## 5. Experimental Design

### 5.1. Frozen Execution

The formal configuration fixes condition order, five-sentence budget, 10,000 bootstrap samples, seed 20260808, ROUGE stemming, TextRank parameters, both mixture definitions, and the report as resampling unit. The freeze manifest binds the configuration, dataset, builder, method module, runner, Python 3.12.10, NetworkX 3.6.1, and `rouge-score` 0.1.2. The freeze-manifest SHA-256 is `406ee363703fa5850339c586bfae87b403431bfec12294e3bc77787bec0fc477`.

The runner refuses an existing output directory. It writes a `RUNNING` state before loading data, verifies every frozen hash before predictions, and writes a failure record if execution stops. A completed run contains per-document predictions, aggregate metrics, paired bootstrap comparisons, a runtime/freeze manifest, and terminal state.

### 5.2. Evaluation Metrics

ROUGE-1, ROUGE-2, and ROUGE-L F1 compare each five-sentence extract with the official Executive Summary. ROUGE-L is the registered primary metric in the v0.1 protocol, while ROUGE-1 and ROUGE-2 are secondary. Mean pairwise token-set Jaccard among selected sentences measures redundancy; lower values indicate less lexical repetition. Silver role coverage measures overlap with available machine-silver role evidence and is reported only as a diagnostic.

For each baseline and ROUGE metric, paired report-level bootstrap resamples the 16 test reports with replacement 10,000 times and records `C²GES Full minus baseline`. Percentile 95% intervals describe sensitivity to the observed report composition. The emitted two-sided bootstrap (p)-values are exploratory and unadjusted across the 15 comparisons, so the manuscript emphasizes effect estimates and intervals rather than a family-wise significance claim \cite{cameron2008bootstrap}.

### 5.3. Reproduction and Integrity Checks

Run 01 completed with 16 reports and 96 prediction rows. A second execution used the same freeze in a new output directory. `predictions.jsonl`, `aggregate_metrics.json`, and `paired_bootstrap.json` were byte-identical across the two runs. The prediction hash was `4c1ed85dbbdbd0de76f02fd93ee96559b497e5764fb00e2b5d104802a91ab8b2`; aggregate and bootstrap hashes were `4dd1e32756e84c4867ab855bdc4157686ffd5d1db319fe669264889c33e2bd1e` and `f7e697aa8159991a0cf06a956d02e0b8d672925b9844b4fccd306aee1f7f3762`, respectively.

Integrity checks confirmed that every report had all six conditions, every prediction contained five unique sentence IDs, and every metric was a finite value in ([0,1]). Eleven current unit tests cover data-boundary parsing, deterministic graph construction, interventions, constrained selection, six-condition consistency, aggregation, bootstrap determinism, and failure-closed configuration checks.

### 5.4. Auxiliary FEVER Evidence-Selection Assets

The existing narrow-title study provides a separate leakage-controlled evidence-selection analysis on FEVER. Its document-grouped splits contain 8000 training, 1500 development, and 1500 test instances from 745, 141, and 145 underlying documents, with zero document overlap. Across five downstream seeds, predicted-label C²GES obtained evidence F1 0.4920 (SD 0.0021) at (K=3), compared with 0.4864 for BM25. However, the predicted-role minus label-blind difference was only +0.0010, with intervals crossing zero. Frozen MiniLM and BGE comparison families produced no Holm-adjusted promoted finding. These results support the availability of an auditable sentence-ranking implementation; they do not establish NERC summarization quality, a causal-role benefit, or the effectiveness of the graph intervention used in the present report-level method.

## 6. Results

### 6.1. Main Report-Level Results

Table 1 reports means across 16 frozen test reports.

**Table 1. Five-sentence extractive summarization on public NERC reports. Silver role coverage is a machine-label diagnostic, not expert agreement. Bold indicates the largest observed value in a column and does not imply statistical superiority.**

| Condition | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Silver Role Coverage | Redundancy |
|---|---:|---:|---:|---:|---:|
| Lead | 0.2220 | 0.0876 | 0.1262 | 0.2125 | 0.0539 |
| Centroid | 0.2564 | **0.1002** | **0.1405** | 0.2500 | 0.1645 |
| TextRank | 0.2218 | 0.0822 | 0.1267 | 0.1625 | 0.1845 |
| Role | 0.2367 | 0.0831 | 0.1185 | **0.4250** | 0.0614 |
| Graph without CF | **0.2647** | 0.0939 | 0.1326 | 0.4125 | 0.0820 |
| C²GES Full | 0.2608 | 0.0934 | 0.1323 | 0.3750 | 0.0683 |

Full C²GES produced higher observed ROUGE-1 than Lead, Centroid, TextRank, and Role, but lower ROUGE-1 than Graph without CF. Its ROUGE-2 and ROUGE-L were lower than Centroid. Thus, no row dominates all reported content-overlap metrics.

The graph-constrained methods selected less redundant extracts than Centroid and TextRank. Full C²GES redundancy was 0.0683, compared with 0.1645 for Centroid and 0.1845 for TextRank. Lead had the lowest observed redundancy (0.0539), indicating that a low redundancy score alone is not sufficient for high reference overlap.

Role-only ranking achieved the highest silver role coverage, 0.4250, followed by Graph without CF at 0.4125 and full C²GES at 0.3750. Because the same silver layer is available during graph construction, these values measure internal consistency with the machine role record and must not be interpreted as independent causal validity.

### 6.2. Paired Bootstrap Contrasts

Full C²GES minus Lead had an observed ROUGE-1 difference of +0.0388, with a 95% percentile interval of [0.0136, 0.0663]. Full C²GES minus TextRank was +0.0390, with interval [0.0070, 0.0782]. These are the only reported ROUGE contrasts for which the v0.1 interval did not cross zero.

For the registered primary metric, ROUGE-L, every full-model comparison interval crossed zero. Full minus Centroid was -0.0082, with interval [-0.0259, 0.0058]; full minus Role was +0.0138, with interval [-0.0063, 0.0368]; and full minus Graph without CF was -0.0003, with interval [-0.0053, 0.0055]. Full minus Lead and TextRank were also small on ROUGE-L, with intervals spanning zero.

These results support a narrow statement: full C²GES improved ROUGE-1 relative to Lead and TextRank for the observed 16-report benchmark. They do not support superiority on the registered primary metric, across all baselines, or across all ROUGE variants.

### 6.3. Counterfactual Component Comparison

The complete method did not improve on Graph without CF. Their observed ROUGE-1/2/L values were 0.2608/0.0934/0.1323 and 0.2647/0.0939/0.1326, respectively. The full-minus-no-CF intervals crossed zero for all three ROUGE metrics. Moreover, the two conditions use different registered non-counterfactual weights, so their contrast is not a pure removal test.

The correct conclusion is therefore negative but useful: v0.1 provides no evidence that the current leave-one-node-out graph-flow score improves summary overlap. A strict next test should remove only the counterfactual channel from the full score, proportionally renormalize the four retained weights, keep all other selection decisions fixed, and freeze the comparison before examining test results.

### 6.4. Reproducibility Result

Both executions generated exactly the same 96 prediction records, aggregate table, and 15 paired bootstrap contrasts. This determinism does not establish scientific validity, but it removes run-to-run variation as an explanation for the reported v0.1 differences and permits each table cell to be traced to sentence IDs, source hashes, condition settings, and report-level metrics.

## 7. Discussion

### 7.1. What the Current Evidence Supports

The experiment establishes that a transparent causal-proxy graph and constrained selector can be executed end to end on public power-grid reports under a frozen and reproducible protocol. Full C²GES raises ROUGE-1 relative to two lightweight baselines and reduces redundancy relative to Centroid and TextRank. The output also remains extractive, so a reviewer can inspect every selected sentence in its source report.

The observed pattern suggests that causal-function coverage and redundancy constraints change what the model selects, but it does not identify which component is responsible for the ROUGE-1 differences. Role-only ranking has higher silver coverage but lower ROUGE, the full method does not beat the no-CF condition, and Centroid remains strongest on observed ROUGE-L. These results argue against a simple narrative in which more causal structure automatically produces a better summary.

### 7.2. Meaning of “Causal” and “Counterfactual”

The graph encodes directional role transitions supported by lexical proximity, sentence distance, and optional silver roles. It is interpretable because every node, edge type, edge weight, and intervention can be inspected. Interpretability does not convert the proxy into ground-truth causality. The selected relations may reflect report rhetoric, repeated terminology, or errors in machine role evidence.

Similarly, the counterfactual score is a graph-deletion sensitivity. It quantifies how much registered edge weight disappears when a node is absent. It does not estimate what would have happened in the grid under a physical intervention, and it does not generate minimally edited counterfactual text. This distinction should be stated in the title-page abstract, method, and limitations to prevent the retained original title from carrying a stronger causal claim than the implementation warrants.

### 7.3. Practical Relevance

The method's immediate value is an auditable summary packet: five source-ordered sentences, their stable IDs, graph context, component scores, and selection reasons. Such a packet can help an engineer locate a concise cause--event--impact--mitigation trail before returning to the complete official report. It should be viewed as decision support, not an autonomous root-cause determination. Any operational use requires human review, source linking, access control, and procedures for rejecting or supplementing the selected evidence.

The corpus also sets a useful but bounded domain target. NERC reports contain genuine reliability and disturbance language, yet differ from utility-internal maintenance tickets, work orders, and asset-management records. Performance on this benchmark should not be generalized to confidential maintenance corpora without a separate license, segmentation audit, and sealed evaluation.

### 7.4. Limitations

First, the test set contains only 16 reports. Report-level bootstrap accounts for sampling the observed documents, but the intervals remain sensitive to genre composition and cannot represent all power-grid reporting practices.

Second, official Executive Summaries are long: the test median is 790.5 words, whereas predictions are fixed at five sentences. ROUGE therefore mixes content selection with a severe length mismatch. The registered ten-sentence sensitivity and length-matched analysis have not yet been executed.

Third, the v0.1 weights are frozen defaults, not development-selected parameters, despite an earlier protocol statement anticipating development-set selection. This departure must remain visible. A later tuned study must define its search space and decision rule before opening the test results.

Fourth, the causal-role records are machine silver. They are suitable for pipeline development and diagnostics, but not expert agreement, causal fidelity, or domain accuracy claims. Independent qualified reviewers would need a frozen manual, blinded sentence selection, retained disagreements, human adjudication, and a sealed test subset.

Fifth, the graph relies on role cues, token Jaccard similarity, and local distance. No neural semantic encoder is used in the report-level run. The comparison set lacks a strong modern semantic summarizer or cross-encoder, so improvement over Lead or TextRank cannot be interpreted as state-of-the-art performance.

Sixth, Graph without CF is not a pure single-factor ablation. Its independently chosen remaining weights confound channel removal with reweighting. The absence of an observed full-model advantage is clear, but the causal reason for that absence is not identified.

Seventh, the bootstrap outputs include 15 unadjusted comparisons. Two ROUGE-1 intervals exclude zero, but no family-wise confirmatory claim has been registered. Future analysis should preselect a smaller contrast family or apply a stated multiplicity procedure.

Finally, PDF-to-text extraction can fail at section boundaries, tables, repeated page headers, and scanned pages. The detected 25,209-word boundary incident demonstrates this risk. Deterministic regression tests reduce a known failure mode but do not prove perfect extraction for every layout.

## 8. Conclusions

This study rebuilds the original C²GES idea around verifiable assets. The resulting method constructs a typed sentence-level causal proxy graph, applies deterministic leave-one-node-out graph interventions, and selects a source-ordered extract under causal-function coverage and redundancy constraints. A frozen benchmark derived from public NERC reports contains 28 eligible reports and a 16-report test set with official Executive Summaries as references.

At a five-sentence budget, full C²GES achieved ROUGE-1/2/L F1 of 0.2608/0.0934/0.1323. Its ROUGE-1 differences over Lead and TextRank were positive with report-level bootstrap intervals excluding zero, but Centroid obtained the highest observed ROUGE-2 and ROUGE-L, and Graph without CF obtained the highest observed ROUGE-1. The counterfactual comparison was effectively tied and cannot support an effectiveness claim.

The main contribution at this stage is therefore an auditable domain benchmark, an executable causal-graph-constrained baseline, and a reproducible evidence ledger rather than broad algorithmic superiority. Strong semantic baselines, a strict counterfactual ablation, budget sensitivity, development-locked weight selection, and independent human validation are required before stronger claims can be considered.

## 9. Back Matter Recommendations

### Supplementary Materials

The supplementary package should include the dataset build manifest and exclusion audit; frozen configuration and freeze manifest; method and runner code; unit tests; both run directories; 96-row prediction ledger; aggregate and bootstrap outputs; and an artifact hash index. Public source PDFs should not be redistributed unless their licenses permit it. The first boundary-failure directory should remain in the internal audit package and be explicitly excluded from reported results.

### Author Contributions

**Recommended CRediT text:** Conceptualization, B.L. and Y.Y.; methodology, B.L.; software, B.L.; validation, B.L.; formal analysis, B.L.; investigation, B.L.; resources, Y.Y.; data curation, B.L.; writing—original draft preparation, B.L.; writing—review and editing, B.L. and Y.Y.; visualization, B.L.; supervision, Y.Y.; project administration, Y.Y.; funding acquisition, Y.Y. All authors have read and agreed to the published version of the manuscript.

The authors must confirm that this allocation matches their actual work before submission.

### Funding

This research was funded by the Science and Technology Project of NARI Group Corporation (State Grid Electric Power Research Institute), grant number **521300250006**.

### Institutional Review Board Statement

Not applicable. The study did not involve human participants or animals. It used public technical reports and an existing public human-annotated auxiliary benchmark. This statement should be rechecked if a future round adds real expert annotation as research data.

### Informed Consent Statement

Not applicable.

### Data Availability Statement

FEVER is available from its original providers \cite{thorne2018fever}. Public project code and license-cleared reproducibility materials are available at <https://github.com/gaoxingkele/c2ges>. Owing to third-party licensing restrictions, NERC source documents and submission-version materials not included in the public repository are available from the corresponding author upon reasonable request for editorial and peer-review verification, subject to third-party permission and applicable licenses. The verification package should contain the frozen dataset manifest, source URLs and hashes, builder and audit code, configuration, method implementation, predictions, statistics, reproduction outputs, and explicit machine-silver provenance. Corresponding-author email: **[author to supply before submission]**.

### Acknowledgments and AI-Assistance Disclosure

During preparation of the manuscript, AI-assisted tools were used for drafting, editing, code review, and reproducibility checks. Any models used to create or adjudicate causal-role records must be named in the final disclosure. The authors reviewed and edited all outputs and take responsibility for the publication. Machine-produced labels are not presented as human or domain-expert ground truth.

### Conflicts of Interest

The authors declare no conflicts of interest. The funder had no role in the design of the study; collection, analysis, or interpretation of data; writing of the manuscript; or decision to publish the results. The authors should verify this standard statement against the actual project governance before submission.

### Author and Affiliation Block

**Bijing Liu**\(^{1,2}\) and **Yong Yang**\(^{1,2,*}\)

1. NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China.
2. Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China.
3. *Correspondence:* Yong Yang; email **[author to supply before submission]**.

### References

No new references are introduced in this Round-1 draft. All citation keys are drawn from the current verified Applied Sciences bibliography. Citation rendering, bibliography completeness, DOI checks, and MDPI numeric ordering should be audited only when this Markdown draft is promoted into the LaTeX manuscript.
