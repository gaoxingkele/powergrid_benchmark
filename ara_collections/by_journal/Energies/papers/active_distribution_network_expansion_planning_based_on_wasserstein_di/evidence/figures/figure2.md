# Figure 2: Flowchart of model solving

- **Source**: Figure 2, Section 4.1 (Overall Solution Framework)
- **Caption**: "Flowchart of model solving."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components / flow (top to bottom)**:
  1. "A Distributed Robust Programming Model Based on Wasserstein Distance" (the original bi-level MINLP model).
  2. Two parallel constraint groups: "Nonlinear Constraints" → "SOCP Constraints" (via convex relaxation), and "Wasserstein Distance Constraint" → "Equivalent Constraint" (equivalent transformation).
  3. Objective-function transformation chain: "Min-max" --dual--> "Min-min" --merge--> "Min" (Lagrange duality of the inner max, then merge inner/outer layers).
  4. "McCormick relaxation method to eliminate bilinear terms".
  5. "Obtain the MISOCP programming model and solve it by CPLEX solver".
- **Connections**: top model feeds the constraint-transformation block and the objective-transformation block; both feed the McCormick step; result is the solvable MISOCP.
- **What it conveys**: the three-stage reformulation pipeline — (a) constraint transformation (SOCP + Wasserstein equivalence), (b) Lagrange dualization of the inner worst-case max into a min and merge, (c) McCormick linearization of residual bilinear terms — converts the intractable min–max nonconvex model into a single-level MISOCP.

Mirrored into `logic/solution/method.md` (overall solution framework).
