# MA-SQLGrid v5 Post-Score Independent Audit B

**Decision: `PASS_INTEGRATION`**

Auditor: `/root/ma_v5_postscore_audit_b`  
Completed: 2026-08-05T14:55:55.8825302Z  
Scope: read-only audit of the v5 formal result and release chain. I did not read or rely on the other new post-score auditor's conclusion, and I did not modify the result, manuscript, or core scripts.

## Bottom line

The formal v5 output is internally complete, reproduces the frozen canonical snapshot, respects the 66-question primary / 114-question diagnostic-hold boundary, and is correctly bound into the release manifest. I found no integration-blocking defect. Integration remains limited to the frozen claim: a retrospective automated multi-state gold-SQL agreement stress test, not a human semantic audit.

## Independent checks

| Check | Independent evidence | Result |
|---|---:|---|
| Freeze identity | File SHA-256 `cccd903b...6e898`; canonical content SHA-256 recomputed as `eb29201b...a0818`; 35/35 frozen files matched hash and size | PASS |
| Launch binding | Freeze file/content plus both pre-score re-audit identities matched the launch companion | PASS |
| Atomic coverage | 25,920 rows and 25,920 unique `(backbone, condition, question, state)` keys | PASS |
| Factorial balance | 2 backbones × 4 conditions × 180 questions × 18 states; 1,440 rows/state, 144 rows/question | PASS |
| SQL outcomes | 29,160 independent read-only executions; six stored outcome fields compared on every atomic row; zero mismatches | PASS |
| SQL safety | Zero mutating prediction SQL and zero safety rejections; all gold SQL succeeded | PASS |
| Error accounting | 24,426 prediction successes and 1,494 ordinary SQLite execution errors; errors remain failed observations rather than being excluded | PASS |
| Adjudication boundary | 66 order-insensitive primary questions and all 114 order-sensitive questions held; zero row-level boundary mismatches | PASS |
| Frozen denominators | 7,920 primary semantic-state rows; 16,416 hold diagnostic rows; 528 primary and 912 held prediction groups | PASS |
| Canonical snapshot | 1,440/1,440 T0 outcomes matched canonical v2 | PASS |
| Suite aggregation | Independently rebuilt all 1,440 suite records; zero record mismatches; CSV and JSONL agree after type normalization | PASS |
| Statistical release | Replayed 9 estimates, 9 × 100,000 cluster sign-flips, 9 × 20,000 cluster bootstraps, and Holm-9; maximum numerical difference was 0 | PASS |
| Manifest | 9/9 artifact hashes and sizes matched; `RELEASE_V3_VERIFY PASS` | PASS |
| SVG/TeX | Both carry the correct contrast-CSV source hash; SVG parsed as 900×420 XML and rendered successfully in headless Edge; title plus all nine lines were legible and unclipped | PASS |

## Error and denominator interpretation

The 1,494 prediction execution errors are ordinary read-only SQLite failures, not unsafe write attempts. They are represented as failed predictions in the atomic and suite outcomes. Among primary-eligible atomic rows, the `execution_error_hold` label is only an error-class label: eligibility remains tied to the frozen question boundary, and the failed outcome remains in the primary denominator. I verified this behavior row by row.

The released contrasts use the 66-question finite primary corpus, which maps to 12 clusters within the frozen 70-cluster map. All 114 order-sensitive questions are executed only as diagnostics and never enter claim-promoting suite effects.

## Verifier note

`verify_v5_freeze.py` is a pre-launch guard and deliberately asserts that `formal_v5_results` does not yet exist. It therefore raises after a completed launch. This is not a post-score integrity failure: I replaced that inapplicable guard with an independent canonical-content recomputation and physical hash/size verification of every frozen file. The dedicated release verifier passed.

## Gate decision

All ten audit gates passed: freeze/launch identity, atomic coverage, SQL safety, independent outcome reexecution, 66/114 adjudication, fixed denominators, suite/canonical consistency, statistical recalculation, manifest lineage, and SVG/TeX usability.

**Final decision: `PASS_INTEGRATION`.**
