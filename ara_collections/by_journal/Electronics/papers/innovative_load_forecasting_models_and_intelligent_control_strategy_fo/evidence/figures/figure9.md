# Figure 9: Comparative performance

- **Source**: Figure 9, §4.2(c) (page 17, bottom)
- **Caption**: "Comparative performance."
- **Screenshot**: figure9.png
- **Figure type**: quantitative_plot (four panels)
- **Extraction method**: visual_description (trend) + digitized_estimate (ranges)
- **Reading confidence**: medium
- **Plot kind**: line (predictions vs actual time series)

## Panels and axes
Four subplots, each: X = time index (samples, linear), Y = Energy Consumption (MWh, linear). Three overlaid series per panel: "GRU Predictions" (green), "LSTM Predictions" (red), "Actual" (blue).

| Panel | Dataset | Approx Y range (MWh) |
|-------|---------|----------------------|
| Top-left | COMED_hourly.csv | ≈9,000–17,000 |
| Top-right | EKPC_hourly.csv | ≈1,000–1,850 |
| Bottom-left | NI_hourly.csv | ≈7,500–12,000 |
| Bottom-right | PJM_Load_hourly.csv | ≈24,000–46,000 |

## Trend summary
In all four panels the GRU and LSTM prediction curves track the Actual curve closely through the oscillating (roughly diurnal) load pattern, with the two model predictions nearly overlapping each other and only small deviations from Actual at peaks/troughs. Demonstrates that both models reproduce the temporal load shape across datasets of very different magnitude (hundreds to tens of thousands of MWh). Supports C01 (both models capture temporal structure) and C02 (LSTM≈GRU). Note these panels use datasets beyond the five tabulated (EKPC, NI, PJM_Load), so no per-dataset error numbers accompany them.
