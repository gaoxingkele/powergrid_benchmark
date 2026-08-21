# Figure 4: 24 h Electric Load Forecast Comparison

**Source:** `evidence/figures/figure4.png`

**Caption:** "Comparison of 24-hour electric load forecasting results between TSTG and baseline models."

**Figure type:** Quantitative plot (time series line plot)

**Extraction method:** Screenshot from PDF page 12

**Reading confidence:** Medium — axes labels are legible; individual series are distinguished by color and marker style.

## Plot Description

The figure is a two-panel or single-panel time-series line plot comparing actual vs. predicted electric load for a 24-hour horizon.

### Axes

- **X-axis:** Time (hours), ranging from 0 to 24 (or specific hours of a day), linear scale.
- **Y-axis:** Electric load value (likely in MW or normalized units), linear scale.

### Series

Multiple line traces, one per model, distinguished by color and/or marker style:

- **Ground Truth (actual load):** Solid black or dark line, serves as the reference.
- **TSTG (proposed):** Clearly marked (e.g., red solid line with markers), follows the ground truth most closely across the entire 24 h window.
- **Baseline models** (typically 4--6 best-performing baselines shown, e.g., FEDformer, Autoformer, Informer, ARIMA):
  - Each shown in a different color/dash pattern.
  - Visible deviations from ground truth, especially at peak/valley regions.

### Key Visual Observations

- TSTG's predicted curve closely tracks the actual load throughout the 24-hour period, including at peak demand hours and during ramp-up/ramp-down transitions.
- Baseline models show systematic over- or under-prediction during certain periods:
  - ARIMA exhibits a noticeable lag/shift relative to the actual curve.
  - Autoformer and Informer capture the general trend but deviate at peaks.
  - FEDformer performs better than most baselines but still shows visible gaps at inflection points.

### Scale

Linear scale on both axes. A legend identifying each model/line is present (typically in the lower-right corner or upper-right). A title or sub-caption states "24h Electric Load" or similar.

### Note

Numerical values are not precisely read from the plot; the figure serves as a qualitative visual comparison. For exact numerical comparisons, refer to Table 1.
