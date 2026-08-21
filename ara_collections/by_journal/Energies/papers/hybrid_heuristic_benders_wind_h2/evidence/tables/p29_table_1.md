# Table 1: Algorithm Performance on Explicit Non-Convex Problem (N=1000)

| Algorithm | Variables/Constraints | Time (s) | Optimal Cost |
|-----------|---------------------|----------|--------------|
| Gurobi (MINLP) | 240,005 / 192,000 | 36.58 | -381,058.9 |
| GSOA-Benders | 4 / 240 | 45.66 | -342,939.52 |

**Key findings**:
- Gurobi presolve eliminated ~25% of problem scale in 0.43s
- Gurobi's MINLP branch-and-bound outperformed GSOA-Benders on both speed and solution quality
- GSOA-Benders managed to solve the problem but with lower performance
- This confirms the paper's premise: commercial solvers remain preferred for explicit models
