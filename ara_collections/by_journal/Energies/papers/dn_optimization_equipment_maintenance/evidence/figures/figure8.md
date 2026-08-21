# Figure 8: Cost Comparison Among Different Optimization Models Under Typical Scenarios

**Source**: Page 14, Section 3.2, Figure 8
**Screenshot**: evidence/figures/figure8.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels
**Reading confidence**: high

## Subfigures

### (a) High Wind-Solar Generation and Peak Load
Cost comparison under the most challenging scenario: simultaneous high renewable generation and peak demand. The deterministic model shows the highest cost. The stochastic model shows moderate improvement. The robust model provides better worst-case protection. The proposed DRO model achieves the lowest cost.

### (b) Medium Wind-Solar Generation and Flat Load
Cost comparison under typical operating conditions. All models show lower absolute costs than in scenario (a). The relative ordering remains consistent, with the proposed DRO model showing the best performance.

### (c) Low Wind-Solar Generation and Valley Load
Cost comparison under low renewable output and minimal demand. This scenario has increased risk of flexibility deficits. The proposed DRO model maintains the lowest cost, demonstrating robustness across diverse operating conditions.

## Axes
- X-axis (each subfigure): Optimization model (deterministic, stochastic, robust, proposed)
- Y-axis (each subfigure): Total operating cost (CNY 10,000), linear scale

## Trend Summary
Across all three typical scenarios (high/medium/low renewable generation with corresponding load conditions), the proposed DRO model consistently achieves the lowest total operating cost. The deterministic model consistently shows the highest cost. The stochastic and robust models fall between the extremes, with the robust model showing less variance but higher average cost than stochastic.

**Note:** The paper reports: "Our model achieves an average cost reduction of 6.8% compared with traditional robust methods, and up to 14.5% compared with deterministic optimization." [Source: Page 14]
