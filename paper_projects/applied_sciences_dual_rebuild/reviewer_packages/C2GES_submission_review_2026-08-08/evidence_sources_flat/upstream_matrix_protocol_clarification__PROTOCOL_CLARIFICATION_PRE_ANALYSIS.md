# Pre-analysis clarification

**Recorded:** 2026-08-06 17:18 +08:00, while the formal matrix was still running and before any new performance outcome was inspected.

The frozen JSON correctly defines the primary estimand as predicted-role, full-mode macro evidence F1 at K=3. Its `primary_variance_question` also mentions a full-minus-label-blind contrast. The 25-run matrix does not retrain a separate label-blind model inside every upstream cell; it contains the predicted-role model and its existing inference modes. Consequently:

1. the confirmatory analysis is the variation of predicted-role full-mode F1 across five grouped-OOF upstream refits and five downstream training seeds;
2. the `no_role` row may be reported only as an inference ablation and must not be renamed a retrained label-blind model or used to claim a causal role contribution;
3. the previously reported five-seed retrained label-blind experiment remains the authoritative role-effect analysis;
4. no seed, run, cutoff, model, or endpoint is added or removed.

This clarification narrows an over-broad sentence in the freeze; it does not respond to an observed result.
