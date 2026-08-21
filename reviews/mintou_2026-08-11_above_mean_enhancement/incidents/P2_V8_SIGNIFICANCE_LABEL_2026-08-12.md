# P2 v8 significance post-processing label incident — 2026-08-12

- Input: the frozen 440-row exact-hierarchy result table.
- Outcome: the first post-processing invocation stopped at its precondition check because it filtered for `OLS`, while the frozen enumeration is `OLS-Reconciled`.
- Data impact: none. No output table was created and no experiment was rerun.
- Corrective action: change only the label match and output label to `OLS-Reconciled`, retaining the same test, multiplicity families, and frozen input.
