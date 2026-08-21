# Pre-Three-Pack Minimal Text-to-SQL Smoke Report

## Scope

- Purpose: verify provider, baseline/method prediction contracts, and evaluator scoring before three-pack generation.
- This is not a formal experiment and must not be used for paper claims.
- Questions: Q001, Q002, Q003, Q004, Q005 from the dev split only.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.

## Artifacts

- predictions: `smoke/run/predictions.jsonl`
- scores: `smoke/run/scores.jsonl`
- traces: `smoke/run/traces/`

## Contract Summary

- prediction records written: 10
- expected records: 10
- records with contract errors: 0
- records with unsafe SQL: 0
- records with model/extraction errors: 0

## Condition Diagnostic Scores

| condition | records | evaluator_correct | evaluator_errors |
|---|---:|---:|---|
| C1_StrongDirect | 5 | 5 | none |
| C5_VG_Rerank_Minimal | 5 | 5 | none |

## Per-Question Results

| question_id | condition | safe_sql | evaluator_correct | error_type | contract_errors |
|---|---|---:|---:|---|---|
| Q001 | C1_StrongDirect | True | True | correct | none |
| Q001 | C5_VG_Rerank_Minimal | True | True | correct | none |
| Q002 | C1_StrongDirect | True | True | correct | none |
| Q002 | C5_VG_Rerank_Minimal | True | True | correct | none |
| Q003 | C1_StrongDirect | True | True | correct | none |
| Q003 | C5_VG_Rerank_Minimal | True | True | correct | none |
| Q004 | C1_StrongDirect | True | True | correct | none |
| Q004 | C5_VG_Rerank_Minimal | True | True | correct | none |
| Q005 | C1_StrongDirect | True | True | correct | none |
| Q005 | C5_VG_Rerank_Minimal | True | True | correct | none |

## Gold-Leakage Check

- Prompts include question text, schema, compact domain values, answer-shape metadata, order sensitivity, and required literal metadata.
- Prompts do not include gold SQL, gold result rows, expected hashes, or test examples.
- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.
- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this smoke.

## Decision Rule

This smoke passes only if all 10 prediction records exist, satisfy the JSONL contract, contain read-only SQL, and can be scored by the evaluator without crashing. Accuracy is diagnostic only.
