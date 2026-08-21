# v5 pre-score repair report

Status: `READY_AWAITING_V5_REAUDIT`.

The preserved v4 incident records six T0 mismatches, all Q075, caused by
misclassifying scalar `REPLACE()` as write SQL. No v4 output directory or formal
result was written. v5 separates scalar-function syntax from `REPLACE INTO` and
freezes both positive and negative safety regression tests.

The required evidence is a 1,620-query T0-only preflight with zero canonical
mismatches and zero output writes, plus the retained zero-SQL preflight. No
multi-state result is created or inspected during this repair.

