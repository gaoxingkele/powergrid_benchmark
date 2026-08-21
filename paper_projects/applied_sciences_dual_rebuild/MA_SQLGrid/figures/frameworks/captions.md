# Caption drafts

> Protocol/method diagrams only. No unfrozen experimental result is represented.

## ma_f01_pipeline

MA-SQLGrid protocol-level pipeline. A natural-language request is grounded against schema and sampled values, compressed into a task-relevant context, augmented by an explicit answer-shape contract, and translated into SQL. A safe parser and reference-answer-independent validator either accepts the query or sends it through bounded repair before read-only execution. Every transition is retained in an audit trace. The figure defines registered structure and reports no performance.

Source evidence: MASTER_EXECUTION_PLAN.md Sections 3.2, 3.5-3.7; experiment_registry.json MA-M01, MA-A01, MA-X01; MA_SQLGrid/external_protocol/artifacts/manifest.json

## ma_f02_factorial_external_flow

Registered 2×2 context-by-shape factorial and external-database evidence flow. GridDB-Maintenance is development-touched; RTS-GMLC and SimBench currently contain unsealed automatic candidates and must pass the eligibility gate before benchmark promotion. Identical paired questions and database snapshots feed all Full/Compact × Shape/No-Shape cells. Immutable instance outputs proceed to independent paired statistics and the E4 audit; no outcome values are shown.

Source evidence: experiment_registry.json MA-M01-M04, MA-M02; MA_SQLGrid/external_protocol/artifacts/manifest.json; MA_SQLGrid/data/rts_gmlc_pilot/W3_RTS_GMLC_REPORT.md; MA_SQLGrid/data/simbench_pilot/W3_SIMBENCH_REPORT.md

## ma_f03_human_review_sealed_gate

Human-review and sealed-test eligibility gate. Machine precheck only prioritizes risk. Two real reviewers independently assess every promoted item; a third person adjudicates conflicts, then corrected SQL is re-executed and hashed. Development-visible items can become human-reviewed unsealed data but cannot retroactively become sealed. Only previously unused, family-isolated and access-controlled items may enter a one-time sealed run after method freeze.

Source evidence: MA_SQLGrid/data/human_review_packet/REVIEW_PROTOCOL.md; MA_SQLGrid/data/human_review_packet/W4_MA_HUMAN_REVIEW_PACKET_REPORT.md; experiment_registry.json MA-M04
