# Experiments: Integrated Multi-Criteria Planning for Resilient VRE-Based Microgrid

## E01: Deterministic DRP comparison — TOU VP-CPP vs SSAP VP-CPP (Cases 2 & 3)

- **Verifies**: C1 (SSAP VP-CPP DRP reduces TLCC compared to TOU-based DRP)
- **Evidence**: Table 3 (Case 2 rank 1 vs Case 3 rank 1), Section 5.3, Section 5.4, Figure 9b-c
- **Run**: MATLAB simulation using MOPSO-TOPSIS on the Kenyan case study microgrid with 8760-hour deterministic scheduling horizon, no uncertainty modeling.
- **Setup**: Case 2 applies TOU VP-CPP DRP with three static pricing periods (peak at 150%, off-peak at 100%, low peak at 50% of reference, critical at 200%). Case 3 applies SSAP VP-CPP DRP with dynamic pricing based on power imbalance. Both use identical techno-economic parameters (Table 1) and FDR capacity (+/-10% of load). Decision variables: PV, WT, BESS capacities. Three objectives: minimize TLCC, DPSP, LPPP.
- **Procedure**: Run MOPSO for each case to generate Pareto front of non-dominated solutions. Apply TOPSIS to rank solutions. Compare top-ranked solutions across cases. Extract TLCC, DPSP, LPPP, and component capacities.
- **Expected outcome**: Case 3 (SSAP VP-CPP) should achieve lower TLCC than Case 2 (TOU VP-CPP) due to dynamic pricing enabling better FDR utilization and reduced BESS dependency. BESS capacity should be notably smaller in Case 3.

## E02: Stochastic DRP comparison — TOU VP-CPP vs SSAP VP-CPP with LSTM forecasting (Cases 5 & 6)

- **Verifies**: C1 (SSAP VP-CPP DRP reduces TLCC), C2 (LSTM + SSAP improves reliability)
- **Evidence**: Table 3 (Case 5 rank 1 vs Case 6 rank 1), Section 5.6, Section 5.7, Figure 9e-f
- **Run**: MATLAB simulation using MOPSO-TOPSIS with MCS uncertainty scenarios. LSTM forecasting implemented in Python (Scikit-learn) to generate forecast MAE, then MCS generates 50 scenarios within 25% MAE range for wind speed, solar irradiance, and load demand.
- **Setup**: Case 5 combines TOU VP-CPP DRP with LSTM forecasting and MCS uncertainty scenarios. Case 6 combines SSAP VP-CPP DRP with LSTM forecasting and MCS scenarios. Both use identical uncertainty modeling parameters. FDR capacity +/-10%.
- **Procedure**: Generate 50 MCS scenarios for each stochastic parameter based on LSTM forecast MAE. Run MOPSO for each case across all scenarios. Apply TOPSIS for ranking. Extract and compare top-ranked TLCC, DPSP, LPPP, and component sizes.
- **Expected outcome**: Case 6 (SSAP + LSTM) should achieve lower TLCC, lower DPSP, and lower LPPP than Case 5 (TOU + LSTM). The adaptive pricing should more effectively match FDR activation to VRE availability. BESS capacity should be smaller in Case 6.

## E03: Robustness comparison — Stochastic without DRP (Case 4) vs integrated LSTM + SSAP (Case 6)

- **Verifies**: C2 (LSTM + SSAP improves reliability under uncertainty)
- **Evidence**: Table 3 (Case 4 rank 1 vs Case 6 rank 1), Section 5.5, Section 5.7
- **Run**: MATLAB simulation comparing pure stochastic planning (Case 4: uncertainty only, flat pricing, no forecasting) against fully integrated planning (Case 6: LSTM forecasting + SSAP VP-CPP DRP + MCS uncertainty). Both use 50 MCS scenarios.
- **Setup**: Case 4 uses flat reference pricing ($0.158/kWh) with no DRP and no forecasting. Case 6 uses SSAP VP-CPP DRP with LSTM forecasting. Uncertainty modeling identical (50 MCS scenarios from same data).
- **Procedure**: Run MOPSO-TOPSIS for each case. Compare top-ranked component capacities, TLCC, DPSP, and LPPP.
- **Expected outcome**: Case 6 should have dramatically lower component capacities (especially BESS), lower TLCC, lower LPPP, and comparable or better DPSP. The integration of forecasting and DRP should substitute for hardware oversizing.

## E04: Multi-objective Pareto front analysis

- **Verifies**: C3 (MOPSO-TOPSIS resolves TLCC-DPSP-LPPP trade-off)
- **Evidence**: Figure 9a-f (Pareto fronts for all six cases), Table 3 (ranked solutions)
- **Run**: Analysis of MOPSO output across all six simulation cases.
- **Setup**: Each case produces a 3D Pareto front in TLCC-DPSP-LPPP space. TOPSIS ranks the non-dominated solutions.
- **Procedure**: Visualize and compare Pareto fronts across cases. Examine the spread of non-dominated solutions. Analyze TOPSIS ranking consistency.
- **Expected outcome**: All six cases should show well-distributed Pareto fronts spanning the trade-off space. Lower TLCC solutions should generally have higher DPSP and/or higher LPPP. TOPSIS should rank solutions with balanced performance highest.

## E05: Deterministic vs stochastic SSAP comparison (Case 3 vs Case 6)

- **Verifies**: C4 (Deterministic SSAP costs less but stochastic SSAP is more robust)
- **Evidence**: Table 3 (Case 3 rank 1 vs Case 6 rank 1), Section 5.4, Section 5.7
- **Run**: Comparison of deterministic SSAP VP-CPP (Case 3, no uncertainty) vs stochastic SSAP VP-CPP (Case 6, with MCS uncertainty and LSTM forecasting).
- **Setup**: Both cases use SSAP VP-CPP DRP. Case 3 ignores all uncertainty. Case 6 models VRE and load uncertainty via 50 MCS scenarios and incorporates LSTM forecasting.
- **Procedure**: Compare TLCC, DPSP, LPPP, and component capacities. Evaluate the cost premium of stochastic planning.
- **Expected outcome**: Case 3 should have lower TLCC (cost savings from ignoring uncertainty) but higher DPSP vulnerability under stressed conditions. Case 6 should have higher TLCC but guaranteed reliability and more realistic planning. Component capacities should be larger in Case 6 for PV and WT but not necessarily BESS.
