# C2GES MiniLM truncation audit

Status: post-run diagnostic; no embeddings or selections were regenerated.

The frozen model is `sentence-transformers/all-MiniLM-L6-v2` at revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Its Sentence-Transformers configuration sets `max_seq_length=256` although the underlying BERT configuration supports 512 positions. Token lengths below include special tokens and were measured with truncation disabled solely to quantify what the production encoder would truncate.

| Split | Candidates | Median tokens | P95 | Maximum | Over 256 | Fraction over 256 |
|---|---:|---:|---:|---:|---:|---:|
| dev | 3420 | 31.0 | 81.0 | 673 | 9 | 0.0026 |
| test | 9504 | 33.0 | 90.0 | 525 | 29 | 0.0031 |
| all | 12924 | 33.0 | 89.0 | 673 | 38 | 0.0029 |

This audit measures exposure to truncation; it does not establish whether truncation changed rankings. A ranking comparison with layout-aware short units or an explicitly pooled long-context representation remains required before claiming truncation robustness.
