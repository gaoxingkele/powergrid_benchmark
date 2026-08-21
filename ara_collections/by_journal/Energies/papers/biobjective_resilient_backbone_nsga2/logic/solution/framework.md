# Framework: Three-Stage Bi-Objective Resilient Backbone-Grid Planning

## High-Level Architecture

The overall framework integrates three components:

### 1. Resilience Quantitative Index System
- Recovery-distance contribution (F2_dist): Weighted shortest-path electrical distance from core-load buses to black-start/pumped-storage buses
- Capacity-weighted betweenness centrality (BC_psh): Combines topological betweenness centrality with power capacity ratings
- System resilience mismatch index (F2 = F2_dist * (1 - 0.3 * BC_psh))

### 2. Mathematical Planning Model
- Decision variables: Binary line selection vector Y
- Objective 1 (F1): Minimize normalized impedance sum (economic cost)
- Objective 2 (F2): Minimize resilience mismatch index
- Constraints: Connectivity, N-1 connectivity (edge connectivity >= 2), dual-scenario power flow security

### 3. TER-NSGA-II Optimization Engine
- Three-stage iterative execution
- Graph-theoretic constraint validation (max-flow min-cut)
- Periodic reverse learning mechanism
- Greedy post-processing

## Flow Diagram
```
Grid Data + Candidate Lines
        |
        v
    Initial Population
        |
        v
    Stage I: Connectivity Construction   <--- Graph search connectivity
        |
        v
    Stage II: N-1 Reinforcement   <--- Max-flow min-cut edge connectivity
        |
        v
    Stage III: Safety Convergence   <--- DC power flow risk indices
        |
        v
    Greedy Post-Processing
        |
        v
    Pareto-Optimal Backbone Grid Configurations
```

## Constraint Hierarchy
```
Constraint Type          | Stage Active | Validation Method
-------------------------|-------------|-------------------
Connectivity             | I, II, III  | Graph BFS/DFS
N-1 Connectivity         | II, III     | Max-flow min-cut (Dinic)
Power Flow Safety        | III         | DC power flow risk indices
```

## Parameter Configuration (IEEE 118-bus)
- T1 = 77 (stage I to II switch)
- T2 = 115 (stage II to III switch)
- Treverse = 49 (reverse learning interval)
- Tuned via irace (Iterated Racing procedure)

## Post-Processing
Greedy redundant line removal: Under the condition that F2 change does not exceed a preset threshold, redundant lines are removed one by one while checking constraint satisfaction, yielding a more concise final Pareto front.
