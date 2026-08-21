# Experiments

## E01: IEEE 118-Bus System Main Validation
- **Purpose**: Validate the proposed bi-objective planning approach and TER-NSGA-II algorithm on a medium-scale benchmark system
- **Test System**: IEEE 118-bus system with core generation buses (10, 69, 80, 89), core-load buses (11, 16, 20, 29, 50), and pumped-storage units at buses 63 and 64 (each 240 MW)
- **Algorithms Compared**: TER-NSGA-II, NSGA-II, NSGA-III/NG
- **Settings**: Population size = 50, max generations = 200, 50 independent runs per algorithm
- **Stages**: T1 = 77 (stage I->II), T2 = 115 (stage II->III), Treverse = 49 (reverse learning interval)
- **Metrics**: F1 mean/std/min, F2 mean/std/min, feasible-run rate, IGD+, HV, Spread
- **Key Results**: TER-NSGA-II achieves 100% feasible-run rate, lowest F1 mean (0.2276) and F2 mean (0.4738), best HV (0.2632)
- **Reference**: Section 6.3, Tables 2-3, Figures 3-4

## E02: irace Parameter Tuning
- **Purpose**: Automatically configure the stage-related parameters T1, T2, and Treverse to avoid purely empirical settings
- **Method**: irace (Iterated Racing for Automatic Algorithm Configuration)
- **Parameters Tuned**: p1 = T1/G, p2 = T2/G, pr = Treverse/G (normalized ratios relative to total generations G)
- **Candidates Compared**: Baseline (empirical), Candidate A, Candidate B, Candidate C
- **Selection Criteria**: Mean tuning cost, zero-cost frequency, feasible-solution generation capability, run-to-run stability
- **Final Configuration**: Candidate C selected (p1=0.387, p2=0.577, pr=0.247), corresponding to T1=77, T2=115, Treverse=49 for G=200
- **Reference**: Section 6.2, Table 1

## E03: Capacity-Weighted Betweenness Centrality Validation
- **Purpose**: Validate the arithmetic-mean aggregation form for the pumped-storage hub effect against alternatives
- **Schemes Compared**: Arithmetic mean (proposed), Geometric mean, Unweighted average
- **Evaluation**: IGD+, HV, Spread, F2 mean computed on five independent Pareto solution sets
- **Key Results**: Arithmetic mean achieves best IGD+ (0.007524), HV (0.108089), and F2 mean (0.474463)
- **Reference**: Section 6.4, Table 4

## E04: IEEE 300-Bus System Scalability Validation
- **Purpose**: Test scalability of the proposed method on a larger network
- **Test System**: IEEE 300-bus system under the same modeling framework
- **Algorithms Compared**: TER-NSGA-II, NSGA-II, NSGA-III/NG
- **Settings**: 10 independent runs per algorithm
- **Metrics**: F1 mean/std/min, F2 mean/std/min, IGD+, HV, Spread
- **Key Results**: TER-NSGA-II achieves lowest F1 mean (0.339519) with smallest std dev (0.000216), best IGD+ (0.000040) and HV (0.010866)
- **Reference**: Section 6.6, Tables 6-7, Figure 6

## E05: Surrogate Form Comparison (Appendix)
- **Purpose**: Compare multiplicative vs additive surrogate forms of the resilience mismatch index
- **Schemes**: Multiplicative form (proposed), Additive form, Distance-only form, Hub-only form
- **Scenarios**: Baseline (intact network) and severe perturbation (critical-line-drop)
- **Metric**: Relative degradation under severe perturbation compared to baseline
- **Key Results**: Multiplicative form shows 10.64-14.21% degradation vs 2.82-4.83% for additive form
- **Reference**: Appendix A.1, Table A1

## E06: Alpha Sensitivity Analysis (Appendix)
- **Purpose**: Evaluate the local stability of the hub effect influence coefficient alpha
- **Alpha Values Tested**: 0.1, 0.3, 0.5
- **Scenarios**: Baseline and severe perturbation
- **Key Results**: F2 varies linearly with alpha without abnormal jumps. Baseline consistently lower than severe perturbation across all alpha values. Alpha = 0.3 selected as balanced configuration.
- **Reference**: Appendix A.3, Table A2

## E07: Computational Performance Analysis
- **Purpose**: Compare runtime and feasible-solution count of compared algorithms
- **Systems**: IEEE 118-bus and IEEE 300-bus
- **Metrics**: Runtime (seconds), feasible-solution count
- **Key Results**: TER-NSGA-II requires more runtime but yields larger feasible-solution sets. IEEE 118-bus: 1336.49s runtime, 24.42 feasible solutions. IEEE 300-bus: 814.62s runtime, 50.00 feasible solutions.
- **Reference**: Section 6.7, Table 8
