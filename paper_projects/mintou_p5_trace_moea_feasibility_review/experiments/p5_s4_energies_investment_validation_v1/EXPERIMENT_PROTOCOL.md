# P1 Frozen Confirmatory Experiment Protocol

**Stage:** `p1_v2_s04_frozen_experiment_protocol`

**Status:** `FROZEN / NOT_EXECUTED / NO_RESULTS`

**Frozen on:** 2026-09-05 (Asia/Shanghai)

**Machine-readable authority:** `config.json`

**Protected predecessor:** `../p5_s3_matched_sensitivity/` is read-only.

This protocol is prospective. It records planned comparisons and cannot be
cited as an experiment result. Pilot outputs, if any, belong under `pilot/` and
are excluded from tuning, confirmatory analysis, and manuscript result tables.

## Data, Licence, and Task-Family Freeze

The only optimization data permitted are a freshly materialized copy of the
existing 120-candidate P5 proxy pool, deterministically constructed from the
documented RTS-GMLC, SimBench, and NERC-metadata inputs. The source files and
candidate table are not present in this isolated worktree. Their licences and
redistribution permissions have not been verified here; formal execution must
stop until the data manifest is completed with immutable file hashes and
source-specific licence evidence. Synthetic costs remain synthetic units.

Candidate-level cost calibration and AC/OPF validation are `NO_GO`. The
portfolio bits do not map to auditable cost records or to buses, branches,
generators, topology, dispatch, or controls. Existing NERC/MTEP16 analyses are
`DESCRIPTIVE_ONLY` and are not rerun or included in the confirmatory family.

Task families are disjoint:

- development/tuning only: `benchmark_portfolio_optimization`,
  `distribution_project_review`, `reliability_driven_review`, and
  `renewable_accommodation_review`;
- confirmatory only: `budget_ranking_stability`,
  `preference_aware_support`, and `traceability_evaluation`;
- descriptive external checks: existing NERC/MTEP16 artifacts only.

No development scenario, development seed, pilot row, or legacy outcome may be
used in confirmatory model selection or inference.

## Methods and Component Matrix

All stochastic methods receive exactly 3,200 objective-function calls per
method--scenario--seed run. The four hybrid arms isolate the named layers:

| Arm | NDS/search kernel | Deterministic repair | Preference-guided retention | Interpretation |
|---|---|---|---|---|
| Full TRACE | on | on | on | joint system |
| NoPreferenceRanking | on | on | off | direct preference-retention control |
| NoFeasibilityRepair | on | off | on | direct deterministic-repair control |
| NSGA2Only | on | off | off | bare NDS/search control; joint removal of both added layers |

The strong stochastic baselines are tuned NSGA-II, tuned R-NSGA-II, and tuned
MOEA/D. AHP-TOPSIS, Weighted Sum, and Greedy BCR are deterministic descriptive
references; they are not assigned fake replicates or treated as having a
stochastic evaluation budget. `NSGA2Only` supports a joint comparison only and
must not be described as isolating either removed layer.

## Tuning Freeze and Separation

Only Full TRACE, NSGA-II, R-NSGA-II, and MOEA/D are tuned. Each receives four
predeclared configurations, the same four development scenarios, the same ten
development seeds, 3,200 calls per run, and a 30-minute wall-time cap per run.
The grids are frozen in `config.json`. Selection maximizes the median primary
HV over all development cells; exact ties use the lexicographically smallest
configuration ID. The selected configuration and every grid result must be
released. Ablations inherit the selected Full TRACE settings except for their
named switch, preventing separate favorable tuning.

The thirty confirmatory seeds and three confirmatory scenarios are disjoint
from tuning. After the first confirmatory objective value is visible, no method
configuration, bound, outcome, comparison family, or failure rule may change.

## Budgets

- stochastic run: exactly 3,200 objective-function calls and at most 1,800
  wall-clock seconds;
- deterministic reference: one complete deterministic execution and at most
  120 seconds, reported descriptively;
- tuning: 640 runs total (4 methods x 4 configurations x 4 development
  scenarios x 10 seeds), hence 2,048,000 planned objective calls;
- main confirmatory matrix: 630 runs (7 stochastic methods x 3 confirmatory
  scenarios x 30 seeds), hence 2,016,000 planned objective calls;
- budget scan: Full TRACE, NSGA-II, and R-NSGA-II at
  0.75/0.88/1.00/1.25 times B in `preference_aware_support`; the 1.00-B cells
  reuse the main matrix, so 270 additional runs and 864,000 additional calls;
- total unique formal stochastic workload: 900 runs and 2,880,000 calls.

Early stopping, cross-method caching, and adding calls after timeout are
forbidden. Wall time is a failure guard and a secondary implementation metric,
not a cross-platform efficiency claim.

## Outcomes and Method-Independent Bounds

The primary outcome is five-dimensional feasible-front hypervolume using
definition-derived conservative analytic bounds in `bounds.csv`, no clipping,
and reference point `(1.1,1.1,1.1,1.1,1.1)`. The nominal and 0.88-B numeric
bounds are copied from the preserved Stage-3 analytic-bound artifact whose
SHA-256 is recorded in every row. The 0.75-B and 1.25-B scan rows apply the same
analytic rule, changing only the cost upper bound to the frozen budget. Their
construction uses no method output. The Stage-4 file hash is frozen in
`config.json` and must match every future run manifest.

Secondary outcomes are: legacy clipped empirical-bound HV at reference 1.1;
analytic-bound HV at reference 1.2; common-reference IGD+; feasible returned-
front proportion; budget utilization; synthetic cost index; portfolio
cardinality; risk proxy; and event-position co-occurrence. Event counts and
co-occurrence do not establish replacement, lineage, replay, explanation
quality, human value, or deployment effectiveness. The three deterministic
engineering translations (cardinality difference, budget-utilization
difference, and risk-proxy difference) are reported alongside HV and remain
descriptive.

## Estimand, Comparison Family, and Multiplicity

The analysis unit is one paired method--scenario--seed run. The primary
estimand is the paired difference in primary HV between Full TRACE and each of
the six stochastic opponents within each of the three confirmatory scenarios.
All 18 two-sided paired sign tests form one confirmatory family and receive a
single Holm correction at familywise alpha 0.05. Report the raw and adjusted
p-values, paired median difference, rank-biserial effect, and a 5,000-resample
paired bootstrap confidence interval. Scenario-balanced pooled summaries and
all secondary outcomes are descriptive and cannot replace a failed primary
test. Deterministic references are excluded from inferential tests.

Preference-strength labels are computed from frozen scenario weight vectors as
`D(s)=std(w)/mean(w)` before method execution and are descriptive strata only;
they do not create a post hoc testing family.

## Failure and Negative-Result Policy

Infrastructure failures before an objective call may be rerun once with the
same method, scenario, seed, configuration, and environment after documenting
the cause. Algorithm exceptions, non-finite objectives, budget overruns, and
wall-time overruns are outcomes: keep the row, mark it failed, and do not
replace its seed. If more than 5% of any stochastic method--scenario cell fails,
stop confirmatory inference and report the cell and study incomplete. No
imputation, favorable complete-case substitution, or extra seed is allowed.

Every null, adverse, timeout, infeasible, and normalization-sensitive result is
reported. Failure of Full TRACE to beat a comparator cannot be reframed through
a winning subset, a secondary metric, a different bound, or the budget scan.
Component claims require their direct controls; combined controls support only
joint conclusions. Formal results remain proxy-benchmark findings regardless
of direction and cannot support realized return, electrical feasibility,
expert-review accuracy, causal effectiveness, or deployment claims.

## Execution Gate

`planned_vs_executed.json` is intentionally `NOT_EXECUTED`. Before a pilot or
formal run, complete the data hashes/licence fields, verify and hash
`bounds.csv`, verify the exact runtime from `environment.json`, and implement an
objective-call counter. Any change after this freeze requires a dated amendment
that states whether outcomes had become visible; outcome-informed amendments
invalidate confirmatory status.
