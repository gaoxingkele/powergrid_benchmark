# MA-SQLGrid C1-C5 Experiment Report

## Scope

- Run mode: `formal`.
- Records: 180.
- Seeds: [0].
- Formal seed policy: `single deterministic pass`.
- Dev smoke seed policy: `three-seed dev smoke for contract evidence only`.
- Model/provider: `gpt-5.4-mini` via `krill` `https://api.krill-ai.com/codex/v1` with `wire_api=responses` and temperature `0`.
- Dataset: controlled deterministic GridDB-Maintenance-v2 v0.1.

## Conditions

- C1_SchemaOnly_Direct
- C2_FullSchemaValues_Direct
- C3_CHESSLite_Generic
- C4_MASQLGrid_DomainContext
- C5_MASQLGrid_DomainContext_Validated

## Contract Checks

- Prediction records: 900.
- Contract-error records: 0.
- Unsafe-SQL records: 0.
- Provider/model/extraction error records: 0.
- Leakage scan problems: 0.

## Metrics

| condition | execution accuracy mean | std | valid SQL | shape accuracy | value coverage | prompt tokens | latency ms | errors |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| C1_SchemaOnly_Direct | 0.3944 | 0.0000 | 1.0000 | 0.3278 | 1.0000 | 381.3 | 3259.8 | {'shape_mismatch': 95, 'wrong_denotation': 14} |
| C2_FullSchemaValues_Direct | 0.4389 | 0.0000 | 1.0000 | 0.3667 | 1.0000 | 710.3 | 2959.0 | {'wrong_denotation': 11, 'shape_mismatch': 90} |
| C3_CHESSLite_Generic | 0.4000 | 0.0000 | 1.0000 | 0.5056 | 1.0000 | 202.0 | 2895.1 | {'wrong_denotation': 26, 'shape_mismatch': 67, 'execution_error': 15} |
| C4_MASQLGrid_DomainContext | 0.7000 | 0.0000 | 1.0000 | 0.8889 | 0.9716 | 259.2 | 2887.5 | {'wrong_denotation': 34, 'execution_error': 20} |
| C5_MASQLGrid_DomainContext_Validated | 0.7278 | 0.0000 | 1.0000 | 0.9722 | 0.9972 | 258.2 | 5562.5 | {'wrong_denotation': 44, 'execution_error': 5} |

## Leakage Scan

- No forbidden prompt/trace or prediction-record tokens found.
