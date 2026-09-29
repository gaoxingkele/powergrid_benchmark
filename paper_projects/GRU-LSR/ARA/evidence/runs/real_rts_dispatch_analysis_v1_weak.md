# Real RTS-GMLC Dispatch Analysis - DSTAR-GRU

Status: public RTS-GMLC benchmark-derived dispatch experiment v1. This experiment uses actual RTS-GMLC generators, fuel/cost fields, day-ahead regional load, wind/PV time series, and branch ratings. It is not a full AC-OPF or unit-commitment solver.

- Proposed method: `DSTAR-GRU`
- Proposed composite dispatch score: `0.74111716`
- Best baseline: `Renewable-First ED` with `0.74024403`
- Best ablation: `Ablation-NoTopology` with `0.74228760`
- Relative gain over best baseline: `-0.12%`
- Relative gain over best ablation: `0.16%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This benchmark validates data ingestion, dispatch-state retrieval, renewable curtailment, reserve shortage, topology-risk proxy, baseline coverage, and ablation wiring. It does not prove AC feasibility or production-cost optimality. Manuscript-level claims require OPF/UC solver validation or Grid2Op-style topology experiments.

## Compliant Optimization Path

- Add PGLib/MATPOWER DC-OPF feasibility checks.
- Add rolling scenario splits and renewable-stress subsets.
- Preserve weak baselines and ablations in evidence tables.
