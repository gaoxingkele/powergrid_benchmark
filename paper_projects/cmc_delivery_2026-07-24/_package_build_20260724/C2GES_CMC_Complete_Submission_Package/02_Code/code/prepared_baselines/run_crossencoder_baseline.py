#!/usr/bin/env python3
"""Prepared cross-encoder reranking baseline for the C2GES benchmark.

Scores each (role-conditioned question, sentence) pair with a supervised
MS MARCO cross-encoder and selects the top-K sentence IDs under the paper's
protocol (same data, K=3 budget, metrics, and document-cluster bootstrap).
CPU-capable; no fine-tuning is performed.

Example (once the workspace data is supplied; see MISSING_ARTIFACTS.md):
    python run_crossencoder_baseline.py \
        --data-dir /path/to/verification_pilot/agent_audit_40doc \
        --out-dir  ./outputs/crossencoder_msmarco_minilm \
        --reference-details /path/to/c2ges_role_selective_graph/details.jsonl
"""

from common import run_cross_encoder_condition

if __name__ == "__main__":
    run_cross_encoder_condition(
        description=__doc__,
        default_model="cross-encoder/ms-marco-MiniLM-L-6-v2",
        condition="crossencoder_msmarco_minilm",
    )
