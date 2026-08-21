# W5 Staging Draft: MA-SQLGrid Materials, Data, Protocol, and Statistics

**Status.** This file is an evidence-bound writing draft for later assembly into an *Applied Sciences* manuscript. It does not modify the current CMC manuscript, does not report a new model result, and must not be copied into a Results section until the pending evidence gates identified below have been closed.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: acceptance scope and prompt-only status -->

## 2. Materials and Methods

### 2.1. Study Design and Evidence Boundary

We formulate the revised MA-SQLGrid study as a paired, question-level factorial evaluation of two context interventions for executable text-to-SQL in maintenance and operational databases. The first factor controls schema scope (full versus compact), and the second controls whether an answer-shape hint is absent or present. The primary GridDB protocol consequently contains four cells: `full_shape_absent`, `full_shape_present`, `compact_shape_absent`, and `compact_shape_present`. This design separates the marginal contribution of compact schema context from that of answer-shape guidance and permits an interaction estimate instead of attributing their joint effect to either component alone.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w1_validation/ma_factorial_dryrun/manifest.json | KEYS: factorial_design.cells -->

The registered GridDB dry run contains 180 held-out questions and four prompts per question, producing 720 prompt records. It validates prompt construction, cell balance, identifier uniqueness, gold-field exclusion, and record-level auditability only. At the time of this draft, its manifest reports zero predictions and zero scores; therefore, no statement about accuracy, robustness, latency, token use, cost, or component benefit follows from this artifact.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w1_validation/ma_factorial_dryrun/manifest.json | KEYS: question_count,prompt_count,prediction_count,score_count,status -->

The external protocol is a mechanical portability test over automatically generated candidates from RTS-GMLC and SimBench. It contains 91 candidates and 364 factorial prompt records, with all reference SQL statements passing the registered read-only safety and executability checks. These records are development-visible, automatically constructed, non-human-reviewed, and non-sealed. They support claims about plumbing, symmetry, and reproducibility, but not about semantic benchmark validity or model generalization.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/W4_MA_EXTERNAL_PROTOCOL_REPORT.md | KEYS: candidate_count,prompt_count,safety,executability,evidence_boundary -->

The earlier CMC evaluation is retained solely as legacy diagnostic context. In particular, projection-tolerant rescoring changes the ordering observed under the older scoring contract, so those results cannot establish an independent content-retrieval gain for the compact-context component. The revised manuscript will keep historical results separate from the confirmatory factorial table and will not describe legacy numbers as new evidence.

<!-- CLAIM: MA-C04 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/legacy_rescore_summary.json | KEYS: projection-tolerant rescoring and evidence restriction -->

### 2.2. Task Definition

Let a natural-language question be \(x_i\), a database be \(D_i\), and its introspected schema be \(S_i\). A system produces one SQL string \(\hat{y}_{i,s,h}\) under schema condition \(s\in\{0,1\}\) and shape-hint condition \(h\in\{0,1\}\), where 0 and 1 denote full/compact schema and absent/present shape guidance, respectively. The experimental unit is the question, not the individual prompt, because all four conditions are constructed for the same question and database.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w1_validation/ma_factorial_dryrun/manifest.json | KEYS: factorial_design and question pairing -->

The context supplied to a generator is proposed as

\[
C_{i,s,h}=G_s(x_i,S_i)\oplus N(x_i,V_i)\oplus h\,H(x_i),
\]

where \(G_s\) selects either the full or compact schema representation, \(N\) denotes deterministic domain-value normalization over the permitted value inventory \(V_i\), \(H\) emits an answer-shape instruction, and \(\oplus\) denotes serialization into a fixed prompt template. This equation defines the intended intervention interface; it is not evidence that any term improves performance.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: proposed MA-SQLGrid factorial intervention -->

The generator and validator are represented as

\[
\tilde{Y}_{i,s,h}=M(C_{i,s,h};\theta,r),\qquad
\hat{y}_{i,s,h}=R\!\left(\tilde{Y}_{i,s,h},D_i\right),
\]

where \(M\) is a frozen model configuration, \(r\) is a registered repeat or seed, and \(R\) performs syntax, safety, execution, and candidate-ranking operations without access to reference SQL or reference answers. Model identities, versions, decoding settings, and repeat counts remain execution-time fields and must be frozen before a result-bearing run.

<!-- CLAIM: MA-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: model execution and validator comparison plan -->

### 2.3. MA-SQLGrid Processing Pipeline

The proposed pipeline has four auditable stages. First, schema context is obtained from database introspection rather than hand-written table summaries. Second, a deterministic selector constructs the compact representation when the compact condition is active. Third, domain values and requested output shape are represented in separate prompt fields so that the shape intervention can be toggled without changing question text or schema scope. Fourth, generated candidates are checked under a read-only execution policy and mapped to a structured prediction record. These stages describe the implementation contract; their independent benefits await the registered model run.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: architecture and ablation plan -->

For the external portability protocol, full schemas are serialized from SQLite introspection, whereas compact schemas contain only automatically selected question-relevant schema elements. The answer-shape flag is produced by a deterministic heuristic over the question text. A low-relevance table perturbation is registered identically across the four cells for each external candidate, enabling a symmetry audit that checks whether only the intended factor-specific fields change.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/W4_MA_EXTERNAL_PROTOCOL_REPORT.md | KEYS: schema construction, shape heuristic, perturbation, symmetry audit -->

Candidate SQL is restricted to one read-only `SELECT` or `WITH` statement. Multi-statement inputs and write-capable statements are rejected, and external reference queries are executed against databases opened in read-only mode. Passing this policy establishes mechanical executability and limits accidental database mutation; it does not establish that an automatically generated question–SQL pair is semantically correct.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/W4_MA_EXTERNAL_PROTOCOL_REPORT.md | KEYS: sql safety and read-only evaluation -->

#### Proposed Algorithm 1. Evidence-Bound Factorial Inference and Evaluation

```text
Input: registered questions Q; read-only databases D; schema mode s;
       shape mode h; frozen model configuration theta; repeat r
For each question i in Q:
    introspect schema S_i and load permitted value inventory V_i
    construct G_s(x_i, S_i) and, if h = 1, construct H(x_i)
    serialize C_{i,s,h} with the frozen template
    assert that gold SQL, gold result, and gold-only fields are absent
    call the model once using the registered configuration
    parse candidates; reject multi-statement or write-capable SQL
    execute allowed candidates on D_i opened read-only
    select a candidate without reference SQL or reference results
    persist prediction, status, timing, usage, hashes, and error class
After all four cells complete:
    run Cartesian, duplicate, missing-record, cluster, and hash audits
    compute paired metrics, confidence intervals, tests, and corrections
Output: immutable prediction ledger, score ledger, audit report, result tables
```

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: gold isolation, audits, resume-safe execution interface -->

Algorithm 1 is a proposed result-bearing workflow. Its prompt-construction and audit stages have been exercised by the dry runs, but its model-call, candidate-selection, timing, usage, and comparative scoring stages are not yet evidenced. The final paper must replace this staging note with precise runtime identifiers and links to immutable output artifacts.

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/W2_REPORT.md | KEYS: no configured endpoint and zero model calls -->

### 2.4. Data Resources

#### 2.4.1. GridDB Primary Corpus

The primary corpus contains 200 question records divided into 20 development records and 180 records used by the registered factorial protocol. The latter partition has already been inspected during prior development and is therefore held out from the current prompt-building code but is not a previously unseen sealed test set. We use it for paired component estimation and label its evidence boundary explicitly rather than presenting it as an independently administered benchmark.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/dataset_inventory.json | KEYS: GridDB question_count and split profile -->

Gold SQL and gold-derived result fields are removed before prompt serialization. The dry-run builder also asserts that the exact gold SQL is absent from each prompt. This is a code-level leakage control for the evaluated input, but it cannot undo prior analyst exposure to the corpus or convert the partition into sealed evidence.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: gold isolation and evidence boundary -->

No explicit GridDB redistribution license has been located in the current data inventory. Accordingly, the revised paper should publish construction code, schemas or derived statistics where permitted, and checksum-based provenance, while withholding redistribution of the underlying records until permission is confirmed. The Data Availability Statement must distinguish accessible code and metadata from data whose redistribution status is unresolved.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/W2_REPORT.md | KEYS: license audit -->

#### 2.4.2. RTS-GMLC Portability Pilot

The RTS-GMLC pilot materializes 10 relational tables with 360,530 rows in total. It includes 120 branches, 73 buses, 158 generator records, 158 generator-cost records, 158 generator-constraint records, 26,352 load rows, 254,736 renewable-profile rows, 26,352 reserve-requirement rows, seven reserve-product rows, and 52,416 day-ahead dispatch rows. The demand, renewable, and reserve series cover 8784 hourly positions in 2020, whereas the materialized dispatch interval contains 336 hours for 156 generators.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/rts_gmlc_pilot/artifacts/build_summary.json | KEYS: table_counts,total_rows,time_coverage -->

The pilot generator creates 55 candidates from 11 template families, with five instances per family. Its development allocation comprises 30 training-visible, 10 validation-visible, and 15 holdout-labelled but unsealed candidates, with no template-family overlap across those allocations. All 55 reference statements executed successfully during construction, but all labels and questions are automatic and zero candidates have completed human review.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/rts_gmlc_pilot/W3_RTS_GMLC_REPORT.md | KEYS: candidates,families,splits,execution,human_review -->

The pinned RTS-GMLC source includes permission to use, copy, and distribute while requiring retention of its notice and acknowledgement of the US Department of Energy, NREL, and Alliance contributors. Because the captured notice ends mid-sentence, it is preserved verbatim in provenance and requires legal or repository-owner review before redistribution of the derived database.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/rts_gmlc_pilot/W3_RTS_GMLC_REPORT.md | KEYS: licensing caveat -->

#### 2.4.3. SimBench Portability Pilot

The SimBench pilot uses one `1-MV-urban--0-sw` network and materializes eight tables: one network, two voltage levels, 144 buses, 147 lines, two transformers, 139 loads, 134 generators, and 305 switches. It provides 36 automatic candidates, with six examples in each of six query classes: single-table retrieval, filtering, aggregation, joins, top-k retrieval, and topology queries.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/simbench_pilot/data_card.json | KEYS: network,tables,query_count,query_classes -->

Four SimBench reference queries return empty result sets: `SB-AUTO-008`, `SB-AUTO-009`, `SB-AUTO-010`, and `SB-AUTO-035`. They are retained to expose empty-result behavior rather than silently filtering difficult cases. An empty result is not counted as evidence of semantic invalidity, but it must be reported separately because result-set equality is less discriminating when both reference and predicted queries return no rows.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/simbench_pilot/W3_SIMBENCH_REPORT.md | KEYS: empty_result_query_ids and retention policy -->

The source is pinned to SimBench 1.6.2. The database is identified as ODbL, database contents as DbCL, and code as BSD-3-Clause. Publication artifacts must preserve attribution and share-alike requirements where applicable, and redistribution of the derived database should be reviewed against those terms rather than inferred from the code license alone.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/simbench_pilot/data_card.json | KEYS: source_version and licenses -->

#### 2.4.4. Human-Review Boundary

A review packet exists for all 91 external candidates, but no completed expert forms are available. Machine triage marks four records high priority, 69 medium priority, and 18 low priority; it also flags four empty results, six outputs exceeding 50 rows, 44 cases without an explicit unit in the question, 57 cases with high within-family similarity, and 22 top-k tie-handling hints. These are screening signals for reviewers, not expert judgements or benchmark certification.

<!-- CLAIM: MA-C06 | STATUS: HUMAN-DEPENDENT | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/human_review_packet/W4_MA_HUMAN_REVIEW_PACKET_REPORT.md | KEYS: review_status and machine_triage_counts -->

Because sealing cannot be applied retroactively to development-visible material, a future confirmatory external set should be newly authored or deeply rewritten and administered under a documented access protocol. Until that gate is completed, the 91 candidates will be described as an automatic development and portability set, never as human-gold, expert-validated, sealed, or publication-ready gold data.

<!-- CLAIM: MA-C05 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/human_review_packet/W4_MA_HUMAN_REVIEW_PACKET_REPORT.md | KEYS: nonhuman,nonsealed boundary and recommended future set -->

### 2.5. Registered Experimental Protocol

For every included question, the protocol constructs all four factorial cells using the same question identifier, database snapshot, prompt template version, and perturbation assignment. Only schema scope and shape-hint presence may differ according to the registered cell. The GridDB dry run contains exactly 180 records in each cell; the external dry run contains 91 in each cell, and both audits report complete Cartesian coverage.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: GridDB balance and Cartesian audit -->

The result-bearing run should freeze the selected model configurations, decoding parameters, repeat identifiers, retry policy, and failure accounting before the first paid or remote call. Every scheduled cell must produce either a prediction record or a terminal error record; resumptions must not overwrite completed records. Endpoint availability and final model identities were not established during W2, so they remain explicit pre-run gates rather than hidden degrees of freedom.

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/W2_REPORT.md | KEYS: endpoint audit and zero calls -->

Primary comparisons are compact versus full schema at fixed shape status and shape present versus absent at fixed schema status. Secondary comparisons estimate the interaction, evaluate error classes, and contrast GridDB with the automatic external portability set without pooling their semantic-validity claims. Any model-to-model comparison is secondary to the within-question intervention contrasts and must retain the same registered prompt and scoring contracts.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: factorial estimands and cross-dataset analysis -->

### 2.6. Outcomes, Scoring, and Failure Taxonomy

For question \(i\), define strict execution correctness as

\[
z_{i,s,h,r}=\mathbf{1}\!\left[\operatorname{Exec}(\hat{y}_{i,s,h,r},D_i)
\equiv \operatorname{Exec}(y_i^\star,D_i)\right],
\]

where equivalence follows one frozen contract for column identity, row multiplicity, row ordering, null values, and numeric tolerance. The final implementation must report the strict contract and any diagnostic alternative separately; projection-tolerant scoring must not replace the primary outcome after results are observed.

<!-- CLAIM: MA-C04 | STATUS: PROHIBITED | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/legacy_rescore_summary.json | KEYS: scoring-contract sensitivity -->

The principal aggregate is execution accuracy, \(\bar{z}_{s,h}=N^{-1}\sum_i z_{i,s,h}\). We will also report syntax-valid rate, safe-executable rate, empty-result rate, and mutually exclusive terminal error categories. For the SimBench subset, the four known empty-reference cases will be shown as a labelled sensitivity stratum in addition to their inclusion in the complete-set analysis.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/simbench_pilot/W3_SIMBENCH_REPORT.md | KEYS: empty-result cases; proposed reporting stratum -->

Efficiency outcomes are proposed as prompt tokens, completion tokens, end-to-end latency, successful-query latency, and monetary cost under the price schedule recorded at execution time. These outcomes will be summarized jointly with correctness and failure counts; no efficiency advantage is currently claimed because no registered model-call ledger exists.

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w2_ma/W2_REPORT.md | KEYS: zero model calls and absent usage ledger -->

Validator effects require a paired comparison between the frozen validation/ranking procedure and a registered alternative applied to identical raw candidate outputs. Repair success must be distinguished from changes caused by access to additional candidates or reference information. Until that candidate-level replay is executed, the manuscript will describe validation as a method component and will not attribute an accuracy gain to it.

<!-- CLAIM: MA-C08 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: validator ablation requirement -->

### 2.7. Statistical Analysis

The two marginal intervention estimands and the interaction are proposed as

\[
\Delta_{S}=\tfrac12[(\bar z_{1,0}-\bar z_{0,0})+(\bar z_{1,1}-\bar z_{0,1})],
\]

\[
\Delta_{H}=\tfrac12[(\bar z_{0,1}-\bar z_{0,0})+(\bar z_{1,1}-\bar z_{1,0})],
\]

\[
\Delta_{SH}=(\bar z_{1,1}-\bar z_{1,0})-(\bar z_{0,1}-\bar z_{0,0}).
\]

Positive values denote higher strict execution accuracy for compact schema, shape guidance, and their difference-in-differences interaction, respectively. These definitions are prospective and contain no observed effect estimate.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: registered factorial contrasts -->

All uncertainty calculations preserve question-level pairing. We propose question-clustered paired bootstrap intervals for accuracy differences and exact McNemar tests for prespecified binary pairwise contrasts. When multiple primary or secondary contrasts are tested within one model–dataset family, Holm correction will control the family-wise error rate. Raw and adjusted p-values, effect sizes, confidence intervals, discordant-pair counts, and the number of analysable question clusters will be reported together.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: paired bootstrap, exact McNemar, Holm plan -->

If stochastic repeats are used, predictions remain nested within questions and are not treated as independent observations. The final analysis plan must freeze whether repeats are aggregated per question or incorporated through a hierarchical resampling unit before inspecting outcomes. Missing and terminal-error records remain failures in the intention-to-evaluate denominator, while infrastructure-wide outages trigger a documented rerun rather than selective deletion.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: repeat handling and failure policy to freeze -->

### 2.8. Reproducibility and Data Governance

The GridDB dry-run manifest records a prompt hash of `28009f...ad5`, a data hash of `199fcf...f266`, a code hash of `8d94...43b`, and a configuration hash of `62a0...029b`. The external protocol records prompt hash `d8492231...a004` and reference-result hash `384ce242...ec8`. These abbreviated values are for prose readability; the final reproducibility table must copy the full digests directly from the manifests.

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w1_validation/ma_factorial_dryrun/manifest.json | KEYS: prompt_hash,data_hash,code_hash,config_hash -->

The external manifest pins RTS-GMLC database, schema, question, and source-manifest hashes and records source commit `3ece0...ab4`; it likewise pins the SimBench artifacts and source commit `c426...af7`. Together with the 364-record Cartesian and leakage audits, these identifiers make the automatic protocol reconstructable, but they do not supersede the source-license conditions or the absent human-review gate.

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/artifacts/manifest.json | KEYS: source_commits,artifact_hashes,audit -->

Every result-bearing run should preserve a run identifier, repository revision, configuration snapshot, model and endpoint identifiers, seed or repeat identifier, start and completion times, environment lock, stdout and stderr, usage accounting, and checksums for prompts, predictions, scores, and tables. The Data Availability Statement should enumerate each released artifact and separately explain restrictions caused by GridDB’s unresolved license, RTS notice obligations, and SimBench ODbL/DbCL terms.

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: execution provenance and data availability plan -->

## Proposed Table Interfaces

### Table 1. Dataset and Evidence Characteristics

| Dataset | Database scope | Questions | Construction | Human review | Sealed | License/redistribution note | Permitted claim |
|---|---:|---:|---|---|---|---|---|
| GridDB | Local maintenance database | 200 total; 20 development, 180 factorial | Existing corpus | Previously inspected | No | Explicit license unresolved | Paired development-visible factorial evaluation |
| RTS-GMLC pilot | 10 tables; 360,530 rows | 55 | 11 automatic families | None completed | No | Preserve source notice and credits; review redistribution | Mechanical portability and, after review, scoped external evaluation |
| SimBench pilot | 1 network; 8 tables | 36 | 6 automatic query classes | None completed | No | ODbL/DbCL for data; BSD-3-Clause code | Mechanical portability and, after review, scoped external evaluation |

<!-- CLAIM: MA-C02 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/artifacts/manifest.json | KEYS: consolidated dataset interface -->

### Table 2. Factorial Conditions

| Cell | Schema scope | Shape hint | GridDB prompts | External prompts | Controlled invariant fields |
|---|---|---|---:|---:|---|
| full_shape_absent | Full | Absent | 180 | 91 | Question, database, template, perturbation |
| full_shape_present | Full | Present | 180 | 91 | Question, database, template, perturbation |
| compact_shape_absent | Compact | Absent | 180 | 91 | Question, database, template, perturbation |
| compact_shape_present | Compact | Present | 180 | 91 | Question, database, template, perturbation |

<!-- CLAIM: MA-C01 | STATUS: ELIGIBLE-DIAGNOSTIC | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/w1_validation/ma_factorial_dryrun/manifest.json | KEYS: cells and per-cell counts -->

### Table 3. Prediction Ledger Interface

| Field group | Required fields |
|---|---|
| Identity | run_id, dataset_id, question_id, model_id, repeat_id, cell_id |
| Provenance | code_hash, data_hash, config_hash, prompt_hash, environment_hash |
| Output | raw_response, parsed_sql, terminal_status, error_class |
| Execution | safety_status, execution_status, result_hash, row_count |
| Resources | prompt_tokens, completion_tokens, latency_ms, cost_currency |
| Scoring | strict_correct, diagnostic_correct, scorer_version |

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: proposed immutable run ledger -->

### Table 4. Main Factorial Results — Reserved Interface

| Dataset | Model | Repeat policy | Full/no shape | Full/shape | Compact/no shape | Compact/shape | \(\Delta_S\) [95% CI] | \(\Delta_H\) [95% CI] | \(\Delta_{SH}\) [95% CI] |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| GridDB | **PENDING** | **PENDING** | — | — | — | — | — | — | — |
| RTS-GMLC automatic set | **PENDING** | **PENDING** | — | — | — | — | — | — | — |
| SimBench automatic set | **PENDING** | **PENDING** | — | — | — | — | — | — | — |

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: empty result interface; do not populate without E4 -->

### Table 5. Statistical Contrast Interface

| Family | Contrast | Effect | 95% paired cluster-bootstrap CI | Discordant pairs | Exact McNemar p | Holm-adjusted p |
|---|---|---:|---|---:|---:|---:|
| Primary | Compact vs. full, shape absent | — | — | — | — | — |
| Primary | Compact vs. full, shape present | — | — | — | — | — |
| Primary | Shape vs. absent, full schema | — | — | — | — | — |
| Primary | Shape vs. absent, compact schema | — | — | — | — | — |
| Secondary | Difference-in-differences | — | — | n/a | n/a | — |

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/W1_ACCEPTANCE_REPORT.md | KEYS: statistical audit interface -->

### Table 6. Reproducibility and Data-Governance Interface

| Artifact | Version/commit | Full checksum | Release status | License/restriction | Verification command |
|---|---|---|---|---|---|
| GridDB factorial prompts | Frozen manifest | From manifest | Metadata/code proposed | Source-data license unresolved | **PENDING** |
| RTS-GMLC derived database | `3ece0...ab4` | From manifest | Review before redistribution | Notice and credit obligations | **PENDING** |
| SimBench derived database | `c426...af7`; SimBench 1.6.2 | From manifest | Review share-alike terms | ODbL/DbCL | **PENDING** |
| Predictions and scores | **PENDING RUN** | **PENDING RUN** | Not available | Model-provider terms to record | **PENDING** |

<!-- CLAIM: MA-C09 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/artifacts/manifest.json | KEYS: proposed provenance table populated only with existing protocol evidence -->

## Figure and Diagram Interfaces

1. **Figure 1, system diagram:** question and introspected schema → factorial context builder → frozen model → safety/parser/executor → reference-free ranker → prediction ledger. Visually separate method components from the gold-only scorer.
2. **Figure 2, experimental design:** paired question clusters branching into four cells, followed by marginal and interaction contrasts. Mark GridDB as development-visible and the external records as automatic/non-human/non-sealed.
3. **Figure 3, data construction:** pinned RTS-GMLC and SimBench sources → relational materialization → automatic candidate templates → SQL safety/execution → review packet → incomplete human-review gate.
4. **Figure 4, results:** reserved forest plot for \(\Delta_S\), \(\Delta_H\), and \(\Delta_{SH}\) with paired confidence intervals; create only after E4 artifacts exist.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: proposed figure interfaces -->

## Reference Placeholders (Do Not Fabricate Metadata)

- `[REF-TEXT2SQL-SURVEY]`: recent peer-reviewed survey defining executable text-to-SQL evaluation.
- `[REF-SCHEMA-LINKING]`: primary source for schema linking or schema selection.
- `[REF-EXECUTION-GUIDED]`: primary source for execution-guided decoding or reference-free validation.
- `[REF-RTS-GMLC]`: canonical RTS-GMLC paper and official repository/data citation.
- `[REF-SIMBENCH]`: canonical SimBench paper and official dataset/software citation.
- `[REF-MCNEMAR]`: primary or standard statistical reference for the exact paired McNemar test.
- `[REF-PAIRED-BOOTSTRAP]`: statistical reference for question-clustered paired bootstrap confidence intervals.
- `[REF-HOLM]`: original Holm multiple-testing procedure.
- `[REF-MDPI-DATA]`: current *Applied Sciences*/MDPI research-data and reproducibility guidance.

<!-- CLAIM: MA-C03 | STATUS: PENDING-EVIDENCE | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/MASTER_EXECUTION_PLAN.md | KEYS: citation acquisition list -->

## Pending-Evidence Register

- **MA-C03 — PENDING-EVIDENCE:** Execute the frozen 2×2 model protocol and produce prediction, score, audit, and statistical artifacts before claiming compact-schema, shape-hint, or interaction effects.
- **MA-C06 — HUMAN-DEPENDENT:** Obtain independent completed review forms and adjudication for an external set; the current 91 candidates remain automatic and development-visible.
- **MA-C08 — PENDING-EVIDENCE:** Replay identical raw candidates through the registered validator ablation before claiming repair or ranking benefit.
- **MA-C09 — PENDING-EVIDENCE:** Record model usage, latency, failure, price-version, and cost fields before describing an accuracy–cost–latency trade-off.
- **MA-C04 — PROHIBITED:** Do not claim independent content-retrieval improvement from the legacy joint-condition experiment.
- **MA-C05 — PROHIBITED:** Do not call the 91 external candidates human-gold, expert-validated, sealed, or publication-ready gold data.
- **MA-C07 — LEGACY-ONLY:** Keep earlier GridDB model scores in a labelled historical diagnostic subsection; do not merge them into the new factorial result table.

<!-- CLAIM: MA-C07 | STATUS: LEGACY-ONLY | ARTIFACT: paper_projects/applied_sciences_dual_rebuild/CLAIM_LEDGER.md | KEYS: MA claim states and release gates -->
