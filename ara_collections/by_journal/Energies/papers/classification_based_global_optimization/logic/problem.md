# Problem Specification

## Observations

### O1: High power losses in radial distribution networks
- **Statement**: IEEE 33-bus and 69-bus radial distribution networks exhibit base-case active power losses of 210.99 kW and 225.00 kW respectively, with corresponding reactive power losses of 143.13 kVAR and 102.17 kVAR, prior to any DG or CB integration (Tables 2–5).
- **Evidence**: Tables 2, 3 (33-bus), Tables 4, 5 (69-bus), Section 4.
- **Implication**: Significant energy is wasted as losses in the base configuration, representing both economic cost and environmental impact.

### O2: Voltage degradation along radial feeders
- **Statement**: Minimum voltage in the base case is 0.9038 p.u. for the IEEE 33-bus system and 0.9092 p.u. for the IEEE 69-bus system, both below the desired 0.95 p.u. threshold (Tables 2–5).
- **Evidence**: Tables 2, 3, 4, 5, Section 4.
- **Implication**: Voltage regulation is inadequate, risking equipment damage and power quality issues.

### O3: EV penetration increases network stress
- **Statement**: Adding EV charging loads at hosting factors of 30%, 40%, and 50% increases branch loading, thermal stress, and voltage drops relative to the base case, as EVCS loads add concentrated demand (Section 5).
- **Evidence**: Section 5, Tables 2, 4.
- **Implication**: Growing EV adoption will exacerbate existing network problems unless coordinated planning is adopted.

### O4: Metaheuristic optimization methods have inherent limitations
- **Statement**: Existing approaches (PSO, GA, Firefly, GWO) suffer from excessive computational load, parameter sensitivity, black-box interpretability issues, and risk of local optima (Table 1, Section 1.3).
- **Evidence**: Table 1, Section 1.3.
- **Implication**: A deterministic, interpretable alternative is needed for distribution network planning.

### O5: Unsynchronized thermal capacity considerations
- **Statement**: Distribution branches' thermal capacity limits are seldom synchronized in existing planning frameworks, risking overloading under high EV penetration (Section 1.3, Table 1 limitations row).
- **Evidence**: Table 1, Section 1.3.
- **Implication**: Thermal limits must be integrated as constraints in the optimization to ensure practical feasibility.

## Gaps

### G1: No existing framework coordinates DG, CB, and EVCS planning under multiple hosting factors
- **Statement**: Existing studies optimize individual components or specific operational objectives but lack a unified framework that simultaneously addresses active power injection (DG), reactive power compensation (CB), and EV charging infrastructure (EVCS) under varying hosting factors.
- **Caused by**: O4, O5
- **Existing attempts**: Hybrid PSO-GA (Ref [23]), Multi-objective PSO ([24]), GA ([25]), Fuzzy Firefly ([26]) each address subsets but not the full three-component integration.
- **Why they fail**: Every existing method omits at least one of EVCS, CB, or thermal limits; most rely on stochastic search with parameter tuning issues.

### G2: Black-box optimization limits engineering interpretability
- **Statement**: Metaheuristic methods (PSO, GA, GWO) produce solutions without transparency into why particular buses are selected, reducing trust and transferability to different networks.
- **Caused by**: O4
- **Existing attempts**: None of the cited methods ([23]–[27]) incorporate engineering-driven bus classification.
- **Why they fail**: They treat the network as a black box, ignoring the electrical engineering principle that heavily loaded buses benefit most from local generation and compensation.

### G3: No deterministic framework with proven scalability
- **Statement**: Existing methods either are stochastic (non-reproducible) or tested only on small systems without evidence of computational efficiency at scale.
- **Caused by**: O4
- **Existing attempts**: CGO was previously applied without EVCS integration (Ref [28]); prior CGO lacked thermal capacity limits, CO2 calculation, and EV hosting factor analysis.
- **Why they fail**: Ref [28] covers DG+CB but omits EVCS entirely and does not study hosting factor impact.

## Key Insight
- **Insight**: Network buses can be classified by voltage sensitivity, active power demand, and reactive power demand before optimization, so resources are allocated only to the branches with highest need. This engineering-driven classification narrows the search space from all N buses to a small subset of high-load branches, enabling a deterministic, computationally efficient search that outperforms stochastic metaheuristics.
- **Derived from**: O1, O2, O3, O4, O5
- **Enables**: A Classification-based Global Optimization (CGO) framework that is deterministic (no randomness), computationally efficient (<29 s), interpretable (buses selected by engineering criteria), and capable of simultaneously placing DGs, CBs, and EVCSs under multiple EV hosting factors.

## Assumptions
- A1: Radial distribution network topology (unidirectional power flow in base case).
- A2: Two EVCSs, two DGs, and two CBs are assumed for each network; increasing the number of units would improve performance but increase capital cost.
- A3: DGs operate at unity power factor (reactive power support from DGs is not utilized in this study).
- A4: EV charging load is initially split equally between two stations but distributed at different levels at the final solution.
- A5: Steady-state peak loading scenario is used for annual energy loss estimation (multiplying by 8760 h/year); time-varying load profiles are not considered.
- A6: Constant load power at each interval; no stochastic DG generation profiles.
- A7: Network bus classification based on known load values ensures no misclassification risk.
