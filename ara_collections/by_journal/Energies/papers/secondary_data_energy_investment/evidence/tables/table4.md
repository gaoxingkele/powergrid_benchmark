# Table 4: Effect of Alternative Weighting Assumptions on Country Prioritization

- **Source**: Energies 2026, 19, 3243, page 16
- **Caption**: Effect of alternative weighting assumptions on country prioritization.
- **Screenshot**: `table4.png`
- **Extraction type**: raw_table
- **Data table**:

| Configuration | Empirical Weighting Logic | Spearman with Baseline | Top-5 Overlap | Top-10 Overlap | Top-Ranked Countries |
|--------------|--------------------------|----------------------|--------------|---------------|-------------------|
| Equal-weight baseline | All 18 criteria receive identical weights. | 1.000 | 5/5 | 10/10 | Norway; Denmark; United States |
| Entropy objective weighting | Weights reflect information diversity and dispersion in the normalized matrix. | 0.892 | 3/5 | 8/10 | United States; Norway; Canada |
| CRITIC objective weighting | Weights reflect criterion variability and conflict with other criteria. | 0.986 | 5/5 | 8/10 | Norway; Denmark; Switzerland |
| Hybrid objective weighting | Entropy and CRITIC weights are averaged to form a balanced objective benchmark. | 0.974 | 4/5 | 9/10 | United States; Norway; Denmark |
