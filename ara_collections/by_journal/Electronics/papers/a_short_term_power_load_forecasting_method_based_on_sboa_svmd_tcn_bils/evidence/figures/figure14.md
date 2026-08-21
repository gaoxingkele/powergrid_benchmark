# Figure 14: Error distribution of each model

- **Source**: Figure 14, Section 5.7, p. 20 (body of page, below Table 8)
- **Caption**: "Error distribution of each model. (a) Spring; (b) Summer; (c) Autumn; (d) Winter."
- **Screenshot**: figure14.png (same page as Table 8; Figure 14 is the four-panel histogram grid)
- **Figure type**: quantitative_plot
- **Extraction method**: visual_description
- **Reading confidence**: low

- **Plot kind**: histogram (relative-error distribution; 4 season panels, each with 4 stacked sub-histograms for LSTM, ELM, BiLSTM, TCN-BiLSTM)
- **Axes**: X = Relative error (MW), linear, ranges differ per model/season (e.g. spring ≈ −200 to 1200 MW). Y = Rate (%), linear, ≈0–15%.

## Trend summary
Points were not individually readable (reading confidence low). Qualitatively: in spring and autumn the proposed TCN-BiLSTM concentrates its relative errors within ±200 MW, whereas LSTM/ELM/BiLSTM spread into the >200 MW range. In summer and winter all models' error distributions widen (performance declines), but the proposed model shows a markedly smaller proportion of high-error bins than the baselines. No exact frequencies extracted — see Table 8 for the numeric MAE/RMSE per season.
