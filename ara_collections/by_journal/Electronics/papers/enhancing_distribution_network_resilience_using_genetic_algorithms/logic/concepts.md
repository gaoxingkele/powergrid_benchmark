# Concepts

## Resilience (power distribution)
- **Notation**: —
- **Definition**: A system's ability to sustain performance during multiple component failures (per
  the N-k criterion) and to facilitate rapid recovery following extreme events. Distinguished in the
  paper from reliability (coping with one or two concurrent faults, N-1/N-2, and Low-Impact
  High-Frequency events), robustness (resistance to stress using existing infrastructure, without
  inherent post-failure recovery), and security (threat prevention, esp. cyber).
- **Boundary conditions**: No universally accepted definition; the paper adopts an N-k, recovery-
  oriented view and splits it into Operational Resilience (onset → partial restoration) and
  Infrastructure Resilience (partial → full restoration).
- **Related concepts**: Trapezoidal resilience curve, N-k criterion, HIHF events.

## Trapezoidal resilience curve
- **Notation**: functionality F(t) with levels F0 > F1 > F2 over event times t1…t5
- **Definition**: A graphical model of system functionality versus time through a disturbance, with
  distinct trapezoidal stages: normal operation, disruptive-event onset, degradation/system failure,
  partial recovery, plateau (state past partial recovery), full restoration, post-event normal
  operation. Preferred over the "triangular" curve for a more nuanced depiction of degradation and
  recovery stages.
- **Boundary conditions**: A conceptual/interpretive frame; the paper notes such curves have
  limitations in capturing the full complexity of system behavior and exact degradation magnitude.
- **Related concepts**: Resilience, Operational vs Infrastructure Resilience.

## N-k criterion
- **Notation**: N-k
- **Definition**: The requirement/assessment that a system sustains performance under simultaneous
  loss of k components. Resilience is framed against N-k (multiple failures); reliability against
  N-1/N-2 (one or two faults).
- **Boundary conditions**: Used qualitatively here; the case study evaluates a single DER-trip
  contingency rather than a full N-k sweep.
- **Related concepts**: Resilience, reliability, contingency.

## Distributed Energy Resource (DER)
- **Notation**: P_DER,i, Q_DER,i (real/reactive output at bus i)
- **Definition**: A controllable generation source (here PV) integrated at load buses, able to
  provide both real and reactive power within its inverter limits. In this study DERs at buses 2, 3,
  4 are the primary control variables the GA dispatches.
- **Boundary conditions**: Assumed dispatchable and deterministic; variability/stochastic profiles
  deferred to future work. Bounded by 0 ≤ P_DER,i ≤ P_max,i and |Q_DER,i| ≤ Q_max,i.
- **Related concepts**: Inverter capacity constraint, reactive power support, network reconfiguration.

## Weighted multi-objective function (F = w1·f1 + w2·f2 + w3·f3)
- **Notation**: F = w1·f1 + w2·f2 + w3·f3
- **Definition**: The scalarized fitness minimized by the GA, combining a voltage-profile term
  f1 = Σ_{i=1}^{6} |V_i − 1_pi|² (squared deviation from nominal), a loss term f2 = Σ_{k=1}^{5} I_k²·R_k
  (resistive line loss), and a resilience penalty f3 for configurations causing voltage collapse or
  overloads under DER faults, with weights (w1, w2, w3) = (0.4, 0.4, 0.2).
- **Boundary conditions**: Fixed weight vector; f3 is a penalty rather than an explicitly stated
  functional form (its exact expression is not given in the paper).
- **Related concepts**: Genetic Algorithm, resilience penalty, power flow constraints.

## Genetic Algorithm (GA)
- **Notation**: Ps (population), Np (crossover parts), Pm (mutation prob.), Nc (offspring per pair),
  Nmax (max generations), ee (mean error)
- **Definition**: A population-based evolutionary optimizer using reproduction, crossover, and
  mutation over binary-encoded chromosomes, followed by fitness-based natural selection retaining the
  Ps best individuals each generation, iterating until convergence (no significant improvement in
  mean error, or generations exceed Nmax).
- **Boundary conditions**: Binary encoding; selection minimizes the objective; termination on
  stagnation or generation cap. Here: population 50, crossover prob. 0.8, mutation rate 0.05, 100
  generations.
- **Related concepts**: Weighted multi-objective function, network reconfiguration.

## Network reconfiguration (radial)
- **Notation**: —
- **Definition**: Changing the on/off status of switchable branches to alter power-flow paths while
  preserving the radial (single-path, tree) structure of the feeder; one of the GA's control actions
  alongside DER setpoints and voltage-regulator taps.
- **Boundary conditions**: Must maintain radiality (no loops); the case study is a 6-bus radial
  feeder with a single path from source to each load.
- **Related concepts**: Radial distribution network, DER dispatch, operational constraints.
