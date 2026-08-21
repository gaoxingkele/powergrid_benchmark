# Figure 3: Scatter Plot of Load vs Datetime

- **Source**: Figure 2 (in-text reference in Section 3.1, p.6); note the paper refers to this as a scatter visualization of the raw load series
- **Caption**: Not independently captioned — referenced alongside Figure 2 as part of the exploratory data analysis.
- **Screenshot**: figure3.png
- **Figure type**: scatter plot
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A scatter plot with datetime on the x-axis and load (MW) on the y-axis, showing the full Elia Grid Load dataset for 2022.

**Axes**:
- X-axis: Datetime (January 2022 through December 2022).
- Y-axis: Load (MW), ranging from approximately 0 MW to approximately 14,000 MW.

**Key visual features**:
- The scatter points form a dense band that follows a **U-shaped seasonal trend**: load values are highest in January–February and November–December (winter peak ~10,000–14,000 MW), lowest in July–August (summer trough ~5,000–8,000 MW).
- A cluster of near-zero points (~0 MW) is visible at scattered dates — these are low outliers in the dataset (likely data recording artifacts).
- The vertical spread at any given date is wide, reflecting within-day variation (daily load profile of peak vs. off-peak hours).
- Seasonal transitions (spring: Mar–May; autumn: Sep–Oct) show intermediate load values and higher variance.

**What it conveys**: The U-shaped seasonal pattern confirms the presence of strong annual periodicity and non-stationarity in load. The wide vertical scatter at each date demonstrates high intra-day volatility, motivating models that can handle both trend and short-term fluctuations.

**Relevant observations**: Supports O3 (load has spikes, non-stationarity, randomness).
