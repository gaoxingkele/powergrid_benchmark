# Environment

## Software Environment
- **Optimization tool**: HOMER Pro version 3.14.2 (UL Renewables / HOMER Energy)
- **Modeling capability**: Hourly time-step simulation; economic optimization via NPC minimization; sensitivity analysis
- **Equations used**:
  - PV power output: P_PV = Y_PV * f_PV * (G_T / G_T_STC) * [1 + alpha_P * (T_c - T_c_STC)]
  - Wind turbine power: piecewise function based on cut-in, rated, and cut-out wind speeds
  - Wind speed height adjustment: v(t) = v_ref * (H_WT / H_ref)^alpha
  - Diesel fuel consumption: Fuel_c_DG = a * T_DG + b * P_DG
  - Battery capacity: C_Batt = (E_L * AD) / (eta_inv * DOD * eta_bat)
  - Inverter power: P_inv = P_peak / eta_inv
  - NPC: sum(R_t / (1+i)^t)
  - Real discount rate: i = (i' - f) / (1 + f)
  - LCOE: C_ann_tot / E_served

## Data Sources
- **Meteorological data**: NASA Surface Meteorology and Solar Energy database (POWER) [84]
  - Daily solar irradiation and clearness index
  - Sunshine duration
  - Temperature
  - Wind speed
- **Grid pricing**: EPIAS (Energy Exchange Istanbul) April-June 2025
  - Purchase price: USD 0.096/kWh
  - Sellback price: USD 0.076/kWh
- **Economic data**: Turkiye Central Bank discount rate (9.75%)
- **Component specifications**: Manufacturer datasheets (LG, Eocycle, TommaTech, SAFT/Kinetic, Generic)

## Economic Parameters Used
| Parameter | Value |
|-----------|-------|
| Project lifetime | 25 years |
| Nominal discount rate | 9.75% |
| Base inflation rate | 10% |
| Grid power price | $0.096/kWh |
| Grid sellback rate | $0.076/kWh |
| Diesel fuel price (base) | $1.5/L |
| Sensitivity: inflation | 5%, 10%, 30% |
| Sensitivity: solar irradiance | 2.0, 4.5, 7.0 kWh/m2/d |
| Sensitivity: fuel price | $1.2, $1.5, $1.8/L |
| Sensitivity: grid power price | $0.10-$0.16/kWh |
| Sensitivity: grid sellback | $0.08-$0.18/kWh |

## System Modeling Approach
1. Load profile determination (Equation 1: L_s = sum(Q_n * P_n * H_n))
2. Resource assessment (NASA POWER data)
3. Component selection (Table 1 specifications)
4. Architecture definition (16 configurations across grid-connected and off-grid)
5. HOMER Pro optimization (NPC minimization, hourly simulation)
6. Sensitivity analysis (parametric variation of key inputs)
7. Environmental impact assessment (CO2 emission reduction)
