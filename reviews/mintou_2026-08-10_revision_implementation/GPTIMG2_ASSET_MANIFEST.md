# GPT Image 2 Architecture Asset Manifest

All six generated images are **style masters**, not final scientific diagrams. Final labels, arrows, and topology are produced by `scripts/mintou/generate_architecture_figures.py` from verified manuscript/code descriptions.

Common prompt constraints: wide scientific architecture figure; pure white background; flat vector-like design; restrained navy/teal/cool-gray/muted-orange palette; Arial/Helvetica-like typography; consistent thin arrows and rounded boxes; no gradient, shadow, 3D, diagonal hatching, grid texture, logo, or watermark; readable at two-column reduction.

| Paper | Prompt-specific content | Style master | Exact vector source/output |
|---|---|---|---|
| P1 | RTS-GMLC target, temporal windows, GRU, metric embedding, retrieval/head blend, 1 h/24 h metrics | `paper_projects/mintou_p1_dstar_gru_dispatch/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |
| P2 | Multi-region load/calendar, shared encoder, series embedding, three attention-weight switches, fusion, horizons and datasets | `paper_projects/mintou_p2_hygraph_load_forecasting/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |
| P3 | SimBench candidates, jDE/two-strategy DE, decode/repair, constraint selection, archive, HV and AC validation | `paper_projects/mintou_p3_samode_distribution_planning/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |
| P4 | Candidates/scenarios, population-dependent worst-K, hybrid GA/DE, repair, robust selection, held-out stress and AC checks | `paper_projects/mintou_p4_shield_resilience_planning/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |
| P5 | Public projects, five objectives, preference layer, repair, NSGA-II, one-way quarantined trace archive, external checks | `paper_projects/mintou_p5_trace_moea_feasibility_review/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |
| P6 | Candidates/budget/dependencies, NSGA-II, forward/backward moves, dependency repair, selection, negative backward annotation | `paper_projects/mintou_p6_bilonsga_project_review/manuscript/figures/gptimg2_architecture_style_master.png` | `fig_architecture.svg/.pdf/.png` |

The exact generator deliberately corrects generative-image topology errors and preserves negative-result annotations. Re-run with:

```powershell
python scripts\mintou\generate_architecture_figures.py
```
