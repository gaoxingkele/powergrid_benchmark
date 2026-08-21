# Claims

## C01: Resilience Mismatch Index Quantifies Pumped-Storage Resilience Value
- **Statement**: The proposed system resilience mismatch index F2 = F2_dist x (1 - alpha x BC_psh), coupling recovery-distance contribution with capacity-weighted betweenness centrality, provides an explicit quantification of the resilience value of pumped storage in backbone-grid planning.
- **Mechanism**: The recovery-distance contribution F2_dist captures the electrical cost of restoring power from black-start buses to core loads. The capacity-weighted betweenness centrality BC_psh captures the topological hub role and power support capability of pumped-storage buses. Their multiplicative coupling provides a system-level resilience metric where lower values indicate better resilience.
- **Conditions**: The index is valid under the assumption that DC power flow approximates active power flows adequately. Requires a fixed set of pumped-storage buses with known capacity ratings.
- **Sources**: Section 3.1-3.4, Equations (3)-(8), Appendix A
- **Status**: Supported by comparative analysis of aggregation forms (Table 4) and sensitivity analysis of alpha (Table A2, Appendix A.3)
- **Falsification Criteria**: The claim is falsified if (a) the multiplicative form does not provide clearer discrimination than additive alternatives under severe perturbations, or (b) the index fails to distinguish between backbone configurations with known resilience differences.
- **Proof**: Appendix A.1 shows the multiplicative form exhibits 10.64%-14.21% relative degradation under severe perturbation versus 2.82%-4.83% for the additive form across three representative schemes. Appendix A.3 shows smooth, monotonic variation with alpha without discontinuities.
- **Evidence Basis**: Table 4 (Section 6.4), Table A1, Table A2 (Appendix A)
- **Dependencies**: Depends on correct computation of weighted shortest-path distances and betweenness centrality on the network graph.
- **Tags**: resilience, pumped-storage, index, quantitative

## C02: TER-NSGA-II Achieves 100% Feasible-Run Rate vs 48.11% for NSGA-II
- **Statement**: The TER-NSGA-II algorithm achieves a 100% feasible-run rate across 50 independent runs on the IEEE 118-bus system, while standard NSGA-II achieves only 48.11%, demonstrating significantly more reliable feasible-domain search under rigid connectivity, N-1 connectivity, and power flow safety constraints.
- **Mechanism**: The three-stage framework activates constraints in layers (connectivity -> N-1 -> power flow), and the max-flow min-cut theorem provides precise validation for edge-connectivity enhancement. Elite retention and hierarchical constraint screening guide the population toward feasibility.
- **Conditions**: All algorithms use the same decision encoding, population size (50), termination criterion (200 generations), network data, and constraint-evaluation criteria.
- **Sources**: Section 6.3, Table 2
- **Status**: Supported by experimental results
- **Falsification Criteria**: The claim is falsified if (a) TER-NSGA-II's feasible-run rate drops below 100% under the same settings in independent reproduction, or (b) the gap between TER-NSGA-II and NSGA-II is not statistically significant.
- **Proof**: Table 2 reports TER-NSGA-II feasible-run rate = 100.00%, NSGA-II = 48.11% over 50 independent runs.
- **Evidence Basis**: Table 2
- **Dependencies**: The result depends on the specific parameter settings (T1=77, T2=115, Treverse=49) tuned via irace.
- **Tags**: TER-NSGA-II, feasible-run-rate, constraint-handling, IEEE-118

## C03: Three-Stage Framework with Max-Flow Min-Cut Ensures Strict Edge Connectivity >= 2
- **Statement**: The three-stage hierarchical constraint-handling framework (connectivity construction -> N-1 reinforcement -> safety convergence), combined with max-flow min-cut theorem for edge-connectivity validation, ensures strict satisfaction of N-1 connectivity (edge connectivity >= 2) while maintaining search efficiency.
- **Mechanism**: Stage I focuses on connectivity construction with a large feasible space. Stage II applies max-flow min-cut to compute edge connectivity between core-load and pumped-storage pairs, identifying minimum cut sets for targeted reinforcement. Stage III fine-tunes with power flow safety. The layered approach avoids the exponential complexity of monolithic constraint handling.
- **Conditions**: The network graph must be undirected for edge connectivity calculation. The Dinic algorithm is used for max-flow computation.
- **Sources**: Section 5.1-5.2, Section 5.5
- **Status**: Supported by theoretical complexity analysis and experimental validation
- **Falsification Criteria**: The claim is falsified if (a) any feasible solution in the Pareto set violates edge connectivity >= 2, or (b) the computational complexity grows faster than O(T_max M^2 + T_max M H) as claimed.
- **Proof**: Time complexity analysis in Section 5.5: O(T_max M^2 + T_max M H) compared to standard NSGA-II's O(T_max M^2). In IEEE 118-bus system, only 10 core-load/PSH bus pairs need computation, making this less time-consuming than non-dominated sorting.
- **Evidence Basis**: Section 5.5, Table 2 (100% feasible-run rate implies all solutions satisfy constraints)
- **Dependencies**: Depends on the correctness of max-flow min-cut implementation for edge connectivity validation.
- **Tags**: N-1-connectivity, edge-connectivity, max-flow-min-cut, three-stage

## C04: Periodic Reverse Learning Enhances Global Search
- **Statement**: The periodic reverse learning mechanism in TER-NSGA-II enhances global search capability by generating structurally diverse yet feasible candidate solutions through bitwise chromosome inversion followed by connectivity/constraint repair, reducing the risk of premature convergence.
- **Mechanism**: Every Treverse generations, reverse individuals are generated by bitwise inversion (Y_bar = 1 - Y) of current population individuals. These are then repaired for connectivity and stage-appropriate constraints, merged with the original population, and subjected to environmental selection. This creates complementary search directions.
- **Conditions**: Reverse learning is triggered when t mod Treverse = 0. The mechanism relies on effective connectivity repair to re-integrate reverse individuals.
- **Sources**: Section 5.3, Figure 1
- **Status**: Supported by design description but indirect experimental evidence (overall TER-NSGA-II performance)
- **Falsification Criteria**: The claim is falsified if removal of the reverse learning mechanism does not degrade solution quality or if reverse individuals never survive environmental selection.
- **Proof**: Ablation study not explicitly presented in the paper. The claim is supported by the algorithmic design rationale and the overall superior performance of TER-NSGA-II.
- **Evidence Basis**: Sections 5.3, Figure 1; overall results in Tables 2-3, 6-7
- **Dependencies**: Depends on connectivity repair effectiveness and appropriate Treverse parameter tuning.
- **Tags**: reverse-learning, diversity, global-search, NSGA-II

## C05: TER-NSGA-II Achieves Superior Multi-Objective Performance
- **Statement**: TER-NSGA-II achieves lower mean F1 (economy) and F2 (resilience) values, smaller standard deviations, and competitive multi-objective metrics (IGD+, HV, Spread) compared to NSGA-II and NSGA-III/NG on both IEEE 118-bus and IEEE 300-bus systems.
- **Mechanism**: The three-stage constraint handling and periodic reverse learning enable TER-NSGA-II to find better-quality Pareto solutions that are closer to the true Pareto front with better coverage of the objective space.
- **Conditions**: All algorithms run with same population size, iterations, and problem definition.
- **Sources**: Sections 6.3, 6.6, Tables 2, 3, 6, 7
- **Status**: Supported by experimental results
- **Falsification Criteria**: The claim is falsified if NSGA-II or NSGA-III/NG achieves statistically significantly better mean F1 and F2 values than TER-NSGA-II under the same experimental conditions in independent reproduction.
- **Proof**: IEEE 118-bus: TER-NSGA-II F1 mean = 0.2276 (vs NSGA-II 0.3065, NSGA-III/NG 0.2845), F2 mean = 0.4738 (vs 0.5088, 0.5071). IEEE 300-bus: TER-NSGA-II F1 mean = 0.339519 (vs 0.344422, 0.340238).
- **Evidence Basis**: Tables 2, 3, 6, 7
- **Dependencies**: Depends on the quality of the reference Pareto front used for computing IGD+ and HV.
- **Tags**: performance, Pareto, multi-objective, comparison

## C06: Multiplicative Surrogate Provides Stronger Resilience Discrimination
- **Statement**: The multiplicative surrogate form F2 = F2_dist x (1 - alpha x BC_psh) provides stronger discriminative capability for resilience differences between backbone-grid schemes compared to additive alternatives under severe perturbation scenarios.
- **Mechanism**: The multiplicative form amplifies the coupled degradation between increased recovery distance and weakened hub support under high-impact disturbances. The additive form tends to compress differences between schemes.
- **Conditions**: Evaluated on three representative backbone-grid schemes (economic, transitional, resilience-oriented) under baseline and severe perturbation (critical-line-drop) scenarios.
- **Sources**: Appendix A.1, Table A1
- **Status**: Supported by comparative analysis
- **Falsification Criteria**: The claim is falsified if the additive form shows equal or greater relative degradation than the multiplicative form under severe perturbation across the same schemes.
- **Proof**: Table A1 shows multiplicative form degradation: 10.64% (economic), 14.21% (transitional), 14.20% (resilience) vs additive form: 2.82%, 4.83%, 4.82%.
- **Evidence Basis**: Table A1
- **Dependencies**: The comparison is conducted on a fixed set of representative solutions, so results show index structure differences rather than optimization process differences.
- **Tags**: resilience-index, surrogate-form, multiplicative, discrimination
