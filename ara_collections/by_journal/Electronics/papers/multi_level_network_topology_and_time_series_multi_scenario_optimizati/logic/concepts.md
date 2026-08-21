# Concepts

## Hybrid AC/DC Distribution System (for data centers)
- **Notation**: —
- **Definition**: A distribution network in which parts of the topology (buses, lines, sub-systems) operate in DC and parts in AC, coupled through voltage-source converters, designed so that data-center DC loads and DC-output distributed generation connect within DC sub-systems to eliminate conversion links.
- **Boundary conditions**: Applies to medium/low-voltage distribution feeding data-center loads (10 kV mains down to 750 V DC bus and 336/240 V DC / 380/220 V AC equipment).
- **Related concepts**: Multi-Level Network Topology, DC Sub-system, Voltage-Source Converter

## Multi-Level Network Topology (reliability-tier design)
- **Notation**: —
- **Definition**: A physical-level supply-architecture design that assigns bus count, path redundancy, and backup to a data center according to its reliability tier (GB50174 A/B/C ↔ Uptime/TIA Tier I-IV), ranging from dual hot-standby DC buses (fault-tolerant) to a single non-redundant path (basic).
- **Boundary conditions**: Qualitative design at the physical level; availability is not computed numerically.
- **Related concepts**: Hybrid AC/DC Distribution System, Data-Center Reliability Tier

## Data-Center Reliability Tier
- **Notation**: A / B / C (GB50174); Tier I-IV (Uptime/TIA-942)
- **Definition**: A classification of data centers by required reliability/availability: A (fault-tolerant, highest), B (redundant, intermediate), C (basic, lowest), mapped to Uptime Tiers I-IV and to power-supply configuration methods (single mains, N+1, 2N, etc.).
- **Boundary conditions**: Per Table 1 correspondence; grade A maps to both Tier III and Tier IV.
- **Related concepts**: Multi-Level Network Topology

## Time-Series Multi-Scenario Planning
- **Notation**: N_t typical time-series scenarios; N_{s,j} scenarios; p_{s,j} probabilities; T=48 daily slots
- **Definition**: A planning formulation in which DG output and load are represented as probability-weighted typical time-series scenarios over the day and year, and the objective sums cost, loss, and voltage stability across all scenarios, coupling investment to operational variation.
- **Boundary conditions**: 12 typical time-series scenarios, 48 slots/day in this paper.
- **Related concepts**: Bi-Level Optimization, Voltage Stability Index

## DC-Load Penetration
- **Notation**: —
- **Definition**: The proportion of a data center's (or node's) load that is DC-driven; the driving variable whose growth shifts the cost-optimal topology from AC toward DC.
- **Boundary conditions**: Studied 0-80% at the network level and per-node in Table 4.
- **Related concepts**: Hybrid AC/DC Distribution System

## Voltage Stability Index (line ab)
- **Notation**: L_ab; L_VS = max{L_1,...,L_N}
- **Definition**: A per-AC-line index (Eq. 6) computed from the active/reactive power flow and voltage at the line ends, characterizing voltage drop/stability; the system objective f3 minimizes the maximum line index. DC branches are assigned index 0.
- **Boundary conditions**: Defined for AC branches only; based on ref [22].
- **Related concepts**: Time-Series Multi-Scenario Planning

## SABPSO (Pareto-niche hybrid chaotic binary PSO)
- **Notation**: —
- **Definition**: The hybrid chaotic binary particle-swarm optimization algorithm based on Pareto dominance and small-niching (small-habitat) sharing used to solve the multi-objective planning problem; particles are binary-coded over DG type/capacity, line DC-conversion flags, and new-load-point line choices (Eq. 11).
- **Boundary conditions**: Multi-objective minimization; compromise solution selected via fuzzy affiliation and variance assignment.
- **Related concepts**: Time-Series Multi-Scenario Planning, Pareto Dominance

## Converter Cost (capacity-proportional)
- **Notation**: C_conv, α_c, S_{i,g}, η_g
- **Definition**: The annualized cost of a converter, taken proportional to its active capacity; the economic pivot that makes DC retrofit uneconomic at low DC-load share and economic at high share, and that keeps high-capacity grid-connection buses AC.
- **Boundary conditions**: VSC unit cost $170/kVA in the examples; conversion efficiency 95%.
- **Related concepts**: DC Sub-system, DC-Load Penetration
