# MA-SQLGrid Supplemental Experiment Feasibility Audit

Date: 6 August 2026  
Scope: read-only inventory and execution plan  
Outcome: **TECHNICALLY_EXECUTABLE; HUMAN GATES DOMINATE**

No BIRD call or other model call was made, and the manuscript was not modified.

## Executive finding

The workspace already contains enough data, code, models, runtime controls, and GPU capacity to address the four largest remaining evidence gaps: cross-database performance, independent baselines, sealed external validation, and generation repeatability. The limiting resources are not software or GPU memory. They are:

1. explicit human authorization for the frozen 5,000-call BIRD run;
2. two qualified external reviewers and a real adjudicator for the 91 RTS-GMLC/SimBench candidates;
3. independent human authors/reviewers and an access custodian for a genuinely new sealed set;
4. author approval of a new five-seed stochastic protocol and the associated compute scope;
5. source-license and redistribution decisions.

## Executable inventory

### Compute and models

- One NVIDIA RTX 3090, 24,576 MiB total and 23,200 MiB free at audit time; GPU utilization was 4%.
- Qwen2.5-Coder-7B-Instruct Q4_K_M: 4,683,073,536 bytes, SHA-256 `509287f7...894d3c`, Apache-2.0.
- Granite-3.3-8B-Instruct Q4_K_M: 4,942,873,344 bytes, SHA-256 `77bcee06...15dca`, Apache-2.0.
- Pinned llama.cpp CUDA runtime `b9637@aedb2a5...`; formal policy is one server/model at a time.
- No llama-server process or listener on ports 8080/8091/8092 was present during this read-only audit.

Observed calibration is fast: 720 GridDB calls took 0.08 summed GPU-hours for Qwen and 0.15 for Granite; the 364-call Qwen external diagnostic took 0.04 hours. Planning estimates below deliberately add large margins for longer BIRD prompts, server transitions, database execution, auditing, and incidents.

### Data and protocol assets

| Asset | Available evidence | Current boundary |
|---|---|---|
| GridDB | 180 questions, 8 tables, 98 rows; two backbones; 4-cell factorial and component code | Development-visible controlled case study |
| BIRD Mini-Dev | 500 questions over 11 SQLite databases; 500/500 gold preflight | Public cross-database comparator, not sealed |
| RTS-GMLC | 10 tables, 360,530 rows; 55 candidates in 11 families | Automatic, development-visible, unreviewed |
| SimBench | 8 tables; 36 candidates in 6 families | Automatic, development-visible, unreviewed |

The BIRD freeze is especially mature: `FROZEN_NOT_RUN`, SHA-256 `29C780C63A2DC2BAAE221CFCE52252C716D8720DBEECDC2F7A2FDD5756B42AF5`, technical audit 39/39 PASS, two pinned models, 2,500 materialized calls per model, deterministic order, official evaluator, read-only execution, exact token budgets, and zero formal outputs. Its four independent methods are Direct, Decomposition, deterministic Schema Selection, and mandatory two-call Execution Repair. It is explicitly not a DKASQL reproduction.

The external packet is also operationally ready: two blinded 91-row forms, reviewer field definitions, agreement code, conflict template, data/schema access, and deterministic hashes. It has zero completed human reviews and zero sealed items. The existing 364-call Qwen run is useful failure-analysis history only: 321 executable predictions, 43 execution errors, and 15 automatic-reference matches that are not accuracy.

## Prioritized supplemental experiment matrix

| Priority | Experiment | New calls | GPU estimate | Main evidence gained | Blocking human dependency |
|---|---|---:|---:|---|---|
| P0 | Frozen BIRD comparator, 500 questions × 11 DBs × 2 models | 5,000 | 3–6 h; reserve 8 h | Cross-database validity and independent baselines | Exact human launch approval bound to freeze SHA |
| P1A | Dual review/adjudication of existing 91, then new 91×4×2 run | 728 | 0.5–1 h | Expert-checked power-grid external evidence | Two reviewers, adjudicator, license review; 35–55 human-hours |
| P1B | New sealed set: 30 RTS + 30 SimBench, four cells, two models | 480 | 0.5–1 h | Untouched confirmatory external evidence | Independent authors/reviewers/custodian; 40–70 human-hours |
| P2 | Five-seed GridDB factorial: 180×4×2×5 | 7,200 | 2–4 h | Seed sensitivity and generation stability | Author approval and a new pre-run freeze |
| P3 | Cross-evidence synthesis and failure analysis | 0 | CPU 2–4 h | Applied interpretation and robustness | Upstream results and author/domain interpretation |

Full program: **13,408 new local generation calls**, approximately **6–12 GPU-hours** on the RTX 3090; reserve 14 hours for transitions and validation. CPU postprocessing is roughly 6–10 hours. Human work is approximately 75–125 hours. Paid API calls: zero.

## Statistical plan

### P0 — BIRD

Use the 11 databases as the dependence clusters. Predeclare three contrasts within each backbone—Schema Select vs Direct, Execution Repair vs Direct, and Execution Repair vs Schema Select—plus their three Granite-minus-Qwen modifiers. This gives one nine-test Holm family.

- Enumerate all $2^{11}=2048$ database-cluster sign assignments exactly.
- Report per-database all-attempt execution rates and failure counts.
- Use database-cluster composition-sensitivity bootstrap intervals; do not call them population confidence intervals.
- Independently re-execute all 4,000 final predictions and verify all 5,000 call rows before analysis.

### P1A — reviewed but unsealed RTS/SimBench

- Both real reviewers complete all 91 items; report critical-field coverage, raw agreement, Cohen's $\kappa$, and Gwet AC1 because prevalence may be extreme.
- Every disagreement and missing critical field goes to a third adjudicator. Revised SQL is re-executed and re-hashed.
- Use the 17 template families as dependence clusters, not the two datasets. Report dataset-stratified denominators separately.
- Use exact family-cluster paired randomization where feasible and family-stratified bootstrap intervals.
- Rerun both models after adjudication. The previous Qwen diagnostic cannot become canonical retroactively.

### P1B — genuinely sealed confirmation

Create 60 new or deeply rewritten items, balanced 30/30 across RTS-GMLC and SimBench and spanning at least 12 family/SQL-structure strata. The development team must not see questions or gold SQL before the method/configuration freeze. Run one registered, no-drop batch of 480 calls.

- Audit normalized-SQL, template-family, lexical, and semantic similarity against GridDB and the existing 91 before sealing.
- Report all-attempt rates, Wilson descriptive intervals, dataset denominators, and family-cluster paired contrasts.
- No prompt repair, threshold change, item deletion, or rerun after unsealing.

### P2 — five-seed generation repeatability

Changing the seed at temperature 0 is not a meaningful stochastic replication. Freeze one common nonzero sampling configuration before any run and regenerate all five seeds symmetrically.

- Report cell/backbone means, ranges, within-question variance, SQL exact-match stability, and denotation stability.
- Fit a hierarchical logistic model or GEE respecting repeated outcomes by question, structural cluster, and seed.
- Use paired cluster bootstrap intervals and a predeclared Holm family; retain every generation failure.

### P3 — synthesis

Produce an evidence-tier table, per-dataset effect-direction matrix, failure taxonomy, empty-result sensitivity appendix, and claim-to-artifact ledger. Do not pool datasets in a way that hides database-specific failures or promote an effect merely because one evidence tier is favorable.

## Required deliverables

Each generated experiment must produce:

- immutable protocol freeze, deterministic call order, prompts, predictions, scores, logs, and incident records;
- model/data/code/runtime SHA-256 manifests;
- an independent re-execution and statistics audit;
- machine-readable CSV plus publication TeX tables;
- vector PDF/SVG and PNG figure lineage;
- exact denominator/failure tables and bounded claim language;
- reviewer-response and claim-ledger updates only after the corresponding gate passes.

Recommended figures are a per-database BIRD forest plot, a reviewed-versus-sealed external effect panel, a five-seed stability heatmap, and a cross-dataset failure taxonomy. Avoid another framework diagram unless the experimental evidence tiers cannot be expressed clearly in a table.

## Recommended sequence

1. Seek the BIRD launch decision and recruit external reviewers/authors in parallel.
2. Freeze the five-seed GridDB protocol and sealed-set governance before any new generation.
3. If authorized, run BIRD sequentially Qwen then Granite; preserve any failed run as an incident and perform independent audit before looking at inferential tables.
4. Complete review/adjudication of the existing 91. Separately author, leakage-audit, review, and seal the new 60-item set.
5. Run reviewed-unsealed and sealed batches only after their respective gates pass.
6. Run the five-seed GridDB factorial without adaptive changes.
7. Integrate only independently audited evidence whose gate is closed.

## Non-negotiable boundaries

- Do not run BIRD without a real human approval companion bound to `29C780...B42AF5`.
- Do not call BIRD sealed or a DKASQL reproduction.
- Do not relabel the current 91 candidates as sealed.
- Do not substitute agent review for qualified human domain review.
- Do not promote the existing Qwen external diagnostic after the fact.
- Do not cherry-pick seeds, silently drop failures, or run both model servers concurrently.
