# Figure 3: GSOA-Benders Framework Flowchart

**Source**: Page 9 of the PDF.

**Visual Description**:
A flowchart illustrating the iterative solution procedure of the GSOA-Benders hybrid framework. The process alternates between two main components:

**Left side — Master Problem (MP)**:
- **GSOA search engine**: Population-based metaheuristic that proposes candidate investment decisions x
- Inputs: Benders cuts from subproblem, decision bounds, fitness function
- Output: Candidate investment vector x^{(k)}

**Right side — Sub-Problem (SP)**:
- **LP solver (Gurobi dual-simplex)**: Solves N=500 scenario subproblems for the fixed x^{(k)}
- Inputs: Candidate x^{(k)}, scenario parameters ξ_s
- Outputs: Operational costs Q(x^{(k)}, ξ_s) and dual variables λ_s

**Center — Cut Generation**:
- Aggregates scenario subproblem results into a single expected Benders cut (probability-weighted average)
- Adds the cut to the master problem for the next iteration

**Iteration loop**:
1. GSOA proposes x^{(k)}
2. For each scenario s, solve LP subproblem → get Q_s and λ_s
3. Compute expected cut: Q-bar and g-bar
4. Add cut to master problem
5. Check stability gap convergence criterion
6. If not converged, return to step 1; if converged, return x* as the solution

**Data extraction**: Not applicable — this is a flowchart/algorithm diagram, not a quantitative visualization.
