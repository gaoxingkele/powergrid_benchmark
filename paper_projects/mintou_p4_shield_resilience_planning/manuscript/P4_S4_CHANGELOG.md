# P4 Stage-4 Results-Narrative Changelog

Date: 2026-08-13. Stage: `p4_s4_results_narrative`.

## Evidence and artifact contract

- Added `evidence/manifests/p4_s4_results_artifact_manifest_20260813.json` as
  the canonical source map for this stage. It pins the current planning,
  inference, mechanism-control, sensitivity, AC, and stage-3 boundary sources
  by SHA-256 and row count where applicable.
- Added `manuscript/figures/build_results_artifacts.ps1`. It refuses to build
  when a source hash or row count differs from the manifest, derives four CSV
  tables, renders four PNG figures, and writes the output-hash build record
  `evidence/manifests/p4_s4_results_artifact_build_record.json`.
- No optimization, sensitivity, or AC experiment was added or rerun. Existing
  seeds, p-values, intervals, null findings, and negative findings were
  preserved.

## Narrative integration

- Results now lead with the held-out proxy-quality comparison against the
  strongest external comparator, NSGA-II with post-hoc final-population repair.
  The label-level table and figure distinguish four independently seeded
  identical-range blocks from four active configuration changes; the former
  are not described as independent uncertainty regimes.
- Mechanism attribution now presents repair first. Removing repair reduces
  pooled proxy HV by 8.10% and is Holm-significant in 8/8 labels.
- Screening is presented as a quality--call asymmetry: 17,920 versus 51,200
  static plan--scenario objective rows (65% lower), no detected held-out-HV
  difference in 8/8 labels, no equivalence test, no instrumented objective-call
  counter, and no archived wall-clock saving.
- AC language is consistently illustrative and associational. The rebuilt AC
  figure uses the current six-network aggregate (108 mapped cases per method),
  replacing the stale 72-case SimBench-only panel. It does not claim nodal-plan
  validation, independent optimizer replication, or causal mechanism effects.

## Regenerated outputs

- `manuscript/derived_tables/p4_s4_proxy_quality_by_label.csv`
- `manuscript/derived_tables/p4_s4_pooled_framework_quality.csv`
- `manuscript/derived_tables/p4_s4_mechanism_quality_calls.csv`
- `manuscript/derived_tables/p4_s4_ac_mapping.csv`
- `manuscript/figures/fig_proxy_quality.png`
- `manuscript/figures/fig_repair_screening.png`
- `manuscript/figures/fig_screening_quality_calls.png`
- `manuscript/figures/fig_ac_mapping.png`

## Remaining human blockers

- Author identities, affiliations, ORCIDs, CRediT roles, funding, APC
  responsibility, persistent archive URL/DOI, and source-data terms remain
  author inputs.
- The complete shared historical executable/evidence supplement and reciprocal
  shared-infrastructure disclosure in the companion project remain outside
  this isolated stage.

## Build-environment limitation

- The official preview builder refreshed the journal-submission TeX and copied
  the current figures, but this environment has no `pdflatex`; consequently the
  existing journal-submission PDF predates stage 4 and is not a current build.
