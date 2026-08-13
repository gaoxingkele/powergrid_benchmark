# Title-to-Evidence Map

- **Aligned title:** *BiLo-NSGA: Budget-Aware Project-Level Local Moves with Accepted-Move Logging for Power-Grid Portfolio Optimization*.
- **Budget-aware project-level local moves** maps to the disclosed hard budget, forward insertion under residual slack, atomic delete--insert substitution, and deterministic feasibility recovery in `manuscript/MANUSCRIPT.md`, Sections 3.1 and 4. The title does not claim that both local directions improve performance.
- **Accepted-move logging** is bounded to a run-level event log. The log contains committed `forward_insert` and `backward_substitute` events plus deterministic `repair_drop` events. The retained aggregate `manuscript/derived_tables/p6_search_audit_efficiency.csv` reports `mean_moves`, `mean_trace_events`, and `mean_coverage`; for BiLo-NSGA these are 3667.954, 3667.954, and 0.9964326 over 240 runs. The file name is historical and is not evidence of audit completeness.
- The event log spans explored offspring. The available derived table does not establish a parent--child lineage from initialization to a final portfolio, a causal explanation for a selected portfolio, or a recommendation path.
- The retained method name **BiLo-NSGA** is a proper label. The title and contribution list do not expand it into a bidirectional-gain claim.

# Primary Estimand and Analysis Unit

- The primary outcome is standard four-objective hypervolume of the feasible non-dominated front, with fixed per-experiment normalization bounds and reference point `(1.1, 1.1, 1.1, 1.1)` as specified in Section 5.3.
- The primary analysis unit is one seeded method-by-scenario invocation. Stochastic comparisons use 30 seeds per method and scenario and two-sided Mann--Whitney tests with Holm correction within the declared stochastic-opponent family. Pooled means across eight scenarios are descriptive because scenarios change pools, budgets, weights, and random streams.
- Deterministic AHP-TOPSIS, Greedy BCR, and WeightedRankingOnly outputs have effective sample size one per scenario; their repeated provenance rows do not create inferential replication.
- Logged-event count and final-front project coverage are secondary run-level diagnostics. They are not optimization objectives, do not enter selection, and do not measure explanation or audit quality.
- NERC rule alignment and MISO MTEP16 outcomes are separate project-level descriptive diagnostics. They do not share the primary seeded-portfolio analysis unit and are not confirmatory evidence of practical review validity.

# Comparison Budget and Data Visibility

- Evolutionary methods use population 40 for 40 generations. The Pareto Local Search control has a numerical ceiling of 1600 evaluated neighbors, which matches the nominal offspring-evaluation ceiling but not computational work; runtime is reported separately.
- The full manuscript reports 18 methods by 8 scenarios by 30 invocations (4320 rows), but this isolated worktree retains only the two derived CSV summaries under `manuscript/derived_tables/`. This narrative stage does not independently reconstruct the raw 4320-row archive or the event-level log.
- The budget-indexed result is not a controlled budget-only experiment. Full-pool scenarios at 0.75x, 0.88x, 1.00x, and 1.20x also vary scalar weights and use independent random streams.
- The 1.20x point is a large-pool-labeled setting, and `Ablation-LooseBudget` changes the search budget while evaluation uses the true budget. Neither supports a causal estimate of budget slack alone.
- MTEP16 uses 10 seeded compromise-portfolio runs and project-level outcome diagnostics, unlike the 30-seed primary hypervolume protocol. Its raw p-values are descriptive because portfolio dependence and a multiplicity family are not modeled.

# Negative and Null Results

- Removing forward insertion yields a higher pooled mean hypervolume (0.17257 versus 0.17190), even though the full method wins significantly in three of eight scenarios. This is scenario-dependent evidence, not forward dominance.
- Removing atomic substitution yields a higher pooled mean (0.17294, +0.61% relative to the full method), and no scenario-level contrast is significant under the declared family. Replacing atomic substitution with standalone legacy deletion also yields a higher pooled mean (0.17228, +0.22%) with unresolved scenario-level contrasts. Atomic substitution is not supported as an accuracy mechanism.
- Against NSGA-II, the 0.75x scenario has a nominal -0.64% difference with Holm-adjusted `p = 1.000`; the renewable-filtered scenario has a nominal -1.31% difference with Holm-adjusted `p = 1.000`; the 0.88x gain is also unresolved after multiplicity correction.
- In the MTEP16 budget-constrained backtest, AHP-TOPSIS has the highest broad capture (1.0995 versus 1.0715 for BiLo-NSGA). BiLo-NSGA strict capture is 1.0093 and strict ordering is unresolved.
- NERC Kendall associations are non-significant, the NERC source overlaps benchmark construction at the project-kind level, and the MTEP16 approved-plan pool has a severe built-project base rate. These checks support descriptive consistency only.
- Pareto Local Search is lower in all eight scenarios under the disclosed 1600-neighbor implementation, but this does not support superiority over Pareto local search, memetic search, or exact knapsack methods as families.
- No evidence in this worktree establishes dependency synergy, audit completeness, explanation sufficiency, recommendation-path fidelity, deployment benefit, expert agreement, calibrated economics, or electrical feasibility.

# Shared Assets and Independent Contribution

- The companion project is **`mintou_p5_trace_moea_feasibility_review`** (TRACE-MOEA).
- Shared assets are the versioned candidate-generation pipeline, the RTS-GMLC and SimBench inputs used by that pipeline, the public NERC source corpus, and the public MISO MTEP16 source records. The 120-candidate benchmark is therefore a shared asset, not an independently created P6 contribution.
- P6 isolates the local-search question: budget-aware forward insertion, atomic substitution, dependency-aware move scoring, deterministic feasibility recovery, and the associated run-level event log inside a non-dominated-sorting framework.
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
- Confirm a persistent repository URL/DOI and third-party redistribution terms. The current manuscript states that the full run archive and event-level data are in a supplementary review package, but those raw files are not present in this isolated worktree.
- Confirm with both paper teams that the P5/P6 descriptions of shared assets and paper-specific run archives are accurate and that simultaneous-submission and text-overlap policies are satisfied.
- Human evaluation is required before the event log can be described as useful, sufficient, or complete for review. Until then it remains an aggregate run-level record, not an audit trail or recommendation lineage.
