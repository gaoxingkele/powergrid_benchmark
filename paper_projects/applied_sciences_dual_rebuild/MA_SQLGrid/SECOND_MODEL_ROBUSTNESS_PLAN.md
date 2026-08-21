# MA-SQLGrid Second-Backbone Robustness Plan

## Hard boundary and decision gate

This document is a bounded candidate and execution plan only. **Do not download, merge, extract, start, or query any second model until both conditions hold:**

1. the independent post-run audit accepts the clean Qwen-7B formal directory `formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1`; and
2. the root agent explicitly selects one candidate and completes `SECOND_MODEL_ROBUSTNESS_FREEZE.template.json` as a new immutable freeze manifest.

The clean Qwen-7B prompts, predictions, scores, manifest, logs, and hash manifest are read-only. A second model must use a new model root, a new server-log directory, and a new factorial output directory. No second-model result enters a paper claim until it receives its own independent provenance and paired-statistics audit.

## Candidate comparison

The exact repository revisions and LFS OIDs below were read from the official Hugging Face model/tree APIs on 2026-08-05. An LFS OID is the expected downloaded-file SHA-256; an Xet hash is recorded separately and must not be substituted for it.

| Candidate | Official artifact and provenance | Context / RTX 3090 envelope | Methodological value | Decision |
|---|---|---|---|---|
| **A. Qwen2.5-Coder-14B-Instruct Q4_K_M** | `Qwen/Qwen2.5-Coder-14B-Instruct-GGUF`; revision `d0a692ef765eefbf2fabb130b3cb2e8917e3d225`; single merged file `qwen2.5-coder-14b-instruct-q4_k_m.gguf`; 8,988,110,272 bytes; LFS/file SHA-256 `c1e659736d89ac1065fb495330fb824d94001974a4bfa78e7270e43476a8d940`; Xet `f87bfd654aed5318df1819cc17b5204270b69d05d905c0fa6960d84e4843ba18`; Apache-2.0. | Official Qwen documentation reports 14.7B parameters and long context well beyond the registered 16k server cap. Expected Q4 16k serving VRAM is approximately 11-14 GiB. Expected 720-call time on the RTX 3090 is roughly 8-12 minutes, to be replaced by measured smoke timing. | Cleanly tests **within-family scale robustness** against the accepted 7.61B Qwen backbone while holding coder tuning, chat family, quantization class, prompt set, and runtime nearly fixed. It does not establish cross-family generalization. | Lowest operational risk; recommended only if the paper states “scale robustness within Qwen2.5-Coder,” not “backbone robustness.” |
| **B. IBM Granite 20B Code Instruct Q4_K_M** | `ibm-granite/granite-20b-code-instruct-8k-GGUF`; revision `6e9f892709473675166a5f71d9c07e14d65d67ca`; file `granite-20b-code-instruct.Q4_K_M.gguf`; 12,820,207,360 bytes; LFS/file SHA-256 `60143bf35eb71b18e2982bc61e9a38411e90bafc58badad12418aaa865fca0af`; Xet `82d5c4019305908ed0ee714dd1e425687f78eba9866956b489fead65e8163e3d`; Apache-2.0. | Granite Code 20B is documented as an 8k-context model. Q4 weights should fit the 24 GiB RTX 3090, with an estimated 16-20 GiB serving envelope, but a 16k server context exceeds the documented training window. Expected 720-call time is roughly 12-20 minutes. | Strong independent-family and code/SQL relevance: IBM documents code instruction tuning that includes NL2SQL11. However, using 16k would add an unregistered extrapolation confound; using 8k would break runtime-context parity unless both models receive a separately registered 8k rerun. | **Conditional, not the default.** Select only if a prompt-token audit proves every frozen prompt safely fits 8k and the protocol explicitly accepts an 8k model-native cap. Do not claim a matched 16k comparison. |
| **C. IBM Granite 3.3 8B Instruct Q4_K_M** | `ibm-granite/granite-3.3-8b-instruct-GGUF`; revision `e40e9dd739c7be00fa965c16ce167088190ce114`; file `granite-3.3-8b-instruct-Q4_K_M.gguf`; 4,942,873,344 bytes; LFS/file SHA-256 `77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca`; Xet `2915ea8442203224ce80a51d60b8c9286e034a821b4a9ffe6b110694d63d8887`; Apache-2.0. | IBM documents 8B parameters and a 128k context, so the registered 16k cap is native and conservative. Expected VRAM is approximately 7-9 GiB and expected 720-call time approximately 5-8 minutes. | Best bounded test of **cross-family robustness** at roughly matched scale and identical 16k serving conditions. It is code-capable but general instruction-tuned rather than SQL-specialized, so differences combine architecture/family and specialization. | **Preferred second backbone** when the scientific goal is robustness beyond Qwen. Interpret as cross-family instruction-backbone robustness, not a pure scale or pure SQL-specialization effect. |

Sources: [official Qwen 14B GGUF repository](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-GGUF), [Qwen2.5-Coder family specifications](https://qwenlm.github.io/blog/qwen2.5-coder-family/), [official Granite 20B Code GGUF repository](https://huggingface.co/ibm-granite/granite-20b-code-instruct-8k-GGUF), [IBM Granite Code models and training description](https://github.com/ibm-granite/granite-code-models), and [official Granite 3.3 8B model card](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct).

## Scientific assessment

A Qwen-7B + Qwen-14B pair is scientifically sufficient for the narrow statement that the observed factorial pattern is or is not stable under a same-family scale increase. It is **not sufficient** for a broad claim of model-family or backbone robustness: the tokenizer, pretraining lineage, coder post-training, chat template, and many inductive biases remain shared.

For a paper whose central claim concerns prompt/context design rather than model scaling, an independent family is more informative. Candidate C is therefore the preferred bounded second backbone because it changes family while retaining an official Apache-2.0 GGUF, native 16k support, and low operational risk. Candidate B has stronger explicit NL2SQL relevance but cannot provide a clean matched-16k design. If resources later allow two robustness extensions, the strongest sequence is A for within-family scaling followed by C for cross-family generalization; the two analyses must remain separate.

## Frozen protocol after selection

1. **Audit gate:** obtain written acceptance of the clean Qwen-7B formal run and record the auditor/report hash in the completed freeze manifest.
2. **Selection gate:** root selects exactly one repository/revision/file. Re-query the official repository and tree API; stop if revision, byte count, license, or LFS OID differs from this plan.
3. **Download gate:** use the workspace aria2-first helper only after selection. Download to a candidate-specific directory outside all Qwen-7B artifact trees. Never overwrite or merge into the Qwen directory.
4. **Artifact verification:** verify exact bytes and file SHA-256 before extraction/use. For Qwen 14B, prefer the official already-merged single GGUF; do not download both merged and split variants. For any split artifact selected later, record every shard hash plus the merged-file hash.
5. **Runtime freeze:** initially reuse llama.cpp b9637 / commit `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`, CUDA 13.3. If the selected model fails compatibility, stop rather than silently upgrading; any runtime change requires a new freeze and a compatibility assessment against the Qwen run.
6. **Server containment:** bind only to `127.0.0.1` on a newly selected unused port; `--parallel 1`, temperature 0, seed 20260805, retries 0, max output 800. Candidate A or C uses `--ctx-size 16384`; Candidate B uses at most its documented 8192-token cap unless a separately justified protocol is approved.
7. **Template audit:** verify the model-native chat template and reasoning mode. Do not add model-specific SQL exemplars or content hints. If Granite 3.3 emits reasoning tags, freeze a deterministic, model-agnostic SQL extraction rule before any formal call; do not clean outputs manually.
8. **Noncanonical smoke:** one development question × four cells, then the existing 20-question development split if the first smoke passes. Require four real responses, zero provider errors, non-null response hashes, safe read-only extraction, no gold in prompts, and no truncation.
9. **Prompt budget:** tokenize all 720 already-frozen prompts with the selected tokenizer. Record maximum and percentile input tokens; no prompt may reach the effective context boundary after chat-template overhead and 800-token output reserve.
10. **Formal execution:** only after smoke review, create a new directory and execute 180 × 4 calls. Do not reuse, resume from, or write into Qwen outputs. Preserve every raw response and failure.
11. **Independent audit:** verify generation count equals 720, unique keys equal 720, all hashes match, and no concurrent harness process existed. Run paired question-level analysis separately from the Qwen analysis. No claim promotion before acceptance.

## Stop conditions

Stop before formal execution for any hash/license/revision mismatch, non-loopback listener, unreviewed runtime substitution, prompt truncation, chat-template incompatibility, systemic provider error, unsafe extracted statement, concurrent harness process, or evidence-write failure. Individual model SQL errors during an otherwise healthy formal run are retained and scored, not repaired.
