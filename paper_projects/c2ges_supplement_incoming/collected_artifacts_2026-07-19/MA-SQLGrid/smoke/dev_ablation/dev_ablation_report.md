# Dev-Only Prompt/Context Ablation Pilot

## Scope

- Purpose: identify whether C5's apparent value comes from value/shape context, reranking, or neither.
- This is not a formal experiment and must not be used for paper claims.
- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.

## Conditions

- C1_LiteSchemaOnly: question plus schema only.
- C1_StrongDirect: question plus schema, compact values, answer shape, order sensitivity, and required literals.
- C5_VG_Rerank_Minimal: value-grounded candidate generation plus reference-free execution-aware reranking.

## Artifacts

- predictions: `smoke/dev_ablation/predictions.jsonl`
- scores: `smoke/dev_ablation/scores.jsonl`
- traces: `smoke/dev_ablation/traces/`

## Contract And Runtime Checks

- prediction records written: 60
- expected records: 60
- records with contract errors: 0
- records with unsafe SQL: 0
- records with model/extraction errors: 0
- candidate count distribution: {('C1_LiteSchemaOnly', 1): 20, ('C1_StrongDirect', 1): 20, ('C5_VG_Rerank_Minimal', 5): 12, ('C5_VG_Rerank_Minimal', 3): 4, ('C5_VG_Rerank_Minimal', 4): 4}

## Accuracy Diagnostics

| condition | records | evaluator_correct | accuracy | evaluator_errors |
|---|---:|---:|---:|---|
| C1_LiteSchemaOnly | 20 | 8 | 0.400 | {'wrong_denotation': 5, 'shape_mismatch': 7} |
| C1_StrongDirect | 20 | 20 | 1.000 | none |
| C5_VG_Rerank_Minimal | 20 | 20 | 1.000 | none |

## Paired Diagnostics

- C5 correct while lite is wrong: 12
- strong correct while lite is wrong: 12
- C5 correct while strong is wrong: 0
- strong correct while C5 is wrong: 0

| question_id | lite | strong | C5 | lite error | strong error | C5 error |
|---|---:|---:|---:|---|---|---|
| Q001 | False | True | True | wrong_denotation | correct | correct |
| Q002 | False | True | True | wrong_denotation | correct | correct |
| Q003 | True | True | True | correct | correct | correct |
| Q004 | True | True | True | correct | correct | correct |
| Q005 | False | True | True | wrong_denotation | correct | correct |
| Q006 | False | True | True | wrong_denotation | correct | correct |
| Q007 | False | True | True | wrong_denotation | correct | correct |
| Q008 | True | True | True | correct | correct | correct |
| Q009 | False | True | True | shape_mismatch | correct | correct |
| Q010 | False | True | True | shape_mismatch | correct | correct |
| Q011 | False | True | True | shape_mismatch | correct | correct |
| Q012 | True | True | True | correct | correct | correct |
| Q013 | False | True | True | shape_mismatch | correct | correct |
| Q014 | True | True | True | correct | correct | correct |
| Q015 | False | True | True | shape_mismatch | correct | correct |
| Q016 | True | True | True | correct | correct | correct |
| Q017 | False | True | True | shape_mismatch | correct | correct |
| Q018 | False | True | True | shape_mismatch | correct | correct |
| Q019 | True | True | True | correct | correct | correct |
| Q020 | True | True | True | correct | correct | correct |

## Gold-Leakage Check

- C1_LiteSchemaOnly receives only schema and question.
- C1_StrongDirect and C5 receive answer-shape metadata and required literals, but not gold SQL, gold result rows, expected hashes, or test examples.
- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.
- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this dev-only pilot.

## Decision

C5 improves over schema-only prompting, but not over C1_StrongDirect. The likely contribution is value/shape context rather than reranking superiority.
