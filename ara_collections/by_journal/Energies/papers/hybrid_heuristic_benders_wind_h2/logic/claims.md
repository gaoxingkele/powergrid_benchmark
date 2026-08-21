# Claims

## Claim 1: Commercial solvers are superior for explicit analytical models but cannot directly process black-box cost functions
- **Statement**: Gurobi 12.0 solves the explicit non-convex MINLP formulation (N=1000 scenarios) in 36.58s, outperforming GSOA-Benders (45.66s) on both speed and solution quality. However, Gurobi cannot model or solve problems where the first-stage cost is a black-box evaluator (non-analytical, compiled, or externally computed).
- **Conditions**: Demonstrated on the explicit non-convex problem where all functions are analytically defined within Gurobi's syntax. The black-box infeasibility is demonstrated by the sinusoidal + power-law benchmark where Gurobi returned "Direct exact solve unavailable" (0.00s, N/A).
- **Sources**: Table 1 (Experiment I), Table 2 (Experiment II), Section 4.2, Section 4.3.1
- **Status**: Confirmed by paper evidence
- **Falsification criteria**: Showing Gurobi solving a WH-IES problem where the hydrogen tank cost is computed by external compiled code or a neural network without an explicit reformulation layer would falsify this claim.
- **Proof**: Experiment I: Gurobi objective −381,058.9 vs GSOA-Benders −342,939.52. Experiment II: Both Algorithm A (Gurobi-Monolithic) and Algorithm B (MILP-Benders) return N/A.
- **Evidence basis**: Tables 1 and 2; Sections 4.2, 4.3.1
- **Dependencies**: None
- **Tags**: benchmarks, commercial_solver, black_box, limitation

## Claim 2: GSOA-Benders provides a viable framework for black-box WH-IES planning
- **Statement**: The proposed GSOA-Benders framework converges within 35.86s on the 500-scenario black-box test case, identifying investment plan x = [1, 0.53, 23.23, 0] with total annualized cost −242,940.18, successfully handling non-analytical first-stage costs while retaining efficient scenario decomposition.
- **Conditions**: Black-box hydrogen tank cost function (power-law + sinusoidal perturbation + minimum threshold), 500 scenarios, MATLAB R2023b + Gurobi 12.0.3 for LP subproblems. Valid for problems where the recourse function is linear and scenario-separable.
- **Sources**: Section 4.3, Table 2, Section 4.4, Equation (27)
- **Status**: Confirmed by paper evidence
- **Falsification criteria**: Showing that GSOA-Benders fails to converge (e.g., stability gap does not decrease) on a problem with the same structure but different cost evaluator, or that repeated runs produce materially different solutions exceeding the stability gap.
- **Proof**: Table 2 shows Algorithm E (GSOA-Benders) "Successfully Converged" in 35.86s; the investment vector is explicitly reported as x* = [1, 0.53, 23.23, 0].
- **Evidence basis**: Table 2, Section 4.3, Section 4.4, Figure 6 (convergence curve)
- **Dependencies**: Claim 3 (Benders cut validity), Claim 4 (stability gap definition)
- **Tags**: core_result, framework, convergence, case_study

## Claim 3: Benders cuts provide valid lower approximations for the convex expected recourse function
- **Statement**: The expected second-stage operating cost Q-bar(x) = Σ π_s Q_s(x) is convex and piecewise-linear in x because each scenario subproblem is an LP. Benders cuts generated from optimal dual solutions produce valid supporting hyperplanes that lower-bound Q-bar(x).
- **Conditions**: The operational subproblem must be feasible for all x in the domain (achieved via slack variables with high penalty). The cuts do NOT bound or convexify the black-box investment cost C_inv(x).
- **Sources**: Section 3.1, Equations (19)-(21), Section 2.4
- **Status**: Confirmed (standard Benders decomposition theory applied to LP recourse)
- **Falsification criteria**: Showing the expected recourse function is non-convex for any WH-IES with linear operational constraints, or that dual solutions do not yield valid supporting hyperplanes.
- **Proof**: Standard LP duality: Q_s(x) = max_{λ} { λ^T (h_s - T_s x) | A^T λ ≤ c, λ ≥ 0 } which is convex and piecewise linear. Benders cut derived from λ^{(k)}_s gives Q_s(x) ≥ Q_s(x^{(k)}) + g^{(k)T}_s (x - x^{(k)}).
- **Evidence basis**: Section 3.1, Equations (19)-(21)
- **Dependencies**: None
- **Tags**: methodology, benders_decomposition, convexity, duality

## Claim 4: The stability gap is the appropriate convergence metric (not a strict optimality gap)
- **Statement**: Because the master problem solver (GSOA) is a derivative-free metaheuristic that does not guarantee global optimality for the non-convex black-box master problem, the convergence measure is defined as a stability gap: G_stab_k = |UB_k - c_LB_k| / max(1, |UB_k|), where UB_k is the best feasible total cost found and c_LB_k is the best master value over the cut approximation. This gap indicates solution stability with respect to the accumulated cut-plane approximation, not global optimality.
- **Conditions**: Applicable whenever the master problem solver cannot certify global optimality (i.e., metaheuristic or gradient-free optimization).
- **Sources**: Section 3.1, Equations (22)-(23), Section 1 contribution 2
- **Status**: Confirmed (explicitly defined and acknowledged in the paper)
- **Falsification criteria**: Claiming GSOA-Benders provides a provable global optimality certificate for black-box master problems would falsify this claim.
- **Proof**: The paper explicitly states "it should not be interpreted as a mathematical certificate of global optimality for a non-convex black-box master problem" (Section 3.1).
- **Evidence basis**: Section 3.1, Equations (22)-(23)
- **Dependencies**: Claim 3
- **Tags**: methodology, convergence, stability_gap, limitations

## Claim 5: Simulation-based optimization (GSOA+Simulation) is computationally prohibitive for large scenario sets
- **Statement**: A pure GSOA+Simulation approach (evaluating all 500 LPs for each of ~5000 fitness evaluations) would require approximately 17,500 seconds (~4.86 hours), making it impractical for multi-scenario stochastic planning.
- **Conditions**: 100 GSOA iterations × 50 particles = 5000 fitness evaluations, each solving 500 LPs at ~0.007s per LP. This estimate assumes sequential LP solving without parallelization.
- **Sources**: Section 4.3.2, Equation (26)
- **Status**: Confirmed (theoretical estimate, not empirically run to completion — confirmed timeout at >17,500s in Table 2)
- **Falsification criteria**: Running GSOA+Simulation on a similar problem and completing optimization in substantially less than 4.86 hours without parallelism, or showing the estimate is wrong by an order of magnitude.
- **Proof**: T_total ≈ 5000 evals × (500 LPs × 0.007 s/LP) ≈ 17,500 s. Table 2 shows Algorithm C "Failed (Timeout) >17,500".
- **Evidence basis**: Table 2, Section 4.3.2, Equation (26)
- **Dependencies**: None
- **Tags**: benchmarks, computational_efficiency, limitation

## Claim 6: GSOA-Benders outperforms SFOA-Benders (alternative heuristic) in computational speed
- **Statement**: GSOA-Benders achieves a 1.43× speedup over SFOA-Benders (51.15s vs 35.86s) on the same black-box test case with identical algorithmic structure (only the master solver differs). Both converge to the same objective value (−242,940.18).
- **Conditions**: SFOA = Starfish Optimization Algorithm, used as drop-in replacement for the master solver. Same Benders cut structure, same scenario set, same hardware.
- **Sources**: Table 2, Section 4.3.3, Algorithm D definition
- **Status**: Confirmed by paper evidence
- **Falsification criteria**: Running both algorithms on the same problem and showing SFOA-Benders is not slower, or finding that the SFOA implementation is suboptimal.
- **Proof**: Table 2: Algorithm D (SFOA-Benders) 51.15s vs Algorithm E (GSOA-Benders) 35.86s.
- **Evidence basis**: Table 2
- **Dependencies**: Claim 2
- **Tags**: benchmarks, computational_efficiency, comparison

## Claim 7: The optimal solution exploits the non-convex cost structure (hydrogen tank at 23.23 MWh)
- **Statement**: The GSOA solver identifies E_H2 = 23.23 MWh, which coincides with a local minimum ("cost valley") in the sinusoidal perturbation of the hydrogen tank cost function. This demonstrates that the framework can exploit non-convex characteristics to discover solutions that linear approximations would miss, rather than merely accommodating the complexity.
- **Conditions**: The sinusoidal perturbation C_cyc(E_H2) = κ_cyc·sin(E_H2/10) creates regular local minima at specific capacities.
- **Sources**: Section 4.4.2, Equation (27)
- **Status**: Supported by economic interpretation in the paper
- **Falsification criteria**: Showing that a different starting point or metaheuristic configuration leads to a materially different tank capacity (e.g., >30 MWh or <10 MWh) with lower total cost, or that 23.23 MWh is actually a random outcome rather than a cost-minimizing selection.
- **Proof**: The investment solution x = [1, 0.53, 23.23, 0] includes E_H2 = 23.23 MWh. The paper argues this exploits the sin(E_H2/10) local minimum.
- **Evidence basis**: Section 4.4.2, Figure 2, Equation (27)
- **Dependencies**: Claim 2
- **Tags**: economic_analysis, non_convex, solution_interpretation

## Claim 8: The P2G2P (Power-to-Gas-to-Power) round-trip arbitrage is economically unviable under the tested parameters
- **Statement**: The optimal solution sets P_FC = 0 (no fuel cell investment), confirming that hydrogen-to-electricity reconversion is not economically justified given the efficiency losses in the conversion loop and current cost parameters. The wind farm's primary value is direct electricity sales to the grid (FiT revenue), not hydrogen storage cycling.
- **Conditions**: Tested parameters: linear fuel cell cost κ_FC, efficiency η_FC, TOU electricity prices, FiT rates. This result is parameter-dependent and would change with higher electricity prices or lower fuel cell costs.
- **Sources**: Section 4.4.1 (especially "Fuel Cell (P_FC = 0)")
- **Status**: Confirmed by paper results; acknowledged as parameter-dependent
- **Falsification criteria**: Finding P_FC > 0 in the optimal solution with the same cost parameters, or showing that a P2G2P configuration would yield lower total cost.
- **Proof**: The optimal vector explicitly sets P_FC = 0. The economic analysis explains that efficiency losses outweigh arbitrage revenue.
- **Evidence basis**: Section 4.4.1, Equation (27)
- **Dependencies**: Claim 2
- **Tags**: economic_analysis, fuel_cell, p2g, limitations
