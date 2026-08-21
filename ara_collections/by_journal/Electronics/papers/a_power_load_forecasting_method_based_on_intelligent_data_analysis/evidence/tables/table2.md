# Table 2 - LSTM input settings

**Source**: Table 2, §5.2 (p.12)
**Caption**: "LSTM input settings."
**Screenshot**: table2.png
**Extraction type**: raw_table
**Location on page**: lower third of the page, below the paragraph on input configuration.

| Predicted Time Period Length | Sampling Interval | Single Input Sequence Length | Length of Input Data |
|------------------------------|-------------------|------------------------------|----------------------|
| One hour | 1 h | 48 | 2 d |
| One day | 24 h | 48 | 24 d |

**Note**: Both settings use 48 historical IMF component values to predict the next value; the
input-data span differs (2 days for hourly, 24 days for daily). Supports C01 (single-step protocol).
