# Algorithm: NSGA-II (Non-dominated Sorting Genetic Algorithm II)

## Overview
NSGA-II is a multi-objective evolutionary algorithm introduced by Deb et al. [27]. It uses fast non-dominated sorting, crowding distance assignment, and an elite-preserving strategy to find diverse sets of Pareto-optimal solutions.

## Key Components

### 1. Fast Non-dominated Sorting
Individuals in the population are ranked into different non-domination levels (fronts). Each individual is assigned a rank equal to its non-domination level, where rank 1 is the best (Pareto-optimal) front.

### 2. Crowding Distance
For each individual in a front, the crowding distance measures the density of solutions surrounding it:

```
d_i = sum_{m=1}^{M} |f_m(i+1) - f_m(i-1)| / (f_m_max - f_m_min)
```

where M is the number of objectives, and f_m(i) is the value of the m-th objective for individual i. A larger crowding distance indicates less crowding and is preferred.

### 3. Selection
Binary tournament selection based on:
1. Rank (lower rank preferred)
2. Crowding distance (higher distance preferred when ranks are equal)

### 4. Genetic Operators
- **Crossover probability**: 0.5
- **Mutation probability**: 0.5
- Offspring production: 60 per generation
- Population size: 20 (maintained constant across generations)

### 5. Elite Strategy
Parent and offspring populations are merged before selection, ensuring that the best individuals are never lost.

## Parameter Settings for This Study
| Parameter | Value |
|-----------|-------|
| Population size | 20 |
| Offspring per generation | 60 |
| Generations | 300 |
| Crossover probability | 0.5 |
| Mutation probability | 0.5 |
| Decision variables | 2 (P_es, S_es) |
| Objectives | 2 (Cost, Volatility) |
| P_es range | 0-12 MW |
| S_es range | 0-48 MWh |

## Algorithm Steps (Simplified)
1. Input wind farm parameters; define feasible ranges for P_es and S_es; initialize random population of 20 individuals.
2. Evaluate each individual using objective functions and constraints.
3. For 300 generations: perform reproduction (crossover + mutation), evaluate offspring, merge parent and offspring populations, perform non-dominated sorting, compute crowding distances, select 20 individuals for next generation.
4. Extract Pareto-optimal solutions; apply selection methods (ideal point or inflection point) to identify the optimal configuration.
5. Visualize results (Pareto frontier plots).

## Benchmark Algorithm: MOPSO
| Parameter | Value |
|-----------|-------|
| Population size | 50 |
| Archive size | 100 |
| Generations | 300 |
| Inertia weight (W) | 0.4 |
| Cognitive coefficient (C1) | 1.5 |
| Social coefficient (C2) | 1.5 |
