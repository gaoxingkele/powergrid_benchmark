# Figure 10: Grid resilience performance comparison

- **Source**: Figure 10, §4.3 (page 18, top)
- **Caption**: "Grid resilience performance comparison." (in-plot title: "Grid Resilience Scores for LSTM and GRU Models")
- **Screenshot**: figure10.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line (marker) — score per dataset, two series
- **Axes**: X = Dataset (categorical: AEP_hourly, COMED_hourly, DAYTON_hourly, DEOK_hourly, DOM_hourly), Y = Score (dimensionless, linear, ~0.74–0.86)

| Dataset | LSTM (blue) | GRU (orange) |
|---------|-------------|--------------|
| AEP_hourly.csv | ≈0.78 | ≈0.75 |
| COMED_hourly.csv | ≈0.81 | ≈0.78 |
| DAYTON_hourly.csv | ≈0.85 | ≈0.82 |
| DEOK_hourly.csv | ≈0.83 | ≈0.80 |
| DOM_hourly.csv | ≈0.80 | ≈0.77 |

## Trend summary
The LSTM series sits above the GRU series at every one of the five datasets; both peak at DAYTON and are lowest at AEP/DOM. Critically, this ranks LSTM above GRU on "grid resilience," the opposite of the forecasting-error ranking (Table 6, where GRU has lower MSE/MAPE everywhere) — the basis for C05. The resilience-score construction is not defined in the paper, so values are estimated off the axis and the metric is unverifiable. Reading confidence medium (clear gridlines, no data labels).
