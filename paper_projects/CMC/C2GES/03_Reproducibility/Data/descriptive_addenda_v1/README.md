# Descriptive Addenda v1 (Q1 / Q6 / Q10)

Deterministic, aggregate-only descriptive analyses answering three external-reviewer
questions on the C²GES Information manuscript (2026-09-25). No verbatim report or
reference text is written here; per-unit records carry identifiers and counts only.
Nothing in this directory upgrades any claim: all outputs are descriptive and close
no row of the evidence gates.

## Questions

- **Q1 — path-change error profile** (`q1_path_change_error_profile_*.csv`): for the
  seven-series matched-budget pilot, units whose selection changed between Full (AB-5)
  and no-path (AB-6), decomposed by typed-edge incidence, chronology-violating incident
  edges, incident-edge distance profile, and role-compatible pairs blocked by the
  12-position window.
- **Q6 — per-role token alignment** (`q6_per_role_precision_coverage_*.csv`): selected
  units and reference sentences labeled by the SAME lexical cues (unit-scaled within
  each text set, abstaining on ties); token precision = share of role-r selected-unit
  content tokens occurring in role-r reference sentences; token coverage = share of
  role-r reference-sentence content tokens recovered by the extract. Token level is
  used because sentence-level ROUGE-L recall against differently worded
  executive-summary sentences essentially never fires (verified during development).
  Reference-side roles are sparse (root cause never fires); empty cells are structural.
- **Q10 — long-block audit detail** (`q10_*.csv`): per-condition legacy long-unit
  counts (unit budgets K=5/10, 15 historical test reports), the block-preserving
  audit distribution over all 27 historical reports, and non-verbatim examples of
  long selected units (word counts, table markers, reference-token overlap). The
  block-preserving segmentation was not used to rerun ranking; whether the relative
  ordering would change remains unanswered by design.

## Provenance

- Code: `03_Reproducibility/Code/descriptive_addenda_v1/run_descriptive_addenda.py`
  (tests: `test_descriptive_addenda.py`, 5/5 pass, Python 3.12).
- Inputs (SHA-256 recorded in `ADDENDA_MANIFEST.json`): the exploratory pilot dataset
  (private derived JSONL, not redistributed), `factorial_selected_ids.jsonl`,
  `factorial_item_metrics.csv` (e3_factorial_exploratory_v3), the historical test
  dataset and formal `predictions.jsonl` (applied_sciences_dual_rebuild workspace),
  `layout_unit_per_report.csv` (postrun_layout_audit), and
  `output_length_per_report.csv` (postrun_diagnostics).
- Deterministic: no sampling, no seeds; rerunning the script reproduces the CSVs
  byte-identically except for the manifest timestamp.

## Boundaries

- Descriptive only; not a confirmatory or unseen evaluation; no new inferential test
  is introduced and no Holm correction is applied (no claims are made).
- Cue-versus-cue alignment is not expert-validated role correctness (see Table S9
  construct audit and the reserved human-validation protocol in the main text).
