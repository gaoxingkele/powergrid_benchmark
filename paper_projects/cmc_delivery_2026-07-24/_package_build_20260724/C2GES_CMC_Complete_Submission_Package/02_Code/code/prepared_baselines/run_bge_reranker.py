#!/usr/bin/env python3
"""Prepared BGE reranker baseline for the C2GES benchmark.

Scores each (role-conditioned question, sentence) pair with BAAI/bge-reranker-base
via the sentence-transformers CrossEncoder interface and selects the top-K
sentence IDs under the paper's protocol (same data, K=3 budget, metrics, and
document-cluster bootstrap). CPU-capable; no fine-tuning is performed.

Example (once the workspace data is supplied; see MISSING_ARTIFACTS.md):
    python run_bge_reranker.py \
        --data-dir /path/to/verification_pilot/agent_audit_40doc \
        --out-dir  ./outputs/bge_reranker_base \
        --reference-details /path/to/c2ges_role_selective_graph/details.jsonl
"""

from common import run_cross_encoder_condition

if __name__ == "__main__":
    run_cross_encoder_condition(
        description=__doc__,
        default_model="BAAI/bge-reranker-base",
        condition="bge_reranker_base",
    )
