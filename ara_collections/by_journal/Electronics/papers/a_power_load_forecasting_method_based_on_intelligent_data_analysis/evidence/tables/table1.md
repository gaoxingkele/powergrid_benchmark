# Table 1 - The comparison of related works

**Source**: Table 1, §1 (p.2)
**Caption**: "The comparison of related works. ("√" if the solution satisfies the property, "×" if not)."
**Screenshot**: table1.png
**Extraction type**: raw_table
**Location on page**: mid-page, below the paragraph ending "...is shown in Table 1."

| Ref. | Focus | Main Contribution | Adaptive Data | Signal Frequency Overlap | Vanishing Gradient |
|------|-------|-------------------|---------------|--------------------------|--------------------|
| [8] | Residential electricity load forecasting | The study tested a framework based on LSTM-RNN to predict the expected future load. | × | × | √ |
| [9] | Predicting activity signal frequencies | A deep learning model called EMD-LSTM-CNN, based on LSTM, CNN, and EMD methods, is proposed to predict frequency signals. | √ | × | √ |
| [10] | High-speed nonlinear circuit prediction | A BN-RNN method is proposed for predicting circuit. | × | × | √ |
| Our work | Residential electricity load forecasting | A user electricity consumption forecasting method is proposed, using CEEMDAN and LSTM network. | √ | √ | √ |

**Note**: Only "Our work" (CEEMDAN-LSTM) satisfies all three properties, in particular Signal
Frequency Overlap (mode-mixing handling), which the EMD-LSTM-CNN baseline [9] does not. Supports
C02 (adaptive-noise decomposition addresses signal-frequency overlap/mode mixing).
