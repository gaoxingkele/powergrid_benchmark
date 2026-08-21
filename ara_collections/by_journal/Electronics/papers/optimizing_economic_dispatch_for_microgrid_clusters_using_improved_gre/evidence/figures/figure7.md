# Figure 7: Comparison of improved GWO (CDGWO) with common intelligent optimization algorithms

- **Source**: Figure 7, Section 4.3.1
- **Caption**: "Comparison of improved GWO (CDGWO) with common intelligent optimization algorithms."
- **Screenshot**: figure7.png
- **Location on page**: Page 13 (PDF page 13), lower portion of the page.
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: low
- **Plot kind**: line
- **Axes**: X = Number of Iterations (0-500, linear), Y = Fitness Value (×10^4, 0-3.5, linear)

| Series (legend) | Qualitative convergence behaviour |
|---|---|
| CDGWO | Converges fastest to the lowest fitness plateau; reaches optimum around iteration 65 (per Table 5) |
| GWO | Steady descent; converges ≈ iteration 93 |
| FA | Converges ≈ iteration 70 to a low value, but very high runtime |
| PSO | Converges ≈ iteration 90; prone to local optima |
| GA | Converges in fewest iterations (≈56) to a moderate value |
| WOA | Slowest; needs ≈350 iterations, stepwise descent |
| SA | Converges ≈ iteration 130 to a higher (worse) value |

## Trend summary
Seven convergence curves. Most algorithms drop steeply in the first ~50-100 iterations; WOA is the visible outlier with a long, stepwise gray staircase requiring ~350 iterations. CDGWO's curve reaches the lowest final fitness of the set. The figure should be read together with Table 5, which holds the precise fitness, runtime, iteration-count, and variance numbers; per-iteration values here are not reliably readable.
