# Figure 11: Comparison of annual average voltage stability indicators for planning schemes with or without DC consideration

- **Source**: Figure 11, Section 5.3–5.4 (page 19)
- **Caption**: "Comparison of annual average voltage stability indicators for planning schemes with or without DC consideration."
- **Screenshot**: figure11.png
- **Location on page**: Top of page 19.
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: low

- **Plot kind**: bar
- **Axes**: X = "Branch circuit" (branch index, ~0 to 40, linear), Y = "Annual average voltage stability index" (dimensionless, 0 to 0.1, linear)
- **Series**: Blue = "Exclude DC retrofit and DC new build"; Yellow = "Consider DC retrofit and DC new build"

| Branch (approx) | Y Exclude (blue) | Y Consider (yellow) |
|---|---|---|
| ~branch 4/5 (tallest) | ≈0.09 | ≈0.085 |
| most branches | ≈0.01–0.05 | ≈ lower than or equal to blue |
| branches 13, 17, 20, 23, 24, 30, 31 (DC-converted) | (nonzero) | ≈0 (set to 0) |
| branches 35, 36, 37 (new DC lines) | n/a | ≈0 (set to 0) |

## Trend summary
Across nearly every branch the "Consider DC" (yellow) index is at or below the "Exclude DC" (blue) index; branches that were converted to DC or newly built as DC (13, 17, 20, 23, 24, 30, 31 and 35, 36, 37) have their index explicitly set to 0 (no AC-type stability problem). Overall the hybrid AC/DC scheme has stronger (lower-index) branch voltage stability than the pure-AC scheme. Exact per-branch values are not printed; readings are approximate.
