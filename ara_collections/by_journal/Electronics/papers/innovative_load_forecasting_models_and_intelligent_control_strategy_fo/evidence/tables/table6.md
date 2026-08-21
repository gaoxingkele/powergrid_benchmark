# Table 6 - Comparison of LSTM and GRU

**Source**: Table 6, §4.2(c) Discussion (page 17)
**Caption**: "Comparison of LSTM and GRU."
**Screenshot**: table6.png
**Extraction type**: raw_table

| Test Dataset | LSTM Model MSE | GRU Model MSE | LSTM Model MAPE | GRU Model MAPE |
|--------------|----------------|---------------|-----------------|----------------|
| AEP_hourly.csv | 162.435 | 138.292 | 0.546% | 0.501% |
| COMED_hourly.csv | 58.772 | 49.846 | 0.667% | 0.618% |
| DAYTON_hourly.csv | 29.821 | 26.612 | 0.459% | 0.401% |
| DEOK_hourly.csv | 93.464 | 79.110 | 0.621% | 0.568% |
| DOM_hourly.csv | 23.962 | 22.988 | 0.418% | 0.391% |

**Verbatim finding (page 17)**: "In all the cases, it is observed that the performance of the GRU model is superior to that of the LSTM model as per the analysis based on the MSE and MAPE."

**Verbatim finding (page 18)**: "the results of the GRU model are very close to those obtained by the LSTM model, with only slight changes in the MSE and MAPE" ... "both models can handle dynamic load forecasting tasks, and selecting one over the other may depend on needs and computing limitations".

Note: consolidates Tables 2–5. GRU has lower MSE and lower MAPE than LSTM on all five datasets, but margins are small (e.g. DOM MAPE 0.418% vs 0.391%). This juxtaposes with Figure 10, where LSTM scores higher on grid resilience (see C05).
