# Concepts

## 1. Wind-Hydrogen Integrated Energy System (WH-IES)
- **Notation**: WH-IES
- **Definition**: An integrated energy system combining wind power generation, electrolyzer (for hydrogen production), hydrogen storage tank, and fuel cell (for hydrogen-to-electricity reconversion). The system is connected to the utility grid, allowing both purchase and sale of electricity.
- **Boundary conditions**: Includes wind-H2 path but not solar, battery, or other storage technologies in the base configuration. The system boundary is the investment planning and daily operational horizon.
- **Related concepts**: Power-to-Gas (P2G), Power-to-Gas-to-Power (P2G2P), multi-energy system, sector coupling

## 2. Two-Stage Stochastic Programming
- **Notation**: 2-SP
- **Definition**: A mathematical programming framework for decision-making under uncertainty where first-stage (here-and-now) decisions are made before uncertainty is realized, and second-stage (wait-and-see) recourse decisions are optimized after observing the realized uncertainty scenario.
- **Boundary conditions**: Uses a finite scenario set with known probabilities (expected value optimization), distinct from robust optimization which uses a worst-case uncertainty set.
- **Related concepts**: Stochastic programming, recourse model, scenario-based uncertainty, expected value optimization

## 3. General Soldiers Optimization Algorithm (GSOA)
- **Notation**: GSOA
- **Definition**: A population-based metaheuristic algorithm that operates as a derivative-free black-box solver. It maintains a population of candidate solutions and iteratively applies exploration and exploitation phases inspired by military command structures (leaders, general, soldiers). The exploration phase uses four update strategies (cosine movement, mean perturbation, differential perturbation, and uniform-random blending). The exploitation phase uses differential vectors from reference solutions.
- **Boundary conditions**: Requires only a fitness function that maps decision vectors to scalar costs. Does not require differentiability, continuity, or convexity. Designed for bounded decision domains.
- **Related concepts**: Metaheuristic, swarm intelligence, derivative-free optimization, population-based optimization

## 4. Benders Decomposition
- **Notation**: Benders
- **Definition**: A decomposition algorithm for solving large-scale optimization problems with complicating variables. The problem is split into a master problem (containing complicated variables) and subproblems (scenario-separable). Subproblem dual solutions generate cuts (supporting hyperplanes) that are added to the master problem, progressively improving the approximation of the recourse cost function.
- **Boundary conditions**: Requires the subproblem to be convex (here, LP) for valid cut generation. Standard Benders also requires the master problem to be solvable exactly — a condition relaxed in the GSOA-Benders framework.
- **Related concepts**: Benders cuts, L-shaped method, decomposition, column-and-constraint generation (C&CG)

## 5. Non-Analytical (Black-Box) Cost Function
- **Notation**: Black-box C_inv(x)
- **Definition**: A cost evaluator that accepts a decision vector and returns a cost value without providing an explicit algebraic or closed-form expression. Examples include supplier quotation engines with hidden discount rules, compiled simulation software, site-specific civil-work cost estimators, and trained machine learning models.
- **Boundary conditions**: The internal logic is opaque to the optimizer. The function may be non-convex, non-differentiable, discontinuous, or contain discrete jumps. Cannot be directly input into standard MINLP solvers without an explicit reformulation or surrogate layer.
- **Related concepts**: Derivative-free optimization, simulation-based optimization, surrogate modeling

## 6. Stability Gap
- **Notation**: G_stab_k
- **Definition**: A convergence metric for the GSOA-Benders hybrid framework defined as G_stab_k = |UB_k - c_LB_k| / max(1, |UB_k|), where UB_k is the best feasible total cost found up to iteration k and c_LB_k is the best master problem value over the accumulated Benders cut approximation. Unlike a classical optimality gap, the stability gap does not certify global optimality of the non-convex black-box master.
- **Boundary conditions**: The gap indicates solution stability with respect to the cut-plane approximation, not a mathematical optimality certificate. Stopping criteria: G_stab_k ≤ epsilon plus no material UB improvement for a fixed number of iterations.
- **Related concepts**: Optimality gap, convergence criteria, Benders decomposition, metaheuristic convergence

## 7. Expected Benders (Average) Cut
- **Notation**: `g(k)` cut
- **Definition**: Instead of generating one Benders cut per scenario, the framework constructs a single expected cut by probability-weighted averaging of the operational costs and dual variables across all N scenarios: Q-bar(k) = Σ π_s Q(x(k), ξ_s) with gradient g-bar(k) = Σ π_s g_s(k). This single "average cut" is added to the master problem per iteration.
- **Boundary conditions**: Valid because the expected recourse is the probability-weighted sum of convex scenario recourse functions. The averaging preserves the convexity and the supporting-hyperplane property of the cuts.
- **Related concepts**: Benders decomposition, multicut Benders, expected value

## 8. Hydrogen Storage Tank Cost with Sinusoidal Perturbation
- **Notation**: C_H2(E_H2)
- **Definition**: A composite non-convex cost function for hydrogen storage: C_H2(E_H2) = max(C_min, C_base(E_H2) + C_cyc(E_H2)). C_base is a power function (E_H2^0.7) with a step discount (×0.9) above 50 MWh reflecting economies of scale. C_cyc = κ_cyc · sin(E_H2/10) is a sinusoidal perturbation serving as a stylized proxy for irregular pricing from land constraints, modular procurement, or supplier-specific rules. C_min = $1M is a minimum investment threshold.
- **Boundary conditions**: The sinusoidal term is explicitly identified as a stylized numerical benchmark, not a first-principles engineering cost model. The parameters are chosen for methodological evaluation, not as universally valid equipment prices.
- **Related concepts**: Non-convex optimization, economies of scale, step-wise discount, black-box benchmark

## 9. Scenario Generation and Reduction
- **Notation**: N_initial → N
- **Definition**: Monte Carlo simulation generates N_initial = 1000 initial wind/load scenarios. A scenario reduction procedure selects N = 500 representative scenarios for the optimization, balancing solution accuracy with computational tractability.
- **Boundary conditions**: Scenario reduction preserves statistical representativeness of the wind-load distribution. The reduction method is not specified in detail but is visually validated in Figure 4.
- **Related concepts**: Monte Carlo simulation, scenario tree, stochastic programming, representativeness

## 10. Recourse Convexity
- **Notation**: Q-bar(x) convex
- **Definition**: For a fixed scenario s, the operational subproblem is an LP of the form Q_s(x) = min{c^T y : Wy ≥ h - Tx, y ≥ 0}. By LP duality, Q_s(x) = max{λ^T(h - Tx) : A^T λ ≤ c, λ ≥ 0}, which is the pointwise maximum of affine functions in x and therefore convex. The expected recourse Q-bar(x) = Σ π_s Q_s(x) inherits this convexity.
- **Boundary conditions**: Requires the subproblem to be feasible for all x (enforced via slack variables with high penalty = complete recourse).
- **Related concepts**: LP duality, convex function, Benders decomposition, supporting hyperplane

## 11. Stability-Gap Interpretation
- **Notation**: (implicit)
- **Definition**: A conservative acknowledgment that the hybrid heuristic-Benders framework cannot provide a strict global optimality certificate. The stability gap measures convergence in a practical engineering sense — the incumbent solution has stabilized under the accumulated cut approximation — but does not prove that no better solution exists in the non-convex black-box master space.
- **Boundary conditions**: The paper explicitly warns against interpreting the stability gap as a rigorous global optimality gap. It is fit for engineering decision-support, not for mathematical certification.
- **Related concepts**: Optimality gap, engineering decision support, solution quality, metaheuristic

## 12. Power-to-Gas-to-Power (P2G2P) Round-Trip
- **Notation**: P2G2P
- **Definition**: The process chain of converting electricity to hydrogen via electrolysis (P2G), storing the hydrogen, and reconverting it back to electricity via a fuel cell (G2P). The round-trip efficiency is the product of electrolyzer and fuel-cell efficiencies.
- **Boundary conditions**: In the WH-IES case study, P_FC = 0 in the optimal solution, indicating P2G2P is not economically viable under the tested parameters. However, the hydrogen itself is used as an energy carrier for direct hydrogen demand (e.g., industrial), not solely for electricity reconversion.
- **Related concepts**: Electrolyzer, fuel cell, energy storage arbitrage, sector coupling
