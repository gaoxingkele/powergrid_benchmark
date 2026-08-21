# Architecture: Bi-Level (Two-Tier) HESS Optimization Framework

## Overview
The architecture implements a closed-loop bi-level optimization framework coupling long-term planning (upper level) with short-term operational dispatch (lower level).

## Diagram (Textual)

```
+------------------------------------------------------------------+
|                    UPPER LEVEL (Planning)                         |
|  Objective: Minimize lifecycle cost C_total = C_inv + C_OM       |
|  Decision variables: Location, Rated Capacity, Rated Power       |
|  Solver: IWAA (Improved Weighted Average Algorithm)              |
|                                                                   |
|  Output: ESS configuration parameters                             |
|  {node_k, E_k, P_k} for k in {Li-ion, Flow Battery}              |
+------------------------------------------------------------------+
           |                                ^
           | ESS config                     | Operational results
           v                                |
+------------------------------------------------------------------+
|                    LOWER LEVEL (Operation)                        |
|  Objectives: Minimize [f1, f2, f3, f4]                            |
|    f1: Operational cost (O&M)                                     |
|    f2: Flexibility deficiency penalty cost                        |
|    f3: Voltage deviation                                           |
|    f4: Line losses                                                 |
|                                                                   |
|  Sub-module: VMD-PSO Power Allocation                              |
|    - Decompose total ESS power into IMFs via VMD                  |
|    - PSO optimizes K and alpha for VMD                            |
|    - Median frequency threshold separates high/low components     |
|    - Li-ion absorbs high-frequency, FB absorbs low-frequency      |
+------------------------------------------------------------------+
```

## Component Details

### Upper Level Planner
- **Input**: Load demand, wind/PV profiles, candidate nodes, ESS cost parameters
- **Process**: IWAA generates candidate ESS configurations (locations, capacities, powers)
- **Evaluation**: Each configuration's lifecycle cost is computed
- **Output**: Pareto front of optimal ESS configurations

### Lower Level Operator
- **Input**: ESS configuration from upper level, system state (load, generation)
- **Process**: 
  1. Calculate flexibility gap theta(t) = demand - supply
  2. VMD-PSO decomposes total ESS power into frequency components
  3. Allocate Li-ion power (high-freq) and FB power (low-freq)
  4. Compute flexibility penalty, voltage deviation, line losses
- **Output**: Multi-objective performance metrics fed back to upper level

### VMD-PSO Sub-module
- **PSO**: Optimizes VMD parameters K (mode number) and alpha (penalty factor)
- **VMD**: Decomposes ESS target power into K IMFs
- **Split**: Median frequency threshold separates IMFs into high-freq and low-freq groups
- **Reconstruction**: Sum of high-freq IMFs -> Li-ion target, sum of low-freq IMFs -> FB target

## Closed-Loop Iteration
1. Upper level generates candidate ESS configurations
2. For each configuration, lower level runs operational optimization
3. Multi-objective results (cost, flexibility, voltage, losses) are computed
4. IWAA updates the population based on fitness evaluations
5. Pareto set is maintained via dynamic crowding distance
6. Loop continues until MaxIter or convergence

## Key Mathematical Components

### Upper Level Objective
```
C_total = C_inv + C_OM
C_inv = sum(E_k * S_E,k) + sum(P_k * S_P,k)   // capacity + power costs
C_OM = sum(sum(c_OM,k^P * |P_ESS,k(t)|) + c_OM,k^Q * E_k)
```

### Lower Level Objectives
```
f1 = C_OM (operational cost)
f2 = sum(p_s * sum(Q_penal * |theta(t) - P_ESS(t)|))  // flexibility penalty
f3 = sum(p_s * sum(|U_i(t) - U_bar(t)|))  // voltage deviation
f4 = sum(sum((P_ij^2 + Q_ij^2) * R_ij / U_i^2))  // line losses
```
