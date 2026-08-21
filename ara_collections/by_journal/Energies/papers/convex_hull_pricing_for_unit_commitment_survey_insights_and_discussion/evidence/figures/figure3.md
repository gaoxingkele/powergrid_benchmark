# Figure 3: Non-convex fuel cost function over the convex hull (two-block example)

- **Source**: Figure 3, Section 3.2 (polyhedron approach), page 8 (lower figure on the page)
- **Caption**: "Non-convex fuel cost function over the convex hull. A two-block example. (a) Fuel cost function over the feasible operating region. (b) Convex envelope over the convex hull."
- **Screenshot**: figure3.png (lower figure on PDF page 8)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - Same 3D axes as Figure 2: `x_{g,t}` (commitment, value 1), `f_g` (fuel cost), `p_{g,t}` (generation) with landmarks `0`, `P_g^min` (Break-point), `P_g^max`.
  - Panel (a): two-block fuel cost curve (blue, "First block" / "Second block") over the feasible operating region; here the slope from `0` to `P_g^min` (over `[0, P_g^max]`) is larger than the first-block slope, making the cost function non-convex over the convex hull.
  - Panel (b): the convex envelope (red outline) over the convex hull (green shaded region), obtained by scaling the original cost function using the commitment variable `x_{g,t}`.
- **Connections / annotations**: Because `x_{g,t} ≤ 1`, the scaled cost function underestimates or equals the original (blue) cost, producing a valid convex envelope (red) — the general framework of Ref. [8].
- **What it conveys**: When the per-unit fuel cost is non-convex over the convex hull, integer relaxation alone does NOT yield the convex envelope; a convexification (scaling by the commitment variable) is required. Contrasts directly with the convex case of Figure 2.
