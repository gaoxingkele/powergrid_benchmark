# Closest-work comparator: DKASQL and MA-SQLGrid

This table is qualitative by design. It imports no published accuracy/latency number and makes no superiority claim. DKASQL facts below are limited to the independently checked MDPI version of record summarized in the Round-1 reviews (DOI `10.3390/app152011121`).

| Dimension | DKASQL (Applied Sciences, 2025) | MA-SQLGrid current audited study | Comparability consequence |
|---|---|---|---|
| Primary research question | dynamic domain-knowledge adaptation for domain-specific Text-to-SQL | paired effects and interaction of two frozen prompt-package factors across two local snapshots | different contribution type |
| Domain corpus | ElecSQL: 104 expert-authored power-grid supply-chain pairs | GridDB: 180 formal questions over one synthetic 8-table/98-row maintenance database | no shared grid corpus |
| General benchmark | BIRD validation: 1527 questions | none in current canonical analysis | no common public test |
| Knowledge adaptation | domain-knowledge extraction/adaptation and memory | global value inventory versus question-conditioned schema/value/normalization package | modules are not intervention-equivalent |
| Generation workflow | iterative extraction/generation with verification | exactly one model generation per question/cell/backbone | current MA path has no repair loop |
| Comparator families reported | direct, CoT, DIN-SQL, CHASE-SQL; module ablations | four internal factorial prompt packages only | F00 is an internal reference, not a literature-level baseline suite |
| Model coverage | multiple 7B/14B/32B and proprietary models | Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M and Granite-3.3-8B-Instruct GGUF Q4_K_M | breadth differs materially |
| Evaluation emphasis | benchmark performance plus extraction/verification ablations | execution equality, structural diagnostic, paired factorial effects, cluster uncertainty, complete ledgers | metrics/designs answer different questions |
| External validity | BIRD plus expert-authored domain set | external RTS-GMLC/SimBench candidates remain automatic, visible, and human-unreviewed | MA external accuracy is not yet available |
| Open/reproducible evidence needed for a fresh comparison | released implementation should be checked/reproduced where feasible | local prompts, predictions, manifests, audits and hashes exist; public DOI/license pending | published point estimates must not be compared as if same-environment |
| Defensible novelty statement | direct same-journal predecessor | methodological: paired factorial decomposition, backbone sensitivity, evidence ledger, and retained negative results | no “first grid Text-to-SQL” or performance-superiority claim |

## What a numerical comparator requires

A valid numerical comparison must run a released DKASQL implementation, or a clearly labeled **DKASQL-style** reimplementation, in the same environment as MA-SQLGrid: same public benchmark subset, databases, model snapshots, quantization, prompt budget policy, decoding, all-attempt denominator, evaluator, and hardware accounting. Until that run exists, cite DKASQL’s design and evidence scope but do not copy its reported scores beside MA-SQLGrid values.

