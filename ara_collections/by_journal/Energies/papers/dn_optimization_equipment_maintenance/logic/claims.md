# Claims

## C01: Flexibility-Grid Interconnection Synergy Reduces Flexibility Deficits

**Statement:** Integrating both a branch flexibility adequacy index and grid interconnection capability in the upper-layer optimization reduces flexibility deficits more effectively than applying either measure individually, because interconnection enables cross-grid resource sharing that resolves localized flexibility shortages.

**Conditions:** Active distribution network with multiple interconnected sub-grids, each containing renewable generation (wind/PV), energy storage, and flexible loads. Requires controllable tie-lines between sub-grids and real-time branch monitoring.

**Sources:**
- "Scheme 3 employs the double-layer optimization model proposed in this paper, allowing power interconnection between grids." [Source: Page 11]
- "Compared with Scheme 1 and Scheme 2, Scheme 3 achieves a dynamic balance of supply and demand in each grid." [Source: Page 11]
- "Scheme 2 introduces a flexibility index into the optimization but lacks grid interconnection. It reduces flexibility losses but cannot fully leverage flexible resources across the system, resulting in unbalanced performance among grids." [Source: Page 12]

**Status:** Supported by simulation evidence.

**Falsification criteria:**
- If a system with both flexibility index and interconnection shows flexibility deficits equal to or higher than a system with only one of these features.
- If the flexibility deficit cost in Scheme 3 (0.0184) is not lower than in Scheme 2 (0.0815) or Scheme 1 (0.1685).

**Proof:** E01 (Three-scheme comparison), E03 (Grid interconnection analysis)

**Evidence basis:**
- Table 1: Grid 1 flexibility deficit drops from 0.18 (Scheme 1) and 0.14 (Scheme 2) to 0.04 (Scheme 3). Grid 2 drops from 0.31 (Scheme 1) and 0.17 (Scheme 2) to 0.06 (Scheme 3).
- Table 2: Flexibility deficit cost drops from 0.1685 (Scheme 1) to 0.0815 (Scheme 2) to 0.0184 (Scheme 3) — a 89% reduction from Scheme 1 to Scheme 3.

**Dependencies:** C02 (DRO provides operational robustness enabling the benefits of reconfiguration)

**Tags:** flexibility, grid_interconnection, multi_grid, reconfiguration

---

## C02: DRO with Comprehensive Norm Ambiguity Set Outperforms Deterministic, Stochastic, and Robust Models

**Statement:** A distributionally robust optimization (DRO) framework using a joint 1-norm and infinity-norm ambiguity set achieves lower average cost and lower worst-case cost under renewable and load uncertainty compared to deterministic, stochastic programming, and traditional robust optimization approaches, because it balances robustness against conservatism through probabilistic ambiguity set construction.

**Conditions:** Renewable generation uncertainty from wind and PV, load forecast errors. Requires historical data for initial scenario construction. Tested on a 62-node system with 500 Monte Carlo scenarios.

**Sources:**
- "The proposed DRO model adopts an ambiguity set approach to capture uncertainty without requiring precise probability distributions. This allows for a more balanced solution that maintains robustness while improving economic efficiency." [Source: Page 12]
- "The deterministic model exhibits the highest average and maximum costs due to its inability to account for uncertainty." [Source: Pages 12-13]
- "Although the stochastic optimization model achieves a lower average cost, it lacks robustness, resulting in high operational risks under unfavorable renewable generation and load conditions." [Source: Page 13]
- "The robust model offers better protection against cost spikes, but its overly conservative nature leads to higher comprehensive costs." [Source: Page 13]
- "The proposed model achieves the lowest average cost and the lowest maximum cost across all scenarios." [Source: Page 13]

**Status:** Supported by Monte Carlo simulation evidence.

**Falsification criteria:**
- If an alternative method (deterministic, stochastic, or robust) shows lower average AND lower maximum cost than the proposed DRO model across 500 scenarios.
- If the comprehensive norm ambiguity set (joint 1-norm and infinity-norm) leads to worse performance than a single-norm ambiguity set.

**Proof:** E02 (Monte Carlo comparative analysis)

**Evidence basis:**
- Figure 7: Bar chart comparison of Monte Carlo statistical results showing the proposed model (DRO) achieves lowest average and maximum cost.
- Figure 8: Cost distribution comparisons across three typical scenarios (high/medium/low renewable output).
- "Our model achieves an average cost reduction of 6.8% compared with traditional robust methods, and up to 14.5% compared with deterministic optimization." [Source: Page 14]

**Dependencies:** E02, C01 (better topology from reconfiguration enables better DRO performance)

**Tags:** DRO, uncertainty, robustness, Monte_Carlo, comparative_analysis

---

## C03: Hybrid ACO-FHO-DE Algorithm Effectively Solves Two-Layer Optimization

**Statement:** The hybrid metaheuristic combining Ant Colony Optimization (global exploration), Fire Hawk Optimization (local refinement), and Differential Evolution (mutation/crossover), enhanced by Tent chaos mapping and adaptive weight mechanisms, solves the coupled two-layer topology-dispatch optimization problem more effectively than any single algorithm alone.

**Conditions:** Non-convex, mixed-integer optimization problem with both discrete topology variables (branch switching states) and continuous dispatch variables. Requires sufficient computational budget for iterative convergence.

**Sources:**
- "The hybrid algorithm fully utilizes the global search capability of ACO, the local optimization capability of FHO, and the global exploration capability of DE." [Source: Page 6]
- "Tent chaotic mapping can enhance population diversity, and the adaptive weight mechanism balances global and local searches." [Source: Page 6]
- "These techniques help the algorithm handle multivariable optimization problems in complex models while also ensuring that high-quality solutions are found within a reasonable computational time." [Source: Page 6]

**Status:** Supported by algorithmic description and convergence claims.

**Falsification criteria:**
- If a single algorithm (ACO, FHO, or DE alone) achieves equal or better solution quality within the same computational time.
- If the algorithm fails to converge to a stable solution within reasonable iterations.
- If the adaptive weight mechanism does not measurably improve convergence speed or solution quality.

**Proof:** E01, E02 (the algorithm is used in both experiments)

**Evidence basis:**
- The two-layer optimization framework converged and produced consistent results across schemes and scenarios (Table 1, Table 2, Figures 7-8).
- Algorithm flow described in Section 2.3 (Figure 2) and Equations (19)-(26).

**Dependencies:** None (algorithm operates as a solver; no other claim depends on it except through solution quality)

**Tags:** metaheuristic, hybrid_algorithm, ACO, FHO, DE, optimization

---

## C04: Branch Flexibility Evaluation Enables Predictive Maintenance

**Statement:** The branch flexibility adequacy (FBF) index, when used as an optimization objective in grid reconfiguration, identifies optimal switching strategies and branch stress levels that support predictive and condition-based maintenance decision-making.

**Conditions:** Distribution network with switchable branches and monitoring infrastructure capable of measuring or estimating branch loading and stress levels.

**Sources:**
- "The model contributes to predictive maintenance by identifying optimal switching strategies and branch stress levels." [Source: Abstract, Page 1]
- "In practical applications, the model also enhances maintainability by using branch flexibility indices and switchable topology to support predictive and condition-based maintenance through improved load balancing and branch stress monitoring." [Source: Page 15, Section 4]

**Status:** Claimed but weakly validated (qualitative discussion only, no quantitative maintenance metrics).

**Falsification criteria:**
- If branch flexibility adequacy does not correlate with actual branch stress/loading levels in the simulation results.
- If no measurable improvement in equipment stress distribution can be attributed to the FBF-based optimization.
- If predictive maintenance outcomes (e.g., reduced outage frequency, extended equipment life) cannot be quantitatively estimated from the model outputs.

**Proof:** E01 (scheme comparison shows different branch stress patterns)

**Evidence basis:**
- Table 1 shows branch flexibility adequacy values (Grid 1: 0.72, 0.67, 0.62 across schemes; Grid 2: 0.35, 0.31, 0.57; Grid 3: 0.86, 0.86, 0.71), but the link to maintenance outcomes is not directly quantified.
- The claim is discussed qualitatively in Section 4 but lacks experimental validation with maintenance metrics.

**Dependencies:** C01 (flexibility-reconfiguration synergy enables the branch stress improvements)

**Tags:** predictive_maintenance, branch_flexibility, equipment_health

---

## C05: Two-Layer Architecture Separating Topology and Dispatch Improves Tractability

**Statement:** Decomposing the distribution network optimization into an upper-layer topology-reconfiguration problem and a lower-layer robust dispatch problem, with iterative feedback between layers, improves computational tractability compared to solving the fully coupled problem in one stage, while preserving the benefits of coordination.

**Conditions:** Optimization problem with both structural (binary switching variables) and operational (continuous dispatch variables) decisions under uncertainty.

**Sources:**
- "The two-layer model uses a centralized distributed optimization structure, where the upper layer uses centralized optimization and the lower layer uses distributed optimization for each grid." [Source: Page 6]
- "Through the mutual iteration of the upper- and lower-layer models, the solution to the problem is achieved." [Source: Page 6]
- "The proposed method is theoretically grounded in bilevel optimization theory, which decomposes structural and operational decision-making to improve computational tractability." [Source: Page 15]

**Status:** Supported by architecture description and successful simulation results.

**Falsification criteria:**
- If a monolithic (single-layer) formulation solves the same problem to the same solution quality in less time.
- If the iterative feedback loop does not converge or oscillates between solutions.
- If the decomposition leads to significantly suboptimal solutions compared to the joint optimum.

**Proof:** E01, E02 (the architecture is used in all experiments)

**Evidence basis:**
- The framework successfully produced feasible and convergent solutions across all three schemes and 500 Monte Carlo scenarios.
- Figure 2 illustrates the two-layer iterative solution process.

**Dependencies:** C03 (the hybrid algorithm implements the two-layer iteration)

**Tags:** bilevel_optimization, architecture, decomposition, tractability
