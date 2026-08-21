# Independent pre-score re-audit of semantic-reliability freeze v2

## Decision

**BLOCK. Formal Stage-B scoring is not authorized.**

This decision is bound to freeze content SHA-256
`7ea872fe554f72547664d3c160577bc26501d8e2e09aab298d354a57966f5052`
(freeze file SHA-256
`8f47cc5d91c952f94c9b752107cde1b22444f999ff298a7704d6a2c8d5f020a4`).
No Stage-B formal scoring was run, no formal outcome was opened, and no frozen
v2 code, state, trace, manifest, protocol, review, or coverage artifact was
modified.

The experiment is close to score-ready: state construction, coverage,
comparison semantics, and the archived ledger identities all pass independent
checks. Authorization is blocked by exact-freeze and downstream fail-closed
defects, not by the 18 state databases themselves.

## Evidence that passes

### Freeze and Stage A

- The freeze content hash recomputes exactly, and all 17 entries in
  `frozen_files` match SHA-256 and byte count.
- Static inspection confirms that Stage A accepts only `--base-db`, `--policy`,
  `--out`, and `--trace-dir`. It imports no scorer/comparator, contains no
  benchmark/ledger path, and the operator policy contains no question ID.
- Both clean generations contain 18 states. All 18 state hashes and all 18
  trace hashes match pairwise. Both manifest content hashes recompute.
- All 18 databases return `integrity_check=ok`, zero foreign-key violations,
  and row counts equal their manifests. Runtime SQLite 3.49.1 and the complete
  compile-option sequence match the frozen manifest.

### Independent gold-only re-execution

I independently re-executed 180 gold SQL statements against all 18 read-only
states: 3240/3240 executed without error. The changed-denotation union is
180/180. The five snapshot-empty questions became nonempty in the following
numbers of non-snapshot states:

| Question | Nonempty states |
|---|---:|
| Q073 | 2 |
| Q104 | 6 |
| Q107 | 6 |
| Q110 | 5 |
| Q140 | 2 |

The frozen coverage CSV also contains exactly 3240 unique state-question rows
and zero gold errors.

### Ordering evidence and comparator

Both technical reviewers cover all 114 declared order-sensitive items and all
18 top-k items. Each reports zero `TOTAL_ORDER_VALID`; the present adjudication
therefore holds all 114 and leaves 66 order-insensitive questions eligible.
The safe runtime policy is also hard-coded in Stage B: every metadata-declared
order-sensitive item is held.

The frozen comparator and 11/11 pre-score unit tests pass. An independent
exhaustive check over 47,989 small multiset pairs agreed with a permutation
oracle. Pairwise finite `isclose`, duplicate-preserving bipartite matching,
ordered sequences, NULL, numeric affinity, and header diagnostics behave as
declared. Headers are explicitly diagnostic rather than primary; that choice
is a claim boundary, not an undisclosed implementation accident.

### Prediction loading evidence

Without executing candidate SQL, both ledgers pass:

- 720 rows and 720 unique expected question-condition keys per backbone;
- zero duplicate, missing, or unexpected keys and 720 successful statuses;
- row-level data/code/configuration hashes are singleton sets equal to the run
  manifests;
- prediction and manifest physical hashes equal canonical-v2 accepted inputs.

The existing v1 design-audit gate has decision `NO_GO_CLAIM_PROMOTING` and no
matching v2 freeze SHA, so it does not satisfy the current Stage-B audit
condition.

## Blocking findings

### B1. Frozen protocol contradicts the frozen state denominator

`PROTOCOL_V2.md` says “Sixteen states” and then describes three insertion
permutations. The policy, both manifests, and freeze actually contain **18
total states: 15 semantic-suite states plus 3 physical-order diagnostic
states**. Because this protocol is itself frozen, the inconsistency can
mislead readers about the suite denominator and cannot be repaired by an
unfrozen note.

### B2. Adjudication is not bound to the exact freeze

The two reviewer JSON hashes are bound by the freeze. The current adjudication
(`afa677f152136e9fb8a9d3ce9f8bd63b1b08a2f27abcb402a72dc21c0f3909b7`)
correctly records 114 holds and 66 eligible items, but its hash and bytes are
absent from the freeze. The freeze therefore cannot use that mutable external
file as exact-SHA adjudication evidence.

### B3. Re-audit authorization token and Stage-B gate disagree

The required decision vocabulary is `PASS_AUTHORIZE_FORMAL_SCORE` or `BLOCK`.
Frozen `stage_b_score_v2.py` accepts only the literal `audit.decision ==
"PASS"`. Consequently a conforming positive re-audit would be rejected, while
an underspecified two-field JSON using another decision vocabulary could pass.
The gate also does not require the re-audit schema or an all-gates-pass field.

### B4. Stage B does not pin the canonical-v2 freeze file before trusting it

The current canonical-v2 file matches the binding, and the current ledgers
pass. However, Stage B loads `FREEZE_AND_METHOD.json` and immediately trusts
its `accepted_inputs` without asserting the file's SHA-256 and byte count
against `canonical_v2_binding`. A later change to that file could silently
change which ledger artifacts the exact v2 freeze accepts.

### B5. Statistics, denominators, and release verification are not executable frozen specifications

The prose declares the finite 66-question estimand, 114 holds, 15 semantic
states, three diagnostic permutations, paired 2x2 contrasts, clustering, and
one Holm family. No frozen aggregation/statistics program or release verifier
enforces them. In particular, the required invariants are:

- 25,920 atomic rows (`2 backbones x 4 cells x 180 questions x 18 states`);
- 7,920 pre-AND primary-eligible semantic rows
  (`2 x 4 x 66 x 15`), excluding all three T1 states;
- 16,416 order-hold diagnostic rows (`2 x 4 x 114 x 18`);
- every prediction/execution error retained in its declared denominator;
- logical AND across exactly the 15 semantic states;
- a hashed cluster map, exact resampling seed/count, contrast family, Holm
  implementation, and composition-sensitivity labels;
- independent traceability from atomic rows through statistics to paper
  tables and figures.

Stage B currently writes atomic rows only and labels eligibility by question;
it does not mark the frozen semantic-state partition or implement the above
aggregation and release audit.

## Minimum verified repair set

All repairs change frozen evidence or code and therefore require a new freeze
SHA and another independent pre-score re-audit:

1. Correct the protocol to “18 total = 15 semantic + 3 physical-order
   diagnostic states.”
2. Bind `semantic_order_review/adjudication.json` by SHA-256 and bytes, and test
   its 114-held/66-eligible result.
3. Make Stage B accept only `PASS_AUTHORIZE_FORMAL_SCORE` for the exact freeze
   SHA; require the re-audit schema and all applicable gates to pass.
4. Verify the physical canonical-v2 freeze hash and bytes before using
   `accepted_inputs`.
5. Freeze an atomic-to-suite/statistics implementation with the exact
   denominators, state partition, cluster map, resampling parameters, and Holm
   family above.
6. Freeze a release manifest builder and independent verifier covering atomic
   rows, suite aggregation, statistics, tables, figures, and provenance.

Until those six changes are refrozen and re-audited, no formal score should be
generated from freeze SHA
`7ea872fe554f72547664d3c160577bc26501d8e2e09aab298d354a57966f5052`.
