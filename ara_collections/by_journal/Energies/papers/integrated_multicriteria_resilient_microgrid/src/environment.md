# Computational Environment and Dependencies

## Primary Simulation Platform
- **Software**: MATLAB (version not specified)
- **Purpose**: MOPSO algorithm implementation, TOPSIS ranking, system simulation, and Pareto front visualization

## Forecasting Environment
- **Language**: Python (version not specified)
- **Library**: Scikit-learn (for LSTM implementation and MAE computation)
- **Purpose**: LSTM model training, one-hour-ahead point forecasting, and forecast error metric calculation

## Key Dependencies

### MATLAB Toolboxes (assumed)
- Global Optimization Toolbox (for MOPSO framework)
- Statistics and Machine Learning Toolbox (for random scenario generation)
- Signal Processing Toolbox (for time series operations)

### Python Libraries
- Scikit-learn (LSTM implementation via MLP or equivalent)
- NumPy (numerical operations)
- Pandas (data handling)
- Matplotlib (forecast visualization)

### Input Data Requirements
1. **Weather data**: Hourly wind speed (m/s), solar irradiance (W/m^2), temperature (C) for one year (8760 hours) at the specific geographic location
2. **Load demand data**: Hourly electricity consumption (kW) for one year
3. **Techno-economic parameters**: Investment costs, O&M costs, lifetimes, efficiencies, discount/inflation rates (Table 1)
4. **DRP parameters**: Price elasticity matrix (Table 2), reference price, price bounds, FDR limits

## Hardware Requirements (Not Specified)
Computational requirements are not reported. The simulation involves:
- 50 MCS scenarios per stochastic case
- MOPSO with swarm population and iteration count (not specified)
- 8760-hour (annual) scheduling horizon at hourly resolution
- Three decision variables (PV, WT, BESS capacities)

## Reproducibility Notes
- LSTM training details (architecture depth, number of units, learning rate, epochs) are not specified
- MOPSO parameters (swarm size, iteration count, inertia weight range, repository size, mutation rate) are not fully specified
- TOPSIS weights for the three objectives are not explicitly stated
- Random seed for MCS is not specified, limiting exact reproducibility
