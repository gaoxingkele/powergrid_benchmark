# Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports

**Article type:** Article  
**Target journal:** *Applied Sciences*  
**Round:** R2 staging draft; formal test output exists but remains quarantined pending independent post-run audit

**Liu Bijing**^1,2^ and **Yang Yong**^1,2,*^

^1^ NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China  
^2^ Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China  
* Correspondence: Yang Yong; **email address to be completed manually before submission**

## Abstract

Power-grid engineering reports combine initiating conditions, event sequences, impacts, and corrective actions across long technical documents. This article presents C²GES, a deterministic extractive summarization framework that combines semantic relevance, sentence-role evidence, a typed textual proxy graph, and a path-deletion structural perturbation score. The title retains the intended maintenance-review application; the measured population, however, consists of public North American Electric Reliability Corporation (NERC) reliability, disturbance, event-analysis, recommendation, and assessment reports rather than utility maintenance work orders. Consequently, maintenance-domain effectiveness is an untested transfer claim, and neither the graph nor its perturbations identify physical causal effects.

The benchmark was rebuilt from 40 complete PDFs comprising 3,200 declared pages. Conservative summary-boundary and quality gates retained 27 reports, split into 12 development and 15 untouched test reports, and yielded 12,924 non-summary candidate sentences without a fixed candidate cap. Independent Stage-1 audit found no reference/candidate page overlap, no normalized exact candidate/reference sentence match, no residual common substring of at least 50 characters, and no occurrence of the eight registered extraction-pollution patterns. A 144-configuration development search selected the frozen scoring weights and graph limits. The newly defined counterfactual channel measures the loss of qualified two-to-four-edge typed path strength under node deletion and is mathematically distinct from weighted degree. On development data, however, Full minus strict no-counterfactual ROUGE-L F1 at five sentences was −0.005665; this negative result is retained without reinterpretation. One hash-authorized formal execution has completed, but its comparisons against strict no-CF, Semantic-MMR, and TextRank remain **EVIDENCE_PENDING_TEST** until a fresh independent post-run audit accepts the result artifacts. Any accepted test result will be described as post-audit corrective and descriptive, not fresh confirmatory evidence, because earlier versions of the test population were inspected during corrective reconstruction.

**Keywords:** extractive summarization; typed textual proxy graph; structural perturbation; reliability reports; power-grid text analytics; reproducible evaluation

## 1. Introduction

Technical reporting in the power sector is sequential and relational. A useful short extract may need to preserve an initiating condition, the event or system response, the resulting impact, and the mitigation or recommendation, while also retaining equipment identifiers and quantities. Extractive summarization is appropriate for this setting because every selected sentence remains traceable to a source document and page.

The retained title reflects the intended use of summaries in maintenance-oriented engineering review. It must not be read as a description of the evaluation population. The present study evaluates public NERC reliability, disturbance, event-analysis, recommendation, and assessment reports. These documents contain maintenance-relevant lessons and corrective recommendations, but they are not equivalent to maintenance work orders, inspection records, or asset-management narratives. Performance on those title-concordant genres remains untested.

Earlier C²GES assets contained an executable deterministic proxy-graph pipeline, but the R1 audit exposed two foundational defects. First, the previous node-deletion flow loss was algebraically identical to weighted degree and therefore did not constitute a distinct counterfactual channel. Second, Executive Summary text remained in candidate pools because candidates were extracted from capped excerpts with an incomplete boundary rule. The affected v0.1 and v0.2 outputs have been withdrawn as primary scientific evidence and are preserved only as corrective history.

R2 rebuilds the study around complete PDFs, a fail-closed summary/body boundary, a development-only configuration ledger, a distinct typed-path deletion score, and a strong Semantic-MMR comparator. The term *counterfactual* is used only for a computational graph perturbation: remove one sentence node and recompute a registered typed-path utility. The operation does not generate alternative event narratives, estimate a treatment effect, or validate a causal relation in grid physics.

The scoped contributions are fourfold. First, we construct and independently audit a full-PDF NERC benchmark with explicit inclusion, extraction, leakage, split, and rights ledgers. Second, we define a deterministic typed textual proxy graph and a path-deletion score that is not reducible to weighted degree. Third, we freeze a seven-condition, two-budget evaluation with Semantic-MMR and report-level paired inference, including a strict single-channel no-CF ablation. Fourth, we expose negative development evidence, corrective incidents, and the maintenance-transfer boundary instead of converting them into favorable claims.

## 2. Related Work

### 2.1. Extractive and Technical-Document Summarization

Extractive summarization selects source sentences and thereby preserves direct traceability. Lead, centroid, and graph-ranking baselines remain important in technical documents because they reveal whether a more elaborate selector adds value beyond position, lexical centrality, or sentence similarity. Long technical reports also require diversity control: relevance-only ranking can repeatedly select sentences describing the same local event.

Query-focused and evidence-selection studies motivate sentence-level identifiers, reproducible candidate sets, and report-level evaluation. The present task is global report summarization rather than open-corpus retrieval. Every condition receives the same candidates from one report and returns a five- or ten-sentence extract restored to source order.

### 2.2. Graph-Based Summarization and Causal Language

Graph summarizers model relations among sentences, entities, topics, or discourse units. C²GES uses a transparent typed sentence graph rather than a learned graph neural network. Nodes are candidate sentences; directed edges are permitted only between registered sentence-role stages and are weighted by distance, lexical overlap, and role confidence.

Causal language requires stricter interpretation than graph connectivity. A text-derived edge is a proxy relation and may reflect rhetorical order, shared terminology, or a heuristic role transition. It is not a validated structural equation or physical mechanism. Accordingly, this study distinguishes graph-structural sensitivity from causal identification and requires future qualified-domain validation before operational claims.

### 2.3. Power-Grid Report Analytics

Power-grid language technologies have been studied for information extraction, entity–relation recognition, retrieval, and decision support. Report-level summarization differs from those tasks because it must compress a complete document while maintaining cross-sentence event structure. The present corpus provides authentic reliability and disturbance language, but it cannot establish generalization to maintenance logs, work orders, or private utility records.

## 3. Materials and Methods

### 3.1. Study Scope and Evidence Class

Let a report contain candidate sentences \(D=\{s_1,\ldots,s_n\}\). For budget \(K\in\{5,10\}\), a method returns \(\hat{Y}_K\subseteq D\), with \(|\hat{Y}_K|=\min(K,n)\), and the selected sentences are restored to source order. The official Executive Summary is the reference only; it is not an eligible source of candidates.

The study is a post-audit corrective evaluation. Earlier test-population outcomes were inspected while diagnosing R1, so a later freeze cannot recover outcome-unseen confirmatory status. The v0.3.1 protocol therefore treats any formal test output as descriptive evidence for the fixed corrective benchmark. A genuinely new sealed holdout would be required for confirmation.

### 3.2. Source PDFs, Inclusion, and Partitioning

The source manifest binds 40 local NERC PDFs with distinct SHA-256 values and 3,200 declared pages. A deterministic full-PDF builder retained 27 reports and excluded 13 before graph construction or outcome computation. One formerly retained report was conservatively excluded because its Executive Summary end could not be located using the registered generic boundary rules; no report-specific repair was introduced.

The retained dataset contains 12 development and 15 untouched test reports. The complete, development, and test JSONL hashes are, respectively, `87F7F754...AA15`, `27CE41D3...7F79`, and `A9342BD7...D127`; the full hashes are recorded in the evidence registry and freeze manifest. Series-aware report grouping and deterministic splitting prevent an individual report from crossing partitions. The formal test file is not read by this staging manuscript.

### 3.3. Full-PDF Candidate Construction and Leakage Gates

Candidates are segmented from the full body after a conservatively detected Executive Summary boundary. No fixed sentence cap is applied. Across 27 reports, the builder emits 12,924 candidates, with 51–1,898 candidates per report; 25 reports contain more than 80 candidates, and none is declared truncated.

The independent Stage-1 re-audit reconstructed every included row directly from the source PDFs. It found zero reference/body page-interval overlap, zero candidate sentence before the registered body page, zero normalized exact candidate/reference sentence match, and zero residual normalized common substring of at least 50 characters. It also found zero instances of the eight registered pollution classes: Executive Summary running heads, section–table fusion, public markers, replacement characters, common mojibake, page markers, dot leaders, and spaced uppercase running titles. These deterministic checks do not imply that every extracted sentence is semantically or stylistically clean.

### 3.4. Sentence Roles and Typed Textual Proxy Graph

Each candidate receives transparent lexical evidence for five textual roles: root cause, trigger event, propagation or response, impact, and mitigation. Positive top-score ties abstain rather than using fixed role order; the audited development graphs contained 111 such ties, all assigned no dominant role and no directed incident edge. The v0.3 builder supplies no silver role evidence to the selector.

A directed edge is permitted only for registered stage-monotone role transitions and within the selected sentence-distance limit. Edge weights combine positional distance, token-set Jaccard overlap, and role confidence. Weighted degree, normalized within a report, forms the graph-salience channel \(G_i\). This graph encodes a reproducible textual hypothesis; it is not a learned GNN, a power-system topology, or a validated causal graph.

### 3.5. Typed Path-Deletion Structural Perturbation

Let \(\mathcal{P}(G)\) be the set of simple, stage-monotone typed paths with two to four edges that begin at a root-cause or trigger node and end at an impact or mitigation node. For path \(p\), define

\[
\operatorname{strength}(p)=\left(\prod_{e\in p}w_e\right)^{1/|p|}\frac{\max\operatorname{stage}(p)-\min\operatorname{stage}(p)}{4}.
\]

The registered graph utility is

\[
U(G)=\sum_{p\in\mathcal{P}(G)}\operatorname{strength}(p),
\]

and the raw node-deletion score is

\[
C_i=U(G)-U(G_{-i})
=\sum_{p\in\mathcal{P}(G):i\in p}\operatorname{strength}(p).
\]

The score depends on multi-edge path membership, role order, and the geometric mean of edge weights. Weighted degree depends only on the sum of incident edge weights; the two are not algebraically identical in general. A registered counterexample gives two nodes the same weighted degree while only one participates in a qualified cause-to-impact path, producing different \(C_i\). Unit and property tests also verify deletion-loss equality, deterministic scaling, cache equivalence, and fail-closed path/expansion limits. These are mathematical and software-identifiability checks, not evidence of physical causality or summarization benefit.

### 3.6. Full Score and Constrained Selection

The development-selected Full score is

\[
S_i=0.40Q_i+0.20R_i+0.15G_i+0.15C_i+0.10P_i,
\]

where \(Q_i\) is lexical report-centroid relevance, \(R_i\) is role evidence, \(G_i\) is weighted-degree salience, \(C_i\) is normalized typed path-deletion loss, and \(P_i\) is a positional prior. Greedy selection subtracts \(0.50\) times the maximum token-set Jaccard overlap with an already selected sentence. The maximum edge distance is 12; qualified paths contain two to four edges; path and expansion caps are 250,000 and 2,000,000. Limit exhaustion fails closed.

The strict no-CF ablation changes only the coefficient of \(C_i\) from 0.15 to 0. All remaining coefficients, graph construction, redundancy penalty, tie rules, and budgets are unchanged; no coefficient renormalization is performed. This single-factor contrast isolates the implemented perturbation channel more closely than R1.

### 3.7. Development-Only Configuration Selection

The development search evaluated 144 registered configurations over the 12 development reports. Its ordered objective was: maximize mean ROUGE-L F1 at \(K=5\); break ties by mean ROUGE-1 F1, lower redundancy, and then the earliest grid record. Grid index 60 was selected with mean development ROUGE-L F1 0.1195126 and ROUGE-1 F1 0.2713870. The minimum report-level maximum absolute difference between the CF and graph channels was 0.501651, supporting non-identity.

The selected Full method did not outperform strict no-CF on the development primary metric: Full minus no-CF ROUGE-L F1 at \(K=5\) was −0.0056652. This unfavorable value is retained as development evidence. It neither decides the untouched test result nor supports a counterfactual-benefit claim.

### 3.8. Comparators

Seven conditions are frozen in a common candidate space: Lead, lexical Centroid, TextRank, Semantic-MMR, Role, graph without CF (strict), and Full C²GES. Semantic-MMR uses the frozen local `all-MiniLM-L6-v2` snapshot and greedily maximizes

\[
0.5\cos(e_i,\bar e_D)-0.5\max_{j\in A}\cos(e_i,e_j),
\]

where \(e_i\) is the normalized sentence embedding, \(\bar e_D\) is the normalized document centroid, and \(A\) is the selected set. Its 0.5 balance was fixed symmetrically rather than optimized on development or test outcomes. It provides a semantic relevance-and-diversity comparator rather than the weaker relevance-only semantic centroid used in R1.

### 3.9. Frozen Test Protocol and Statistical Analysis

The v0.3.1 freeze registers budgets \(K=5\) and \(K=10\), ROUGE-L F1 as the primary metric, and three Full-minus-baseline contrasts at each budget: strict no-CF, Semantic-MMR, and TextRank. The six primary tests form one Holm step-down family. Paired report-level bootstrap intervals use 10,000 resamples and seed 20260808. ROUGE-1, ROUGE-2, redundancy, and remaining pairwise contrasts are exploratory.

The freeze binds dataset, code, configuration, model-tree, dependency-lock, regression-test, and corrective-history hashes. It additionally requires an independent PASS audit and exact hash-bound author authorization before one physical test attempt. The durable attempt registry is claimed before test content is decoded; failed or successful attempts cannot be retried under the same freeze. The v0.3.1 pre-test audit returned PASS for freeze SHA-256 `DE3205B0...19B5`, exact authorization was recorded, and run `c2ges_v031_formal_20260808` reached `COMPLETE`. Its numerical outputs remain quarantined from this manuscript pending an independent post-run audit.

### 3.10. Reproducibility, Rights, and Human Oversight

The full-PDF sources and extracted text are subject to third-party terms. The rights ledger therefore fails closed: source PDFs and verbatim benchmark text are not authorized for public redistribution pending responsible-human or institutional review. Subject to third-party permissions, materials needed for editorial or reviewer verification may be requested from the corresponding author. Hashes, extraction rules, code, configuration, and non-verbatim audit metadata can be prepared separately.

The public repository is `https://github.com/gaoxingkele/c2ges`. The manuscript must not state that this repository reproduces R2 until the exact release is synchronized, tagged, and verified from a fresh clone. No qualified power-grid expert validation is reported. Before any consequential use, an engineer must inspect source-linked outputs and may reject or abstain from using them.

## 4. Results

### 4.1. Dataset and Extraction Audit

Table 1 reports the evidence available before formal test execution.

| Item | Audited value | Status |
|---|---:|---|
| Source PDFs / pages | 40 / 3,200 | Independently checked |
| Included / excluded reports | 27 / 13 | Independently checked |
| Development / untouched test reports | 12 / 15 | Test content not read for this draft |
| Candidate sentences | 12,924 | No fixed cap |
| Candidates per report | 51–1,898 | 25 reports >80 |
| Reference/body page overlap | 0 | Independently checked |
| Exact normalized candidate/reference matches | 0 | Independently checked |
| Common substrings ≥50 characters | 0 | Independently checked |
| Registered pollution-pattern hits | 0 | Limited to eight deterministic patterns |

### 4.2. Development Selection and Counterfactual Diagnostic

| Development quantity | Value | Interpretation |
|---|---:|---|
| Configurations | 144 | Complete frozen grid |
| Selected grid index | 60 | Dev-objective winner |
| Full ROUGE-L F1 at K=5 | 0.1195126 | Development only |
| Full ROUGE-1 F1 at K=5 | 0.2713870 | Development tie-break quantity |
| Full − strict no-CF ROUGE-L F1 at K=5 | −0.0056652 | Negative development evidence |
| Minimum report max |CF − graph| | 0.5016510 | Software-signal non-identity, not efficacy |

The non-identity diagnostic establishes only that the new perturbation channel differs numerically and mathematically from weighted degree. The negative ablation result provides no development-set evidence that adding this channel improves summary overlap.

### 4.3. Formal Test Results

**EVIDENCE_PENDING_TEST.** The single authorized v0.3.1 execution is complete, but do not insert aggregate scores, intervals, adjusted p-values, favorable claims, or method rankings until an independent result audit is complete. Preliminary artifacts are not manuscript evidence.

| Condition | K | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Redundancy |
|---|---:|---:|---:|---:|---:|
| Lead | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| Lexical Centroid | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| TextRank | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| Semantic-MMR | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| Role | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| Graph without CF (strict) | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |
| Full C²GES | 5, 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST |

### 4.4. Primary Contrasts and Sensitivity Analysis

**EVIDENCE_PENDING_TEST.** The final table must contain report-level paired mean differences, 95% intervals, raw p-values, and Holm-adjusted p-values for exactly six registered ROUGE-L tests. A paired per-report plot must show all 15 test-report differences rather than only aggregate bars. Any effect estimate is descriptive because the benchmark is post-audit corrective.

| Primary contrast | K | Mean Δ ROUGE-L | 95% paired interval | Holm-adjusted p | Evidence class |
|---|---:|---:|---:|---:|---|
| Full − strict no-CF | 5 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |
| Full − strict no-CF | 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |
| Full − Semantic-MMR | 5 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |
| Full − Semantic-MMR | 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |
| Full − TextRank | 5 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |
| Full − TextRank | 10 | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | EVIDENCE_PENDING_TEST | Post-audit corrective |

## 5. Discussion

### 5.1. What the Rebuild Establishes

The rebuild establishes a cleaner experimental object than R1. Candidates derive from complete PDFs rather than fixed event-focused excerpts, summary leakage is tested at page, sentence, and substring levels, the development search is recorded, and the counterfactual channel is structurally non-equivalent to graph degree. Semantic-MMR also closes the principal strong-baseline gap by controlling both semantic relevance and redundancy.

These improvements establish implementation integrity, not algorithmic superiority. The negative development ablation already cautions against assuming that a distinct structural signal is useful merely because it is identifiable. Final interpretation must follow the untouched test result even if that result is null or unfavorable.

### 5.2. Maintenance-Workflow Transfer Boundary

The exact title is retained to preserve continuity with the original research objective. Its application scope remains broader than the measured corpus. NERC reliability and disturbance reports can support maintenance-oriented lessons-learned review, but work orders and inspection records differ in length, vocabulary, narrative structure, asset granularity, and reference-summary availability. The current evidence therefore supports only an evaluation on NERC technical reports and a proposed maintenance-review use case. It does not support an effectiveness claim for maintenance work orders.

### 5.3. Causal and Counterfactual Interpretation Boundary

The typed graph organizes text into role-conditioned paths. Its direction and path score are heuristic, reproducible hypotheses. Without qualified-domain annotation or an identified physical causal model, an edge cannot be treated as a true causal relation. Likewise, node deletion measures the dependence of a graph utility on one sentence; it is not a potential-outcome estimand, a do-intervention on grid state, or evidence that an event would change if a sentence were absent.

### 5.4. Limitations

The study has five main limitations. First, the title-concordant maintenance/work-order population is not represented. Second, the 15-report test set is modest and belongs to a previously inspected population, so results are descriptive. Third, official Executive Summaries are long references and ROUGE overlap does not measure engineering usefulness, factual sufficiency, or causal-chain completeness. Fourth, role and edge construction lack blinded qualified-expert validation. Fifth, third-party rights constrain redistribution of source PDFs and verbatim derived text.

### 5.5. Future Validation

Future work should freeze a license-cleared maintenance corpus at report or site level, create an untouched holdout, and obtain blinded review from qualified power-grid personnel. Human evaluation should separately score source faithfulness, coverage of cause/event/impact/mitigation elements, engineering usefulness, and unsafe omission. Inter-rater agreement and adjudication should be reported; LLM judgments must not be labeled expert validation. A deployment study should additionally record abstention frequency and the consequences of rejected or incomplete summaries.

## 6. Conclusions

C²GES is rebuilt as a deterministic, auditable extractive method operating on full NERC technical reports. The new typed path-deletion score is mathematically distinct from weighted degree, the benchmark has explicit leakage and extraction audits, and the comparison set includes Semantic-MMR and a strict single-channel ablation. The development result is unfavorable to a CF-benefit claim, and formal test evidence remains pending. Therefore, this R2 staging manuscript makes no superiority, maintenance-domain effectiveness, physical-causality, or expert-validation claim. Its principal current contribution is a bounded and reproducible study design that can support a valid descriptive test once the independent audit and authorization gates are satisfied.

## Supplementary Materials

The intended supplement will include the source manifest, per-report extraction audit, rights ledger, development-search ledger, freeze manifest, dependency lock, regression-test report, formal-run registry, prediction ledger, aggregate metrics, paired statistics, and figure-lineage records. Source PDFs and verbatim extracted text are excluded unless third-party permission is confirmed.

## Author Contributions

**CRediT roles require final author confirmation before submission.** Required confirmation sentence: “All authors have read and agreed to the published version of the manuscript.” This sentence must not be treated as confirmed until both authors approve the submission package.

## Funding

This research was funded by **[funder name to be confirmed by the authors]**, grant number **521300250006**. The funder-role statement must be completed and approved by the authors before submission.

## Institutional Review Board Statement

Not applicable. The computational study uses published technical reports and does not involve human participants or animal subjects.

## Informed Consent Statement

Not applicable.

## Data Availability Statement

Code is intended for release at `https://github.com/gaoxingkele/c2ges`; the public repository must be synchronized, tagged, and fresh-clone verified before submission, and this staging draft does not claim that it currently reproduces R2. Owing to third-party licensing restrictions, source PDFs and verbatim derived text are not publicly redistributed; subject to applicable permissions, materials needed for editorial and peer-review verification may be requested from the corresponding author. Hashes, configuration, non-verbatim audit metadata, and reproducibility records will accompany the submission package.

## Acknowledgments

**[Optional author-supplied acknowledgments pending.]**

## Conflicts of Interest

The authors must confirm the final conflict-of-interest statement before submission. No statement is inferred in this staging draft.

## Declaration of Generative AI and AI-Assisted Technologies

**[Tool-by-tool disclosure to be completed from the project provenance ledger before submission, including provider, model/version if known, date, purpose, affected content, and human verification. No AI system is treated as a qualified power-grid expert or as an author.]**

## References

**REFERENCE_INTEGRATION_PENDING.** Import only references verified in the R1 bibliography or subsequently checked against authoritative metadata. Do not retain citations merely because they appeared in the original Word manuscript.
