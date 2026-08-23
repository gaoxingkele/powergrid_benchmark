# Automated Error Taxonomy under the Unified Evaluator

This is a post-review evaluator-state decomposition. It is not expert semantic adjudication and cannot identify business-meaning errors.

| Method | Correct | Execution error | Shape mismatch | Wrong denotation |
|---|---:|---:|---:|---:|
| C000_fixed_order_equal_budget | 76 | 1 | 85 | 18 |
| validation_rank_equal_budget_no_cf | 99 | 0 | 42 | 39 |
| full_coordination_complete_metamorphic | 100 | 0 | 41 | 39 |
| qwen:F01_Full_WithShape | 129 | 5 | 1 | 45 |

Gold execution and gold-shape errors were retained as fail-closed categories; their observed counts are available in `method_error_counts.csv`. The item ledger contains identifiers, labels, counts, and hashes only. Qualified review is still required to distinguish status, time, unit, topology, and operational-intent errors.
