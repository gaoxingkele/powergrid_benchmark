# C2GES layout-boundary audit protocol

Version: 1.0  
Date: 2026-09-06  
Status: `FROZEN_FOR_DEVELOPMENT_PILOT / HUMAN_LABELS_PENDING`  
Applies to: `layout_dev_pilot_v2/layout_boundary_sample_blank.csv`

## Purpose

This audit evaluates whether the layout-aware builder produces usable extraction
units before its rules are frozen for a clean external-series run. It does not
evaluate summary quality, graph validity, or system superiority.

## Review process

Two reviewers independently inspect each sampled locator in the local source PDF.
They must not view model scores, selected summaries, ROUGE values, or each other's
labels. Each reviewer enters one of the following values in their own reviewer
column:

- `valid_standalone`: complete and understandable without adjoining text;
- `valid_with_adjacent_context`: boundary is intact but interpretation requires
  immediately adjoining material;
- `fragment_or_truncated`: extraction begins or ends inside a statement;
- `fused_unrelated_content`: more than one unrelated statement was merged;
- `header_footer_contamination`: running matter or page numbering remains;
- `table_body_fusion`: table content and prose were incorrectly mixed;
- `incorrect_unit_type`: boundary is usable but `unit_type` is wrong;
- `duplicate`: substantively duplicates another candidate in the same report;
- `cannot_judge`.

If either reviewer selects a contamination/error label, `contamination_type` must
repeat the applicable label. Free-text notes must remain non-verbatim and must not
copy report sentences. Agreement is calculated before any discussion. The
reviewers then adjudicate disagreements and enter the final label in
`adjudication`.

## Predefined estimands and gates

- Primary candidate-validity rate: adjudicated proportion labelled
  `valid_standalone` or `valid_with_adjacent_context`, excluding only
  `cannot_judge` from the denominator.
- Primary pass gate: candidate-validity rate >= 0.90.
- Table/body fusion rate: proportion labelled `table_body_fusion` among all
  auditable sampled units; pass gate <= 0.05.
- Header/footer contamination rate: reported separately with a target of zero.
- Unit-type accuracy: proportion not labelled `incorrect_unit_type` among
  auditable sampled units, reported overall and by generated type.
- Boundary-risk analysis: report `possible_fragment`,
  `repaired_cross_boundary`, and `tokenizer_length:gt256` strata separately.
- Pre-adjudication agreement: raw agreement plus Krippendorff's alpha or Cohen's
  kappa, with the statistic and its limitations stated explicitly.

No threshold may be changed after either reviewer's labels are inspected. If the
primary gate fails, revise the builder only on development reports, issue a new
version, regenerate a new deterministic sample, and repeat the audit. Do not open
clean external-report bodies until a builder version passes.

## Evidence handling

The public CSV contains hashes and locators only. Source PDFs and private candidate
text remain outside the release package. Completed reviewer files must use coded
reviewer identifiers and must not include copied report text.
