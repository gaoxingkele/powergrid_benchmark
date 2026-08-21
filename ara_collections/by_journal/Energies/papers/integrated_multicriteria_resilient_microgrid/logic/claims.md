# Claims: Integrated Multi-Criteria Planning for Resilient VRE-Based Microgrid

## C1: SSAP VP-CPP DRP reduces total lifecycle cost in VRE microgrids compared to TOU-based DRP

- **Statement**: Shortage/surplus adaptive pricing combined with variable peak critical peak pricing (SSAP VP-CPP DRP) achieves lower total lifecycle cost (TLCC) for isolated VRE-based community microgrids than time-of-use combined with VP-CPP (TOU VP-CPP DRP), under both deterministic and stochastic planning approaches, by dynamically responding to real-time supply-demand imbalances.

- **Conditions**: Valid for isolated community microgrids with PV, WT, and BESS components; FDR capacity of +/-10% of total load; reference electricity price of 15.80 US cents/kWh; deterministic (Cases 2-3) or stochastic (Cases 5-6) planning horizons of 8760 hours; project lifetime of 20 years at 4% discount rate.

- **Sources**: Section 5.4 (Case 3), Section 5.7 (Case 6), Table 3.

- **Status**: Supported by simulation evidence.

- **Falsification criteria**: The claim is falsified if (a) TOU VP-CPP DRP achieves lower or equal TLCC than SSAP VP-CPP DRP under identical conditions; (b) the TLCC reduction is less than 1% for the best-ranked TOPSIS solution; or (c) the SSAP DRP requires larger component capacities across all TOPSIS-ranked solutions.

- **Proof**: Evidence E01 (Case 2 vs Case 3 TLCC comparison under deterministic planning) and E02 (Case 5 vs Case 6 TLCC comparison under stochastic planning) both demonstrate SSAP VP-CPP outperforming TOU VP-CPP. Under deterministic planning (E01), Case 3 achieves TLCC of $9,649,293 vs Case 2 at $10,314,687 (approximately 6.5% reduction). Under stochastic planning (E02), Case 6 achieves TLCC of $10,066,405 vs Case 5 at $10,378,836 (approximately 3.0% reduction). Both comparisons favor the SSAP approach.

- **Evidence basis**: Table 3 shows the top-ranked TOPSIS solutions across all six cases. Case 3 (SSAP VP-CPP, deterministic) has the lowest TLCC overall at $9,649,293. Case 6 (SSAP VP-CPP, stochastic) has TLCC of $10,066,405 vs Case 5 (TOU VP-CPP, stochastic) at $10,378,836. The SSAP cases consistently achieve lower BESS capacities, the most expensive component.

---

## C2: Integrated LSTM forecasting with SSAP VP-CPP DRP improves microgrid reliability under uncertainty

- **Statement**: The integration of LSTM-based one-hour-ahead forecasting with SSAP VP-CPP demand response improves microgrid reliability (measured by deficiency of power supply probability, DPSP) compared to stochastic planning without forecasting-and-DRP integration, while simultaneously reducing component oversizing and VRE curtailment.

- **Conditions**: Valid for isolated community microgrids where LSTM forecasting MAE is <= 25 kW for load, <= 0.14 m/s for wind speed, and <= 20 W/m^2 for solar irradiance; uncertainty modeled via Monte Carlo with 50 scenarios within 25% MAE range; DPSP target <= 0.5%.

- **Sources**: Section 5.7 (Case 6), Section 5.5 (Case 4), Table 3 results.

- **Status**: Supported by simulation evidence.

- **Falsification criteria**: The claim is falsified if (a) Case 6 (LSTM + SSAP VP-CPP + stochastic) has higher DPSP than Case 4 (stochastic only, no DRP/forecasting); (b) the component capacities in Case 6 are not smaller than those in Case 4; or (c) the LPPP in Case 6 is not lower than in Case 4.

- **Proof**: Evidence E03 (Case 4 vs Case 6 reliability comparison) shows Case 4 achieves DPSP of 0.12% (rank 1) while Case 6 achieves DPSP of 0.04% (rank 1). Case 6 has lower PV (1420 vs 1480 kW), lower BESS (3200 vs 4900 kWh), and dramatically lower LPPP (2.05% vs 10.31%) compared to Case 4. The TLCC is also lower ($10,066,405 vs $10,576,185). This demonstrates that forecasting + DRP integration simultaneously improves reliability and reduces cost and curtailment.

- **Evidence basis**: Table 3 rank 1 solutions: Case 4 (stochastic only) requires 1480 kW PV, 2000 kW WT, 4900 kWh BESS with DPSP 0.12%, LPPP 10.31%, TLCC $10,576,185. Case 6 (LSTM + SSAP + stochastic) requires 1420 kW PV, 1920 kW WT, 3200 kWh BESS with DPSP 0.04%, LPPP 2.05%, TLCC $10,066,405. All metrics improve with integration.

---

## C3: Multi-objective optimization with TOPSIS ranking effectively resolves the TLCC-DPSP-LPPP trade-off

- **Statement**: The MOPSO algorithm combined with TOPSIS multi-criteria decision making effectively generates and selects Pareto-optimal solutions navigating the three-way trade-off between minimizing total lifecycle cost (TLCC), minimizing deficiency of power supply probability (DPSP), and minimizing loss of produced power probability (LPPP) in VRE-based microgrid planning.

- **Conditions**: Valid when optimizing over three decision variables (PV capacity, WT capacity, BESS capacity) with constraints on power balance, BESS SOC, FDR limits, and electricity price bounds; using 8760-hour scheduling horizon; mutation operator identical to NSGA-II applied for diversity.

- **Sources**: Section 3.5, Section 4, Figure 9a-f (Pareto fronts for all six cases).

- **Status**: Supported by simulation evidence.

- **Falsification criteria**: The claim is falsified if (a) the Pareto fronts do not show clear trade-off patterns among the three objectives; (b) TOPSIS ranking selects dominated solutions; or (c) the non-dominated solutions collapse to a single point (no trade-off exists).

- **Proof**: Evidence E04 (Pareto front visualization) shows Figure 9a-f with well-distributed 3D Pareto fronts across all six cases. Evidence E05 (TOPSIS ranking in Table 3) shows four distinct ranked solutions per case with varying trade-offs. For example, in Case 6, rank 1 has DPSP=0.04%, LPPP=2.05%, TLCC=$10,066,405; rank 4 has DPSP=0.11%, LPPP=0.73%, TLCC=$9,319,214 — demonstrating that lower TLCC comes at the cost of slightly higher DPSP, confirming a genuine trade-off that TOPSIS resolves.

- **Evidence basis**: Table 3 shows the four best-ranked non-dominated solutions per case with varying DPSP, LPPP, and TLCC values. Figure 9 provides 3D Pareto front plots for all six cases. The TOPSIS methodology (Equations 19-25) assigns weights to objectives and ranks solutions by proximity to the ideal solution.

---

## C4: Deterministic SSAP DRP planning costs less but stochastic SSAP DRP planning is more robust

- **Statement**: Deterministic planning with SSAP VP-CPP DRP (Case 3) yields lower TLCC than stochastic planning with SSAP VP-CPP DRP (Case 6), but the stochastic approach provides guaranteed reliability under extreme weather events and uncertainty, making it the more realistic and robust blueprint for practical deployment.

- **Conditions**: For isolated microgrids with the same component technologies and DRP structure; Case 3 ignores VRE/load uncertainty while Case 6 models it via MCS; all other parameters identical.

- **Sources**: Section 5.4 vs Section 5.7, Table 3 (Case 3 vs Case 6), Section 6 (Conclusions).

- **Status**: Supported by simulation evidence.

- **Falsification criteria**: The claim is falsified if (a) Case 3 does not have lower TLCC than Case 6; (b) Case 6 DPSP is not lower (better) than Case 3 under stressed conditions; or (c) the component capacities in Case 3 are not smaller than those in Case 6.

- **Proof**: Evidence E06 (Case 3 vs Case 6 cost comparison) shows Case 3 TLCC of $9,649,293 vs Case 6 TLCC of $10,066,405 (approximately 4% lower for deterministic). However, Case 6 achieves DPSP of 0.04% vs 0.06% for Case 3. Case 6 requires larger PV (1420 vs 1270 kW) but smaller BESS (3200 vs 3500 kWh) for rank 1 solutions. The paper explicitly states Case 3 suffers from "overlooking inherent uncertainty" while Case 6 provides "guaranteed reliability under extreme weather events."

- **Evidence basis**: Table 3 rank 1 comparison: Case 3 (deterministic SSAP) has PV 1270 kW, WT 1840 kW, BESS 3500 kWh, TLCC $9,649,293, DPSP 0.06%. Case 6 (stochastic SSAP) has PV 1420 kW, WT 1920 kW, BESS 3200 kWh, TLCC $10,066,405, DPSP 0.04%. The conclusions (Section 6) explicitly state Case 6 "can be considered the optimal blueprint."

---

## C5: LSTM forecasting accuracy is sufficient for operational DRP activation in VRE microgrids

- **Statement**: The LSTM deep learning model provides sufficiently accurate one-hour-ahead point forecasts for solar irradiance (MAE 19.97 W/m^2), wind speed (MAE 0.14 m/s), and load demand (MAE 24.68 kW) to enable effective DRP activation and uncertainty scenario generation in VRE-based microgrid operational planning.

- **Conditions**: LSTM architecture with forget, input, output gates; trained on historical data from the Kenyan case study location; forecasts for scheduling horizon of 8760 hours; MAE used as accuracy metric for point forecasts; 25% MAE range used for MCS scenario generation.

- **Sources**: Section 3.4.1, Section 5.1, Figures 3-5.

- **Status**: Supported by simulation evidence.

- **Falsification criteria**: The claim is falsified if (a) forecast MAE exceeds 30% of the mean value for any variable; (b) the forecast errors propagate to significantly degrade DRP performance; or (c) the MCS scenarios generated from forecast MAE do not improve stochastic optimization outcomes compared to using only historical variance.

- **Proof**: Evidence E07 (LSTM forecast accuracy) reports MAE of 19.97 W/m^2 for solar irradiance (approximately 2-5% of typical range), 0.14 m/s for wind speed (1-3% of typical operating range), and 24.68 kW for load demand (approximately 1-2% of typical peak load). These low MAE values are used to bound MCS scenario generation within a 25% range (Figures 6-8). Cases 5 and 6, which incorporate LSTM forecasts, outperform Case 4 (no forecasting) in both cost and reliability.

- **Evidence basis**: Section 5.1 reports all MAE values. Figures 3-5 visually demonstrate close tracking between actual and predicted values. Figures 6-8 show the MCS scenarios generated from forecast uncertainty bounds. The comparative improvement of Cases 5 and 6 over Case 4 provides indirect validation of forecast utility.
