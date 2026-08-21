# MA-SQLGrid Independent V4 Pre-Score Re-Audit A

## Decision

**PASS_AUTHORIZE_FORMAL_SCORE**

Exact freeze audited: content SHA-256 `0d817c6597f3b6528d7c8a24da96a5f1685fabd65e00f75def8d24de1ac1e791`; file SHA-256 `73cacffbf2bb647c0dc1d1c4e67dbadc08ce01ba7124b418a54cf432552b0064`; 19,639 bytes.

This audit was pre-score only. I did not execute formal scoring, inspect formal outcomes, or modify frozen v4 files.

## Decisive results

- Independently verified all 28 frozen artifacts by SHA-256 and byte count.
- Verified both prediction ledgers and manifests against the new `prediction_bindings`; all four live files match their frozen SHA-256 and sizes.
- Verified the freeze-bound pre-score coverage and order-checklist evidence.
- Ran the valid synthetic audit plus companion through the actual Stage-B `--preflight-only` path. It returned: `authorization=1 canonical=1 ledgers=1440 states=18 order=114 sql_executions=0 output_written=0`.
- Ran the invalid authorization test. It failed with nonzero status and created no output directory.
- Ran full test discovery: 19/19 passed.
- Reconfirmed the frozen denominator chain: 25,920 atomic rows; 7,920 primary semantic-state rows; 16,416 held diagnostic rows; 1,440 suite rows; 528 primary and 912 held predictions; 15 semantic states in the primary AND and 3 physical states excluded.
- The frozen synthetic analysis/release exercise passes through aggregation, the 9-test Holm family, manifest construction, source-hash lineage, and release verification.

## Ten required gates

| Gate | Status | Evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | Frozen `prediction_bindings` exist; Qwen and Granite manifests/predictions match live SHA-256 and bytes; preflight loads 1,440 ledger rows. |
| `G2_STAGE_A_BLINDNESS` | PASS | Stage-A remains prediction/benchmark blind and read-only with respect to the base database; blindness tests pass. |
| `G3_STATE_REPRODUCIBILITY` | PASS | Exact 15+3 partition; 18/18 state and trace pairs reproduce; preflight validates all 18 live states. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | Pre-score evidence is frozen; 3,240 gold executions have zero errors; all 18 databases pass integrity and foreign-key checks. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Changed-denotation union is 180/180; all snapshot-empty cases obtain nonempty witnesses in at least two states. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Checklist, two reviews, and adjudication are bound; all 114 order-sensitive items remain held; 66 are primary eligible. |
| `G7_COMPARISON_CONTRACT` | PASS | Tolerance, duplicate-preserving matching, order, NULL, affinity, and header behavior are covered; 19/19 tests pass. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | PASS | Actual valid preflight traverses authorization, canonical, ledger, state, and order checks with zero SQL and zero output; invalid authorization fails closed with no output. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | Exact denominators, 15/3 separation, seed 20260805, 100,000 sign flips, 20,000 bootstraps, and one 9-test Holm family are frozen and tested. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen analysis, release builder, and verifier bind atomic, suite, statistics, table, figure, summary, and freeze lineage; synthetic release verification passes. |

The machine-readable authority is `INDEPENDENT_V4_REAUDIT_A.json`. Formal Stage-B remains locked until a separate companion binds the finalized JSON name, SHA-256, byte count, and exact v4 freeze content hash.
