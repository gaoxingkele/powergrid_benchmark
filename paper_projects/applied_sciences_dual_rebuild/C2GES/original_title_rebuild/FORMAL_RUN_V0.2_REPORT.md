# C²GES Formal Offline Run v0.2: Strict CF Ablation and Budget Sensitivity

## Material Passport

- Protocol: `C2GES-NERC-FORMAL-v0.2-20260808`
- Status: complete and independently reproduced
- Test reports: 16
- Conditions: 7
- Budgets: 5 and 10 sentences
- Prediction rows: 224
- External API/network use: none
- Semantic baseline: local `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`
- Silver-label boundary: machine-verified candidate evidence, not human/expert gold

## Registered Changes from v0.1

v0.1 remains unchanged. v0.2 makes three prospective changes:

1. `graph_no_cf_strict` removes only the full model's 0.25 CF channel. The retained relevance/role/graph/position weights are divided by 0.75, yielding 0.40/0.2666667/0.2666667/0.0666667. The redundancy penalty and all other decisions remain unchanged.
2. Both five- and ten-sentence budgets are evaluated on the same reports.
3. A semantic-centroid baseline is loaded from a hash-bound local MiniLM snapshot with network access forbidden.

The frozen local model tree contains 11 files (91,578,415 bytes) and has aggregate SHA-256 `2250ea06d09dc1d42d92913d69dd3c0448ed7d31b26657e773ccc6b475c1fb1e`.

## Aggregate Results

### K = 5

| Condition | R-1 F1 | R-2 F1 | R-L F1 | Silver Role Coverage | Redundancy |
|---|---:|---:|---:|---:|---:|
| Lead | 0.2220 | 0.0876 | 0.1262 | 0.2125 | 0.0539 |
| Centroid | 0.2564 | **0.1002** | **0.1405** | 0.2500 | 0.1645 |
| TextRank | 0.2218 | 0.0822 | 0.1267 | 0.1625 | 0.1845 |
| Semantic Centroid | 0.2483 | 0.0889 | 0.1270 | 0.2125 | 0.1031 |
| Role | 0.2367 | 0.0831 | 0.1185 | **0.4250** | 0.0614 |
| Graph without CF, strict | **0.2616** | 0.0924 | 0.1320 | 0.3875 | 0.0805 |
| C²GES Full | 0.2608 | 0.0934 | 0.1323 | 0.3750 | 0.0683 |

### K = 10

| Condition | R-1 F1 | R-2 F1 | R-L F1 | Silver Role Coverage | Redundancy |
|---|---:|---:|---:|---:|---:|
| Lead | 0.3361 | 0.1337 | 0.1629 | 0.3000 | **0.0516** |
| Centroid | 0.3439 | 0.1281 | **0.1681** | 0.3625 | 0.1309 |
| TextRank | 0.3252 | 0.1171 | 0.1583 | 0.2750 | 0.1376 |
| Semantic Centroid | 0.3521 | 0.1288 | 0.1616 | 0.2750 | 0.0984 |
| Role | 0.3540 | 0.1321 | 0.1565 | **0.6250** | 0.0585 |
| Graph without CF, strict | **0.3755** | **0.1396** | 0.1668 | 0.6125 | 0.0762 |
| C²GES Full | 0.3595 | 0.1276 | 0.1593 | 0.5625 | 0.0650 |

Bold marks only the observed column maximum.

## Strict Counterfactual Contrast

At K=5, Full minus strict no-CF was -0.0009 for ROUGE-1 (95% interval [-0.0089, 0.0061]), +0.0010 for ROUGE-2 ([-0.0064, 0.0085]), and +0.0003 for ROUGE-L ([-0.0048, 0.0060]). All intervals cross zero.

At K=10, Full minus strict no-CF was -0.0160 for ROUGE-1 ([-0.0320, -0.0005]), -0.0120 for ROUGE-2 ([-0.0280, 0.0028]), and -0.0075 for ROUGE-L ([-0.0213, 0.0033]). The primary ROUGE-L interval crosses zero. The ROUGE-1 interval is wholly negative, which is evidence against a beneficial CF contribution at this budget in the observed benchmark. Because the emitted comparison family is not multiplicity-adjusted, this remains a bounded exploratory finding rather than a general harm claim.

The strict ablation therefore confirms the v0.1 conclusion: the implemented graph-flow counterfactual sensitivity has no demonstrated benefit. It should remain a tested component with a negative result, not be promoted as the source of performance.

## Semantic Baseline

At K=5, Full minus Semantic Centroid was +0.0125/+0.0045/+0.0052 for ROUGE-1/2/L; all intervals cross zero. At K=10, the corresponding differences were +0.0074/-0.0012/-0.0023, again with all intervals crossing zero. The semantic baseline therefore adds a useful stronger comparator but produces no supported difference from Full.

## Budget Sensitivity

All methods have higher observed ROUGE scores at K=10 than K=5, which is expected when a longer extract is compared with long official Executive Summaries. Full C²GES rises from 0.2608/0.0934/0.1323 to 0.3595/0.1276/0.1593. This is not evidence of improved precision or causal fidelity; it primarily shows the length sensitivity of overlap metrics.

Strict no-CF becomes the strongest observed R-1/R-2 condition at K=10, while Centroid remains the strongest observed R-L condition. The absence of a single dominating condition is stable across the two budgets.

## Reproduction and Integrity

Run 01 and a second full run in a new directory produced identical core hashes:

| Artifact | SHA-256 |
|---|---|
| `predictions.jsonl` | `1f82961f5a406a9aecf561851f66e551bb7ccc33eb7fcabb52f4fd03c1e43be1` |
| `aggregate_metrics.json` | `b26d436ad18f3507b404374b7f6712b4d22ccf14f0031341c12bf4afa5c82f71` |
| `paired_bootstrap.json` | `4ca4aacd66c3c065c7e1e21accafba8464a37f4d805fa3b7932e22e4b54b5ab8` |

All 224 document-budget-condition cells are present, and all metrics are finite values in `[0,1]`.

## Manuscript Decision

Use v0.2 as the authoritative report-level results because it provides the strict CF ablation, K sensitivity, and local semantic comparator. Preserve v0.1 as the initial frozen run and reproducibility history. The manuscript must say:

- Full improves R-1 over Lead and TextRank at K=5 under the earlier v0.1 paired intervals.
- Full is tied with strict no-CF at K=5 and is lower on observed K=10 metrics; CF effectiveness is not supported.
- Centroid has the highest observed R-L at both budgets.
- The local Semantic Centroid is statistically unresolved relative to Full.
- Silver coverage is diagnostic and not expert causal fidelity.
