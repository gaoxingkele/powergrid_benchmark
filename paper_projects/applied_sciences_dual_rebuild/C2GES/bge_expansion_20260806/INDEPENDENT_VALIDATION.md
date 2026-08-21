# Independent BGE Expansion Validation

Decision: **PASS_INTEGRATION**

Freeze: `ace48ac0ab12d6177ab251193332652ebcdeb2d363d2484762b24c552dd446d1`

- PASS — BGE 6000 unique rows: `{'rows': 6000, 'unique': 6000}`
- PASS — BGE four complete budgets: `{1: 1500, 3: 1500, 5: 1500, 10: 1500}`
- PASS — BGE mode and finite metrics: `all rows`
- PASS — 145 BGE document clusters: `145`
- PASS — cell coverage c2ges_full K=1: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage c2ges_full K=3: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage c2ges_full K=5: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage c2ges_full K=10: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bm25 K=1: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bm25 K=3: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bm25 K=5: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bm25 K=10: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage minilm_cross_encoder K=1: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage minilm_cross_encoder K=3: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage minilm_cross_encoder K=5: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage minilm_cross_encoder K=10: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bge_reranker_base K=1: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bge_reranker_base K=3: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bge_reranker_base K=5: `{'claims': 1500, 'clusters': 145}`
- PASS — cell coverage bge_reranker_base K=10: `{'claims': 1500, 'clusters': 145}`
- PASS — independent 16-cell metric recomputation: `0.0`
- PASS — independent three-contrast statistics and Holm recomputation: `0.0`
- PASS — formal provenance prediction binding: `a7fa35666bcee3bab13932ba4fb214ed69891712b5511645b51caa40e9283c4c`
- PASS — formal run success and counts: `{'status': 'success', 'boundary': 'model load plus complete FEVER test scoring and all-K extraction', 'device': 'cpu', 'wall_seconds': 727.0614125999855, 'sampled_peak_rss_bytes': 1564876800, 'documents': 1500, 'instances': 1500, 'candidate_pairs': 16825, 'prediction_rows': 6000}`
- PASS — model revision binding: `2cfc18c9415c912f9d8155881c133215df768a70`
- PASS — artifact manifest identity: `{'checked': 19, 'bad': []}`
- PASS — SVG figures parse: `2`
- PASS — TeX and raster/vector assets present: `all present`

Integration is authorized only within the frozen human-gold FEVER zero-shot comparison boundary; this is not NERC validation.
