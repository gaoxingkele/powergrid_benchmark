# Dev-Only CHESS-Style MA-SQLGrid Feasibility Pilot

## Scope

- Purpose: test whether a CHESS-style pipeline with power-grid domain context, value normalization, shape control, and validation is viable before three-pack generation.
- This is not a formal experiment and must not be used for paper claims.
- Split: dev only, Q001-Q020. The test split Q021-Q200 is not evaluated.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.

## Conditions

- C1_SchemaOnly_Direct: full schema and question only.
- C2_FullSchemaValues_Direct: full schema plus database value dictionary, without gold metadata.
- C3_CHESSLite_Generic: generic keyword/value retrieval, schema selection, and direct SQL generation.
- C4_MASQLGrid_DomainContext: C3 plus power-grid domain normalization and answer-shape hints inferred from question text.
- C5_MASQLGrid_DomainContext_Validated: C4 plus multi-candidate generation, reference-free execution/shape/value validation, ranking, and one repair opportunity.

## Artifacts

- predictions: `smoke/dev_chess_style/predictions.jsonl`
- scores: `smoke/dev_chess_style/scores.jsonl`
- contexts: `smoke/dev_chess_style/contexts.jsonl`
- traces: `smoke/dev_chess_style/traces/`

## Contract And Runtime Checks

- prediction records written: 100
- expected records: 100
- records with contract errors: 0
- records with unsafe SQL: 0
- records with model/extraction/provider errors: 0
- provider/model failure counts by condition: none
- outer model-call retries by condition: {'C1_SchemaOnly_Direct': 0, 'C2_FullSchemaValues_Direct': 0, 'C3_CHESSLite_Generic': 0, 'C4_MASQLGrid_DomainContext': 0, 'C5_MASQLGrid_DomainContext_Validated': 0}
- Note: the project LLM client may perform internal retries before surfacing an exception; those internal retries are visible in console logs but are not exposed in prediction records.

## Accuracy, Validity, And Prompt Size

| condition | records | correct | accuracy | valid SQL rate | avg prompt tokens est. | evaluator errors |
|---|---:|---:|---:|---:|---:|---|
| C1_SchemaOnly_Direct | 20 | 8 | 0.400 | 1.000 | 366.9 | {'wrong_denotation': 6, 'shape_mismatch': 6} |
| C2_FullSchemaValues_Direct | 20 | 13 | 0.650 | 1.000 | 696.0 | {'wrong_denotation': 3, 'shape_mismatch': 4} |
| C3_CHESSLite_Generic | 20 | 8 | 0.400 | 1.000 | 180.9 | {'wrong_denotation': 4, 'execution_error': 1, 'shape_mismatch': 7} |
| C4_MASQLGrid_DomainContext | 20 | 13 | 0.650 | 1.000 | 244.9 | {'wrong_denotation': 3, 'shape_mismatch': 4} |
| C5_MASQLGrid_DomainContext_Validated | 20 | 13 | 0.650 | 1.000 | 242.9 | {'wrong_denotation': 3, 'shape_mismatch': 4} |

## Shape And Value Diagnostics

| condition | shape mismatches by inferred shape | missing value-hint records | execution failures | empty-result records |
|---|---:|---:|---:|---:|
| C1_SchemaOnly_Direct | 12 | 0 | 0 | 3 |
| C2_FullSchemaValues_Direct | 11 | 0 | 0 | 0 |
| C3_CHESSLite_Generic | 9 | 0 | 1 | 2 |
| C4_MASQLGrid_DomainContext | 0 | 0 | 0 | 0 |
| C5_MASQLGrid_DomainContext_Validated | 0 | 0 | 0 | 0 |

## Context Selection Diagnostics

- Generic context average table recall vs dev metadata: 1.000
- Generic context average column recall vs dev metadata: 0.711
- Generic context average value recall vs dev metadata: 0.675
- Domain context average table recall vs dev metadata: 1.000
- Domain context average column recall vs dev metadata: 0.929
- Domain context average value recall vs dev metadata: 1.000

| question_id | generic table R | generic column R | generic value R | domain table R | domain column R | domain value R |
|---|---:|---:|---:|---:|---:|---:|
| Q001 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| Q002 | 1.000 | 0.333 | 0.000 | 1.000 | 1.000 | 1.000 |
| Q003 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q004 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| Q005 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q006 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 1.000 |
| Q007 | 1.000 | 0.333 | 0.500 | 1.000 | 0.667 | 1.000 |
| Q008 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 1.000 |
| Q009 | 1.000 | 0.333 | 0.500 | 1.000 | 1.000 | 1.000 |
| Q010 | 1.000 | 1.000 | 1.000 | 1.000 | 0.750 | 1.000 |
| Q011 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q012 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q013 | 1.000 | 0.667 | 0.667 | 1.000 | 1.000 | 1.000 |
| Q014 | 1.000 | 0.800 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q015 | 1.000 | 0.750 | 0.500 | 1.000 | 1.000 | 1.000 |
| Q016 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q017 | 1.000 | 0.667 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q018 | 1.000 | 0.333 | 0.500 | 1.000 | 0.667 | 1.000 |
| Q019 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q020 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 |

## Paired Viability Checks

- C4 correct while C1 is wrong: 5
- C5 correct while C1 is wrong: 5
- C4 correct while C3 is wrong: 6
- C5 correct while C3 is wrong: 6
- C2 correct while C5 is wrong: 2
- C5 correct while C2 is wrong: 2

| question_id | C1 | C2 | C3 | C4 | C5 | C1 error | C3 error | C5 error |
|---|---:|---:|---:|---:|---:|---|---|---|
| Q001 | False | True | False | True | True | wrong_denotation | wrong_denotation | correct |
| Q002 | False | True | False | True | True | wrong_denotation | execution_error | correct |
| Q003 | True | True | False | True | True | correct | wrong_denotation | correct |
| Q004 | True | True | True | True | True | correct | correct | correct |
| Q005 | False | False | False | True | True | wrong_denotation | shape_mismatch | correct |
| Q006 | False | True | True | False | False | wrong_denotation | correct | wrong_denotation |
| Q007 | False | False | False | False | False | wrong_denotation | shape_mismatch | shape_mismatch |
| Q008 | True | True | True | True | True | correct | correct | correct |
| Q009 | False | False | False | True | True | shape_mismatch | wrong_denotation | correct |
| Q010 | False | False | False | False | False | shape_mismatch | shape_mismatch | wrong_denotation |
| Q011 | False | True | False | False | False | shape_mismatch | wrong_denotation | shape_mismatch |
| Q012 | True | True | True | True | True | correct | correct | correct |
| Q013 | True | True | True | True | True | correct | correct | correct |
| Q014 | False | False | False | False | False | shape_mismatch | shape_mismatch | shape_mismatch |
| Q015 | False | False | False | False | False | shape_mismatch | shape_mismatch | shape_mismatch |
| Q016 | True | True | True | True | True | correct | correct | correct |
| Q017 | True | True | False | True | True | correct | shape_mismatch | correct |
| Q018 | False | False | False | False | False | shape_mismatch | shape_mismatch | wrong_denotation |
| Q019 | True | True | True | True | True | correct | correct | correct |
| Q020 | False | True | True | True | True | wrong_denotation | correct | correct |

## Gold-Leakage Check

- C1 receives only schema and question.
- C2 receives schema, database value dictionary, and question; it does not receive answer-shape metadata, required-literal metadata, order-sensitive metadata, gold SQL, or gold result rows.
- C3/C4/C5 context selection uses question text, schema, foreign-key graph, database values, and fixed local normalization rules only.
- Dev metadata is used only after prediction generation for scoring and diagnostic recall/error analysis.
- C5 validation uses only read-only execution status, inferred shape, inferred value hints, and inferred ordering hints. It does not use evaluator denotation feedback.

## Decision

PASS: the CHESS-style MA-SQLGrid direction is viable on this dev-only pilot. C4/C5 improve over schema-only and generic CHESS-lite context while staying close enough to the full-schema-values direct baseline to justify prepare-paper packaging.
