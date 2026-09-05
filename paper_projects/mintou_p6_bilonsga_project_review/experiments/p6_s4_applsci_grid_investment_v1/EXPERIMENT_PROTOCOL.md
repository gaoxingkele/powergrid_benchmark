# P2 Frozen Orthogonal and Matched-Compute Experiment Protocol

**Stage:** `p2_v2_s04_frozen_experiment_protocol`

**Status:** `FROZEN PROTOCOL / INPUT GATE NO-GO / NO_RESULTS`

**Locked title:** *Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization*

**Protected predecessor:** `../p6_s3_matched_effort/` is read-only.

This is a prospective protocol, not an experiment report. Its design is frozen in `config.json`. Formal execution remains prohibited because neither action registry, source digest, objective implementation, cost-model provenance record, family budget, nor numeric normalization bounds are present. Those omissions are listed without fabricated substitutes in `data_manifest.json` and `planned_vs_executed.json`.

## 1. Tasks, arms, and comparators

The two independently generated task families are `rts_transmission_reinforcement` (identified RTS-GMLC branch-rating increases) and `simbench_feeder_reinforcement` (identified SimBench line-rating increases). They have separate source snapshots, action namespaces, task generators, costs, budgets, objective bounds, seeds, caches, rows, metric reference sets, and inference families. No pooled task-family estimate or claim is permitted.

The principal 2-by-2 component design fixes non-dominated sorting as the common outer algorithm and crosses forward insertion off/on with standalone backward deletion off/on:

| Arm | Forward | Backward | Allowed conclusion |
|---|---:|---:|---|
| `nds_only` | off | off | common-kernel reference |
| `forward_only` | on | off | forward simple effect at backward=off |
| `backward_only` | off | on | backward simple effect at forward=off |
| `bidirectional` | on | on | joint arm; not by itself evidence of either component or interaction |

The interaction is the paired difference-in-differences `(bidirectional - backward_only) - (forward_only - nds_only)`, with the sign reversed where lower is better. Forward then backward is the frozen order in `bidirectional`; each pass stops at its first non-improvement. The forward and backward depth caps are 2 and 2. Equality and non-finite objective values reject. `backward_only` is deletion, not delete--insert substitution. Atomic substitution is outside this formal matrix and cannot be substituted silently.

Two baselines are frozen: the fully specified stage-local constrained `nsga2` and the disclosed stage-local `pareto_local_search`. They provide, respectively, a canonical evolutionary comparator and a neighborhood-search comparator already implemented and bounded in this project. No additional “strong” comparator is admitted: the worktree contains no audited, task-aligned NSGA-III, MOEA/D, exact, or other implementation and no fair tuning result. This is a declared limitation, not evidence that those comparator families are weaker.

## 2. Pairing and compute budgets

Formal analysis uses seed indices 0--29. Within each task family, every arm and baseline receives the same family-specific seed for a given index. The RTS and SimBench seed-value lists differ; seeds are never substituted. Five disjoint pilot indices use separate seeds and cannot contribute to formal estimates.

The primary `matched_unique_evaluations` protocol ends at 3,200 cache-miss phenotypes or 6,400 total scoring requests, whichever occurs first. Every request increments `requested_evaluations`; a cache miss additionally increments `unique_evaluations`, while a hit increments `cache_hits`. Population and local search share one cache per run. A method that reaches the request backstop before 3,200 unique evaluations retains the shortfall and termination reason and is not extended selectively.

The secondary `matched_wall_time` protocol has a 0.20-second monotonic-clock search deadline, checked before each scoring request. The same 3,200-unique and 6,400-request ceilings are safety caps. Final-front extraction and metrics occur after the search clock. Both target and realized search time, total process time, requested and unique evaluations, and cache hits are retained. Wall time is machine-specific; it is never pooled across environments.

There are 720 planned formal runs: 2 task families x 6 methods x 30 seed indices x 2 protocols. Per-run requests and unique evaluations are outcomes bounded as above; therefore no fabricated aggregate realized count is stated before execution.

## 3. Outcomes and metric rules

All objectives are minimized. Only feasible, finite, unique objective vectors enter a run's non-dominated front. The family-specific analytic lower and upper bounds must be inserted into the data manifest and frozen before pilot execution; formal test outcomes cannot set or amend them.

- **Primary outcome:** clipped normalized hypervolume (HV). Normalize objective `q` as `(f_q-L_q)/(U_q-L_q)`, clip to `[0,1]`, and use reference coordinate 1.05 in every dimension. An empty feasible front has HV 0. The implementation and objective-count-specific reference vector must pass the pilot gate.
- **Secondary quality outcome:** IGD+. Within each task family, task instance, and compute protocol, form one empirical reference set from the non-dominated union of feasible finite fronts from all frozen methods and all 30 formal seed indices, using the same frozen normalization. Compute minimization-form IGD+ from each run front to that shared set. Do not pool families. If the union is empty, IGD+ is unavailable for the whole cell; if a run front is empty while the reference exists, its IGD+ is positive infinity and remains a failure-relevant outcome.
- **Feasibility outcomes:** any feasible final solution, feasible fraction of the final population, feasible-front cardinality, minimum/mean normalized budget violation, repair calls/removals, and termination reason. These establish only benchmark-budget feasibility, not AC load-flow, OPF, construction, expert, or deployment feasibility.
- **Cost outcomes:** selected synthetic cost units, cost-to-budget ratio, and feasible-front cost distribution. A calibrated-cost column may be populated only after a traceable calibration source and transform are frozen; otherwise it remains null and the label “synthetic benchmark units” is mandatory. No ROI or real investment-effectiveness inference is allowed.
- **Compute outcomes:** requested evaluations, unique evaluations, cache hits, target/realized search seconds, total process seconds, and cap reached.

## 4. Comparisons and multiplicity

The analysis unit is one seeded method--task-family invocation and pairing is by family plus seed index. Each task family has its own families of tests; results are never pooled across RTS and SimBench.

For primary HV, the orthogonal family contains four paired contrasts (`forward_only-nds_only`, `bidirectional-backward_only`, `backward_only-nds_only`, `bidirectional-forward_only`) plus the paired interaction. The baseline family contains `bidirectional-nsga2` and `bidirectional-pareto_local_search`. Each family uses a two-sided paired randomization/sign-flip test at alpha 0.05 with Holm adjustment across its frozen contrasts. The same contrast structure for IGD+ is a separately corrected secondary family. Wall-time outcomes and feasibility/cost/compute outcomes are descriptive unless a later protocol amendment is made before any formal result exists.

Report the paired median difference, Hodges--Lehmann paired location estimate, rank-biserial effect size, and a deterministic seed-index bootstrap 95% interval alongside adjusted p-values. Ties remain in descriptive summaries and contribute zero to signed statistics. A combined arm supports a joint conclusion only; a component or interaction claim requires its registered contrast.

## 5. Failures, visibility, and negative results

Infrastructure failures may be rerun once with the identical method, task snapshot, configuration hash, environment, and seed. Both attempts remain in the ledger. Algorithmic exceptions, non-finite objectives, cap shortfalls, and empty feasible fronts are outcomes, not infrastructure rerun grounds. Seeds are never replaced.

Inference uses paired blocks with valid outcomes for every method needed by that contrast; excluded blocks and reasons are reported per contrast. There is no imputation. If more than 3 of 30 blocks are unavailable for a contrast, or failures are method-dependent, that contrast is downgraded to descriptive and marked inconclusive. The full failure table remains visible.

All positive, negative, null, reversed, and inconclusive results are retained. In particular, this stage cannot erase the protected historical finding that BiLo-NSGA loses four of eight primary matched-evaluation comparisons to NSGA-II and wins none. A favorable result in one new family cannot be generalized to the other family, the historical proxy, or deployment. Pilot output is diagnostic only and cannot appear as confirmatory evidence.

## 6. Execution gate

`RUNBOOK.md` is the controlling order of operations. Formal execution is **NO-GO** until every pending field in `data_manifest.json` and `environment.json` is filled from inspected evidence, both independent source/action registries validate, objective/cost implementations and numeric bounds are frozen, pilot accounting passes, and hashes are recorded. Filling those evidence-bound values requires a pre-run manifest revision and new hashes; it may not change the arms, seed indices, compute caps, metric rules, comparison families, correction, or failure/negative-result policies after any formal result is visible.

This protocol adds no cybersecurity semantics, experiment run, numerical result, calibrated cost, expert label, or deployment evidence.
