# MA-SQLGrid Candidate-Order and Risk--Coverage Audit Protocol

Status: frozen before executing the audit script on 2026-08-23. This is a post-review, outcome-aware diagnostic protocol. It is not a preregistered primary comparison and must not be presented as confirmatory evidence.

## Objective

Recompute candidate-order sensitivity under the same unified shape-and-denotation evaluator used for the reconciled historical-pool results. The audit replaces the manuscript's non-comparable historical row-only sensitivity values and does not make model calls or generate new SQL.

## Frozen population and inputs

- Population: the same 180 GridDB question identifiers in the historical-pool study.
- Candidate pool: eight frozen slots per question: Qwen F00/F01/F10/F11 followed by Granite F00/F01/F10/F11.
- Evidence: the sealed pre-gold blackboards. Gold-relative outcomes are used only after selection to score the selected slot.
- Evaluator: `MA-SQLGrid-GridDB-T0-shape-denotation-v1`, including the expected-column-count gate and denotation comparison specified in `MA_SQLGRID_EVALUATOR_PROTOCOL_2026-08-23.md`.
- No SQL text is emitted by the audit outputs.

Input SHA-256 values:

- `blackboards_sealed_before_gold.jsonl`: `2B447A63D47D225E15148E0A75C660DDAFC83E5C50AAA2DDC207D252B9FB6777`
- `canonical_rows_v2.jsonl`: `A290770448219ECB81B01DB61E3A789C4101F5CC38BF342BD34E2931FC7E10F9`
- `unified_evaluator_results.json`: `A863EDC1620FE252A816666C6C4B64516AC3272CC1DA6ADB8F6E7DF2A6877B85`
- frozen adjudicator implementation: `EA8105FC3AB6F8F54B59E74B0AD9AC96D5CD1ABB073469C51E9DB5A7066915BE`

## Frozen selection reconstruction

For each question and each selector, retain only eligible candidates and rank them lexicographically by:

1. validation points;
2. counterfactual pass rate scaled by 1,000,000, or -1 when no counterfactual evidence is used;
3. evaluated counterfactual-state count.

Candidate order is used only to resolve equality on all three fields. The reconstruction must reproduce the recorded original-order choices for all 180 questions before sensitivity results are accepted.

## Order perturbation

Enumerate all `8! = 40,320` global permutations of the eight frozen slot positions. Apply each global order to every question and use it only as the final tie breaker. Report, separately for validation-only and complete-witness selection:

- the exact distribution of unified-evaluator correct counts;
- minimum, median, mean, and maximum correct counts;
- the original-order count and reverse-order count;
- the number and size distribution of top-score ties.

No permutation is selected as a preferred policy after observing its result.

## Descriptive risk--coverage audit

For thresholds `k = 1,...,8`, cover a question only when its top-score tie set contains at most `k` candidates. When covered, use the original frozen order as the tie breaker. Report coverage, covered-set accuracy, and total correct yield. The `k=1` row is the strict no-tie abstention rule. This curve is descriptive and cannot establish calibration on an unseen population.

## Acceptance checks

- 180 unique questions and 1,440 fixed-slot unified outcomes are present.
- Original-order choices match both sealed decisions for all 180 questions.
- Unified original-order counts reproduce 99/180 for validation-only and 100/180 for complete-witness selection.
- C000 reproduces 76/180.
- Exactly 40,320 permutations are counted for each selector.
- Output tables contain identifiers, scores, tie information, and Boolean correctness only; they contain no question or SQL text.

## Transparent post-run extension

After the exact slot-order audit had been run, the audit script was extended to hash the eight SQL strings per question using the unified evaluator's comment/fence normalization. This extension reports the number of unique normalized SQL strings, duplicate slots within top-score sets, and a descriptive right-step area under the tie-size risk--coverage curve. It emits hashes/counts rather than SQL text. These quantities were not part of the initially frozen protocol and are therefore explicitly outcome-aware diagnostics; they do not define a deduplicated production selector or a calibrated abstention threshold.
