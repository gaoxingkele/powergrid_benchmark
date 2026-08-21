# Figure 9: Prediction results of the power data set of Tétouan City

- **Source**: Figure 9, Section 4, p12
- **Caption**: "Prediction results obtained of the power data set of Tétouan City."
- **Screenshot**: figure9.png (page 12; upper plot on the page)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = Time (10 min intervals, linear, 0–150), Y = Load (kW, linear, 23,000–46,000)

| Time (10min) | Actual (kW) | LSTM/CNN-LSTM/TCN/LSTM-CNN |
|--------------|-------------|----------------------------|
| 0    | ≈31,000 | all clustered ≈30,500–31,000 |
| ~20  | ≈27,000 (trough) | baselines slightly above/below actual |
| ~42  | ≈24,500 (sharp dip) | Actual dips lowest; baselines overshoot (predict higher) |
| ~70  | ≈36,800 (local peak) | closely tracked by all |
| ~118 | ≈46,000 (global peak) | Actual peaks highest; LSTM-CNN (red) closest |
| ~145 | ≈32,000 | converge |

## Trend summary
All five curves (Actual + LSTM, CNN-LSTM, TCN, LSTM-CNN) follow the same daily shape: trough near
x≈20–42, rise to a plateau ≈36,800 near x≈70, then a global peak ≈46,000 near x≈115–120, then
decline. The three-channel model (legend "LSTM-CNN", red) tracks the Actual (blue) most closely,
especially at the sharp dip near x≈42 and the global peak, where the other baselines overshoot the
actual value. Exact per-point values are estimates read against gridlines. Supports C01, C06 (E04);
exact metric values are in evidence/tables/table4.md.
</content>
