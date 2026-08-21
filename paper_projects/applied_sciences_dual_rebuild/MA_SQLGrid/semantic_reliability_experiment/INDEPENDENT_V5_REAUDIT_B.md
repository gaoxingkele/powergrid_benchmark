# MA-SQLGrid semantic reliability v5 — independent re-audit B

## Decision

**PASS_AUTHORIZE_FORMAL_SCORE** for exact content SHA
`eb29201bd078e6903bea158d0dba6a974c0e1647dbf3e43972b38499b52a0818`.

The 22,556-byte freeze file has exact physical SHA-256
`cccd903bd7f3309f50fae4a5d7084b1f272b094ef0afd42467287a51b376e898`.
All ten policy gates pass. No formal multistate scoring was run and no formal
multistate outcome was accessed.

## Gate results

| Policy gate | Result | Evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | 35/35 frozen files plus immutable, canonical-v2, review, ledger and manifest bindings match live SHA/bytes. |
| `G2_STAGE_A_BLINDNESS` | PASS | Gold coverage accessed no prediction/score input; blindness test passes. |
| `G3_STATE_REPRODUCIBILITY` | PASS | Exact 18 = 15 + 3 partition; 18/18 state and trace hashes reproduce. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | All states pass integrity/FK checks; 3,240 gold runs have zero errors; T0 independently reruns 180 gold queries. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Changed-denotation union is 180/180 with zero uncovered questions. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Bound A/B/adjudication chain holds all 114 order-sensitive questions and leaves 66 primary questions. |
| `G7_COMPARISON_CONTRACT` | PASS | Scalar `REPLACE(...)` is allowed; `REPLACE INTO`, including after `WITH`, is rejected; SQLite authorizer remains read-only; T0 labels match 1440/1440. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | PASS | 0-SQL authorization preflight passes with no output; T0-only preflight performs exactly 1620 queries with zero canonical mismatch and no output; invalid-gate test remains fail-closed. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | 25,920/7,920/16,416/528/912 chain, missing-row rejection, 15-state AND, 3-state exclusion, 70 clusters and nine-test Holm are frozen and tested. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen builder/verifier enforce artifact hashes, denominators, nine-test family and CSV-to-TeX/SVG/summary lineage. |

## Executed verification

- Freeze verifier: exact v5 content SHA **PASS**.
- Zero-SQL preflight: `ledgers=1440 states=18 order=114 sql_executions=0
  output_written=0`.
- T0 canonical preflight: `gold=180 ledgers=1440 sql_executions=1620
  canonical_mismatches=0 output_written=0`.
- Test discovery: **22 tests, 21 passed, 1 skipped, 0 failed**. The skip is
  intentional and sound: the immutable v4 parent binds its old runner while the
  live runner is versioned v5; the equivalent v5 0-SQL path was executed
  directly and passed.
- `formal_v5_results` was absent before and after verification.

Formal scoring remains conditional on a launch companion binding this exact
audit JSON path, SHA-256 and byte count to the exact v5 freeze content SHA.

