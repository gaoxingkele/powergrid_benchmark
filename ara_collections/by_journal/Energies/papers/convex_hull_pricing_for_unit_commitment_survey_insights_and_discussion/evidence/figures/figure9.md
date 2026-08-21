# Figure 9: Novel quality measure of convex hull prices

- **Source**: Figure 9, Section 4.3 (SLR-based quality measure), page 16
- **Caption**: "Novel quality measure of convex hull prices."
- **Screenshot**: figure9.png (figure in the upper band of PDF page 16)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Axes `q(λ)` (vertical, dual objective) vs `λ` (horizontal, price). A concave "Dual function" curve (red) rises to a peak near `λ*`. Horizontal reference levels: "Feasible cost" (top), "Upper bound?" (a sought level just above the dual peak), and "Lower bound = dual value" (at/below the peak). Brackets on the right label "Duality gap = uplift payment" (between feasible cost and lower bound) and on the left "Measure of CH price quality" (the narrower gap between the upper bound and lower bound near the peak). Points `λ_k` and `λ*` are marked on the λ-axis.
- **Connections / annotations**: The standard duality gap (feasible cost − dual value) equals the uplift payment. The novel quality measure is the much smaller gap between a newly derived upper bound on the optimal dual value `q*` and the best-available lower bound (dual value).
- **What it conveys**: The SLR method [36] can generate a new upper bound on the optimal dual value [41]; the difference between this upper bound and the lower bound (best Lagrangian dual value) is a tighter quality measure for approximate convex hull prices than the standard duality gap. Testing on the IEEE 118-bus system shows advantages over the standard duality gap in accuracy and computational effort.
