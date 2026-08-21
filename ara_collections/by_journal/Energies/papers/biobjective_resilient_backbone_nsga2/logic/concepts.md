# Concepts

## C01: Resilient Backbone Grid
A core network structure designed to ensure continuous power supply to critical loads during extreme disaster scenarios. It is formed by optimized transmission channels with topological redundancy and rapid recovery capabilities. The backbone grid must satisfy connectivity, N-1 connectivity (edge connectivity >= 2), and power flow security constraints while covering all critical power buses, core-load buses, and black-start buses.

## C02: System Resilience Mismatch Index (F2)
A composite index quantifying system resilience as the product of recovery-distance contribution (F2_dist) and a pumped-storage hub effect correction term (1 - alpha * BC_psh). Lower values indicate better resilience. The recovery-distance component measures the electrical distance from core loads to black-start sources, while the hub effect captures the topological centrality and power capacity of pumped-storage buses.

## C03: TER-NSGA-II (Three-Stage Evolutionary Reverse Learning NSGA-II)
A modified NSGA-II algorithm that divides the optimization into three stages: (I) connectivity construction, (II) N-1 connectivity reinforcement using max-flow min-cut validation, and (III) safety-constrained convergence. It incorporates periodic reverse learning and hierarchical constraint screening to handle rigid engineering constraints effectively.

## C04: Capacity-Weighted Betweenness Centrality (BC_psh)
A metric that integrates both topological betweenness centrality and available power capacity of pumped-storage buses. It extends standard betweenness centrality by weighting each pumped-storage bus's centrality by its rated capacity, providing a comprehensive evaluation of hub status and operational potential.

## C05: N-1 Connectivity (Edge Connectivity >= 2)
A constraint requiring at least two edge-disjoint paths between each core-load bus and each pumped-storage bus, ensuring that a single line fault cannot interrupt power supply to critical loads. This is validated using the max-flow min-cut theorem on a unit-capacity undirected graph representation.

## C06: Dual-Scenario Power Flow Security
The requirement that the backbone grid must satisfy safe operating conditions (line flow limits and bus angle difference limits) under two distinct operating scenarios: (1) generation scenario with 100% base load and pumped-storage units operating at 50-100% rated capacity for generation, and (2) pumping scenario with 70% base load and pumped-storage units at 100% rated capacity for pumping.

## C07: Recovery-Distance Contribution (F2_dist)
A normalized metric quantifying the minimum weighted electrical distance from core-load buses to black-start/pumped-storage buses. The weighted distance is based on line reactance adjusted by a capacity factor that reflects stronger power-transmission capability of higher-capacity lines, with a special discount factor for lines directly connected to pumped-storage buses.

## C08: Periodic Reverse Learning
A mechanism in TER-NSGA-II that generates complementary search directions by performing bitwise inversion (Y_bar = 1 - Y) on the binary chromosomes of current population individuals, followed by connectivity repair and stage-appropriate constraint handling. Triggered every Treverse generations to maintain population diversity and escape local optima.
