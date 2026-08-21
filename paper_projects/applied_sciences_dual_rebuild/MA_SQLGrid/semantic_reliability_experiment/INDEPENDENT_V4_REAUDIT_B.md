# MA-SQLGrid semantic reliability v4 — independent re-audit B

## Decision

**PASS_AUTHORIZE_FORMAL_SCORE** for exact freeze content SHA
`0d817c6597f3b6528d7c8a24da96a5f1685fabd65e00f75def8d24de1ac1e791`.

The audited freeze file is exactly 19,639 bytes with physical SHA-256
`73cacffbf2bb647c0dc1d1c4e67dbadc08ce01ba7124b418a54cf432552b0064`.
Its canonical content hash recomputes exactly. All ten required launch-policy
gates pass. This audit did not run formal Stage-B, access formal outcomes, or
modify the freeze/code.

## Ten-gate result

| Gate | Result | Core evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | 28/28 frozen files, 2/2 immutable inputs, 2/2 canonical bindings, 13/13 canonical accepted inputs, and 2/2 prediction bindings match SHA/bytes; both ledgers are 720/720 unique successes. |
| `G2_STAGE_A_BLINDNESS` | PASS | Gold coverage records no prediction/score access; the Stage-A blindness test passes. |
| `G3_STATE_REPRODUCIBILITY` | PASS | Exact 18 = 15 + 3 partition; 18/18 state and trace hashes match both generations. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | 18/18 integrity checks, zero FK violations, and 3,240 gold executions with zero errors. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Changed-denotation union 180/180, zero uncovered questions, snapshot-empty coverage condition satisfied. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Reviews A/B each cover 114 and admit zero ordered items; bound adjudication holds 114 and leaves 66 primary questions. |
| `G7_COMPARISON_CONTRACT` | PASS | Frozen comparator and read-only execution contract pass numeric, multiset, order, NULL, header, lexical, and SQLite-authorizer tests. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | PASS | v4 contains prediction/pre-score keys and verifies frozen files, immutable inputs, policy, manifest, canonical-v2, review chain and ledgers. Valid synthetic audit+companion reaches the SQL boundary with 0 SQL/0 output; one BLOCK gate is rejected with no output. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | 25,920 atomic, 7,920 primary-state, 16,416 held-state, 528 primary-prediction and 912 hold-prediction contracts pass, including missing-row fail-closed, 15-state AND, 3-state exclusion, 70 clusters and nine-test Holm. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen release builder/verifier rehash artifacts, enforce denominators/family size, and trace CSV to TeX/SVG and analysis lineage. |

## Executed checks

- Test suite: **19/19 PASS**.
- Freeze verifier: **PASS** for the exact v4 content SHA.
- Valid synthetic audit+companion `--preflight-only`:
  `authorization=1 canonical=1 ledgers=1440 states=18 order=114
  sql_executions=0 output_written=0`.
- Invalid audit with a correctly bound companion and one `BLOCK` gate:
  rejected with return code 1, explicit all-gates rejection, no output directory,
  and zero SQL executions.
- `formal_v4_results` was absent before and after verification.

Formal scoring is authorized only after a launch companion binds the exact
path, SHA-256 and byte count of this audit JSON together with the exact v4
freeze content SHA.

