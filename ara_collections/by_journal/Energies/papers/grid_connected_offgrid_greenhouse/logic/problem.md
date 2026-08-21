# Problem Framing

## Domain
Energy system optimization for agricultural greenhouse facilities.

## Core Problem
How to design a hybrid energy system (combining solar PV, wind turbines, diesel generators, battery storage, and grid connection) that optimally balances:
1. **Economic objectives**: Minimize Net Present Cost (NPC) and Levelized Cost of Energy (LCOE)
2. **Technical objectives**: Reliably meet the facility's daily load of 369.52 kWh (peak 52.59 kW)
3. **Environmental objectives**: Maximize CO2 emission reduction and renewable fraction (RF)

## Problem Scope
Two distinct operational contexts are evaluated:
- **Grid-connected systems**: Facility remains connected to the utility grid, can buy/sell electricity
- **Off-grid (standalone) systems**: Facility operates independently, no grid access

## Key Decision Variables
- System architecture (which components to include)
- Component sizing (PV capacity, number of wind turbines, battery capacity, generator size)
- Dispatch strategy

## Constraints
- Site location: Sandikli, Afyonkarahisar, Turkiye (38.45N, 30.25E)
- Load profile: 134,875 kWh annual demand, 369.52 kWh/day, 52.59 kW peak
- Available components: specific PV panels, wind turbines, batteries, inverters, generators
- Economic parameters: discount rate 9.75%, grid purchase price $0.096/kWh, sellback $0.076/kWh
- Project lifetime: 25 years

## Stakeholders
- Greenhouse facility operators seeking energy cost reduction
- Agricultural businesses in rural areas with limited grid access
- Policymakers designing renewable energy incentives for agriculture

## Success Criteria
Optimal configurations ranked by NPC and LCOE, with CO2 reduction as a secondary objective. Sensitivity analysis to test robustness under varying inflation, fuel prices, and renewable resource availability.
