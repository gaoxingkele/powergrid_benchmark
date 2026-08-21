# Figure 7: Convergence trajectory — extreme-point subdifferential vs. subgradient method

- **Source**: Figure 7, Section 4.2 (extreme-point subdifferential approach), page 14
- **Caption**: "Convergence trajectory of (a) extreme-point subdifferential method vs. the convergence trajectory of (b) subgradient method [17], where ρ1 and ρ2 are the price vectors in the Lagragian dual function space."
- **Screenshot**: figure7.png (upper two panels on PDF page 14)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium

- **Plot kind**: line (iterate trajectory over contour/level sets of the dual function in 2-D price space)
- **Axes**: X = ρ1 (price vector component, dimensionless, scale: linear, range ≈60–85), Y = ρ2 (price vector component, dimensionless, scale: linear, range ≈75–90). Background shows nested contour lines (level sets / facets/ridges) of the Lagrangian dual function.

| Iterate | Panel (a) subdifferential — (ρ1, ρ2) ≈ | Panel (b) subgradient — (ρ1, ρ2) ≈ |
|---------|-----------------------------------------|-------------------------------------|
| 1 | ≈(80, 80) | ≈(80, 80) |
| 2 | ≈(76, 83) | ≈(76, 83) |
| 3 | ≈(72, 86) | ≈(73, 86) |
| 4 | ≈(68, 84) | ≈(72, 86) |
| 5,7 | ≈(69, 84) | 5 ≈(70, 85.5) |
| 6 | ≈(65, 85) | ≈(69, 85) |
| 8 | ≈(66, 85) | ≈(68, 85) / then cluster near (65, 85) |
| 9,10 | — | tight cluster ≈(64–65, 85) |

*(Iterate coordinates are approximate visual readings off the labeled points; the figure is illustrative of trajectory shape, not a data table.)*

## Trend summary
Both methods start at iterate 1 ≈(80, 80) and climb toward the ridge near ρ2 ≈ 85. The subgradient method (b) exhibits many short, zigzagging steps that crowd together (iterates 5–10 cluster tightly along the ridge, making little progress), illustrating multiplier zigzagging across the ridges of the non-smooth dual function. The extreme-point subdifferential method (a) takes fewer, larger, smoother steps toward the same neighborhood, illustrating alleviated zigzagging via steepest-ascent directions — at higher per-iteration computational cost. Supports the dual-category convergence claim.
