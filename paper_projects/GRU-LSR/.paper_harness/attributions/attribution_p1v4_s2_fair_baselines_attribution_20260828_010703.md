# Attribution report: `p1v4_s2_fair_baselines_attribution`

## 1. Proximate cause

The outer executor reached its fixed 1,800-second wall-clock limit and returned `exit_code=124`. The harness then marked the stage `BLOCKED` before either acceptance command ran.

At interruption:

- No `acceptance.json`, candidate commit, or `candidate_ready` event existed.
- `run_manifest.json` remained `status: "running"` with an empty `outputs` map.
- Only `run_results.partial.csv` existed.
- The validator expects 2,310 rows, but the preserved partial file contained 1,925 rows; the 0.80-cap execution was incomplete.
- Therefore, the experiment completeness and comparability gates correctly remain unsatisfied.

## 2. Root cause

The root cause is a harness execution-budget and process-lifecycle mismatch.

The 1,800-second allowance covered both implementation work and the scientific run. The stage began at 00:31:51, but the immutable experiment started at approximately 00:53:07, leaving less than nine minutes before the formal timeout for a frozen workload containing 240 training trajectories and 2,310 result rows.

There is also a containment defect: during read-only inspection, the partial result grew from 1,540 to 1,925 rows after the 01:01:53 `stage_blocked` event. The run log likewise recorded activity through at least 01:05:20. Thus, the harness recorded `BLOCKED` before the child workload was demonstrably quiescent, despite `executor.log` claiming that the controlled process tree had been terminated.

There is no evidence here of a scientific-method failure, adverse-result failure, missing author input, or corrupted source data. CPU-only execution contributed to elapsed time but is not itself an environment failure.

## 3. Classification

**Primary classification: harness blocker.**

The immediate symptom is an executor timeout, but the controlling defects are harness-level:

- an unsuitable fixed timeout for a combined implementation-and-computation stage; and
- failure to verify child-process termination before recording the terminal stage state.

The incomplete evidence is a consequence of this blocker, not evidence that the frozen protocol or any model comparison failed scientifically.

## 4. Safe recovery

1. Preserve the current worktree, executor log, run log, manifest, scripts, validator changes, and partial CSV without modification. Wait for verified process quiescence, then record final hashes and timestamps.
2. Mark the current namespace as an interrupted forensic attempt. Do not publish, merge, or use its 1,925 rows for inference.
3. Retry the unchanged, human-approved plan v4 in a fresh worktree and empty immutable attempt namespace. Do not overwrite or resume the interrupted namespace.
4. Before retrying, review the WIP runner and validator against the accepted contract hashes. Any scientific-protocol change requires a new plan and approval; transport-only timeout and containment fixes do not.
5. Give the retry a workload-derived allowance; 7,200 seconds is a conservative immediate ceiling, subject to preflight estimation.
6. Accept only after the manifest is atomically sealed as `completed`, all 2,310 expected rows and all ledgers are present, every frozen cap/horizon/seed/method cell is accounted for, late writes have ceased, and both approved acceptance commands pass. Failed, null, and adverse cells must remain recorded exactly as required.

## 5. Harness improvement proposal

Introduce a fail-closed scientific-job supervisor with:

- Separate budgets for agent implementation and the launched experiment.
- A preflight runtime estimate based on frozen trajectory/row counts, device, and observed per-cell throughput.
- Heartbeats containing the last completed cap/horizon/seed and estimated remaining work.
- OS job-object containment with this timeout sequence: request cancellation, terminate descendants, verify the process group is empty, then emit `stage_blocked`.
- A distinct `child_survived_timeout` classification when quiescence cannot be established.
- Atomic, immutable attempt manifests recording timeout reason, last completed cell, process IDs, termination verification time, and artifact hashes.
- Chunked immutable execution artifacts that may support audited orchestration-level recovery, while final acceptance remains impossible until the complete frozen key ledger and all Hard Gate checks pass.

No partial-result acceptance, Hard Gate bypass, or fabrication of missing evidence is warranted.
