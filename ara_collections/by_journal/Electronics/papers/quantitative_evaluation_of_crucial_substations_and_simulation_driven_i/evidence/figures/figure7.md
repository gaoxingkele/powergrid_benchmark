# Figure 7: Scatter and fitting plot of substation importance scores and grid incremental costs

- **Source**: Figure 7, §4.4 (p. 18)
- **Caption**: "Scatter and fitting plot of substation importance scores and grid incremental costs."
- **Screenshot**: figure7.png (rendered from PDF page 18)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate (y-values exact from Table 7; x-positions read off the axis)
- **Reading confidence**: medium

- **Plot kind**: scatter (panel a) + scatter with fitted line (panel b)
- **Axes**: X = "substation score", dimensionless, linear, 0–~0.09 (ticks 0, 0.02, 0.04, 0.06, 0.08); Y = "incremental cost", %, linear, 0–5% (ticks every 1%)

Six points, one per deferred substation. The y-values match Table 7 exactly; x read from the plot:

| Substation | X (plotted score) | Y (incremental cost) |
|---|---|---|
| 6 | ≈0.055 | 1.63% |
| 3 | ≈0.058 | 1.46% |
| 2 | ≈0.062 | 2.43% |
| 4 | ≈0.068 | 2.61% |
| 5 | ≈0.076 | 4.24% |
| 1 | ≈0.081 | 3.95% |

**Axis-scale note**: the plotted x-values (≈0.055–0.081) are NOT the Table 5/Table 7 scores (0.1367–0.2035); they are consistent with those scores multiplied by ≈0.4 (a rescaling not explained in the paper). The ordering of substations along x is identical to the Table 5 score ranking, so the correlation reading is unaffected.

- **Panel (a)**: raw scatter (red circles).
- **Panel (b)**: same points (blue circles) with a solid positively-sloped fitted regression line; dashed vertical segments mark each point's residual distance to the fit. Text (§4.4) states linear regression "reveals a significant linear relationship"; no R², slope, or p-value is printed — Not specified in paper.

## Trend summary
Strongly positive, approximately linear relationship: incremental cost rises from ≈1.5% at the lowest scores to ≈4% at the highest. Local non-monotonicity at the top (No. 5 at 4.24% exceeds top-scored No. 1 at 3.95%) and bottom (No. 6 at 1.63% exceeds No. 3 at 1.46%); residuals around the fit are small. Primary visual evidence for C02 (and, via the gradient, C03). Produced by E05.
