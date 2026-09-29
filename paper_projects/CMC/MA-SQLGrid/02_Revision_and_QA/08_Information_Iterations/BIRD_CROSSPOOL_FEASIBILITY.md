# BIRD cross-pool diagnostic feasibility — evidence-backed input audit

2026-09-13. No selector experiment executed in this audit; no manuscript
results changed. See `BIRD_CROSSPOOL_INPUT_AUDIT.json` for machine evidence.

## Verified availability

Original `MA_PUBLIC_BIRD_v1_1_{qwen,granite}_clean1` files were found under
`paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/public_baseline_protocol/formal_runs/`.
All four final-score/call-ledger SHA-256 values exactly match the existing
post-run independent audit. Each model has 2000 final records, 2500 calls,
500 unique questions and four methods per question. Both models cover the
same question/database pairs across 11 databases. Empty SQL occurs in 18
Qwen and 25 Granite final records and must remain in the denominator.

The 500-item annotation file matches the documented SHA
`88ceb0710163cae46a256ecea8f0a8c98286599530b60587fda5c3cfe57d45d2`.
All 11 database paths exist; this audit checked existence, NOT their current
file hashes or query execution. Original licence notes support local study;
no new public redistribution of raw text or databases is authorized here.

## Actual adaptation boundary

The final rows contain SQL and official correctness but do not contain
`shape_ok`, `order_ok`, `value_hits`, `safe`, or `executable`. These cannot be
invented from correctness. They require a new, recorded extraction/execution.

Inspection of current source found a reusable question-only `QueryAnalyst`
in `Code/framework/ma_sqlgrid_agents.py`. The historical
`offline_coordination_study_v2.py::validation_for` derives aggregation and
ordering features from question/SQL and lexical overlap without gold SQL.
Thus reference-free score reconstruction is feasible in principle without
LLM calls. Its `shape_ok` name means aggregation-pattern compliance here,
not matching the gold result's number of columns. Preserve that distinction.

The historical driver equates `safe` with successful execution; a new BIRD
runner must use the existing read-only bounded executor, explicitly record
its version and acknowledge the execution-environment difference. It must
not load/run arbitrary candidate SQL with an unrestricted database connection.

## Protocol requirements before replay

1. Keep two separate four-slot pools (one per backbone), ordered B0, B1, B2,
   B3. An eight-slot joint pool can be a separately declared sensitivity,
   not silently substituted for the primary setting.
2. Preserve B3's extra repair call: equal final-slot counts do not imply
   equal generation cost. This is diagnosis of retained pools, not a new
   budget-matched generation superiority experiment.
3. Fix original question-only feature rules and weights 10/5/capped-5 before
   producing new selector outcomes. Do not use reference SQL, official_ex,
   gold-derived shape, evidence annotations or correctness to form features.
4. Seal candidate ids, hashes, features, gate decisions and chosen ids before
   joining retained correctness labels for the failure partition. Historical
   exposure is already known; a new seal does not create unseen-test status.
5. Report all 500 questions per model, empty/malformed SQL and gate failures;
   report per-database partitions and item-weighted/equal-database summaries.
   Avoid significance-first analysis and no post-result rule tuning.
6. This can test the validation-only gate–score–tie diagnosis. It cannot
   establish full witness transfer: the three GridDB-specific transformations
   have no validated BIRD counterparts. Do not fabricate complete-witness
   evidence or claim an exact end-to-end replication.
7. Hash the databases and code, bind runtime and resource limits, test the
   adapter with synthetic fixtures, and verify no gold accesses in selection.
   Then execute to a new directory; preserve logs and all failures.

## Interpretation

The next safe step is a frozen exploratory replay adapter, not another model
generation campaign. Even a successful replay would extend the diagnosis
across these retained non-grid schemas, not validate power-grid semantics or
establish prospective external performance. The existing R3 ZIP remains an
unchanged historical candidate and does not include this subsequent audit.
