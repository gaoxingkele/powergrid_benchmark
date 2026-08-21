# Experiments

## Experimental Setup

### Test System
- **Network**: Modified IEEE 39-bus transmission network (220 kV voltage level)
- **Reference bus**: Node 1 (connects to upstream grid via substation)
- **Thermal units**: Nodes 31 and 33 (3500 MW total capacity)
- **PV units**: Node 30
- **Wind units**: Nodes 36, 37, 38
- **Supply area**: 12,735 km^2, 5.68 million population, 2.33466 million customers
- **Data source**: Real operational data from a power grid company in Southwest China
- **Peak-valley load difference**: 3091 MW

### Computational Environment
- **Platform**: MATLAB R2024b
- **OS**: Windows 10
- **RAM**: 16 GB
- **CPU**: Intel Core i7-11800H

## Planning Schemes

Five comparative schemes were designed:

| Scheme | Description | Configuration |
|--------|-------------|---------------|
| Scheme 1 | No energy storage | Baseline without ESS |
| Scheme 2 | Single Li-ion battery | Node 33: 5370 MWh, 3280 MW |
| Scheme 3 | Single flow battery | Node 21: 5700 MWh, 4400 MW |
| Scheme 4 | Hybrid storage at same node | Node 15: 2410 MWh Li-ion + 4860 MWh FB, 550 MW + 3880 MW |
| Scheme 5 | Proposed multi-node HESS | Nodes 21, 15: 2600 MWh Li-ion + 5300 MWh FB, 2160 MW + 4500 MW |

## Algorithm Comparison Experiment

Five algorithms compared over 30 experimental trials:
- **COOT** [23]
- **PSO** [25] 
- **DE** [26]
- **WAA** [27] (standard version)
- **IWAA** (proposed improved version)

### Performance Metrics
- Penalty costs: Best, Average, Standard deviation
- Total costs: Best, Average, Standard deviation

## Key Results

### Table 2 — Comparison of Planning Schemes
| Metric | Scheme 1 | Scheme 2 | Scheme 3 | Scheme 4 | Scheme 5 |
|--------|----------|----------|----------|----------|----------|
| Voltage Fluctuation (pu) | 56.55 | 26.15 | 28.71 | 24.05 | 20.52 |
| Line Loss (pu) | 106.94 | 58.12 | 60.74 | 50.63 | 45.27 |
| Penalty Cost (CNY) | 1.6042e7 | 4.0281e6 | 5.3612e6 | 2.9062e6 | 2.3960e6 |
| Total Cost (CNY) | 1.6042e7 | 1.1638e7 | 1.0736e7 | 9.1448e6 | 8.7718e6 |

### Table 3 — Algorithm Comparison Results
| Metric | COOT | PSO | DE | WAA | IWAA |
|--------|------|-----|----|-----|------|
| Penalty Best | 2.67e6 | 2.41e6 | 2.53e6 | 2.49e6 | **2.16e6** |
| Penalty Avg | 3.12e7 | 2.74e7 | 2.85e7 | 2.86e6 | **2.43e6** |
| Penalty Std | 2.64e6 | 2.37e6 | 2.11e7 | 2.34e6 | **1.95e6** |
| Total Best | 9.64e6 | 9.97e6 | 9.59e6 | 9.06e6 | **8.58e6** |
| Total Avg | 1.22e7 | 1.35e7 | 9.85e6 | 9.42e6 | **8.74e6** |
| Total Std | 3.09e6 | 2.63e6 | 2.08e6 | 2.57e6 | 2.48e6 |

### VMD-PSO Reconstruction Accuracy
- Maximum reconstruction error: 1.14e-13
- Root Mean Square Error (RMSE): 4.74e-15

## Sensitivity Analysis

### Penalty Coefficient Variation (Table 4)
Tested penalty coefficients: {0.1, 0.2, 0.3, 0.4, 0.5} * lambda_0

| Lambda | Li-ion Cap (MWh) | Li-ion Power (MW) | FB Cap (MWh) | FB Power (MW) |
|--------|-------------------|-------------------|---------------|----------------|
| 0.1*lambda_0 | 3068 | 2484 | 6254 | 5175 |
| 0.2*lambda_0 | 2860 | 2333 | 5830 | 4860 |
| 0.3*lambda_0 | 2600 | 2160 | 5300 | 4500 |
| 0.4*lambda_0 | 2236 | 1901 | 4558 | 3960 |
| 0.5*lambda_0 | 1950 | 1685 | 3675 | 3110 |

**Key finding**: Capacity decreases monotonically as penalty coefficient increases. For stability-focused operators, 0.2-0.3 lambda_0 recommended.

## Key Observations
1. HESS significantly outperforms no-storage and single-type storage schemes
2. Multi-node coordinated deployment (Scheme 5) is superior to co-located HESS (Scheme 4)
3. IWAA demonstrates best performance across all algorithm comparison metrics
4. VMD-PSO achieves near-perfect reconstruction accuracy
5. Penalty coefficient selection significantly impacts optimal capacity configuration
