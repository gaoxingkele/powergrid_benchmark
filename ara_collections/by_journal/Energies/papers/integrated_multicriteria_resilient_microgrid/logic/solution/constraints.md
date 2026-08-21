# Constraints: Integrated Multi-Criteria Planning for Resilient VRE-Based Microgrid

## Boundary Conditions

1. **System configuration**: Community microgrid comprises only PV, wind turbine (WT), and battery energy storage (BESS). No diesel generator, fuel cell, or grid connection included. The system targets 100% VRE generation.

2. **Geographic scope**: Case study is an isolated community microgrid in Kenya (coordinates 2.3369N, 37.9904E). Techno-economic parameters (Table 1) and weather data are specific to this location.

3. **Planning horizon**: 8760 hours (one full year) with hourly resolution. The project lifetime is 20 years for NPV-based lifecycle cost calculations.

4. **Optimization approach**: Three-objective minimization (TLCC, DPSP, LPPP) using MOPSO with external repository and mutation operator. TOPSIS applied for final ranking of non-dominated solutions.

5. **Pricing structure**: Reference electricity price is 15.80 US cents/kWh (Kenyan Energy Regulatory Commission tariff). DRP price bounds: 50% to 200% of reference price.

6. **Flexible demand**: FDR capacity limited to +/-10% of system load at any time t. Price elasticity coefficients from Table 2.

7. **BESS constraints**: SOC range 10%-90% of rated capacity. Critical SOC threshold used to trigger VP-CPP mode. Charging/discharging limits determined by C-rate.

8. **Uncertainty modeling**: Monte Carlo with 50 scenarios generated within 25% MAE range from LSTM forecasts. MAE computed from Scikit-learn in Python.

## Assumptions

1. Demand response participation is voluntary; consumers may choose not to adjust consumption in response to price signals.

2. Price elasticity coefficients (Table 2) are assumed constant across all load levels and time periods.

3. The LSTM model's MAE is a sufficient indicator of uncertainty magnitude for MCS scenario generation.

4. All system components operate at their rated efficiency throughout the project lifetime (no degradation considered beyond derating factor).

5. The BESS replacement cost (every 10 years) equals the initial investment cost in real terms.

6. Inflation and discount rates are equal at 4%, simplifying real discount rate calculation.

7. The 50 MCS scenarios provide adequate coverage of the uncertainty space for robust planning decisions.

8. Critical events are unambiguously identified by the condition (SOC <= SOC_critical) AND (total VRE generation <= 0).

## Limitations

1. **Single case study**: Results are validated for only one geographic location (Kenya). Generalizability to other regions with different weather patterns, tariff structures, and load profiles is not established.

2. **No grid interaction**: The isolated microgrid assumption excludes the possibility of grid backup, power trading, or ancillary service provision, which could alter optimal planning decisions.

3. **Limited DRP types compared**: Only two DRP variants (TOU VP-CPP and SSAP VP-CPP) are compared. Other DRP variants (RTP, CPP-only, incentive-based) are not evaluated.

4. **No electric vehicle integration**: EV charging as a flexible demand resource is not considered, despite its growing relevance in microgrid contexts.

5. **Point forecasts only**: LSTM provides deterministic point forecasts without prediction intervals. Probabilistic forecasting could provide richer uncertainty information for risk-based decision making.

6. **No thermal or hydrogen storage**: Only BESS is considered. Other storage technologies (thermal storage, hydrogen, pumped hydro) are not evaluated.

7. **Single-objective ranking**: TOPSIS requires subjective weight assignment to objectives. Alternative multi-criteria methods (AHP, PROMETHEE, ELECTRE) could yield different rankings.

8. **No dynamic component degradation**: Component aging and capacity fade (particularly BESS) are modelled only through replacement timing, not through progressive performance degradation within each 10-year period.

9. **Computational scalability**: MOPSO performance for larger systems with more decision variables or finer temporal resolution is not investigated.

10. **No model validation against real operation**: The proposed planning results are not validated against actual microgrid operational data, as the study is simulation-based using historical data.
