# Dev-Only AutoCompact Context Pilot

## Scope

- Purpose: test whether automatic compact context approaches full-context accuracy with materially smaller prompts.
- This is not a formal experiment and must not be used for paper claims.
- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.

## Conditions

- C1_SchemaOnly: full schema and question only.
- C2_FullContext: full schema, compact value dictionary, answer-shape metadata, order sensitivity, and required literals.
- C3_AutoCompactContext: deterministic question/schema/DB-value selector builds compact context, then one SQL generation call.
- C4_AutoCompactContext_Validated: C3 plus one execution/shape repair attempt when validation fails.

## Artifacts

- predictions: `smoke/dev_autocompact/predictions.jsonl`
- scores: `smoke/dev_autocompact/scores.jsonl`
- contexts: `smoke/dev_autocompact/contexts.jsonl`
- traces: `smoke/dev_autocompact/traces/`

## Contract And Runtime Checks

- prediction records written: 80
- expected records: 80
- records with contract errors: 0
- records with unsafe SQL: 0
- records with model/extraction errors: 0

## Accuracy And Prompt Size

| condition | records | correct | accuracy | avg prompt tokens est. | errors |
|---|---:|---:|---:|---:|---|
| C1_SchemaOnly | 20 | 9 | 0.450 | 354.9 | {'wrong_denotation': 3, 'shape_mismatch': 8} |
| C2_FullContext | 20 | 20 | 1.000 | 561.4 | none |
| C3_AutoCompactContext | 20 | 9 | 0.450 | 117.0 | {'wrong_denotation': 3, 'shape_mismatch': 8} |
| C4_AutoCompactContext_Validated | 20 | 9 | 0.450 | 117.0 | {'wrong_denotation': 3, 'shape_mismatch': 8} |

## AutoCompact Context Selection Quality

- average table recall vs dev metadata: 1.000
- average column recall vs dev metadata: 1.000
- average value recall vs dev metadata: 0.742
- C3 prompt token reduction vs C2: 79.2%
- C4 prompt token reduction vs C2: 79.2%
- C3 matches C2 correctness on 9/20 dev questions
- C4 matches C2 correctness on 9/20 dev questions

| question_id | table_recall | column_recall | value_recall | selected_tables | selected_columns | matched_values |
|---|---:|---:|---:|---:|---:|---:|
| Q001 | 1.000 | 1.000 | 0.000 | 4 | 24 | 1 |
| Q002 | 1.000 | 1.000 | 1.000 | 4 | 25 | 2 |
| Q003 | 1.000 | 1.000 | 1.000 | 4 | 25 | 2 |
| Q004 | 1.000 | 1.000 | 0.000 | 4 | 28 | 1 |
| Q005 | 1.000 | 1.000 | 1.000 | 4 | 25 | 2 |
| Q006 | 1.000 | 1.000 | 1.000 | 4 | 27 | 3 |
| Q007 | 1.000 | 1.000 | 0.500 | 5 | 30 | 4 |
| Q008 | 1.000 | 1.000 | 0.333 | 4 | 25 | 4 |
| Q009 | 1.000 | 1.000 | 0.500 | 4 | 27 | 3 |
| Q010 | 1.000 | 1.000 | 1.000 | 4 | 30 | 2 |
| Q011 | 1.000 | 1.000 | 1.000 | 4 | 28 | 2 |
| Q012 | 1.000 | 1.000 | 1.000 | 4 | 27 | 1 |
| Q013 | 1.000 | 1.000 | 1.000 | 4 | 24 | 5 |
| Q014 | 1.000 | 1.000 | 1.000 | 5 | 32 | 4 |
| Q015 | 1.000 | 1.000 | 0.500 | 4 | 27 | 4 |
| Q016 | 1.000 | 1.000 | 1.000 | 4 | 27 | 1 |
| Q017 | 1.000 | 1.000 | 1.000 | 4 | 26 | 3 |
| Q018 | 1.000 | 1.000 | 0.500 | 4 | 25 | 3 |
| Q019 | 1.000 | 1.000 | 1.000 | 4 | 27 | 4 |
| Q020 | 1.000 | 1.000 | 0.500 | 4 | 25 | 2 |

## Gold-Leakage Check

- AutoCompact selection uses only question text, schema, foreign-key graph, and database values.
- Dev metadata is used only after prediction generation to compute table/column/value recall in this report.
- C2_FullContext includes metadata and is therefore an oracle-like full-context reference, not a deployable baseline.
- C4 repair uses only SQL execution errors from the local database, not gold denotation feedback.
- Gold SQL and gold result rows are used only by `evaluator.score_prediction` after prediction generation.

## Decision

AutoCompact does not yet reach the near-FullContext accuracy plus prompt-reduction target.
