# P3 Frozen 2-by-2 Mechanism and AC-Validation Protocol

**Stage:** `p3_v2_s04_frozen_experiment_protocol`

**Protocol status:** `FROZEN`

**Execution gate:** `BLOCKED_ACTION_AND_AC_PROVENANCE / NO_RESULTS`

**Protected predecessor:** all P3 S3 scripts, archives, and reported values are read-only.

`FROZEN` means that the prospective comparison and analysis rules below may not
be changed after results are inspected. It does not mean that the experiment is
ready to run. Formal and pilot execution remain prohibited until every blocker
in Section 11 is resolved and recorded before execution. No optimizer or power-
flow result was generated for this protocol stage.

## 1. Scientific question and analysis unit

The confirmatory question is whether parameter adaptation, strategy adaptation,
or their interaction changes five-objective proxy-front quality under the fixed
planning benchmark and equal objective-row budget. The optimizer master seed is
the independent analysis unit. Network, operating-case, and selected-plan rows
are repeated measurements nested within a seed and must never be counted as
independent optimizer replicates. For the paper-level primary estimate, compute
each seed's contrast separately in each of the six configurations and then take
their equal-weight mean; configurations are a fixed panel and receive no
population-level inference.

The AC layer asks whether the plans selected by a frozen, method-neutral rule
remain feasible under the registered actions and six deterministic operating
cases. It is an engineering validation outcome, not a replacement for the
optimizer outcome and not deployment evidence.

## 2. Frozen four-arm factorial

| Display name | Arm ID | Parameter adaptation | Strategy adaptation |
|---|---|---:|---:|
| Fixed-Fixed | `fixed_parameter__fixed_strategy` | off | off |
| AdaptiveParam-FixedStrategy | `adaptive_parameter__fixed_strategy` | on | off |
| FixedParam-AdaptiveStrategy | `fixed_parameter__adaptive_strategy` | off | on |
| Full-SAMODE | `adaptive_parameter__adaptive_strategy` | on | on |

All four arms use the implementation semantics in
`../../manuscript/reconstruction_v2/METHOD_IMPLEMENTATION_CONTRACT.md`:
fixed values (F=0.5, CR=0.9), jDE resampling probability 0.1, `rand/1` as the
fixed strategy, a success-driven `rand/1`/`best/1` pool when enabled, heritable
controls, and independent labelled parameter and strategy random streams.
Initialization, decoding at `g >= 0.5`, repair, objectives, selection,
population 40, data visibility, stopping, and seeds are otherwise identical.

The factorial estimands are the parameter main effect averaged over both
strategy levels, the strategy main effect averaged over both parameter levels,
and the difference-in-differences interaction. Full-SAMODE versus Fixed-Fixed
is a joint contrast only; it cannot identify either mechanism.

## 3. Direct controls

Three direct controls are confirmatory and receive the same data, decoder,
population size, seed, initialization contract, objectives, and objective-row
ceiling. Their constraint handling is frozen as stated below:

- `GDE3`: pinned pymoo 0.6.2 generalized DE with `rand/1/bin`, F=0.5,
  CR=0.9, the common `g >= 0.5` decoder, and explicit budget violation.
- `NSDE`: pinned pymoo 0.6.2 non-dominated-sorting DE with `rand/1/bin`,
  F sampled from `[0.3, 0.9]`, CR=0.9, the common decoder, and explicit budget
  violation.
- `NSGA-II`: pinned pymoo 0.6.2 with binary encoding, two-point crossover
  probability 0.9, bit-flip probability `1/n`, and explicit budget violation.

No control may receive extra objective calls, action information, AC outcomes,
or confirmatory-seed feedback during tuning.

## 4. Public data, cases, and action contract

The proxy source is the public SimBench complete mixed dataset
`1-complete_data-mixed-all-0-sw`. The three source-table hashes are frozen in
`data_manifest.json`. The benchmark configurations are base, storage-excluded,
DER-excluded, load 1.3x, budget 0.82x, and budget 1.20x. These are fixed
benchmark configurations, not a random sample of distribution grids.

The AC panel is frozen at four SimBench MV classes already evidenced by the
archive: rural, semi-urban, urban, and commercial. Exact machine identifiers
and file hashes are not present in the worktree evidence and therefore remain
blocked rather than guessed. Before any pilot, `data_manifest.json` must be
amended in a protocol-versioned, pre-result record with the verified identifier,
version, retrieval source, license, and SHA-256 for each class. That amendment
may resolve identity only; it may not select networks using observed outcomes.

Each optimizer coordinate must have exactly one row in `action_registry.json`.
Permitted kinds are reinforcement (registered line and parallel-circuit
increment), storage (registered bus and capacity increment), DER (registered
bus and capacity increment), and automation (registered switch action). Costs
are non-negative benchmark cost units unless an external monetary source is
provided. A row must contain the fields enforced by
`validate_complete_registry`; missing, extra, duplicated, or type-inconsistent
bindings are hard failures. Case-dependent stress rankings are forbidden as a
substitute for a registered target. The current empty registry is an explicit
blocker, not an action set with zero candidates.

## 5. Paired seeds, tuning separation, and budgets

- Pilot seeds: `99001, 99002, 99003`; pipeline checks only, never paper results.
- Tuning seeds: `91001` through `91010`; tuning only.
- Confirmatory paired master seeds: `11001` through `11030`.
- Statistics/bootstrap random seed: `73021`.

The three sets are disjoint. Each method receives the same master seed for a
given paired block. Labelled substreams isolate initialization, parameter,
strategy, variation, selection, and analysis randomness. A failed run retains
its seed; it is not replaced with a more favorable seed.

Every confirmatory method-run has a ceiling of exactly 4,800 raw proxy-
objective rows. The counter includes initial, parent, repeated, and trial rows,
whether or not a cache is used. Normalization-reference construction and AC
post-validation are shared post-processing and are not charged to one method.
Generated candidates, raw objective rows, unique phenotypes, cache hits, repair
calls/removals, power-flow attempts/failures, and wall time are logged
separately. Wall time is provenance, not the fairness budget.

## 6. Plan selection and AC operating cases

For each method and confirmatory seed, retain the final feasible non-dominated
front and select up to five distinct plans by increasing Euclidean distance to
the equal-weight ideal point after the same analytic normalization used for the
primary outcome. Ties are broken by ascending serialized binary phenotype and
then front-row index. If fewer than five distinct feasible plans exist, retain
all and log the shortfall; do not duplicate plans.

Every selected plan is applied through the complete registry to a fresh network
copy and evaluated in all cases below:

| Case ID | Load multiplier | Existing DER multiplier | Contingency |
|---|---:|---:|---|
| `base` | 1.0 | 1.0 | none |
| `peak_load` | 1.3 | 1.0 | none |
| `load_growth` | 1.5 | 1.0 | none |
| `extreme_growth` | 1.8 | 1.0 | none |
| `high_der` | 0.5 | 2.5 | none |
| `growth_n_minus_one` | 1.5 | 1.0 | one preregistered in-service branch |

Loads scale active and reactive demand. Existing DER scales active generation.
The exact N-1 branch, DER reactive-power/power-factor policy, storage dispatch,
and transformer criterion are unresolved blockers and must be frozen before a
pilot. No outcome-dependent operating policy is permitted.

## 7. Outcomes and method-independent reference

The primary outcome is unclipped analytic-normalized hypervolume. Each of the
five minimization objectives is normalized using equation-derived feasible
bounds fixed without inspecting any compared method's outputs. In normalized
space, the method-independent reference point is
`(1.05, 1.05, 1.05, 1.05, 1.05)`; higher hypervolume is better. Any point that
does not dominate that reference is retained in the raw front and flagged; it
is not silently clipped into dominance.

Secondary optimizer outcomes are:

- IGD+ (lower is better) against the non-dominated union of all complete
  confirmatory fronts within the same benchmark configuration, after analytic
  normalization. This is one common empirical reference applied to every
  method, but because the tested methods construct it, it is complementary and
  not an independent external reference.
- final-front size and feasible-candidate fraction as descriptive diagnostics.

Engineering outcomes are convergence, inclusive voltage feasibility
`0.95 <= V <= 1.05` pu, inclusive line loading `<= 100%`, the preregistered
transformer criterion, overall feasibility (all applicable gates pass), losses,
minimum/maximum voltage, and maximum line/transformer loading. The primary AC
summary is each seed's proportion of its registered plan-network-case rows that
are feasible. Component failure rates and continuous margins are secondary.
These proportions describe this fixed panel; they are not grid-population
feasibility probabilities.

## 8. Statistical and multiplicity rules

All inferential comparisons use paired confirmatory seeds. Report paired median
and mean differences with seed-level bootstrap 95% confidence intervals. Use a
two-sided paired sign-flip randomization test with 1,000,000 Monte Carlo draws
from statistics seed 73021 for each contrast; zero differences are retained. The
primary family contains six two-sided paired contrasts on primary HV: the two
factorial main effects, their interaction, Full-SAMODE versus GDE3,
Full-SAMODE versus NSDE, and Full-SAMODE versus NSGA-II. Holm correction
controls family-wise alpha at 0.05. Unadjusted and adjusted p-values must both
be exported. The same six
contrasts for IGD+ and for seed-level AC-feasibility proportions form two
separate, clearly labelled secondary Holm families; they cannot rescue a null
primary result. Configuration-specific and continuous engineering diagnostics
are descriptive unless separately preregistered before the pilot.

## 9. Failure, missingness, and negative results

Non-convergence, non-finite objectives, empty fronts, registry/application
errors, islanding, missing AC outputs, budget overruns, and counter mismatches
produce explicit rows and failure codes. They are never dropped. A method-run
that cannot provide a valid primary front by 4,800 rows receives the
preregistered worst primary score of zero HV. For IGD+, failure receives a
finite worst-rank score equal to one plus the largest valid IGD+ in that
configuration; if no method is valid, the paired configuration block is an
infrastructure incident. A complete-case sensitivity analysis may be shown only
alongside the intention-to-run analysis. AC application or power-flow failure is
engineering-infeasible for that registered row. Infrastructure-wide failures
that affect all methods in a seed block suspend that block pending an incident
record; they do not authorize selective reruns.

All null, negative, reversed, or failure findings are retained.
No post-hoc subset, reference point, favorable network, metric, or seed may
replace the frozen primary result. A positive joint Full-SAMODE contrast cannot
be attributed to one gate. A proxy advantage cannot be described as electrical
or deployment superiority, and an AC-feasibility advantage cannot be described
as economic value.

## 10. Pilot and formal separation

The pilot uses only the three pilot seeds and exists to test deterministic
replay, schema completeness, equal counters, registry coverage, action
application, and failure logging. Its outputs are stored under `pilot/`, carry
`paper_use=false`, and are excluded from tuning and confirmation. Formal runs
may start only after the pilot gate passes and a config/environment hash is
recorded. Formal outputs may not overwrite pilot or legacy namespaces.

## 11. Frozen gate disposition

Formal and pilot execution are currently **BLOCKED** because the evidence does
not provide: (1) a complete nodal action registry and capacity/cost provenance;
(2) verified exact identifiers and hashes for the four AC networks; (3) storage
dispatch and DER reactive-power rules; (4) a fixed N-1 branch; (5) a transformer
loading criterion or justified non-applicability; or (6) a verified pandapower
runtime pin. Resolving these items is a
pre-execution protocol completion record, not permission to alter arms, seeds,
budgets, primary metric, comparison families, or negative-result rules.

## 12. Required output keys

Optimizer rows are keyed by `(configuration_id, method_id, seed)` and contain
status, failure code, counters, front artifact, primary HV, IGD+,
and timing provenance. AC rows are keyed by
`(configuration_id, method_id, seed, plan_rank, network_id, scenario_id)` and
contain the phenotype/action IDs, benchmark cost, convergence, voltage/loading/
loss outputs, transformer policy result, failure code, and feasibility flag.
`planned_vs_executed.json` is initialized with zero executed runs and must be
updated without deleting planned or failed cells.
