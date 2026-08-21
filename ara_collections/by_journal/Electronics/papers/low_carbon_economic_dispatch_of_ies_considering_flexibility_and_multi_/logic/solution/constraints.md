# Constraints, Assumptions, and Limitations

## Model constraints (from §3, equation numbers per source)

### Upper-level (IES operator)
- **Electric power balance**, Eq. (12): P_e^t + P_{e.WT}^t + P_{e.PV}^t + P_{e.GT}^t + P_{e.BT.dis}^t + P_{e.EV.dis}^t = P_{e.load}^t + P_{e.EC}^t + P_{e.EH}^t + P_{e.BT.chr}^t + P_{e.EV.chr}^t
- **Thermal power balance**, Eq. (13): P_{h.GT}^t + P_{h.EB}^t + P_{h.HST.dis}^t = P_{h.load}^t + P_{h.AC}^t + P_{h.HST.chr}^t
- **Cooling power balance**, Eq. (14): P_{q.AC}^t + P_{q.EC}^t = P_{q.load}^t
- **Renewable output bounds**, Eq. (15): 0 ≤ P_{e.WT}^t ≤ P_{e.WT}^{t.max}; 0 ≤ P_{e.PV}^t ≤ P_{e.PV}^{t.max}
- **Device output + ramping bounds**, Eq. (16): −P_j^{down} ≤ P_j^t − P_j^{t−1} ≤ P_j^{up}; P_j^{min} ≤ P_j^t ≤ P_j^{max} (gas turbines, electric boilers, absorption/electric chillers, batteries, heat-storage tanks). Concrete capacities/ramp rates in Table 1 (e.g. gas turbine 1000 kW, ramp 25%).

### Lower-level
- **EV SoC dynamics + charge/discharge bounds**, Eq. (20): S_EV^t = S_EV^{t−1}(1−γ_EV) + (η_{EV.chr} p_{e.EV.chr}^t − p_{e.EV.dis}^t/η_{EV.dis}); S_EV^min ≤ S_EV ≤ S_EV^max; I_{EV.chr} p_{e.EV.chr}^min ≤ p_{e.EV.chr} ≤ I_{EV.chr} p_{e.EV.chr}^max; I_{EV.dis} p_{e.EV.dis}^min ≤ p_{e.EV.dis} ≤ I_{EV.dis} p_{e.EV.dis}^max (binary charge/discharge identifiers).
- **Translatable-load bounds**, Eq. (23): P_{i.in}^t ≤ k1 P_{i.pri}^t; P_{i.out}^t ≤ k2 P_{i.pri}^t; total energy conserved within an operating cycle.
- **Reducible-load bound**, Eq. (24): P_{i.cut}^t ≤ k3 P_{i.pri}^t.
- **Substitutable-load bound**, Eq. (25): printed as P_{i.cut}^t ≤ k3 P_{i.pri}^t (see limitation L5).

## Assumptions
- A1: Deterministic typical-day (24 h) forecasts; no scenario/stochastic uncertainty modeled.
- A2: EVs aggregated into 5 fixed categories with deterministic connection windows/capacities/proportions (Table 4).
- A3: Lower-level model solvable to optimality by CPLEX 12.10 each iteration (assumed linear/convex).
- A4: Flexibility weights ω_e,ω_h,ω_q ∈ (0,1), sum to 1 (Eq. 11); their values are not specified.
- A5: Shiftable-load total energy conserved over an operating cycle (§3.2.2).
- A6: Carbon/green-certificate coefficients (α_GCT, κ_GCT, σ1–σ4, λ_GCT, λ_CET) taken from ref [29]; concrete values not reproduced in this paper.

## Known limitations (paper-stated and observed)
- L1: **Scope** — study is park-level IES; the authors state it has only "certain reference value" for regional-level IES, which is left as future work (§5).
- L2: **Deterministic** — flexibility indicators and EV aggregation are deterministic; the authors note they could be expressed with probabilistic indicators to address randomness (future work, §5).
- L3: **Data realism** — the authors call for updated, realistic electricity costs and device parameters to empirically verify results (§5).
- L4: **Unspecified parameters** — flexibility objective weights, GCT/CET coefficients, and PSO w_max/w_min bounds for Eq. (26) are not given numerically (marked "Not specified in paper").
- L5: **Eq. (25) typo** — the substitutable-load constraint is printed identically to Eq. (24) though its text describes a load-conversion constraint (variable P_ij^t, conversion ratio φ); treated as a source typesetting error.
- L6: **Internal numeric inconsistency** — the Abstract reports a 52.0% iteration reduction while §4.3/§5 report 54.0% (the 54.0% matches the 100→46 iteration data). Recorded in evidence/README.md and figure16.md.
- L7: **Three modeled entity classes only** — operator, aggregator, EVs; gas-network operators and other stakeholders are out of scope.
