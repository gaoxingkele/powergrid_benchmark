# Supplementary Evidence Index and Direction Counts

## Rights-safe 40-report index

The non-verbatim index in `original_title_rebuild/R2_v0_3/postrun_sensitivity/rights_safe_metadata/` accounts for all 40 locally frozen source-manifest entries. It contains source-manifest title and URL metadata, source-collection labels, PDF hashes, page counts, series/grouping identifiers, planned group split, actual inclusion status, exclusion reason, reference length and candidate count when applicable, and the unresolved rights fields. It contains no report body, Executive Summary, candidate sentence, prediction, or selected sentence.

The index records 27 included reports and 13 excluded reports. Exclusions comprise 11 reports without a recognized Executive Summary heading and two without a generic, deterministic summary endpoint. Year values are title-derived labels rather than independently verified publication dates; genre labels describe the NERC source collections rather than expert-adjudicated document genres. All 40 rights rows remain fail-closed: the rights holder is `not_verified`, a license/terms locator is not recorded, and PDF/verbatim redistribution is not authorized pending responsible human or institutional review. Consequently, this index closes sampling-accounting transparency but does not close the rights/permission blocker.

## Immutable report-level direction counts

Direction is computed as Full minus comparator in ROUGE-L F1 on the 15 frozen reports:

| K | Comparator | Positive | Negative | Tie |
|---:|---|---:|---:|---:|
| 5 | strict no-CF | 7 | 7 | 1 |
| 5 | Semantic-MMR | 14 | 1 | 0 |
| 5 | TextRank | 14 | 1 | 0 |
| 10 | strict no-CF | 6 | 8 | 1 |
| 10 | Semantic-MMR | 11 | 4 | 0 |
| 10 | TextRank | 13 | 2 | 0 |

These counts are descriptive and should accompany the paired-difference figure. They expose heterogeneity and do not establish maintenance-workflow benefit, factual sufficiency, unsafe-omission performance, or physical causal validity.
