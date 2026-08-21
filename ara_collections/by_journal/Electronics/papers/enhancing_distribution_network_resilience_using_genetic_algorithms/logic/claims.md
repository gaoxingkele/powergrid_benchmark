# Claims

Claims distill the mechanism/relationship each result reveals. Exact numbers live in `evidence/` and
are reached via `Proof`/`Evidence basis`; `**Sources**` entries ground each load-bearing number with
a verbatim quote from the paper.

## C01: Folding a resilience penalty into a weighted multi-objective GA lets one optimizer improve steady-state and contingency performance together
- **Statement**: When network control is posed as a single weighted objective that adds a
  contingency-penalty term to the conventional voltage-profile and loss terms, an evolutionary
  search over DER setpoints and radiality-preserving reconfiguration can move steady-state operation
  and disturbance survivability in the same direction, because both are governed by the same
  underlying DER-dispatch and topology levers rather than being separate design problems.
- **Conditions**: Radial distribution feeder with dispatchable DERs at multiple buses; a fixed
  priority weighting between the terms; demonstrated on one small proof-of-concept feeder — untested
  whether the joint improvement holds when the steady-state and resilience optima conflict more
  sharply (e.g. larger meshed networks, stochastic DER output, or heavier weighting of one term).
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A feeder on which adding the f3 resilience-penalty term to the objective
  leaves contingency metrics (min voltage / overloaded branches / load served under a DER trip)
  no better than optimizing f1+f2 alone, or degrades steady-state voltage/loss to buy the resilience
  gain, would refute the claim that the terms co-improve.
- **Proof**: [E01, E02, E03, E04]
- **Evidence basis**: The same GA run yields both the steady-state gains (Table 3 voltage profile,
  Table 4 losses) and the contingency gains (Table 6), demonstrating one optimizer serving both
  objectives; framing in §5 objective function and §6 results.
- **Tags**: multi-objective, genetic-algorithm, resilience-penalty, distribution-network

## C02: GA-coordinated DER dispatch corrects the downstream voltage sag characteristic of radial feeders, with benefit growing along the feeder
- **Statement**: Coordinated reactive/real DER dispatch selected by the optimizer raises bus voltages
  most where the radial feeder sags most — at buses electrically farthest from the substation — so the
  voltage-profile improvement is not uniform but increases with distance down the feeder, pulling the
  whole profile back inside the operational band.
- **Conditions**: Radial feeder with monotonically rising line R/X downstream and DERs sited at
  mid-feeder buses; holds for the tested static load snapshot — boundary at time-varying load and
  stochastic DER output is untested.
- **Sources**: [0.95 ← §5 objective, p.9 «0.95 ≤ Vi ≤ 1.05» [input]]
- **Status**: supported
- **Falsification criteria**: A radial feeder where the optimized profile fails to keep all bus
  voltages within the 0.95–1.05 pu band, or where the base-vs-optimized voltage gap does not widen
  with electrical distance from the substation, would refute the mechanism.
- **Proof**: [E01]
- **Evidence basis**: Table 3 / Figure 4 — base case declines monotonically to the lowest voltage at
  the farthest bus while the optimized curve stays in-band and the two curves diverge progressively
  downstream (base bus 6 = 0.92 pu, optimized bus 6 = 0.97 pu).
- **Dependencies**: C05
- **Tags**: voltage-regulation, radial-feeder, DER-dispatch, voltage-profile

## C03: Loss reduction from evolutionary DER-dispatch search accrues mostly in the early generations, converging smoothly without oscillation
- **Statement**: Searching DER injection/reconfiguration to minimize resistive line losses exhibits a
  single-elbow convergence — most of the achievable loss reduction is captured in the first fraction
  of generations and the remainder is refined by a slow monotonic tail — indicating the objective
  surface for this class of radial-feeder loss problem is dominated by a few high-leverage dispatch
  decisions rather than many marginal ones.
- **Conditions**: GA with the stated population/crossover/mutation regime on a small radial feeder;
  the "early-generations dominate" shape is observed for this loss objective and is not established
  for larger feeders or different fitness weightings.
- **Sources**: [55.3 ← §6 results, p.10 «total losses of 55.3 kilowatts» [result]; 29.7 ← §6 results, p.10 «these losses dropped to 29.7 kilowatts» [result]; 46.3 ← §6 results, p.10 «representing a reduction of approximately 46.3 percent» [result]]
- **Status**: supported
- **Falsification criteria**: A convergence trace on a comparable feeder showing oscillatory or
  late-breaking loss reduction (large gains after the elbow), or no meaningful loss reduction versus
  the un-optimized feeder, would refute the "early-dominant, smooth" characterization.
- **Proof**: [E02]
- **Evidence basis**: Figure 5 convergence curve (steep drop over the first ~20 generations, then a
  slow tail to ~gen 100) and Table 4 endpoints (55.3 kW → 29.7 kW, ≈46.3% reduction).
- **Tags**: convergence, power-loss, genetic-algorithm, optimization-landscape

## C04: An explicit contingency-penalty term converts a steady-state optimizer into one that also shields the network against a DER-outage disturbance
- **Statement**: Penalizing configurations that would cause voltage collapse or branch overload under
  a DER fault steers the optimizer toward dispatch/topology choices that keep post-disturbance
  voltages shallower, avoid thermal overloads, and preserve load service — i.e. the resilience gain is
  a direct consequence of pricing contingency behavior into the objective, not a by-product of better
  nominal operation alone.
- **Conditions**: Single DER-trip contingency (fault-induced trip at one mid-feeder bus) on a radial
  feeder; established for one contingency on one feeder — behavior under simultaneous multi-DER or
  line contingencies (fuller N-k) is untested.
- **Sources**: [100 ← abstract, p.1 «the optimized configuration preserves 100% load delivery» [result]; 89 ← abstract, p.1 «compared to 89% in the base case» [result]]
- **Status**: supported
- **Falsification criteria**: A DER-outage test in which the resilience-penalized optimum leaves
  overloaded branches, drops load below the un-penalized configuration, or shows no shallower voltage
  dip than steady-state-only optimization would refute that the f3 term buys contingency robustness.
- **Proof**: [E03, E04]
- **Evidence basis**: Table 6 — under a DER trip at bus 3 the optimized case holds 0.94 pu min
  voltage, 0 overloaded branches, and 100% load served, versus 0.88 pu, 2 overloads, and 89% for the
  base case; mapped onto the trapezoidal resilience curve (shallower degradation, faster recovery).
- **Dependencies**: C01
- **Tags**: resilience, contingency, N-k, load-served, penalty-term

## C05: In a radial feeder, DER reactive absorption is the lever for voltage support and central real-power injection is the lever for loss/flow balance
- **Statement**: The optimizer's dispatch pattern reveals two distinct levers — DER units set to
  absorb reactive power counteract inductive loads and line reactance to hold up voltage, while the
  largest real-power injection is placed at the electrically central bus to balance power flow and cut
  resistive losses — so voltage support and loss reduction are served by different, separable dispatch
  degrees of freedom kept within inverter capacity.
- **Conditions**: Radial feeder with DERs at mid-feeder buses and inverter apparent-power limits;
  inferred from a single optimized dispatch snapshot — not shown to generalize across loading levels
  or DER sitings.
- **Sources**: [130 ← Table 5, p.11 «3 130 −30» (P_DER at bus 3 = 130 kW) [result]]
- **Status**: supported
- **Falsification criteria**: An optimized dispatch on a comparable feeder that achieves the same
  voltage/loss gains with net reactive injection (positive Q) at DER buses, or with the largest real
  injection at a feeder-end rather than central bus, would refute the claimed lever assignment.
- **Proof**: [E04]
- **Evidence basis**: Table 5 — all three DERs take negative Q (−20/−30/−15 kVAR) and the largest P
  (130 kW) sits at the central bus 3; §6 narrative attributing voltage support to reactive absorption
  and flow balance to central real injection.
- **Tags**: DER-dispatch, reactive-power, voltage-support, loss-minimization
