# MA-SQLGrid Component Ablation Addendum

## Scope

- Split: held-out GridDB-Maintenance-v2 v0.1 test questions Q021-Q200.
- Generator/provider: same fixed provider contract as the repaired C1-C5 formal run.
- Decoding: temperature 0; seed 0 is a deterministic pass label.
- Contract: no gold SQL, gold denotation rows, evaluator correctness, required-literal metadata, answer-shape metadata, or order-sensitive metadata in prompts or prediction records.
- Status: addendum only; it does not replace the repaired C1-C5 main results.

## Conditions

- C4_NoValueHints: uses the C4 domain-selected schema and answer-shape hints but removes exact matched values and normalized value hints from the prompt.
- C4_NoShapeHints: uses the C4 domain-selected schema and value hints but removes answer-shape hints from the prompt.

## Results

| condition | correct | execution accuracy | safe SQL | answer-shape accuracy | prompt tokens | latency ms | error taxonomy |
|---|---:|---:|---:|---:|---:|---:|---|
| C4_NoValueHints | 118/180 | 0.6556 | 1.0000 | 0.9167 | 233.0 | 4718.7 | {'wrong_denotation': 47, 'execution_error': 14, 'shape_mismatch': 1} |
| C4_NoShapeHints | 77/180 | 0.4278 | 1.0000 | 0.4389 | 229.7 | 4404.7 | {'wrong_denotation': 9, 'shape_mismatch': 89, 'execution_error': 5} |
