# Experiments / Studies

## E01: WGAN-GP Scenario Generation Validation
- **Type**: Generative model validation
- **Purpose**: Verify that the WGAN-GP model generates wind–solar output scenarios with distributional consistency to historical data.
- **Setup**: Real measured wind and PV output data used as baseline samples. WGAN-GP model learns the joint wind–solar output distribution. Generated samples compared to historical samples via CDF plots.
- **Evaluation**: Visual comparison of cumulative distribution functions (CDFs) of generated vs. real samples for both wind and PV power outputs.
- **Results**: The CDF curves of generated samples closely match those of historical data, confirming accurate capture of fluctuation characteristics and distributional properties. K-medoids clustering then extracts 4 representative scenarios (optimal cluster count determined by Silhouette Coefficient).

## E02: Uncertainty Impact Analysis
- **Type**: Comparative planning study
- **Purpose**: Evaluate the impact of considering wind–solar output uncertainty on ADN planning outcomes.
- **Setup**: Two planning schemes compared — (1) planning with WGAN-GP-based uncertainty scenarios, and (2) planning without considering uncertainty (deterministic).
- **Evaluation**: Comparison of annual total cost and component-wise costs (feeder, substation, E-SOP, PV, wind investment, electricity purchase, O&M, curtailment penalty).
- **Results**: Planning with uncertainty increases total cost marginally while improving operational flexibility and robustness through enhanced allocation of flexible resources and DG. Deterministic planning can serve as a practical approximation when uncertainty impact is small.

## E03: E-SOP Configuration Comparison
- **Type**: Comparative configuration study
- **Purpose**: Verify the economic efficiency and flexibility of the proposed E-SOP coordinated planning model vs. alternative flexible resource configurations.
- **Setup**: Three configuration schemes compared — (a) SOP-only (no energy storage), (b) BESS-only (no SOP), (c) E-SOP (proposed, integrating both SOP and BESS).
- **Evaluation**: Comparison of investment + O&M cost, electricity purchase cost, curtailment penalty cost, and annual total cost across the three schemes.
- **Results**: E-SOP configuration achieves the lowest total cost and eliminates renewable curtailment entirely, despite higher upfront investment. The improved spatiotemporal flexibility enables greater local renewable utilization and reduced grid dependence.

## E04: SCCR Algorithm Performance Comparison
- **Type**: Algorithm performance study
- **Purpose**: Evaluate the effectiveness and computational performance of the proposed SCCR algorithm vs. conventional convex–concave programming (CCP).
- **Setup**: Both algorithms applied to the same ADN expansion planning model with E-SOP integration. Convergence process tracked over iterations.
- **Evaluation**: Comparison of annual total cost (solution accuracy), number of iterations to convergence, computation time, and convex relaxation gap.
- **Results**: Both algorithms achieve identical total cost, confirming solution accuracy. The proposed SCCR converges in significantly fewer iterations and shorter computation time, with the relaxation gap reduced to a very small threshold.

## E05: Planning Results Visualization
- **Type**: Case study demonstration
- **Purpose**: Illustrate the optimal substation expansion and feeder layout scheme produced by the proposed method.
- **Setup**: The proposed planning model solved on the 54-bus ADN test system, producing optimal siting and sizing decisions for substations, feeders, DG, and E-SOP devices.
- **Evaluation**: Visual inspection of the resulting network topology showing existing/new feeders, existing/new substations, PV installations, wind power installations, and E-SOP locations.
- **Results**: The proposed method produces a feasible network topology that integrates all resource types with coordinated spatial deployment.
