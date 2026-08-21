# Concepts

## Integrated Energy System (IES)
- **Notation**: Coupled electricity–gas–heat–cooling multi-network
- **Definition**: An advanced energy infrastructure synthesizing production, transmission, storage, and consumption of electricity, thermal energy, natural gas, and cooling via interconnected multi-networks, achieving cross-carrier synergy and cascade utilization.
- **Boundary conditions**: The paper focuses on electricity–gas coupling with P2G and gas-fired units; heat/cooling are described but not modeled in constraints.
- **Related concepts**: IESO, P2G, CHP, DistFlow, Weymouth equation.

## Price-Based Demand Response (PDR)
- **Notation**: TOU price vector λ_t_e; cross-price elasticity matrix E
- **Definition**: A demand-side management mechanism where the IESO sets time-of-use retail prices (peak/flat/valley blocks), and end-users adjust consumption through self- and cross-price elasticities. Loads are categorized as fixed, shiftable (energy-conserving), and interruptible (curtailable).
- **Boundary conditions**: Shiftable loads conserve total daily energy (Eq. 7). Interruptible loads have max curtailment P^max_inter. Market-stability constraints enforce tariff ordering and peak-to-valley ratio γ ∈ [γ_min, γ_max] = [2, 5].
- **Related concepts**: Cross-price elasticity, TOU tariff, Shiftable load, Interruptible load.

## Vehicle-to-Grid (V2G)
- **Notation**: P^{V2G,ch}_t, P^{V2G,dis}_t
- **Definition**: Bidirectional energy exchange between aggregated EV fleets and the distribution grid. EVs charge during valley periods (absorbing surplus wind) and discharge during peak periods (reducing gas-turbine peaking). Fleet modeled with stochastic arrival/departure via normal distributions (µ_arr=17.47, µ_dep=8.58).
- **Boundary conditions**: 1000 homogeneous EVs at Node 11. Battery 60 kWh, charging/discharging power 7 kW, 90% efficiency. SOC bounds [0.1, 0.9]. Cannot charge and discharge simultaneously.
- **Related concepts**: EV aggregation, Bidirectional charging, SOC, Distributed storage.

## Power-to-Gas (P2G)
- **Notation**: P^{elec}_{P2G,j,t}, G^{P2G}_{i,t}
- **Definition**: Technology that converts surplus (primarily curtailed) electricity into synthetic natural gas via electrolysis and methanation. Coupled to curtailed wind availability (Eq. 38). Creates a bidirectional energy loop between power and gas networks.
- **Boundary conditions**: Subject to min/max power limits (Eq. 39). Efficiency η_P2G, heat value conversion HGV. Intake coupled to curtailed wind per Eq. 38.
- **Related concepts**: SNG, Electrolysis, Bidirectional coupling, Wind curtailment.

## Levelized Cost of Electricity (LCOE)
- **Notation**: C_{LCOE} (RMB/kWh)
- **Definition**: A lifecycle cost metric for EESS: amortizes initial capital expenditure (CAPEX) and year-wise operational expenditure (OPEX) over total discharge energy. Used in the objective (Eq. 12, C3) to penalize aggressive storage cycling.
- **Boundary conditions**: Discount rate 8%. Includes power-based and capacity-based capital costs, maintenance, and labor.
- **Related concepts**: EESS, CAPEX, OPEX, Cycling degradation.

## DistFlow Model
- **Notation**: Eqs. 18–21
- **Definition**: A branch-flow model for radial distribution networks capturing active/reactive power balance, voltage drop, and current flow. Includes squared voltage and current variables for convex formulation.
- **Boundary conditions**: Applies to the IEEE 33-bus radial network; linearized for MILP compatibility.
- **Related concepts**: Power flow, Distribution network, Voltage security.

## Weymouth Equation
- **Notation**: F_{ij,t} = C_{ij} · sgn(π_i,t − π_j,t) · sqrt(|π²_i,t − π²_j,t|)
- **Definition**: The nonlinear relation governing steady-state gas flow in pipelines, determined by the pressure differential between nodes. Piecewise-linearly approximated (12 segments per pipeline, max deviation <1.0%).
- **Boundary conditions**: Non-convex in native form; approximated via piecewise-linear segments with binary sign encoding for MILP compatibility.
- **Related concepts**: Gas network, Nodal pressure, Natural gas flow.

## Time-of-Use (TOU) Tariff
- **Notation**: λ_t_e for t ∈ {Ω_peak, Ω_flat, Ω_valley}
- **Definition**: A retail electricity pricing scheme segmenting the 24 h horizon into peak, flat, and valley blocks with distinct tariff levels. Must satisfy ordering (λ_valley < λ_flat < λ_peak) and peak-to-valley ratio constraint γ ∈ [2, 5].
- **Boundary conditions**: Hour boundaries predetermined. Market-stability constraints (Eqs. 13–17) enforce price bands and ratio limits.
- **Related concepts**: PDR, Peak-to-valley ratio, Market stability.

## Cross-Price Elasticity Matrix
- **Notation**: E = [ε_{ij}]_{n×n}
- **Definition**: A matrix whose entry ε_{ij} represents the sensitivity of demand in period i to price change in period j. Diagonal entries are self-elasticities (negative); off-diagonal entries are cross-elasticities reflecting inter-temporal substitution.
- **Boundary conditions**: Exogenous parameters adopted from established DR literature. Self- and cross-elasticities treated as representative of price-responsive commercial/residential mix.
- **Related concepts**: PDR, Shiftable load, Interruptible load, Demand elasticity.

## Electrochemical Energy Storage System (EESS)
- **Notation**: P^{ch}_{i,t}, P^{dis}_{i,t}, SOC_{i,t}
- **Definition**: Behind-the-meter battery storage providing intertemporal energy shifting. Governed by mutually exclusive charge/discharge states, SOC bounds [5%, 95%], energy balance with self-discharge, daily cycle conservation (Eq. 46), and max cycle limit (Eq. 47).
- **Boundary conditions**: LCOE degradation cost in objective. Cycle limit K^max_i constrains daily throughput.
- **Related concepts**: SOC, LCOE, Cycling limit, Distributed storage.
