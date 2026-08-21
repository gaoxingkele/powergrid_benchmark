# Figure 2: Learning factor iteration graph

- **Source**: Figure 2, Section 4.2.3 (page 10)
- **Caption**: "Learning factor iteration graph." (plot title inside: "Comparison of Two Functions")
- **Screenshot**: figure2.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: high
- **Plot kind**: line
- **Axes**: X = Iteration Number (t), range 0-2000, linear; Y = Function Value (c), range 0-2, linear

| Iteration t | c1 (solid red) | c2 (dashed blue) |
|-------------|----------------|-------------------|
| 0    | ≈2.0 | ≈0.0 |
| 500  | ≈1.7 | ≈0.3 |
| 1000 | ≈1.0 | ≈1.0 |
| 1500 | ≈0.3 | ≈1.7 |
| 2000 | ≈0.0 | ≈2.0 |

## Trend summary
c1 (individual learning factor, Eq. 28) decreases monotonically from ≈2 at t=0 to ≈0 at t=Tmax=2000; c2 (group learning factor, Eq. 29) increases monotonically from ≈0 to ≈2. The two curves are mirror images crossing at t≈1000 (Tmax/2) where both ≈1. This realizes the intended shift from exploration (individual/cognitive term dominant early) to exploitation (social/global term dominant late). Endpoints at ≈0 and ≈2 are exact by construction of the sin^2 formulas.
