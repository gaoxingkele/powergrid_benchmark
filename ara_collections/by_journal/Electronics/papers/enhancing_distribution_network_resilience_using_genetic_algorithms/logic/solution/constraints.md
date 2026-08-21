# Constraints, Assumptions, and Limitations

## Boundary conditions (operational / optimization)
- **Bus voltage band**: 0.95 ≤ V_i ≤ 1.05 pu for all buses (§5, p.9). Optimization drives voltages
  into this band; violations outside it are penalized in the fitness.
- **Line thermal limits**: line currents must not exceed branch thermal capacity (Table 1: 200 A on
  all lines L1–L5).
- **DER inverter limits**: 0 ≤ P_DER,i ≤ P_max,i and |Q_DER,i| ≤ Q_max,i. The numeric P_max,i /
  Q_max,i values are **Not specified in paper** (stated as "specified maximum capacities").
- **Radiality**: reconfiguration must preserve the radial (single-path, loop-free) topology.

## Assumptions
- **A1 — Dispatchable DERs**: PV/DER units are treated as dispatchable, deterministic, controllable
  sources; variability and stochastic generation profiles are explicitly deferred to future work
  (§4, p.8).
- **A2 — Constant-power loads**: loads at buses 2–6 modeled as constant power (Table 2).
- **A3 — Fixed weighting**: a single weight vector (w1, w2, w3) = (0.4, 0.4, 0.2) encodes the
  priority tradeoff among voltage, loss, and resilience.
- **A4 — Single contingency**: the resilience assessment (Table 6) evaluates one fault-induced DER
  trip at bus 3, not a full N-k contingency sweep.
- **A5 — Deterministic snapshot**: a single static load/generation operating point; no time series.

## Known limitations (from §7 Conclusions and the text)
- **Small proof-of-concept system**: the test bed is a simplified 6-bus radial feeder; the authors
  state results "confirm the effectiveness and practicality" but generalization is not established.
  Future work will extend to standard IEEE feeders (13-bus, 33-bus) (§7, p.12).
- **No time-series / stochastic dynamics**: dynamic resilience under variable renewable generation
  and load is not captured; future work will incorporate time-series simulations (§7, p.12).
- **f3 form unspecified**: the resilience-penalty term is described qualitatively (penalize voltage
  collapse / overloads under DER faults); no explicit functional form or penalty weight-within-f3 is
  given, limiting exact reproducibility.
- **No released code/data**: implementation named (MATLAB R2025, PowerFactory 2024) but no code, seed,
  or dataset artifact is released (Data Availability Statement, p.12).
- **Internal labeling tension**: Table 4's base case is "(No DER)" while Table 6's base case is a
  DER-trip contingency and the abstract references an 89% base-case load delivery — the several
  "base cases" correspond to different operating points and are not cross-defined in one place.
- **Figure 3 vs Table 1 topology conflict**: Figure 3 as drawn shows the L5 diagonal originating
  at bus 3 and ending at bus 6, while Table 1 lists L5 as "5–6" and the §4 prose describes each
  bus connected to its upstream neighbor (a 1–…–6 chain). The paper does not reconcile the two;
  both readings are recorded (evidence/figures/figure3.md).
