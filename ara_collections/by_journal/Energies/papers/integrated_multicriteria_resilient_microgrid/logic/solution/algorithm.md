# Algorithm: MOPSO-TOPSIS for Integrated Multi-Criteria Microgrid Planning

## Purpose

The MOPSO-TOPSIS algorithm jointly optimizes capacity sizing (PV, WT, BESS capacities) and operational planning (pricing decisions, FDR activation, BESS scheduling) for a VRE-based community microgrid under three conflicting objectives: minimize TLCC (economic), minimize DPSP (reliability), and minimize LPPP (utilization efficiency).

## Inputs

- Techno-economic parameters (Table 1): investment costs, O&M costs, lifetimes, efficiencies
- Weather data: hourly wind speed, solar irradiance, temperature
- Load demand profile: hourly time series
- DRP parameters: price bounds, FDR capacity limits, elasticity coefficients (Table 2)
- MOPSO parameters: swarm size, iterations, inertia weight range, mutation rate
- LSTM forecast model (pre-trained): MAE for each variable
- MCS parameters: number of scenarios (50), uncertainty range (25% MAE)

## Core Steps

1. **LSTM Forecasting**: Train LSTM on historical data. Compute MAE for wind speed, solar irradiance, and load demand.

2. **MCS Scenario Generation**: Generate 50 scenarios for each stochastic parameter within +/-25% MAE range.

3. **MOPSO Initialization**: Initialize particle swarm with random positions (PV, WT, BESS capacities) and velocities within bounds. Evaluate initial fitness (TLCC, DPSP, LPPP) for each particle for each scenario.

4. **Pareto Front Evolution**: For each iteration:
   a. Update particle velocities using Pbest and Gbest positions
   b. Update particle positions (capacities)
   c. Evaluate objective functions for each particle
   d. Update personal bests
   e. Update external repository of non-dominated solutions
   f. Apply mutation operator for diversity

5. **Multi-Criteria Ranking (TOPSIS)**:
   a. Normalize the decision matrix from non-dominated solutions
   b. Assign equal or user-specified weights to TLCC, DPSP, LPPP
   c. Compute positive-ideal and negative-ideal solutions
   d. Calculate Euclidean distances from both ideal solutions
   e. Compute relative closeness scores
   f. Rank solutions by closeness score

6. **Output Selection**: Select top-ranked solution as recommended planning configuration with capacities and operational strategy.

## Outputs

- Optimal capacities: PV (kW), WT (kW), BESS (kWh)
- TLCC ($), DPSP (%), LPPP (%) for selected solution
- Pricing schedule (hourly) for selected DRP type
- BESS SOC trajectory over planning horizon
- Pareto front visualization (3D scatter plot)
- TOPSIS ranking table

## Key Equations

- Power balance: Sw(t) + Spv(t) + Sds_b(t) - Sch_b(t) = S_L_DRP(t) (Equation 29)
- BESS SOC update: SOC(t) = SOC(t-1)(1-SDb) + Sch_b(t)*eta_c - Sds_b(t)/eta_d (Equation 3)
- SSAP pricing: delta_E(t) based on supply-demand imbalance (Equation 12)
- TLCC: sum of NPV of IC, O&M, RC, SV over project lifetime (Equation 26)
- DPSP: sum(S_curtailed_load)/sum(S_load) * 100% (Equation 27)
- LPPP: sum(S_curtailed_VRE)/sum(S_VRE) * 100% (Equation 28)
