# MA-SQLGrid evaluator reconciliation report

Status: PASS. No model was called.

Qwen F00 and historical C000 are the same 180 normalized SQL artifacts. The historical row-only evaluator counted 80/180 because it ignored output shape before comparing rows. The frozen unified evaluator enforces the question's expected column count before denotation equality, reproduces all 1,440 canonical-v2 fixed-slot outcomes, and scores C000 as 76/180. Q104, Q107, Q110 and Q140 are the four discrepant empty-result cases; each has row-only equality but a candidate column-count mismatch.

| Method | Correct/180 | Accuracy | Difference vs C000 | 95% composition interval | Rescues/harms | Exact p | Holm p |
|---|---:|---:|---:|---:|---:|---:|---:|
| qwen:F00_Full_NoShape | 76/180 | 0.4222 | +0.0000 | [+0.0000, +0.0000] | 0/0 | 1.000000 | -- |
| qwen:F01_Full_WithShape | 129/180 | 0.7167 | +0.2944 | [+0.2222, +0.3667] | 56/3 | 0.000000 | 0.000000 |
| qwen:F10_Compact_NoShape | 78/180 | 0.4333 | +0.0111 | [-0.0111, +0.0333] | 3/1 | 0.625000 | 1.000000 |
| qwen:F11_Compact_WithShape | 108/180 | 0.6000 | +0.1778 | [+0.1000, +0.2556] | 46/14 | 0.000042 | 0.000211 |
| granite:F00_Full_NoShape | 77/180 | 0.4278 | +0.0056 | [-0.0278, +0.0444] | 6/5 | 1.000000 | 1.000000 |
| granite:F01_Full_WithShape | 100/180 | 0.5556 | +0.1333 | [+0.0500, +0.2222] | 45/21 | 0.004272 | 0.017090 |
| granite:F10_Compact_NoShape | 74/180 | 0.4111 | -0.0111 | [-0.0500, +0.0278] | 6/8 | 0.790527 | 1.000000 |
| granite:F11_Compact_WithShape | 108/180 | 0.6000 | +0.1778 | [+0.1056, +0.2500] | 42/10 | 0.000009 | 0.000054 |
| C000_fixed_order_equal_budget | 76/180 | 0.4222 | +0.0000 | [+0.0000, +0.0000] | 0/0 | 1.000000 | -- |
| validation_rank_equal_budget_no_cf | 99/180 | 0.5500 | +0.1278 | [+0.0778, +0.1833] | 25/2 | 0.000006 | 0.000040 |
| full_coordination_complete_metamorphic | 100/180 | 0.5556 | +0.1333 | [+0.0778, +0.1889] | 26/2 | 0.000003 | 0.000024 |

The intervals are paired question-composition intervals and the exact values are post-result reconciliation tests. They do not support a five-role end-to-end effect claim or power-grid semantic validity beyond this frozen synthetic benchmark.
