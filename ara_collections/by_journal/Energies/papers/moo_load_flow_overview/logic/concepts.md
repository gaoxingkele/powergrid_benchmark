# Concepts

## Core Domain Concepts

- **Optimal Power Flow (OPF)**: An optimization problem aiming to identify the optimal state of operation for power systems, satisfying constraints while minimizing or maximizing objective functions.

- **Multi-Objective Optimal Power Flow (MOOPF)**: An extension of OPF that simultaneously optimizes multiple competing objectives (e.g., cost, emissions, losses, voltage stability) subject to operational and physical constraints.

- **Pareto Optimality / Pareto Front**: A set of non-dominated solutions where no objective function can be improved without degrading at least one other objective. The Pareto front represents the trade-off surface of optimal solutions.

- **Renewable Energy Sources (RESs)**: Wind, solar, and other variable renewable generation sources whose integration introduces uncertainty and variability into power system optimization.

## Optimization Technique Categories

- **Classical (Deterministic) Optimization**: Methods including Linear Programming (LP), Nonlinear Programming (NLP), Quadratic Programming (QP), Mixed-Integer Programming (MIP), and Newton's method. These are mathematically rigorous but limited in handling non-linearity, integer variables, and large-scale problems.

- **Metaheuristic (Stochastic) Optimization**: Nature-inspired algorithms including Genetic Algorithms (GA), Particle Swarm Optimization (PSO), Differential Evolution (DE), Ant Colony Optimization (ACO), and their multi-objective variants (NSGA-II, MOPSO, MOEA/D).

- **Hybrid Optimization**: Approaches combining deterministic and stochastic methods to leverage the precision and convergence speed of classical methods with the exploration capability of metaheuristics.

- **AI-based Techniques**: Machine learning (ML), deep learning (DL), and deep reinforcement learning (DRL) approaches that use historical and simulated data to learn optimal power system configurations and control policies.

## Power System Topologies

- **Radial (Star) Networks**: Simple, low-cost configuration where feeders branch from a single source. Common in distribution systems but vulnerable to single-point failures.

- **Loop Networks**: Closed-path configuration offering improved reliability over radial design, with alternative supply routes, at the cost of increased protection complexity.

- **Mesh (Connected) Networks**: Highly interconnected configuration with multiple parallel power flow paths, typical of high-voltage transmission networks, offering maximum reliability at highest cost and complexity.

## Application Domains

- **Economic Dispatch**: Minimizing generation cost while meeting load demand
- **Network Reconfiguration**: Optimizing topology for loss minimization and voltage improvement
- **Reactive Power Planning**: Optimizing reactive power sources for voltage stability
- **Unit Commitment**: Scheduling generator on/off states over time horizons
- **Emission/Pollution Dispatch**: Balancing economic and environmental objectives

## Key Algorithm Concepts

- **Swarm Intelligence**: Population-based algorithms inspired by collective behavior (PSO, ACO, GWO, WOA, ALO)
- **Evolutionary Algorithms**: Genetic algorithms using selection, crossover, and mutation (GA, NSGA-II, DE, NSGA)
- **Decomposition-based MOEA (MOEA/D)**: Decomposes multi-objective problem into scalar subproblems
- **Constraint Handling**: Techniques like Superiority of Feasible Solutions (SF), Penalty Function Method (PFM), Constraint-Objective Sorting Rule (COSR)
- **Clustering and Decision Support**: Fuzzy C-Means (FCM), Grey Relational Projection (GRP), k-means Data Clustering Method (DCM)

## Uncertainty Modeling

- **Weibull Distribution**: Standard probability density function for modeling wind speed
- **Beta Distribution**: Standard probability density function for modeling solar irradiance
- **Information Gap Decision Theory (IGDT)**: Framework for managing uncertainty in multi-objective optimization
- **Monte Carlo Simulation**: Probabilistic technique for simulating network performance under uncertainty
