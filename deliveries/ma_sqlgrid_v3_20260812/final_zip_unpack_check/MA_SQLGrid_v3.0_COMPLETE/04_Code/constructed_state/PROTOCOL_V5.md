# Multi-state reliability protocol v5 — canonical snapshot gate

v5 preserves the v4 design and complete freeze-key preflight. It corrects one
lexical safety defect: SQLite scalar `REPLACE(value, old, new)` is legal inside
a read-only SELECT and is now allowed, while `REPLACE INTO` is rejected wherever
it appears, including after a WITH prefix.

Before v5 can receive independent authorization, two preflights are mandatory:

1. the existing zero-SQL path through authorization, canonical identity,
   1,440 ledger records, 18 state identities, and 114 order records;
2. a canonical-snapshot-only path executing exactly 180 gold plus 1,440
   prediction queries on T0 (1,620 total), requiring zero disagreement with the
   frozen canonical-v2 labels and writing no scoring output.

The T0 preflight never opens any of the other 17 states. Its report contains
only counts, exact freeze identity and pass/fail status, not candidate SQL or
multi-state outcomes. A v5 re-audit must independently reproduce this gate
before issuing `PASS_AUTHORIZE_FORMAL_SCORE`.

