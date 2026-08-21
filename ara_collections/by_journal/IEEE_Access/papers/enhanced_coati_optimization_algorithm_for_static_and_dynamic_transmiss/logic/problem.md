# Problem Specification

## Observations

### O1: Load growth forces costly transmission expansion decisions
- **Statement**: Growing energy demand requires integrating new generation units and transmission lines at optimal locations and minimal cost; the TNEP objective minimizes the investment cost of added lines. Garver's original 6-bus example added a sixth bus with a 545 MW production unit to a system with 760 MW consumption and 215 MW production.
- **Evidence**: §I (Introduction), §IV; Garver 1970 [3].
- **Implication**: TNEP is an optimization problem over discrete line-addition decisions with strong economic stakes.

### O2: Mathematical (exact) optimization scales poorly on TNEP
- **Statement**: TNEP is a large-scale mixed-integer, nonlinear problem; exact methods (LP, MILP, MINLP, MBLP) rely on slope information, incur high computational time, and can be trapped in local optima, so they "cannot solve the problem effectively" at realistic scale.
- **Evidence**: §I; refs [3], [11]–[14].
- **Implication**: Metaheuristics are motivated by low computation time and gradient-free global search.

### O3: Generic metaheuristics get stuck in local optima on high-dimensional problems
- **Statement**: Hundreds of metaheuristics exist, but their common failure is getting stuck in local solution traps and converging early in high-dimensional search spaces, giving poor or random performance.
- **Evidence**: §I; §III.
- **Implication**: Design operators that maintain diversity and rebalance exploration/exploitation are needed.

### O4: The base Coati Optimization Algorithm is accurate but unstable
- **Statement**: COA (Dehghani et al., 2023) achieves the highest average performance in low-dimensional space but at the price of high variance; its coefficient of variation rises sharply with dimensionality, revealing randomness/instability, and it is the least effective algorithm in the study's benchmark rankings.
- **Evidence**: §III-B (scalability discussion, Table 7); Tables 2–4, 8–10 (COA ranked last / rank 10).
- **Implication**: COA needs guidance to convert its raw accuracy into reliable, scalable performance.

### O5: FDB and OBL are established, transferable enhancement operators
- **Statement**: Fitness-Distance Balance (Kahraman et al., 2020) is a selection method balancing candidate fitness and distance-to-best that has improved many metaheuristics (SFS, AGDE, LSHADE, TLABC, LFD, SDO, PPSO); OBL improves convergence speed and search-space coverage by using candidate solutions together with their opposites.
- **Evidence**: §I, §III-B, §III-C; refs [33]–[50].
- **Implication**: Both operators are candidate mechanisms to enhance COA, but their best configuration for COA was unknown.

## Gaps

### G1: The best position(s) inside COA to apply FDB selection was unknown
- **Statement**: FDB can be inserted at several position-update points of COA, and it was not established which insertion yields the best exploration/exploitation balance for COA.
- **Caused by**: O4, O5.
- **Existing attempts**: FDB applied to other algorithms (SOS, MRFO, ARO, etc.).
- **Why they fail**: Those studies do not address COA's specific two-stage (hunting/escaping) update structure; the optimal FDB variant is algorithm-specific.

### G2: The best OBL scheme to seed COA's initial population was unknown
- **Statement**: Eight distinct OBL schemes exist (Classical, Quasi-Reflection, Quasi, Super, Elite, Random, Dynamic, Probabilistic), and which produces the best initial diversity for the FDB-enhanced COA was not established.
- **Caused by**: O3, O5.
- **Existing attempts**: Individual OBL schemes used in various algorithms.
- **Why they fail**: No comparative identification of the best OBL scheme within the COA/FDBCOA pipeline had been done "for the first time."

### G3: COA had not been applied to Static and Dynamic multistage TNEP
- **Statement**: COA and an FDB+OBL-enhanced COA had not been used to solve the static or dynamic multistage TNEP problem, nor benchmarked against literature TNEP methods on small/medium/large systems.
- **Caused by**: O1, O2.
- **Existing attempts**: SA, GA, TS, PSO/DPSO/LPSO/MGPSO, ACO, ASSO, DABC, LSHADE-SPACMA, IBBA, GA-PSO, GBMO, MOX, DEA, CGA, HGA, EGA on TNEP.
- **Why they fail**: Prior methods leave headroom in investment cost, stability, and scalability, especially on the high-dimensional dynamic multistage case.

## Key Insight
- **Insight**: COA's raw accuracy can be turned into reliable, scalable performance by two independent, composable interventions at distinct points of the algorithm — (1) FDB selection at a chosen position-update step to steer the search away from local traps, and (2) opposition-based seeding of the initial population to maximize starting diversity — with the exact placement (which update equation gets FDB; which OBL scheme seeds) being the decisive tuning decision, resolved empirically via CEC2020/CEC2022 statistics.
- **Derived from**: O3, O4, O5.
- **Enables**: A concrete FDBCOA1-OBL5 configuration that solves static and dynamic TNEP competitively with literature.

## Assumptions
- A1: DC power flow is an acceptable approximation for TNEP (line resistances and reactive flow neglected); computed via MATPOWER.
- A2: Test-system cost coefficients are simplified/general and may differ from real cost volatility, but are adequate for benchmarking algorithms.
- A3: Constraint violations are handled by additive penalty terms with fixed penalty weights, rather than as hard constraints.
- A4: The maximum number of parallel lines between any two buses is 4 for all three test systems.
- A5: For the dynamic case, year 2002 is the base year and the annual interest rate I = 10%.
