# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions
- Short-horizon (next-timestamp) hourly load forecasting only; multi-step / long-horizon forecasting not evaluated.
- Five regional PJM-style hourly datasets (AEP, COMED, DAYTON, DEOK, DOM) for the quantitative tables; three more (EKPC, NI, PJM_Load) appear only in the qualitative overlay (Figure 9).
- History-only inputs in the reported experiments: although temperature and price are listed as dataset features (Table 1), the reported forecasts and the discussion treat weather/price as *future* enrichment, not used in the current runs.
- The intelligent control strategy is evaluated in simulation, not on real hardware.

## Assumptions
- Min–max normalisation to [0,1] is appropriate and applied per feature.
- MSE (Eq. 16) and MAPE (Eq. 17) adequately capture forecast quality for load-management decisions.
- The simulation's ESS/DR/DER dynamics are representative enough for the reported peak-load and voltage-fluctuation improvements to transfer qualitatively.

## Known limitations
- **Generalisation caveat (stated by authors)**: the proposed LSTM-GRU is "optimized for global annual energy consumption" and "may not fully represent global energy consumption patterns despite utilizing diverse datasets" (Table 7, §4.3).
- **Claimed enhancements not formalised**: the "modified" LSTM cell-state update (Eq. 3) is algebraically identical to the standard update (Eq. 12), and the "modified" GRU hidden-state update (Eq. 4) is identical to the standard update (Eq. 8). The prose-described attention mechanism (LSTM) and dynamic/context-aware gating (GRU) are never given equations, hyperparameters, or code. The mechanistic novelty is therefore unverifiable from the paper.
- **Metric-definition irregularities**: the printed MSE (Eq. 16) divides squared error by $A_i$, and the printed MAPE (Eq. 17) omits the absolute value and the $1/n$ averaging, both departing from the definitions described in the surrounding text.
- **Undefined resilience score**: Figure 10 plots a "grid resilience score" per model per dataset, but the score's construction is never defined, so C05's ranking inversion cannot be causally attributed.
- **No training details**: learning rate, hidden dimensions, number of hidden layers, dropout rate, epochs, batch size, sequence length, train/validation/test split sizes, and hardware are all unspecified.
- **No statistical testing**: the small GRU-vs-LSTM differences are reported without variance, confidence intervals, or significance tests; runs appear single-shot.
- **Inconsistent headline figures**: §4.3 reports ~10% average peak-load reduction and a 4–7.5%→3–5% voltage narrowing, while the Conclusions state "up to 15%" operational-cost reduction and "~20%" grid-stability improvement; the derivation linking these is not shown.
- **Data availability**: "The data will be made available on request"; no repository or code is released.
