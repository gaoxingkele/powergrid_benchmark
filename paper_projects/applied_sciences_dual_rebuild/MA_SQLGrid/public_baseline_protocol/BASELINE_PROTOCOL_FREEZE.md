# MA public baseline protocol freeze

**Protocol:** `MA-PUBLIC-BIRD-MINIDEV-v1.0`  
**State:** technically frozen, not run; formal execution remains human-gated  
**Formal generation calls so far:** 0

## Frozen experiment

All 500 official BIRD Mini-Dev SQLite questions and all 11 databases are retained. Every method receives the official question-specific evidence. Qwen2.5-Coder-7B Q4_K_M and Granite-3.3-8B Q4_K_M run sequentially on the same RTX 3090 and pinned llama.cpp build.

- `B0_DIRECT`: full-schema direct SQL, one call.
- `B1_DECOMP`: one structured `schema_links`/`clause_plan`/`final_sql` call; only `final_sql` is scored.
- `B2_SCHEMA_SELECT`: deterministic BM25 selection with mandatory keys and deterministic shortest-FK closure, one call.
- `B3_EXEC_REPAIR`: candidate generation, safe read-only SQLite feedback, and an always-executed second call—even after `SAFE_EXECUTED`.

This is an independent transparent comparator suite, never a DKASQL reproduction.

## Passed technical gates

- Python 3.10.11 / SQLite 3.40.1: 500/500 gold SQL executions across 11/11 databases.
- Official Mini-Dev EX code pinned at repository commit `b3d4bcbbae9a96934ad812551eb400c7a3b23c12`; the official boundary compares sets of result-row tuples, so row order and duplicate multiplicity are ignored while column order remains material.
- 2500 calls per model materialized (500 questions × 5 calls); total future work is exactly 5000 generation calls.
- Qwen maximum call/input bound 6257 tokens and maximum item-method aggregate 7301; Granite 6649 and 7769. No 12,000 aggregate-input or 15,872 context-minus-margin violation.
- No gold SQL, difficulty label, or gold-derived selector information enters generation prompts. Gold schema recall is offline analysis only.
- Selector audit: mean gold-table recall 0.9921, mean conservative lexical gold-column recall 0.8601, with zero questions at zero table or column recall.
- Read-only URI, `query_only`, authorizer denial, progress timeout, frozen feedback vocabulary, all-attempt denominator, zero retries, deterministic SHA item order, and cyclic method order are implemented and tested.

## External gates

The BIRD data are marked CC BY-SA 4.0. The checked Mini-Dev repository does not expose a repository-level SPDX license, so redistributing the extracted evaluator files remains a release/license review item even though their exact local hashes are frozen. A real human author must approve the exact freeze hash before launch. Human signature, artifact DOI, and publication redistribution decisions are not supplied or fabricated here.

See `FORMAL_RUNBOOK.md` for the guarded commands. Merely reading that runbook does not authorize execution.

## Amendment v1.0.1 (2026-08-07)

Defect fix in `freeze_public_baseline.py::safe_execute`: catch `sqlite3.Warning` in addition to `sqlite3.Error`. Python's `sqlite3.Warning` is not an `sqlite3.Error` subclass; multi-statement model outputs (e.g. `SELECT ...; SELECT ...`) raised it and aborted the formal run at call_index 2134 (question 98, financial, B1_DECOMP) instead of being classified. Such outputs now classify as `OTHER_EXECUTION_ERROR` — a status already present in the frozen feedback vocabulary — receive EX=0, and the all-attempt denominator is preserved. Regression test `test_multi_statement_output_is_classified` added to `test_public_baseline_freeze.py` (6/6 pass under the pinned runtime). No prompt, call order, model, database, gold SQL, evaluator, or scoring-semantics artifact was changed; only error-classification robustness of the safety wrapper. The freeze manifest and independent audit were regenerated after this amendment, and the author re-signed the launch approval binding the new freeze SHA-256.
