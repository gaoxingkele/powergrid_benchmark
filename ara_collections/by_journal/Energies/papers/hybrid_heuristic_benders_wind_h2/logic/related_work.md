# Related Work

## 1. Stochastic and Robust Planning for Renewable-Dominant Systems
- **Key works**: [13] Zeng & Zhao (2013) — C&CG method; [14] Bertsimas et al. (2013) — adaptive robust optimization for SCUC; [15] Wang et al. (2016) — risk-based admissibility
- **Relevance**: These works establish the methodological foundation for two-stage and tri-level planning under uncertainty in power systems. C&CG is identified as a powerful approach for explicit two-stage/tri-level robust planning models.
- **Differentiation**: The present paper uses stochastic programming (expectation over scenarios) rather than robust optimization (worst-case). More fundamentally, C&CG requires explicit master problem formulation, which is unavailable when the first-stage cost is black-box.

## 2. Bi-Directional Converter Planning with C&CG
- **Key works**: [16] Liang et al. (2025) — bi-directional converter interconnection for hybrid microgrids, tri-level robust planning with fully parallel C&CG
- **Relevance**: This recent work demonstrates the state of the art in C&CG for renewable-dominant systems, including convexification of converter-efficiency nonlinearity. It represents the type of approach that is preferred when explicit formulation is available.
- **Differentiation**: The present paper explicitly contrasts its problem structure (black-box first-stage cost, stochastic expectation) with C&CG's domain (explicit master, robust/tri-level). The differentiation is a key positioning point of Section 2.1.

## 3. MILP/MINLP Reformulation Methods
- **Key works**: [17] Gurobi reference manual; [19] Vielma (2015) — MILP formulation techniques; [20] Belotti et al. (2013) — MINLP methods
- **Relevance**: These methods are the standard approach for solving explicit optimization problems. Gurobi's MINLP solver handles non-convex explicit problems effectively.
- **Differentiation**: The paper acknowledges that MILP/MINLP reformulation (e.g., piecewise linearization, SOS2 constraints) could theoretically be applied to the hydrogen tank cost function. However, the sinusoidal component would require an excessive number of binary variables, and more importantly, true black-box evaluators (compiled code, neural networks) cannot be reformulated at all.

## 4. Heuristic and Surrogate-Assisted Optimization for Energy Planning
- **Key works**: [21] Khan et al. (2022) — review of optimization for H2 systems; [22] Kennedy & Eberhart — PSO; [23] Mirjalili et al. — Grey Wolf Optimizer; [24] Kaabeche et al. — sizing optimization; [25] Audet & Hare — derivative-free optimization
- **Relevance**: Metaheuristics and surrogate methods are widely used for hybrid renewable energy planning, especially when the problem exhibits non-convex, non-differentiable, or black-box characteristics.
- **Differentiation**: Pure heuristic approaches evaluate the full operational model for every candidate solution, which is computationally prohibitive for large scenario sets. The GSOA-Benders framework uses Benders cuts as an efficient surrogate for the expected operational cost, avoiding exhaustive LP evaluations in the master search.

## 5. Benders Decomposition for Power Systems
- **Key works**: [30] Shahidehpour & Fu (2005) — Benders decomposition survey for power systems; [31] Zhong et al. (2025) — Starfish Optimization Algorithm (SFOA)
- **Relevance**: Benders decomposition is a standard technique for decomposing large-scale power system problems. SFOA-Benders serves as a direct benchmark (Algorithm D) in the paper.
- **Differentiation**: Classical Benders requires the master problem to be solved exactly. The GSOA-Benders framework relaxes this by using GSOA (a metaheuristic) for the master, which introduces the stability gap as a practical convergence measure instead of a strict optimality certificate.

## 6. WH-IES Planning Studies
- **Key works**: [10] Liu et al. (2024); [11] Pan et al. (2020); [12] Khodaei (2017)
- **Relevance**: These works study optimal planning and capacity sizing for wind-hydrogen and electricity-hydrogen integrated energy systems, providing the domain context for the present paper.
- **Differentiation**: Prior WH-IES planning works typically formulate the investment cost as explicit analytical functions solvable via standard MILP/MINLP. The present paper addresses the case where the hydrogen storage cost is available only through a black-box evaluator.
