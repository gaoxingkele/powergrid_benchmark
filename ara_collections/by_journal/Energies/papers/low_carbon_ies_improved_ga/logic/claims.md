# Claims

## C01: Cyclic crossover preserves advantageous parental genetic structure while enhancing population diversity
- **Statement**: Cyclic crossover preserves the relative ordering and co-occurrence of genes from parent individuals by exchanging them along closed cycles, which prevents disruption of co-adapted gene combinations while simultaneously increasing offspring diversity by avoiding duplicate gene patterns — a pairing of structure preservation and diversity that standard crossover operators do not jointly provide.
- **Conditions**: Holds for real-coded GA optimization of multi-objective IES scheduling problems with 7 decision variables per time slot. The advantage may diminish for problems where gene loci are independent (no epistasis) or where the chromosome encoding does not admit meaningful cycles.
- **Sources**: [Cyclic crossover preserves genetic structure while avoiding duplicate combinations <- Section 3.3 «The cyclic crossover operation can preserve part of the genetic structure of the parent individuals and generate new offspring individuals... cyclic crossover can avoid producing duplicate gene combinations, thereby increasing the diversity of the population» [input]]
- **Status**: supported
- **Falsification criteria**: A systematic comparison on a set of multi-objective optimization problems where cyclic crossover produces populations with lower hypervolume or increased duplicate-gene frequency compared to standard simulated binary crossover (SBX) under matched conditions.
- **Proof**: [E01]
- **Evidence basis**: Section 3.3 describes the cyclic crossover mechanism: a starting gene is copied from parent 1 to offspring 1, then the matching gene in parent 2 is found and copied to offspring 2, and the chain continues. This preserves parental gene order while preventing duplicates. Figure 3 illustrates the operation schematically. The performance benefit is evidenced by IGA's Pareto front superiority over MGA (which uses standard crossover) in Figure 17, where IGA achieves lower-cost and lower-emission solutions.
- **Dependencies**: None
- **Tags**: crossover, genetic algorithm, cyclic crossover, IES optimization

## C02: Adaptive polynomial mutation with dynamic distribution index balances exploration and exploitation
- **Statement**: A distribution index for polynomial mutation that starts at a low value (favoring larger exploratory jumps) and increases monotonically with generation count transitions the search from broad exploration in early generations to fine-grained exploitation in later ones, preventing both premature convergence from overly aggressive mutation and stagnation from overly conservative mutation under a single fixed rate.
- **Conditions**: Holds for the distribution index range starting at βmin_m = 1 and increasing linearly with iteration count. The initial value βm = 1 provides a symmetric, uniform-like distribution appropriate for moderate exploration. The adaptive mechanism requires the number of iterations n to be available and monotonically increasing.
- **Sources**: [βm = βmin_m + n with βmin_m = 1 <- Section 3.4, Eq. (36) «βm = βmin_m + n... βm is the distribution index of the mutation, which can take any non-negative value. In this paper, it is initially set to 1» [input]; polynomial mutation adaptively adjusts mutation amplitude based on individual's fitness <- Section 3.4 «polynomial mutation operation... allows the mutation amplitude to be adaptively adjusted based on the individual's fitness» [input]]
- **Status**: supported
- **Falsification criteria**: A controlled experiment where IGA with fixed βm outperforms adaptive βm on a standard multi-objective benchmark, indicating that the dynamic adjustment either provides no benefit or actively harms convergence.
- **Proof**: [E01]
- **Evidence basis**: Section 3.4 defines polynomial mutation via Eq. (32)-(36). The parameter σ is computed from the polynomial distribution based on random number a and the current ψ (distance to bounds), and βm increases with iteration count. This mechanism is credited with enabling thorough solution space exploration while preventing premature convergence.
- **Dependencies**: [C01]
- **Tags**: mutation, polynomial mutation, adaptive parameter, genetic algorithm

## C03: Constraint-prioritizing parent selection with infeasible-solution elimination reduces equality constraint violations below practical thresholds
- **Statement**: A three-tier selection principle — (1) among feasible individuals, fast non-dominated sorting determines rank; (2) feasible individuals always dominate infeasible ones; (3) among infeasible individuals, smaller constraint violation degree is preferred — combined with offspring retention that eliminates constraint-violating individuals, enables systematic reduction of equality constraint violations to a small fraction of the system's load magnitude, orders of magnitude below what penalty-function methods achieve, across diverse operational scenarios.
- **Conditions**: Holds for the 49 equality constraints in the IES problem (24h power balance + 24h heat balance + initial ESS SOC constraint). The 0.3 kW bound is demonstrated for IES systems with load magnitudes on the order of hundreds of kW. The parent selection method is embedded within a GA framework; its effectiveness in non-GA optimization algorithms is untested.
- **Sources**: [Constraint violations below 0.3 kW across scenarios <- Table 1 «IGA V: 0.20 (S1), 0.29 (S2), 0.30 (S3)» [result]; three-tier selection principle <- Section 3.2 «(1) Among the individuals that do not violate the constraints, the fast non-dominated sorting algorithm is used... (2)...individuals who do not violate the constraints are considered winners. (3) Among individuals that violate the constraints, the individuals with smaller constraint violation degrees are considered winners» [input]; less than 0.2% deviation <- Abstract «representing less than 0.2% deviation from the IES's power demand» [result]]
- **Status**: supported
- **Falsification criteria**: An alternative constraint-handling method (e.g., augmented Lagrangian, ε-constrained method) produces lower maximum constraint violations than IGA on the same IES problem instances while maintaining comparable or better objective values.
- **Proof**: [E02, E03, E04]
- **Evidence basis**: Table 1 shows IGA achieves max constraint violations of 0.20 kW (Scenario 1), 0.29 kW (Scenario 2), and 0.30 kW (Scenario 3). These are substantially lower than MPSO (17.6, 13.4, 10.91) and MABC (2.5, 4.8, 3.74), and competitive with SGA (0.18, 0.32, 0.30). Figures 8, 12, and 16 show the 49 individual constraint violations per scenario.
- **Dependencies**: None
- **Tags**: constraint handling, parent selection, feasibility, IES, genetic algorithm

## C04: IGA achieves up to 5% improvement in both operating cost and carbon emission objectives compared to unimproved single-objective GA
- **Statement**: The combined cyclic crossover, adaptive polynomial mutation, and constraint-prioritizing selection enable the IGA to find solutions that are simultaneously lower in both operating cost and carbon emissions than those found by the single-objective GA baseline (SGA), across multiple IES operational scenarios.
- **Conditions**: Holds for the three operational scenarios defined in the paper (Scenario 1: normal PV+wind; Scenario 2: PV-outage+high prices; Scenario 3: PV-outage only). The 5% improvement is relative to the SGA baseline; absolute improvement depends on the scenario's load and price profiles. Improvement is measured at the weighted-score Pareto solution (w1 = w2 = 1).
- **Sources**: [5% improvement maximum <- Abstract «achieved maximum 5% improvement in both operational cost reduction and carbon emission minimization objectives compared to the unimproved single-objective genetic algorithm» [result]; Scenario 1 o1: IGA=3202.13, SGA=3468.18 <- Table 1 [result]; Scenario 1 o2: IGA=4216.66, SGA=4463.21 <- Table 1 [result]; Scenario 2 o1: IGA=8094.54, SGA=8295.44 <- Table 1 [result]; Scenario 3 o1: IGA=3381.65, SGA=3486.24 <- Table 1 [result]]
- **Status**: supported
- **Falsification criteria**: A replication study where IGA does not consistently outperform SGA on both objectives across the three scenarios, or where the improvement margin falls below 2% on either objective in any scenario.
- **Proof**: [E05]
- **Evidence basis**: Table 1 provides full numerical comparison. IGA achieves lower o1 (operating cost) and o2 (carbon emissions) than SGA, MGA, MPSO, and MABC in all three scenarios. IGA also achieves lower o1 and o2 than MGA in all scenarios, validating the contribution of the cyclic crossover and polynomial mutation enhancements.
- **Dependencies**: [C01, C02, C03]
- **Tags**: performance, multi-objective, IGA, IES optimization, carbon emissions

## C05: GA-based approaches with the proposed parent selection outperform penalty-function-based methods (MPSO, MABC) in constraint satisfaction across all IES operational scenarios
- **Statement**: The proposed parent selection strategy that eliminates infeasible solutions and carries successful chromosomes forward produces consistently lower equality constraint violations than penalty function methods (used by MPSO and MABC), because penalty functions treat equality constraints as soft objectives that can be traded off against cost, while the explicit elimination approach treats feasibility as a hard requirement.
- **Conditions**: Holds for the specific comparison between GA variants (IGA, MGA, SGA — all using the proposed parent selection) and non-GA methods (MPSO, MABC — using penalty function formulation of Eq. (38) with α1 = α2 = 1). The advantage magnitude depends on the penalty coefficient choice; insufficient penalty weight in MPSO/MABC would increase violations, while excessive weight would degrade their objective optimization.
- **Sources**: [MPSO max violation 17.6 (S1), 13.4 (S2), 10.91 (S3) <- Table 1 [result]; MABC max violation 2.5 (S1), 4.8 (S2), 3.74 (S3) <- Table 1 [result]; all GA variants below 0.33 in all scenarios <- Table 1 [result]; penalty function formulation Eq. (38) <- Section 4.5 «C′ = α1C + α2 Σ |...| ... The weights of α1 and α2 are set to 1» [input]]
- **Status**: supported
- **Falsification criteria**: A re-implementation where MPSO or MABC with carefully tuned penalty weights achieves constraint violations comparable to GA variants (<0.5 kW) while maintaining competitive objective values.
- **Proof**: [E05]
- **Evidence basis**: Table 1 shows a stark gap: GA variants maintain max violations <0.33 kW across all scenarios, while MPSO ranges 10.91-17.6 kW and MABC ranges 2.5-4.8 kW. Section 4.5 explains that MPSO and MABC use the penalty formulation (Eq. 38) which adds penalty terms to the objective function, treating constraints as soft.
- **Dependencies**: [C03, C04]
- **Tags**: constraint handling, penalty function, comparison, MPSO, MABC, genetic algorithm
