# Problem Specification

## Observations

### O1: DER penetration shifts distribution flow from unidirectional to multidirectional
- **Statement**: Modern distribution networks are transitioning from traditional unidirectional
  power-flow structures to multidirectional configurations, driven by increasing Distributed Energy
  Resource (DER) integration, which significantly influences system operation.
- **Evidence**: §1 Introduction, p.1.
- **Implication**: Control variables (DER setpoints, network configuration) must be co-optimized;
  static designs no longer suffice under high DER penetration.

### O2: The threat landscape is shifting from low-frequency to high-frequency high-impact events
- **Statement**: The evolving threat landscape is characterized by a transition from High-Impact
  Low-Frequency (HILF) to High-Impact High-Frequency (HIHF) events, particularly those driven by
  climate change, underscoring the growing importance of designing for resilience.
- **Evidence**: §2 Resilience, p.4 (refs [31]); resilience distinguished from reliability (N-1/N-2)
  and robustness via the N-k criterion, p.2.
- **Implication**: Design must target resilience (endure + recover from multiple failures), not just
  reliability against one or two faults.

### O3: In the base 6-bus feeder, downstream voltages sag and losses are high
- **Statement**: In the un-optimized base case the voltage at the farthest bus (bus 6) drops to 0.92
  pu and total real power loss is 55.3 kW; a fault-induced DER trip at bus 3 drives min voltage to
  0.88 pu, overloads 2 branches, and limits supply to 89% of load.
- **Evidence**: Table 3, Table 4, Table 6; abstract, §6, pp.9–11.
- **Implication**: A downstream voltage-support and loss-reduction problem coexists with a
  contingency (resilience) problem — both should be addressed by one control strategy.

### O4: GA is an established optimizer for power-system parameter estimation and search
- **Statement**: Genetic Algorithms, inspired by natural selection, are extensively used in science
  and engineering for complex search/optimization and have proven effective on prior power-system
  problems (arrester models, polluted insulators, soil parameters).
- **Evidence**: §3, p.6 (refs [37–42]).
- **Implication**: GA is a credible engine for the mixed continuous/discrete control-variable search
  (DER setpoints + reconfiguration) under nonlinear power-flow constraints.

## Gaps

### G1: Resilience is rarely embedded as an explicit objective in distribution optimization
- **Statement**: Traditional distribution optimization targets voltage support and loss minimization
  but does not explicitly integrate resilience (contingency survivability) as an objective within
  the same optimization function.
- **Caused by**: O1, O2.
- **Existing attempts**: Resilience curves (triangular/trapezoidal) visualize response but "exhibit
  limitations in accurately capturing the full complexity of system behavior" (§2, p.4); smart-grid
  monitoring and AI response optimization exist but are not framed as a single multi-objective search.
- **Why they fail**: They separate steady-state power-flow optimization from resilience assessment,
  so contingency performance is not directly optimized.

### G2: No unified framework links conventional power-flow optimization to resilience assessment
- **Statement**: There is a missing multi-objective function that combines voltage regulation,
  active-power-loss reduction, AND a resilience-oriented penalty in one optimization.
- **Caused by**: O3, G1.
- **Existing attempts**: Weighted objectives for voltage/loss exist; resilience penalties for DER
  contingencies are not standard.
- **Why they fail**: Without a penalty term for voltage collapse / branch overload under DER faults,
  the optimizer has no incentive to improve contingency (N-k) performance.

## Key Insight
- **Insight**: Add a third, resilience-oriented penalty term (f3) that penalizes configurations
  leading to voltage collapse or branch overloads during DER contingencies, and fold it into a
  single weighted objective F = w1·f1 + w2·f2 + w3·f3 alongside voltage-profile (f1) and loss (f2)
  terms — thereby linking conventional power-flow optimization directly with resilience assessment.
- **Derived from**: O1, O2, O3, G1, G2.
- **Enables**: A GA that searches DER setpoints and reconfiguration actions to improve steady-state
  performance AND contingency survivability simultaneously.

## Assumptions
- A1: DER (PV) units are dispatchable/controllable sources within fixed inverter limits; variability
  and stochastic profiles are deferred to future work (§4, p.8).
- A2: Loads are constant-power at buses 2–6 (Table 2).
- A3: The network is radial; only radiality-preserving reconfiguration is admissible (§5, p.8).
- A4: The proof of concept is a single simplified 6-bus feeder; results are demonstrative, not yet
  validated on standard IEEE feeders (§7, p.12).
- A5: A single, fixed weight vector (w1, w2, w3) = (0.4, 0.4, 0.2) encodes the priority tradeoff.
