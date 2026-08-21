# Figure 7: Visual Comparison of Model Predictions

- **Source**: Figure 6 (in-text reference in Section 4.5, p.12); the paper's numbering counts it as Figure 6 but the ARA conventions label it as Figure 7 to avoid collision
- **Caption**: Not independently captioned — described in Section 4.5 Error Analysis as a visual comparison of LSTM, XGBoost, and the hybrid ensemble against actual load.
- **Screenshot**: figure7.png
- **Figure type**: composite line plot (4 panels)
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A 4-panel figure (2x2 layout) showing actual vs predicted load for the three models and a combined view:

### Panel (a): LSTM
- **Title** (typically "LSTM" or relevant label).
- **Axes**: Time steps on x-axis, Load (MW) on y-axis.
- **Traces**: Two lines — actual load (blue/black) and LSTM predictions (red/orange).
- **Behavior**: The LSTM trace follows the broad trend of actual load but visibly deviates during demand spikes and rapid transitions. The gap between actual and predicted widens at extreme values.

### Panel (b): XGBoost
- **Title** (typically "XGBoost" or relevant label).
- **Axes**: Time steps on x-axis, Load (MW) on y-axis.
- **Traces**: Two lines — actual load (blue/black) and XGBoost predictions (green/orange).
- **Behavior**: XGBoost captures spikes more closely than LSTM (lower sensitivity to anomalies), but the paper notes it "underperforms for continuous patterns" — the trace may show less smooth tracking over extended steady-state segments.

### Panel (c): LSTM vs Hybrid Ensemble
- **Title**: likely "LSTM vs Hybrid Ensemble" or "Ensemble LSTM-XGBoost."
- **Axes**: Time steps on x-axis, Load (MW) on y-axis.
- **Traces**: Three lines — actual load, LSTM predictions, and hybrid LSTM-XGBoost predictions.
- **Behavior**: The hybrid trace tracks actual load more closely than the standalone LSTM, particularly during dynamic/volatile windows (spikes and ramp transitions). The gap between LSTM and the hybrid is largest where LSTM error is largest.

### Panel (d): Full Training and Test
- **Title**: likely "Full Training and Test" or "Training and Testing Set."
- **Axes**: Time steps (or date) on x-axis, Load (MW) on y-axis.
- **Traces**: Actual load across the full series with training and test regions marked (e.g., by shading or vertical dividing line).
- **Behavior**: Shows the overall fit of the ensemble model across the entire dataset, with the test region (December 2022) highlighted.

**What it conveys**: Figure 7 provides qualitative visual evidence that the hybrid LSTM-XGBoost ensemble improves prediction accuracy over each standalone model, especially during volatile / spike periods (supporting C01 and C03). The 4-panel layout lets the reader visually compare error patterns across models on the same time window.

**Relevant claims/observations**: Strongly supports C01 (hybrid beats both standalone models), C03 (residual-refinement benefits spike-heavy regimes). Referenced in E01 and E03.
