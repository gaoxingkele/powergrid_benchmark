# Title-to-Evidence Map

- **Aligned title:** *BiLo-NSGA: Budget-Aware Project-Level Local Moves with Accepted-Move Logging for Power-Grid Portfolio Optimization*.
- **Budget-aware project-level local moves** maps to the normalized hard-budget violation, forward insertion under residual slack, atomic delete--insert substitution, and deterministic feasibility recovery in `manuscript/MANUSCRIPT.md`, Sections 3.1 and 4. The title does not claim that both local directions improve performance.
- **Accepted-move logging** maps to an in-memory list containing accepted `forward_insert` and `backward_substitute` events plus deterministic `repair_drop` events. Rejected proposals are not counted. The run writer reduces the list to `local_move_count`, `trace_event_count`, and final-front/event pool-position co-occurrence; it does not serialize event payloads.
- The retained aggregate `manuscript/derived_tables/p6_search_audit_efficiency.csv` reports `mean_moves`, `mean_trace_events`, and `mean_coverage`; for BiLo-NSGA these are 3667.954, 3667.954, and 0.9964326 over 240 runs. Equality of the first two fields follows from one increment and one event per accepted local move or repair drop. The historical file and field names are not evidence of trace completeness.
- The transient event list includes initialization repairs and events on explored offspring that may be discarded. It stores generation labels and pool-local integer positions but not parent/child identity, portfolio states, objective deltas, or final-portfolio links. The retained data therefore establish neither chronology nor lineage, causal explanation, replay, an audit trail, or a recommendation path.
- The retained method name **BiLo-NSGA** is a proper label. The title and contribution list do not expand it into a bidirectional-gain claim.

# Primary Estimand and Analysis Unit

- The primary outcome is standard four-objective hypervolume of the feasible non-dominated front, with fixed per-experiment normalization bounds and reference point `(1.1, 1.1, 1.1, 1.1)` as specified in Section 5.3.
- The primary analysis unit is one seeded method-by-scenario invocation. Stochastic comparisons use 30 seeds per method and scenario and two-sided Mann--Whitney tests with Holm correction within the declared stochastic-opponent family. Pooled means across eight scenarios are descriptive because scenarios change pools, budgets, weights, and random streams.
- Deterministic AHP-TOPSIS, Greedy BCR, and WeightedRankingOnly outputs have effective sample size one per scenario; their repeated provenance rows do not create inferential replication.
- The local acceptance scalar is not an estimand or evaluation metric. It is an equal-weight sum of four objectives normalized from the current generation's parent plus pre-repair offspring rows, plus `10` times the normalized budget violation. These bounds are frozen for that generation and are distinct from the fixed hypervolume bounds.
- Event count and final-front/event pool-position co-occurrence are secondary run-level diagnostics. They are not optimization objectives, do not enter selection, and do not measure attempted moves, explanation, lineage, replay, or audit quality.
- NERC rule alignment and MISO MTEP16 outcomes are separate project-level descriptive diagnostics. They do not share the primary seeded-portfolio analysis unit and are not confirmatory evidence of practical review validity.

# Comparison Budget and Data Visibility

- The committed implementation and generated configuration were inspected from the repository history at `src/powergrid_benchmark/mintou_real_project_review.py`, `papers/mintou/mintou_p6_bilonsga_project_review/src/code/run_real_project_review.py`, and `.../src/configs/real_project_review_config.json`. These source/config files are not checked out in this isolated narrative worktree, so no code or configuration was modified in this stage.
- BiLo-NSGA initializes each of 40 rows by drawing a row-specific selection density uniformly from 0.03 to 0.15, drawing Bernoulli bits at that density, and repairing to budget. Each generation produces 40 children from uniformly sampled parent indices with replacement, a per-bit 0.5 crossover mask, and bit-flip probability `1/n`. After repair, the first 20 array positions receive local search; this is a fixed positional rule rather than fitness-based or random offspring selection.
- The move score is the raw mixed-scale sum `reliability + renewable + load_support + 0.5*(compliance + evidence)`, divided by `max(cost, 1)`. There is no `b_jq` normalization and no scenario weighting in local search or repair. The 1.06 group-label multiplier affects only insertion/replacement proposal order; no dependency benefit or constraint is operationalized.
- Exact local/repair score ties resolve to the smallest eligible pool-local index because ascending eligible arrays feed NumPy `argmin`/`argmax`. Crowding and scalar-ranking baselines use `argsort` without an explicit stable secondary key; exact cross-version tie replay is therefore not certified.
- BiLo-NSGA, its evolutionary ablations, NSGA-II, and NSGA-III use population 40 for 40 generation labels. MOEA/D uses 35 four-objective Das--Dennis directions as its effective population. The Pareto Local Search control has a ceiling of 1600 evaluated neighbors. The run archive does not retain `n_eval`, so identical computational or objective-call budgets are not claimed; runtime is reported separately.
- Constraint handling differs by method: the full custom method combines repair with normalized-violation constraint dominance; NSGA-II/III receive normalized violation as one pymoo inequality; MOEA/D adds `1e4 * violation` to every objective; point rules use affordable greedy fill; and Pareto Local Search uses repaired starts, feasible moves, and feasible-archive filtering. All final hypervolume calculations discard infeasible rows.
- The full manuscript reports 18 methods by 8 scenarios by 30 invocations (4320 rows), but this isolated worktree retains only the two derived CSV summaries under `manuscript/derived_tables/`. This narrative stage does not independently reconstruct the raw 4320-row archive or the event-level log.
- The default unnormalized scenario-weight vector is `(0.26, 0.18, 0.20, 0.14, 0.12, 0.26, 0.38)` for reliability, renewable, load, compliance, evidence, risk, and cost. Budget-labeled scenarios set cost to 0.50; the dependency-labeled scenario sets reliability/risk to 0.40/0.36; the local-move scenario sets cost/risk to 0.44/0.32; and the renewable scenario sets renewable to 0.42. The other scenarios use the default. These weights affect only Greedy BCR, AHP-TOPSIS, and WeightedRankingOnly.
- The budget-indexed result is not a controlled budget-only experiment. Full-pool scenarios at 0.75x, 0.88x, 1.00x, and 1.20x vary weights for some scalarizing baselines and use independent random streams.
- The 1.20x point is a large-pool-labeled setting, and `Ablation-LooseBudget` changes the search budget while evaluation uses the true budget. Neither supports a causal estimate of budget slack alone.
- MTEP16 uses 10 seeded compromise-portfolio runs and project-level outcome diagnostics, unlike the 30-seed primary hypervolume protocol. Its raw p-values are descriptive because portfolio dependence and a multiplicity family are not modeled.
- The generated JSON is not a complete replay manifest: it omits local depth, local penalty, generation-local normalization, group bonus, fixed first-20 offspring selection, ties, effective MOEA/D population, library/dependency versions, and pymoo operator defaults.

# Negative and Null Results

- Removing forward insertion yields a higher pooled mean hypervolume (0.17257 versus 0.17190), even though the full method wins significantly in three of eight scenarios. This is scenario-dependent evidence, not forward dominance.
- Removing atomic substitution yields a higher pooled mean (0.17294, +0.61% relative to the full method), and no scenario-level contrast is significant under the declared family. Replacing atomic substitution with standalone legacy deletion also yields a higher pooled mean (0.17228, +0.22%) with unresolved scenario-level contrasts. Atomic substitution is not supported as an accuracy mechanism.
- Against NSGA-II, the 0.75x scenario has a nominal -0.64% difference with Holm-adjusted `p = 1.000`; the renewable-filtered scenario has a nominal -1.31% difference with Holm-adjusted `p = 1.000`; the 0.88x gain is also unresolved after multiplicity correction.
- In the MTEP16 budget-constrained backtest, AHP-TOPSIS has the highest broad capture (1.0995 versus 1.0715 for BiLo-NSGA). BiLo-NSGA strict capture is 1.0093 and strict ordering is unresolved.
- NERC Kendall associations are non-significant, the NERC source overlaps benchmark construction at the project-kind level, and the MTEP16 approved-plan pool has a severe built-project base rate. These checks support descriptive consistency only.
- Pareto Local Search is lower in all eight scenarios under the disclosed 1600-neighbor implementation, but this does not support superiority over Pareto local search, memetic search, or exact knapsack methods as families.
- No evidence in this worktree establishes dependency synergy, audit completeness, explanation sufficiency, recommendation-path fidelity, deployment benefit, expert agreement, calibrated economics, or electrical feasibility.
- The LowDependencyDensity stress variant changes labels rather than disabling an operational dependency constraint; its unresolved result cannot establish a dependency benefit.

# Shared Assets and Independent Contribution

- The companion project is **`mintou_p5_trace_moea_feasibility_review`** (TRACE-MOEA).
- Shared assets are the versioned candidate-generation pipeline, the RTS-GMLC and SimBench inputs used by that pipeline, the public NERC source corpus, and the public MISO MTEP16 source records. The 120-candidate benchmark is therefore a shared asset, not an independently created P6 contribution.
- P6 isolates the local-search question: budget-aware forward insertion, atomic substitution, a heuristic group-label proposal bonus, deterministic feasibility recovery, and accepted-move/repair counters inside a non-dominated-sorting framework.
- The manuscript reports the hard-budget formulation, BiLo-NSGA implementation, scenario definitions, run records, selected portfolios, and comparisons as P6-specific. This stage did not inspect the companion worktree, so textual and archive independence still requires author/repository confirmation before submission.
- Shared public records do not make the NERC or MTEP16 checks independent replications. Each retains the scope qualifiers stated in the manuscript.

# New or Rerun Experiments

- No experiment was added, rerun, filtered, or retuned in this narrative stage.
- No evidence CSV, numerical result, p-value, effect size, or figure was changed. The title and contributions were narrowed to the evidence already retained in the worktree.
- The existing NERC rule check and MTEP16 historical-outcome backtest remain descriptive analyses with their original protocols and limitations; this stage does not relabel them as new validation.
- Any future weight sensitivity, dependency-bonus sensitivity, second benchmark family, expert-label study, cost calibration, later-MTEP cohort, or load-flow check must be reported as new evidence only after the corresponding run records are available.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** confirm the author list, affiliations, correspondence details, and CRediT roles with every author. This stage does not infer contributions from author order.
- **AUTHOR INPUT REQUIRED:** provide the verified funder and grant number or confirm the no-external-funding statement; also confirm any APC funder.
- Confirm a persistent repository URL/DOI and third-party redistribution terms. The raw 4320-row archive is not present in this isolated worktree, and the inspected run writer does not serialize event payloads; submission materials must not describe those payloads as released unless the archive is extended and verified.
- Confirm with both paper teams that the P5/P6 descriptions of shared assets and paper-specific run archives are accurate and that simultaneous-submission and text-overlap policies are satisfied.
- Human evaluation is required before the accepted-move summaries can be described as useful, sufficient, or complete for review. Stable identifiers, ordered serialized payloads, parent/child and before/after states, and replay tests are required before lineage or replay claims.
