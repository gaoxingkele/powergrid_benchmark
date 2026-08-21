# Figure 4: Voltage Profile Comparison

- **Source**: Figure 4, Section 6 (Results), page 9
- **Caption**: "Voltage Profile Comparison."
- **Screenshot**: figure4.png (plot in the lower half of page 9)
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high
- **Plot kind**: line
- **Axes**: X = Bus (bus index 1–6, linear), Y = Voltage (pu, linear, gridlines at 0.92/0.94/0.96/0.98/1.00)

Values below are the exact numbers printed in the companion Table 3 (the plot renders the same data;
no data labels are drawn on the plot itself, but the underlying values are stated exactly in Table 3).

| Bus | Voltage (pu) (Base Case) | Voltage (pu) (Optimized GA) |
|-----|--------------------------|------------------------------|
| 1   | 1.00 | 1.00 |
| 2   | 0.97 | 1.01 |
| 3   | 0.95 | 1.00 |
| 4   | 0.94 | 0.99 |
| 5   | 0.93 | 0.98 |
| 6   | 0.92 | 0.97 |

## Trend summary
Base case (solid black) declines monotonically from 1.00 pu at the substation (bus 1) to 0.92 pu at
the farthest bus (bus 6), sitting exactly at the 0.95 pu limit at bus 3 and dropping below it from
bus 4 onward (0.94/0.93/0.92). Optimized GA (dashed
grey) is at or above the base case at every bus, peaks slightly above nominal at bus 2 (1.01), and
stays within the 0.95–1.05 band across all buses, ending at 0.97 pu at bus 6. The two curves diverge
progressively downstream — the GA benefit grows with electrical distance from the substation.
