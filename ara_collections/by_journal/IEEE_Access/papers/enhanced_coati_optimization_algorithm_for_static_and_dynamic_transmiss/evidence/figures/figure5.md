# Figure 5: Convergence curves and boxplot graphs of FDBCOA1 and its three variants with OBL for CEC2020 (P=50, Dim=20)

- **Source**: Figure 5, §III-C (p.35089)
- **Caption**: "The convergence curves and boxplot graphs of FDBCOA1 algorithm and its three variants with OBL for CEC 2020 benchmark problems (P = 50, Dim = 20)."
- **Screenshot**: figure5.png (top of page; 4 columns × 2 rows)
- **Figure type**: quantitative_plot (mixed: convergence + boxplots)
- **Extraction method**: visual_description
- **Reading confidence**: low (log axes, dense markers)
- **Plot kind**: line (function-error vs fitness evaluations) + box (best fitness)

## Panels
Columns: F1 (Unimodal), F3 (Basic), F6 (Hybrid), F8 (Composition). Series: FDBCOA1 (black), FDBCOA1-OBL1 (blue), FDBCOA1-OBL5 (red), FDBCOA1-OBL7 (green).

## Trend summary
Top row: the OBL-seeded variants settle below the FDBCOA1-without-OBL baseline (black); FDBCOA1-OBL5 (red) reaches the lowest error band. Bottom boxplots: OBL5 (red) has the lowest/tightest box in F1, F3, F6, F8. Confirms OBL seeding improves over FDBCOA1 and OBL5 is best. Supports C03.
