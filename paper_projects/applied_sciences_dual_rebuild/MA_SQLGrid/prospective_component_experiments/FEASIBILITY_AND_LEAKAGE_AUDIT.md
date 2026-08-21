# Feasibility, Reuse, and Leakage Audit

## What can be reused safely

- The frozen 180-question GridDB-Maintenance test split, SQLite snapshot, schema, evaluator, and 70-cluster mapping are locally available and hashed.
- Both accepted local GGUF snapshots and the pinned llama.cpp backend are available. Their manifests contain file size, revision, license, and SHA-256; the execution entry point recomputes the multi-gigabyte model hash before its first call.
- The existing domain context builder and `rank_candidates` implementation are executable. The validator uses schema/database execution evidence and question-derived constraints, not reference SQL or answers.
- Existing canonical Qwen and Granite direct runs remain valid for the original factorial but cannot answer E2 because they contain one SQL per response. Their fixed F00→F11 call order also makes their latency suitable only as descriptive planning evidence, not the new controlled E4 result.

## What is not reused as formal evidence

- An older 900-row C1–C5 run contains three-candidate/validator traces, but it used `gpt-5.4-mini-2026-03-17` through the `krill` provider. Mixing it with the two local canonical backbones would change model, provider, prompts, and runtime environment. It is excluded from E1/E2/E4.
- The existing repair loop is excluded. E2 is candidate replay only, so validator effect is not confounded with a second model call.
- The 10 byte-identical V0/V1 questions are excluded from E1/E4 before outcomes exist. They remain in E2.
- RTS-GMLC/SimBench automatic candidates and uncompleted human forms are outside these component experiments.

## Leakage audit result

The builder uses a two-field whitelist (`question_id`, `question`) before calling the selector. It asserts exact gold SQL absence and V0 removal of both value blocks. Frozen V0/V1 records have identical hashes for selected tables, selected columns, and inferred shape. `verify_freeze.py` checks 360 unique prompt keys, every embedded prompt/context hash, both call orders, and prohibited V0 blocks. The verifier passes.

The experiment still uses a development-touched synthetic database and corpus-tailored structural hints. These experiments strengthen component attribution inside that controlled case; they do not replace the independently reviewed external/sealed benchmark required for broad real-world generalization.
