# Frozen-Prediction Rescoring on the Simulated-Expert Subset

**Disclosure:** labels are adjudicated from three AI simulated-expert
annotations; they are not human-gold labels.

- Documents: 15
- Questions: 75
- Original/adjudicated exact-set agreement: 0.387
- Original/adjudicated mean set F1: 0.765

| Method | F1 | Precision | Recall | Hit@3 | MRR@3 | nDCG@3 |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_query | 0.2257 | 0.1733 | 0.3656 | 0.4933 | 0.3911 | 0.3340 |
| bm25_query | 0.2712 | 0.2133 | 0.4200 | 0.5733 | 0.4800 | 0.4089 |
| sbert_query | 0.2321 | 0.1778 | 0.3711 | 0.5067 | 0.3889 | 0.3368 |
| c2ges_query_only | 0.2488 | 0.1911 | 0.4033 | 0.5467 | 0.4089 | 0.3555 |
| c2ges_no_role | 0.2641 | 0.2044 | 0.4222 | 0.5733 | 0.4378 | 0.3793 |
| c2ges_no_graph | 0.2637 | 0.2044 | 0.4178 | 0.5600 | 0.4422 | 0.3817 |
| c2ges_full | 0.2719 | 0.2133 | 0.4256 | 0.5867 | 0.4222 | 0.3727 |
| bge_reranker_base | 0.3035 | 0.2356 | 0.4811 | 0.6667 | 0.5044 | 0.4360 |
| crossencoder_msmarco_minilm | 0.3155 | 0.2444 | 0.5011 | 0.6667 | 0.5156 | 0.4517 |
| llm_zeroshot::deepseek-chat | 0.5699 | 0.4667 | 0.8300 | 0.9333 | 0.8533 | 0.8118 |

## Paired document-cluster bootstrap (F1)

| Comparison | Mean difference | 95% CI | p |
|---|---:|---:|---:|
| c2ges_full_vs_tfidf_query | 0.0463 | [-0.0033, 0.0989] | 0.0662 |
| c2ges_full_vs_bm25_query | 0.0007 | [-0.0580, 0.0580] | 0.9700 |
| c2ges_full_vs_sbert_query | 0.0399 | [-0.0034, 0.0873] | 0.0752 |
| c2ges_full_vs_c2ges_query_only | 0.0232 | [-0.0277, 0.0780] | 0.3954 |
| c2ges_full_vs_c2ges_no_role | 0.0078 | [-0.0364, 0.0549] | 0.7610 |
| c2ges_full_vs_c2ges_no_graph | 0.0083 | [0.0000, 0.0210] | 0.2480 |
| c2ges_full_vs_bge_reranker_base | -0.0316 | [-0.0956, 0.0289] | 0.3214 |
| c2ges_full_vs_crossencoder_msmarco_minilm | -0.0436 | [-0.0944, 0.0110] | 0.1160 |
| c2ges_full_vs_llm_zeroshot::deepseek-chat | -0.2980 | [-0.3592, -0.2411] | 0.0000 |
