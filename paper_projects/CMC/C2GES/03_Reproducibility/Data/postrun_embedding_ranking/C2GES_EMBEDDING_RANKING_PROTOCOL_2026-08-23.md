# C2GES MiniLM Truncation and Ranking-Sensitivity Protocol

Status: frozen before executing the ranking audit on 2026-08-23. This is a post-run representation sensitivity, not a new confirmatory experiment.

## Frozen population and model

- Retained test JSONL: 15 reports / 10 series, SHA-256 `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.
- Model: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- Frozen local snapshot tree SHA-256: `62FFD0D66684928CE0B0F68FD2A411078405B80B7FAF915195ADBDD63454DDF7`.
- Same Semantic-MMR coefficient 0.5, normalized embeddings, CPU, candidate order, source-order output, ROUGE stemming policy, and unit budgets 5/10 as the historical run.

## Representation variants

1. `production_256`: unchanged Sentence-Transformers encoding with `max_seq_length=256`.
2. `extended_512`: same model and pooling stack with `max_seq_length=512`; candidates longer than 512 remain truncated at 512.
3. `chunk_mean_254`: retain the production embedding for candidates of at most 256 tokens. For longer candidates, tokenize without special tokens, divide into non-overlapping chunks of at most 254 content tokens, decode each frozen-token chunk, encode each chunk with the production 256-token stack, average normalized chunk embeddings, and normalize the mean.

The chunk method is an explicit diagnostic pooling rule, not a claim that MiniLM was trained for long-document pooling.

## Selection and endpoints

- Recompute Semantic-MMR selections separately for each representation at K=5 and K=10.
- Report candidate-vector cosine differences, selection overlap, changed report--budget cells, ROUGE-1/2/L, and redundancy.
- Primary diagnostic contrasts: `extended_512 - production_256` and `chunk_mean_254 - production_256` in ROUGE-L at both budgets.
- Estimand: equal-weight mean over the 10 report series; equal-report mean is sensitivity.
- Uncertainty: 10,000 deterministic series bootstrap draws; seeds `20260823 + budget*100 + variant_index`.
- Exact two-sided sign flip over all 1024 series sign assignments; Holm adjustment across four contrasts.

## Privacy and acceptance

- No candidate, reference, prediction, or decoded chunk text is written to outputs.
- Recomputed `production_256` selections and metrics must match the frozen formal Semantic-MMR ledger within numerical tolerance; otherwise the audit fails.
- Exactly 15 reports, 9504 candidates, 10 series, 90 selection rows, and four contrast rows.
- The audit records candidates exposed to each truncation rule and all changed selections.

The audit can identify ranking sensitivity to these representation choices. It cannot establish that any alternative is generally better, semantically correct, or suitable for unseen reports.
