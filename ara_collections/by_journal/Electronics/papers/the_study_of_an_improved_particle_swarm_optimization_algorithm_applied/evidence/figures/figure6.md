# Figure 6: Iteration comparison of different Particle Swarm Optimization algorithms

- **Source**: Figure 6, Section 4.2.5 (page 13, upper figure)
- **Caption**: "Iteration comparison of different Particle Swarm Optimization algorithms."
- **Screenshot**: figure6.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line (four convergence curves + zoom inset)
- **Axes**: X = Iterations, range 0-2000, linear; Y = Optimum (objective value), range 0-50, linear. Inset zoom (iterations 1500-2000): Y range ≈0-0.7.

| Iterations | SCMPSO (red solid) | CPSO (blue dash-dot) | QPSO (purple dashed) | PSO (black dash-dot) |
|------------|--------------------|-----------------------|-----------------------|-----------------------|
| 0    | ≈45-50 | ≈45-50 | ≈45-50 | ≈45-50 |
| 500  | ≈0-1 (first to bottom) | ≈2-5 | ≈2-5 | ≈5-10 |
| 1000 | ≈0 | ≈0.3 | ≈0.3 | ≈0.5 |
| 2000 (inset) | ≈0.1 (lowest, flat) | ≈0.3 | descending ≈0.4->0.3 | ≈0.4-0.3 |

## Trend summary
All four PSO variants collapse from ≈45-50 toward ≈0; SCMPSO descends fastest and settles to the lowest final band. The zoom inset over iterations 1500-2000 shows the final ordering SCMPSO (≈0.1, flat) < CPSO (≈0.3) < QPSO ~ PSO (≈0.3-0.4, still gently descending). The text states all four "tend to approach 0" by ≈500 iterations, motivating a minimum iteration budget of 500 and the paper's choice of 2000 as the standard. Ordering (SCMPSO best) is reliable; exact final values are estimates.
