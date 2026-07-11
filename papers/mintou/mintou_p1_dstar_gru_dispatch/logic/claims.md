# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `DSTAR-GRU` improves the benchmark-derived composite dispatch score against target-journal-level baselines. | Supported narrowly by RTS-GMLC v3 | E-real-RTS: fixed score `0.73965420` vs Renewable-First ED `0.74024403`; rolling `0.85295455` vs `0.85352723` |
| C2 | The retrieval/topology-aware component contributes beyond the strongest ablation. | Supported narrowly by RTS-GMLC v3 | E-real-RTS: fixed strongest ablation `0.74228760`; rolling strongest ablation `0.85500571`; high-renewable ablation gap `3.08%` |
| C3 | The method remains feasible under reserve/renewable/topology-risk proxy stress. | Partially supported by RTS-GMLC v3 | E-real-RTS: high-renewable stress gain `0.72%` over best baseline; high-topology and ramp-stress are ties/near ties |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Public benchmark-derived evidence available | E-real-RTS; `src/code/run_real_rts_dispatch.py`; `src/configs/real_rts_dispatch_config.json` |

Current public-data evidence is a narrow positive proxy signal. Strong manuscript claims require OPF/UC feasibility validation and topology-control experiments.
