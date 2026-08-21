# Table 2: Comparison of different optimizers

- **Source**: Table 2, Section 3 (Experimental Parameter Settings), p10
- **Caption**: "Comparison of different optimizers."
- **Screenshot**: table2.png (page 10; table appears in the lower half of the page)
- **Extraction type**: raw_table

| Optimizer | RMSE/MW | MAE/MW | MAPE/% |
|-----------|---------|--------|--------|
| SGD     | 523.866 | 423.7 | 1.493 |
| RMSprop | 335.207 | 287.5 | 1.102 |
| Nadam   | 327.914 | 280.1 | 1.038 |
| Adam    | 321.198 | 266.4 | 0.974 |

**Notes**: Adam best on all three metrics. Per §3: Adam improves MAPE by 0.519% vs SGD; Nadam's MAPE
is 6.2% higher than Adam; RMSprop showed faster initial convergence but weaker final accuracy on
coupled temporal-meteorological features. Supports C04 (E02).
</content>
