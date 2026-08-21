# Granite 3.3 8B Cross-Family Formal Execution Report

## Status

The clean Granite 3.3 8B execution completed 180 held-out questions in all four frozen cells: 720 prompts, 720 real model responses, 720 scores, and exactly 720 server generation records. It used one foreground harness process (PID 14476), one loopback-only llama.cpp server (PID 26516), no resume, reasoning disabled, temperature 0, seed 20260805, and retries 0.

This run is **not eligible for cross-model or paper claim promotion until an independent post-run audit passes**. The values below are descriptive execution-manifest values, not inferential conclusions.

## Provenance and gates

- Official model: `ibm-granite/granite-3.3-8b-instruct-GGUF`, revision `e40e9dd739c7be00fa965c16ce167088190ce114`, Apache-2.0.
- Artifact: `granite-3.3-8b-instruct-Q4_K_M.gguf`, 4,942,873,344 bytes, SHA-256 `77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca`.
- Runtime: llama.cpp b9637 / `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`, CUDA 13.3, RTX 3090.
- Server: `127.0.0.1:8081`, 16,384-token context versus 131,072 native training context, `--reasoning off`, one slot.
- Prompt-budget preflight: maximum 2,725 tokens; maximum plus 800-token output reserve 3,525; context headroom 12,859.
- Noncanonical smoke: 4/4 provider successes and 4/4 safe executions; zero provider/parse errors and no reasoning text in outputs.
- Formal integrity: 720 unique keys in each artifact, zero provider/parse/scoring errors, zero retries, zero missing response hashes, and zero frozen-hash/model mismatches.

## Descriptive manifest values

| Cell | Correct / 180 | Execution accuracy | Shape-correct / 180 | Shape accuracy |
|---|---:|---:|---:|---:|
| F00 Full, no shape hints | 77 | 42.78% | 82 | 45.56% |
| F01 Full, with shape hints | 100 | 55.56% | 158 | 87.78% |
| F10 Compact, no shape hints | 74 | 41.11% | 79 | 43.89% |
| F11 Compact, with shape hints | 108 | 60.00% | 166 | 92.22% |

Stored labels across 720 attempts are 359 correct, 161 wrong denotation, 151 shape mismatch, and 49 execution error. No cross-backbone effect, significance, or robustness claim is made here.

## Evidence boundary

The authoritative Granite directory is `granite_formal/granite33_8b_q4km_seed20260805_clean1`; exact hashes and PID/generation accounting are in `GRANITE33_FORMAL_EXECUTION_HASH_MANIFEST.json`. The interrupted first artifact transfer is documented separately in `GRANITE33_DOWNLOAD_INCIDENT_01.json`; it affected only acquisition, was resumed without a parallel downloader, and the final file passed exact byte/SHA verification before model loading.

After capture, harness PID 14476 was absent, server PID 26516 exited, port 8081 had no listener, and GPU use returned from 8,936 MiB to 1,266 MiB. The Qwen canonical artifacts were rehashed after the Granite run and remained byte-identical to their accepted independent-audit values.
