# Figure 11: Voltage fluctuation statistics of isolated island under different scenarios

**Source**: Figure 11, Section 5.2, page 18
**Location on page**: top-middle of page 18
**Caption**: "Voltage fluctuation statistics of isolated island under different scenarios."
**Screenshot**: figure11.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels (range from text) + digitized_estimate (box positions)
**Reading confidence**: medium
**Plot kind**: box (box-and-whisker per node)
**Axes**: X = Node (2, 3, 4, 5, 6, 7, 22, 23, 24, 25, 26), Y = Voltage (pu, linear, 1.08-1.1)

Legend: "+" desired value, red line = mid value, blue box = 25%-75%, black whisker = 9%-91%, circle = other.

| Node (visual median, pu) | Reading |
|--------------------------|---------|
| 2 | ≈1.0875 |
| 3 | ≈1.0863 (inset: box ≈1.084-1.086, median ≈1.0855) |
| 4 | ≈1.0855 |
| 5 | ≈1.0842 |
| 6 | ≈1.0838 |
| 7 | ≈1.083 |
| 22 | ≈1.089 |
| 23 | ≈1.0925 |
| 24 | ≈1.1 (highest, DG3 node) |
| 25 | ≈1.0842 |
| 26 | ≈1.0842 |

## Trend summary
20 random wind-power scenarios; box plots show voltage spread per node. Across ALL 20 scenarios every
node voltage lies within [1.08, 1.1] pu — no limit violation (text). Node 24 (diesel DG3) sits at the
top ≈1.1 pu; downstream nodes (5,6,7) are lowest ≈1.083 pu. Boxes are narrow (small
scenario-to-scenario dispersion), evidencing robustness of the islanding strategy to wind uncertainty.
Values ≈ approximate except the [1.08, 1.1] envelope which is stated in text.
