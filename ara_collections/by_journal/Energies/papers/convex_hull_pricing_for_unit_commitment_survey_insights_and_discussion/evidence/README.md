# Evidence Index

This survey contains **9 numbered figures (Figure 1–Figure 9)** and **no numbered tables**. Every
figure is filed below with both a markdown transcription/description and a rendered screenshot
(`.png`). All figures in this paper are conceptual diagrams (geometry of convex hulls/envelopes,
reformulation schematics, algorithm-convergence depictions); Figure 7 is a quantitative-style
convergence-trajectory plot and is filed as such. The paper reports no result tables — its
"results" are synthesized conclusions about the surveyed approaches, captured in `logic/claims.md`.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| — | — | — | No numbered tables appear in this survey. |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §1 | C01 | Convex envelope (tightest convex under-estimator) and convex hull (smallest convex set of feasible points), MILP illustration |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3.2 | C05, C06 | Convex fuel-cost case: integer relaxation yields convex envelope over convex hull (two-block example) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §3.2 | C05, C06 | Non-convex fuel-cost case: commitment-variable scaling convexifies the cost for the convex envelope |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §3.2 | C06, C07 | State transition diagram enumerating commitment statuses; (x_e, y_e) network-flow reformulation |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §3.3 | C06, C07 | DP-to-dual mapping: single-unit convex hull vertices map to dual-problem vertices |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §3.4 | C08 | Systematic tightening: relax integrality, drop fractional vertices, re-derive tight (approximate) convex hulls |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.2 | C09 | Convergence trajectories: extreme-point subdifferential (smooth) vs subgradient (zigzagging) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4.2 | C09 | Level method: projection of price onto the level set for smoother updates |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4.3 | C10 | Novel SLR-based quality measure: upper-minus-lower bound on optimal dual value vs standard duality gap |

## Notes on accounting
- Objects filed: Figure 1–9 (9 of 9). None omitted.
- No `Table N` object exists in the source (verified by full-text scan of all 20 pages).
- Equations (1)–(26) are formulations, not numbered figures/tables; they are transcribed in
  `logic/solution/uc_formulation.md` and `logic/solution/dual_approaches.md`.
