# Attribution report: `p1v4_s2_fair_baselines_attribution`

## 1. Proximate cause

The stage was blocked because the mandatory evidence acceptance command exited with code 1 while collecting `tests/test_mintou_experiments.py`:

```text
ModuleNotFoundError: No module named 'powergrid_benchmark'
```

The failure occurred before any scientific regression assertion ran. The frozen experiment validator independently passed all **2,310/2,310 rows**.

The executor’s statement that both checks passed under `PYTHONPATH=../../src` does not supersede the harness-recorded acceptance failure, which ran without an equivalent import-path setup.

## 2. Root cause

The scientific acceptance launcher assumes that `powergrid_benchmark` is already importable from the isolated worktree, but it does not establish that condition itself:

- It invokes the ambient `pytest` executable.
- It sets the working directory to the worktree root.
- It does not prepend `<worktree>/src` to `PYTHONPATH`.
- The retry worktree lacks the root `pytest.ini` that would otherwise add `src`.
- Consequently, the worktree-local package could not be resolved during test collection.

This is a deterministic acceptance-launch integration defect. It is not caused by missing experiment rows, adverse results, or a violation of the frozen scientific contract.

The earlier 1,800-second transport timeout was a separate first-attempt harness incident. The retry completed the executor successfully; the current blocking event is the import-path failure at acceptance.

## 3. Classification

**Primary classification: harness blocker**

**Contributing manifestation: environment/configuration blocker**

Not classified as:

- **Manuscript/evidence:** The experiment validator passed with 2,310 complete rows and the expected contract hash.
- **Executor:** The retry executor exited successfully and recorded the required artifacts.
- **Human input:** No author-supplied metadata or scientific judgment is needed to make the package importable.

The preserved adverse and null outcomes—including Persistence outperforming selected GRU-LSR, the retrieval reversal, and zero positive onset cells—are valid scientific results and must not be altered or treated as acceptance failures.

## 4. Safe recovery

1. Preserve both incident worktrees, the retry nonce, logs, acceptance record, results, and hashes unchanged.
2. Rerun the **same frozen evidence acceptance check** using the retry worktree’s own source tree, explicitly setting `PYTHONPATH` to `<retry-worktree>/src`.
3. Record the resolved package location and verify that it lies inside worktree `3437e2e7751343b3`, preventing accidental use of the mutable main checkout.
4. If collection and all evidence tests pass, use the harness’s documented candidate-recovery path and retain both the original failure and recovery audit trail.
5. If any test fails after imports succeed, keep the stage `BLOCKED` and attribute that substantive failure separately.

This recovery does not modify plan v4, rerun or select experiments opportunistically, suppress adverse findings, or bypass the Hard Gate.

## 5. Harness improvement proposal

Make acceptance execution self-contained and worktree-local:

- Launch tests with `sys.executable -m pytest`, avoiding an unrelated ambient `pytest` interpreter.
- Deterministically prepend `<worktree>/src` to the subprocess import path.
- Add a preflight import that records:
  - Python executable and version
  - working directory
  - effective source path
  - resolved `powergrid_benchmark` module location
- Fail with a distinct `acceptance_environment_error` when import setup is invalid, instead of reporting it as scientific evidence regression.
- Assert that imported project modules resolve beneath the immutable worktree.
- Add a harness regression test that runs acceptance from a clean environment with no inherited `PYTHONPATH` and no dependency on root-level `pytest.ini`.
- Preserve acceptance command, environment fingerprint, stdout, stderr, and exit code in the stage record.

The candidate must remain blocked until the unchanged evidence gate executes successfully.
