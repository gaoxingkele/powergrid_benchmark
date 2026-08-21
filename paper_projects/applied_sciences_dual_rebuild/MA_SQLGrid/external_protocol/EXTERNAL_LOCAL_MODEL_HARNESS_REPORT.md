# External local-model harness report

## Outcome

A safe, reproducible execution harness is now available at `code/external_local_model_harness.py`. It consumes the registered 91 RTS-GMLC/SimBench questions in all four symmetric factorial cells (364 exact prompt keys). No model endpoint was called while building or testing it.

## Integrity and safety controls

- Revalidates the frozen protocol size, per-cell balance, unique database/question/perturbation/cell keys, and database/schema/question/perturbation/context/prompt/source/code hashes.
- Copies only prompt-path fields and rejects registered reference SQL or gold/reference markers in prompt text. Reference SQL remains outside request construction.
- Allows model execution only by explicit `--execute`, against a loopback OpenAI-compatible URL, with a required pinned model/runtime manifest and verified model-file size/SHA-256.
- Extracts exactly one read-only `SELECT` or `WITH ... SELECT`; rejects multiple statements and mutation/schema tokens. Executes in SQLite read-only/immutable/query-only mode with an authorizer, VM-step budget, and row limit.
- Labels all current comparisons `AUTO_CANDIDATE_REFERENCE_SCORING_NOT_HUMAN_GOLD`. `HUMAN_SEALED` mode is refused. `canonical_result_eligible` remains false because the review packet records zero completed human reviews and zero sealed items.

## Incident controls

Following `FORMAL_RUN_INCIDENT_01.json`, an exclusive PID/host/token lock prevents concurrent generation. Append-and-fsync checkpoints avoid whole-file replacement during generation. Resume refuses duplicate exact keys, prediction/score key divergence, changed prompts, or any configuration/code/data/runtime fingerprint mismatch. Stale locks and suspect evidence are never silently removed or repaired. An explicit quarantine operation preserves the entire inactive run, records an incident, exits, and requires a clean run directory; active local PIDs cannot be quarantined.

## Validation

The offline suite checks the 91 x 4 registry, prompt/reference separation, loopback filtering, single-query guard, read-only SQLite execution, dry-run output, lock overlap refusal, and the human-sealed gate. The harness does not launch a server, call an endpoint in dry-run/tests, edit review forms, simulate reviewers, seal data, or modify manuscript/claim-ledger files.
