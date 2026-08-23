# MA-SQLGrid unified evaluator protocol freeze

Freeze date: 2026-08-23 (Asia/Shanghai)
Repository baseline: `840dcce5835423a5cdc3ee9f84eccfc601a6f4f6`
Evaluator ID: `MA-SQLGrid-GridDB-T0-shape-denotation-v1`
Status: frozen before the eight-slot reconciliation run.

## Evaluation universe and artifact identities

- Questions: all 180 frozen GridDB-Maintenance-v2 v0.1 records; no exclusions.
- Candidate grid: Qwen and Granite under `F00_Full_NoShape`, `F01_Full_WithShape`, `F10_Compact_NoShape`, and `F11_Compact_WithShape`, eight fixed slots per question.
- Selector outputs: the already sealed `fixed_order_equal_budget`, `validation_rank_equal_budget_no_cf`, and `full_coordination_complete_metamorphic` choices. No model is called and no selector is retuned.
- Database: frozen `T0_snapshot.sqlite` only.
- Runtime target: Python 3.12.10, SQLite 3.49.1. Runtime identity is recorded by the audit.

## Correctness rule

1. Candidate and gold SQL must execute successfully under the same read-only, query-only SQLite boundary. Extensions, writes, schema mutation and metadata access are denied. Limits are 2 s, 2,000,000 opcodes and 10,000 result rows.
2. Errors, safety rejection, timeout, opcode exhaustion or row-limit overflow are incorrect.
3. The predicted result must have exactly `answer_shape.column_count` columns. The gold result must also match that frozen count.
4. `NULL` is distinct. Finite floating values are normalized at absolute tolerance `1e-6`; non-floating values are compared without coercion.
5. For `order_sensitive=true`, normalized row sequences must be identical. Otherwise duplicate-preserving normalized row multisets must be identical.
6. Empty result sets are not automatically correct: execution and both shape gates must pass before empty-row equality is considered. This rule is decisive for Q104, Q107, Q110 and Q140.
7. SQL text canonicalization is not a correctness criterion. SQL SHA-256 is used only for artifact identity and duplicate tracing.

## Frozen paired analysis

- Baseline policy: `C000`, the frozen first candidate, which must be byte-identical in normalized SQL to Qwen F00 for all 180 questions.
- Report counts and accuracy for the eight fixed sources, the C000 alias and two selectors.
- Paired difference: mean of question-level correctness differences relative to C000.
- Interval: deterministic 10,000-draw paired question-composition percentile interval; seed base `20260823`.
- Paired test: exact two-sided binomial sign test on rescue/harm discordances.
- Multiplicity: Holm step-down across nine unique comparisons to C000 (seven other fixed sources plus two selectors). The Qwen-F00/C000 identity is not counted as a separate test.
- All resulting inference is post-result reconciliation/sensitivity evidence, not preregistration.

## Bound files

```text
78B7782E4FF489979A6E84A885093C2CDBA46E65A4F2CA9E606BEE83665E44AD  source/code/evaluator/evaluator.py
3F28F832F437CFE74DEC56E989D54A5626BBEB5DD4B1311A7D2681D3F314DC55  Code/framework/sqlite_readonly_executor.py
0843A7555AE3E00B2B8AE469138F9E017E37E2EBAC154E7BBD248C7146C5A573  historical_pool/study_config_v3.json
0B37F551F98ADB3CFB1942B2C3B8EDD700D40A7F49C416CCF95A3AE71DDE594E  historical_pool/selection_inputs.jsonl
2B447A63D47D225E15148E0A75C660DDAFC83E5C50AAA2DDC207D252B9FB6777  run_v3a/blackboards_sealed_before_gold.jsonl
5FA94B199203FC904EB51F736872667C7E878C40C9AF8E782618F99656B76021  run_v3a/selection_ledger_pre_gold.jsonl
53AAF0C9659F6A6B71B66FF64D34ED925664742205D0CA4FD7585D7FE5C9F5E3  qwen predictions.jsonl
BE433AC853F60EBC8882FDCC7BD01033BCA8868FA23B298114B0977476983E3D  granite predictions.jsonl
BA74E84F30C15ECF04BF2B1FFB5D1CCBB978A9E210B69F4676B9BDE64E5BBC46  T0_snapshot.sqlite
A08F302AFB47BC2E7C352D20CA69EFA0068B74D9AD296C988BC7B27160593A82  questions.jsonl
```

The audit output may contain question IDs, counts, SQL hashes, row counts and column counts. It must not duplicate gold or candidate SQL text.
