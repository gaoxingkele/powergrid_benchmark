## 1. Proximate cause

The formal evidence acceptance check failed during pytest collection:

```text
ModuleNotFoundError: No module named 'powergrid_benchmark'
```

Consequently, the scientific evidence tests never executed. The experiments validator independently passed and confirmed all **2,310 expected rows**, so the immediate blockage is not a missing experiment cell or an adverse scientific result.

The executor’s statement that both checks passed reflects a separate rerun with an added package path; it does not supersede the preserved `acceptance.json`, which remains the authoritative Hard Gate result.

## 2. Root cause

The acceptance subprocess was not given a reliable worktree-local import environment. Although the retry intended to use `PYTHONPATH=../../src`, that setting was either not propagated to the official acceptance subprocess or was resolved relative to a different working directory.

This is a recurring harness defect: earlier stages also required rerunning the scientific gate with the isolated worktree’s `src` path. The harness does not hermetically establish package imports before invoking pytest.

## 3. Classification

**Primary classification: harness blocker.**

- **Environment symptom:** missing worktree-local package path.
- **Not a manuscript/evidence blocker:** experiment completeness validation passed; adverse/null findings are explicitly allowed by the frozen contract.
- **Not an executor blocker:** the executor exited successfully and produced the frozen result set.
- **Not a human-input blocker:** no scientific or author-supplied information is missing.

## 4. Safe recovery

1. Preserve the locked worktree, immutable results, logs, manifest, hashes, and failed acceptance record.
2. Resolve the worktree’s `src` directory to an absolute path and inject it into the environment of the **official evidence acceptance subprocess**, or install that exact worktree package into its isolated environment.
3. Request another harness-managed retry under unchanged, approved plan version 4.
4. Reuse the completed experiment artifacts only after verifying their contract, source, script, manifest, and result hashes; do not silently regenerate or alter results.
5. Run both declared acceptance checks and require pytest to complete collection and execute the scientific tests successfully.
6. Do not edit `acceptance.json`, manually mark the candidate accepted, or treat the executor’s successful ad hoc rerun as fulfillment of the Hard Gate.

## 5. Harness improvement proposal

Introduce a hermetic acceptance-environment layer:

- Resolve package paths absolutely from the active worktree rather than using relative `PYTHONPATH` entries.
- Use the same environment-construction function for executor, validator, and acceptance subprocesses.
- Before expensive execution, run a preflight import from the exact acceptance working directory and interpreter:

  ```python
  import powergrid_benchmark
  ```

- Log the interpreter, working directory, sanitized `sys.path`, and imported package origin.
- Distinguish infrastructure/collection failures from scientific-test failures while continuing to fail closed.
- Add a regression test using a fresh temporary worktree with no globally installed `powergrid_benchmark`.
- Prevent executor summaries from declaring acceptance success until the harness has reconciled them with the authoritative `acceptance.json`.
- Permit hash-verified reuse of immutable completed experiments after an acceptance-infrastructure failure, while still rerunning every required acceptance gate.
