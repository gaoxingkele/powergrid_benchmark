# Prospective MA-SQLGrid Component Protocol Freeze

Status: **FROZEN_NOT_RUN**. Freeze revision: **v1.1**, dated 2026-08-05. This directory is additive and does not replace either existing canonical release. The registered aggregator and eight synthetic tests were completed before any formal output existed.

## Registered design

One prospective candidate-generation experiment supplies three non-overlapping analyses without outcome-dependent redesign:

- **E1, value-evidence presentation ablation.** `V0_NoValueEvidence` and `V1_WithValueEvidence` have identical question, selected tables/columns, join paths, structural/SQL-operation hints, candidate prompt, model snapshot, and decoding. V0 removes both the exact matched-value block and question-derived normalization-value block. The estimand is therefore the **bundled presented value-evidence effect**, not a pure retrieval effect and not a schema-selection effect.
- **E2, candidate replay validator.** Each successful response requests exactly three candidates. On V1, the first parsed candidate is compared with the frozen reference-answer-independent ranker selection using safety, SQLite executability, output-column shape, ordering, non-empty execution, and presented value coverage. There is no repair call. Selection is sealed before gold is loaded.
- **E4, controlled efficiency.** E1's consecutive within-question calls provide paired wall latency and model-reported token telemetry under deterministic AB/BA order. This estimates the incremental cost of presenting the value package; it does not estimate end-to-end enterprise deployment cost or energy consumption.

The test split has 180 questions and 70 pre-existing normalized-SQL template clusters. The intervention changes frozen context for **170 questions spanning 61 clusters**. The other 10 questions are structurally ineligible for E1/E4 because V0 and V1 contexts are byte-identical; they receive only V1 and remain eligible for E2.

## Models and calls

- Qwen2.5-Coder-7B-Instruct Q4_K_M, frozen SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3`.
- Granite-3.3-8B-Instruct Q4_K_M, frozen SHA-256 `77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca`.
- llama.cpp backend revision `b9637@aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`; temperature 0, seed 20260805, maximum 600 output tokens.
- 350 scored calls per backbone (170 paired V0/V1 + 10 V1-only), 700 total; four unscored warm-up calls per backbone, eight total.

Question order is separately seeded per backbone. Each eligible question's two calls are adjacent, while a deterministic hash balances V0-first and V1-first order. Inference is within backbone only; model loading and server swaps are not included in per-question latency.

## Leakage boundary

Prompt construction receives only `question_id` and `question`. Gold SQL, required literals, answer shape, annotated tables/columns, and results are excluded by whitelist. Selector tables/columns, inferred structural hints, matched values, and normalization hints are computed from the question and database only. `offline_replay.py select` reconstructs V1 context from the frozen non-gold question and seals selections. Only `offline_replay.py score`, which refuses a missing or changed seal, loads evaluator records.

## Immutable artifacts

`PROTOCOL_FREEZE.json` is authoritative for every input hash, prompt-ledger hash, call-order hash, model identity, decoding setting, and population count. `frozen_prompts.jsonl`, `warmup_prompts.jsonl`, and the two `call_order_*.jsonl` ledgers are ready. Re-running `build_freeze.py` after any code or input change creates a new protocol version; it must never silently overwrite an already-started run.

No formal model call was made while creating this freeze.

`aggregate_results.py` is now part of the hashed freeze. It validates prediction, selection, scoring, model, and freeze identities; implements the exact registered bootstrap/randomization/Holm families; emits the descriptive E2 rescue/harm/oracle fields and guarded E4 results; and writes a release manifest. `current_status.py` distinguishes the immutable protocol from adjacent execution state.
