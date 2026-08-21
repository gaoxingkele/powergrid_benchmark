# Table 3: Performance analysis of different historical load input lengths

- **Source**: Table 3, Section 3 (Experimental Parameter Settings), p11
- **Caption**: "Performance analysis of different historical load input lengths."
- **Screenshot**: table3.png (page 11; table appears at the top of the page)
- **Extraction type**: raw_table

| Input Length (days) | RMSE/MW | MAE/MW | MAPE/% |
|---------------------|---------|--------|--------|
| 1 | 321.198  | 277.1  | 0.974 |
| 2 | 405.693  | 338.9  | 1.130 |
| 3 | 512.023  | 425.6  | 1.536 |
| 4 | 1310.602 | 1005.8 | 4.520 |

**Notes**: Input length = number of prior days of same-hour historical load. Length 1 (previous day)
best; error worsens monotonically, with a large jump at length 4. Per §3, the 1-day MAPE is lower
than the others by 0.156%, 0.562%, and 3.564% respectively. Supports C05 (E03).
</content>
