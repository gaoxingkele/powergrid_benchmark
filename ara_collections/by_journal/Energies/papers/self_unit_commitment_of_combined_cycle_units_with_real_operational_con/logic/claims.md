# Claims

## C01: Representing a combined-cycle plant as individual coupled units, rather than one aggregate entity, exposes a unit-level dispatch that respects per-unit coupling an aggregate model structurally cannot express
- **Statement**: When a CCGT is modelled as separate gas- and steam-turbine units carrying configuration-style coupling constraints (minimum gas units per steam unit, per-unit output limits, per-unit ramps), the resulting commitment plan resolves each turbine's individual contribution and enforces couplings — like the steam-to-gas unit-count relationship — that an aggregate/mode representation abstracts away; the mechanism is that feasibility of the whole plant is governed by per-unit states that only a component-resolved model can carry.
- **Conditions**: Holds for a CCGT with multiple gas turbines feeding shared steam turbines through common HRSGs (here a 5 × 2 plant with identical units); assumes a constant steam-to-gas factor. Untested boundary: heterogeneous units and variable steam-to-gas ratios are not evaluated.
- **Sources**: [5 gas + 2 steam ← Table 1 «NC 5 p.u.» / «NS 2 p.u.» [input]; 0.613 ← Table 1 «STF 0.613 p.u.» [input]]
- **Status**: supported
- **Falsification criteria**: If an aggregate/mode CCGT model could reproduce the same per-unit dispatch and honour the minimum-gas-units-per-steam-unit and load-distribution couplings without any component-level variables, the granular representation would carry no additional information and the claim would fail.
- **Proof**: [E01, E02, E04]
- **Evidence basis**: Figures 5 and 7 show the per-unit decomposition (GT1–GT5, ST1, ST2) the model produces; Figure 3 shows the modelled 5 × 2 topology; Eqs. (7)–(10) encode the steam–gas unit-count coupling. Aggregate heuristic curves in Figures 4/6 show only bulk output.
- **Tags**: component-vs-mode, granular-modeling, coupling

## C02: A CCGT startup trajectory is feasible only for the thermal state the unit is actually in, so a schedule that assumes a hotter state than the plant occupies cannot be physically followed
- **Statement**: Because startup ramps are thermal-state-dependent (hot/warm/cold), the set of achievable output trajectories is fixed by how long the unit has been offline; a dispatch that assumes a hot start when the unit is in a warm or cold state prescribes a rise the plant cannot realise, forcing deviation from the program and risking thermo-mechanical damage. The mechanism is that thermal state gates the admissible ramp, not operator choice.
- **Conditions**: Holds for thermal units following predetermined hot/warm/cold ramp block sequences (Table 2) with state windows set by downtime thresholds (t1/t2/t3, KGC); demonstrated on two initial-condition scenarios. Untested boundary: continuous (sub-hourly) thermal dynamics and units with different ramp block tables.
- **Sources**: [t≤16 / 16<t≤30 / t>30 ← Table 1 «t1 t <= 16 Hours» / «t2 16 < t <= 30 Hours» / «t3 t > 30 Hours» [input]; 6 blocks cold vs 4 hot ← Table 2 «H4 210 … H6 … 210» [input]]
- **Status**: supported
- **Falsification criteria**: Observe a real CCGT (or a higher-fidelity thermodynamic simulator) start from a cold/warm thermal state and successfully follow a hot-startup ramp without exceeding steam temperature/pressure limits or incurring damage — that would refute the state-gates-the-ramp mechanism.
- **Proof**: [E01, E02, E03]
- **Evidence basis**: Case I uses a hot startup ramp, Case II requires a warm startup (Figures 4, 6); the heuristic opts for a hot startup regardless of prior state (§3.2), which the paper links to equipment damage (Figure 1). Table 2 gives the differing block counts per thermal state.
- **Tags**: startup-ramps, thermal-state, feasibility

## C03: Gating steam-turbine startup on a minimum number of gas-turbine operating hours delays and reshapes the feasible startup, because the steam turbine cannot start until the gas turbines have supplied heat long enough to reach the required steam conditions
- **Statement**: Requiring that gas turbines run a minimum number of hours (and a minimum count of units) before a steam turbine may start imposes a temporal precedence in the commitment plan: steam contribution is deferred until the thermal prerequisite is met, so the plant's ramp to full output is bounded by this coupling rather than by the steam turbine's own ramp alone. The mechanism is heat-accumulation timing between the gas and steam stages.
- **Conditions**: Holds for HRSG-coupled CCGTs where steam is raised from gas-turbine exhaust; the required lead time and gas-unit count are parameters (KGC, KMH, MUG). Untested boundary: plants with supplementary firing sufficient to raise steam independently, or storage that decouples the timing.
- **Sources**: [3 h ← Table 1 «KGC 3 Hours» / §3.1 «necessitating at least 3 h of operation from the gas units» [input]; 2 units ← Table 1 «MUG 2 p.u.» [input]; 9 h ← §2.6 «a hot start cannot be performed unless the steam turbine has been dispatched within the preceding 9 h» [input]]
- **Status**: supported
- **Falsification criteria**: If a steam turbine could be brought to its rated conditions and dispatched with no minimum gas-turbine lead time (gas units just started, below the required hours) without violating steam temperature/pressure limits, the minimum-hours coupling would be unnecessary and the claim would fail.
- **Proof**: [E01, E02]
- **Evidence basis**: §3.1 states ST2 undergoes a cold startup "necessitating at least 3 h of operation from the gas units"; Eqs. (33)–(37) encode the 9 h / 6 h / KMH / MUG gating; Figure 2 shows the downtime-threshold state machine.
- **Tags**: gas-steam-coupling, minimum-hours, startup-precedence

## C04: Supplementary firing decouples a steam turbine's output boost from its gas turbines' fuel output, letting the plant reach maximum capacity without raising gas-turbine output
- **Statement**: By adding heat at the HRSG, supplementary fires raise steam-turbine output independently of the gas-turbine power level, so the plant can meet a peak requirement through extra steam rather than more gas-turbine generation. The mechanism is that the HRSG provides a second, gas-output-independent lever on steam production.
- **Conditions**: Holds while steam quality is maintained and each gas unit's supplementary fire is within its cap (PAF); demonstrated at the plant's maximum-capacity periods. Untested boundary: sustained heavy supplementary firing and its effect on steam quality (assumed maintained, not measured).
- **Sources**: [4.75 MW ← §3.2 «including one supplementary fire, contributing an additional 4.75 MW» [result]; 15 MW cap ← Table 1 «PAF 15 MW» [input]]
- **Status**: supported
- **Falsification criteria**: If activating a supplementary fire failed to increase steam-turbine output at fixed gas-turbine output (or only did so by raising gas output), the decoupling mechanism would be refuted.
- **Proof**: [E04]
- **Evidence basis**: §3.2 reports one supplementary fire contributing an additional 4.75 MW to reach maximum capacity in Case II; Eqs. (14)–(15) define supplementary-fire contribution to steam output bounded by PAF; Figure 7 shows the full-output periods.
- **Tags**: supplementary-fire, HRSG, capacity

## C05: Penalising the pairwise output difference between gas turbines that are both above technical minimum drives an even load distribution, which the paper links to reduced steam-rotor thermal stress
- **Statement**: Introducing an objective penalty on the absolute output difference between any two gas turbines (active only when both are above technical minimum) pushes the optimum toward equal loading; because the shared collector mixes steam from all gas turbines, equal gas loading yields uniform steam thermal characteristics and, per the paper, lower rotor temperature gradients and less long-term damage. The mechanism is that objective-level penalisation of a physical asymmetry propagates to a thermal-uniformity outcome.
- **Conditions**: Holds when gas turbines share a common steam collector and the ISO does not force asymmetric output; the difference is only counted when both units exceed technical minimum. Untested boundary: the damage-reduction link is argued from plant experience, not quantified; grid conditions may force uneven loading in practice.
- **Sources**: []
- **Status**: hypothesis
- **Falsification criteria**: Measure rotor thermal stress under enforced even vs uneven gas-turbine loading and find no difference — that would refute the even-loading-reduces-stress mechanism the constraint is designed to exploit.
- **Proof**: [E04]
- **Evidence basis**: Eqs. (41)–(46) define the pairwise-difference variable, the both-above-minimum indicator δ, and its penalisation via DSC in the objective (Eq. 1); §2.7 argues the thermal-uniformity rationale; Figures 5/7 show near-equal gas-turbine outputs (~100 MW each) at full load.
- **Dependencies**: C01
- **Tags**: load-distribution, thermal-stress, objective-penalty

## C06: A dispatch produced by a model that omits ramp and thermal-state constraints is not merely less accurate but economically penalised, because the gap between the unfollowable schedule and realisable output crosses the market deviation threshold
- **Statement**: When the scheduling model ignores the plant's real ramp/thermal constraints, the realisable generation departs from the scheduled generation by more than the market's tolerated deviation, converting a modelling omission into a recurring monetary penalty (and a need for balancing reserves). The mechanism is that infeasible schedules are settled against actual output, so physical infeasibility is priced.
- **Conditions**: Holds under a market that penalises deviations beyond a fixed percentage (Colombian rule, 5%) and settles against actual generation; magnitude scales with startup frequency. Untested boundary: markets with different deviation rules or intraday re-dispatch that absorbs the gap.
- **Sources**: [5% ← §3.1 «deviations exceeding five percent between the heuristic and actual generation are penalized» [input]; USD 60,957 ← §3.1 «this would result in a daily penalty of USD 60,957 for Case I» [result]; USD 66,093 ← §3.2 «we found daily penalties amounting to USD 66,093» [result]]
- **Status**: supported
- **Falsification criteria**: If a heuristic-scheduled CCGT could track its program within the 5% band despite omitting ramp/thermal constraints (i.e., the omitted constraints never bind), no penalty would arise and the claim would fail.
- **Proof**: [E03]
- **Evidence basis**: §3.1/§3.2 compute daily penalties (USD 60,957 for Case I; USD 66,093 for Case II) from the model-vs-heuristic deviation using the PCC price and the 5% rule of ref [25]; Figures 4/6 show the diverging trajectories.
- **Dependencies**: C02
- **Tags**: deviation-penalty, market-settlement, economics
