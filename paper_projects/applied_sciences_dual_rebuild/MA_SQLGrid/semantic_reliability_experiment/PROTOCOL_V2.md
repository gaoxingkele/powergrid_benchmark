# Multi-state reliability protocol v2 — re-audit draft

This is a retrospective robustness reanalysis over already archived model
outputs. It is not a preregistered model experiment and is not a human semantic
audit.

Stage A is the standalone `stage_a_generate_states.py`. Its CLI accepts only a
base SQLite file, the frozen operator policy, an output directory, and a trace
directory. It cannot accept or locate benchmark records, gold SQL, predictions,
scores, or correctness. Sixteen states retain every v1 operator family and add
three physical insertion permutations, categorical covering, numeric/date
boundary and tie cohorts, NULL witnesses, anti-join/relationship witnesses,
topology motifs, and string decoys. State construction is determined solely by
schema, base-row domains, policy, and seed.

Stage B may read questions/gold only after the Stage-A manifest is fixed. A
gold-only pre-score audit measures state relevance and produces the complete
114-item ordering and 18-item top-k checklist. Two independently blinded agent
reviewers found zero `TOTAL_ORDER_VALID` items. Consequently all 114 declared
order-sensitive questions are frozen as adjudication holds, including the 19
items for which the local machine heuristic considered tied output rows
indistinguishable. Only the 66 order-insensitive questions are eligible for the
automatic primary suite. Held items are still executed on all states and
reported diagnostically, never treated as automatic failures. If general operators do not change all 180 gold denotations, only the
covered subset is eligible for the prespecified secondary analysis; uncovered
items remain explicit holds. No question-specific state adaptation is allowed.

The tolerant comparator uses finite pairwise `math.isclose` with absolute
tolerance `1e-6` and relative tolerance `1e-9`. Ordered results remain
sequences. Unordered results are partitioned by exact nonnumeric fields and use
deterministic bipartite matching within each group, preserving duplicates and
NULL. Strict exact numeric equality is a sensitivity analysis. Output headers
and aliases are explicitly irrelevant to the primary denotation criterion;
prediction-vs-gold and prediction-vs-metadata normalized header agreement are
retained as diagnostics because aliases do not establish column provenance.

All candidate statements must be a single read-only SELECT/CTE, use an
immutable read-only SQLite connection plus authorizer, and obey time, row, and
byte caps. Errors are distinct holds/failures and never treated as empty
results. Every prediction remains in its declared denominator.

Formal scoring is locked until an independent reviewer signs the exact v2
freeze SHA. The loading gate must verify 720 unique expected keys per backbone,
all successful statuses, row-level run hashes, physical run-manifest and ledger
hashes, and the canonical-v2 accepted-input bindings before executing any
candidate SQL.
