---
title: "An Operating-State Retrieval Framework and Reproducible Curtailment-Risk Benchmark for Power System Decision Support"
tag: "mintou"
paper_id: "mintou_p1"
status: "route_a_framework_pivot_v5"
target_journal: "IEEE Access"
backup_journal: "Applied Sciences"
algorithm: "DSTAR-GRU"
---

# An Operating-State Retrieval Framework and Reproducible Curtailment-Risk Benchmark for Power System Decision Support

## Algorithm Identity

- Short name: `DSTAR-GRU` (retained as the name of the retrieval component inside the framework, not as a superiority-claiming method)
- Full name: Digital-twin Siamese Temporal Alignment and Retrieval GRU
- Tag: `mintou`
- Target journal: IEEE Access (framework/evaluation paper; distilled precedent for internally-compared framework papers)
- Backup journal: Applied Sciences

## Abstract

This is a framework/tool paper, not a method-superiority paper. Its contributions are:

(a) **A method-agnostic, reproducible public curtailment-risk benchmark**: full-year RTS-GMLC (8760 hours), curtailment defined by a fixed reference operating policy with a 70% instantaneous non-synchronous penetration (SNSP-type) cap, an onset/transition-slice evaluation protocol for the operationally relevant warning moments (onset threshold 0.02, detection thresholds calibrated on the training window identically for all methods), and a 10-seed statistical protocol (Mann-Whitney U with Holm correction).

(b) **An operating-state retrieval framework with learned-embedding Siamese retrieval (DSTAR-GRU) and a complete characterization of its scale-dependent utility**: at the 1h horizon the Siamese retrieval component is significantly better than all learned baselines and all mechanism ablations (NoSiamese p=0.0004, NoRetrievalBank p=0.001, LSTM/MLP p=0.001); at the 24h day-ahead onset horizon the same retrieval mechanism is significantly harmful — it pulls predictions toward persistence-like behavior and is significantly beaten by NoSiamese, NoRetrievalBank, LSTM, and MLP. Retrieval-based decision support is thus beneficial for short-horizon smoothing and detrimental for day-ahead warning.

(c) **Honest negative findings as evidence of benchmark discriminative power**: naive Persistence dominates overall MAE at both horizons (1h -6.4%, 24h -51.6% against the framework), and simple baselines (Ridge F1 0.236, raw-feature kNN 0.226) lead 24h onset detection, while the framework's own LSTMEncoder/NoTopology ablations edge it at 1h onset. These results are reported as findings, not failures: they demonstrate that the benchmark separates method families and exposes where learned retrieval helps and where it hurts.

No dispatch-optimization superiority, topology-uncertainty capability, OPF feasibility, or overall forecasting superiority is claimed.

## Current Engineering Status

The benchmark pipeline (`src/powergrid_benchmark/mintou_real_curtailment.py`, v4 `public_rts_curtailment_v4_real_models` → v5 `public_rts_curtailment_v5_onset_eval`) is implemented and fully run: fixed reference policy, real GRU encoder + learned-embedding Siamese retrieval, 6 baselines + 5 mechanism ablations, 10 seeds, Mann-Whitney/Holm. Evidence lives in `evidence/runs/real_curtailment_*` and `evidence/tables/real_curtailment_*`.

Historical evidence: the v3 dispatch-proxy artifacts (`real_rts_dispatch_*`) are preserved as deprecated history — the v3 pipeline contained a proxy-method disease (hand constants plus a DSTAR-exclusive renewable-bias formula that manufactured the apparent curtailment gap), documented in `JOURNAL_REVIEW.md`. The v3→v5 evidence chain is itself part of the paper's methodological narrative.

## Boundary

The reference operating policy is an SNSP-cap proxy, not AC-OPF or unit commitment; curtailment-risk labels are policy-derived, and all claims are scoped to the benchmark protocol and the retrieval component's measured, scale-dependent utility. No claim of dispatch-optimization advantage is made anywhere in the manuscript.
