# Experiments

## E01: Scenario 1 — Drought / Limited Hydroelectric Availability
- **Objective**: Evaluate dispatch optimization under reduced water availability for hydroelectric plants.
- **System**: 4 hydraulically coupled hydroelectric plants, 5 thermoelectric plants, 6 photovoltaic solar plants, 1 wind farm.
- **Water inflow**: Drought conditions (low natural water inflow as shown in Figure 7b).
- **Demand**: 24-hour profile (Figure 4).
- **Algorithms compared**: DE (F=0.8, CR=0.9, 1000 iter), PSO (inertia [0.55,1.1]), GWO (20 agents, 2000 iter), CA (pop=50, alpha=0.3, beta=0.5, paccept=0.35).
- **Constraint penalties**: pen1=20 (DE/PSO/CA), pen1=30 (GWO); pen2=360 (all).
- **Repetitions**: 2 independent runs per algorithm.
- **Results reported**: Best cost, avg cost, worst cost, best iteration, best cost time, avg time, function evaluations.
- **Evidence**: Table 10, Table 11, Figures 8, 9, 10, 11.

## E02: Scenario 2 — High Water Availability
- **Objective**: Evaluate dispatch optimization under abundant hydroelectric generation capacity.
- **System**: Same as E01.
- **Water inflow**: High water availability (Figure 7a).
- **Demand**: Same 24-hour profile.
- **Algorithms**: Same four algorithms with identical parameter settings.
- **Results reported**: Same metrics as E01.
- **Evidence**: Table 12, Table 13, Figures 12, 13, 14, 15.

## E03: Sensitivity Analysis — Demand Variation +/-10%
- **Objective**: Test robustness of the dispatch model under demand uncertainty.
- **Procedure**: Total electrical demand modified by +/-10%; optimization repeated for all algorithms.
- **Key finding**: DE maintained best performance; cost variations within +/-4%.
- **Evidence**: Discussed in Section 6.4.

## E04: Monte Carlo Renewable Resource Forecasting
- **Objective**: Generate probabilistic forecasts of solar irradiance, wind speed, and temperature over a 24-hour horizon.
- **Data**: 5 years (2018-2022) of August hourly measurements.
- **Method**: PDF fitting (Weibull for wind/solar, GMM for temperature), 1000 Monte Carlo simulations per variable.
- **Output**: Mean, 10th and 90th percentile bounds for each resource.
- **Evidence**: Figures 1, 5, 6; Table 7.
