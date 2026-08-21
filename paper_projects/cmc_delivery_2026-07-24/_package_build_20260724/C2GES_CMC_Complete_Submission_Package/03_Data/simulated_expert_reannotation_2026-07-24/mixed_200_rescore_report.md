# Mixed-Label 200-Question Rescore

75 labels are AI simulated-expert adjudications; 125 retain the original
agent-verified candidate labels. No label is human gold.

| Method | F1 | Precision | Recall | Hit@3 | MRR@3 | nDCG@3 |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_query | 0.1987 | 0.1850 | 0.2500 | 0.4750 | 0.3650 | 0.2632 |
| bm25_query | 0.2213 | 0.2050 | 0.2762 | 0.5150 | 0.3883 | 0.2892 |
| sbert_query | 0.1851 | 0.1700 | 0.2358 | 0.4500 | 0.3242 | 0.2392 |
| c2ges_query_only | 0.2012 | 0.1833 | 0.2596 | 0.4850 | 0.3708 | 0.2658 |
| c2ges_no_role | 0.2161 | 0.2000 | 0.2737 | 0.5200 | 0.4133 | 0.2913 |
| c2ges_no_graph | 0.2805 | 0.2683 | 0.3358 | 0.6350 | 0.4725 | 0.3506 |
| c2ges_full | 0.2882 | 0.2767 | 0.3429 | 0.6600 | 0.4892 | 0.3578 |
| bge_reranker_base | 0.2500 | 0.2300 | 0.3162 | 0.5650 | 0.4392 | 0.3274 |
| crossencoder_msmarco_minilm | 0.2717 | 0.2533 | 0.3392 | 0.6100 | 0.4850 | 0.3580 |
| llm_zeroshot::deepseek-chat | 0.5872 | 0.5750 | 0.6737 | 0.9550 | 0.8667 | 0.7466 |

## Full C2GES paired document bootstrap

- c2ges_full_vs_tfidf_query: +0.0895, 95% CI [+0.0605, +0.1194], p=0.0000
- c2ges_full_vs_bm25_query: +0.0669, 95% CI [+0.0325, +0.1000], p=0.0000
- c2ges_full_vs_sbert_query: +0.1030, 95% CI [+0.0666, +0.1409], p=0.0000
- c2ges_full_vs_c2ges_query_only: +0.0870, 95% CI [+0.0564, +0.1174], p=0.0000
- c2ges_full_vs_c2ges_no_role: +0.0720, 95% CI [+0.0428, +0.1014], p=0.0000
- c2ges_full_vs_c2ges_no_graph: +0.0076, 95% CI [+0.0017, +0.0140], p=0.0078
- c2ges_full_vs_bge_reranker_base: +0.0382, 95% CI [+0.0005, +0.0763], p=0.0472
- c2ges_full_vs_crossencoder_msmarco_minilm: +0.0164, 95% CI [-0.0189, +0.0513], p=0.3618
- c2ges_full_vs_llm_zeroshot::deepseek-chat: -0.2990, 95% CI [-0.3360, -0.2618], p=0.0000
