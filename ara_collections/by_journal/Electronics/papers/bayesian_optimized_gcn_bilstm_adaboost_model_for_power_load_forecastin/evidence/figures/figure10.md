# Figure 10: Prediction error comparison of one week

- **Source**: Figure 10, §4.3 (page 15, top of page)
- **Caption**: "Prediction error comparison of one week."
- **Screenshot**: figure10.png (full-page render of p.15; also contains Figure 11)
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels (each bar carries a printed data label)
- **Reading confidence**: high
- **Plot kind**: bar (grouped by metric)
- **Axes**: X = metric group (MAE(MW), MAPE(%), RMSE(MW)), categorical; Y = Error Value, linear,
  0–4+

| Model | MAE (MW) | MAPE (%) | RMSE (MW) |
|-------|----------|----------|-----------|
| LSTM | 1.61 | 3.48 | 2.16 |
| CNN-LSTM | 1.21 | 2.41 | 1.75 |
| GCN-LSTM | 0.78 | 1.63 | 1.02 |
| GRU | 1.99 | 4.23 | 2.61 |
| Proposed model | 0.34 | 0.68 | 0.43 |

## Trend summary
On the one-week horizon the Proposed model again has the lowest error on all three metrics
(≈2–6× below the best baseline). The baseline ordering differs from the one-day case: GCN-LSTM
becomes the strongest baseline and GRU the weakest — i.e., the graph-spatial baseline generalizes
better over the longer horizon, consistent with the value of spatial feature extraction (C01).
The proposed model's week-level values (0.34 / 0.68% / 0.43) equal the "Proposed model / A Week"
row of Table 4 and the Spearman row of Table 2, confirming internal consistency across evidence
objects. Supports C01.

**Discrepancy note**: as in Figure 9, no CNN-BiLSTM series is shown despite §4 naming it as a
baseline (see `logic/solution/constraints.md`, item 10).
