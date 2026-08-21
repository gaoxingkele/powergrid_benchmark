# Experiment Artifact Audit and Paired Statistics

- Overall audit: **PASS**
- Input: `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\w2_ma\new_deterministic_predictions_scores.jsonl`
- SHA-256: `23e73d7fa90190f0581f0e8078641cdf878ce70dba5573b7ad7153b379a50cd1`
- Rows / items / clusters: 360 / 180 / 180
- Conditions: DEV_1NN_SQL_COPY, DEV_1NN_LITERAL_TRANSFER
- Cartesian cells (observed/expected): 360/360

## Audit findings

No schema, completeness, identity, cluster, or hash defects were detected.

## Paired comparisons

| Baseline | Treatment | Metric | Pairs | Delta | Bootstrap CI | McNemar p | Holm p |
|---|---|---|---:|---:|---|---:|---:|
| DEV_1NN_SQL_COPY | DEV_1NN_LITERAL_TRANSFER | strict_execution_correct | 180 | 0.0111111 | [0, 0.0277778] | 0.5 | 1 |
| DEV_1NN_SQL_COPY | DEV_1NN_LITERAL_TRANSFER | projection_contract_correct | 180 | 0 | [0, 0] | 1 | 1 |
| DEV_1NN_SQL_COPY | DEV_1NN_LITERAL_TRANSFER | sql_executable | 180 | 0 | [0, 0] | 1 | 1 |
| DEV_1NN_SQL_COPY | DEV_1NN_LITERAL_TRANSFER | safe_sql | 180 | 0 | [0, 0] | 1 | 1 |

## Interpretation contract

Positive delta means treatment minus baseline. Confidence intervals use paired cluster resampling; McNemar is emitted only for binary paired outcomes. Holm adjustment spans all applicable pairwise metric tests in this report.
