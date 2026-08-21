# MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases

**Round 1 section draft for Applied Sciences**  
**Evidence status:** mixed inherited evidence plus an unevaluated prospective coordination core  
**Citation rule:** this draft uses only citation keys already present in `manuscript_applsci/references_verified.bib`; no bibliography entry is added or modified.

**Authors:** Liu Bijing \(^{1,2}\), Sun Chenglong \(^{1,2}\), and Yang Yong \(^{1,2,*}\)  
**Affiliation 1:** NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China  
**Affiliation 2:** Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China  
**Corresponding author:** Yang Yong; email address to be completed manually before submission

> Assembly note. The original-title DOCX supplies the five-role architectural intention, but none of its unsupported public-benchmark, large-corpus, agent-ablation, or claimed counterfactual-gain numbers are retained. The quantitative text below is restricted to audited GridDB, component, BIRD, multi-state, and retrospective-coverage artifacts. “Retrospective offline coordination diagnostic” is never treated as an accuracy result.

## Abstract

Natural-language access to power-grid databases requires more than syntactically valid SQL: a query must use the intended schema elements, remain read-only, execute under a defined database state, and expose enough evidence for human review. This paper presents MA-SQLGrid, a structured multi-agent framework that separates query analysis, schema grounding, SQL synthesis, safety and execution validation, and counterfactual criticism, with a deterministic adjudicator coordinating the roles through an append-only blackboard. The implemented coordination core rejects unsafe or multi-statement SQL, abstains when no eligible candidate exists, records missing counterfactual evidence as unknown, and seals its decision trace before any gold query or result is loaded. We integrate this architecture with previously frozen evidence rather than relabeling earlier single-generation experiments as multi-agent runs. The inherited GridDB study evaluates two quantized local backbones in a paired 2-by-2 prompt design over 180 questions, producing 1440 predictions. No primary factorial execution effect or cross-backbone modifier survived Holm correction, although the composite structural/SQL-operation hint increased projected-column adherence. A separate 700-call component study found a positive presented-value effect for Qwen (+0.1059; 95% composition-sensitivity interval [0.0282, 0.2013]; adjusted p = 0.0310) but not Granite; deterministic candidate selection met the declared efficacy rule for neither backbone. On BIRD Mini-Dev, 5000 generation calls yielded 4000 independently re-executed final predictions; the descriptively best methods reached execution accuracy 0.394 for Qwen and 0.236 for Granite. A 15-state GridDB stress test produced logical-AND agreement rates from 0.6212 to 0.8182, with no registered effect surviving correction. Finally, a hash-locked retrospective replay found at least two safe candidates with consistent frozen snapshot evidence for 172 of 180 questions. That replay measures candidate-pool coverage only, not accuracy or multi-agent improvement. The combined evidence supports an auditable framework and a prospectively testable coordination design, not a deployed-system or universal robustness claim.

**Keywords:** text-to-SQL; multi-agent systems; power-grid databases; schema grounding; execution validation; counterfactual testing; reproducibility

## 1. Introduction

Power-grid organizations maintain relational data about assets, locations, topology, sensor readings, work orders, technicians, and maintenance activity. SQL provides precise access to these records, but it requires knowledge of table names, join keys, identifiers, units, aggregation conventions, and local coding rules. Text-to-SQL systems aim to reduce this access barrier by translating a natural-language request into an executable query. In an engineering workflow, however, a fluent query is not sufficient evidence of correctness. A query can execute while selecting the wrong status field, omitting a required filter, using an unintended join path, or returning the right number of columns with the wrong content.

Cross-database benchmarks such as Spider and BIRD have made schema generalization and realistic database content central evaluation concerns \cite{yu2018spider,li2023bird}. Schema-aware models, constrained decoding, context selection, decomposition, and execution guidance address different failure surfaces \cite{wang2020ratsql,scholak2021picard,nan2023enhancing,pourreza2023dinsql,talaei2024chess}. These methods also expose a design problem: the steps that improve generation are frequently bundled together. A system may change schema serialization, value presentation, domain normalization, structural hints, candidate count, and repair policy simultaneously. An observed score difference then cannot be assigned cleanly to “schema linking,” “reasoning,” or “validation.”

The original MA-SQLGrid concept addressed this problem through five specialized roles: an analyst interprets the request, a cartographer maps it to the schema, a synthesizer proposes SQL, a validation engine checks safety and execution, and a counterfactual critic probes robustness. A deterministic controller resolves the resulting evidence. This separation remains useful because each role has a distinct contract and failure mode. It also makes the trace inspectable: a reviewer can distinguish what the question parser inferred, which schema elements were retained, which candidates were proposed, which candidates executed, and why a final candidate was selected or rejected.

The architecture must nevertheless be separated from the evidence used to evaluate it. The inherited GridDB factorial study was not a multi-agent execution. It used one model generation per question and prompt cell, followed by deterministic parsing, read-only validation, execution, and offline scoring. The BIRD study likewise compared four frozen prompting procedures rather than five interacting agents. These assets can motivate modules, supply baselines, and test replay interfaces, but they cannot be renamed as results of the new coordination core.

This distinction leads to the paper’s central research program. First, can role-specific, structured handoffs be implemented with a gold-isolated and auditable selection boundary? Second, what do the existing controlled experiments establish about context packages, structural hints, presented values, candidate selection, public-database transfer, and multi-state execution agreement? Third, do the frozen assets contain enough genuinely distinct candidates to support a future matched coordination experiment without new labels or fabricated data? A final question—whether the full multi-agent condition improves execution accuracy under a fixed generation budget—remains prospectively testable and is not answered by retrospective replay.

The paper makes four contributions.

1. **A testable multi-agent coordination core.** MA-SQLGrid defines five specialist roles plus a deterministic adjudicator. An append-only blackboard records every typed handoff and emits a canonical SHA-256 audit digest. Gold SQL, gold results, and correctness labels are excluded from all pre-evaluation interfaces.
2. **A conservative integration of frozen experimental assets.** The paper retains a 1440-prediction paired GridDB factorial experiment, a 700-call prospective component study, a 25,920-row multi-state execution ledger, and a 5000-call BIRD Mini-Dev comparison without altering their run identities, denominators, or method labels.
3. **A fail-closed retrospective replay.** The replay verifies the hashes of two 720-row prediction ledgers and the 25,920-row state ledger, deduplicates existing SQL per question, and exercises the new validator, critic, and adjudicator without making a model call. Questions with insufficient candidate coverage are retained as failures of the diagnostic gate.
4. **A prospectively falsifiable experiment design.** Matched single, staged, multi-candidate, and full coordination conditions are specified with equalized candidate/call budgets, sealed blackboards, clustered inference, explicit incident retention, and abstention reporting.

The resulting contribution is deliberately narrower than the original manuscript’s claims. No Spider or WikiSQL experiment is reported, no unsupported large power-grid question–SQL corpus is asserted, and no accuracy advantage is attributed to the new multi-agent framework before the prospective coordination experiment is frozen and executed.

## 2. Related Work

### 2.1 Text-to-SQL Evaluation and Schema Generalization

Text-to-SQL systems map a natural-language question and database schema to a query. Spider established a cross-domain setting with previously unseen databases, drawing attention to table selection, joins, grouping, nesting, and ordering \cite{yu2018spider}. BIRD extends public evaluation toward larger and more content-rich databases \cite{li2023bird}. These resources are important external comparators, but a benchmark result depends on the exact split, evaluator, database engine, execution boundary, and model configuration. The present paper therefore reports only the completed BIRD Mini-Dev protocol and makes no claim about datasets that were discussed but not run.

Exact SQL match and execution-based evaluation answer different questions. String match can penalize equivalent SQL, whereas result equality can reward nonequivalent queries on an insufficiently discriminating database state. Robust evaluation should retain predicted SQL, record execution failures, and specify the state on which equality was observed. MA-SQLGrid uses strict result equality for the inherited snapshot experiment and separately reports projected-column conformity and multi-state agreement. Neither auxiliary endpoint is described as semantic certification.

### 2.2 Schema Linking, Context Packages, and Output Contracts

Schema linking connects spans in a question to tables, columns, values, and foreign-key relations \cite{wang2020ratsql,lei2020reexamining,liu2022semantic}. Full-schema context preserves recall but can increase token cost and distraction. Compact context reduces the search space but risks dropping a required join key or predicate. Value examples can disambiguate coded attributes, while question-derived instructions can identify the required aggregation, result shape, ordering, or limit. These interventions are coupled in many practical systems.

The inherited GridDB factorial study isolates two implemented prompt factors: a full-DDL/global-values package versus a compact/domain-grounded package, and the absence versus presence of a composite structural/SQL-operation hint. The compact package is not a pure schema-length manipulation because it also changes value presentation and introduces corpus-tailored normalization rules. The hint is not merely a formatting instruction because it can include aggregation, grouping, projection, ordering, and limit guidance. The paper retains these precise labels instead of assigning broader causal interpretations.

Constrained generation and execution guidance reduce invalid candidates. PICARD constrains decoding so inadmissible SQL continuations can be rejected during generation \cite{scholak2021picard}. CHESS combines contextual grounding and SQL synthesis components \cite{talaei2024chess}. Other prompt-based methods investigate decomposition and representation choices \cite{nan2023enhancing,sun2023sqlprompt,pourreza2023dinsql}. MA-SQLGrid differs at the coordination boundary: its new core accepts externally produced candidates, checks them with deterministic contracts, and records evidence before selection. It does not claim that the current lexical cartographer or fixed adjudicator supersedes learned schema-linking systems.

### 2.3 Agentic Decomposition and Auditable Control

Agentic decomposition can make intermediate decisions explicit, but naming pipeline stages as agents does not establish a multi-agent benefit. Evidence of such a benefit requires a comparison that holds the model, data, decoding configuration, and generation budget constant. Otherwise, a multi-candidate system may improve simply because it receives more samples, while a repair system may consume more calls than its baseline.

MA-SQLGrid treats an agent as a role with a typed input/output contract rather than assuming that each role must be a separately hosted model. The Query Analyst and Schema Cartographer can be deterministic or model-assisted; the SQL Synthesizer can receive candidates from a frozen generator; the Validator uses a fixed read-only policy; the Counterfactual Critic consumes named state evidence; and the Adjudicator is deterministic. This implementation choice allows component substitutions to be tested without changing the blackboard schema. It also prevents the controller from hiding gold-guided selection behind an opaque “debate” label.

### 2.4 Power-Grid Data and External Validity

Power-system datasets combine topology, equipment attributes, measurements, time series, costs, and constraints. RTS-GMLC and SimBench provide reproducible engineering resources that can be transformed into relational structures \cite{barrows2020rts,meinecke2020simbench}. Their availability does not automatically create a text-to-SQL benchmark: natural-language questions, intended projections, units, ordering, ties, and reference SQL require semantic review.

The current external assets are consequently separated into evidence tiers. GridDB is a small synthetic maintenance-oriented case study. BIRD Mini-Dev supplies a public cross-database comparison. RTS-GMLC, SimBench, and NERC-derived question–SQL candidates are machine-screened silver resources, not expert gold. This distinction follows the broader engineering requirement that fluent model output and automatically generated references remain subject to qualified human inspection before operational use.

## 3. Task Definition and Data Resources

### 3.1 Task and Safety Contract

For question (x_i), read-only database (D_i), and introspected schema (S_i), a generator produces one or more candidate queries

\[
\mathcal{Y}_i=\{\widetilde{y}_{i1},\ldots,\widetilde{y}_{ik}\}.
\]

Before execution, each candidate must satisfy a single-statement read-only contract. The accepted leading form is `SELECT` or `WITH`; comments, multiple statements, write operations, schema changes, attachment commands, and pragmas are rejected. Execution evidence is obtained from a read-only database connection or from a frozen execution ledger whose identity is bound to the exact candidate source. A candidate is eligible for adjudication only when it is safe and executable.

The offline evaluator may later compare the selected query with a reference result. Let (E_i=1) when the selected SQL executes and its result equals the frozen reference result under the registered evaluator, and (E_i=0) otherwise. The reference SQL, reference result, (E_i), and any derivative correctness field are forbidden from the Query Analyst, Schema Cartographer, SQL Synthesizer, Validator, Counterfactual Critic, and Adjudicator inputs. Evaluation occurs only after the blackboard is sealed.

### 3.2 GridDB-Maintenance-v2

GridDB-Maintenance-v2 v0.1 is a synthetic SQLite case study with eight tables and 98 rows: `asset_types` (6), `assets` (18), `grid_topology` (9), `locations` (8), `maintenance_logs` (8), `sensor_readings` (26), `technicians` (8), and `work_orders` (15). It contains 200 natural-language–SQL records. Twenty records form a development partition and 180 form the factorial evaluation partition. All 200 reference queries executed during dataset generation.

The 180 evaluation records include 66 easy, 91 medium, and 23 hard items. They map to 70 normalized gold-SQL structural clusters, with cluster sizes from 1 to 19 and 58 singleton clusters. The evaluation partition had been visible during earlier project development. It is therefore a controlled finite-set case study, not a newly administered sealed benchmark or an unbiased estimate of production performance.

### 3.3 BIRD Mini-Dev

BIRD Mini-Dev contributes 500 public items over 11 SQLite databases. The authorized protocol `MA-PUBLIC-BIRD-MINIDEV-v1.1` froze item and method order, prompts, two local model files, evaluator behavior, Python 3.10.11/SQLite 3.40.1, and a zero-retry policy. Qwen and Granite each made 2500 generation calls: one call per item for direct prompting, decomposition, and schema selection, plus two adjacent calls for bounded execution repair. This produced 2000 final predictions per backbone and 4000 final predictions overall. An independent audit re-executed all 4000 predictions and 500 gold queries with zero score mismatches. Two earlier failed attempts, totaling 2476 physical calls, remain immutable incident records and are excluded from scoring.

### 3.4 Multi-State and External Diagnostic Assets

The GridDB reliability release contains 18 database states: the canonical snapshot, three insertion permutations, and 14 additional schema-valid stress states involving retained clones, attribute rotation, relation rewiring, numeric/time shifts, categorical covering, boundary values, null witnesses, anti-join coverage, isolated parents, topology motifs, and string decoys. The formal scorer produced 25,920 prediction-state rows ((1440\times18)). A prediction-blinded automated protocol admitted a 66-question subset for the primary 15-state semantic analysis and retained 114 order-sensitive questions as diagnostics. These constructed states are not operator-certified grid snapshots.

RTS-GMLC, SimBench, and NERC assets support schema-portability and annotation-pipeline diagnostics. Their labels are machine-adjudicated silver data. They must not be described as domain-expert judgements or included in an external accuracy denominator until qualified reviewers complete the specified semantic review.

### 3.5 Asset Provenance Classes

Every quantitative artifact is assigned one of four provenance labels.

- **Inherited:** a hash-consistent result from an existing frozen protocol, retaining its original run ID and denominator.
- **Recomputed:** a deterministic recalculation from inherited rows under a declared script and manifest.
- **New:** a result from a newly frozen, authorized prospective protocol.
- **Diagnostic:** an interface, coverage, sensitivity, or failure analysis that cannot support the primary performance claim.

The new coordination core is currently implementation evidence. Its retrospective replay is Diagnostic. Neither is a New execution-accuracy result.

## 4. MA-SQLGrid Framework

### 4.1 Architecture and Blackboard

MA-SQLGrid comprises five specialist roles coordinated by a deterministic controller. The controller is not treated as a sixth reasoning model. It enforces message order, calls the roles, applies the registered adjudication rule, and seals the trace. Each role posts a typed payload to an append-only blackboard. Messages receive consecutive sequence numbers, and the complete sealed trace is serialized canonically to a SHA-256 digest.

The blackboard has two purposes. First, it makes the collaboration observable: a failed query can be traced to an intent field, schema selection, candidate string, execution result, or state-specific objection. Second, it constrains leakage: the public coordination interface does not accept gold SQL, gold results, answer labels, or evaluator correctness. A late write after sealing raises an error.

**[FIGURE SLOT F1]** Five specialist roles around an append-only blackboard, with the deterministic controller shown as a control boundary rather than an LLM agent. The evaluator and gold results must be drawn outside the sealed boundary.

### 4.2 Query Analyst

The Query Analyst converts the question into a structured intent record. The implemented deterministic skeleton records the question identifier, lexical tokens, detected aggregation operators, whether ordering appears necessary, and an explicit limit when present. For example, “How many” maps to `COUNT`, while “highest” implies ordering and a one-row limit. This heuristic layer is intentionally small; it establishes a stable interface that can later accept a stronger parser without changing downstream message types.

The role does not select SQL and does not see execution correctness. Its output is a question-derived constraint set, not a claim that the natural-language intent has been fully understood.

### 4.3 Schema Cartographer

The Schema Cartographer maps lexical intent to tables, columns, and foreign-key edges. The current skeleton scores table and column token overlap deterministically, caps the selected table count, retains matching columns, and records unmatched question tokens. Existing GridDB assets provide a richer domain-grounded context builder with exact-value matching, corpus-tailored synonyms, normalization rules, and foreign-key expansion to at most six tables. That inherited builder can be connected through an adapter, but its GridDB-specific rules must remain disclosed.

This role exposes the schema recall–precision trade-off. Selecting too much context increases distraction and token cost; selecting too little can remove a required field or join. A production version should therefore record both the selected sub-schema and its fallback behavior when confidence is low.

### 4.4 SQL Synthesizer

The SQL Synthesizer packages one or more externally produced SQL candidates. The new core contains no model client and performs no hidden API call. It canonicalizes whitespace and terminal semicolons, removes exact duplicates without changing first occurrence, assigns stable candidate identifiers, and records source and ordinal position. An empty candidate set is rejected.

Separating candidate generation from coordination is methodologically important. It permits the same frozen candidates to be replayed under alternative adjudication rules and permits a future experiment to equalize generation calls across conditions. Candidate diversity, however, is not free evidence: a method with more candidates has a larger opportunity to contain a correct query. The prospective design must therefore hold candidate count and physical call budget constant for the primary coordination contrast.

### 4.5 Validation Engine

The Validation Engine first applies the read-only SQL contract. Unsafe, commented, or multi-statement outputs are marked ineligible and are never passed to an executor. Safe candidates are executed through an injected read-only executor or matched to frozen T0 execution evidence. The returned record contains safety, single-statement status, executability, result-shape conformity, ordering conformity, presented-value hits, an error field, and an optional result hash.

No failed call is silently retried. When execution evidence is unavailable, the candidate is marked non-executable for adjudication rather than assumed valid. When identical SQL strings are associated with conflicting frozen evidence, the replay fails closed for that candidate.

### 4.6 Counterfactual Critic

The Counterfactual Critic consumes named state results and records the number of evaluated, passed, and failed states. A state passes only when the candidate executes and the registered reference-free equivalence predicate passes. Duplicate state identifiers are rejected. Missing states remain unknown, and coverage is complete only when the observed state set exactly matches the registered set.

This interface is stricter than the original manuscript’s proposed paraphrase-based reasoning. The available formal-v5 state ledger compares prediction results with gold results. Those fields are valid for offline evaluation but would leak correctness information if used to choose a candidate. The retrospective replay therefore supplies no counterfactual pass labels to the critic and records zero reference-free counterfactual coverage. A future prospective run must define candidate-level robustness evidence that does not use gold during adjudication, for example invariants specified from the question and schema before candidate generation.

### 4.7 Deterministic Adjudicator and Abstention

Eligibility requires safety and successful execution. For eligible candidates, the frozen implementation assigns 40 points for safety, 40 for execution, 10 for shape conformity, 5 for ordering conformity, and up to 5 points for presented-value hits. It then applies the following deterministic tie order: validation points, counterfactual pass rate when available, number of evaluated counterfactual states, and original candidate order. Floating-point comparison is avoided in the implemented pass-rate calculation. If no candidate is eligible, the system abstains.

For the retrospective coverage diagnostic, comparative adjudication is permitted only when at least two distinct candidates are safe and supported by consistent frozen T0 execution evidence. Questions with one unique or one eligible candidate remain in the ledger with a fail-closed status.

**[ALGORITHM SLOT A1]** Serialize role handoffs, validate candidates, bind named state evidence, adjudicate deterministically, seal blackboard, then load gold only for offline evaluation.

## 5. Experimental Design

### 5.1 Inherited GridDB Factorial Experiment

The inherited paired experiment crosses context package (c\in\{0,1\}) and composite hint (h\in\{0,1\}). F00 uses full DDL and a global value dictionary without the hint; F01 adds the hint; F10 uses compact domain-grounded context without the hint; and F11 combines compact context and the hint. Each of the same 180 questions appears in all four cells for each backbone, yielding 720 Qwen and 720 Granite predictions.

The Qwen 2.5 Coder 7B Q4_K_M and Granite 3.3 8B Q4_K_M configurations use temperature zero and fixed model snapshots. Each prompt produces exactly one response. The parser retains the first SQL candidate through the first semicolon, and the validator applies a single-statement read-only policy to the parsed candidate. There is no candidate ranking, multi-agent negotiation, or repair in this formal factorial experiment. Gold SQL and reference results are excluded from prompt construction and generation.

Strict execution equality is the primary endpoint. A common-target projected-column indicator is a secondary manipulation check. Inference uses paired finite-set contrasts over the 180 questions, with normalized-SQL structural clusters as the dependence proxy, registered sign-flip tests, composition-sensitivity bootstrap intervals, and Holm correction across the declared families. The intervals describe sensitivity to the observed corpus composition and are not population confidence intervals.

### 5.2 Prospective Component Study

The separately frozen component study contains 700 scored calls. E1 compares candidate generation with and without presented value evidence on the eligible question subsets. E2 requests up to three candidates and compares a deterministic reference-answer-independent selector with the first candidate on all 180 questions. Candidate selection is sealed before gold SQL or results are loaded. Rescue, harm, and oracle-at-three are reported descriptively; oracle-at-three is a post hoc upper-bound diagnostic and is not deployable.

E1 and E2 use 20,000 group-bootstrap draws and 100,000 group sign flips, with Holm correction applied to their registered contrast families. A positive component result requires a positive estimate, an interval excluding zero, and adjusted (p<0.05). A positive result on one backbone is not treated as replication.

### 5.3 Multi-State Reliability Study

The retrospective v5 reliability protocol first reproduced all 1440 canonical T0 labels. It then executed every prediction over 18 registered states, producing 25,920 atomic rows. The primary semantic analysis uses a prediction-blinded 66-question subset across 15 semantic states. It defines a logical-AND endpoint: a prediction passes only when it agrees with the reference on every included state. The remaining 114 order-sensitive questions were executed but retained as diagnostics.

The same within-backbone and cross-backbone factorial contrasts form a separate nine-test Holm family. Because the eligible subset maps to only 12 normalized-SQL clusters, the release enumerates all (2^{12}=4096) sign assignments for sensitivity. This is a constructed-state robustness test, not proof of equivalence over arbitrary databases.

### 5.4 Public BIRD Comparison

The BIRD protocol compares direct prompting, decomposition, schema selection, and bounded execution repair under two local backbones. Each method has a fixed call pattern and zero retries. Pairwise method differences are evaluated by exact database-cluster sign randomization across 11 databases, followed by Holm correction. The experiment is a same-environment public comparison. It is not a reproduction of DKA-SQL and does not use an official DKA-SQL implementation \cite{bian2025dkasql}.

### 5.5 Retrospective Offline Coordination Diagnostic

The replay reads three immutable inputs after verifying their SHA-256 values: 720 Qwen predictions, 720 Granite predictions, and 25,920 formal-v5 atomic rows. For each GridDB question, it pools the eight already generated outputs from two backbones and four prompt cells, canonicalizes SQL, and removes exact duplicates. Frozen T0 fields provide only safety-independent execution and metadata-shape evidence. The validator rejects unsafe candidates; the critic records counterfactual evidence as unavailable because the existing state-agreement labels are gold-relative; and the adjudicator acts only when at least two candidates remain eligible.

This design is intentionally diagnostic. Candidates were generated under different models and prompt conditions, so the pool does not represent a deployable matched multi-agent run. No output is compared with gold to produce an accuracy number. The diagnostic asks only whether the existing assets have enough diversity and reference-free execution evidence to exercise the coordination interfaces.

### 5.6 Planned Prospective Coordination Experiment

The next frozen experiment should compare four matched conditions:

1. `SINGLE`: one direct candidate and no inter-role coordination;
2. `STAGED`: query/schema handoffs, one candidate, and validation without alternative selection;
3. `MULTI_NO_CF`: a fixed candidate budget, validation, and deterministic adjudication without counterfactual evidence;
4. `MULTI_FULL`: the same candidate pool plus a pre-registered reference-free state or invariant suite.

The primary contrast must equalize model snapshot, question order, database state, decoding parameters, candidate count, and physical generation-call budget. If budget cannot be equalized, a separate budget-controlled estimand must be registered. The primary endpoint is paired execution accuracy after the blackboard is sealed. Secondary endpoints include valid SQL rate, unsafe SQL rate, abstention, rescue and harm, state coverage, latency, and token use. Every attempted call receives a terminal ledger row; failures and incidents are retained without silent retry, deletion, or denominator changes.

**[EVIDENCE SLOT E-P1: PROSPECTIVE COORDINATION]** Insert only after the protocol hash is independently audited and explicitly authorized. Required fields: protocol ID and SHA-256, model/data/runtime hashes, exact physical calls, terminal status counts, eligible denominator, execution accuracy by condition, paired effect estimates, multiplicity-adjusted tests, abstentions, and incident statement.

## 6. Results and Evidence Slots

### 6.1 Complete GridDB Cell Results

All 1440 scheduled predictions are present, and independent SQLite re-execution reproduced the stored execution verdicts. Table 1 reports strict execution equality.

| Backbone | F00 full/no hint | F01 full/hint | F10 compact/no hint | F11 compact/hint |
|---|---:|---:|---:|---:|
| Qwen | 0.4222 | 0.7167 | 0.4333 | 0.6000 |
| Granite | 0.4278 | 0.5556 | 0.4111 | 0.6000 |

The common-target projected-column diagnostic is 0.5222 in F00 for both backbones. Qwen obtains 0.9667, 0.5889, and 0.9611 in F01, F10, and F11; Granite obtains 0.8778, 0.5667, and 0.9222. These values demonstrate that returning the expected number of columns is easier than returning the intended rows. For example, Qwen F01 reaches 0.9667 on projected-column conformity but 0.7167 on execution equality.

### 6.2 Factorial Effects and Multiplicity

For Qwen, the composite-hint execution effect is +0.2306, the package–hint interaction is −0.1278, and the compact-package main effect is −0.0528. Granite’s corresponding estimates are +0.1583, +0.0611, and +0.0139. None of the nine primary execution tests survives Holm correction. Qwen’s hint effect has raw/adjusted (p=0.01372/0.09604), its interaction (0.00919/0.07352), and the cross-backbone hint modifier (0.00640/0.05760). The paper therefore does not describe any primary factorial execution effect or modifier as statistically nonzero.

In the separately corrected secondary family, the common-target hint effects survive: +0.4083 for Qwen (adjusted (p=0.000090)) and +0.3556 for Granite (adjusted (p=0.01944)). Because the hint supplies structural information later scored by this endpoint, these are manipulation-check results rather than independent evidence of semantic benefit.

### 6.3 Component Results

The component run completed all 700 scored calls. Presented value evidence increased Qwen first-candidate execution equality by +0.1059 over 170 eligible questions (95% composition-sensitivity interval [+0.0282, +0.2013], adjusted (p=0.0310)). Granite’s estimate was zero with an interval spanning zero. The cross-backbone modifier did not meet the registered rule, so the Qwen result is not described as replicated across backbones.

The deterministic selector changed 24 Qwen and 36 Granite choices. Relative to the first candidate, it rescued eight and harmed one Qwen question, and rescued ten while harming none for Granite. The execution effects were +0.0389 and +0.0556. Neither survived its two-test Holm family. Oracle-at-three values of 0.6389 and 0.4667 are gold-only diagnostics and are not selector results available at deployment.

### 6.4 Multi-State Reliability Results

The v5 scorer produced all 25,920 registered rows, and its T0 slice reproduced 1440 of 1440 canonical snapshot labels. Across the 66-question automatic subset, 15-state logical-AND rates ranged from 0.6212 (Granite F01) to 0.8182 (Granite F00). All nine Holm-adjusted values equal 1.0000 under the exact cluster-sign sensitivity analysis. No context, hint, interaction, or cross-backbone multi-state effect meets the declared evidence rule. The rates characterize agreement over the constructed witness states, not population accuracy or human-certified semantic equivalence.

### 6.5 Public BIRD Results

Across 500 BIRD Mini-Dev items, Qwen schema selection was descriptively best at 0.394 execution accuracy, followed by direct prompting at 0.378, bounded execution repair at 0.348, and decomposition at 0.302. Granite bounded execution repair was descriptively best at 0.236; its other methods ranged from 0.202 to 0.210. After Holm adjustment, two Qwen contrasts remained: decomposition was 0.076 below direct prompting (adjusted (p=0.0430)), and schema selection was 0.092 above decomposition (adjusted (p=0.0117)). No Granite contrast survived correction. The differing method order across two snapshots argues against a universal prompting recipe.

### 6.6 Retrospective Replay Coverage

The replay audited all 180 GridDB questions without a generation call. At least two distinct frozen SQL candidates were present for 173 questions. After safety checks and binding to consistent frozen T0 execution evidence, 172 questions had at least two eligible candidates and entered retrospective adjudication. Seven questions failed closed because only one unique SQL remained, and one failed because fewer than two candidates were eligible.

| Replay coverage gate | Questions |
|---|---:|
| Audited | 180 |
| At least two unique frozen SQL candidates | 173 |
| At least two eligible candidates | 172 |
| Retrospectively adjudicated | 172 |
| Failed: one unique candidate | 7 |
| Failed: fewer than two eligible candidates | 1 |
| Reference-free counterfactual evidence | 0 |

Unique candidate counts ranged from one to eight: 1 (7 questions), 2 (19), 3 (15), 4 (18), 5 (27), 6 (23), 7 (45), and 8 (26). These counts show that the frozen assets can populate a future coordination interface for most questions. They do not show that the retrospectively selected query is correct. No retrospective accuracy, execution gain, rescue rate, or multi-agent superiority is reported.

**[EVIDENCE SLOT E-R1: RETROSPECTIVE SELECTED-OUTPUT ACCURACY — PROHIBITED IN R1]** Do not fill from the current replay. A post-selection gold comparison would be an exploratory diagnostic and would require a separate predeclared interpretation. It cannot substitute for the matched prospective coordination experiment.

### 6.7 Prospective Coordination Result Slot

**[EVIDENCE SLOT E-P2: PRIMARY RESULT TABLE]** Rows: SINGLE, STAGED, MULTI_NO_CF, MULTI_FULL. Columns: attempted calls, terminal predictions, safe SQL rate, execution accuracy, abstention rate, mean tokens, median latency, and complete-state coverage. Every cell requires a frozen artifact locator and denominator.

**[EVIDENCE SLOT E-P3: PAIRED CONTRASTS]** Report MULTI_FULL−SINGLE as the primary contrast; STAGED−SINGLE and MULTI_FULL−MULTI_NO_CF as secondary contrasts. Include cluster definition, interval method, raw and adjusted (p)-values, and failure accounting. Until filled, no sentence may state that the multi-agent framework improves accuracy or robustness.

## 7. Discussion

### 7.1 What the Current Evidence Supports

The combined evidence supports three bounded conclusions. First, explicit structural and SQL-operation instructions strongly alter projected-column adherence, but this surface conformity does not establish correct execution. Second, presented value evidence can matter for one frozen model snapshot while showing no effect for another. Third, candidate selection and prompting procedures are backbone-dependent: the component selector did not meet its registered efficacy rule, and the descriptively best BIRD method differed between Qwen and Granite.

These findings justify a framework that separates intent, schema grounding, synthesis, validation, and robustness evidence. They do not establish that five roles are superior to one model call. The architecture’s current value is methodological and engineering-oriented: typed contracts, explicit eligibility, deterministic selection, abstention, incident retention, and a sealed gold boundary make a future comparison reproducible and falsifiable.

### 7.2 Interpreting the Retrospective Replay

The replay answers a coverage question: do the inherited ledgers contain enough distinct, executable candidates to exercise the new coordination interfaces? For 172 of 180 questions, the answer is yes. This reduces the implementation risk of a prospective experiment and identifies eight fail-closed cases that require either a registered fallback or a new matched candidate-generation policy.

The replay cannot estimate a coordination effect. Its candidate pool mixes two backbones and four prompt packages, so generation conditions and candidate diversity are confounded. It also lacks reference-free counterfactual equivalence evidence. Scoring the selected candidates against gold after observing the pool would produce an exploratory post hoc quantity, not a valid substitute for a prospective matched comparison.

### 7.3 Reliability and Power-Grid Use

Read-only execution, syntactic validity, and result-shape conformity are necessary safeguards, not operational certification. A safe query can return the wrong assets, omit time bounds, misinterpret status codes, or mishandle ties. Multi-state witnesses reduce the risk of accidental snapshot equality but cannot cover all data distributions or schema changes. Generated SQL and returned source rows therefore require human inspection before any maintenance, protection, dispatch, or asset-management decision.

The framework is best positioned as an auditable decision-support interface. The blackboard can expose which schema elements were selected, which candidates failed, and why the controller abstained. This trace can support reviewer and operator diagnosis, but it must not be presented as an explanation of a model’s internal causal reasoning.

### 7.4 Negative Results and Reproducibility

Negative results are part of the contribution. Zero of nine primary GridDB factorial execution tests survived multiplicity correction. The deterministic component selector did not meet its efficacy rule for either model snapshot. No registered multi-state effect survived correction. Granite and Qwen did not share the same best BIRD method. Retaining these outcomes prevents the paper from collapsing several prompt and coordination choices into a single success narrative.

Reproducibility is strengthened by immutable prompt and prediction ledgers, explicit incident directories, direct SQLite re-execution, registered statistical families, portable manifests, and input/output hashes. The retrospective replay additionally checks its three input hashes before reading them and records tool and output hashes. These controls verify artifact identity and deterministic processing; they do not remove development exposure or create external validity.

## 8. Limitations and Future Work

The primary domain corpus is one synthetic maintenance database with eight tables, 98 rows, and 180 evaluation questions. Its evaluation partition was visible during project development. The 70 normalized-SQL groups are dependence proxies rather than independent authoring-template identifiers, and 58 are singletons. Results should not be generalized to production utility schemas, permissions, missing-data patterns, units, access-control policies, or concurrent workloads.

Only two quantized local model snapshots were evaluated. Model family, parameter count, quantization, serving software, and prompt serialization may interact. One positive Qwen component effect and the observed BIRD method ordering do not establish replication. Broader evaluation requires additional frozen backbones and databases under the same evaluator and call budget.

The compact context package bundles schema reduction, value matching, domain normalization, and serialization changes. The composite hint bundles projection, aggregation, grouping, ordering, and limit instructions. The inherited factorial experiment identifies package-level effects, not the causal contribution of each internal rule.

The five-role coordination core is implemented and unit-tested but has not completed a prospectively frozen generation experiment. Its Query Analyst and Schema Cartographer are deterministic skeletons, the Synthesizer packages externally supplied candidates, and the deterministic scoring weights have not been optimized or independently validated. The retrospective replay is not an accuracy experiment.

The counterfactual interface currently lacks selection-eligible evidence. Existing formal-v5 agreement fields compare candidates with gold and are intentionally excluded from adjudication. A future protocol must define reference-free invariants before generation or reserve counterfactual testing entirely for post-selection evaluation. Constructed database states remain incomplete witnesses rather than a proof of arbitrary semantic equivalence.

RTS-GMLC, SimBench, and NERC question–SQL assets remain machine-adjudicated silver data. Qualified domain review is still required for intended projections, units, ordering, tie handling, and result granularity. Any future human annotation must distinguish reviewer identity, qualification, blind procedure, disagreement resolution, and retained exclusions.

Future work should therefore prioritize the matched prospective coordination protocol, followed by independent domain review and external database evaluation. Further extensions may replace lexical grounding with a trained schema linker, add a registered low-confidence fallback, compare deterministic adjudication with budget-matched voting, and evaluate abstention calibration. These extensions should preserve the sealed gold boundary and should be introduced as new protocol versions rather than silent changes to prior runs.

## 9. Conclusion

MA-SQLGrid reframes power-grid text-to-SQL as an auditable coordination problem. Five specialist roles separate question analysis, schema mapping, candidate generation, safety and execution validation, and counterfactual criticism; a deterministic controller records their handoffs, selects only eligible candidates, and abstains when evidence is insufficient. This architecture restores the core intent of the original title while maintaining a strict boundary between implementation and demonstrated performance.

The inherited experiments provide a substantial but bounded evidence base. The 1440-prediction GridDB factorial study shows strong projected-column instruction uptake but no primary execution effect surviving Holm correction. The 700-call component study supports a presented-value effect for one Qwen snapshot, not Granite, and does not validate the candidate selector under its registered rule. The 25,920-row state study finds no corrected factorial reliability effect. The 5000-call BIRD protocol supplies a public comparison whose best method depends on the backbone. The retrospective replay confirms adequate candidate coverage for 172 of 180 GridDB questions, while deliberately reporting no accuracy or counterfactual gain.

The next scientific gate is therefore prospective rather than rhetorical: freeze a budget-matched multi-agent comparison, seal all blackboards before gold evaluation, retain every failure, and report the result whether positive or negative. Until that gate is completed, MA-SQLGrid should be described as a reproducible framework with inherited component evidence and a validated coordination interface, not as a proven superiority result or deployed power-grid system.

## 10. Back Matter Recommendations

### Supplementary Materials

The supplementary package should contain hash-bound prompts, predictions, scores, frozen protocols, incident records, independent re-execution audits, statistical tables, figure sources, the multi-state release, BIRD v1.1 ledgers, the five-role coordination core, unit tests, the retrospective diagnostic ledger, and its manifest. Inherited and new artifacts must remain in separate directories with their original protocol identifiers.

### Author Contributions

Conceptualization, B.L. and Y.Y.; methodology, B.L.; software, B.L.; validation, B.L. and C.S.; formal analysis, B.L. and C.S.; investigation, B.L. and C.S.; resources, Y.Y.; data curation, B.L. and C.S.; writing—original draft preparation, B.L.; writing—review and editing, C.S. and Y.Y.; visualization, B.L.; supervision, Y.Y.; project administration, Y.Y.; funding acquisition, Y.Y. All authors have read and agreed to the published version of the manuscript.

> Author verification required before submission: confirm that these CRediT assignments reflect actual contributions. Correspondence: Yang Yong; email to be completed manually.

### Funding

This research was funded by the Science and Technology Project of NARI Group Corporation (State Grid Electric Power Research Institute), grant number **521300250006**.

### Institutional Review Board Statement

Not applicable. This study did not involve human participants or animals.

### Informed Consent Statement

Not applicable.

### Data Availability Statement

Public project code and license-cleared reproducibility materials are available at <https://github.com/gaoxingkele/ma-sqlgrid>. BIRD Mini-Dev remains available from its public provider. Owing to third-party licensing restrictions, materials not included in the public repository, including restricted source records and source-dependent RTS-GMLC and SimBench artifacts, are available from the corresponding author upon reasonable request for editorial and peer-review verification, subject to third-party permission and applicable licenses. The verification package should include hash-bound prompts, predictions, scores, audits, generated tables and figures, BIRD Mini-Dev v1.1 ledgers, the post-run audit, and machine-adjudicated external-review artifacts.

### Acknowledgments and AI-Use Disclosure

During preparation of this manuscript, the authors used OpenAI Codex (GPT-5-based) for drafting, editing, code review, and reproducibility checks. The authors reviewed and edited the outputs and take full responsibility for the publication. Machine-generated external question–SQL candidates were not treated as human or domain-expert ground truth in the quantitative evaluation.

> Policy verification required at submission: confirm the final disclosure wording against the then-current Applied Sciences/MDPI policy and disclose any additional models used for figures, annotations, or language editing.

### Conflicts of Interest

The authors declare no conflicts of interest. The funder had no role in the design of the study; in the collection, analysis, or interpretation of data; in the writing of the manuscript; or in the decision to publish the results.

### Operational Safety Statement

MA-SQLGrid is an experimental read-only decision-support prototype. Generated SQL and returned records require human inspection before consequential use. The study does not validate deployment in operational control, protection, maintenance scheduling, or safety-critical decision making.

## R1 Evidence-to-Claim Gate

| Claim | Current evidence | R1 disposition |
|---|---|---|
| Five-role coordination core exists | Source code and 11 passing offline tests | May claim implementation and deterministic interface behavior |
| Existing assets support candidate replay | 180-row hash-locked replay; 172 questions pass coverage gate | May claim candidate-pool coverage only |
| Full multi-agent framework improves accuracy | No matched prospective run | **Prohibited; evidence slot only** |
| Counterfactual critic improves robustness | No reference-free selection evidence | **Prohibited** |
| GridDB prompt factors improve execution | Zero of nine primary tests survives Holm | Report estimates and negative inference |
| Presented values help | Positive registered Qwen effect; Granite null | Bounded one-snapshot claim only |
| Candidate selector improves execution | Neither backbone meets registered rule | Report rescue/harm and negative inference |
| BIRD method is universally best | Best method differs by backbone | **Prohibited** |
| External grid accuracy is established | Machine-silver RTS-GMLC/SimBench/NERC assets | **Prohibited pending qualified review** |
| Spider/WikiSQL or unsupported large-corpus results exist | Unsupported original-DOCX claims | **Removed from R1** |
