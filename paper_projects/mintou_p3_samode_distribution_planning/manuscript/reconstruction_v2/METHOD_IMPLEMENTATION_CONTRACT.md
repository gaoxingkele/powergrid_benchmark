# P3 Action-Aligned Method Implementation Contract

**Stage:** `p3_v2_s03_action_method_implementation_contract`  
**Status:** `IMPLEMENTATION_SPLIT_COMPLETE / ACTION_REGISTRY_NO-GO / NO_NEW_RESULTS`  
**Scope:** prospective method and engineering specification only. The immutable P3 S3 archive and all reported numerical results remain unchanged.

## 1. Evidence boundary and gate decision

The historical optimizer exposes one `strategy_adaptive` switch. In the archived source, that switch simultaneously (i) resamples (F/CR), (ii) selects between `rand/1` and `best/1`, and (iii) updates strategy-success masses. Moreover, (F/CR) remain attached to population slots after environmental selection rather than following the selected genomes. Therefore, the archived `Ablation-FixedDE` contrast is a coupled contrast and cannot identify parameter or strategy effects separately.

The prospective implementation in `scripts/p3_s03_method_contract.py` separates `parameter_adaptive` and `strategy_adaptive`, attaches (F/CR) to individuals, applies survivor indices to those controls, and derives independent parameter and strategy random streams from a labelled hash of the master seed. `AdaptationConfig.from_legacy(bool)` preserves the historical public-switch semantics: `true` opens both gates and `false` closes both. This compatibility mode preserves configuration meaning, not numerical equivalence to the archived implementation, because correcting control inheritance and separating random streams intentionally changes the random process. No rerun has been performed, and no effect is attributed to either gate.

The action-aligned gate is **NO-GO at this stage**. Legacy decision IDs contain only `subnet::kind`; they do not name a unique target bus, line, transformer, or switch in any validation network. The archived composition mapper chooses targets from case-specific stress rankings, which is not a one-to-one decision-variable mapping. Inventing element IDs or monetary costs would violate the evidence contract. Formal optimization and AC post-validation are prohibited until a complete action registry passes `validate_complete_registry`.

## 2. Four-arm mechanism contract

| Arm ID | Parameter gate | Strategy gate | Interpretation |
|---|---:|---:|---|
| `fixed_parameter__fixed_strategy` | off | off | fixed (F=0.5, CR=0.9); `rand/1` only |
| `adaptive_parameter__fixed_strategy` | on | off | heritable jDE-style (F/CR); `rand/1` only |
| `fixed_parameter__adaptive_strategy` | off | on | fixed (F/CR); success-driven `rand/1`/`best/1` pool |
| `adaptive_parameter__adaptive_strategy` | on | on | both mechanisms enabled |

All four arms must share initialization, decoding, repair, environmental selection, population size, stopping rule, objective functions, and paired master seeds. Each gate owns a separate labelled random stream. Toggling the strategy gate must not consume parameter draws, and toggling the parameter gate must not consume strategy draws. The unit tests cover the four arms, legacy mapping, stream separation, fixed-seed replay, and heritable control selection.

The confirmatory estimands are the two gate main effects and their interaction. A coupled on--on versus off--off contrast may be reported only as a joint contrast and must not be used to attribute an effect to either gate.

## 3. Decision variable, action, cost, and effect registry

Every optimizer coordinate must have exactly one registry row with the following non-empty fields before a run:

| Field | Requirement |
|---|---|
| `variable_id` | Stable optimizer-coordinate ID; unique and identical to the registry key. |
| `kind` | One of `reinforcement`, `storage`, `der`, or `automation`. |
| `source_subnet` | Provenance link to the legacy candidate source only; not a target locator. |
| `target_network` | Exact public-network identifier and version. |
| `target_element_type`, `target_element_id` | Exact persistent element binding: line for reinforcement, bus for storage/DER, switch for automation. |
| `cost_units` | Finite non-negative benchmark cost with source/formula provenance. It must not be described as currency unless externally calibrated. |
| `capacity_increment`, `capacity_unit` | Fixed action size and physical unit. |
| `provenance` | Source record, transformation, and version sufficient to reproduce the binding. |

The implementation maps a validated row as follows:

| Decision kind | Auditable network action | Cost | Electrical and proxy effect |
|---|---|---|---|
| Reinforcement | Increase the registered line's parallel-circuit count by the registered increment. | Registered benchmark cost units. | Changes branch impedance/current capacity in AC post-validation; proxy terms may include loss, voltage-risk, hosting, reliability, and resilience effects. |
| Storage | Add the registered storage increment at the registered bus under a frozen dispatch rule. | Registered benchmark cost units. | Adds a signed controllable injection at that bus; proxy terms may include all five planning objectives plus DER support. |
| DER | Add the registered static-generation increment at the registered bus. | Registered benchmark cost units. | Adds active/reactive injection under the frozen power-factor rule; proxy terms may include loss, hosting, reliability, resilience, and DER support. |
| Automation | Apply the registered switch/control action. | Registered benchmark cost units. | No steady-state injection or impedance effect is credited; any reliability effect requires a separately specified contingency/restoration model. |

No case-dependent stress ranking may replace the registered target. A missing, extra, duplicated, type-inconsistent, or key-mismatched row is a hard failure. The current legacy variable set cannot pass this gate because exact targets and capacity increments are absent.

## 4. Phenotype and repair contract

The phenotype is (x_j=I[g_j\ge 0.5]) for every four-arm and baseline implementation that uses a continuous genome. The equality case is selected. The prospective runner must use this one rule throughout; this does not retroactively change the archived strict-(>0.5) CARS-MODE results.

Budget feasibility is calculated from the registered per-variable costs. If selected cost exceeds the budget, deterministic repair repeatedly removes the selected variable with the smallest preregistered benefit-to-cost score. Exact ties are broken by ascending stable `variable_id`. Repair returns only the phenotype; the continuous genome is not silently rewritten. Repair removals, pre/post cost, and selected IDs must be logged for every evaluation. Zero-cost variables are never removed on a finite ratio unless a separate frozen rule says otherwise.

## 5. Load, DER, contingency, and AC limits

To retain continuity with the archived diagnostic without claiming stochastic scenario coverage, the prospective pilot freezes the following six deterministic operating cases:

| Case | Load multiplier | Existing DER multiplier | Contingency |
|---|---:|---:|---|
| base | 1.0 | 1.0 | none |
| peak load | 1.3 | 1.0 | none |
| load growth | 1.5 | 1.0 | none |
| extreme growth | 1.8 | 1.0 | none |
| high DER | 0.5 | 2.5 | none |
| growth + N-1 | 1.5 | 1.0 | one preregistered in-service branch outage |

These are fixed stress cases, not random scenarios and not optimizer replications. Loads scale both active and reactive demand. Existing DER scales active generation; reactive behavior/power factor, storage dispatch, and the N-1 branch ID must be frozen in the action registry/run configuration before the pilot. The archived rule that chooses an outage after a pre-plan stress ranking is not admissible for action-aligned confirmation.

An AC case is feasible only when all conditions pass: solver convergence; every in-service bus voltage within inclusive ([0.95,1.05]) pu; and every in-service line loading at or below 100%. Non-convergence, missing/non-finite outputs, islanding not covered by the solver, or a requested action that cannot be applied is an explicit failure, never a dropped row. Transformer-loading limits are **not evidenced in the current materials**; before a formal run, the selected public network requires a preregistered transformer criterion or an explicit, justified not-applicable statement.

## 6. Evaluation accounting and comparison budget

The runner must separately count and export:

1. generated candidate phenotypes;
2. raw proxy-objective rows evaluated, including repeated parent evaluations;
3. unique phenotype evaluations if caching is used;
4. repair calls and removals;
5. AC power-flow attempts, convergence failures, and action-application failures; and
6. wall time as environment-specific provenance.

Formal comparisons require equal maximum raw objective-row budgets across the four arms and declared baselines, with termination on that counter rather than generation count alone. Paired master seeds and the same data visibility apply to every arm. Tuning and evaluation seed sets must be disjoint and frozen before results are read. The preregistered quality-per-evaluation endpoint is the objective-row count at first attainment of a fixed analytic-HV threshold; failures to attain it are retained as censored/non-attainment outcomes under the frozen analysis rule. Wall time cannot substitute for the objective-row budget.

## 7. AC post-validation and reporting

For each frozen optimizer seed, the selection rule for top-(k) plans, (k), tie handling, and preference/reference data must be frozen before optimization. Every selected phenotype is converted through the complete registry, applied to a fresh copy of the same network, and evaluated over all six fixed cases. The output key is `(arm, optimizer_seed, plan_rank, network, scenario_id)`; it must retain the selected variable IDs, applied actions, benchmark cost, convergence flag, minimum/maximum voltage, maximum line loading, losses, failure code, and feasibility flag.

The optimizer seed is the replication unit for method comparisons. Network--scenario rows nested under a selected plan are repeated measurements, not independent replicates. Any aggregation must preserve seed-level pairing. Pilot data are pipeline evidence only and cannot enter confirmatory estimates. Combined on--on/off--off results remain joint results; separate gate effects require the complete 2x2 design.

## 8. Required artifacts before the next stage

- `scripts/p3_s03_method_contract.py` and passing `scripts/test_p3_s03_method_contract.py`;
- `experiments/p3_s4_energies_samode_ac_planning_v1/method_implementation_contract.json`;
- a complete, provenance-bearing action registry for every optimizer variable;
- a pinned public-network/data manifest and environment record;
- a frozen pilot configuration containing dispatch, power factor, transformer policy, N-1 element, seeds, top-(k), budgets, and output schema; and
- a gate record that is `GO` only after registry validation and deterministic replay pass.

Until those inputs exist, the protocol remains `SCAFFOLD_ONLY / NO_RESULTS`, the AC action gate remains `NO-GO`, and the manuscript's composition-level and coupled-adaptation limitations remain controlling.

