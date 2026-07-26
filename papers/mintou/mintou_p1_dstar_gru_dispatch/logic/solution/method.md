# Method

## Framework pivot note (2026-07-15)

This project pivoted from a method-superiority paper ("similarity-aware multi-objective dispatch") to a **framework/benchmark paper** ("operating-state retrieval framework + reproducible curtailment-risk benchmark"), per the user's Route A decision and third-party review option 7.3-3 ("Operating-state retrieval as a service", `reviews/2026-07-13_round2_mintou_p1_dstar_gru_review.md`). Reasons and evidence chain:

- **v3 (deprecated)**: the RTS-GMLC dispatch-proxy pipeline contained hand constants plus a DSTAR-exclusive renewable-bias formula that manufactured the apparent ~30x curtailment gap; artifacts preserved as historical evidence (`evidence/runs/real_rts_dispatch_*`), disease documented in `JOURNAL_REVIEW.md`.
- **v4 (`public_rts_curtailment_v4_real_models`)**: real rewrite — fixed 70% SNSP-type reference policy, real GRU + learned-embedding Siamese retrieval, 6 baselines + 5 mechanism ablations, 10 seeds, Mann-Whitney/Holm. Component story validated at 1h (significant vs all learned baselines/ablations), but Persistence wins overall MAE at both horizons.
- **v5 (`public_rts_curtailment_v5_onset_eval`)**: full-year 8760 h onset-slice evaluation — final verdict: no defensible superiority on overall MAE, 1h onset, or 24h onset; retrieval is significantly beneficial at 1h and significantly harmful at 24h onset. Superiority framing is therefore abandoned; the scale-dependent-utility characterization and the benchmark itself are the contributions.

## Framework Components

- **Benchmark layer (method-agnostic)**: RTS-GMLC full-year curtailment labels from a fixed reference operating policy (70% instantaneous non-synchronous penetration cap); onset/transition-slice evaluation protocol (onset threshold 0.02; detection thresholds calibrated on the training window, identically for all methods); 10-seed protocol with Mann-Whitney U + Holm.
- **Retrieval component under evaluation**: `DSTAR-GRU` — GRU encoder producing learned embeddings, Siamese retrieval over a historical operating-state bank, validation-set-calibrated blend weights. Named as the framework's retrieval component, with no superiority claim attached.
- **Evaluation matrix**: 6 baselines (incl. Persistence, Seasonal-24h, Ridge, kNN, MLP, LSTM) + 5 mechanism ablations (no_siamese_branch, lstm_encoder, no_retrieval_bank, no_topology_features, small_reference_bank), all under the identical protocol.

## Innovation Handles (framework framing)

- First reproducible public curtailment-risk early-warning benchmark with an onset-slice protocol and seeded statistical testing.
- Complete, significance-backed characterization of the scale-dependent utility of learned-embedding retrieval (1h beneficial / 24h onset harmful).
- Honest negative results (persistence and simple baselines dominate overall MAE and day-ahead onset) presented as evidence of benchmark discriminative power.

## Baseline Coverage (v4/v5 actually run)

- Persistence
- Seasonal-24h
- Ridge
- kNN (raw features)
- MLP
- LSTM

## Ablation Coverage (v4/v5 actually run)

- no_siamese_branch
- lstm_encoder
- no_retrieval_bank
- no_topology_features
- small_reference_bank
