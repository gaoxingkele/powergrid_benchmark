# Experimental Environment

## Hardware
- **CPU**: 12th Gen Intel(R) Core(TM) i5-12490F
- **Logical processors**: 12
- **RAM**: 16 GB

## Software
- **OS**: Not explicitly stated
- **MATLAB**: R2023b
- **Gurobi**: 12.0.3
- **Gurobi API**: MATLAB interface for LP subproblem solving (dual-simplex algorithm)

## Solver Configuration
- LP subproblems solved via Gurobi's dual-simplex algorithm
- Master problem solver: GSOA (custom implementation in MATLAB)
- Population size: not explicitly stated (assumed ~50 based on runtime estimate)
- Maximum iterations: not explicitly stated (assumed ~100 based on runtime estimate)

## Scenario Configuration
- Initial scenarios (N_initial): 1000 (Monte Carlo generated)
- Representative scenarios (N): 500
- Time periods (T): 24 hours (daily operation)
- Annualization factor: 365 days/year
- Economic lifetime (L): 10 years (base case)

## Data Sources
- Scenario generation: Monte Carlo simulation [29]
- Scenario reduction: unspecified procedure (visualized in Figure 4)
- Electricity prices: Time-of-Use (TOU) purchase tariff and Feed-in Tariff (FiT) sell price
- Hydrogen demand profile: inflexible window (09:00-17:00)
