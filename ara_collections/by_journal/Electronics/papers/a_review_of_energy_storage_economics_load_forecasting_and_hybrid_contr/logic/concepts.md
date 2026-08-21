# Concepts

## Non-Network Solution (NNS)
- **Notation**: —
- **Definition**: A strategic, flexible alternative to capital-intensive grid expansion in which BESS (or other distributed assets) are deployed to manage peak loads and thermal constraints, deferring or eliminating traditional pole-and-wire upgrades. Contrasted with "network solutions" (physical reinforcement).
- **Boundary conditions**: Applies where storage can be sited/sized to relieve congestion and support voltage/frequency; effectiveness depends on AC-microgrid stability and spatial constraints (§5).
- **Related concepts**: BESS, expansion planning, STATCOM, System Health Index, cost-reflective pricing

## State of Charge (SoC)
- **Notation**: `SoC_t = SoC_0 − ∫₀ᵗ i(ξ)dξ / C_n`; operational ratio `SoC = Remaining Charge (Ah) / Nominal Capacity (Ah) × 100` (Eqs 7, 9)
- **Definition**: The remaining available charge of a battery, quantified via Coulomb counting; C_n is nominal capacity.
- **Boundary conditions**: Does not account for nonlinear terminal-voltage dynamics during operation, so it misrepresents deliverable energy; appropriate for internal cell balancing. Not directly measurable — estimated (§BMS, ref [50]).
- **Related concepts**: State of Energy, Coulomb counting, BMS, co-estimation

## State of Energy (SoE)
- **Notation**: `SoE_t = SoE_0 − ∫₀ᵗ i(ξ)u(ξ)dξ / E_n`; operational ratio `SoE = Remaining Energy (kWh) / Nominal Capacity (kWh) × 100` (Eqs 8, 10); correlation `SoE = a·SoC²(k) + b·SoC(k) + c` (Eq 11)
- **Definition**: The remaining releasable energy, obtained by integrating power (current × terminal voltage u(ξ)) over time; E_n is nominal energy. Provides a more direct/accurate representation of energy an NNS can supply to the grid than SoC.
- **Boundary conditions**: Prioritized over SoC for load-distribution and energy-production decisions in islanded AC microgrids; states are co-estimated (not measured). Related to SoC via a stable quadratic polynomial (§BMS).
- **Related concepts**: State of Charge, co-estimation, grid-aware dispatch, degradation-aware operation

## SoC/SoE Co-estimation
- **Notation**: —
- **Definition**: BMS use of advanced algorithms processing current, voltage, and temperature data (under offline simulation) to jointly estimate SoC and SoE, correcting sensor noise and cumulative error by cross-referencing their strong positive correlation.
- **Boundary conditions**: Required because both states are directly unmeasurable; underpins reliable grid-aware dispatch (§BMS, refs [95–100]).
- **Related concepts**: SoC, SoE, BMS, Kalman/sliding-mode/neural estimators

## Degradation-Aware Modelling
- **Notation**: —
- **Definition**: Optimization/planning that explicitly models battery ageing — distinguishing cycle ageing (proportional to energy exchanged and depth of discharge) from calendar ageing — so that operational strategies extend battery lifespan while preserving economic feasibility.
- **Boundary conditions**: Contrasted with static planning that ignores ageing and can be trapped in local optima; especially relevant for lithium-ion in high-cycling/high-DoD regimes (§1.2.1, §3.6).
- **Related concepts**: LCOS, cycle ageing, calendar ageing, depth-of-discharge, techno-economic optimization

## Levelized Cost of Storage / Energy (LCOS / LCOE) and Net Present Cost (NPC)
- **Notation**: NPC ≈ total annualized cost / capital recovery factor (§3.1)
- **Definition**: LCOS/LCOE are per-unit lifecycle cost metrics for storage/energy (capital, efficiency losses, operational expense, degradation); NPC is total lifetime cost adjusted to the present year and is the primary optimization objective in HOMER-based frameworks.
- **Boundary conditions**: The review emphasizes structural optimization over fixed monetary values because prices are volatile/location-dependent (§3.1); static cost analysis is insufficient under market fluctuation.
- **Related concepts**: CAPEX, OPEX, capital recovery factor, tariff sensitivity, feed-in tariff

## Hybrid Energy Storage System (HESS)
- **Notation**: —
- **Definition**: An architecture combining complementary storage technologies — most commonly batteries + supercapacitors — where batteries handle medium-to-long-term energy balancing and supercapacitors buffer fast transients/high-power events, reducing high-C-rate stress and degradation.
- **Boundary conditions**: Increasingly adopted in AC microgrids and high-renewable-penetration systems requiring both long-duration balancing and fast transient response (Table 2, §2.2.3).
- **Related concepts**: Supercapacitor, integration topology, degradation stress, multi-scale response

## Integration Topology (AC-coupled / DC-coupled / Hybrid)
- **Notation**: —
- **Definition**: The electrical arrangement of renewable generators, storage, and power-electronic interfaces. AC-coupled: separate inverters onto a common AC bus (modular, retrofit-friendly, more conversion stages/losses). DC-coupled: shared DC bus via DC–DC converters with a single grid inverter (fewer stages, direct PV-to-battery charging, higher efficiency, more control/protection complexity). Hybrid: combines topologies/technologies.
- **Boundary conditions**: Choice affects conversion efficiency, controllability, fault management, retrofit ease, and control bandwidth (§2.2, §2.3).
- **Related concepts**: HESS, solid-state transformer, EMS, conversion losses

## Solid-State Transformer (SST)
- **Notation**: —
- **Definition**: Power-electronic interface integrating conversion stages to enable controllable power exchange among medium-voltage AC, low-voltage AC, DC buses, RES, and storage — supporting voltage regulation, bidirectional flow, reactive-power support, and coordinated AC/DC link control.
- **Boundary conditions**: Less commercially mature; high capital-cost variability, protection challenges, semiconductor-reliability and supervisory-control requirements; best for advanced hybrid AC/DC microgrids (§2.2.4, §2.3).
- **Related concepts**: Integration topology, multiport routing, grid-forming operation

## Grey Wolf Optimizer – Particle Swarm Optimization (GWO-PSO) Hybrid
- **Notation**: —
- **Definition**: A dual-strategy metaheuristic where GWO's global-exploration capability locates promising regions and PSO exploits the local optimum within a region (top GWO solutions seed PSO particle initialization; Figure 7), balancing robustness with computational efficiency for multi-objective microgrid optimization.
- **Boundary conditions**: Applied to grid-connected PV–battery management and HRES sizing/control; targeted at the exploration-vs-exploitation dilemma of standalone algorithms (§4.2, ref [63]).
- **Related concepts**: Metaheuristic, exploration-exploitation, multi-objective optimization, MPC

## Multi-Objective Optimization Objective Functions
- **Notation**: F_emissions (Eq 1), F_losses (Eq 2), F_autonomy = LPSP (Eq 3), F_cost (Eq 4), F_total = Σ wᵢ Fᵢ (Eq 5)
- **Definition**: The set of objective functions guiding optimization-based EMS: emission minimization, network-loss minimization, autonomy maximization, total-cost minimization, combined via weighting coefficients into a single weighted objective.
- **Boundary conditions**: Weights wᵢ selected per economic/environmental/technical/reliability priority; enables trade-off search (e.g. cost-minimizing dispatch may raise degradation) rather than single-metric optimization (§4.2).
- **Related concepts**: LPSP, GWO-PSO, degradation cost, weighted sum

## Loss of Power Supply Probability (LPSP)
- **Notation**: `F_autonomy = LPSP = Σ L_unmet(t) / Σ L_demand(t)` (Eq 3)
- **Definition**: Ratio of unmet load to total load demand over the horizon; a reliability/autonomy metric where lower LPSP indicates higher local supply reliability and reduced dependence on external grid support.
- **Boundary conditions**: Used as the autonomy-maximization objective in renewable-integrated microgrid optimization (§4.2).
- **Related concepts**: Objective functions, autonomy, reliability

## Deterministic Forecasting
- **Notation**: —
- **Definition**: Structured (non-black-box) predictive modelling of PV output, wind availability, and load that offers enhanced accuracy on nonlinear patterns versus traditional statistical models (ARIMA/SARIMA), enabling proactive EMS scheduling. Evaluated primarily via MAPE and RMSE.
- **Boundary conditions**: Targeted at non-stationary/volatile renewable conditions; the review scopes deliberately to deterministic (and structured ML) rather than opaque black-box methods (§1.2.2, §4.1).
- **Related concepts**: MAPE, RMSE, signal decomposition, EMS, proactive scheduling

## Signal Decomposition and Preprocessing
- **Notation**: EMD, VMD, WT, PCA, STL; Min–Max, Z-Score (Table 6)
- **Definition**: Preprocessing/feature-extraction techniques that de-noise and structure non-stationary renewable time series: decomposition (Empirical Mode Decomposition, Variational Mode Decomposition, Wavelet Transform) breaks signals into sub-components/IMFs; scaling (Min–Max, Z-score) accelerates convergence; PCA reduces redundancy; STL separates seasonal/trend/residual.
- **Boundary conditions**: Technique choice depends on dataset characteristics (volatility, outliers, seasonality); a prerequisite for reliable forecasting and hybrid control execution (§4.3, Table 6).
- **Related concepts**: Intrinsic Mode Function, deterministic forecasting, data normalization

## Low-Inertia Grid / RoCoF
- **Notation**: —
- **Definition**: Operating condition of inverter-dominated networks lacking synchronous-generator rotational inertia, leading to higher rate-of-change-of-frequency (RoCoF), reduced damping, and greater sensitivity to supply–demand imbalance; motivates fast (sub-second) storage response and offline time-domain control validation.
- **Boundary conditions**: Intensifies with rising IBR/PV penetration; distribution-level effects include voltage rise and reverse power flow (§1.1).
- **Related concepts**: Synthetic inertia, frequency response, transient stability, STATCOM

## Energy Trilemma
- **Notation**: —
- **Definition**: The requirement to simultaneously balance energy security, social equity, and environmental sustainability, which drives the renewable transition and frames storage-integration decisions.
- **Boundary conditions**: Used as the overarching motivating objective of the review (§1).
- **Related concepts**: Decarbonization, renewable energy sources, techno-economic optimization

## STATCOM (Static Synchronous Compensator)
- **Notation**: —
- **Definition**: A power-electronics-based device providing dynamic reactive-power support to maintain short-term voltage stability during transient grid disturbances; coordinated with distributed BESS to maximize voltage-stability enhancement at fixed investment cost.
- **Boundary conditions**: Complements (does not replace) storage-based NNS; especially relevant in wind-penetrated AC microgrids (§5, refs [74]).
- **Related concepts**: Non-network solution, voltage stability, reactive power, transient disturbance
