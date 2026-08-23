# Role-Utilization and Score-Ablation Audit

This is a post-review diagnostic over the frozen historical pool, not a prospective role-removal experiment.

## Utilization finding

The Query Analyst feeds aggregation, ordering, and lexical-match features into validation. The Schema Cartographer's grounding is recorded in the blackboard but has no downstream consumer in the frozen historical-pool driver. The candidate provider is a frozen-ledger adapter and makes no model calls. Validation evidence drives both selectors; constructed-state evidence is consumed only by the complete selector.

## Unified-evaluator ablations

| Variant | Correct/180 | Changed choices | Gains/losses vs parent |
|---|---:|---:|---:|
| validation_original | 99/180 | 0 | 0/0 |
| validation_no_query_features | 76/180 | 64 | 2/25 |
| validation_no_shape | 99/180 | 0 | 0/0 |
| validation_no_order | 77/180 | 49 | 1/23 |
| validation_no_value | 99/180 | 14 | 1/1 |
| complete_original | 100/180 | 0 | 0/0 |
| complete_no_query_features | 77/180 | 63 | 2/25 |
| complete_no_constructed_state | 99/180 | 1 | 0/1 |
| complete_no_schema_grounding | 100/180 | 0 | 0/0 |

Removing Schema Cartographer output changes zero selections because the frozen driver never consumes that output. This is an implementation finding, not evidence that schema grounding is generally unnecessary. Removing constructed-state evidence reduces the complete selector exactly to validation-only; its one-match difference is Q039 in the original order.

## Recorded cost boundary

The ledgers contain 3960 blackboard messages and 5760 database attempts, of which 332 failed. Recorded attempt time totals 839.000 ms (median 0.000 ms; p95 0.000 ms). These are local ledger measurements, not deployment-scale or model-token estimates.
