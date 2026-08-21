# Figure 6: Comparison of convergence characteristic curves for four CGWO variants and traditional GWO

- **Source**: Figure 6, Section 4.2
- **Caption**: "Comparison of convergence characteristic curves for four CGWO variants and traditional GWO."
- **Screenshot**: figure6.png
- **Location on page**: Page 12 (PDF page 12), lower portion of the page.
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: low
- **Plot kind**: line
- **Axes**: X = Number of iterations (0-500, linear), Y = Fitness Value (×10^4, 0-5, linear)

| Series | Approx. start fitness (iter 0) | Approx. converged fitness | Note |
|---|---|---|---|
| GWO_Logistic | ≈4.5×10^4 | ≈0.17×10^4 | fastest early convergence (notably within first ~20 iters) |
| GWO_Chebyshev | ≈high | ≈0.17×10^4 | solution closest to actual optimum |
| GWO_Tent | ≈high | ≈low | suboptimal speed and precision |
| GWO_Sine | ≈high | ≈low | poorest / slowest early convergence |
| GWO (traditional) | ≈1×10^4 | ≈low | baseline, slower descent than Logistic/Chebyshev |

## Trend summary
All five curves collapse from a high initial fitness toward a low plateau within the first ~50-100 iterations, then flatten out to ~500 iterations. The paper's qualitative reading (Section 4.2) is the reliable signal: Sine is worst (slowest early convergence), Tent is suboptimal on both speed and precision, Chebyshev reaches the value closest to the true optimum, and Logistic converges fastest (acceleration concentrated in the first ~20 iterations). Exact per-iteration values are unreadable at this resolution; precise end values are tabulated in Table 4.
