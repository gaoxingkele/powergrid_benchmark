# MA-SQLGrid R3 Complete Descriptive Evidence Tables

These tables are deterministic recomputations from retained ledgers. They involve no model call, no new label, and no post-hoc rule selection. Source paths, SHA-256 values, and byte counts are recorded in `R3_EVIDENCE_TABLES.json`.

## Top-tie diagnostic

| method | questions | top_ties | mean_multiplicity | multiplicity_counts |
|---|---|---|---|---|
| validation_rank_equal_budget_no_cf | 180 | 130 | 5.4000 | {"1": 50, "2": 5, "3": 3, "4": 4, "5": 5, "6": 8, "7": 26, "8": 79} |
| full_coordination_complete_metamorphic | 180 | 130 | 5.3889 | {"1": 50, "2": 5, "3": 3, "4": 4, "5": 5, "6": 9, "7": 26, "8": 78} |

The original-order rule is arbitrary for this outcome-exposed release. The complete 360-row item table and selected-source distributions are retained in the JSON/CSV artifacts.

## GridDB eight cells

| backbone | condition | correct | n | rate |
|---|---|---|---|---|
| qwen | F00_Full_NoShape | 76 | 180 | 0.4222 |
| qwen | F01_Full_WithShape | 129 | 180 | 0.7167 |
| qwen | F10_Compact_NoShape | 78 | 180 | 0.4333 |
| qwen | F11_Compact_WithShape | 108 | 180 | 0.6000 |
| granite | F00_Full_NoShape | 77 | 180 | 0.4278 |
| granite | F01_Full_WithShape | 100 | 180 | 0.5556 |
| granite | F10_Compact_NoShape | 74 | 180 | 0.4111 |
| granite | F11_Compact_WithShape | 108 | 180 | 0.6000 |

## Component endpoints

| backbone | condition | endpoint | correct | n | rate |
|---|---|---|---|---|---|
| qwen | V0_NoValueEvidence | first_correct | 83 | 170 | 0.4882 |
| qwen | V0_NoValueEvidence | validator_selected_correct | 83 | 170 | 0.4882 |
| qwen | V0_NoValueEvidence | oracle_at_3_correct_diagnostic_only | 100 | 170 | 0.5882 |
| qwen | V1_WithValueEvidence | first_correct | 105 | 180 | 0.5833 |
| qwen | V1_WithValueEvidence | validator_selected_correct | 112 | 180 | 0.6222 |
| qwen | V1_WithValueEvidence | oracle_at_3_correct_diagnostic_only | 115 | 180 | 0.6389 |
| granite | V0_NoValueEvidence | first_correct | 69 | 170 | 0.4059 |
| granite | V0_NoValueEvidence | validator_selected_correct | 69 | 170 | 0.4059 |
| granite | V0_NoValueEvidence | oracle_at_3_correct_diagnostic_only | 72 | 170 | 0.4235 |
| granite | V1_WithValueEvidence | first_correct | 71 | 180 | 0.3944 |
| granite | V1_WithValueEvidence | validator_selected_correct | 81 | 180 | 0.4500 |
| granite | V1_WithValueEvidence | oracle_at_3_correct_diagnostic_only | 84 | 180 | 0.4667 |

## Fifteen-state eight cells

| backbone | condition | passed_all_15_states | n | rate |
|---|---|---|---|---|
| granite | F00_Full_NoShape | 54 | 66 | 0.8182 |
| granite | F01_Full_WithShape | 41 | 66 | 0.6212 |
| granite | F10_Compact_NoShape | 51 | 66 | 0.7727 |
| granite | F11_Compact_WithShape | 49 | 66 | 0.7424 |
| qwen | F00_Full_NoShape | 49 | 66 | 0.7424 |
| qwen | F01_Full_WithShape | 48 | 66 | 0.7273 |
| qwen | F10_Compact_NoShape | 53 | 66 | 0.8030 |
| qwen | F11_Compact_WithShape | 43 | 66 | 0.6515 |

## Selector sensitivity: all 18 cells

| weight_policy | minimum_invariant_passes | tie_rule | correct | covered | n | accuracy_all |
|---|---|---|---|---|---|---|
| default | 1 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| default | 1 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| default | 2 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| default | 2 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| default | 3 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| default | 3 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| intent_emphasis | 1 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| intent_emphasis | 1 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| intent_emphasis | 2 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| intent_emphasis | 2 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| intent_emphasis | 3 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| intent_emphasis | 3 | reverse_candidate_order | 117 | 180 | 180 | 0.6500 |
| validation_equal | 1 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| validation_equal | 1 | reverse_candidate_order | 118 | 180 | 180 | 0.6556 |
| validation_equal | 2 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| validation_equal | 2 | reverse_candidate_order | 118 | 180 | 180 | 0.6556 |
| validation_equal | 3 | original_candidate_order | 101 | 180 | 180 | 0.5611 |
| validation_equal | 3 | reverse_candidate_order | 118 | 180 | 180 | 0.6556 |

## Q039 projection trace

| method | selected_candidate_id | correct | robust_invariance | gold_access_phase |
|---|---|---|---|---|
| fixed_order_equal_budget | C000 | False | False | after_all_blackboards_sealed |
| validation_rank_equal_budget_no_cf | C000 | False | False | after_all_blackboards_sealed |
| full_coordination_complete_metamorphic | C001 | True | True | after_all_blackboards_sealed |

Q039 is an outcome-exposed synthetic projection trace. The SQL text is retained in the JSON/CSV artifact; this case is not evidence of a general semantic rescue, counterfactual-reasoning benefit, robustness gain, or multi-agent gain.
