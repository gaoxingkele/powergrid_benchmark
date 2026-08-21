# Figure 8: Impact of SOP and interconnection switch costs on planning results

- **Source**: Figure 8, Section 5.4 (Impact of SOP and Interconnection Switch Costs on Planning Results)
- **Caption**: "Impact of SOP and interconnection switch costs on planning results."
- **Screenshot**: figure8.png
- **Figure type**: quantitative_plot
- **Extraction method**: numerical_report
- **Reading confidence**: medium (exact axis values not independently verified; trend directions are clear)

## Visual description
- **Components**: Multi-line chart(s) showing how the annual net profit and optimal planning scheme change as the unit investment cost coefficients of SOPs and interconnection switches vary.
- **Axes**:
  - X-axis: Cost coefficient multiplier (e.g., 0.5x, 0.75x, 1.0x, 1.25x, 1.5x of nominal unit cost).
  - Y-axis: Annual net profit (CNY 10^4/year) and/or total investment.
- **Series** (estimated):
  - A curve showing net profit decreasing as SOP cost increases (since higher SOP investment reduces economic viability).
  - A curve showing net profit decreasing as interconnection switch cost increases.
  - A crossover point where cheaper switches become more economical than SOPs.
- **What it conveys**: Sensitivity of the planning outcome to device cost assumptions. As SOP costs decrease, the model installs more SOP capacity and achieves higher net profit. As interconnection switch costs increase, the model may substitute switches with SOPs. The analysis demonstrates that the optimal collaborative planning configuration is sensitive to the relative cost of the two interconnection technologies, and identifies the cost threshold ranges where one technology dominates the other.

Supporting context from Section 5.4: The paper reports that when the SOP investment cost drops below a certain threshold, the model prefers SOPs over switches everywhere; conversely, when switch cost rises, SOPs become more attractive. This sensitivity quantifies the robustness of the Case 1 planning result.
