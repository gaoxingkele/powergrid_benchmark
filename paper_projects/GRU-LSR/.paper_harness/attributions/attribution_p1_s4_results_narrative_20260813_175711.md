## 1. Proximate cause

The executor was terminated by the 1,800-second wall-clock limit:

- Stage started: `2026-08-13 17:16:01`
- Blocked: `2026-08-13 17:46:02`
- Exit code: `124`
- Reported condition: `codex exec 超时（>1800s）`

No `candidate_committed`, `candidate_ready`, or acceptance result was recorded for this stage.

## 2. Root cause

The stage bundled several expensive operations—artifact regeneration, figure/table synchronization, multi-section rewriting, and full acceptance—into one uncheckpointed executor invocation that did not complete within the harness deadline.

The preserved log does not identify the executor’s last completed subtask or whether it stalled, repeatedly rebuilt artifacts, or was merely still progressing. Therefore, the deeper internal cause is **待核实**. Missing scientific evidence is not established as the cause: the preceding fair-experiment stage was accepted at `17:15:56`.

## 3. Classification

**Primary classification: executor blocker.**

The executor failed to satisfy its completion-time contract. The harness also has an observability weakness because it records only the terminal timeout, but there is no evidence of:

- a manuscript or evidence Hard-Gate failure;
- an environment failure;
- missing human input;
- an acceptance-check failure.

## 4. Safe recovery

1. Preserve the stage worktree, branch, executor log, and timeline cursor.
2. Inspect the worktree diff and generated artifacts to determine the last completed subtask; treat every partial output as unaccepted.
3. Validate that all numerical content derives from the accepted Stage 3 run manifest. Do not reconstruct or interpolate missing results.
4. Retry the approved stage through bounded checkpoints: manifest validation → tables → figures → Results → Abstract/Discussion/Conclusion → supplement.
5. Run the complete original acceptance suite after recomposition. Do not accept the candidate unless every configured Hard Gate passes.
6. If inspection reveals genuinely missing scientific evidence, stop and re-plan through a new approved plan version rather than filling the gap narratively.

## 5. Harness improvement proposal

Add checkpointed execution with heartbeat-based timeout diagnostics:

- Record subtask start/completion, elapsed time, active command, and last modified artifact.
- Apply separate budgets to generation, manuscript rewriting, and acceptance.
- Issue a soft-timeout warning before termination and save a resumable checkpoint.
- On timeout, capture the process state, Git diff summary, completed checkpoints, and pending acceptance checks.
- Resume only from verified checkpoints, while always rerunning the full Hard Gate before `candidate_ready`.

This improves recovery and attribution without relaxing acceptance criteria or manufacturing scientific evidence.
