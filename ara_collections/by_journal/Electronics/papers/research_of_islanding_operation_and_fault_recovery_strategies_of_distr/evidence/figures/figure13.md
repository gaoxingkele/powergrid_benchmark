# Figure 13: Voltage of Island 1 at different time periods when the initial energy storage capacity is 80%

**Source**: Figure 13, Section 5.2 / 5.3, page 19
**Location on page**: top of page 19 (3-panel: (a) stereogram, (b) vertical view, (c) front view)
**Caption**: "Voltage of Island 1 at different time periods when the initial energy storage capacity is 80%."
**Screenshot**: figure13.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels (max from text) + digitized_estimate (per-bar)
**Reading confidence**: medium
**Plot kind**: bar (3D bar chart + 2D views)
**Axes**: X = Time period (Period1-5), Y = Node (10,11,12,13,14,15,16,17,29,30,31,32), Z = Voltage (pu, linear, 1.075-1.095)

| Period | Total load (MW) | Line loss (kW) |
|--------|-----------------|----------------|
| 1 | 2.08 | 4.51 |
| 2 | 1.98 | 4.44 |
| 3 | 2.08 | 4.52 |
| 4 | 2.21 | 4.55 |
| 5 | 1.83 | 4.52 |

Maximum node voltage over 5 periods = 1.094 pu (text); no voltage-limit violation.

## Trend summary
Same Island 1, but initial storage SOC = 80% of rated. Loads differ from the 50% case
(2.08/1.98/2.08/2.21/1.83 MW) because more stored energy lets the schedule serve more load early; line
losses ≈4.4-4.55 kW. Max voltage 1.094 pu, within limits. Together with Figure 12 this shows the
islanding/operation strategy is applicable across different initial storage capacities.
