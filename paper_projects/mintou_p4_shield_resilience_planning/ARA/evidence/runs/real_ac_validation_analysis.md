# SimBench AC Load-Flow Validation - P4 SHIELD-MOEA

Status: `public_cross_family_ac_validation_v3_simbench_cigre_ieee33`. pandapower AC power flow on four SimBench MV networks
plus the independent CIGRE MV and IEEE 33-bus network families across
6 stress scenarios (1-MV-rural--0-sw, 1-MV-semiurb--0-sw, 1-MV-urban--0-sw, 1-MV-comm--0-sw, pandapower-cigre-mv, pandapower-ieee33),
validating the compromise-plan compositions exported by the real-MOEA
planning pipeline (`real_simbench_planning_compromise_compositions.csv`,
seed-0 compromise solution per method/experiment).

## Headline

- No-Plan reference AC-feasible rate: `0.388889` (stress-only: `0.333333`)
- `SHIELD-MOEA` AC-feasible rate: `0.685185` (stress-only: `0.622222`)
- Best baseline: `NSGA-II+Repair` with `0.694444` (stress-only: `0.633333`)
- `SHIELD-MOEA` mean min voltage: `0.969017` pu vs No-Plan `0.939739` pu
- `SHIELD-MOEA` mean max line loading: `52.6508%` vs No-Plan `78.6284%`

## Summary Table

| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |
|---|---|---|---|---|---|---|
| NoPlan | reference | 0.388889 | 0.333333 | 0.939739 | 78.6284 | 0.568707 |
| NSGA-II+Repair | baseline | 0.694444 | 0.633333 | 0.968824 | 52.6568 | 0.373346 |
| Ablation-NoRepair | ablation | 0.694444 | 0.633333 | 0.968988 | 54.2987 | 0.383906 |
| SHIELD-MOEA | proposed | 0.685185 | 0.622222 | 0.969017 | 52.6508 | 0.376904 |
| Ablation-NoResilienceObj | ablation | 0.685185 | 0.622222 | 0.969522 | 55.9803 | 0.384360 |
| NSGA-II | baseline | 0.666667 | 0.611111 | 0.967390 | 52.7615 | 0.376201 |
| GA | baseline | 0.666667 | 0.600000 | 0.968648 | 48.0520 | 0.361837 |
| Ablation-NoScenarioScreen | ablation | 0.629630 | 0.566667 | 0.965061 | 51.4980 | 0.390451 |
| Ablation-NoOutage | ablation | 0.574074 | 0.533333 | 0.968639 | 66.9942 | 0.462712 |
| Weighted Sum | baseline | 0.416667 | 0.333333 | 0.944572 | 73.7100 | 0.536747 |
| Deterministic Planning | baseline | 0.416667 | 0.400000 | 0.971322 | 132.0397 | 1.193695 |
| MOEA/D | baseline | 0.388889 | 0.333333 | 0.939739 | 78.6284 | 0.568707 |

## Mapping Assumptions (read before citing)

Planning candidates live on aggregated SimBench subnet statistics, so plan
*compositions* (action-kind counts) are mapped onto concrete MV networks with
fixed, method-independent rules: reinforcement adds a parallel conductor on the
most-loaded lines; storage connects at the weakest-voltage load buses
(+/-3% of net load, discharging under load stress and charging
under DER stress); DER adds PV at the highest-load buses (4% of net
load, scaled with the scenario DER factor); automation has no steady-state
electrical effect. This validates whether each method's plan mix restores or
preserves AC feasibility under stress; it is not a nodal siting/sizing study.

## Interpretation

- `ac_feasible` requires convergence, all bus voltages within [0.95, 1.05] pu,
  and no line above 100% loading.
- The peak_n1_outage scenario drops the highest-loaded line whose outage leaves
  all buses supplied (radial spurs are skipped).
- Scenario axis doubles as a sensitivity analysis over load growth and DER
  penetration; per-scenario rows are in the results CSV.
