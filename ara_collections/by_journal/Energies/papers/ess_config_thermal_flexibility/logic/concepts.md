# Concepts

## Temperature-Controlled Load (TCL) / Controllable Load
- **Notation**: \(T_t, T_{\min}, T_{\max}, P_t, P_{\max}\)
- **Definition**: A building load (primarily air conditioning) whose power consumption can be modulated within a comfort temperature range \([T_{\min}, T_{\max}]\) while satisfying a first-order equivalent thermal parameter (ETP) model: \(C(T_{t+1} - T_t) = \Delta t[(T_{out,t} - T_t)/R_{wa} + (T_{out,t} - T_t)/R_w + C_{GP} \cdot P_t + M^{rad}_t \cdot k \cdot F_w + Q_{in}]\). The power is bounded \(0 \le P_t \le P_{\max}\).
- **Boundary conditions**: Applies to buildings with air conditioning systems. The model assumes single-zone lumped thermal capacitance and does not capture multi-zone thermal coupling or occupancy-driven internal gains.
- **Related concepts**: Demand-side flexibility, pre-cooling, building thermal mass, virtual energy storage

## Energy Storage Station (ESS) Configuration Cost
- **Notation**: \(C_1, C_2, C_3, C_4, F_2\)
- **Definition**: The comprehensive life-cycle cost of the ESS, consisting of four components: acquisition cost \(C_1 = \sum_{i=1}^n \frac{r(1+r)^D}{(1+r)^D-1}[Q_i c_i(n_i+1)]\); installation cost \(C_2 = \sum_{i=1}^N \sum_{j=1}^{n_i} \frac{r(1+r)^D}{(1+r)^D-1}(1+r)^{-d_{ij}}(1-\alpha_i)^{d_{ij}} C_{i,j}^{rep} N_i\); O&M cost \(C_3 = \sum_{i=1}^N \sum_{t=1}^T [u_{i,1}(t)|P_{SB,i}(t)|k_{ch} + u_{2,i}(t)|P_{SB,i}(t)|k_{dis}]\); and equipment residual value recovery \(C_4 = \sum_{i=1}^N \sum_{j=0}^{n_i} \frac{r(1+r)^D}{(1+r)^D-1}(1+r)^{-d_{ij}} C_{4,i} N_i\).
- **Boundary conditions**: The model assumes battery ESS technology, fixed 10.5-year lifetime, and deterministic replacement cycles. It does not capture degradation-dependent capacity fade or second-life battery value.
- **Related concepts**: Life-cycle cost, acquisition cost, O&M cost, equipment residual value

## Grid Operating Cost
- **Notation**: \(F_1 = \min\{C_{grid} + C_{loss} + C_{DG} + C_{LO}\}\)
- **Definition**: The sum of four cost components: electricity purchase cost \(C_{grid} = \sum_{t=1}^{24} c_t^{buy} P_t^{grid} \Delta t\); generation cost \(C_{DG} = \sum_{t=1}^{24} \sum_{i \in \Omega_{MG}} (c_{MG}^{fuel} P_{t,i}^{MG}/\eta_i + c_{MG}^{oper} P_{t,i}^{MG}) \Delta t\); network loss cost \(C_{loss} = \sum_{t=1}^{24} c_t^{buy} \sum_{j=1}^{N_{node}} u_j^t \sum_{k \in \Omega_L^j} u_k^t G_{jk} \cos \delta_{jk}^t \Delta t\); and load cost \(C_{LO} = \sum_{t=1}^{24} c_t^{buy} (P_t + P_{load})\).
- **Boundary conditions**: Uses deterministic time-of-use tariffs; no real-time pricing. Network losses are modeled through a linearized power flow model.
- **Related concepts**: Time-of-use tariff, power purchase cost, network loss, distributed generation cost

## POA-GWO-CSO Hybrid Algorithm
- **Notation**: POA-GWO-CSO
- **Definition**: A hybrid metaheuristic optimization algorithm that combines three strategies: (1) the Pelican Optimization Algorithm (POA) base structure with move-to-prey (exploration) and skimming (exploitation) phases; (2) Grey Wolf Optimization (GWO) leader strategy incorporating \(\alpha, \beta, \delta\) wolf pack hierarchy to guide the position update with nonlinear inertia weights \(p(t) = (p_{max} - p_{min})/[1 + \exp(-q(t - T/2))] + p_{min}\); and (3) Crisscross Optimization (CSO) with horizontal crossover \(Zx^{p2}_{i1j} = r_1 x^{p2}_{ij} + (1-r_1)x^{p2}_{ik} + c_1(x^{p2}_{ij} - x^{p2}_{ik})\) and vertical crossover \(Xx^{p2}_{ij} = r_3 x^{p2}_{ij} + (1-r_3)x^{p2}_{ik}\).
- **Boundary conditions**: Performance depends on population size \(N\), maximum iterations \(T\), inertia weight bounds \([p_{min}, p_{max}]\), and crossover parameters. Designed for and validated only on the ESS multi-objective problem; generalization not established.
- **Related concepts**: Metaheuristic, multi-objective optimization, hybrid algorithm, exploration-exploitation trade-off

## Second-Order Cone Relaxation (SOCR)
- **Notation**: \(\Delta_{diff,t} = P_{mn,t}^2 + Q_{mn,t}^2 - i_{mn,t}V_{m,t}\)
- **Definition**: A convexification technique that converts the nonconvex power flow constraint \(i_{mn,t}v_{m,t} = P_{mn,t}^2 + Q_{mn,t}^2\) into a second-order cone constraint \(\|[2P_{mn,t}, 2Q_{mn,t}, i_{mn,t} - v_{m,t}]\|_2 \le i_{mn,t} + v_{m,t}\). The relaxation error is measured by \(\Delta_{diff,t}\); when it reaches the set accuracy, the SOCP solution is considered equivalent to the actual optimal solution.
- **Boundary conditions**: Exactness of relaxation depends on the radial/loopy network topology and operating conditions; may introduce nonzero duality gap for heavily meshed networks.
- **Related concepts**: SOCP, convex optimization, power flow, relaxation gap

## Pre-Cooling via Building Thermal Mass
- **Notation**: — (no dedicated symbol)
- **Definition**: A demand-side management strategy wherein the air conditioning system increases its power consumption before a peak tariff period to lower the indoor temperature below the comfort setpoint, effectively storing "cold energy" in the building's thermal mass. During the peak period, AC power is reduced as the indoor temperature passively rises within the comfort range, shifting electricity consumption from high-price to low-price hours.
- **Boundary conditions**: Effectiveness depends on building thermal time constant, comfort range width, and peak tariff duration. Requires predictive knowledge of tariff periods and ambient temperature.
- **Related concepts**: Thermal load flexibility, virtual energy storage, demand shifting, building thermal inertia

## Energy Storage Battery (ESB) State Constraints
- **Notation**: \(S_{SOC}(t), E^{ESS}_B, \beta, S_{SOC}^{min}, S_{SOC}^{max}, P^{ESS}_{B,min}, P^{ESS}_{B,max}\)
- **Definition**: Constraints governing the battery's energy state: capacity bounds \(E^{ESS}_{B,min} \le E^{ESS}_B \le E^{ESS}_{B,max}\) with energy multiplier \(E^{ESS}_B = \beta \cdot P^{ESS}_B\); state-of-charge bounds \(S_{SOC}^{min} \le S_{SOC}(t) \le S_{SOC}^{max}\); power limits \(|P^{ESS}(i)| \le |P^{ESS}_{B,max}|\); and cyclic charge conservation \(S_{SOC}^s = S_{SOC}^e\).
- **Boundary conditions**: Assumes linear charging/discharging efficiency models (\(\eta_{ch}, \eta_{dis}\)) and constant self-discharge rate \(\lambda\). Does not model nonlinear aging effects or temperature-dependent efficiency.
- **Related concepts**: State of charge, depth of discharge, energy multiplier, battery cycling
