# Concepts

## Net Present Cost (NPC)
- **Notation**: NPC
- **Definition**: The present value of all costs incurred over the project lifetime (installation, operation, maintenance, replacement, fuel) minus the present value of all revenues generated, discounted to the present using the real discount rate.
- **Formula**: NPC = sum(Rt / (1+i)^t) where Rt = net cash flow in period t, i = discount rate, t = time period
- **Boundary conditions**: 25-year project lifetime; includes capital, replacement, O&M, fuel, and salvage value; negative values indicate net revenue
- **Related concepts**: LCOE, Discount Rate, Life-cycle Cost

## Levelized Cost of Energy (LCOE)
- **Notation**: LCOE
- **Definition**: The average cost per unit of electrical energy generated over the system's lifetime, calculated as total annualized cost divided by total annualized load served.
- **Formula**: LCOE = Cann_tot / Eserved, where Cann_tot = total annualized cost (USD/yr), Eserved = total annualized load served (kWh/yr)
- **Boundary conditions**: Expressed in USD/kWh; enables comparison across different technologies and system sizes
- **Related concepts**: NPC, Cann_tot, Eserved

## Real Discount Rate
- **Notation**: i
- **Definition**: The rate used to convert future costs and revenues to present values, adjusted for inflation. Calculated from nominal discount rate and expected inflation rate.
- **Formula**: i = (i' - f) / (1 + f), where i' = nominal discount rate, f = expected inflation rate
- **Boundary conditions**: Turkiye central bank discount rate = 9.75% was used
- **Related concepts**: NPC, LCOE, Inflation Rate

## Renewable Fraction (RF)
- **Notation**: RF
- **Definition**: The fraction of total electricity generation derived from renewable sources (solar PV, wind) as opposed to fossil fuel (diesel generator or grid-purchased electricity).
- **Boundary conditions**: Expressed as percentage (0-100%); 100% = fully renewable
- **Related concepts**: CO2 Emission Reduction, PV penetration, Wind penetration

## CO2 Emission Reduction
- **Notation**: Delta_CO2
- **Definition**: Percentage reduction in CO2 emissions compared to a baseline scenario (grid-only for grid-connected, generator-only for standalone).
- **Boundary conditions**: Relative measure, baseline-dependent
- **Related concepts**: Renewable Fraction, Environmental Impact

## Hybrid Renewable Energy System (HRES)
- **Notation**: HRES
- **Definition**: An electricity generation system combining multiple energy sources (solar PV, wind turbines, diesel generators) with energy storage (batteries) and/or grid connection, designed to improve reliability, efficiency, and cost-effectiveness.
- **Boundary conditions**: At least one renewable source plus conventional backup; may be grid-connected or standalone
- **Related concepts**: Microgrid, Distributed Generation

## HOMER Pro
- **Notation**: HOMER Pro (ver. 3.14.2)
- **Definition**: Hybrid Optimization Model for Electric Renewables -- a software tool for modeling and optimizing microgrid architectures by simulating system operation and performing economic and sensitivity analyses.
- **Boundary conditions**: Time resolution from 1 minute to 1 hour; performs NPC optimization across user-defined system configurations
- **Related concepts**: NPC, LCOE, Optimization, Sensitivity Analysis

## Internal Rate of Return (IRR)
- **Notation**: IRR
- **Definition**: The discount rate at which the net present value of all cash flows equals zero. Used as a measure of investment profitability.
- **Boundary conditions**: Higher IRR indicates more profitable investment; compared against cost of capital
- **Related concepts**: NPC, Payback Period, Discount Rate

## Simple Payback Period
- **Notation**: SPB
- **Definition**: The time required for cumulative cash inflows to equal the initial investment, without discounting future cash flows.
- **Boundary conditions**: Expressed in years; shorter payback indicates faster recovery of investment
- **Related concepts**: IRR, NPC, Discounted Payback

## Capacity Factor
- **Notation**: CF
- **Definition**: The ratio of actual electrical output to maximum possible output over a given period.
- **Boundary conditions**: Depends on resource availability (solar irradiance, wind speed) and component characteristics
- **Related concepts**: PV Output, Wind Turbine Output, Renewable Fraction

## Energy Sold / Energy Purchased
- **Notation**: Esold, Epurchased
- **Definition**: For grid-connected systems, energy sold is surplus renewable electricity exported to the grid (revenue-generating), while energy purchased is electricity imported from the grid (cost-incurring).
- **Boundary conditions**: Net energy = Epurchased - Esold; negative net implies net seller
- **Related concepts**: Grid, Net Metering, Energy Charge, Demand Charge

## Agrivoltaics
- **Notation**: N/A
- **Definition**: The simultaneous use of land for both agriculture and solar photovoltaic electricity generation, typically with elevated or semi-transparent PV panels installed above crops.
- **Boundary conditions**: Emerging technology; varies by crop type, panel configuration, and climate
- **Related concepts**: PV, Greenhouse, Land Use Efficiency
