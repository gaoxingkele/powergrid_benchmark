# Table 2 - Performance comparison (graph-construction methods, one week)

**Source**: Table 2, §4.1 (page 12, middle of page)
**Caption**: "Performance comparison."
**Screenshot**: table2.png
**Extraction type**: raw_table

One-week forecasting error by graph-construction method (lower is better). Best value per column in
**bold**.

| Model | MAE | MAPE | RMSE |
|-------|-----|------|------|
| Spearman | **0.34** | **0.68%** | **0.43** |
| KNN | 0.42 | 0.82% | 0.55 |
| Learned Graphs | 0.49 | 0.97% | 0.65 |
| Mutual Information | 0.42 | 0.81% | 0.54 |

**Stated deltas (§4.1)**: vs KNN, Spearman improves MAE/MAPE/RMSE by 0.08 / 0.14% / 0.12; vs Learned
Graphs by 0.15 / 0.29% / 0.22; vs Mutual Information by 0.08 / 0.13% / 0.11. Conclusion §5(4) reports an
average overall improvement of 0.10 / 0.19% / 0.15 across the three alternatives.
