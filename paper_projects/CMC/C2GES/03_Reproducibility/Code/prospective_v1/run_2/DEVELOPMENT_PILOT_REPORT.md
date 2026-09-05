# C2GES component-factorial development pilot (Run 2)

## Status and permitted use

This run is an implementation and mechanism-diagnostic pilot on the existing
development split. It is **not** E1, is **not** confirmatory E3, and does not
support claims of external validity or system superiority. The external test set
was not accessed (`external_test_accessed=false`), and confirmatory claims are
disabled (`confirmatory_claims_allowed=false`).

Run 2 supersedes Run 1 for implementation diagnostics. The only scientific-code
change was to make G-U use the same lexical-overlap function as G-T, so that the
graph contrast does not mix edge typing with a tokenization change.

## Execution audit

- Input: 12 development reports grouped into 6 report series.
- Conditions: AB-0--AB-6, RP-00/RP-10/RP-01/RP-11, and G-U/G-T.
- Budgets: 110 and 260 words, enforced during selection over the complete rank.
- Rows: 312 expected and 312 passed; failed rows: 0.
- Budget check: no selected output exceeded its assigned budget.
- Controlled identities: AB-5=RP-11, AB-6=RP-10, and AB-6=G-T held at the
  selected-unit level for every report and budget.
- Rights-safe output: selected-output records contain identifiers and audit
  fields, not candidate or reference text.
- Machine validation: `py -3.12 validate_run.py run_2` returned `VALIDATION PASS`.

## Exploratory observations (not manuscript results)

| Contrast | Budget | Mean ROUGE-L difference | Series-cluster 95% interval | Holm-adjusted exact value |
|---|---:|---:|---:|---:|
| AB-5 minus AB-6 | 110 | -0.00557 | [-0.01276, 0.00027] | 1.00 |
| AB-5 minus AB-6 | 260 | 0.00650 | [-0.00144, 0.01598] | 1.00 |
| G-T minus G-U | 110 | 0.00016 | [-0.00091, 0.00155] | 1.00 |
| G-T minus G-U | 260 | 0.00207 | [-0.00488, 0.00769] | 1.00 |
| Reservation main effect | 110 | -0.00133 | [-0.00469, 0.00243] | 1.00 |
| Path main effect | 110 | -0.00296 | [-0.00812, 0.00224] | 1.00 |
| Reservation main effect | 260 | 0.00442 | [-0.00122, 0.01186] | 1.00 |
| Path main effect | 260 | 0.00503 | [0.00042, 0.01035] | 0.75 |

The six-series development sample is too small and already participates in
method development. Accordingly, interval direction, exact values, and component
rankings above are implementation diagnostics only. They must not determine
external-test exclusions, endpoints, comparison families, or post-hoc tuning.

## Remaining work before formal E3

1. Freeze the eligible unseen-series inventory and the one-attempt external
   protocol before opening report contents.
2. Freeze the layout-aware candidate builder and pass the boundary audit.
3. Freeze balanced tuning decisions without accessing external-test outcomes.
4. Separate shared preprocessing cost from condition-specific cold-run resource
   benchmarking; current pilot memory is selection-level Python allocation, not
   total process peak memory.
5. Execute the frozen external runner once, then backfill the manuscript only
   from its version-bound outputs.
