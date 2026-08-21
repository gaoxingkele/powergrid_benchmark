# MA-SQLGrid public-baseline feasibility audit

**Audit date:** 2026-08-05  
**Status:** feasibility established; protocol is a draft and no baseline model experiment has started  
**Scope:** MA-SQLGrid Round-1 gaps `MA-R1-M06` and `R1-DV-M02` only. The manuscript was not edited.

## Decision

A same-hardware public comparison is feasible with the two already audited local backbones and the official BIRD SQLite resources. The recommended primary population is the complete, official BIRD Mini-Dev SQLite set of 500 items, not an author-selected subset. It is small enough for a two-backbone/four-method study, already spans 11 databases and three official difficulty levels, and removes result-dependent item selection from the design.

The experiment must **not** be described as a reproduction of DKASQL. The version-of-record article describes the extraction, generation, verification, and memory modules but provides no official implementation, supplementary code, environment lock, prompt files, or immutable code revision. Its Data Availability Statement links BIRD and ElecSQL data only. Searches of the article, its DOI/title, author names, and official-source links found no author-maintained implementation as of the audit date. A transparent `DKASQL-style` label is permissible for a newly implemented comparator, but its point estimates cannot be presented as a reproduction or compared numerically as though protocols were identical.

## Inputs read

- Both independent Round-1 reviews and issue matrices.
- `manuscript_support/REFERENCE_AUDIT.md` and the verified bibliography.
- Bian et al., “DKASQL: Dynamic Knowledge Adaptation for Domain-Specific Text-to-SQL,” *Applied Sciences* 15(20), 11121, DOI `10.3390/app152011121` (version of record).
- BIRD project website, official `AlibabaResearch/DAMO-ConvAI/bird` repository, official `bird-bench/mini_dev` repository, and official `birdsql` Hugging Face organization resources.
- Existing Qwen, Granite, llama.cpp, run manifests, and hardware audit in this workspace.

Only original/official sources were admitted. Third-party BIRD mirrors and unofficial harnesses were excluded.

## Local asset audit

| Asset | Local status | Evidence / implication |
|---|---|---|
| BIRD databases | Absent | No BIRD-named database/archive directory was found in the workspace or `external_repos`. The official database package remains to be downloaded after protocol approval. |
| BIRD/DAMO code | Absent | No local clone was found. Official evaluation code is available under `AlibabaResearch/DAMO-ConvAI/bird` and is MIT-licensed at repository level. Pin before use. |
| BIRD metadata | Present, metadata only | Version-pinned current dev JSON, Mini-Dev SQLite JSON, and two official READMEs are in `official_metadata/`; their hashes are in `DOWNLOAD_LICENSE_CHECKLIST.md`. No database contents were downloaded. |
| DKASQL implementation | Absent; no official release located | Do not claim reproduction. No code download is authorized by the article because no implementation link is supplied. |
| Qwen model | Present and previously audited | Qwen2.5-Coder-7B-Instruct Q4_K_M, 4,683,073,536 bytes, SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. |
| Granite model | Present and previously audited | Granite-3.3-8B-Instruct Q4_K_M, 4,942,873,344 bytes, SHA-256 `77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca`. |
| Runtime | Present and previously audited | llama.cpp b9637, commit `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3`, Windows CUDA 13.3. |
| Hardware | Available | One NVIDIA RTX 3090 (24,576 MiB); one model/server and one generation slot at a time. |

## BIRD facts verified from official resources

### License and distribution

The BIRD project announced that its data license was changed to **CC BY-SA 4.0** on 27 April 2024. The current official Hugging Face dataset cards also declare `cc-by-sa-4.0`. Attribution, license notice, change indication, and ShareAlike obligations therefore apply to redistributed dataset derivatives. The DAMO-ConvAI repository is MIT-licensed. The `bird-bench/mini_dev` repository itself does not expose a repository-level SPDX license through the GitHub API, so its code should not be redistributed independently until the maintainers clarify that boundary; the dataset may be used under the BIRD data license.

### Current clean dev annotation

The official resource `birdsql/bird_sql_dev_20251106` was pinned at Hugging Face revision `3c11fb193e5439b338e23677fa0aae11e8b85db9`. Its 946,793-byte JSON contains 1,534 records with fields:

`question_id`, `db_id`, `question`, `evidence`, `SQL`, `difficulty`.

It covers 11 databases and has 860 simple, 443 moderate, and 231 challenging questions. There are 1,432 `SELECT`-prefixed and 102 `WITH`-prefixed gold SQL statements; no write statement was observed. There are 1,533 unique `(db_id, question)` pairs, so one duplicate natural-language/database pair must be documented rather than silently dropped if the full dev set is ever used.

### Official Mini-Dev SQLite subset

The official `birdsql/bird_mini_dev` metadata was pinned at revision `f65faf4ae3b638c1fa6df1d3370c8d92c8366301`. The SQLite split has exactly 500 unique `question_id` values across the same 11 databases:

| Difficulty | Items |
|---|---:|
| Simple | 148 |
| Moderate | 250 |
| Challenging | 102 |

Database counts are California Schools 30, Card Games 52, Codebase Community 49, Debit Card 30, European Football 51, Financial 32, Formula 1 66, Student Club 48, Superhero 52, Thrombosis Prediction 50, and Toxicology 40. The 500-item official subset is the primary recommendation because it is public and fixed independently of MA-SQLGrid results.

### Download size and format

- Current clean dev annotation JSON: 946,793 bytes.
- Mini-Dev SQLite annotation JSON: 278,513 bytes.
- Official `dev.zip` database package: 346,207,293 compressed bytes (HTTP HEAD, 2026-08-05), ETag `04B4AF221C9186361F09B16ABFD917EC`, last modified 2024-06-29. The project does not publish a SHA-256 on the checked page; compute one after download and freeze it before extraction/use.
- The official repository expects per-database folders with SQLite contents and `database_description` CSV files. Each question row provides database ID, natural-language question, expert evidence, gold SQL, and difficulty. Official EX evaluation executes predicted and gold SQL on the named database.

The metadata revision and database archive are separate version boundaries. Compatibility must be checked by requiring all 11 Mini-Dev `db_id` directories and by executing all 500 gold SQL statements before prompt construction. Any failure blocks the formal run; no item may be dropped.

## DKASQL reproducibility boundary

The paper reports BIRD validation (1,527 questions in that article's snapshot) and ElecSQL (104 pairs), hybrid BGE-m3/keyword retrieval, FAISS, PyTorch 1.13, Transformers 4.38, API-served LLMs, and an RTX 3090 for non-LLM components. It does not provide enough material to reconstruct its prompts, thresholds, stopping rules, knowledge-memory update order, API snapshots, or evaluator implementation exactly.

Consequences:

1. Do not name any new row `DKASQL reproduced` or `DKASQL replication`.
2. Do not import the article's BIRD number into a same-table head-to-head comparison: its 1,527-item snapshot, API models, knowledge aggregation, and evaluator boundary differ from the proposed current 500-item run.
3. A comparator inspired by its published modules must be named `dynamic-retrieval-and-repair (DKASQL-style, independent implementation)` and accompanied by complete prompts/code/hashes.
4. A closest-work table may compare task, data snapshot, knowledge source, modules, models, metrics, external evidence, and open artifacts qualitatively.

## Baseline feasibility on current offline models

All four classes can run with both current GGUF backbones through the existing loopback-only llama.cpp service. No extra generative model is required.

| ID | Class | Frozen implementation | Model calls/item | Current Qwen/Granite |
|---|---|---|---:|---|
| `B0_DIRECT` | Direct | Question + full DDL/key relations + official oracle evidence; SQL-only response. | 1 | Ready after BIRD DB/preflight |
| `B1_DECOMP` | CoT/decomposition | One structured response with schema links, clause plan, and final SQL; only final SQL is scored. No hidden reasoning claim. | 1 | Ready after prompt adapter |
| `B2_SCHEMA_SELECT` | Schema selection/retrieval | Deterministic lexical/BM25 table-column ranking plus foreign-key closure; frozen top-k/threshold/fallback; one SQL generation. Selector uses no gold fields. | 1 | Ready after selector implementation and recall-only offline audit |
| `B3_EXEC_REPAIR` | Candidate verification/repair | Initial candidate, deterministic safety/SQLite execution, then a second call with bounded error feedback and selected schema; final candidate is scored on all attempts. | 2 | Ready after replay/repair harness implementation |

`B3_EXEC_REPAIR` is a genuine execution-feedback pipeline, not a DKASQL reproduction. Its second call is always made, including when the first SQL executes, so call accounting and selection do not depend on outcome.

## Resource estimate

For 500 questions, four methods, and two backbones, the plan requires **5,000 generation calls**: `500 × 2 models × (1+1+1+2)`. Each method receives the same per-question total envelope of at most 12,000 input tokens and 800 generated tokens; `B3` splits the output allowance 400+400 and the aggregate input allowance across two calls. Exact tokenizer counts are logged. If any method cannot fit without truncation, preflight fails and the common budget must be revised before freezing.

| Resource | Expected requirement |
|---|---|
| GPU | One RTX 3090; sequential Qwen then Granite; one slot; no concurrent harness |
| Peak VRAM | Prior observed Qwen approximately 6.65 GiB used and Granite approximately 8.94 GiB used; conservatively reserve 12 GiB and record actual peak |
| Additional disk | 0.35 GB compressed BIRD dev archive; plan 2–5 GB working/extracted space plus <2 GB ledgers/logs |
| Generation time | Prior short-GridDB runs took 5.0 min (Qwen, 720 calls) and 9.4 min (Granite, 720 calls). BIRD prompts/SQL are longer; budget **3–8 GPU-hours**, plus up to 2 hours for gold preflight/evaluation/audit. This is a planning range, not a measured BIRD throughput claim. |
| Calls | Qwen 2,500; Granite 2,500; 5,000 total; retries frozen to zero |
| Output token ceiling | 4,000,000 tokens total worst case; actual usage expected lower and must be reported |

## Blocking gates

1. Download the official database archive with the repository `aria2c` policy; record bytes and SHA-256.
2. Confirm the archive contains all 11 expected Mini-Dev databases and no symlink/reparse-point surprise before extraction.
3. Pass 500/500 official gold execution checks; do not drop failures.
4. Implement and unit-test BIRD prompt serialization, output extraction, official EX scoring, and safe read-only execution.
5. Freeze all four prompt templates, selector thresholds, FK closure, execution feedback sanitization, stop rules, token budgets, run order, and exact hashes.
6. Independently audit that no gold SQL, difficulty label, or gold-required schema is available to generation/selection.
7. Decide whether oracle evidence is included. The current draft freezes it **included for every method** to match the standard BIRD oracle-evidence track; changing this creates a different experiment.
8. Have a second reviewer sign the JSON freeze before any model server is started.

## Scientific interpretation allowed after execution

This suite may establish same-snapshot differences among four transparent baselines on a public BIRD development subset. It cannot establish DKASQL replication, uncontaminated test generalization, or power-grid-domain effectiveness. BIRD Mini-Dev is development-visible and cross-domain; the separate human-reviewed/sealed grid experiment remains necessary for the Applied Sciences application claim.

