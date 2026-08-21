# Table 2: Benchmark Comparison on Black-Box Problem (N=500)

| Algorithm | Solution Status | Time (s) | Cost |
|-----------|----------------|----------|------|
| A: Gurobi-Monolithic | Direct exact solve unavailable | 0.00 | (N/A) |
| B: MILP-Benders (Reformulation) | Direct exact solve unavailable | 0.00 | (N/A) |
| C: GSOA+Simulation (Exhaustive) | Failed (Timeout) | >17,500 | (N/A) |
| D: SFOA-Benders | Successfully Converged | 51.15 | -242,940.18 |
| E: GSOA-Benders (Proposed) | Successfully Converged | 35.86 | -242,940.18 |

**Key findings**:
- Algorithms A and B cannot model the black-box function at all (not a runtime issue)
- Algorithm C is computationally prohibitive (~4.86 hours estimated, >17,500s actual timeout)
- D and E find the same objective value, confirming solution consistency across different master heuristics
- GSOA-Benders achieved 1.43× speedup over SFOA-Benders
- The common solution x = [1, 0.53, 23.23, 0]
