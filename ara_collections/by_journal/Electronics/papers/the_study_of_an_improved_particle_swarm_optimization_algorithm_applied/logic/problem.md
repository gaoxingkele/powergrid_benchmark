# Problem Specification

## Observations

### O1: Renewable volatility threatens microgrid reliability
- **Statement**: Wind and photovoltaic (PV) generation are volatile and uncontrollable; their output depends on weather (irradiance, temperature, wind speed) that varies strongly within a single day. In the case study, PV output swings from 0 kW (night) to ≈93 kW (afternoon) and system load from ≈380 kW to ≈721 kW over 24 h.
- **Evidence**: §1.1-1.2 narrative; Figures 9-12 (load, wind, temperature, irradiance profiles); Table 5 (hourly PV/WT/load).
- **Implication**: A dispatch method must actively coordinate storage, thermal, and grid exchange to keep supply = demand at every hour despite renewable variability.

### O2: Thermal generators are the pollution and fuel-cost driver
- **Statement**: PV and wind are clean (no pollutants), but the small thermal generator (DG) emits CO2/SO2/NOX and consumes fuel, and is indispensable for meeting large/stable load. DG emission factors are far higher than the clean sources' (e.g. CO2 650 g/kWh for DG); DG carries the fuel cost and most of the environmental cost.
- **Evidence**: §3.1; Table 2 (emission factors, treatment costs); Table 6 (fuel + environmental cost columns).
- **Implication**: Minimizing cost and minimizing emissions are aligned through reducing thermal reliance — a cheaper dispatch is also cleaner.

### O3: Standard PSO converges prematurely to local optima
- **Statement**: Particle Swarm Optimization (PSO) is popular for power-system problems (simple, few parameters, good global search) but is susceptible to local optima, early convergence, and uneven particle distribution in the search space.
- **Evidence**: §1.2 (refs [12-14]); §4.1-4.2 narrative.
- **Implication**: A vanilla PSO solver risks returning a sub-optimal, more expensive dispatch; the optimizer itself needs improvement.

### O4: Random PSO initialization gives uneven early coverage
- **Statement**: Randomly generated initial particle positions/velocities produce an uneven spatial distribution early in the search, degrading global search capability.
- **Evidence**: §4.2.1.
- **Implication**: A more uniform / diverse initialization (chaotic mapping) can improve early exploration.

### O5: Fixed inertia weight and learning factors cannot serve both search phases
- **Statement**: A large inertia weight w over-explores (slow convergence, oscillation/instability); a small w over-exploits (local-optima trapping, lost diversity). Similarly, fixed learning factors cannot emphasize global search early and local search late.
- **Evidence**: §4.2.2, §4.2.3.
- **Implication**: w, c1, c2 should be scheduled dynamically across iterations.

## Gaps

### G1: Model incompleteness
- **Statement**: Prior microgrid dispatch models often address only a subset of costs/devices or a single objective; there is room for a more comprehensive model incorporating additional influencing factors (multiple device types, O&M/fuel/depreciation/grid/environmental costs, multiple constraints).
- **Caused by**: O1, O2.
- **Existing attempts**: Model-development line of research (refs [5-11]); weighted-sum / penalty-function multi-to-single objective conversions.
- **Why they fail**: Each captures part of the picture; the paper argues "considerable room for improvement in both model construction and algorithm optimization."

### G2: PSO solver weakness
- **Statement**: Traditional PSO's premature convergence and local-optima susceptibility limit solution accuracy for the dispatch problem.
- **Caused by**: O3, O4, O5.
- **Existing attempts**: New search strategies; hybridizing PSO with other algorithms (refs [15-18]); CPSO, QPSO variants.
- **Why they fail**: Still leave accuracy/convergence gains on the table; the paper positions SCMPSO as a further improvement over PSO/CPSO/QPSO.

## Key Insight
- **Insight**: The exploration-vs-exploitation balance in PSO can be actively steered across the run by combining four coordinated modifications — chaotic (Henon) initialization for diverse early coverage, an adaptive nonlinear inertia weight, complementary sinusoidal learning factors (c1 down, c2 up), and a second-order oscillation term whose sign/magnitude switches at the half-way iteration — so the swarm explores widely early and refines stably late.
- **Derived from**: O3, O4, O5.
- **Enables**: SCMPSO, which the paper reports converges faster, searches a wider range, and escapes local optima better than PSO/CPSO/QPSO, yielding a cheaper, cleaner dispatch.

## Assumptions
- A1: The 24-h scheduling horizon with 1-h resolution adequately represents daily operation; a "typical summer day" of a Jiangsu city is representative.
- A2: Renewable (PV/WT) output, load, and prices are known/forecast inputs (deterministic dispatch, not stochastic within the solve).
- A3: PV and wind produce no pollutants; only DG and grid-imported power carry emissions.
- A4: The weighted/aggregated single objective (operating cost C1 + environmental cost C2) faithfully represents the economic-environmental trade-off.
- A5: Device models (Eqs. 1-5) and constant coefficients (Tables 1-2) hold over the horizon.
