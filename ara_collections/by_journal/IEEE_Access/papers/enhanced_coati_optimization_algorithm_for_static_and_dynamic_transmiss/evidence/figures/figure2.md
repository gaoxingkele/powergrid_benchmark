# Figure 2: Convergence curves and boxplot graphs of COA and its three variants with FDB for CEC2020 (P=50, Dim=10)

- **Source**: Figure 2, §III-B (p.35080)
- **Caption**: "The convergence curves and boxplot graphs of COA algorithm and its three variants with FDB for CEC 2020 benchmark problems (P = 50, Dim = 10)."
- **Screenshot**: figure2.png (top of page; 4 columns × 2 rows: convergence over F1/F3/F5/F8, boxplots below)
- **Figure type**: quantitative_plot (mixed: log-scale convergence curves + boxplots)
- **Extraction method**: visual_description
- **Reading confidence**: low (log y-axes, dense overlapping markers; exact values not readable)
- **Plot kind**: line (top row, function-error vs number of fitness evaluations, log-log) + box (bottom row, best fitness)

## Panels
Columns: F1 (Unimodal), F3 (Basic), F5 (Hybrid), F8 (Composition). Series: COA (black), FDBCOA1 (red), FDBCOA2 (blue), FDBCOA3 (green).

## Trend summary
Top row: all curves fall then plateau; the FDB variants (especially FDBCOA1, red) settle at lower function-error values than COA (black) — the red FDBCOA1 markers sit at the bottom band in F1, F3, F5, F8. Bottom row (box plots of best fitness over 51 cycles): FDBCOA1's box is lowest / tightest in F1, F3, F5, F8, with COA highest. Confirms FDB variants reduce error below COA and FDBCOA1 is best. Supports C01.
