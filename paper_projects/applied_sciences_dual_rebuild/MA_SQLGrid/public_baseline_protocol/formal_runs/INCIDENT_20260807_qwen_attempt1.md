# BIRD Formal Run Incident 2026-08-07 — Qwen attempt 1

- **Run**: MA-PUBLIC-BIRD-MINIDEV-v1.0, model=qwen, output `formal_runs/MA_PUBLIC_BIRD_v1_qwen/`
- **Authorization**: human_launch_approval_bird_20260807.json (DONG LUN HAI, 2026-08-07), freeze SHA-256 verified `29c780c6…b42af5`, pre-launch audit 39/39 PASS
- **Timeline**: server start OK (health 200) → runner started → 261 calls recorded in call_ledger.jsonl → llama-server process died silently ~7 min into the run (no error in server log, no CUDA/OOM/exception entries; last entry mid-generation at 131.85 t/s) → runner failed with ConnectionResetError WinError 10054
- **Diagnosis**: silent native crash of llama.cpp b9637 (Windows, CUDA 13.3 build). GPU/ports/processes verified clean afterward. No evidence of prompt-induced failure; no resource exhaustion recorded.
- **Governance**: per FORMAL_RUNBOOK.md, the crashed run is retained as an incident — directory `MA_PUBLIC_BIRD_v1_qwen/` is NOT resumed, overwritten, or deleted. Its 261 ledger rows are incomplete and must not be used for any score.
- **Disposition**: re-attempt the identical frozen protocol (same pinned model hash, flags, seed, prompts, call order) into a NEW directory `MA_PUBLIC_BIRD_v1_qwen_attempt2/`. Approval scope covers the frozen protocol, not a specific attempt; this re-attempt is recorded here for auditability.
- **If attempt 2 crashes again**: stop, do not retry a third time automatically; report to the author with both incident logs.

---

## Addendum — Qwen attempt 2 (2026-08-07)

- **Run**: same frozen protocol, output `formal_runs/MA_PUBLIC_BIRD_v1_qwen_attempt2/`, 341 calls recorded.
- **Failure**: runner abort `Frozen gold stopped executing at question 701` — deterministic fail-closed gate, NOT a server crash (server stayed healthy).
- **Root cause**: operator error — the runner was launched with system Python 3.12 (SQLite 3.49.1). The frozen protocol's runtime boundary is the pinned Python 3.10.11 / SQLite 3.40.1 (`runtime_compat/`, see SQLITE_RUNTIME_COMPATIBILITY.json): under SQLite ≥3.49 the official Q701 gold query plan degenerates and exceeds the 180 s ceiling; under the pinned 3.40.1 it completes in ~0.25 s with result 0.6644518272425249. Verified by direct re-execution under both runtimes on 2026-08-07.
- **Assessment**: attempt 2 violated the documented runtime boundary and is invalid as a formal run; its ledger is retained as an incident artifact and must not be used for any score. Attempt 3 under the pinned runtime is the first protocol-conforming execution.
- **Governance**: no frozen artifact was modified; no retry of individual calls occurred within any run; each attempt used a fresh output directory.

### Launcher note (2026-08-07)

First attempt-3 launch failed at import time (`ModuleNotFoundError: freeze_public_baseline`) because the embeddable pinned Python isolates sys.path via its `._pth` file; zero calls were made and no output directory was created. Relaunched via `runpy.run_path` wrapper with the protocol directory inserted into sys.path; no frozen file was modified.

---

## Addendum 2 — Qwen attempt 3 (2026-08-07)

- **Run**: pinned runtime (Python 3.10.11 / SQLite 3.40.1) via runpy launcher; output `formal_runs/MA_PUBLIC_BIRD_v1_qwen_attempt3/`; 2135/2500 calls recorded (1707 final rows) before abort.
- **Failure**: `sqlite3.Warning: You can only execute one statement at a time` at call_index 2134 (question 98, db=financial, method B1_DECOMP). The Qwen output contained two SELECT statements joined by a semicolon. The frozen `safe_execute` catches `sqlite3.Error`, but `sqlite3.Warning` is NOT a subclass of `sqlite3.Error`, so the error escapes classification and aborts the run.
- **Assessment**: latent defect in the frozen runner triggered by a deterministic model output. Intent of the frozen design (classify invalid SQL, score 0, keep all-attempt denominator) is documented; the implementation does not cover `sqlite3.Warning`. The frozen code files are hash-bound by the 39/39 independent audit (`code_run_formal_public_baseline.py`, `code_freeze_public_baseline.py`), so no local fix was applied.
- **Governance**: run retained as incident artifact; not usable for scores. Per the incident policy above, automatic retry is suspended pending author decision.
- **Options presented to author**: (1) amend safe_execute + re-freeze + re-audit + re-authorize (clean, full cost); (2) documented launcher-level shim catching sqlite3.Warning as a classified execution failure (files untouched, behavior deviation disclosed); (3) run Granite first and keep Qwen suspended.
