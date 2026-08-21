# MA-SQLGrid Independent V5 Pre-Score Re-Audit A

## Decision

**PASS_AUTHORIZE_FORMAL_SCORE**

Audited exact freeze: content SHA-256 `eb29201bd078e6903bea158d0dba6a974c0e1647dbf3e43972b38499b52a0818`; file SHA-256 `cccd903bd7f3309f50fae4a5d7084b1f272b094ef0afd42467287a51b376e898`; 22,556 bytes. This was read-only pre-score work: no formal scoring, no formal outcomes, and no frozen-file modification.

## Direct execution evidence

- All 35 frozen artifacts match SHA-256 and byte count.
- Valid synthetic authorization/companion `--preflight-only`: `authorization=1 canonical=1 ledgers=1440 states=18 order=114 sql_executions=0 output_written=0`.
- Real T0 canonical snapshot preflight: `ledgers=1440 gold=180 sql_executions=1620 canonical_mismatches=0 output_written=0`; no other state was opened.
- SQL safety tests confirm scalar `REPLACE()` is accepted, while `REPLACE INTO` and a CTE followed by `REPLACE INTO` are rejected.
- Test discovery reports 22 passed and one skip. The skip is only the immutable v4-parent runner test; it does not hide v5 behavior because the equivalent v5 zero-SQL path was run directly and the v5 T0 preflight test passed.
- All v4 identity, blindness, reproducibility, database, coverage, order, comparator, fail-closed, denominator/statistics, and release gates continue to pass.

## Ten gates

| Gate | Status | Key evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | Live prediction bindings provide 1,440 unique keys; canonical identity and all 35 frozen physical identities pass. |
| `G2_STAGE_A_BLINDNESS` | PASS | Stage-A remains benchmark/prediction blind and reads its base database read-only. |
| `G3_STATE_REPRODUCIBILITY` | PASS | 18 states partition 15+3; 18/18 state and trace hashes reproduce; live preflight checks all 18. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | 18/18 DB checks and 3,240 pre-score gold executions pass; actual T0 preflight executes 180 gold plus 1,440 prediction queries with zero mismatch. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Coverage remains 180/180 and snapshot-empty witnesses remain covered; real T0 canonical equivalence passes. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Both reviews, checklist, and adjudication are bound; all 114 order-sensitive items remain held and 66 are primary. |
| `G7_COMPARISON_CONTRACT` | PASS | Comparator tests pass; scalar `REPLACE()` is allowed without reopening `REPLACE INTO` or CTE-write paths. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | PASS | Both valid preflights traverse live checks and write no output; invalid authorization and write SQL fail closed. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | Frozen chain remains 25,920; 7,920/16,416; 1,440; 528/912; 15/3; seed 20260805; 100,000/20,000 resamples; Holm family 9. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen analysis, builder, and verifier retain hashed atomic-to-table/figure lineage and the synthetic release chain passes. |

The machine-readable authority is `INDEPENDENT_V5_REAUDIT_A.json`. A separate post-audit companion must bind that finalized file before formal Stage-B scoring.
