# C2GES Human Structural Validation Protocol

Status: `DRAFT_NOT_FROZEN`  
Version date: 2026-09-06

This protocol validates extraction-unit boundaries, lexical roles, typed edges, typed paths, page locators, source faithfulness, and critical omissions. It must be frozen before annotators see sampled items. Model scores, condition names, and the other annotator's decisions remain blinded during independent annotation.

## Annotators and sampling

- Two independent annotators are required; at least one must have documented power-system reliability, event-analysis, or closely related technical-report experience.
- Target samples are 200 extraction units used for boundary assessment and 200 role judgments (these may be paired views of the same sampled units), 150 typed edges, 80 typed paths, and 30 system-summary sets.
- Sampling must span report series, development/external partitions, layout types, confidence strata, path/no-path units, document-order agreement/disagreement, and Full/no-path agreement/disagreement.
- Sampling code, seed, source hashes, and a rights-safe manifest must be frozen before labeling.

## Blinding and file separation

- `SAMPLING_MANIFEST_TEMPLATE.csv` is an administrator-only schema. It may contain the system condition, automated role, confidence stratum, selection agreement, and source-locator hash. It must not be given to annotators.
- Each annotator receives a securely prepared context packet keyed only by `sample_id` plus one copy of `annotation_form_blank.csv`. The context packet may show the minimum source context required by the task, but it must not show model scores, automated labels, condition names, the other annotator's decisions, or verbatim material outside the project's access rights.
- The command `human_validation.py prepare` creates label-only A/B forms from a completed sampling manifest. Its packet-preparation receipt is retained by the study administrator rather than distributed as annotation material.
- Annotator identifiers must be distinct pseudonyms. Free-text notes are limited to 240 characters, must be non-verbatim, and must not reproduce restricted report text.
- Packet order may be independently randomized by the administrator, but the `sample_id`/`task` key must remain unchanged and the randomization seed must be recorded in the frozen sampling record.

## Stage lock and adjudication

1. Validate the completed independent A/B files with `human_validation.py pre`. The command refuses missing task labels, irrelevant populated fields, duplicate or mismatched samples, shared annotator IDs, and invalid labels.
2. The pre-adjudication artifact stores SHA-256 values for the schema, sampling manifest, and both independent label files, along with raw agreement, Cohen's kappa, and the exact disagreement set.
3. Only after that artifact is frozen may adjudication begin. The adjudication file is long-form and contains exactly one row per frozen disagreement; agreed items must not be re-adjudicated.
4. `human_validation.py final` fails closed if any frozen input changed, a disagreement is missing, an agreement was added, the original A/B values were altered, or an adjudicated label is outside the task schema.
5. Final outputs are computed evidence, not an automatic scientific conclusion. Authors must inspect the distributions, uncertainty, exclusions, and failure taxonomy before revising claims.

## Tasks

1. Unit validity: `standalone`, `needs_adjacent_context`, `fused_or_malformed`, `header_footer_table_contamination`, or `cannot_judge`.
2. Role validity: `root_cause`, `trigger_event`, `propagation_response`, `impact`, `mitigation`, `none_other`, or `ambiguous_multiple`.
3. Edge validity: relation support, direction, lexical-only false relation, and context sufficiency.
4. Path validity: `coherent`, `partially_coherent`, `unsupported`, `directionally_inconsistent`, or `cannot_judge`; also record whether the path adds information beyond role reservation.
5. Faithfulness and omission: factual preservation, negation/condition/actor/time distortion, critical condition/impact/mitigation omission, and page-locator correctness.

## Analysis and claim gates

Report pre-adjudication raw agreement and Cohen's kappa or Krippendorff's alpha as appropriate. Report role macro precision/recall/F1, supported-edge precision, direction accuracy, path-coherence proportions, source-faithfulness rate, critical-omission rate, and layout/confidence strata. Single-label role metrics exclude `cannot_judge` and `ambiguous_multiple`; both exclusions are reported separately and must not be silently folded into a single role. Rate estimates use report-series-equal aggregation with series-cluster bootstrap intervals. Study-specific operating thresholds are role macro-F1 >= 0.70, role/edge agreement >= 0.60, supported-edge precision >= 0.70, coherent-or-partially-coherent paths >= 0.70, page-locator accuracy = 1.00, and source-faithfulness >= 0.90. These are internal decision thresholds, not universal domain standards.

If a threshold is missed, the associated construct must be described as a heuristic proxy and the manuscript claim downgraded. Adjudication occurs only after pre-adjudication metrics are frozen. The authors must record the applicable institutional ethics review or exemption determination before recruitment; this file does not make that determination.
