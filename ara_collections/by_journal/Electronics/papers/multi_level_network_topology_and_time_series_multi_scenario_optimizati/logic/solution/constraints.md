# Constraints, Assumptions, and Limitations

## Boundary Conditions

- **Voltage architecture (topology design, §2.2)**: designs are built around a 750 V DC busbar fed
  from 10 kV DC mains (with 10 kV diesel backup where applicable), serving 380/220 V AC and
  336/240 V DC end equipment through load converters. Medium-voltage AC incoming is typically
  10 kV or 20 kV from 110 kV stations (§2.1).
- **MV-DC economic regime (§2.1)**: medium-voltage DC convergence is stated to be more economical
  when the convergence radius exceeds 5 km and the convergence capacity is not less than 10 MW.
- **UPS capacity rule (§2.2)**: in Tier IV power links UPS can be configured 2N or 2(N+1) and
  critical loads should not exceed 90% of N; in Tier C/I systems critical loads can reach 100% of
  N times a single machine's capacity.
- **Voltage-stability index domain (§3.1, Eq. 6)**: the index L_ab is defined for AC branches only;
  DC branches are assigned index 0 by construction (per §5.3, Figure 11 discussion).
- **Model constraints (§3.2, Eqs. 8–10)**: AC node power balance (Eq. 8), DC node power balance in
  the data center (Eq. 9), node voltage upper/lower limits, branch active-power limits, and DG/
  converter capacity limits 0 ≤ S_{i,g}·η_g ≤ P_{i,g,max} (Eq. 10). The constraint list in §3.2
  also names "capacity constraints for … energy storage devices", but no storage model or storage
  variable appears in the formulation.
- **Test-system scope (§5)**: a 13-node radial system (topology-evolution examples) and a modified
  IEEE33 system (planning examples: per-node DC-load proportions of Table 4; five added load
  points 33–37 totalling 600 kW + j320 kvar with DC-load proportions 0%, 30%, 50%, 70%, 100%;
  each new point connects to exactly one of the 32 non-balancing nodes by a single AC or DC line;
  all existing lines are DC-conversion candidates; DG candidate node set {7, 10, 12, 13, 14, 16,
  17, 18, 19, 20, 22, 23, 24, 25, 26, 29, 30, 31, 32}; DG installed in m × 60 kVA increments,
  m = 0…7). Both networks are radial; meshed networks are untested.

## Assumptions

- A1: DG output and load are representable by a finite set of probability-weighted typical
  time-series scenarios (the solution procedure iterates 12 typical scenarios × 48 daily slots);
  the algorithm generating these scenarios and their probabilities is not specified in the paper.
- A2: Converter cost is proportional to active capacity (Eq. 4); conversion efficiency 95% (§5.1).
- A3: DC branches carry no AC-type voltage-stability constraint (index 0), so hybridization can
  only shrink the AC stability exposure.
- A4: Economic parameters hold over the planning horizon — 13-node example: discount rate 7.5%,
  VSC unit capacity cost $170/kVA, line investment $28,000/km, planning life 15 years,
  conventional power output cost $100/MWh (§5.1); IEEE33 example: new AC line 70,000 RMB/km,
  new DC line 20,000 RMB/km (§5.2).
- A5: The assigned per-node DC-load proportions (Table 4) and 10%-per-cycle penetration growth
  (§5.1) are representative of future data-center-penetrated feeders.

## Known Limitations

- **Undefined f4 / lower-level objective**: the 14-step procedure (§4.2, step 4/7) penalizes "f1
  and f4" and computes fitness from a "lower-level objective function", implying a bi-level
  structure, but only f1–f3 are defined in §3.1 and f4 is never specified. Recorded as a gap
  (see method.md and trace node N16).
- **Scenario generation unspecified**: how the 12 typical time-series scenarios, their days-per-year
  weights d_j and probabilities p_{s,j} are derived from raw data is not specified in the paper.
- **No availability quantification**: the tier-to-architecture mapping (§2.2, Figures 1–5) is
  qualitative; no numeric availability/reliability figure is computed for any design.
- **Currency/parameter heterogeneity**: the 13-node example prices lines in $/km ($28,000/km)
  while the IEEE33 example prices them in RMB/km (70,000 AC / 20,000 DC); no exchange-rate or
  normalization is given.
- **No sensitivity analysis**: results are reported for single parameter settings; no sensitivity
  of the retrofit thresholds (e.g. the 40%→50% transition) to converter cost is reported.
- **Single regional case**: the practical-engineering evaluation (§5.4, Table 9) is a qualitative
  suggestion table for one region with no post-retrofit measurement.
- **No released code / runtime details**: no implementation, solver runtime, population size, or
  iteration counts for the reported runs are given (see src/environment.md).
- **Radial-network scope**: all quantitative results are on radial test systems; meshed networks,
  other converter-cost regimes, and penetration beyond 80% are untested.
