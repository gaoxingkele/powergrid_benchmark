# MA-SQLGrid Independent V3 Pre-Score Re-Audit

## Decision

**PASS_AUTHORIZE_FORMAL_SCORE**

This is a pre-score-only authorization for freeze content SHA-256 `92e62f6983527c02117352f273eb7510de887836bdd0a35b9519cbd00cd3f3bc` and freeze file SHA-256 `aa88e6bc7370edb5a100f674a22e933445666e4a851dceb87c4fff63862887c7`. I did not run Stage-B, inspect formal outcomes, or modify any frozen v3 file.

All 10 launch-policy gates pass. All five v2 block classes are closed. A separate post-audit launch companion must still bind this finalized JSON file's name, SHA-256, byte count, and the exact freeze content SHA before Stage-B can run.

## Independent checks performed

- Recomputed the embedded freeze content hash and verified all 21 frozen artifacts by SHA-256 and byte count.
- Ran the frozen pre-score verifier: PASS for the exact requested content hash.
- Ran full test discovery: 16/16 tests passed.
- Rechecked two 720-key ledgers, frozen row-level identities, canonical-v2 live identity contract, and pre-output T0 consistency enforcement.
- Rechecked 18 states as exactly 15 semantic-suite states plus 3 physical-order diagnostics, including 18/18 state and trace reproducibility pairs.
- Rechecked 18 SQLite databases, 3,240 gold executions, zero execution errors, 180/180 changed-denotation coverage, and the five snapshot-empty questions' nonempty witnesses.
- Rechecked both 114-item order reviews and the freeze-bound adjudication: 114 held, 66 automatically eligible.
- Recomputed the cluster-map content hash: 180 questions in 70 frozen clusters.
- Independently generated a complete synthetic 25,920-row atomic matrix and exercised aggregation, analysis, release-manifest construction, and release verification in a temporary directory. The observed invariants were 7,920 primary semantic-state rows, 16,416 held diagnostic rows, 1,440 predictions, 528 primary predictions, 912 held predictions, and a 9-test Holm family. A physical-state failure did not enter the primary AND; a semantic-state failure did; a missing atomic row failed closed.

## Required gates

| Gate ID | Status | Decisive evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | Each ledger has 720/720 unique expected keys; row and run identities bind to canonical-v2; live canonical freeze and rows are pinned by SHA-256 and bytes. |
| `G2_STAGE_A_BLINDNESS` | PASS | Stage-A accepts only base DB, policy, output, and trace paths; it imports no scorer/comparator and receives no benchmark or ledger input. |
| `G3_STATE_REPRODUCIBILITY` | PASS | Two clean generations have 18/18 matching state hashes and 18/18 matching trace hashes under SQLite 3.49.1 with exact compile options. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | Integrity and foreign-key checks pass for 18/18 databases; 3,240/3,240 gold executions succeed with unique keys. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Changed-denotation union is 180/180; Q073, Q104, Q107, Q110, and Q140 each become nonempty in at least two states. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Both reviewers cover 114 items; exact reviewer and adjudication hashes are frozen; all 114 remain held and 66 are eligible. |
| `G7_COMPARISON_CONTRACT` | PASS | Frozen comparator implements tested finite pairwise tolerance, duplicate-preserving bipartite matching, ordered comparison, NULL distinction, and diagnostic-only headers; 16/16 tests pass. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | PASS | Stage-B requires exact schema/decision/freeze, all ten gates, a post-audit identity companion, live canonical identities, and 1,440 T0 mappings before creating output. The non-authorizing template creates no circular dependency. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | Frozen analysis enforces 25,920; 7,920/16,416; 1,440; 528/912; semantic-only 15-state AND; 70 clusters; seed base 20260805; 100,000 sign flips; 20,000 bootstraps; one 9-test Holm family. Independent synthetic tests passed. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen analysis, release builder, and verifier hash atomic, suite, statistical, table, figure, summary, and freeze lineage. The independent synthetic release chain passed. |

## Closure of the five v2 blocks

1. The protocol contradiction is closed: v3 consistently states 18 total states, partitioned 15 plus 3.
2. The order adjudication is now an exact frozen artifact alongside both reviews.
3. Stage-B now accepts only `PASS_AUTHORIZE_FORMAL_SCORE` under the required audit schema and ten-gate contract.
4. Stage-B verifies the physical identity of live canonical-v2 freeze and row files before scoring/output.
5. Aggregation, clustered inference, denominators, release lineage, and a release verifier are frozen and independently exercised.

The audit machine-readable authority is `INDEPENDENT_V3_REAUDIT.json`. No formal result is asserted here.
