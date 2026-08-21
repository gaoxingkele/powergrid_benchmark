# Algorithm: TER-NSGA-II

## Overview
Three-Stage Evolutionary Reverse Learning NSGA-II (TER-NSGA-II) extends standard NSGA-II by introducing:
1. A three-stage iterative framework matching engineering constraint hierarchy
2. Hierarchical constraint screening using graph-theoretic validation
3. Periodic reverse learning for enhanced global search

## Three-Stage Framework

### Stage I: Connectivity Construction (Generations 1 to T1)
- Goal: Rapidly converge toward the feasible domain
- Mechanism: Prioritize retaining individuals with the lowest constraint violation values
- Constraints active: Connectivity only (largest feasible space)
- Allocation: Early search effort primarily devoted to feasible connectivity construction

### Stage II: N-1 Connectivity Reinforcement (Generations T1+1 to T2)
- Goal: Balance N-1 connectivity and resilience objective F2
- Mechanism: 
  - Individuals satisfying N-1 connectivity receive selection advantage
  - Non-compliant individuals are identified for reinforcement through minimum cut set
  - Identified edges are favored in genetic operations
  - Max-flow min-cut theorem provides precise edge-connectivity validation
- Constraints active: Connectivity + N-1 connectivity

### Stage III: Safety-Convergence (Generations T2+1 to T_max)
- Goal: Objective optimization and Pareto-front refinement
- Mechanism: Population has largely satisfied all hard constraints; focus shifts to objective optimization and retention of Pareto-front individuals
- Constraints active: Connectivity + N-1 connectivity + power flow safety
- Dual-scenario DC power flow risk indices provide continuous search gradient

## Key Mechanisms

### Elite Retention
Top 5 elite individuals from each generation directly enter the next generation, ensuring stable transmission of high-quality solutions.

### Hierarchical Constraint Screening
Rather than "generate-repair" mode, hard constraints are transformed into dynamic selection pressures:
- Stage I: Connectivity via graph search, repair preferring low-cost lines
- Stage II: N-1 via max-flow min-cut, identifying key reinforcement edges
- Stage III: Power flow risk indices provide continuous search gradient

### Periodic Reverse Learning
Triggered every Treverse generations:
1. Each individual undergoes bitwise inversion: Y_bar = 1 - Y
2. Connectivity repair applied (stage-dependent additional constraint handling)
3. Repaired reverse individuals merged with original population and offspring
4. Non-dominated sorting, crowding distance, and elite preservation select next generation

### Greedy Post-Processing
After termination, redundant lines are removed one by one under the condition that F2 change stays within a preset threshold, while checking constraint satisfaction.

## Complexity
- Non-dominated sorting: O(M^2) per generation
- Connectivity/N-1 validation: O(min(V^(2/3), H^(1/2)) * E) per pair (Dinic algorithm)
- Total: O(T_max * M^2 + T_max * M * H)
- Where M = population size, T_max = max generations, H = number of candidate lines

## Pseudocode
```
1. Input: grid parameters, candidate set E
2. Initialize population P0 randomly
3. Evaluate F1, F2; apply connectivity repair
4. For t = 1 to T_max:
   a. Determine current stage based on t
   b. Apply stage-matched hierarchical constraint strategy
   c. Generate offspring Qt via binary tournament, mask crossover, bit-flip mutation
   d. If t mod Treverse == 0:
      - Generate reverse chromosomes Y_bar = 1 - Y
      - Apply connectivity + stage-dependent repair
      - Merge: Qt' = Qt + reverse individuals
   e. Else: Qt' = Qt
   f. Apply stage-matched constraint repair on Qt'
   g. Recalculate F1, F2
   h. Merge Qt' with Pt; apply non-dominated sorting and crowding distance
   i. Select top M individuals for Pt+1
5. Apply greedy post-processing on Pareto front
6. Output: Pareto-optimal solution set
```
