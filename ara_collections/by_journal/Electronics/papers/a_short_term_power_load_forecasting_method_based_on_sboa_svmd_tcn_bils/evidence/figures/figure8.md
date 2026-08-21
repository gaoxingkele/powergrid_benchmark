# Figure 8: Prediction model flowchart

- **Source**: Figure 8, Section 4 (Combined Prediction Model), p. 12
- **Caption**: "Prediction model flowchart."
- **Screenshot**: figure8.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (top→bottom): Start → Original data → SVMD decomposition optimized by SBOA → four parallel branches IMF1, IMF2, IMF3, IMF4 → each into its own TCN-BiLSTM → Hybrid computation → Output predicted values → End.
- **Connections**: One TCN-BiLSTM per IMF (four parallel forecasters); their outputs merge at "Hybrid computation" (summation/reconstruction) to produce the final forecast.
- **What it conveys**: The end-to-end pipeline — SBOA-optimized SVMD splits the load into 4 IMFs, each IMF is forecast independently by a TCN-BiLSTM, and the component forecasts are recombined. Confirms exactly four IMFs / four sub-models.
