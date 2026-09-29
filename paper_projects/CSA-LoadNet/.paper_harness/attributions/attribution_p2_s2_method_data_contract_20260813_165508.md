## 1. Proximate cause

The executor exceeded the fixed 1,800-second limit and was terminated with `exit_code=124`. It therefore never produced `candidate_committed`, `candidate_ready`, or an acceptance result.

The preserved worktree contains uncommitted changes across 11 files. Its last modification occurred at 16:51:43, roughly 87 seconds before termination, indicating ongoing work rather than an immediate crash.

## 2. Root cause

The approved stage was too broad for an indivisible, all-or-nothing 30-minute execution window. It combined:

- Forecast-target and geometry terminology corrections.
- Reconciliation and aggregation specification.
- Model-capacity accounting.
- Three datasets’ cleaning, timestamp, time-zone, daylight-saving, missingness, labeling, and filtering contracts.
- Synchronization of several manuscript and generated representations.

The executor changed approximately 723 added and 1,130 deleted lines but had no durable checkpoint before timeout. Because the log records only the wrapper timeout, the precise final operation is unknown; a deadlock, environment failure, or missing-evidence wait is not demonstrated.

## 3. Classification

**Primary classification: harness blocker.**

| Category | Assessment |
|---|---|
| Harness | **Primary:** fixed wall-clock termination, insufficient progress telemetry, and no resumable checkpoint for an oversized stage. |
| Executor | Secondary symptom: it did not finish or hand off a candidate within the allotted time. |
| Manuscript/evidence | Not established as the cause. Newly introduced scientific and preprocessing details still require verification before acceptance. |
| Environment | Not supported; worktree creation succeeded and files were modified near the timeout. |
| Human input | Not supported; this stage does not require author metadata or other inherently human-only facts. |

## 4. Safe recovery

1. Keep the stage `BLOCKED` and preserve the branch, dirty worktree, logs, and timeline.
2. Snapshot the current diff as a non-acceptable recovery checkpoint. Do not treat it as a candidate.
3. Audit every added numeric or procedural statement—especially missing-row counts, timestamp semantics, hierarchy definitions, parameter counts, and train-only filtering—against code, data, and existing evidence. Mark unsupported items `待核实`.
4. Because the stage granularity is implicated, create a new plan version splitting it into:

   - Geometry terminology and scalar forecast-target contract.
   - Data cleaning, timestamp, missingness, DST, and filter contract.
   - Aggregation, reconciliation, and capacity specification.
   - Regeneration and cross-artifact consistency validation.

5. Obtain human approval for the new plan, replay only verified changes, and run every original Hard Gate. Do not accept the preserved dirty diff directly.

## 5. Harness improvement proposal

Add checkpoint-aware execution with:

- A preflight scope check that flags stages spanning multiple independent scientific contracts.
- Periodic heartbeats recording the active task, changed-file manifest, diff hash, and completed validation steps.
- Separate idle and absolute timeouts, with a graceful checkpoint window before forced termination.
- Canonical-source editing followed by deterministic regeneration of derived Markdown/TeX copies.
- Timeout recovery that preserves a WIP snapshot but always requires a fresh candidate and full Hard-Gate acceptance.

This would retain unfinished work and improve diagnosis without weakening scientific review or manufacturing missing evidence.
