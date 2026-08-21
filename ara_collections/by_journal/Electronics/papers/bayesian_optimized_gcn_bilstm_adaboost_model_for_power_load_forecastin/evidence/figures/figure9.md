# Figure 9: Prediction error comparison of one day

- **Source**: Figure 9, §4.3 (page 14, bottom of page)
- **Caption**: "Prediction error comparison of one day."
- **Screenshot**: figure9.png (full-page render of p.14; also contains Figures 7–8)
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels (each bar carries a printed data label)
- **Reading confidence**: high
- **Plot kind**: bar (grouped by metric)
- **Axes**: X = metric group (MAE(MW), MAPE(%), RMSE(MW)), categorical; Y = Error Value, linear,
  0–4+

| Model | MAE (MW) | MAPE (%) | RMSE (MW) |
|-------|----------|----------|-----------|
| LSTM | 2.60 | 3.96 | 3.10 |
| CNN-LSTM | 1.11 | 1.74 | 1.42 |
| GCN-LSTM | 1.58 | 2.68 | 1.88 |
| GRU | 1.59 | 2.68 | 2.08 |
| Proposed model | 0.19 | 0.33 | 0.26 |

## Trend summary
On the one-day horizon the Proposed model has the lowest error on every metric by a wide margin
(roughly 6–14× smaller than the best single baseline). Among baselines, CNN-LSTM is best,
LSTM worst; GCN-LSTM and GRU are nearly tied on MAE/MAPE. Supports C01. The §4.3 narrative's
stated one-day improvements (e.g., MAE +2.41 vs LSTM, +1.40 vs GRU, +0.92 vs CNN-LSTM, +1.39 vs
GCN-LSTM) are consistent with these labeled values.

**Discrepancy note**: §4 lists CNN-BiLSTM among the comparison baselines, but neither Figure 9 nor
Figure 10 includes a CNN-BiLSTM series, and the §4.3 delta narrative gives only four baseline
pairs. CNN-BiLSTM results are not reported anywhere in the paper (see
`logic/solution/constraints.md`, item 10).
