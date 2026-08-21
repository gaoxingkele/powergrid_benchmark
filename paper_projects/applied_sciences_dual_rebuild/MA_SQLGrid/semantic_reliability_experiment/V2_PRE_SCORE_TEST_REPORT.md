# v2 pre-score test report

No prediction ledger, score file, collision diagnostic, or candidate execution
ledger was read to produce this report.

## Stage-A reproducibility

The query-blind generator was run in two new directories. All 18 state SQLite
SHA-256 hashes and all 18 operator-trace SHA-256 hashes matched exactly. Every
state returned `integrity_check=ok` and zero foreign-key violations. The runtime
is Python SQLite 3.49.1 with the complete compile-option list stored in each
manifest.

## Gold-only coverage

The post-freeze, pre-score audit executed 180 gold queries on all 18 states
(3,240 executions) without error. The changed-denotation union is 180/180.
Each of the five snapshot-empty queries becomes nonempty in at least two frozen
states. This demonstrates state relevance, not natural-language correctness.

The machine checklist contains exactly 114 declared order-sensitive items and
18 top-k items. Although its heuristic labels 19 as tie-output-equivalent, two
blind agent reviewers independently found zero `TOTAL_ORDER_VALID` items.
Their stricter consensus controls the freeze: all 114 are order holds and only
the 66 order-insensitive questions enter the automatic primary suite.

## Unit tests

`python -m unittest discover -s tests -v` passed 11/11 tests, including:

- Stage-A CLI/path blindness;
- byte-identical double generation and database validity;
- all coverage and checklist denominators;
- both blind order reviews and their zero-total-order consensus;
- finite pairwise `isclose` boundary behavior;
- duplicate-preserving bipartite multiset matching;
- ordered sequence, NULL, SQLite numeric affinity, and wrong-header diagnostics;
- the retained v1 freeze/safety checks.

Formal Stage B remains locked until an independent v2 re-audit signs the exact
freeze SHA.
