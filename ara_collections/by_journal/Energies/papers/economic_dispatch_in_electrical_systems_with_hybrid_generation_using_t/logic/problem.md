# Problem: Short-Term Economic Dispatch in Hybrid Generation Systems Under Energy Constraints

## Domain
Power Systems Optimization

## Problem Statement
The short-term economic dispatch (ED) problem for a hybrid generation system (HGS) comprising hydroelectric, thermoelectric, photovoltaic solar, and wind power plants. The system must meet a 24-hour demand profile at minimum operating cost while respecting operational constraints, under scenarios where hydroelectric generation is limited by reduced water availability (drought) or increased by high water availability.

## Key Challenges
1. **Stochastic renewable resources**: Solar irradiance, wind speed, and temperature are inherently uncertain and non-dispatchable.
2. **Nonlinear objective**: Thermoelectric cost functions include valve-point effects via sinusoidal terms, creating non-convex, multimodal landscapes.
3. **Coupled hydro constraints**: Four hydraulically interconnected hydroelectric plants with reservoir volume balance, water discharge limits, and upstream spillage dependencies.
4. **Energy limitation scenarios**: Hydroelectric capacity is restricted in Scenario 1 (drought) vs. fully available in Scenario 2, requiring different dispatch strategies.

## Objective Function
Minimize total fuel cost of thermoelectric plants:

Fix(PTix) = ai(PTix)^2 + bi*PTix + ci + |ei * sin(fi * (PminTi - PTix))|

With penalty terms for power balance and reservoir volume balance violations.

## Constraints
- Power balance: sum of all generation equals demand
- Generation limits: Pmin <= Pgen <= Pmax for each unit
- Water discharge limits: Qmin <= Qjx <= Qmax
- Reservoir volume limits: Vmin <= Vjx <= Vmax
- Reservoir volume balance with inflows, discharges, and spillages
- Coupled reservoir equations for upstream/downstream dependencies

## Optimization Horizon
24-hour planning horizon
