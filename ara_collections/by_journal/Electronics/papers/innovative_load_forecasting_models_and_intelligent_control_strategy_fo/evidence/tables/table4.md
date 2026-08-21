# Table 4 - Comparison of MSE values of GRU

**Source**: Table 4, §4.2(a) (page 15)
**Caption**: "Comparison of MSE values of GRU."
**Screenshot**: table4.png
**Extraction type**: raw_table

| Test Dataset | GRU Model |
|--------------|-----------|
| AEP_hourly.csv | 138.292 |
| COMED_hourly.csv | 49.846 |
| DAYTON_hourly.csv | 26.612 |
| DEOK_hourly.csv | 79.110 |
| DOM_hourly.csv | 22.988 |

Note: values are MSE (Eq. 16). GRU MSE is lower than LSTM MSE (Table 2) on every dataset; range 22.988 (DOM) to 138.292 (AEP).
