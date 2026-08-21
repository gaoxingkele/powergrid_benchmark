# Table 5 - Comparison of MAPE values of GRU

**Source**: Table 5, §4.2(b) (page 16, top)
**Caption**: "Comparison of MAPE values of GRU."
**Screenshot**: table5.png
**Extraction type**: raw_table

| Test Dataset | GRU Model |
|--------------|-----------|
| AEP_hourly.csv | 0.501% |
| COMED_hourly.csv | 0.618% |
| DAYTON_hourly.csv | 0.401% |
| DEOK_hourly.csv | 0.568% |
| DOM_hourly.csv | 0.391% |

Note: values are MAPE (%) (Eq. 17). GRU MAPE is lower than LSTM MAPE (Table 3) on every dataset; range 0.391% (DOM) to 0.618% (COMED).
