# Constraints

## C1: Connectivity Constraint
The backbone grid must form a connected graph with all critical buses belonging to the same connected component.

V_key = V_bs union V_core union V_imp (all critical buses)
V_key subset of V(C1), |C| = 1

where C1 is the largest connected component of the network G(L') formed by selected lines, and |C| is the total number of connected components.

**Handling**: Quickly determined via graph theory search. A "main-component anchoring + incremental component connection" repair strategy is used, preferring low-cost lines.

## C2: N-1 Connectivity Constraint (Edge Connectivity >= 2)
At least two edge-disjoint paths must exist between each core-load bus and each pumped-storage bus.

lambda_G(L')(v, u) >= 2, for all v in V_core, u in V_psh

where lambda_G(L')(v, u) is the edge connectivity between buses v and u in graph G(L').

**Handling**: The network is abstracted as a unit-capacity undirected graph. Edge connectivity is calculated using the max-flow min-cut theorem. The minimum cut set identifies key reinforcement edges that guide evolution.

## C3: Power Flow Safety Constraints
The backbone grid must satisfy safe operating conditions under both pumped-storage generation and pumping scenarios.

### Generation Scenario
- Load at 100% of base value
- Pumped-storage units at 50-100% rated capacity for generation

### Pumping Scenario
- Load at 70% of base value
- Pumped-storage units at 100% rated capacity for pumping

### Safety Limits
|P_i| <= P_bar_i, for all lines i in L' (line flow limits)
|theta_m - theta_n| <= theta_bar, for all lines (angle difference limits)

### Risk Index Formulation
Hard constraints are transformed into continuous risk indices:
- R_line: Maximum line overload ratio
- R_angle: Maximum angle violation ratio
- R_scenario = max(R_line, R_angle) for each scenario
- R_total = max(R_pump, R_gen)

A feasible solution requires R_total = 0.

## Constraint Hierarchy
The constraints are ordered by increasing restrictiveness:
1. Connectivity (largest feasible space)
2. N-1 connectivity (edge connectivity >= 2)
3. Power flow safety (smallest feasible space)

This hierarchy motivates the three-stage evolutionary framework.
