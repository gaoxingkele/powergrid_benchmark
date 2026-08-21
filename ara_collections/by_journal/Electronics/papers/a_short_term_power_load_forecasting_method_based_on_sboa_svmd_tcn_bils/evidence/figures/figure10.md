# Figure 10: Optimization fitness curves

- **Source**: Figure 10, Section 5.4, p. 16 (top of page)
- **Caption**: "Optimization fitness curves."
- **Screenshot**: figure10.png (page 16; Figure 10 is at the top, above Table 3 and Figure 11)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium

- **Plot kind**: line (convergence curves for SBOA, SSA, GWO; objective = minimum permutation entropy)
- **Axes**: X = Number of iterations, linear, 0–60. Left Y = Fitness (SBOA/SSA), linear, ≈0.618730–0.618760. Right Y = Fitness (GWO), linear, ≈0.6187415–0.6187450 (GWO plotted on a separate finer right axis).

| Series | Convergence behavior (approx.) |
|--------|-------------------------------|
| SBOA | Drops in a step near iter ≈40–45 to the lowest final fitness (≈0.618728 on left axis); stable afterward |
| SSA | Steep early drop (first ~5 iters) then plateaus around ≈0.618730; some fluctuation, slower |
| GWO | Nearly flat on its own right axis (≈0.6187418); never reaches SBOA/SSA level |

## Trend summary
SBOA converges to the lowest fitness (best/minimum permutation entropy) and stabilizes without over-searching or local-optima trapping; SSA declines fast early but is less stable; GWO stays flat and worst. Note: SBOA and GWO are drawn on different y-axes, so absolute values are not directly comparable — the paper's claim is the qualitative ordering SBOA < SSA, with GWO failing to reach that level. Exact values read approximately from axes.
