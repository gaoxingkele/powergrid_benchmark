# Claims

Route A framework pivot (2026-07-15): the claim system below replaces the former superiority claims. The paper is a framework/benchmark contribution; DSTAR-GRU is the named retrieval component under evaluation, not a superiority-claiming method.

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | **Benchmark contribution**: a method-agnostic, reproducible public curtailment-risk benchmark — full-year RTS-GMLC (8760 h), fixed 70% SNSP-type reference operating policy, onset/transition-slice evaluation protocol (onset threshold 0.02, training-window-calibrated detection thresholds applied identically to all methods), 10-seed Mann-Whitney U + Holm statistical protocol. | Supported | `src/powergrid_benchmark/mintou_real_curtailment.py` (`public_rts_curtailment_v5_onset_eval`); `src/configs/real_curtailment_config.json`; `evidence/runs/real_curtailment_results.csv`; `evidence/tables/real_curtailment_leaderboard.csv`, `real_curtailment_significance.csv` |
| C2 | **Scale-dependent utility of the retrieval component**: learned-embedding Siamese retrieval is significantly beneficial at the 1h horizon (beats all learned baselines and all mechanism ablations: NoSiamese p=0.0004, NoRetrievalBank p=0.001, SmallBank p=0.001, NoTopology p=0.042, LSTM/MLP p=0.001) and significantly harmful for 24h day-ahead onset warning (significantly beaten by NoSiamese, NoRetrievalBank, LSTM, MLP — retrieval pulls predictions toward persistence-like behavior). Both directions carry significance support. | Supported (both directions) | v4/v5 evidence: `evidence/runs/real_curtailment_analysis.md`; `evidence/tables/real_curtailment_significance.csv`; JOURNAL_REVIEW.md progress updates v4/v5 |
| C3 | **Honest negative findings as benchmark discriminative power**: Persistence dominates overall MAE at both horizons (1h -6.4%, 24h -51.6% vs the framework; at 24h Persistence ≡ Seasonal-24h by construction); simple baselines lead 24h onset detection (Ridge F1 0.236, raw-feature kNN 0.226); at 1h onset the framework (F1 0.176) is edged by its own LSTMEncoder (0.185) and NoTopology (0.185) ablations. Reported as-is; these separations demonstrate the benchmark discriminates method families. | Supported (reported honestly) | v5 evidence: `evidence/tables/real_curtailment_leaderboard.csv`; `evidence/runs/real_curtailment_analysis.md` |

## Prohibited claims (禁止条款)

The manuscript must NOT claim any of the following, anywhere (title, abstract, introduction, conclusion):

1. Dispatch-optimization superiority (the v3 dispatch-proxy signal was manufactured by a DSTAR-exclusive bias formula; deprecated, see JOURNAL_REVIEW.md).
2. Topology-uncertainty handling capability (high_topology evidence was a 0.00% tie; NoTopology ablation ties or beats the full model at onset).
3. OPF/AC feasibility of any output (no OPF/UC validation layer; the reference policy is an SNSP-cap proxy).
4. Overall forecasting superiority (Persistence wins overall MAE at both horizons; this is reported as a finding, not hidden).
5. Evidence-free generalization to other power systems (single test system: RTS-GMLC).
