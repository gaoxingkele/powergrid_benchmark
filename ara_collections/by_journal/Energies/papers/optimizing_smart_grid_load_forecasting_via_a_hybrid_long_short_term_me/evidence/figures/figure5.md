# Figure 5: Box Plot of Load by Date

- **Source**: Figure 4 (in-text reference in Section 3.1, p.6)
- **Caption**: Not independently captioned — referenced as a box plot showing load distribution by date.
- **Screenshot**: figure5.png
- **Figure type**: box plot (vertical, grouped by date)
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A collection of vertical box plots, one per date (or per grouped date interval) across the 2022 Elia Grid Load dataset, showing distribution statistics of 15-min load values within each day.

**Axes**:
- X-axis: Date (January 2022 through December 2022; each tick may represent a single day or a grouped interval).
- Y-axis: Load (MW), ranging from ~0 MW to ~14,000 MW.

**Key visual features**:
- Each box shows the **median** (center line), **interquartile range** (IQR, box bounds at Q1 and Q3), and **whiskers** (typically 1.5x IQR or min/max within range).
- **Outlier points** (dots beyond whiskers) are visible at many dates, especially as low outliers (near 0 MW) and occasional high outliers (spikes above the upper whisker).
- The median load exhibits the same U-shaped seasonal trend: higher medians in winter (~8,000–10,000 MW), lower medians in summer (~5,000–7,000 MW).
- Box widths (IQR spread) appear larger in winter months than summer months, suggesting higher intra-day variance during high-demand periods.
- The low-outlier cluster around ~0 MW is visible across many dates, confirming a systematic data artifact.

**What it conveys**: The box plots demonstrate high day-to-day variability, presence of outliers in nearly every date, and seasonal patterns in both central tendency and spread — all of which the paper argues make the 15-min resolution forecasting problem harder than coarser-resolution tasks.

**Relevant claims/observations**: Supports O3 (load has spikes, non-stationarity, outliers) and C03 (residual-refinement stacking helps most in volatile/spike-heavy regimes).
