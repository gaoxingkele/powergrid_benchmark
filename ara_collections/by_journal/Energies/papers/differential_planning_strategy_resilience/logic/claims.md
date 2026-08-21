# Claims

## C01: DDU-based multi-level hardening reduces worst-case total cost compared to single-level hardening under extreme weather.

- **Statement**: Modeling the decision-dependent relationship between hardening level and line failure probability reduces worst-case expected total cost (load shedding + generation + purchased electricity) compared with traditional single-level (binary) hardening models, because the multi-level framework allocates reinforcement resources more flexibly across graduated hardening levels.
- **Conditions**: When the hardening budget is limited (CNY 1.2 million in the study) and at least two hardening levels exist. Does not apply when budget is unlimited (all lines can be hardened to max level).
- **Sources**:
  - Page 15: "When considering the probability of line failure, the total cost of the DDU model is reduced by CNY 2.37 million compared with the traditional reinforcement model."
  - Page 21: "The DDU-based multi-level line hardening model... achieves a maximum cost reduction of approximately CNY 8.553 million."
- **Status**: Supported by simulation evidence in the paper.
- **Falsification criteria**: A planning case where total cost of the DDU model exceeds that of the single-level model under the same budget and disaster scenarios would falsify this claim.
- **Proof**: E01 (Comparison of Case 1 vs. Case 2 - DDU vs non-DDU); E02 (Five-case comparative analysis).
- **Evidence basis**: Table 2, Table 3, Table 9 — total cost comparisons across cases.
- **Dependencies**: C02 (coordination of multiple resilience measures contributes to cost reduction); Assumption 2 (no repair).
- **Tags**: #DDU #multi-level-hardening #cost-reduction

## C02: Coordinated optimization of MEGs, EVs, demand response, network reconfiguration, and line hardening reduces loss-of-load cost more than any single measure alone.

- **Statement**: The synergistic deployment of mobile emergency generators, vehicle-to-grid-capable electric vehicles, demand response programs, network reconfiguration (tie-line switching), and multi-level line hardening yields lower loss-of-load cost than applying any subset of these measures in isolation, because each measure addresses a different dimension of the post-disaster supply-demand gap.
- **Conditions**: When the system includes at least one MEG station, EV charging stations willing to participate in V2G, and at least one tie line for reconfiguration. The DRO uncertainty set is active (Case 5).
- **Sources**:
  - Page 15: "By comparing Cases 3 and 4... the combined measures of demand response, EVs, and MEGs effectively reduce load shedding. The overall load loss rate decreases from 50.64% in Case 3 to 36.91% in Case 4."
  - Page 21: "Compared with other flexible-resource coordination strategies, the average cost reduction reaches 16.89%."
- **Status**: Supported by simulation evidence across Cases 1-5.
- **Falsification criteria**: A case where adding one of these measures increases total cost (e.g., MEG operating cost exceeding the load-shedding penalty it avoids) would partially falsify this claim.
- **Proof**: E02 (Five-case comparative analysis); E03 (Sobol' sensitivity analysis revealing interaction effects).
- **Evidence basis**: Table 2 (costs and reinforcement strategies across cases), Table 9 (IEEE 123-bus results).
- **Dependencies**: C01 (DDU model enables the multi-level hardening component); Assumptions 3, 6.
- **Tags**: #coordinated-optimization #resilience-measures #V2G #demand-response

## C03: Distributionally robust optimization (DRO) with norm-bounded ambiguity sets provides a financial insurance policy against worst-case disaster scenarios.

- **Statement**: While the DRO model produces slightly higher total cost under nominal conditions, it reduces worst-case total cost compared to a deterministic model that ignores distributional ambiguity, because the DRO formulation biases the hardening strategy toward scenarios with severe damage that the deterministic model would underweight.
- **Conditions**: When at least one ambiguity set parameter (alpha_1 or alpha_infinity) is set below 0.99 and historical data M is finite (making the true distribution uncertain). When the worst-case scenario is not already covered by the deterministic solution.
- **Sources**:
  - Page 16: "Although the total cost of the distributionally robust optimization model is slightly higher than that of the deterministic model, when considering the worst-case scenario, the total cost of Case 5 is lower than that of Case 4."
  - Page 16: "DRO... effectively provides a financial insurance policy against high-impact and highly uncertain disaster scenarios."
- **Status**: Supported by simulation evidence (Table 3 comparison of Case 4 vs Case 5).
- **Falsification criteria**: A case where the DRO model exhibits higher cost in both nominal and worst-case scenarios compared to the deterministic model would falsify this claim.
- **Proof**: E04 (DRO vs deterministic comparison); E05 (Confidence set sensitivity analysis).
- **Evidence basis**: Table 3 (Case 4 vs Case 5 cost comparison), Table 6 (confidence parameter sensitivity).
- **Dependencies**: C01 (DDU-hardening enables the effect); Assumption 5 (initial probability distribution).
- **Tags**: #DRO #ambiguity-set #worst-case #insurance-effect

## C04: Variance-based sensitivity analysis reveals that the marginal resilience contribution of line hardening shifts from main-feeders to secondary lines as the investment budget grows, following a "core-first, then broader-coverage" trajectory.

- **Statement**: The Sobol' first-order index of a line's hardening level represents the direct marginal contribution of that specific investment to overall system resilience. Under constrained budgets, the highest-ranked lines by Si are those whose failure isolates the largest load share (typically upstream feeders and tie lines to critical load clusters). As the budget expands, the Si ranking broadens to secondary lines serving areas with critical loads, revealing a transition from a single-bottleneck pattern to multi-point collaborative resilience improvement.
- **Conditions**: When the resilience index captures expected load supply capability. The Si ranking is budget-dependent and changes monotonically from main-feeder-dominated at low budgets to more distributed at high budgets. The total-effect index STi must also be examined to capture interaction effects with other operational decisions.
- **Sources**:
  - Page 18: "At low budgets (12-15), the main feeder lines 1-2 and 2-3 and the key tie line 31-32 exhibit the highest contributions."
  - Page 19: "By comparing with the total-effect indices in Table 7, it is observed that ST values of lines 31-32 and 32-33 are significantly higher than their first order indices, implying strong interactions."
- **Status**: Supported by Sobol' analysis results in Figure 6 and Table 7.
- **Falsification criteria**: A case where the Sobol' Si ranking remains identical across all budget levels (no transition in investment trajectory) would contradict the "core-first, then broader-coverage" pattern.
- **Proof**: E03 (Sobol' sensitivity analysis).
- **Evidence basis**: Figure 6 (first-order Sobol' contributions across budgets), Table 7 (total-effect Sobol' indices at budget 24).
- **Dependencies**: C01 (DDU model ensures failure probability responds to hardening decisions); Assumption 4 (vulnerability curves known).
- **Tags**: #Sobol #sensitivity-analysis #reinforcement-prioritization #interpretability

## C05: Fault-state pruning that retains only the highest-weighted failure scenarios reduces solution time dramatically while preserving planning accuracy, because low-impact scenarios have negligible influence on the optimal hardening decision.

- **Statement**: Discarding a tail of low-weighted fault states via a threshold on cumulative weighted load loss reduces the combinatorial complexity of the C&CG algorithm without materially affecting the optimal hardening strategy, because the optimization objective is dominated by the high-impact scenarios. The accuracy-loss curve is nonlinear: pruning the first few lowest-impact states is nearly lossless, but further pruning eventually drops scenarios that would have altered the optimal decision, causing accuracy to degrade rapidly.
- **Conditions**: When the distribution of fault-state weighted load loss is sufficiently heavy-tailed (a small number of states account for most of the loss). The pruning ratio alpha_cut must be set to retain the long head (e.g., alpha_cut = 0.95). Reducing to fewer than a minimum number of states (e.g., fewer than 3 from a set of 9) degrades accuracy unacceptably.
- **Sources**:
  - Page 19-20: "When three failure states are reduced, the error is 1.00%. The computation time is shortened by 73.22%."
  - Page 20: "Overall, reducing two or three failure states maintains the error within 1.00%."
- **Status**: Supported by simulation evidence in Table 8.
- **Falsification criteria**: A case where pruning the lowest-weighted states yields error > 5% for the same pruning ratio (e.g., alpha_cut = 0.95) would falsify the claim that accuracy is preserved. Similarly, if the heavy-tailed assumption does not hold (all states have similar weight), pruning would always cause large errors.
- **Proof**: E06 (Scenario reduction computational efficiency).
- **Evidence basis**: Table 8 (cost error and solve time for different reduction schemes).
- **Dependencies**: Assumption 6 (Monte Carlo sampling of disaster scenarios).
- **Tags**: #scenario-reduction #computational-efficiency #fault-state-pruning
