# Figure 9: Hourly specific load prediction

- **Source**: Figure 9, §5.2 (p.14)
- **Caption**: "Hourly specific load prediction."
- **Screenshot**: figure9.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Location on page**: upper-middle of the page (below Table 4).
- **Plot kind**: line (overlay of 5 series)
- **Axes**: X = "Sampling Points (sampling interval 1h)" (linear, ≈1 to ≈165), Y = "Electricity
  consumption (kW·h)" (linear, 2 to 14)
- **Series (legend)**: Actual-Load, LSTM, RNN, EMD-LSTM, CEEMDAN-LSTM

| Feature | Reading |
|---------|---------|
| Baseline load region | ≈3.5–4.5 kW·h |
| Peak events | ≈8–10 kW·h at clustered peaks (e.g. near x≈15, ≈35, ≈110, ≈135, ≈160) |
| Highest actual peak | ≈13 kW·h near x≈135 |
| Y-axis span | 2 to 14 kW·h |

## Trend summary
All five traces track the same spiky hourly pattern; they agree closely in the low-load valleys and
diverge most at the sharp peaks, where the baselines (especially RNN, cyan) over/undershoot. The
CEEMDAN-LSTM trace (black) follows the Actual-Load (red) peaks more tightly than the other models,
consistent with its lowest RMSE/MAE in Table 3. Values estimated (≈); the readable, robust fact is
the relative peak-tracking quality, not exact points. Supports C03.
