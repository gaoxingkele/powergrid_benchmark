# Figure 10: Daily load prediction for a specific user

- **Source**: Figure 10, §5.2 (p.14)
- **Caption**: "Daily load prediction for a specific user."
- **Screenshot**: figure10.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Location on page**: lower-middle of the page.
- **Plot kind**: line (overlay of 5 series)
- **Axes**: X = "Sampling Points (sampling interval 1d)" (days, linear, ≈1 to 30), Y = "Electricity
  consumption (kW·h)" (linear, 60 to 150)
- **Series (legend)**: Actual-Load, LSTM, RNN, EMD-LSTM, CEEMDAN-LSTM

| Feature | Reading |
|---------|---------|
| Load range | ≈70–130 kW·h (daily totals) |
| Low troughs | ≈70–80 kW·h (e.g. near day ≈2, ≈11, ≈27) |
| High peaks | ≈120–130 kW·h (e.g. near day ≈7, ≈14, ≈20) |
| Test span | 30 days (the reserved test set) |

## Trend summary
The daily series is strongly periodic (repeated rise-and-fall cycles of a few days). All models
follow the cycles but the baselines overshoot/undershoot the turning points more; the CEEMDAN-LSTM
trace (black) stays closer to Actual-Load (red) at peaks and troughs, consistent with its lowest
RMSE/MAE in Table 4. Values estimated (≈); the robust reading is relative cycle-tracking fidelity.
Supports C03.
