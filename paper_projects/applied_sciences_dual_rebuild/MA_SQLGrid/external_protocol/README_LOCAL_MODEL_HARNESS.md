# External local-model harness

`code/external_local_model_harness.py` consumes the frozen 91-question RTS-GMLC + SimBench protocol and its four symmetric cells (364 prompts). Dry-run is the default and performs no endpoint call. It copies only prompt-safe fields, verifies exact database/question/perturbation/cell identities and hashes, and rechecks that registered reference SQL and gold/reference field names are absent from every prompt.

## Dry run

Use a new output directory for each run:

```powershell
python code/external_local_model_harness.py --out model_runs/my_dry_run
```

The resulting `run_manifest.json` must say `dry_run_prompts_frozen_not_executed`, `cell_count: 364`, and `canonical_result_eligible: false`.

## Local execution (explicit opt-in)

Copy `runtime_manifest.example.json`, fill it with an immutable model/runtime identity, exact model-file byte count and SHA-256, then start the server separately. The harness accepts only syntactic loopback hosts (`localhost`, `127.0.0.0/8`, or `::1`); credentials in the URL and remote hostnames are rejected.

```powershell
python code/external_local_model_harness.py `
  --execute `
  --out model_runs/qwen_local_seed20260805 `
  --base-url http://127.0.0.1:8000/v1 `
  --model exact-served-model-id `
  --runtime-manifest runtime_manifest.local.json
```

The harness sends one prompt per exact `(dataset_id, question_id, perturbation_id, condition)` key. Responses must contain exactly one `SELECT` or `WITH ... SELECT`. SQLite is opened read-only/immutable with `query_only`, an authorizer denying mutation/schema operations, a VM-step budget, and a row cap.

## Evidence boundary

Current scoring is explicitly `AUTO_CANDIDATE_REFERENCE_SCORING_NOT_HUMAN_GOLD`. It compares canonical SQLite result hashes against the registered automatic references only. `HUMAN_SEALED` is refused because the real two-person review, adjudication, and sealing gates are incomplete. Every run therefore records `canonical_result_eligible: false`; this harness never edits review forms or creates a seal.

## Resume, locks, and incident handling

The incident `FORMAL_RUN_INCIDENT_01.json` showed that wrapper timeout does not prove the child process stopped. Consequently:

- `run.lock.json` is created exclusively and contains PID, host, owner token, timestamp, and run fingerprint. Any active, stale, remote, or unreadable lock blocks execution; never delete it by hand.
- Each prediction and score is append-and-fsync checkpointed under the lock. Resume requires identical configuration, code, source artifacts, model/runtime manifest, prompt bytes, and one unique generation per exact key.
- Duplicate keys, prediction/score disagreement, or fingerprint mismatch are integrity failures. They are never deduplicated or repaired in place.
- Preserve a suspect inactive directory under the managed `model_runs/` root with `--quarantine-existing --quarantine-reason "..."`. This moves it intact under `quarantine/`, writes `QUARANTINE_INCIDENT.json`, and exits. It refuses external paths, links/junctions, and runs owned by an active local PID. Start the clean rerun in a new directory.
- If an outer wrapper times out, first verify/stop the actual harness PID outside this program. Do not start a resume while that PID may still be alive.

Normal clean resumption is:

```powershell
python code/external_local_model_harness.py --execute --resume `
  --out model_runs/qwen_local_seed20260805 `
  --base-url http://127.0.0.1:8000/v1 `
  --model exact-served-model-id `
  --runtime-manifest runtime_manifest.local.json
```

## Tests

```powershell
python -m unittest -v tests/test_external_local_model_harness.py
```

Tests are offline and never call a model endpoint.
