# Qwen-7B External AUTO_CANDIDATE Diagnostic

## Boundary

This run is a strictly noncanonical development diagnostic over the existing unsealed RTS-GMLC and SimBench automatic candidates. `HUMAN_SEALED` was not used or created. The manifest and all 364 score rows retain `canonical_result_eligible=false`, `human_reviewed=false`, `sealed=false`, and the label `AUTO_CANDIDATE_REFERENCE_SCORING_NOT_HUMAN_GOLD`. No claim ledger or manuscript file was updated.

## Preflight and execution integrity

- The dry run contained exactly 91 question instances and 364 exact factorial keys, with 91 rows in each cell: RTS-GMLC 55 questions and SimBench 36.
- Both registered SQLite database hashes matched. All 91 registered automatic reference queries were safe and executable; none entered a model prompt.
- The human packet remained unsealed: zero completed human reviews and zero sealed items.
- Thirteen protocol/harness tests passed before and after execution, including loopback filtering, read-only execution, lock overlap refusal, reference isolation, and explicit rejection of `HUMAN_SEALED`.
- The audited Qwen-7B GGUF reverified at 4,683,073,536 bytes and SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.
- One loopback server ran as PID 25224 on `127.0.0.1:8080`; one foreground harness ran as PID 24132. Its exclusive lock carried the same PID and run fingerprint. No resume occurred.
- Final artifacts contain 364 unique exact keys and 364 unique generation IDs. The server log contains exactly 364 launches and 364 generation timings, with no E-level server record.
- The harness and lock exited cleanly. Server PID 25224 was stopped, port 8080 had no listener, and GPU use returned from 6,754 MiB to 1,257 MiB.

## Mechanical diagnostic results

All 364 extracted statements passed the single-query read-only safety guard. Of these, 321 executed successfully against their mapped read-only SQLite database; 43 RTS-GMLC queries produced ordinary SQLite execution errors. There were no provider errors, parse errors, missing response hashes, model-ID mismatches, or fingerprint mismatches.

| Cell | Attempts | Executable | AUTO_CANDIDATE reference matches |
|---|---:|---:|---:|
| F00 Full, no shape hints | 91 | 79 | 2 |
| F01 Full, with shape hints | 91 | 79 | 3 |
| F10 Compact, no shape hints | 91 | 81 | 5 |
| F11 Compact, with shape hints | 91 | 82 | 5 |

| Dataset | Attempts | Safe | Executable | AUTO_CANDIDATE reference matches |
|---|---:|---:|---:|---:|
| RTS-GMLC automatic pilot | 220 | 220 | 177 | 0 |
| SimBench automatic pilot | 144 | 144 | 144 | 15 |

The 43 execution errors were: 20 references to absent `fuel`, 12 to absent `generator_id`, 9 to absent `nonfuel_start_cost_usd`, and 2 ambiguous `generator_uid` projections. These are retained model outputs, not repaired queries.

The 15 automatic-reference matches are **not human-gold accuracy** and must not be cited as external generalization. They show only how model executions compare mechanically with development-visible automatic references whose language validity, ambiguity, unit conventions, tie policy, and template similarity have not been human-adjudicated.

## Evidence

The authoritative run is `model_runs/qwen7_external_auto_candidate_seed20260805_clean1`; server evidence is under `server_logs/qwen7_external_auto_candidate_seed20260805_clean1`. Exact hashes, PID/generation accounting, database mapping, errors, and evidence flags are frozen in `QWEN7_EXTERNAL_AUTO_CANDIDATE_HASH_MANIFEST.json`. No incident or quarantine was required.
