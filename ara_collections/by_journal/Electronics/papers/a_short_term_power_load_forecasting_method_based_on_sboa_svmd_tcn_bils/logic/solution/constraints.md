# Constraints

## Boundary conditions
- Task: day-ahead short-term load forecasting; each day's forecast uses the previous day's data; daily sequences of 96 points (15-min sampling).
- Data: single region in Belgium, calendar year 2018 (35,040 points). Generalization to other regions/years is untested.
- Decomposition yields exactly four IMFs at the optimized settings on this data; the count is an outcome, not a guarantee for other data.
- SBOA optimizes a single scalar (SVMD maxAlpha); other SVMD parameters fixed to empirical values (Table 1).
- Optimizer budget: population 30, 60 iterations (also for SSA/GWO in the comparison).

## Assumptions
- A1: Permutation entropy is a valid proxy for component predictability (lower entropy ⇒ lower forecast error). The optimizer minimizes entropy, not forecast error directly.
- A2: Four IMFs adequately represent the load at the optimized compactness.
- A3: The quartile outlier method + interpolation upsampling adequately clean missing/abnormal data.
- A4: Min–max normalization to [0,1] is appropriate; predictions are denormalized and daily-aggregated for evaluation.
- A5: Offline-training / online-prediction deployment is acceptable for the day-ahead use case.

## Known limitations
- Single dataset / single region / single year — no cross-dataset or cross-region validation; external validity unquantified.
- Only two EMD-family decomposition baselines (CEEMDAN, ICEEMDAN) and two rival optimizers (SSA, GWO).
- Seasonal and peak-period results use one representative day per season/window — small evaluation samples.
- Figure 10 plots SBOA/SSA on one y-axis and GWO on a separate finer y-axis, so absolute optimizer gaps are qualitative, not directly comparable.
- Mode mixing is asserted as the mechanism behind EMD-family baselines' higher error but is not independently measured for those baselines.
- No formal complexity analysis, no uncertainty/confidence intervals, no statistical significance testing of the reported deltas.
- Dataset available only on request from the authors; no released code — reproduction depends on re-implementation from the paper.
- The "R²/%" table headers label the metric as a percentage but the tabulated values are the raw R² fraction (0–1).
