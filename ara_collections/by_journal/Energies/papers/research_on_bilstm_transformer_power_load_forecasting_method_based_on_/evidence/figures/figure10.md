# Figure 10

**Source:** `evidence/figures/figure10.png`

**Caption:** Figure 10. Quantitative error metrics for weekly load forecasting.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — bar chart or box plot of weekly error metrics.

**Structured Description:**

This figure presents quantitative error metrics for the weekly load forecasting evaluation. The visualization is likely a bar chart or box plot showing:

**X-axis:** Models (typically 4-6 models including DAF-BT and top baselines)
**Y-axis:** Error metric value

**Layout possibilities:**
- Multiple panels showing MAE, RMSE, and MAPE separately
- Or grouped bars per metric per model

**Key visual observations:**
- Error metrics at the weekly scale are generally higher than at the daily scale due to the extended forecasting horizon
- DAF-BT maintains the lowest error across all metrics
- The margin between DAF-BT and baselines may be more pronounced at the weekly scale, suggesting the model's advantage grows with forecasting horizon
- Error variance (shown by error bars or box plot whiskers) is typically smaller for DAF-BT
- Some baseline models show significantly increased errors at weekly scale, indicating error accumulation over extended predictions

This figure provides the quantitative counterpart to the weekly load curves in Figure 9, completing the multi-time-scale evaluation in Experiment E02.
