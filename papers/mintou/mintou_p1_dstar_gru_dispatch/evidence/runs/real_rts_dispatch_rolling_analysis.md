# RTS-GMLC Rolling Dispatch Analysis - DSTAR-GRU

Status: rolling scenario-window benchmark over `3` windows. Lower composite score is better.

- Proposed mean composite score: `0.85295455` +/- `0.05477114`
- Best baseline: `Renewable-First ED` with `0.85352723`
- Best ablation: `Ablation-NoTopology` with `0.85500571`
- Relative gain over best baseline: `0.07%`
- Relative gain over best ablation: `0.24%`
- Rolling value signal: `promising_rolling_signal`

## Boundary

Rolling dispatch evidence improves temporal robustness evidence but remains a standard-library proxy. OPF/UC validation is still required for production-grade claims.
