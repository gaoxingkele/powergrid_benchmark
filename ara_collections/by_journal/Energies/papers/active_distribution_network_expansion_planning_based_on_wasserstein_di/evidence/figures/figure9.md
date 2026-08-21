# Figure 9: Maximum relative error chart

- **Source**: Figure 9, Section 5.5 (Validity Analysis of Distributionally Robust Optimization Method)
- **Caption**: "Maximum relative error chart."
- **Screenshot**: figure9.png
- **Figure type**: quantitative_plot
- **Extraction method**: numerical_report
- **Reading confidence**: medium (values estimated from trend description)

## Visual description
- **Components**: Line chart showing the maximum relative error of the Wasserstein-distance-based distributionally robust optimization method as a function of the Wasserstein distance radius parameter (epsilon).
- **Axes**:
  - X-axis: Wasserstein distance radius epsilon (the size of the ambiguity set).
  - Y-axis: Maximum relative error (%) between the DRO solution and the true (out-of-sample) optimal.
- **Trend** (estimated):
  - At epsilon = 0 (no ambiguity, equivalent to deterministic optimization), the relative error is highest because the model is overconfident in the empirical distribution.
  - As epsilon increases, the model becomes more conservative and the relative error decreases monotonically.
  - Beyond a certain epsilon threshold, the relative error stabilizes at a low plateau, indicating that the ambiguity set adequately covers the true distribution.
- **What it conveys**: The Wasserstein radius epsilon controls the trade-off between conservativeness and out-of-sample performance. An appropriately chosen epsilon yields a DRO solution that is robust to distributional ambiguity while maintaining competitive out-of-sample performance. The chart demonstrates that the Wasserstein ambiguity set effectively hedges against distributional uncertainty without excessive conservatism.

Supporting context from Table 6: The distributionally robust method achieves net profit 4928.18 x 10^4 CNY/year, which is between the deterministic (5089.49, "too ideal") and robust (4770.01, "too conservative") extremes, and is improved by "more than 3%" vs the traditional robust method.
