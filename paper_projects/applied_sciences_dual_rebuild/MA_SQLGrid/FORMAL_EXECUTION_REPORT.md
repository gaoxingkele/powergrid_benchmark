# MA-SQLGrid Formal Factorial Execution Report

## Status

The clean single-process formal execution completed 180 held-out questions in all four registered cells: 720 prompts, 720 real local-model responses, and 720 score records. The server log contains exactly 720 generation timing records. Provider errors, SQL extraction errors, scoring-pipeline errors, missing response hashes, prompt-hash mismatches, returned-model mismatches, and frozen run-hash mismatches are all zero.

This is an execution handoff, not a claim promotion. Independent post-run statistical and provenance audit is still mandatory. No inferential analysis was added here.

## Frozen execution

- Model: `qwen2.5-coder-7b-instruct-q4_k_m@13fb94bf`, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.
- Runtime: llama.cpp b9637, commit `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`, Windows CUDA 13.3.
- Configuration: temperature 0, seed 20260805, max tokens 800, retries 0, one parallel slot, loopback-only endpoint.
- Frozen hashes: configuration `f08809f3...fd5`, data `199fcf7c...f266`, code `c9b52f98...8e72`, prompt set `28009f5b...ad5`.
- Run interval: 2026-08-05 07:28:51Z to 07:33:48Z; no resume.

## Descriptive manifest values

| Cell | Correct / 180 | Execution accuracy | Shape-correct / 180 | Shape accuracy |
|---|---:|---:|---:|---:|
| F00 Full, no shape hints | 76 | 42.22% | 90 | 50.00% |
| F01 Full, with shape hints | 129 | 71.67% | 174 | 96.67% |
| F10 Compact, no shape hints | 78 | 43.33% | 79 | 43.89% |
| F11 Compact, with shape hints | 108 | 60.00% | 173 | 96.11% |

Across all 720 registered attempts, the stored score labels are: 391 correct, 156 wrong denotation, 139 shape mismatch, and 34 execution error. These are descriptive counts only.

## Evidence and boundary

The authoritative clean directory is `formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1`. Exact hashes and integrity checks are in `FORMAL_EXECUTION_HASH_MANIFEST.json`. The earlier directory without `_clean_rerun1` is preserved but quarantined because an outer timeout left one harness process alive while a resume process overlapped it; `FORMAL_RUN_INCIDENT_01.json` records that event.

After evidence capture, the exact llama.cpp PID was stopped. No process or TCP listener remained on port 8080, and GPU memory returned from 6,649 MiB used to 1,151 MiB used.
