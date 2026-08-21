# Constraints, Assumptions, and Limitations

## Boundary conditions
- **Test system**: 24-bus, 26-generator IEEE Reliability Test System (RTS); total installed/available capacity 3105 MW; peak forecasted demand 2670 MW at hour 11.
- **Contingency scope**: N-1 thermal-generator contingencies only — the forced outage of exactly one generating unit at a time. Nine distinct generator contingencies (by capacity/bus) are indexed Cy = 1..9.
- **Reserve settings studied**: 10% (Case 1, CM 310.5 MW), 8% (Case 2a, 248 MW), 5% (Case 2b, 155 MW), 0% (Case 2c, 0 MW) spinning reserve.
- **Reliability threshold**: LOLP_max = 0.05 (CEA India). Operating margin and reliability judgments are relative to this value.
- **Optimizer**: Dynamic Programming, implemented in MATLAB.

## Modeling assumptions (from §V-A and §III)
- A1: Only one unit fails at a time; no simultaneous outages of single units of other ratings (avoids compounded shutdown/startup/maintenance costs; periodic maintenance keeps all units available).
- A2: The conditional probability of one generator outage together with other generators is not considered.
- A3: LOLP is assessed for the forced outage of only one generating unit at a time; outages of more than one unit are not considered for LOLP.
- A4: Conditional probabilities between various generators are not modeled; their impact is deemed negligible.
- A5: DC power flow assumed for the supply-demand balance (Eq. 2).
- A6: Maintenance cost is neglected in the objective (Eq. 1).
- A7: LOLP_max = 0.05, assuming the system operates under strict limits.

## Constraint set (referenced, see formulation.md for equations)
- Supply-demand balance (Eq. 2): committed generation equals forecasted demand each hour.
- Generator fuel cost quadratic in output (Eq. 3).
- Start-up cost = turbine + boiler (with cool-down term) + maintenance start-up (Eq. 4).
- Ramp-up / ramp-down limits (Eq. 5, 6).
- Spinning reserve ≥ 10% (Eq. 7, Case 1).
- Available capacity = max capacity − reserve (Eq. 8).
- Shutdown cost, minimum up-time, minimum down-time, active-power limits: referred from author's prior work [27], not re-derived here.

## Known limitations
- L1: Scope is limited to single thermal-generator contingencies; N-k / simultaneous and transmission-line contingencies are out of scope (flagged for future work).
- L2: Renewable-generation uncertainty and distributed energy resources (DER) are not modeled; only thermal generators are considered.
- L3: Conditional/correlated generator failure probabilities are ignored; the LOLP analysis assumes independent single-unit outages.
- L4: DC power-flow approximation; no AC voltage/reactive constraints, no explicit transmission-line loading limits in the contingency screening.
- L5: Operating margin is derived from the aggregated 24-hour LOLP and a fixed LOLP_max; it does not capture the severity of any individual single contingency, nor time-localized risk within the day.
- L6: Validated on one test system (IEEE RTS) at one demand profile; generalization to larger/more complex or capacity-rich systems is stated as beneficial future work but not demonstrated.
- L7: Solver hardware, runtime, and DP state-space details are not reported; reproducibility relies on the cited generator data and prior-work constraint formulations.
- L8: The 0% CM (Case 2c) case, while most economical and most reliable by LOLP, carries a higher risk of cascading failures/collapse because no headroom remains for further disturbances — a limitation of interpreting LOLP/margin in isolation.
