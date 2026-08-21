# Concepts

## Economic Dispatch (ED)
The operational condition that minimizes generation costs while meeting demand, subject to plant-specific constraints and losses. Classified as short-term (day/week), medium-term (monthly), and long-term (annual/multi-year).

## Hybrid Generation System (HGS)
A power system combining multiple generation types: hydroelectric, thermoelectric, photovoltaic solar, and wind power plants. Renewable sources are prioritized due to negligible operational costs.

## Photovoltaic Solar Power Generation
Ppv = Pn * (Isolar/1000) * (1 - Ci * (Tcell - 25)) * Np * Ns
- Cell temperature: Tcell = Tat + (Isolar/800) * (Nct - 20)

## Wind Power Generation
PWind = Nt * 0.5 * rho * A * e * Ws^3

## Monte Carlo Simulation
Probabilistic method using random sampling from fitted probability distribution functions to forecast renewable resource availability over a 24-hour horizon. 1000 simulations per variable.

## Probability Distribution Functions (PDF)
- **Weibull distribution**: Fitted to wind speed and solar radiation.
- **Gaussian Mixture Model (GMM)**: Fitted to temperature (bimodal behavior).

## Differential Evolution (DE)
Population-based metaheuristic using mutation (weighted difference vectors), crossover, and selection. Parameters: F=0.8, CR=0.9, 1000 iterations.

## Particle Swarm Optimization (PSO)
Social-behavior-inspired algorithm updating particle velocities and positions. Inertia range [0.55, 1.1].

## Cultural Algorithm (CA)
Dual-space (belief + population) evolutionary algorithm using situational and normative knowledge. Population size 50, alpha=0.3, beta=0.5, paccept=0.35.

## Grey Wolf Optimizer (GWO)
Hierarchical hunting-behavior-inspired algorithm. 20 search agents, 2000 iterations.

## Valve-Point Effect
Sinusoidal component added to quadratic fuel cost function to model steam inlet control, creating non-convex characteristics.

## Reservoir Management
Hydroelectric power depends on reservoir volume and water discharge, with coupled upstream/downstream dependencies.
