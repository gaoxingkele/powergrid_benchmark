# Public baseline protocol freeze — DRAFT

**Protocol ID:** `MA-PUBLIC-BIRD-MINIDEV-v0.1-draft`  
**Status:** `DRAFT_NOT_FROZEN`  
**No formal model execution is authorized by this file.**

## Objective

Compare four reproducible text-to-SQL pipeline classes under the same public data snapshot, hardware, local backbones, decoding policy, token envelope, and scoring boundary. The experiment addresses baseline adequacy; it is not a DKASQL reproduction and does not replace the sealed grid-domain validation.

## Population and no-selection rule

Primary population: all 500 rows of official BIRD Mini-Dev SQLite at Hugging Face revision `f65faf4ae3b638c1fa6df1d3370c8d92c8366301`, metadata SHA-256 `88ceb0710163cae46a256ecea8f0a8c98286599530b60587fda5c3cfe57d45d2`.

- Include all 500 official `question_id` values.
- Preserve official `db_id`, difficulty, question, evidence, and gold SQL.
- Do not filter by SQL length, schema size, difficulty, model fit, executability, or pilot outcome.
- Gold-execution incompatibility blocks the complete run; it does not authorize dropping a row.
- Item order is deterministic SHA-256 order of `protocol_id || question_id`, not source order or difficulty.
- BIRD is a public development benchmark. Call the study prospective-method/frozen-run, never sealed or contamination-free.

Resource fallback (not active): if the complete 500-item protocol is rejected before any formal output exists, a new protocol version may freeze 240 rows with quotas 72 simple, 120 moderate, and 48 challenging. Within each difficulty, allocate proportionally by database using largest remainders and rank candidates by SHA-256 of `new_protocol_id || db_id || question_id`. The new manifest and selected IDs must be committed/hash-published before generation. Once any formal output exists, switching to the fallback is prohibited.

## Common data condition

- Dialect: SQLite only.
- Knowledge: official question-specific `evidence` is included for every baseline (`oracle evidence = yes`).
- Schema source: SQLite catalog/DDL, primary keys, and foreign keys from the frozen databases.
- No gold SQL, official difficulty, gold result, or gold-required schema is exposed to prompts or selectors.
- Values: at most three deterministic examples per selected column, ordered by normalized textual value then row identity; no question-conditioned value lookup in this baseline suite unless separately frozen for all four methods.
- Safety: one read-only SQLite connection per evaluation, `query_only=ON` where supported, progress-handler timeout, and rejection of non-`SELECT`/`WITH` output.

## Methods

### B0_DIRECT

One call. Present question, oracle evidence, and full schema serialization. Request exactly one SQLite query with no prose.

### B1_DECOMP

One call. Same common inputs and token envelope. Require a machine-parseable object containing `schema_links`, `clause_plan`, and `final_sql`. Only `final_sql` is executed/scored. This is explicit decomposition, not an unverifiable claim about private chain-of-thought.

### B2_SCHEMA_SELECT

One call after deterministic CPU selection. BM25 ranks table and column documents built from names, types, descriptions, and permitted value examples. Freeze `top_tables`, `top_columns_per_table`, score thresholds, mandatory primary/foreign keys, shortest foreign-key path closure, and a deterministic full-schema fallback for an empty selection. The selector cannot access gold SQL or difficulty. Report selected-table/column counts, prompt tokens, gold-required schema recall as **offline analysis only**, and omission-caused errors.

### B3_EXEC_REPAIR

Two calls for every item. Call 1 receives the same common condition and emits a candidate with a 400-token ceiling. A deterministic validator checks read-only safety, parses/extracts SQL, and executes with a timeout. Call 2 always occurs and receives the question, evidence, bounded schema, first candidate, and one of a frozen feedback vocabulary: `SAFE_EXECUTED`, `PARSE_ERROR`, `UNKNOWN_TABLE`, `UNKNOWN_COLUMN`, `AMBIGUOUS_COLUMN`, `TYPE_OR_FUNCTION_ERROR`, `TIMEOUT`, or `OTHER_EXECUTION_ERROR`. Raw database results and gold information are never returned. Call 2 has a 400-token ceiling and emits final SQL.

This is `execution-feedback repair, independent implementation`; it is not DKASQL.

## Equal-resource controls

| Control | Frozen draft value |
|---|---|
| Hardware | Same RTX 3090; models run sequentially; one server and one slot |
| Runtime | llama.cpp b9637 / `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`, CUDA 13.3 |
| Models | Exact audited Qwen and Granite Q4_K_M files/hashes in JSON freeze |
| Context | 16,384 tokens; preflight must leave 512-token safety margin |
| Aggregate input budget | Maximum 12,000 tokenizer tokens per item-method; B3 sum across both calls |
| Aggregate output budget | Maximum 800 tokens per item-method; B3 = 400 + 400 |
| Decoding | Temperature 0, seed 20260805, retries 0, one completion |
| Prompt examples | Zero few-shot examples for all four methods |
| Run order | Model order Qwen then Granite; within model, SHA-ordered items crossed with cyclic method order to reduce time drift |
| Failure policy | All-attempt denominator; no retry, substitution, resume overlap, or row drop |

Before final freeze, tokenize every prompt for both chat templates. A budget violation blocks execution; it cannot be solved by method-specific ad hoc truncation. If a common deterministic serializer revision is required, regenerate and rehash **all** prompts before any formal call.

## Outcomes and analysis

Primary outcome: official BIRD execution accuracy (EX), all 500 attempts per method/backbone.

Secondary outcomes: executable rate, official Soft-F1 if the pinned evaluator supports the frozen SQLite snapshot, safety/parse/execution error classes, prompt/generated tokens, warm latency, throughput, peak VRAM, and SQL execution time. R-VES is exploratory because its repeated timing protocol adds substantial variability and cost.

- Report every method × backbone point estimate with database-stratified bootstrap intervals.
- Primary paired contrasts within each backbone: `B1-B0`, `B2-B0`, `B3-B0` for EX.
- Backbone effect modifiers are secondary.
- Database is the conservative cluster; also show descriptive difficulty/database strata.
- Adjust the six primary method comparisons (three per backbone) with Holm; keep cluster intervals primary and paired question-level tests descriptive if independence is doubtful.
- Do not tune prompts/selectors after viewing formal outputs. Any repair creates a new protocol version and invalidates the affected run as formal evidence.

## Freeze sequence

1. Acquire archive and official code with `download_official_resources.ps1`.
2. Record archive/code revisions, bytes, SHA-256, and license notices.
3. Validate 500 IDs, 11 databases, and 500/500 gold executions.
4. Implement adapters/evaluator and run unit tests on synthetic SQL only.
5. Materialize all prompts without model calls; audit gold leakage and budgets.
6. Write prompt/code/data/config hashes into the JSON; change status to `FROZEN_NOT_RUN`.
7. Obtain independent reviewer name/date/signature and verify a clean process/GPU/port state.
8. Start one foreground server and one foreground harness. Do not run Qwen and Granite concurrently.

## Promotion gates

No number is manuscript-eligible until an independent script re-executes 500/500 final predictions per cell, verifies all row/prompt/model hashes and call counts, confirms zero dropped items/retries, and reproduces the aggregate tables from row ledgers. Published BIRD or DKASQL values remain contextual literature values, not rows in the same statistical comparison.

