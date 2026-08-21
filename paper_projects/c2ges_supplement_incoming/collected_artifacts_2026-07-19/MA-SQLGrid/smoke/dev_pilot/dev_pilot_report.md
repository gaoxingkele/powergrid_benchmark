# Dev-Only C1 vs C5 Minimum Superiority Pilot

## Scope

- Purpose: check whether C5_VG_Rerank_Minimal shows any dev-set advantage over C1_StrongDirect before three-pack generation.
- This is not a formal experiment and must not be used for paper claims.
- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.

## Artifacts

- predictions: `smoke/dev_pilot/predictions.jsonl`
- scores: `smoke/dev_pilot/scores.jsonl`
- traces: `smoke/dev_pilot/traces/`

## Contract And Runtime Checks

- prediction records written: 40
- expected records: 40
- records with contract errors: 0
- records with unsafe SQL: 0
- records with model/extraction errors: 0
- candidate count distribution: {('C1_StrongDirect', 1): 20, ('C5_VG_Rerank_Minimal', 5): 14, ('C5_VG_Rerank_Minimal', 3): 4, ('C5_VG_Rerank_Minimal', 4): 2}

## Accuracy Diagnostics

| condition | records | evaluator_correct | accuracy | evaluator_errors |
|---|---:|---:|---:|---|
| C1_StrongDirect | 20 | 20 | 1.000 | none |
| C5_VG_Rerank_Minimal | 20 | 20 | 1.000 | none |

## Paired Superiority Diagnostic

- C5 wins: 0
- C1 wins: 0
- ties where both correct: 20
- ties where both wrong: 0
- measurable dev advantage for C5: False

| question_id | C1 correct | C5 correct | outcome | C1 error | C5 error |
|---|---:|---:|---|---|---|
| Q001 | True | True | tie_correct | correct | correct |
| Q002 | True | True | tie_correct | correct | correct |
| Q003 | True | True | tie_correct | correct | correct |
| Q004 | True | True | tie_correct | correct | correct |
| Q005 | True | True | tie_correct | correct | correct |
| Q006 | True | True | tie_correct | correct | correct |
| Q007 | True | True | tie_correct | correct | correct |
| Q008 | True | True | tie_correct | correct | correct |
| Q009 | True | True | tie_correct | correct | correct |
| Q010 | True | True | tie_correct | correct | correct |
| Q011 | True | True | tie_correct | correct | correct |
| Q012 | True | True | tie_correct | correct | correct |
| Q013 | True | True | tie_correct | correct | correct |
| Q014 | True | True | tie_correct | correct | correct |
| Q015 | True | True | tie_correct | correct | correct |
| Q016 | True | True | tie_correct | correct | correct |
| Q017 | True | True | tie_correct | correct | correct |
| Q018 | True | True | tie_correct | correct | correct |
| Q019 | True | True | tie_correct | correct | correct |
| Q020 | True | True | tie_correct | correct | correct |

## Gold-Leakage Check

- Prompts include question text, schema, compact domain values, answer-shape metadata, order sensitivity, and required literal metadata.
- Prompts do not include gold SQL, gold result rows, expected hashes, or test examples.
- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.
- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this dev-only pilot.

## Decision

No measurable dev-set advantage for C5 over C1 appears under this pilot.
