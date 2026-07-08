# BM25 and K-Sensitivity Supplement

This directory contains the isolated post-freeze supplemental validation
approved by Paper-Harness run `run_20260626-234653`.

Scope:

- Add deterministic Okapi BM25 query retrieval.
- Report \(K \in \{1,3,5\}\) evidence-F1 sensitivity for fixed final
  C2GES, TF-IDF query retrieval, BM25 query retrieval, and SBERT query
  retrieval.
- Reuse the same 40-document agent-verified candidate benchmark, sentence
  segmentation, labels, metrics, and selected C2GES configurations from
  `../experiment_outputs/c2ges_role_selective_graph/cv_protocol.json`.
- Do not retune graph gates, role cue weights, mixture weights, labels,
  segmentation, or evaluation metrics.

Primary artifact:

- `experiment_outputs/bm25_k_sensitivity/summary.json`

Key result at primary \(K=3\):

- Full C2GES evidence F1: `0.2983`
- BM25 query retrieval evidence F1: `0.2273`
- Full C2GES minus BM25 evidence-F1 delta: `+0.0710`
- 95% document-cluster bootstrap CI: `[0.0423, 0.1000]`
- Bootstrap p-value: `<0.001`

K-sensitivity evidence F1:

| Method | K=1 | K=3 | K=5 |
| --- | ---: | ---: | ---: |
| TF-IDF query retrieval | 0.1783 | 0.2122 | 0.2162 |
| BM25 query retrieval | 0.1857 | 0.2273 | 0.2208 |
| SBERT query retrieval | 0.1560 | 0.1972 | 0.2042 |
| Full C2GES reranker | 0.2133 | 0.2983 | 0.2850 |

Interpretation:

- C2GES remains ahead of BM25 at \(K=3\) and \(K=5\) under paired
  document-cluster bootstrap.
- At \(K=1\), C2GES has the highest aggregate F1, but the paired gains over
  TF-IDF and BM25 have confidence intervals crossing zero; this strict setting
  is treated as suggestive rather than conclusive.
