# Table 1: Comparison of several commonly used activation functions

- **Source**: Table 1, Section 3 (Experimental Parameter Settings), p10
- **Caption**: "Comparison of several commonly used activation functions."
- **Screenshot**: table1.png (page 10; table appears in the upper-middle of the page)
- **Extraction type**: raw_table

| Activation Function | RMSE/MW | MAE/MW | MAPE/% |
|---------------------|---------|--------|--------|
| Sigmoid    | 393.250 | 315.6 | 1.155 |
| Tanh       | 449.462 | 362.8 | 1.273 |
| ReLU       | 651.879 | 543.2 | 2.218 |
| Leaky ReLU | 321.198 | 275.3 | 0.974 |

**Notes**: Leaky ReLU best on all three metrics; ReLU worst. Per §3, Leaky ReLU's MAPE is lower than
Sigmoid, Tanh, and ReLU by 0.181%, 0.299%, and 1.244% respectively. Supports C03 (E01).
</content>
