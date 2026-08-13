# Title-to-Evidence Map

- **Aligned title:** *BiLo-NSGA: Budget-Aware Project-Level Local Moves with Accepted-Move Logging for Power-Grid Portfolio Optimization*.
- **Budget-aware project-level local moves** maps to affordable forward insertion, atomic delete--insert substitution, deterministic feasibility recovery, and constraint non-dominated environmental selection. The new evidence of record is `experiments/p6_s3_matched_effort/runs/primary_v1/`.
- **Accepted-move logging** remains bounded to in-memory `forward_insert`, `backward_substitute`, and `repair_drop` production in the legacy implementation. Released legacy rows contain counts and final-front/event pool-position co-occurrence, not ordered payloads, states, lineage, replay, or a recommendation path.
- The title does not claim superiority. Under the primary matched-evaluation protocol, BiLo-NSGA is below the disclosed stage-local NSGA-II in all eight scenario means and has four Holm-significant losses. It is above the bounded Pareto Local Search in all eight scenarios.
- The method name **BiLo-NSGA** is a proper label. Neither the title nor the contribution list expands it into a bidirectional-gain, dependency-synergy, audit, or deployment claim.

# Primary Estimand and Analysis Unit

- The primary estimand is the within-scenario difference in standard four-objective hypervolume of the final feasible non-dominated front between BiLo-NSGA and a named comparator after exactly 3200 combined search-evaluation units.
- One unit is one initialization/offspring candidate scored on the four objectives or one evaluated local proposal. Local proposals are not double-counted as population evaluations. Final-front extraction and hypervolume are post-search readouts.
- The primary analysis unit is one seeded method--scenario invocation. There are 30 common seed indices per method and scenario. All eight registered P6 scenario pools, budgets, and objective definitions are shared across the three methods.
- The primary multiplicity family is the 16 BiLo-NSGA contrasts formed by two comparators across eight scenarios. It uses exact two-sided paired sign tests with one Holm correction. The 16 equal-time contrasts form a separately declared secondary family. Sensitivity outputs are descriptive and emit no p-values.
- Under the registered empirical 5%-padded bounds, clipping to `[0,1]`, and reference point `(1.1,1.1,1.1,1.1)`, pooled primary means are 0.1627661 for BiLo-NSGA, 0.1721313 for NSGA-II, and 0.1162594 for Pareto Local Search.
- The equal-time estimand uses a common 0.20-s search deadline. Pooled means are 0.1709792, 0.1722114, and 0.1159257, respectively. Wall-clock values are machine-specific.
- The legacy 4320-row fixed-generation archive remains evidence for its broad baseline and ablation questions, but its 1.12% pooled BiLo-NSGA/NSGA-II difference is not an effort-controlled estimand and is no longer the headline comparison.

# Comparison Budget and Data Visibility

- Every one of the 720 primary rows consumes exactly 3200 units. BiLo-NSGA averages 918.9 population-objective and 2281.1 local-proposal evaluations; NSGA-II uses 3200 and 0; PLS uses 40 and 3160. Equal total does not mean identical allocation because the algorithms expose different search structures.
- Every one of the 720 secondary rows uses the same 0.20-s target. Realized search time ranges from 0.200004 to 0.201374 s because ranking can finish after the last deadline check. The per-run table retains target, realized search time, total invocation time, evaluation counts, feasibility, front size, and a front-objective hash.
- Method order rotates by seed index. All methods receive the same scenario candidate pool, budget, objectives, registered normalization bounds, and common seed value. No seed was dropped or replaced.
- BiLo-NSGA preserves the disclosed shared-engine semantics but adds explicit evaluation metering. PLS is the disclosed 40-start feasible add/delete/swap archive with metering. Repair and ranking use visible attributes without an objective-evaluation charge.
- The recorded `pymoo==0.6.2` optimizer cannot run on this host, and installed `pymoo==0.4.1` lacks its import paths. The matched study therefore labels and fully specifies a stage-local constrained NSGA-II: constraint-rank/crowding tournament, 0.9-probability two-point crossover, `1/n` bit mutation, no repair, and constraint non-dominated selection. Pymoo 0.4.1 supplies only the pure-Python hypervolume indicator. Equivalence to the legacy pymoo baseline is not claimed.
- All 1440 comparison rows have nonempty feasible fronts and final-population feasibility rate 1.0. This is budget feasibility only; no AC load-flow, OPF, construction, expert, or economic feasibility is inferred.
- The hypervolume study contains 4320 per-run rows: six schemes for every primary front. The reported bounds have 1121 of 28,061 points (3.99%) outside `[0,1]` before clipping; 25%-expanded bounds have 197 (0.70%); analytic bounds have none beyond `1e-12`. Pooled ordering is stable, but numerical scales and gaps change.
- The local scan has 560 rows: seven one-factor BiLo-NSGA cells, all eight scenarios, and ten common seeds. Its cells are depth 2/8/16, penalty 5/10/20, and group-order bonus 1.00/1.06/1.12. No observed sensitivity result was used to alter the primary run.

# Negative and Null Results

- Under exact total units, BiLo-NSGA is 5.44% below NSGA-II in the pooled descriptive mean. All eight scenario mean differences are negative. Budget-constrained selection, renewable accommodation, ranking robustness, and the 0.75x budget are Holm-significant losses; the other four are unresolved. There is no significant win over NSGA-II in the primary family.
- Under equal time, the NSGA-II result is heterogeneous: three significant BiLo-NSGA wins, two significant losses, and three unresolved contrasts. The pooled mean is 0.72% lower for BiLo-NSGA. This does not support a universal equal-time advantage for either method.
- BiLo-NSGA is higher than the bounded PLS in all eight scenarios under both protocols, but this is not evidence against Pareto local search, memetic search, large-neighborhood search, or exact knapsack methods as families.
- The registered local depth is not supported as optimal. Depth 2 is descriptively 4.29% above depth 8, and depth 16 is 0.22% above it. The immutable primary configuration was not retuned.
- Penalties 5, 10, and 20 produce identical sensitivity rows because every evaluated local proposal is feasible and the violation term is zero. The penalty sensitivity is a null result for this protocol.
- Changing the group-order multiplier from 1.06 to 1.00 changes the pooled mean by -0.15%; changing it to 1.12 changes it by +0.10%. These descriptive values provide no measured accuracy benefit for 1.06 and no evidence of dependency synergy.
- The reported clipping operation affects 3.99% of primary front points. Removing clipping or changing bounds/reference points materially changes the hypervolume scale and NSGA-II gap, although the pooled three-method ordering is stable across the six schemes.
- Earlier ablations remain asymmetric: NoForwardSearch has the higher pooled legacy mean despite three full-method wins; NoBackwardSearch and LegacyDeletion are unresolved and have higher pooled means. Atomic substitution is not supported as an accuracy mechanism.
- NERC and MTEP16 evidence remains descriptive. No evidence establishes expert agreement, calibrated economics, electrical feasibility, audit completeness, lineage, replay, explanation sufficiency, recommendation fidelity, or deployment benefit.

# Shared Assets and Independent Contribution

- The companion project is **`mintou_p5_trace_moea_feasibility_review`** (TRACE-MOEA).
- Shared assets are the candidate-generation pipeline, RTS-GMLC and SimBench inputs, NERC source corpus, MTEP16 source records, problem utilities, and public-record backtest infrastructure. They are not claimed as independent P6 contributions.
- P6's independent question is project-vocabulary local search: affordable insertion, atomic substitution, group-label proposal ordering, deterministic recovery, accepted-move/repair counters, and the new matched-effort comparisons.
- This stage changes no shared source and no P5 evidence. The shared source SHA256 remains `1780647cc226e1c54a076863154945a9df53686f21ebadf9548c827a9081a4ba`. P5 run, leaderboard, and config SHA256 values are identical before and after execution, as recorded in `primary_v1/validation.json`.
- Shared inputs do not make either paper's method results evidence for the other. P5 and P6 retain separate objectives, configurations, executions, outputs, and claims.

# New or Rerun Experiments

- The frozen design is `experiments/p6_s3_matched_effort/config.json`; the completed immutable evidence-of-record run is `experiments/p6_s3_matched_effort/runs/primary_v1/`.
- New comparisons comprise 1440 rows: three methods by eight scenarios by 30 seeds under two protocols. The primary half uses exactly 3200 combined units; the secondary half uses the common 0.20-s deadline.
- New hypervolume sensitivity comprises 4320 per-run scheme rows. New local sensitivity comprises 560 rows. Raw rows, summaries, inference, configuration, environment, input hashes, execution record, and validation are all retained.
- No run failed, no seed was omitted or replaced, and no result-dependent parameter amendment was made. The unfavorable equal-evaluation NSGA-II results, depth-2 advantage, penalty null, and small bonus effects are all retained.
- The legacy 4320-row archive, NERC check, and MTEP16 backtest were not rerun or relabeled as new matched evidence. Their historical scopes are preserved.
- The host limitation on pymoo 0.6.2 is explicit. No different pymoo optimizer version was substituted; the stage-local NSGA-II implementation is a new, bounded comparison target.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** confirm the author list, affiliations, correspondence details, and CRediT roles with every author. This stage does not infer roles from author order.
- **AUTHOR INPUT REQUIRED:** provide the verified funder and grant number or confirm the no-external-funding statement; also confirm any APC funder.
- **AUTHOR INPUT REQUIRED:** approve a persistent repository URL/DOI and the redistribution terms for the public inputs and stage-local evidence package.
- Confirm with both paper teams that the P5/P6 shared-asset disclosure, textual independence, simultaneous-submission policy, and companion bibliographic status are accurate.
- Human evaluation is required before event summaries can be described as useful or sufficient for review. Stable identifiers, ordered payloads, parent/child states, and replay tests are required before lineage or replay claims.
- Expert labels, calibrated costs, an independent benchmark family, broader local-search controls, and load-flow/OPF checks remain blockers for stronger practical or deployment claims.
