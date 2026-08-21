# Figure 8

**Source:** `evidence/figures/figure8.png`

**Caption:** Figure 8. Quantitative error metrics for daily load forecasting.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — bar chart or box plot of daily error metrics.

**Structured Description:**

This figure presents quantitative error metrics for the daily load forecasting evaluation across models. The visualization is likely a grouped bar chart or box plot showing:

**X-axis:** Models (subset of 4-6 models including DAF-BT)
**Y-axis:** Error metric value (MAE, RMSE, or MAPE)

**Layout possibilities:**
- Multiple panels, one per error metric (MAE, RMSE, MAPE)
- Or grouped bars within a single panel

**Key visual observations:**
- DAF-BT consistently shows the lowest error bars across all metrics
- The error distribution for DAF-BT is narrower (lower variance) than baselines
- The relative ordering of models matches the overall benchmark results (Table 2)
- Daily-level errors may be slightly higher than the overall average if specific challenging days are included

This figure provides the quantitative counterpart to the qualitative daily load curves in Figure 7, supporting the daily scale analysis in Experiment E02.
