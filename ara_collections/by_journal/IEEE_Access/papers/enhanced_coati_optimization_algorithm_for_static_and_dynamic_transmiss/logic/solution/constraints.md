# Constraints, Assumptions, and Limitations

## Boundary conditions
- **Power-flow model**: DC power flow only — active power flow considered; line resistances and
  reactive flow neglected. Computed via MATPOWER 6.0. Chosen for fast solutions with "acceptable
  accuracy"; AC flow is acknowledged as more realistic but more complex and is not used.
- **Constraint handling**: equality (nodal power balance) and inequality (line-flow, generation,
  line-number limits) constraints are enforced softly through additive penalty terms (ω₁, λ₁, λ₂,
  λ₃), not as hard constraints. Penalty weights are fixed per test system.
- **Line-addition limit**: maximum number of parallel transmission lines between any two buses = 4
  for all three test systems.
- **Slack/oscillation bus**: bus 1 for Garver 6-bus; specified per system for IEEE-25 and Colombian.
- **Termination**: benchmark runs terminate at maxFEs = 10000 × Dim; TNEP convergence curves shown
  over ~90 iterations.
- **Dynamic case**: base year 2002; annual interest rate I = 10%; three planning stages
  (2002–2005, 2005–2009, 2009–2012).

## Assumptions
- A1: Test-system cost coefficients are "general"/simplified and "may not be very significantly
  different from the actual cost volatility"; fixed per-km or per-line costs are assumed and
  operational/geographical features (terrain, land, zoning, inflation) are omitted for benchmarking.
- A2: DC power flow adequately approximates the network for planning-cost comparison.
- A3: The FDB weighting coefficient ω and I ∈ {1,2} selection are as defined by the source methods;
  ω's numeric value is not specified.
- A4: OBL is applied only in the initial-population creation phase (not during search phases).
- A5: For the dynamic case, demand basis years are 2002, 2005, 2009.

## Known limitations (stated or evidenced by the paper)
- **No universal dominance (NFL)**: the enhanced variants lose/tie on a residual set of benchmark
  problems (FDBCOA1 loses 6/282, ties 110; FDBCOA1-OBL5 loses 4/282, ties 96); losses concentrate
  at low dimensions and large population sizes (P=100).
- **Placement sensitivity**: only three FDB placements and eight OBL schemes were tested; FDBCOA3
  exhibits "severe scalability problems"; placement in the exploitation update (Eq. 22) was not
  tested.
- **OBL applied only at initialization**: the authors name applying OBL during local/global search
  phases as future work — the current benefit is limited to seeding.
- **Not the cheapest on every TNEP case**: on the Colombian 93-bus system the proposed method ranks
  second to HGA on investment cost (US$497,157,143.3 vs HGA US$491,010,000), though it achieves
  0.00 MW load shedding whereas HGA has 0.41 MW.
- **Real-world scaling caveats**: cost figures are test-system simplifications; realistic
  application would need inflation, regional cost differences, maintenance/repair costs, reliability
  indices, and environmental impacts (named as future extensions).
- **Model omissions**: AC power flow, N-1 security/reliability, and stochastic demand/renewable
  scenarios are not modeled in the solved cases.
- **Cost variance can be high**: worst-case costs are far above best/optimal (e.g. Garver without
  resizing best US$200,000 vs worst US$452,000; IEEE-25 with resizing best US$9,780,000 vs worst
  US$267,508,000), so a single run is not guaranteed optimal — motivating the 51-run protocol.
