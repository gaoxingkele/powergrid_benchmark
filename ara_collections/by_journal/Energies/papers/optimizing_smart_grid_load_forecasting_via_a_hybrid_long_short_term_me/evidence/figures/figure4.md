# Figure 4: Histogram of Load

- **Source**: Figure 3 (in-text reference in Section 3.1, p.6)
- **Caption**: Not independently captioned — referenced as a histogram of the load distribution.
- **Screenshot**: figure4.png
- **Figure type**: histogram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A histogram plot showing the distribution of Elia Grid Load values (MW) across all 15-min intervals in 2022.

**Axes**:
- X-axis: Load (MW), binned across the observed range (approximately 0 MW to ~14,000 MW).
- Y-axis: Frequency (count of intervals in each bin).

**Key visual features**:
- The distribution is **approximately normal / bell-shaped**, centered around ~8,000–9,000 MW.
- The peak (mode) falls in the range of ~7,000–9,000 MW, with tailing off on both sides.
- A left tail extends toward ~0 MW, corresponding to the low-outlier / near-zero data points seen in Figures 2 and 3.
- A right tail extends toward ~12,000–14,000 MW, corresponding to high-demand winter peak periods.
- The distribution appears slightly right-skewed (longer left tail due to the outlier cluster near 0 MW).

**What it conveys**: The approximately normal shape supports the authors' assumption (A1 in problem.md) that the load series is stationary / bell-shaped enough for model generalization, though the near-zero outlier cluster and the overall spread indicate non-ideal conditions at the extremes.

**Relevant claims/assumptions**: Supports Assumption A1 (load series approximately stationary / bell-shaped for model generalization).
