# P1 feasibility pilot plan

This plan was fixed before the first pilot objective value was produced. It
does not amend the confirmatory estimand, tuning grid, bounds, or formal seed
schedule.

- Scope: the declared `preference_aware_support` task only.
- Paired diagnostic methods: `Full_TRACE` and `NSGA-II`.
- Paired pilot seeds: `710003`, `710019`, and `710031`; these are disjoint from
  all frozen tuning and confirmatory seeds.
- Per-run search budget: exactly 3,200 evaluated candidate vectors and the same
  1,800-second failure cap.
- Purpose: code activation, candidate lineage, deterministic replay, synthetic
  cost and budget-feasibility calculations, budget equality, metric direction,
  output schema, and resource estimation only.
- Prohibitions: no configuration selection, no extra seeds, no manuscript
  result use, and no change prompted by the direction or magnitude of a pilot
  metric.

Only the minimal cached source tables consumed by the registered builder are
snapshotted under `inputs/`. The NERC input is a metadata index of public
report titles and URLs; no NERC report PDF or report text is redistributed.
NERC website access does not establish a redistribution licence, so the pilot
may test local lineage but cannot clear that issue for a release data package.

The planned package versions are not silently substituted. The pilot records
the resolved environment and treats any difference from `environment.json` as
a reviewed warning that blocks formal execution pending recreation of the
frozen environment.
