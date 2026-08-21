# Figure 8: Depiction of projection on level set

- **Source**: Figure 8, Section 4.2 (level method), page 15
- **Caption**: "Depiction of projection on level set [18]."
- **Screenshot**: figure8.png (upper figure on PDF page 15)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Axes `q(λ)` (vertical, dual objective) vs `λ` (horizontal, price). A concave piecewise-linear (polyhedral) dual function is drawn with cutting-plane facets. Marked points: `LB_k` (lower bound) on a lower facet, `UB_k` (upper bound) at the peak of the cutting-plane model, and an intermediate point at height `αUB_k + (1−α)LB_k` (the projection level). A horizontal dashed red line marks the level `αUB_k + (1−α)LB_k`. An orange horizontal segment on the λ-axis labeled "Level set" spans between `λ_k` and `λ_{k+1}`; vertical dashed blue lines drop from the level line to `λ_k` and `λ_{k+1}`.
- **Connections / annotations**: The next iterate `λ_{k+1}` is obtained by projecting the current iterate onto the level set defined by `q(λ) ≥ αUB_k + (1−α)LB_k` (Eq. 23), rather than jumping to the cutting-plane optimum. The upward arrows depict the gap between LB_k and the projection level.
- **What it conveys**: The level method (Ref. [18], built on Kelley's algorithm) stabilizes the sequence of prices by moving to a projection on the level set instead of the cutting-plane optimum (α = 0 recovers Kelley's algorithm / no move; the paper uses α = 0.2). This yields smoother, more stable price updates than pure cutting-plane iteration.
