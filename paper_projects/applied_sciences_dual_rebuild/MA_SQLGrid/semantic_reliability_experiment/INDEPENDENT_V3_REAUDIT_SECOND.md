# MA-SQLGrid semantic reliability v3 — independent second re-audit

## Decision

**BLOCK. Do not execute formal Stage-B for freeze content SHA
`92e62f6983527c02117352f273eb7510de887836bdd0a35b9519cbd00cd3f3bc`.**

The freeze file is exactly 13,316 bytes and its physical SHA-256 is
`aa88e6bc7370edb5a100f674a22e933445666e4a851dceb87c4fff63862887c7`.
Its canonical content hash recomputes to the requested content SHA. This audit
did not execute formal Stage-B, did not access formal outcomes, and did not
modify the freeze or code.

## Ten-gate result

| Launch-policy gate | Result | Independent evidence |
|---|---:|---|
| `G1_INPUT_IDENTITY` | PASS | 21/21 frozen files, 2/2 immutable inputs, and 13/13 canonical-v2 accepted inputs match SHA/bytes. Both ledgers have 720 unique expected keys, 720 successes, and singleton data/code/config hashes. |
| `G2_STAGE_A_BLINDNESS` | PASS | Stage A exposes no question/prediction/score input; the bound gold pre-score audit records `prediction_or_score_inputs_accessed=false`. |
| `G3_STATE_REPRODUCIBILITY` | PASS | 18 states partition exactly as 15 semantic + 3 physical diagnostics; 18/18 state and trace hashes match both clean generations. |
| `G4_DATABASE_AND_GOLD_VALIDITY` | PASS | 18/18 integrity checks are `ok`, all foreign-key violation counts are zero, and the bound coverage audit records 3,240/3,240 gold executions with zero errors. |
| `G5_GOLD_STATE_COVERAGE` | PASS | Changed-denotation union is 180/180; no question is uncovered; all five snapshot-empty questions become nonempty in at least two states. |
| `G6_ORDER_REVIEW_AND_ADJUDICATION` | PASS | Review A and B each cover 114/114 and find zero automatically valid ordered items. Their exact hashes feed the bound adjudication, which holds all 114 and leaves 66 order-insensitive primary questions. |
| `G7_COMPARISON_CONTRACT` | PASS | Frozen comparator identity matches; duplicate-preserving unordered matching, ordered comparison, numeric tolerance, NULL, and diagnostic-header policies pass tests. |
| `G8_STAGE_B_FAIL_CLOSED_LOADING` | **BLOCK** | The exact freeze omits required `prediction_bindings` and `pre_score` objects, yet Stage B dereferences them at lines 77 and 84. Stage B also does not verify the frozen-file inventory, immutable question/database hashes, Stage-A manifest physical identity, or launch-policy physical identity. |
| `G9_STATISTICS_AND_DENOMINATORS` | PASS | Exact denominators are enforced: 25,920 atomic, 7,920 primary semantic-state, 16,416 held diagnostic, 528 primary predictions, and 912 held predictions. Missing-row failure, 15-state AND, 3-state exclusion, 70-cluster map, seed 20260805, 100,000 sign flips, 20,000 bootstraps, and one nine-test Holm family are frozen and tested. |
| `G10_RELEASE_AUDIT_SPECIFICATION` | PASS | Frozen builder/verifier hash all release artifacts, enforce atomic/suite/statistical denominators, and bind the contrast CSV to TeX/SVG by source SHA. |

The exact gate IDs and ordering above match
`LAUNCH_APPROVAL_POLICY_V3.json`. Because one required gate is blocked,
`required_gates_all_pass=false` and `authorizes_formal_score=false`.

## Test and identity evidence

- `python -m unittest discover -s tests -p "test_*.py" -v`: **16/16 PASS**.
- `python verify_v3_freeze.py`: **PASS** for content SHA
  `92e62f6983527c02117352f273eb7510de887836bdd0a35b9519cbd00cd3f3bc`.
- Current formal-v3 result directory, V3 launch companion, and V3 formal audit
  were absent before these audit reports were written.
- State and trace re-generation pairs: 18/18 + 18/18 exact hash matches.
- Cluster map: 180 mapped questions, 70 declared clusters, 70 actual clusters.

## Blocking defect

The missing bindings are not cosmetic. `stage_b_score_v2.py` constructs its two
ledger inputs from `freeze["prediction_bindings"]` and its order inventory from
`freeze["pre_score"]["order_checklist_jsonl"]`; neither object exists in the
exact freeze. Adding them would change the content SHA, so this audit cannot
authorize the current freeze.

There is a second fail-closed weakness: Stage B validates the freeze's canonical
content hash and the post-audit companion, but then trusts several current files
without checking the physical identities already recorded by the freeze. In
particular, it does not verify the `frozen_files` array, the current launch
policy, immutable questions/database, or the Stage-A manifest SHA/bytes before
use. An exact-SHA launch gate must reject any such post-audit substitution.

## Required remediation

1. Build a new freeze revision with explicit qwen/granite prediction/manifest
   bindings and the exact pre-score order-checklist binding.
2. Make Stage B verify the frozen-file inventory, policy, immutable inputs, and
   Stage-A manifest physical SHA-256/bytes before reading their content.
3. Perform a fresh full independent audit of the new content SHA and bind that
   exact audit file in the launch companion before formal Stage-B execution.

