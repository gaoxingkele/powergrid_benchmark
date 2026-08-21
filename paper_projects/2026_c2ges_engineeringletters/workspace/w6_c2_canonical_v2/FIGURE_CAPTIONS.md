# Canonical Figure Captions

## fig01_k_sensitivity_f1

Five-seed evidence F1 across evidence budgets; error bars are +/-1 sample SD over training seeds. Oracle-label (hollow marker) is conditional and not end-to-end. The frozen role-conditioning claim is NO-GO, and K=1 remains below BM25.

## fig02_role_effect_forest

Protocol differences with 95% hierarchical seed/Wikipedia-document bootstrap intervals. Every role comparison at the primary K=3 crosses zero, establishing the role-effect NO-GO boundary. Oracle-label comparisons are conditional rather than end-to-end.

## fig03_compute_accuracy_tradeoff

Measured full-script CPU wall time versus K=3 evidence F1; horizontal and vertical error bars are +/-1 seed SD. This is training-plus-evaluation cost, not per-query latency. Oracle-label is a conditional upper-bound protocol, and the role-effect claim remains NO-GO.

## fig04_seed_stability_k3

Per-seed K=3 difference from the fixed BM25 result. Lines show all five frozen seeds without seed selection. Oracle-label is conditional; the predicted-versus-label-blind role effect is NO-GO under the frozen criterion.

## fig05_k3_case_stability

Deterministic K=3 instance outcomes for predicted-label C2GES versus BM25 across all five seeds. Categories use only gold/predicted sentence IDs and evidence F1; they are not semantic error labels. The aggregate role-effect claim is NO-GO.
