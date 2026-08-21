# Figure 5: GA convergence curve for power loss

- **Source**: Figure 5, Section 6 (Results), page 10
- **Caption**: "GA convergence curve for power loss."
- **Screenshot**: figure5.png (plot in the lower half of page 10)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = GA generation (count, linear, 0–100), Y = power losses (kW, linear, ticks at 28/33/38/43/48/53)

No data labels are printed on the curve; the values below are read off the gridlines and marked ≈.
The exact endpoint loss values live in Table 4 (base 55.3 kW, optimized 29.7 kW).

| GA generation | Power losses (kW) |
|---------------|-------------------|
| 0   | ≈52 |
| 10  | ≈42 |
| 20  | ≈38 |
| 40  | ≈35 |
| 60  | ≈33 |
| 80  | ≈31 |
| 100 | ≈29 |

## Trend summary
Monotonically decreasing convergence curve: a steep drop over the first ~20 generations (≈52 → ≈38
kW) followed by a slow, smooth decline toward ≈29 kW by generation 100. The shape is a single-elbow
convergence with no oscillation or premature plateau, consistent with the paper's claim of a
"consistent and smooth decline." The plotted starting value (≈52 kW at gen 0) is a digitized read
and is slightly below the Table 4 base-case figure of 55.3 kW; the final value (≈29 kW) matches the
Table 4 optimized figure of 29.7 kW within reading error.
