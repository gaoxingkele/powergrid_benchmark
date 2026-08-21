# Figure 1: Illustrations of a convex hull and convex envelope

- **Source**: Figure 1, Section 1 (Introduction), page 2
- **Caption**: "Illustrations of a convex hull and convex envelope. (a) The blue solid curve is a non-convex function, and its convex envelope is delineated by the red dashed curve. (b) The blue lines indicate feasible solutions, and the red lines delineate their convex hull."
- **Screenshot**: figure1.png (figure occupies the lower-middle band of PDF page 2)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - Panel (a) "Convex envelope": axes `f(x)` (vertical) vs `x` (horizontal). A blue solid piecewise curve labeled "Non-convex function" rises with a kink; a red dashed curve labeled "Convex Envelope" lies below/under it, smoothly supporting it from beneath.
  - Panel (b) "Convex hull": axes `x1` (vertical) vs `x2` (horizontal). Blue straight lines labeled "Constraints" bound a region; a grid of blue filled dots are feasible integer solutions; a red rectangle labeled "Convex hull" is the smallest convex set enclosing the feasible dots; one dot at bottom-left is marked `x*` (an optimal vertex).
- **Connections / annotations**: In (a) the convex envelope is the tightest convex under-estimator of the non-convex cost; in (b) the convex hull is the smallest convex polytope containing all feasible (integer) points, with the optimum `x*` sitting at a vertex.
- **What it conveys**: Defines the two geometric objects underlying convex hull pricing: the convex envelope (tightest convex function supporting the total-cost function from below) and the convex hull (smallest convex set containing all feasible solutions of a MILP/UC problem). The slope of the convex envelope over the convex hull is the convex hull price and is non-decreasing in demand.
