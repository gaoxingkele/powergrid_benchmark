# Figure 6: A systematic formulation approach to obtain approximate convex hulls

- **Source**: Figure 6, Section 3.4 (approximate convex hulls), page 12
- **Caption**: "A systematic formulation approach to obtain approximate convex hulls [32]."
- **Screenshot**: figure6.png (lower figure on PDF page 12)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two unit squares in the (x1, x2) plane with axes labeled 0..1.
  - Left square: a blue line represents the constraint `x1 + x2 ≥ 0.5`; a red triangle/edge marks the convex hull of the integer-feasible points.
  - Right square: after "Relax integral requirements", the constraint is converted into vertices (blue dots); open (fractional) vertices are dropped and solid (binary-feasible) vertices are kept.
- **Annotations**: Bidirectional arrows between the squares labeled "Relax integral requirements" and "Drop fractional vertices"; constraint shown in blue, convex hull in red.
- **Connections / procedure conveyed**: (1) relax integrality and convert constraints to vertices; (2) drop fractional (open blue dot) vertices since x1, x2 are binary; (3) convert the retained vertices back to constraints — these are tight, i.e., the convex hull is obtained; (4) parameterize the tight constraints (express numerical coefficients as combinations of unit parameters) for re-use.
- **What it conveys**: The systematic tightening approach [32] derives explicit convex hulls for T = 2 and T = 3 consecutive slots and reuses the resulting valid inequalities as approximate convex hulls for T > 3, trading exactness for tractability when exact convex-hull constraints grow exponentially.
