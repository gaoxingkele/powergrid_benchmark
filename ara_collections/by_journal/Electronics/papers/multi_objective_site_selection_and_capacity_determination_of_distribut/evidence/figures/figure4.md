# Figure 4: Wind power output reduction scenarios

- **Source**: Figure 4, Section 5 (Case Analysis), page 7
- **Caption**: "Wind power output reduction scenarios." (in-plot title: "Wind power uncertainty output")
- **Screenshot**: figure4.png (upper plot on page 7)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate (curve values read off axes; only the scenario probabilities in the legend are exact)
- **Reading confidence**: medium

- **Plot kind**: line (5 reduced scenarios over 24 hours)
- **Axes**: X = Time /t (hours), 0–25, linear; Y = Power /kW, 0.5–1.5, linear
- **Legend (exact scenario probabilities from labels)**: Scenario 1 (0.214), Scenario 2 (0.196), Scenario 3 (0.222), Scenario 4 (0.198), Scenario 5 (0.17). These are the reduced-scenario probability weights (sum ≈ 1.0), derived from reducing 500 generated wind–solar scenarios.

| Feature | Reading |
|---------|---------|
| Value band across all scenarios | ≈0.53 (trough near t≈21) to ≈1.49 (peak near t≈13, Scenario 4) |
| Approx. mean level | ≈1.0–1.1 kW, fluctuating hour to hour |
| Scenario 2 (red) | consistently the lowest envelope (≈0.67–1.28) |
| Scenario 4 (purple) | reaches the highest peaks (≈1.45–1.49 around t≈11–13) |

## Trend summary
Wind output is highly volatile hour-to-hour with no smooth diurnal shape; the five reduced scenarios preserve a spread/envelope (Scenario 2 low, Scenario 4 high) rather than collapsing to one mean curve, illustrating that the copula-based reduction retains randomness across scenarios. Deep troughs near t≈6, t≈10, and t≈21 are shared across scenarios (correlated structure).
