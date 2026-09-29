# P3 S5 Three-Round Scientific Closure

This internal provenance record documents the logic, methodology--statistics, and theory--innovation reviews performed against the P3 S3 evidence, P3 S4 canonical narrative manifest, current manuscript, and the read-only shared implementation. It is not a substitute for the manuscript or experiment evidence.

## Evidence inspected

- `manuscript/MANUSCRIPT.md` and `manuscript/DEEP_REVISION_EVIDENCE.md`;
- P3 S3 manifest, analysis, validation report, rerun fronts/index, robustness metrics and inference, clipping audit, and AC scope decision;
- P3 S4 canonical manifest, generated tables, and current result figures;
- read-only `src/powergrid_benchmark/mintou_real_planning.py` at the source hash recorded by the P3 S3 manifest;
- archived weak and near-miss histories retained in the canonical P3 evidence tree, including `real_simbench_planning_analysis_v1_weak.md` through `real_simbench_planning_analysis_v4_near_miss.md`.

No optimizer, AC power flow, parameter sweep, or new benchmark was run in P3 S5.

## Round 1: Logic review

| Finding | Evidence anchor | Disposition |
|---|---|---|
| The display labels "DER-only" and "Storage-only" contradicted the actual configuration contract because reinforcement and automation remain in both 54-variable pools. | Shared source `P3_EXPERIMENTS`, `experiment_pool`; manuscript Table 3; P3 S4 manifest. | Corrected to storage-excluded (DER-focused) and DER-excluded (storage-focused). All numerical results are unchanged. |
| The NoDER paragraph could be read as claiming a 36-coordinate genome, although the implementation retains the experiment's 72- or 54-coordinate genome and makes 36 action columns effectively selectable after the high-cost/mask treatment. | Shared source `method_search_mask`, `run_method`, and the P3 S3 runner's search-pool construction. | Corrected the method description; retained the limitation that NoDER is a problem variant rather than a component ablation. |
| The crowding discussion stated a clustering mechanism more strongly than the ablation identifies. | Shared source `CarsConfig(diversity=False)` and equal-configuration NoDiversity results. | Rewritten as an observed joint contrast: random truncation coincides with lower HV and smaller fronts; no unmeasured cluster-causality claim remains. |

Round-1 negative conclusion retained: the legacy clipped metric supports repair/diversity contrasts only in its declared scope, while FixedDE remains nominally ahead and the adaptive bundle remains unresolved.

## Round 2: Methodology--statistics review

| Finding | Evidence anchor | Disposition |
|---|---|---|
| The manuscript named optimizer seeds as analysis units but did not state as directly that configurations are the units for cross-configuration claims. | P3 S4 aggregation contract; six-configuration tables; seven seed-block inference families. | Added the two-level unit contract: seeds support within-block inference; six fixed configurations support descriptive cross-configuration summaries. The base replicate remains nested within the base configuration. |
| Direct Pareto-DE controls are fairer search-class comparators but not strict equal-function-evaluation controls. | Shared source GDE3/NSDE settings; 40-generation protocol; absent comparable pymoo `n_eval` counters. | Added the explicit fairness boundary. No evaluation-budget equivalence is claimed. |
| AC feasibility fractions could be misread as probabilities from 72 independent observations. | AC scope decision; three run-index-0 compositions per method; four networks x six fixed cases per composition. | Renamed the manuscript presentation to feasible-case fractions and repeated that the rows are dependent and descriptive. No p-value, interval, or optimizer-level physical-feasibility claim was introduced. |
| The legacy primary analysis reports effect sizes and bootstrap intervals in its archived supplement, whereas configuration-equal ranks are descriptive. | Canonical legacy inference table and P3 S3 robustness inference. | Clarified the methods/results boundary and did not manufacture intervals for the six fixed configurations. |

Round-2 null and adverse evidence retained: analytic HV reverses the NSGA-II+Repair ordering in three configurations; common-reference IGD+ favors CARS-MODE in only one; FixedDE remains nominally ahead on all three equal-configuration summaries; AC results do not cover GDE3, NSDE, or NSGA-II+Repair.

## Round 3: Theory--innovation review

| Finding | Evidence anchor | Disposition |
|---|---|---|
| Broad statements that DE is rare or proxy-to-AC mapping is generally asserted exceeded the selected literature table. | Related Work Sections 2.1--2.4 and Table 1. | Scoped the statements to the representative comparison set and explicitly rejected a systematic-census interpretation. |
| The paper integrates known jDE/SaDE ideas, repair, crowding, and a diagnostic workflow; it does not establish a new convergence theory or an individually identified adaptive mechanism. | Method Sections 4.1--4.4; FixedDE joint control; robustness results. | Narrowed the innovation claim to methodological integration and audit, in the gap statement and conclusion. |
| Shared generators could be mistaken for independent corroboration across P3 and P4. | Companion disclosure and shared source tree. | Retained the exact companion name `mintou_p4_shield_resilience_planning` and the statement that shared generators are common infrastructure, not independent replication. |

Round-3 near-miss retained: the complete framework is competitive only within the implemented proxy/control set and under metric-dependent rankings; the evidence does not support normalization-invariant optimizer superiority, electrical superiority, deployment, or monetary claims.

## Final claim alignment

- Title and abstract identify the SimBench-derived mixed-voltage portfolio proxy.
- Method text matches the joint adaptation switch, slot-persistent controls, repair score, retained NoDER genome width, seed derivation, and returned-population repair used in code.
- Statistical claims distinguish seed-block inference from fixed-configuration description and deterministic Weighted Sum provenance rows.
- Pareto controls are described as implemented configurations under a common generation horizon, with the missing exact evaluation-budget equivalence disclosed.
- AC results remain a composition-screening diagnostic with dependent fixed-case rows.
- Discussion and conclusion retain normalization sensitivity, FixedDE's nominal advantage, missing direct-control AC rows, and all unresolved extensions.

## Residual human blockers

- CRediT roles require author approval.
- Funding, grant, and APC-funder statements require verified author input.
- The final public supplementary archive/DOI requires human confirmation.

These blockers are unchanged and are not resolved by scientific text editing.
