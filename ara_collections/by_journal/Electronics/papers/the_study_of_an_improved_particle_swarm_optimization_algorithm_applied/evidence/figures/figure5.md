# Figure 5: Test results of each benchmark function

- **Source**: Figure 5, Section 4.2.5 (page 12, lower multi-panel figure)
- **Caption**: "Test results of each benchmark function."
- **Screenshot**: figure5.png
- **Figure type**: quantitative_plot (multi-panel; five panels, one per benchmark)
- **Extraction method**: digitized_estimate
- **Reading confidence**: low
- **Plot kind**: line (convergence curves)
- **Axes** (each panel): X = Iterations, range 0-2000, linear; Y = Optimum (objective value), range 0-50, linear

| Panel (function) | Approx. iterations to reach the near-0 acceptance band |
|------------------|--------------------------------------------------------|
| Sum of Different | ≈400 (drops steeply from ≈45, small bounce near 400, then flat ≈0) |
| Schwefel | ≈300-400 |
| Rastrigin | ≈400-500 (with a small transient bump before settling) |
| Rosenbrock | ≈400-500 |
| Levy | ≈300-400 |

## Trend summary
For all five benchmark functions the SCMPSO objective starts high (≈40-50) and collapses to the near-zero acceptance band (0.01, per Table 3) within roughly the first 300-500 iterations, then stays flat through 2000. The panels demonstrate fast convergence and successful escape from local optima across unimodal (Sum of Different Powers, Rosenbrock) and multimodal (Rastrigin, Schwefel, Levy) landscapes. Exact per-iteration values are not readable at this resolution; only the "rapid early collapse, then flat" shape is reliable. Panels are individual sub-plots of one figure and are described jointly, not fabricated into a numeric table.
