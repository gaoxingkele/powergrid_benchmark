# C2GES Applied Sciences Narrative Revision

> **Historical record (2026-08-12).** Superseded for release status and current page/reference counts by `PLAN_COMPLETION_AUDIT_2026-08-24.md`, `REFERENCE_EXISTENCE_AUDIT_2026-08-24.md`, and `VISUAL_QA_REPORT.md`. Retained only for change provenance.

Date: 2026-08-12
Base manuscript SHA-256: 971303C53078D370C7084AB20AFF3F25D01E3AA0459E9C67F39C1C3989C61DBC

## Scientific Position

The revised manuscript presents C2GES as a structure-aware, source-linked extractive framework for long power-system technical reports. It does not describe the textual graph as a physical causal model or the node-deletion term as an event-level counterfactual. The selected NERC reports remain a maintenance-oriented proxy rather than operational maintenance records.

## Main Changes

1. Replaced the original over-broad title with a typed-path, technical-report title.
2. Rewrote the article around a method--comparison--component-diagnosis narrative.
3. Defined RQ1 as the fixed-sentence system comparison plus output-length diagnostic; RQ2 as the strict path-deletion endpoint ablation; and exploratory RQ3 as component activity plus development-only coefficient support.
4. Brought the method text into agreement with the bound implementation, including channel scaling, stage mapping, ordered role-group reservation, tie handling, greedy filling, and the unrenormalized strict variant.
5. Moved implementation check details and exact sign-flip values into an independent Supplementary Materials PDF.
6. Replaced the evidence-ladder figure with a data-driven component-diagnostic figure.
7. Redrew Figure 1 to show role-group reservation explicitly and retained vector PDF/SVG outputs.

## Results Retained Without Change

- Full C2GES ROUGE-L: 0.1060 at K=5 and 0.1276 at K=10.
- Strict variant ROUGE-L: 0.1094 at K=5 and 0.1310 at K=10.
- Full minus strict variant: -0.003332 and -0.003360; composition intervals cross zero.
- Full outputs are 54--63% longer than Semantic-MMR/TextRank at equal sentence counts.
- Path-deletion activity: 9774/19,008 score comparisons changed and 28/30 report--budget selections changed.
- Development-only calibration: zero path weight selected in 12/12 leave-one-report-out folds.

No new test-set experiment was run and no experimental result was tuned or overwritten.

## Verification

- Main PDF: 20 pages, 6 figures, 7 tables, 35 references, approximately 198 abstract words.
- Supplement PDF: 2 pages, Tables S1--S4.
- Code regression: 17 standard-library unittest cases passed.
- Main LaTeX: no undefined references or missing figures.
- Visual inspection completed for the title/abstract page, algorithm figure, main comparison, component diagnostic, and conclusion/declarations.

The old fig06_evidence_ladder files are retained only as superseded historical assets and are not referenced by the revised manuscript.
