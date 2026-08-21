# Exact Report-Level Sign-Flip Sensitivity

**Status:** unregistered post-run sensitivity; not confirmatory and not a replacement for the registered percentile intervals.

**Frozen input SHA-256:** `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F` (`predictions.jsonl`, expected 210 rows).

No prediction was regenerated and no test hyperparameter was selected. For each of the same six contrasts, all $2^{15}=32,768$ report-level sign assignments were enumerated. The two-sided statistic is the absolute mean paired ROUGE-L difference. This randomization interpretation requires joint sign symmetry/exchangeability of the paired report-level differences under the sharp null; that assumption is a sensitivity assumption and is not established by the 15 reports. Holm adjustment spans all six values.

| K | Contrast | Mean delta | Signs +/-/= | Exact two-sided p | Holm (6) |
|---:|---|---:|---:|---:|---:|
| 5 | `c2ges_full_minus_graph_no_cf_strict` | -0.003332 | 7/7/1 | 0.436768 | 0.436768 |
| 5 | `c2ges_full_minus_semantic_mmr` | 0.020737 | 14/1/0 | 0.000305 | 0.001526 |
| 5 | `c2ges_full_minus_textrank` | 0.025438 | 14/1/0 | 0.000122 | 0.000732 |
| 10 | `c2ges_full_minus_graph_no_cf_strict` | -0.003360 | 6/8/1 | 0.200684 | 0.401367 |
| 10 | `c2ges_full_minus_semantic_mmr` | 0.014360 | 11/4/0 | 0.006592 | 0.026367 |
| 10 | `c2ges_full_minus_textrank` | 0.012029 | 13/2/0 | 0.009644 | 0.028931 |

The registered bootstrap sign-tail quantities remain frozen machine outputs. Because their resampling distribution is centered at the observed empirical distribution rather than generated under a null, they are descriptive tail summaries, not null-calibrated p-values. Holm adjustment of those descriptive quantities does not convert them into hypothesis-test p-values.
