# Experiments

## E01: Probabilistic Operating Scenario Construction
- **Objective**: Construct a comprehensive scenario matrix capturing all combinations of wind power output, solar power output, and load demand states for reliability assessment.
- **Method**: Discretize probability density functions (normal for load, beta for solar irradiance, Weibull for wind speed) into representative states. Multiply individual state probabilities to obtain joint scenario probabilities.
- **Evaluation**: Verify that the scenario matrix covers the full range of operating conditions and that state probabilities sum to unity.
- **Expected Outcome**: A probabilistic scenario library feeding into the reliability assessment module.
- **Related Claims**: C03

## E02: Reinforcement Planning Optimization with GA
- **Objective**: Solve the reliability-constrained reinforcement planning optimization problem using the GA-based metaheuristic.
- **Method**: Encode decisions (tie line selection, NO switch placement, feeder upgrade alternatives, substation upgrade alternatives, investment timing) into chromosomes. Apply penalty for reliability constraint violations. Evolve population over generations to minimize NPV objective function.
- **Evaluation**: Convergence analysis of GA; comparison of best-found solution to baseline (no reinforcement).
- **Expected Outcome**: Optimal set of reinforcement investments across the planning horizon.
- **Related Claims**: C01, C04, C05

## E03: Case Study 1 -- Reinforcement with Controllable DGs Only
- **Objective**: Evaluate the proposed planning framework on a 54-bus distribution system where only dispatchable/controllable DGs (CDGs) are available.
- **Method**: Apply the GA-based optimization to determine optimal tie lines, NO switches, feeder upgrades, and substation upgrades to meet SAIDI <= 2.5 h/year and ENS <= 5 MWh/year per bus targets over the 15-year planning horizon (3 stages, 3% load growth).
- **Evaluation**: Compare pre- and post-reinforcement SAIDI and ENS values at each bus and stage. Calculate total NPV and individual cost components.
- **Expected Outcome**: Quantified improvements in reliability indices; investment cost breakdown.
- **Related Claims**: C04

## E04: Case Study 2 -- Reinforcement with CDG, Wind, and PV
- **Objective**: Evaluate the proposed framework when both dispatchable and renewable (wind, PV) DGs are integrated, introducing generation intermittency uncertainty.
- **Method**: Include probabilistic wind and PV output modeling in the scenario matrix. Apply the same GA optimization to determine required reinforcements.
- **Evaluation**: Compare pre- and post-reinforcement reliability indices. Compare required investments with Case Study 1 to assess the impact of renewable DG support.
- **Expected Outcome**: Quantified improvements in reliability indices with renewable DG; comparison of investment requirements (tie lines, feeders) between the two cases.
- **Related Claims**: C05

## E05: Sensitivity Analysis and Framework Validation
- **Objective**: Validate the hierarchical contingency recovery strategy by analyzing specific contingency scenarios and demonstrating the two success modes (restoration and islanding).
- **Method**: Examine specific fault cases (e.g., feeders 1-9 and 33-34 for Case 1; feeders 9-22 and 7-8 for Case 2) and verify the decision logic for selecting restoration vs. islanding.
- **Evaluation**: Confirm that operational limits (voltage, thermal, substation capacity) are respected in both success modes.
- **Expected Outcome**: Demonstrated effectiveness of the two-level hierarchy for different contingency types.
- **Related Claims**: C02, C03
