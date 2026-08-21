# Figure 2: Convex fuel cost function over the convex hull (two-block example)

- **Source**: Figure 2, Section 3.2 (network flow / tight formulation), page 8 (upper figure on the page)
- **Caption**: "Convex fuel cost function over the convex hull. A two-block example. (a) Fuel cost function over the feasible operating region. (b) Convex envelope over the convex hull."
- **Screenshot**: figure2.png (upper figure on PDF page 8)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - 3D axes: `x_{g,t}` (commitment axis, marked with value 1), `f_g` (fuel cost, vertical), `p_{g,t}` (generation level, horizontal). Landmarks on `p_{g,t}` axis: `0`, `P_g^min` (Break-point), `P_g^max`.
  - Panel (a): a two-block piecewise-linear fuel cost curve — "First block" and "Second block" (blue) — defined over the feasible operating region `{0} ∪ [P_g^min, P_g^max]`; a green segment marks the cost level at the commitment slice.
  - Panel (b): the convex envelope (red outline) drawn over the convex hull (green shaded region), the convexified operating range `[0, P_g^max]`.
- **Connections / annotations**: In this case the slope of the segment from `0` to `P_g^min` is smaller than the first-block slope, so the fuel cost function is convex over the convex hull, and integer relaxation directly yields the convex envelope (red) over the convex hull (green).
- **What it conveys**: When the per-unit fuel cost is convex over the convex hull, integer relaxation of the tight unit formulation produces both the convex hull and the convex envelope — no extra convexification needed. Supports the network-flow [7] and polyhedron [8] tight-formulation results.
