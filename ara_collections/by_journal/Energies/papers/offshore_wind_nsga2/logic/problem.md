# Problem Description

## Domain
Energy Systems, Offshore Wind Power, Energy Storage Optimization, Multi-Objective Optimization

## Problem Statement
Offshore wind farms exhibit significant output power volatility due to the intermittent and unpredictable nature of wind resources. Configuring battery energy storage systems (BESS) can effectively smooth these fluctuations and improve grid-connected stability. However, energy storage systems entail substantial investment costs. The core challenge is determining the optimal rated power and rated capacity of the BESS that simultaneously minimizes the total investment cost and minimizes the output power fluctuation rate of the wind farm. This trade-off is further complicated when the energy storage system participates in electricity spot market trading, introducing revenue streams that offset costs.

## Scope
- **Wind farm scale**: 40 MW offshore wind farm (16 turbines x 2.5 MW) in Wan'an County, China
- **Energy storage type**: Electrochemical (lithium-ion) battery energy storage system
- **Geographic focus**: China's electricity market policies, using Guangdong Province spot prices
- **Data period**: Wind power output data for 2023; spot electricity price data for 2024
- **Algorithms compared**: NSGA-II (primary) and MOPSO (benchmark)
- **Configurations explored**: Rated power 0-12 MW, rated capacity 0-48 MWh

## Objectives
1. **Objective 1**: Minimize total energy storage system investment cost (C_a), including initial investment, operation and maintenance, replacement, and waste disposal costs.
2. **Objective 2**: Minimize the output power fluctuation rate (sigma), measured as the relative standard deviation of wind power output after storage configuration.

## Decision Variables
- `P_es`: Rated power of energy storage system (MW)
- `S_es`: Rated capacity of energy storage system (MWh)

## Constraints
- State of Charge (SOC) limits: SOC_min <= SOC(t) <= SOC_max
- Power limits: 0 <= P_c(t) <= P_c_max (charging), 0 <= P_dc(t) <= P_dc_max (discharging)
- Grid code requirements: Active power change over 1 min and 10 min must comply with limits based on installed capacity (Table 1)

## Three Configuration Schemes
1. **Scheme 1**: Only the relationship between investment cost and output volatility is considered.
2. **Scheme 2**: Investment cost minus annual electricity sales revenue from spot market participation.
3. **Scheme 3**: Peak-valley arbitrage strategy — batteries charge only during low-price periods and discharge only during high-price periods to maximize revenue.
