# Source Environment

## Language/Runtime
- **Python 3.9** — used for GMM clustering, priority index computation, optimization model building, and evaluation

## Framework/Libraries
- **Gurobi Optimizer v11.0** — mixed-integer nonlinear programming solver for the multi-objective DESS capacity allocation model
- **Standard data science stack** — implied: numpy, scipy, pandas (not explicitly stated but assumed for GMM/Critic computations)
- **scikit-learn** (likely) — for GMM implementation and K-means clustering

## Hardware
- Not explicitly specified in the paper. Standard workstation/workstation-class hardware is assumed.

## Data Sources
1. **Historical wind speed and solar irradiance data** — from Zhejiang Province distribution grid (source not further specified)
2. **Node-level load profiles** — 96 sampling points per day (15-minute resolution), from long-term historical measurements
3. **Annual statistical indicators** — supply reliability, outage duration, frequency noncompliance, voltage deviation, customer complaint rates — from routine utility operational statistics
4. **Socioeconomic statistics and electricity consumption data** — used only for interruption-cost-related indicator (I3)

## Key Dependencies
- **Gurobi v11.0** — optimization solver (commercial, requires license)
- **Python 3.9** — base environment
- **Improved GMM algorithm** — custom implementation with RV-coefficient-based K-means initialization

## Protocols
- **Time-of-use electricity pricing** (China):
  - Residential: peak 0.563 CNY/kWh (8:00–22:00), off-peak 0.291 CNY/kWh (22:00–8:00)
  - Industrial/Commercial: peak 1.092 CNY/kWh (19:00–21:00), standard 0.925 CNY/kWh (8:00–11:00, 13:00–19:00, 21:00–22:00), off-peak 0.412 CNY/kWh (22:00–8:00, 11:00–13:00)
- **DG surplus feed-in tariff**: 0.4153 CNY/kWh
- **Discount rate**: 0.05 (for lifecycle cost calculations)
- **DESS service life**: 12 years

## Random Seeds
- Not reported in the paper. The GMM and K-means clustering likely involve random initialization, but seed values are not documented.
