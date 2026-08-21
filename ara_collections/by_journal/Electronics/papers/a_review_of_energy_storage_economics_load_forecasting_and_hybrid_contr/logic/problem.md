# Problem Specification

## Observations

### O1: Inverter-based renewables strip the grid of rotational inertia
- **Statement**: As Inverter-Based Resources (IBR) progressively replace synchronous generators, the grid loses the rotational inertia that historically buffered frequency deviations, increasing rate-of-change-of-frequency, reducing damping, and raising susceptibility to supply–demand imbalance. In distribution networks, high PV penetration additionally causes voltage rise, reverse power flow, and strain on slow voltage-regulation devices (on-load tap changers, capacitor banks).
- **Evidence**: §1, §1.1 (refs [3–5,8]); paper quantifies advanced control effects: predictive controllers reduce Total Harmonic Distortion to 1.22% (from 6.00%) and improve Voltage Deviation Index to 4.85% under dynamic loads; ESS can provide real power compensation within 0.2 s of a critical RoCoF event.
- **Implication**: Sub-second offline time-domain control validation is required to maintain transient stability in low-inertia AC microgrids.

### O2: ESS integration has become a multi-objective optimization problem
- **Statement**: Energy storage deployment is no longer a hardware installation task; it must simultaneously consider economic viability, degradation-aware sizing/placement, forecasting uncertainty, power-system constraints, and advanced control strategies.
- **Evidence**: §1 (refs [7–11]).
- **Implication**: Storage value is governed by the interaction of economics, renewable uncertainty, and power-electronic control requirements — not by any single dimension.

### O3: Existing reviews treat planning, automation, and control as isolated domains
- **Statement**: Most existing reviews cover individual aspects of grid modernization but overlook the tightly coupled interdependency between macro-scale investment decisions (e.g. degradation-aware BESS sizing) and micro-scale time-domain control needed for stability in low-inertia grids. Prior broad reviews ([12–14]) address microgrid technologies, degradation-aware BESS allocation, and network-level transition challenges, but not an integrated synthesis linking economics + degradation planning + deterministic forecasting + optimization-based EMS + offline dynamic control validation.
- **Evidence**: §1, §1.2 (refs [12–14]).
- **Implication**: There is a structural gap: no unified framework connecting long-term techno-economic storage planning with short-term operational forecasting and dynamic stability assessment in AC microgrids.

### O4: Decoupled planning frameworks let forecast errors accumulate
- **Statement**: Integration frameworks that decouple planning from operation overlook the cumulative impact of forecast errors; the review reports that prioritizing State of Energy reduces capacity estimation errors by 5%, making the planning–control nexus a direct driver of capital efficiency and reliability.
- **Evidence**: §1.2 final paragraph; Table 9 ([99]).
- **Implication**: The planning–control link is quantitative, not merely conceptual.

### O5: Conventional techno-economic tools separate sizing from dispatch fidelity
- **Statement**: HOMER Pro offers robust capacity allocation but its built-in dispatch strategies (cycle charging, load following) are too rigid for dynamic tariffs and high renewables; it also lacks physical fidelity for shading, thermal losses, and electrochemical degradation.
- **Evidence**: §3.4, §3.5 (refs [39,40,41,42]).
- **Implication**: External sizing/dispatch optimization and coupling with physical (PVsyst/Helioscope) and dynamic (MATLAB/Simulink) tools are needed.

## Gaps

### G1: No unified macro-planning ↔ micro-control framework for AC-microgrid storage
- **Statement**: The literature lacks a framework connecting long-term techno-economic storage planning with short-term operational forecasting and dynamic stability assessment for AC microgrids.
- **Caused by**: O2, O3, O4.
- **Existing attempts**: Broad microgrid/BESS-allocation/network-planning reviews [12–14].
- **Why they fail**: They examine domains in isolation and do not synthesize economics + degradation + forecasting + optimization + offline dynamic validation together.

### G2: Static/decoupled planning misses degradation and forecast-error propagation
- **Statement**: Static planning traps sizing in local optima and ignores how dispatch strategy affects battery ageing and how forecast errors propagate into capital inefficiency.
- **Caused by**: O4, O5.
- **Existing attempts**: Static NPC/LCOE cost analysis in HOMER.
- **Why they fail**: Market volatility, tariff sensitivity, and degradation are not captured by static price inputs and fixed dispatch rules.

### G3: Rule-based/linear control inadequate under fast-varying renewables; scaling limits of MPC
- **Statement**: Conventional rule-based/linear controllers struggle in high-renewable dynamic environments; MPC improves tracking but is computationally heavy at scale.
- **Caused by**: O1, O2.
- **Existing attempts**: Rule-based dispatch, MPC, standalone metaheuristics.
- **Why they fail**: Standalone algorithms cannot balance exploration vs exploitation; rule-based controllers are bypassed by fast transients.

## Key Insight
- **Insight**: Energy storage integration is a tightly coupled multidimensional optimization problem; the macro-scale economic planning layer and micro-scale dynamic control layer must be linked through an explicit multi-scale workflow (physical modelling → degradation-aware techno-economics → deterministic forecasting → optimization-based EMS → offline time-domain control validation), with joint SoC/SoE estimation as the bridge and hybrid metaheuristics (GWO-PSO) as the solver.
- **Derived from**: O1–O5.
- **Enables**: The proposed multi-layer synthesis framework (Figure 2; `logic/solution/framework.md`) that iteratively feeds MATLAB/Simulink dynamic results back into planning constraints.

## Assumptions
- A1: AC microgrids remain the dominant infrastructure; AC-specific stability challenges must be solved with advanced hybrid control rather than by wholesale migration to DC microgrids (§1.1).
- A2: The review emphasizes a structural methodology of economic optimization rather than specific monetary values / fixed tariffs, because electricity prices are volatile and location-dependent (§3.1).
- A3: Deterministic (non-black-box) forecasting and control are the target regime — the review deliberately scopes to deterministic modelling and offline (not real-time hardware) simulation.
- A4: Validation is via offline time-domain simulation; real-time Power-Hardware-in-the-Loop (e.g. OPAL-RT) is future work (§6).
