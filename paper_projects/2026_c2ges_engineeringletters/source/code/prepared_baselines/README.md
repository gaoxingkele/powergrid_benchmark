# Prepared Baselines (awaiting original workspace data)

Protocol-matched harness for the learned/LLM baselines requested by reviewers
(assessment items P1-7 / G3). These scripts are complete and runnable, but the
benchmark data (`verification_pilot/agent_audit_40doc/`, 40 docs / 200 questions
with agent-verified labels) is **not in this repository** — see
`../../../MISSING_ARTIFACTS.md` for the exact files to supply and where to put
them. No results exist yet; nothing here is reported in the paper as an outcome.

All three scripts share the paper's exact protocol via `common.py`, which imports
metric and bootstrap functions directly from `../main.py` (evidence P/R/F1,
ROUGE-L, K=3 budget, document-cluster bootstrap with seed 202502), and emit the
same artifact format (`details.jsonl` + `summary.json`).

| Script | Baseline | Extra deps |
|---|---|---|
| `run_crossencoder_baseline.py` | `cross-encoder/ms-marco-MiniLM-L-6-v2` (CPU-capable) | sentence-transformers |
| `run_bge_reranker.py` | `BAAI/bge-reranker-base` (CPU-capable) | sentence-transformers |
| `run_llm_zeroshot_baseline.py` | zero-shot LLM selection via any OpenAI-compatible endpoint (`--model/--base-url/--api-key-env`), stdlib HTTP, response cache | none |

Common options: `--data-dir` (or `--workspace`/`$C2GES_WORKSPACE`), `--out-dir`,
`--k` (default 3), `--limit-docs N` for smoke tests, and
`--reference-details /path/to/c2ges_role_selective_graph/details.jsonl` to add
paired document-cluster bootstrap comparisons against the paper's Executor
predictions (delta = baseline minus reference).
