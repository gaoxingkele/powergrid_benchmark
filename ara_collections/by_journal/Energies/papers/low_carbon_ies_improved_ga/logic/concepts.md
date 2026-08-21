# Concepts

## Integrated Energy System (IES)
- **Notation**: IES
- **Definition**: A system integrating multiple energy forms — power grids, heating networks, flexible loads, and natural gas networks — to improve energy utilization efficiency through coordinated operation. The IES in this paper specifically includes CHP units, gas boilers, waste heat recovery units, photovoltaic generation, wind power generation, and battery energy storage systems.
- **Boundary conditions**: The paper considers day-ahead scheduling over 24 hourly time slots. Renewable generation (PV, wind) and load profiles are assumed known or predictable.
- **Related concepts**: CHP unit, GB, WHU, ESS

## Improved Genetic Algorithm (IGA)
- **Notation**: IGA
- **Definition**: A multi-objective genetic algorithm incorporating three key enhancements: (1) cyclic crossover operation that preserves parental genetic structure while preventing duplicate gene combinations; (2) adaptive polynomial mutation with a dynamically increasing distribution index (βm = βmin_m + n); and (3) a constraint-prioritizing parent selection and offspring retention mechanism that eliminates infeasible solutions.
- **Boundary conditions**: Designed specifically for multi-objective IES optimization problems. Tested on problems with 7 decision variables per time slot over 24-hour horizons.
- **Related concepts**: Cyclic crossover, Polynomial mutation, Fast Non-Dominated Sorting

## Cyclic Crossover
- **Notation**: Described algorithmically in Section 3.3
- **Definition**: A crossover operator where genes are exchanged between parents along a closed cycle. A starting gene is selected from parent 1 and copied to offspring 1; the gene at the same position in parent 2 is found and copied to offspring 2; the matching gene from parent 1 is located and copied to offspring 1; the cycle continues until returning to the starting point. Remaining genes are copied from parent 1 to offspring 2 and parent 2 to offspring 1.
- **Boundary conditions**: Effective when preserving parental gene order is beneficial. Avoids duplicate gene combinations. No formal theoretical analysis of its bias or disruption properties is provided.
- **Related concepts**: Crossover, IGA, Genetic Algorithm

## Polynomial Mutation
- **Notation**: σ computed via Eq. (32); βm (distribution index)
- **Definition**: A mutation operator where the mutation amplitude follows a polynomial probability distribution. The parameter σ is computed from a uniform random number a and the current ψ (normalized distance to bounds), using a piecewise formula (Eq. 32). The distribution index βm controls the shape: lower values favor larger mutations, higher values favor smaller ones. βm starts at βmin_m = 1 and increases linearly with iteration count (βm = βmin_m + n).
- **Boundary conditions**: Requires non-negative βm. The initial value βm = 1 provides a symmetric, uniform-like distribution. Adaptive adjustment is linear and unbounded (may reduce mutation too much at high iteration counts).
- **Related concepts**: Mutation, IGA, Genetic Algorithm

## Tiered Pricing Mechanism
- **Notation**: Cgrid (Eq. 19), Cgas (Eq. 21), CCO2(e) (Eq. 20)
- **Definition**: A pricing structure where different consumption tiers correspond to different unit prices. For electricity and natural gas: consumption below threshold E0 (or V0) is billed at base price; excess is billed at 120% of base price. For carbon emissions: a three-tier structure with thresholds e1, e2 and corresponding unit prices cCO2_l1, cCO2_l2, cCO2_l3.
- **Boundary conditions**: Electricity tier threshold E0 = 175 kWh; natural gas tier threshold V0 = 50 m3; carbon emission tier thresholds e1 = 5000 m3, e2 = 6000 m3, e3 = 6500 m3. Carbon prices: cCO2_l1 = 0.2, cCO2_l2 = 0.3, cCO2_l3 = 0.4 CNY/m3.
- **Related concepts**: Cgrid, Cgas, CCO2, LMP, objective function

## Fast Non-Dominated Sorting (FNS)
- **Notation**: Described in Section 3.6
- **Definition**: A sorting algorithm based on NSGA-II [23] that classifies solutions into Pareto fronts by pairwise dominance comparison. A solution A dominates solution B if A's operating cost ≤ B's cost AND A's emissions ≤ B's emissions, with at least one strict inequality. Non-dominated solutions form the first Pareto front (rank 1). Within each front, crowding distance (normalized distance between adjacent solutions sorted by each objective) maintains diversity.
- **Boundary conditions**: Computational complexity is O(MN^2) where M = number of objectives (2) and N = population size. The two-objective case (cost + emissions) is computationally efficient. Dominance relations may become less discriminating with more objectives.
- **Related concepts**: Pareto front, Crowding distance, IGA, NSGA-II

## Weight-Based Pareto Solution Selection
- **Notation**: sk = w1*o^k_1 + w2*o^k_2 (Eq. 37)
- **Definition**: A post-optimization selection method that assigns each Pareto-optimal solution a score computed as the weighted sum of its normalized objective values. The solution with the lowest score is selected. In this paper, w1 = w2 = 1 (equal importance of cost and emissions).
- **Boundary conditions**: Equal weighting (w1 = w2 = 1) assumes the IES operator considers cost reduction and emission reduction equally important. Different weight choices would select different trade-off solutions from the Pareto front.
- **Related concepts**: Pareto front, FNS, multi-objective optimization
