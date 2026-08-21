# Objective Functions

## F1: Economic Objective (Total Life-Cycle Cost)
Minimizes the normalized sum of impedance moduli of selected transmission lines.

F1(Y) = sum(z_i * y_i) / Z_norm

where:
- z_i = sqrt(r_i^2 + x_i^2) is the impedance modulus of line i
- y_i in {0, 1} is the binary decision variable for line i
- Z_norm = 3 * (total impedance of minimum spanning tree) is the normalization factor, ensuring F1 falls within a reasonable range

## F2: System Resilience Mismatch Index
Minimizes the composite resilience metric coupling recovery-distance and pumped-storage hub effects.

F2(Y) = F2_dist(Y) * (1 - alpha * BC_psh(Y))

where:
- alpha = 0.3 is the hub effect influence coefficient

### F2_dist: Recovery-Distance Contribution
F2_dist = (1 / T_norm) * (1 / |V_core|) * sum(min over u in V_psh of d_w(v, u)) for v in V_core

where:
- V_core: set of core-load buses
- V_psh: set of pumped-storage (black-start) buses
- T_norm: normalization factor (max weighted shortest-path distance from any PSH bus to any core-load bus in the original grid)
- d_w(v, u): weighted shortest path distance from bus v to bus u

d_w(v, u) = min over paths p in P(v, u) of sum(x_i * 100 * k_i) for i in p

where:
- x_i: reactance of line i
- k_i = 1 / (1 + S_i / 1000 * xi_i): capacity adjustment factor
- S_i: rated capacity of line i
- xi_i: special discount factor for lines directly connected to pumped-storage buses

### BC_psh: Capacity-Weighted Betweenness Centrality
BC_psh = (sum over u of C_u * BC(u)) / (sum over u of C_u) for u in V_psh

where:
- C_u: rated capacity (MW) of pumped-storage bus u
- BC(u) = sum of sigma_st(u) / sigma_st for s != u != t: standard betweenness centrality based on weighted distance

## Trade-off
The bi-objective formulation seeks Pareto-optimal solutions that balance economic cost (F1) against resilience (F2). Pareto fronts are constructed from non-dominated solutions where improving one objective necessarily degrades the other. Representative schemes range from "Economic-oriented" (low F1, higher F2) to "Resilience-oriented" (higher F1, low F2).
