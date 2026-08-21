# Figure 12: Voltage of Island 1 at different time periods when the initial energy storage capacity is 50%

**Source**: Figure 12, Section 5.2, page 18
**Location on page**: bottom of page 18 (3-panel: (a) stereogram, (b) vertical view, (c) front view)
**Caption**: "Voltage of Island 1 at different time periods when the initial energy storage capacity is 50%."
**Screenshot**: figure12.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels (max from text) + digitized_estimate (per-bar)
**Reading confidence**: medium
**Plot kind**: bar (3D bar chart + 2D views)
**Axes**: X = Time period (Period1-5), Y = Node (10,11,12,13,14,15,16,17,29,30,31,32), Z = Voltage (pu, linear, 1.075-1.095)

| Period | Total load (MW) | Line loss (kW) |
|--------|-----------------|----------------|
| 1 | 1.84 | 4.51 |
| 2 | 1.90 | 4.43 |
| 3 | 1.96 | 4.55 |
| 4 | 2.02 | 4.62 |
| 5 | 2.08 | 4.31 |

Maximum node voltage over 5 periods = 1.093 pu (text); no voltage-limit violation.

## Trend summary
Island 1 (contains DG2 energy storage at node 13 and DG4 diesel at node 31), initial storage SOC =
50% of rated. Load rises monotonically 1.84->2.08 MW across periods; line losses stay ≈4.3-4.6 kW
(≈0.22-0.26% of load). All node voltages remain below 1.093 pu and within limits. Demonstrates the
strategy holds voltages with a half-charged battery.
