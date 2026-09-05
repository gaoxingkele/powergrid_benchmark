# P1 minimal pipeline and feasibility pilot report

## Scope and exclusion

The declared `preference_aware_support` task was run for Full TRACE and
NSGA-II using three paired pilot seeds (`710003`, `710019`, `710031`). This is
a diagnostic pilot only. `paper_use` is `false`; the rows cannot be used for
configuration selection, confirmatory inference, a manuscript result, or a
claim that either method is better.

The six distinct method--seed rows are in `raw/results.csv`. The pilot score
values are intentionally not summarized here because their direction or
magnitude is outside this gate's decision rule.

## Checks performed

- Data lineage: PASS for local execution. The 120-row candidate snapshot,
  registered builder snapshot, seven source tables, NERC metadata index, and
  available licence/notice files are individually hashed in
  `input_manifest.json`. No NERC PDF or report text was copied.
- Budget equality: PASS. Both methods evaluated exactly 3,200 candidate
  vectors in every seed cell under the same declared 1,800-second failure cap.
- Synthetic cost and feasibility: PASS. Every recorded compromise cost was
  computed from the candidate cost vector; every budget-utilization value was
  between zero and one, and every returned population had feasible proportion
  1.0. These are synthetic-budget checks, not electrical-feasibility evidence.
- Metric orientation: PASS. All five objectives are minimized; feasible-front
  hypervolume is maximized; zero budget violation denotes feasibility. The
  primary calculation used the frozen analytic bounds without clipping and
  the normalized LF hash matched the frozen Stage-4 hash.
- Deterministic replay: PASS. Every method--seed cell was independently rerun;
  objective-call counts, selected-front hashes, and primary HV values matched
  exactly (`replay_audit.csv`).
- Output schema: PASS. `raw/results.csv` follows the frozen required field
  order and binds the config, data-manifest, environment, and bounds hashes.
- Resource estimate: recorded in `resource_estimate.json`. The six distinct
  runs took 0.6714 seconds in total on this host excluding replay, or 0.1119
  seconds per run on average. A mechanical serial extrapolation for 900 formal
  runs is 100.71 seconds. This is only a host-specific feasibility estimate;
  it excludes tuning, replay, statistics, I/O and concurrency effects and is
  not a formal runtime promise or cross-platform efficiency claim.

## Warning review

Every captured warning is retained in `warnings.csv` and was inspected:

1. NumPy was planned as 1.26.4 but resolved as 2.4.6. Formal execution stops;
   no version-equivalence or silent-substitution claim is made.
2. SciPy was planned as 1.12.0 but resolved as 1.18.0. Formal execution stops;
   no version-equivalence or silent-substitution claim is made.
3. NERC metadata was used locally, but access to the official website does not
   establish permission to redistribute the pilot metadata index. No NERC PDF
   or report text is included. Release remains blocked pending human/legal
   review.

No runtime library warning was emitted during the final pilot execution.

## Gate decision

The mechanical pilot gate is `PASS`, and formal execution is `STOPPED`.
Recreate the frozen package environment and resolve the NERC metadata release
permission before any tuning or formal run. No warning was tuned away, no
additional seed was added, and no pilot outcome changed the configuration,
metric, task, or decision.
