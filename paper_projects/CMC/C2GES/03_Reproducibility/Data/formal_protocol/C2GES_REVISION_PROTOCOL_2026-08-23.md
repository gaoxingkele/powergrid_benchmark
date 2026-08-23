# C2GES revision experiment protocol freeze

Freeze date: 2026-08-23 (Asia/Shanghai)
Repository baseline: `840dcce5835423a5cdc3ee9f84eccfc601a6f4f6`
Status: frozen before acquisition or evaluation of any new external report series.

## Scope and evidence classes

The retained v0.3.1 15-report test set remains a descriptive, already observed test set. It will not be reused for tuning. Any new external series must be acquired only after this protocol, kept series-disjoint from development material, and evaluated once after all rules below are fixed. Existing post-run analyses must be labelled exploratory or sensitivity analyses.

## Frozen split and exclusions

- Sampling frame: 40 inspected reports; 27 included, 13 excluded.
- Development: 12 included reports. Retained descriptive test: 15 included reports in 10 `report_series_id` clusters.
- Exclusions remain the recorded extraction-boundary exclusions in the rights-safe metadata. No report may be re-included or excluded based on method performance.
- A future external set must contain complete unseen series; an entire series cannot be split between development and external test.
- Source PDFs and verbatim extracted passages remain restricted and are not part of the public release.

## Frozen endpoints and estimands

- Primary metric for the historical analysis: paired ROUGE-L F1.
- Historical selection budgets: 5 and 10 extraction units.
- Revision matched-budget study: at minimum two word or tokenizer budgets fixed on development data before the external set is opened; selection must obey the budget rather than truncate after selection.
- Series-level primary estimand: equal weight per `report_series_id`; equal weight per report is a sensitivity estimand.
- Series-level uncertainty: deterministic cluster bootstrap, exact series-block sign flip when feasible, and leave-one-series-out analysis.
- Multiplicity family: all confirmatory method contrasts at both frozen budgets; Holm step-down adjustment. Exploratory analyses are reported separately and are not promoted after viewing results.

## Frozen method and tuning rules

- Historical conditions: lead, centroid, TextRank, Semantic-MMR, role, normalized no-path, full C2GES, and the unrenormalized strict historical diagnostic.
- The clean ablation changes one mechanism at a time and preserves comparable positive-weight and redundancy scales.
- All tunable methods receive the same development series and the same predetermined number of evaluated configurations. Tie-breaking is fixed before external evaluation.
- Historical semantic model identity: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU, normalized embeddings.
- The revision truncation audit records tokenizer identity, effective maximum sequence length, padding/truncation policy, token-length distribution, and the fraction truncated before interpreting Semantic-MMR results.
- Historical paired bootstrap seed: `20260808`; revision resampling seeds must be fixed in the analysis artifact before execution.

## Human and external-data gates

Structure validity and task utility require at least two independent qualified annotators, a written rubric, pre-result thresholds, raw judgments, agreement, and adjudication. No automated role, edge, or path score will be described as expert validated without those records. Maintenance work orders or other external text require a documented redistribution/analysis right and a data card before use.

## Bound inputs

```text
C924035295F837B4F94D18D06DED12EC36135628A44345F1F568F9D5582AF14C  formal_config_v0_3_1.json
709F4FBE567A3E9EAE92785D8296C20A44AD9E05D77115C957C4CA7BCADCC47D  rights_safe_report_metadata.csv
ACB61C3E7DA4CF50AFB5291100150BA36AB2E8B6771961F6D9947B8DDA091E15  exact_signflip_results.json
1ED9EFD44C0C9B4A30D7EF948CD324585FA069AD0958BD659FA0989513BC5FD3  run_test_v0_3_1.py
6EB06B4D73D5B0B4A51CB20916564CEF4A8137077B5BB5A339D30D30F8F2EFC2  v031_methods.py
77D89DBEB187A6EA89C5786584D5C1F55BCED5B88A949743F95546D39F5FC6DE  c2ges_offline.py
```

The restricted historical JSONL identities remain those frozen in `TEST_FREEZE_MANIFEST_v0_3_1.json`: development `27CE41...F79`; retained test `A9342B...127`. Ellipses here are display abbreviations; the manifest is authoritative.

## Decision rules

If normalized path deletion has no matched-budget, series-level benefit, the no-path method becomes the default and the path term remains a negative diagnostic. If matched-budget evidence does not favor C2GES, superiority wording is removed. If human validity or external utility gates are not completed, structure and engineering-aid statements remain method properties or unverified objectives, not demonstrated effects.
