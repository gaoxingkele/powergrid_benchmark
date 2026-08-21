# Prospective BGE Expansion Results

Freeze: `ace48ac0ab12d6177ab251193332652ebcdeb2d363d2484762b24c552dd446d1`.

Primary endpoint: claim-weighted exact sentence-ID evidence F1 at K=3 on 1,500 human-gold FEVER claims in 145 document clusters.

| Comparison | Difference | 95% composition interval | Raw p | Holm p | Promoted |
|---|---:|---:|---:|---:|---|
| bge_reranker_base-minus-c2ges_full | -0.0021 | [-0.0137, +0.0090] | 0.7214 | 1.0000 | false |
| bge_reranker_base-minus-bm25 | +0.0026 | [-0.0116, +0.0162] | 0.7210 | 1.0000 | false |
| bge_reranker_base-minus-minilm_cross_encoder | -0.0123 | [-0.0252, -0.0003] | 0.0570 | 0.1710 | false |

Formal CPU run: 727.1 s; sampled peak RSS 1492.4 MiB; 16825 candidate pairs.

This is a zero-shot FEVER baseline comparison, not NERC or deployed power-grid validation.
