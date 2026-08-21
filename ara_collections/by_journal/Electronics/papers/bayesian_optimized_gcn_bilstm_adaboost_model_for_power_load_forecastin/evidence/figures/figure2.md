# Figure 2: Spearman correlation coefficient between features

- **Source**: Figure 2, §2.2 (page 5, lower half of page)
- **Caption**: "Spearman correlation coefficient between features."
- **Screenshot**: figure2.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high
- **Plot kind**: heatmap
- **Axes**: X = feature (categorical), Y = feature (categorical); cell = Spearman correlation
  (colorbar 0.2–1.0). Values are printed in each cell (exact).

Rows/cols order: Load, Humidity, Temperature, Wind Speed, Pressure, Precipitation, Visibility,
Water Vapor, Apparent Temperature.

| feature | Load | Humid | Temp | Wind | Press | Precip | Vis | Vapor | ApTemp |
|---------|------|-------|------|------|-------|--------|-----|-------|--------|
| Load | 1.00 | 0.10 | 0.32 | 0.05 | 0.23 | 0.01 | 0.05 | 0.34 | 0.34 |
| Humidity | 0.10 | 1.00 | 0.05 | 0.33 | 0.22 | 0.32 | 0.49 | 0.48 | 0.13 |
| Temperature | 0.32 | 0.05 | 1.00 | 0.20 | 0.86 | 0.04 | 0.29 | 0.89 | 0.99 |
| Wind Speed | 0.05 | 0.33 | 0.20 | 1.00 | 1.17 | 0.03 | 0.40 | 0.03 | 0.13 |
| Pressure | 0.23 | 0.22 | 0.86 | 1.17 | 1.00 | 0.12 | 0.20 | 0.85 | 0.87 |
| Precipitation | 0.01 | 0.32 | 0.04 | 0.03 | 0.12 | 1.00 | 0.14 | 0.16 | 0.06 |
| Visibility | 0.05 | 0.49 | 0.29 | 0.40 | 0.20 | 0.14 | 1.00 | 0.04 | 0.24 |
| Water Vapor | 0.34 | 0.48 | 0.89 | 0.03 | 0.85 | 0.16 | 0.04 | 1.00 | 0.92 |
| Apparent Temp | 0.34 | 0.13 | 0.99 | 0.13 | 0.87 | 0.06 | 0.24 | 0.92 | 1.00 |

## Trend summary
Strong (|ρ| ≥ 0.8) pairs — which become GCN edges — cluster among the thermodynamically related
variables: Temperature–Pressure (0.86), Temperature–Water Vapor (0.89), Temperature–Apparent Temp
(0.99), Pressure–Water Vapor (0.85), Pressure–Apparent Temp (0.87), Water Vapor–Apparent Temp (0.92),
and Wind Speed–Pressure (1.17). Load correlates weakly (≤0.34) with every weather feature, so Load is
not connected under the ≥0.8 rule. **Anomaly**: the Wind Speed–Pressure cell reads 1.17, which exceeds
the valid [−1, 1] range for a correlation coefficient (printed symmetrically in both off-diagonal
cells); noted as a data/computation error in constraints.md.
