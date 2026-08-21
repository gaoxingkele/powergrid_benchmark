# MA-SQLGrid C1-C5 Experiment Report

## Scope

- Run mode: `formal`.
- Records: 1.
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

- Prediction records: 5.
- Contract-error records: 0.
- Unsafe-SQL records: 0.
- Provider/model/extraction error records: 0.
- Leakage scan problems: 0.

## Metrics

| condition | execution accuracy mean | std | valid SQL | shape accuracy | value coverage | prompt tokens | latency ms | errors |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| C1_SchemaOnly_Direct | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 364.0 | 1433.0 | {'wrong_denotation': 1} |
| C2_FullSchemaValues_Direct | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 693.0 | 2315.0 | {'wrong_denotation': 1} |
| C3_CHESSLite_Generic | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 174.0 | 1776.0 | {'wrong_denotation': 1} |
| C4_MASQLGrid_DomainContext | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 236.0 | 1487.0 | none |
| C5_MASQLGrid_DomainContext_Validated | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 231.0 | 8684.0 | none |

## Leakage Scan

- No forbidden prompt/trace or prediction-record tokens found.
