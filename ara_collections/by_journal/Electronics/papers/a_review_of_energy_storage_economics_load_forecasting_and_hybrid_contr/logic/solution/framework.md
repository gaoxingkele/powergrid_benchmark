# Proposed Multi-Layer / Multi-Scale Synthesis Framework

This is the review's core proposed contribution (not an algorithm the authors invented, but a
structuring framework synthesized from the literature). It links physical renewable modelling,
degradation-aware techno-economic planning, deterministic forecasting, EMS dispatch, and offline
time-domain control validation into one workflow for AC-microgrid energy storage integration.
Reflected from Figure 2 (§1.2, §1.3) and Figure 3 (§2).

## Purpose
Bridge the macro-scale economic planning ↔ micro-scale dynamic control gap (C01, C08) by making the
layers exchange data: long-term planning objectives (NPC, LCOE, storage sizing) are explicitly linked
to short-term operational stability metrics (frequency response, voltage regulation, transient
performance), and operational results feed back to update planning constraints.

## Layers (Figure 2)

1. **Input Data layer**
   - Inputs: PV/Wind profiles, Load Demand, Tariffs & Market data, Battery Data, Weather Data.

2. **Physical Modelling layer (meso-scale)**
   - Tools: PVsyst / ETAP.
   - Function: PV yield, shading, losses, and degradation profiles; electrochemical cell degradation over time.
   - Role: supplies realistic yield and degradation data so downstream economics are grounded in physics, not theoretical capacity (Table 4, C08).

3. **Techno-Economic Planning & EMS layer (macro-scale)**
   - Tool: HOMER Pro (3.18.4).
   - Function: NPC, LCOE, BESS size, SoC/SoE limits, forecasting, and dispatch.
   - Role: capacity allocation and cost optimization; consumes physical yield/degradation from layer 2.

4. **Dynamic Control Validation layer (micro-scale)**
   - Tool: MATLAB/Simulink.
   - Function: frequency, voltage, THD, transients, and converter control; offline time-domain simulation of hybrid metaheuristic (GWO-PSO) control.
   - Role: validates operational constraints against transient behaviour.

5. **Outputs layer**
   - Optimal BESS Size, Dispatch Strategy, Stability Indicators.

6. **Feedback loop**
   - Operational results from MATLAB/Simulink dynamically update system constraints and input parameters, enabling iterative refinement of BESS sizing, dispatch strategies, and transient stability performance (the dashed feedback path in Figure 2).

## Physical microgrid architecture (Figure 3, §2)
- AC-coupled hybrid renewable microgrid on a common Microgrid AC Bus.
- PV Modules → DC/DC (MPPT) Converter → DC/AC Inverter → AC bus; Wind Turbine → Wind Generator → AC-AC Converter → AC bus.
- BESS → DC/DC Converter → Bidirectional DC/AC Grid-Tied Inverter (VSI) → AC bus (absorb excess / discharge to meet demand).
- Central EMS platform performs Forecasting, Optimisation, and Offline time-domain control using telemetry ("Data") from grid and generation.
- AC bus serves Local AC Loads and interacts with the Utility Grid.
- Design principle: every generation/storage asset is an independent parallel node → bidirectional power flow managed across the bus; EMS executes grid-aware dispatch from rigorous SoE estimation.

## Solver and bridge
- **Solver**: hybrid metaheuristic optimization (GWO-PSO) for the weighted multi-objective problem (see `objective_functions.md`, Figure 7). GWO explores; PSO exploits (C04).
- **Bridge metric**: joint SoC/SoE co-estimation in the BMS — SoE prioritized for grid-aware dispatch, SoC for cell balancing (C03).

## What the framework is NOT
The review does not propose a new optimization algorithm, controller, or forecasting model; it
proposes the **integration structure** (which tools, which metrics, which feedback couplings) and
synthesizes evidence that this coupling is necessary. No pseudocode beyond the surveyed GWO-PSO
workflow (Figure 7) is introduced.
