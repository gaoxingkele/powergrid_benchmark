# MA-SQLGrid Automated Error-Taxonomy Protocol

Status: frozen before execution on 2026-08-23. This post-review audit uses the already frozen unified evaluator. It is an automated failure decomposition, not expert semantic adjudication.

## Inputs and evaluator

- Same 180 GridDB questions, T0 snapshot, eight fixed candidates, sealed selector choices, and evaluator `MA-SQLGrid-GridDB-T0-shape-denotation-v1` as the evaluator reconciliation.
- Unified evaluator implementation SHA-256: `7AAF718BECDA86D4CE3C0CECFBD5C81A910A3CE81668C11C0BD382B9303E29E8`.
- Questions, predictions, database, and selection-ledger hashes are those bound in `MA_SQLGRID_EVALUATOR_PROTOCOL_2026-08-23.md`.
- No model calls, retries, selector changes, or new SQL generation.

## Mutually exclusive automated categories

The first applicable evaluator state defines the error category:

1. `candidate_execution_error`;
2. `gold_execution_error`;
3. `candidate_shape_mismatch`;
4. `gold_shape_mismatch`;
5. `wrong_denotation` after successful execution and both shape gates;
6. `correct`.

This taxonomy cannot determine business-semantic causes such as wrong status meaning, units, time boundaries, topology intent, or professional usefulness. Those require independent qualified review and remain an external research gate.

## Outputs

- method-by-error counts for all eight fixed sources, C000, and both selectors;
- selected-item rows containing question ID, method, slot, automatic error type, nonverbatim result-shape counts, difficulty, order flag, table/tag labels, and SQL hashes only;
- failure cross-tabs by difficulty, order sensitivity, table, and SQL feature tag;
- an explicitly labelled non-expert report.

Question text, SQL text, gold SQL, values, and returned cells must not be written to the output.

## Acceptance checks

- exactly 1,620 bounded executions and 1,980 selected-item method rows (11 methods x 180);
- method correct counts exactly reproduce the unified reconciliation;
- C000 and Qwen F00 item verdicts are identical;
- every row has exactly one automated category;
- no verbatim question or SQL field exists in the output schema.
