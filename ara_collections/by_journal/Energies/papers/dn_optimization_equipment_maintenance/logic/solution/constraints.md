# Constraints

## Boundary Conditions

1. **Network topology:** The model assumes radial or weakly meshed distribution network structure compatible with Disflow power flow formulation. Not validated for highly meshed transmission networks [Source: Page 3, Section 2.1].

2. **System size:** Validated on CPS62-node system (62 nodes, 3 sub-grids). Scalability to systems with hundreds or thousands of nodes is unverified [Source: Page 9, Section 3].

3. **Time horizon:** The optimization is formulated for a discrete-time dispatch horizon T. Continuous-time dynamics and transient stability are not modeled [Source: Pages 3-5, Equations (1)-(15)].

4. **Resource types considered:** PV, wind, gas turbines, energy storage systems, and transferable loads. Other flexible resources (electric vehicles, heat pumps, electrolyzers) are not explicitly modeled [Source: Page 5, Equation (12)-(15)].

5. **Uncertainty sources:** Renewable generation (wind, PV) and load demand. Equipment failures, communication delays, and cyber-physical risks are mentioned but not modeled quantitatively [Source: Page 12, Section 3.2; Page 16, Future Work].

## Assumptions

1. **Data availability:** Historical or forecasted renewable and load profiles are available with sufficient accuracy [Source: Page 15, Section 4].

2. **Controllability:** Centralized coordination and controllability of all distributed resources (flexible loads, storage, distributed generation) is achievable [Source: Page 15, Section 4].

3. **Topology controllability:** Grid topology and equipment constraints are known and controllable through switchable branches [Source: Page 15, Section 4].

4. **Computational resources:** Sufficient computational resources exist to solve the bilevel optimization problem offline or in near real-time [Source: Page 15, Section 4].

5. **Uncertainty structure:** Renewable generation uncertainty can be adequately characterized by historical data-based scenario generation (Latin Hypercube Sampling) and K-means-like clustering [Source: Page 5, Section 2.2].

6. **Convex relaxation accuracy:** The big-M convex relaxation of Disflow power flow (Equation 6) provides sufficient accuracy for distribution network optimization [Source: Pages 3-4, Equations (3)-(6)].

7. **Single-phase modeling:** The model uses a single-phase Disflow formulation, not a full three-phase unbalanced power flow. This is a standard simplification for medium-voltage distribution networks but may not capture phase imbalance effects [Source: Page 3, Section 2.1].

## Known Limitations

1. **Algorithmic scalability:** "The hybrid metaheuristic algorithm offers effective global and local search capability, it may encounter scalability challenges when applied to ultra-large distribution systems or real-time operation scenarios." [Source: Page 16, Section 5]

2. **Data dependency:** "The proposed model relies on the availability and accuracy of historical data for renewable generation and load profiles, which may limit reliability in data-sparse regions." [Source: Page 16, Section 5]

3. **Centralized coordination assumption:** "The optimization framework assumes centralized coordination and controllability of distributed resources, which may not always be achievable due to infrastructure constraints." [Source: Page 16, Section 5]

4. **Predictive maintenance validation:** The claim of supporting predictive maintenance is discussed qualitatively in Section 4 but lacks quantitative validation with equipment health metrics or maintenance cost data [Source: Pages 14-15, Section 4].

5. **No cyber-physical risk modeling:** Communication delays, sensor failures, and cyber attacks are not modeled in the current framework, though identified as future work [Source: Page 16, Future Work].

6. **No behavioral uncertainty:** Demand-side behavioral uncertainty and user response variability are not incorporated [Source: Page 16, Future Work].
