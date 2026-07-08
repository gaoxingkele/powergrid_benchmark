# MA-SQLGrid C1-C5 Experiment Report

## Scope

- Run mode: `smoke`.
- Records: 1.
- Seeds: [0, 1, 2].
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

- Prediction records: 15.
- Contract-error records: 0.
- Unsafe-SQL records: 0.
- Provider/model/extraction error records: 0.
- Leakage scan problems: 0.

## Metrics

| condition | execution accuracy mean | std | valid SQL | shape accuracy | value coverage | prompt tokens | latency ms | errors |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| C1_SchemaOnly_Direct | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 367.0 | 1511.3 | {'wrong_denotation': 3} |
| C2_FullSchemaValues_Direct | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 696.0 | 1647.0 | none |
| C3_CHESSLite_Generic | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 166.0 | 3059.3 | {'wrong_denotation': 3} |
| C4_MASQLGrid_DomainContext | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 227.0 | 2197.3 | none |
| C5_MASQLGrid_DomainContext_Validated | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 222.0 | 2310.0 | none |

## Leakage Scan

- No forbidden prompt/trace or prediction-record tokens found.
