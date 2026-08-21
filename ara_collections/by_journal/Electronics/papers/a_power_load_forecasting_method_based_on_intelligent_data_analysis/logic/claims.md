# Claims

## C01: Separating a non-stationary load signal into structured and stochastic parts before forecasting reduces error relative to forecasting the raw signal
- **Statement**: When a nonlinear, non-stationary residential load series is decomposed into trend, periodic, and random sub-components and each is forecast separately before recombination, the reconstructed forecast is more accurate than forecasting the undecomposed signal with the same recurrent network — because isolating high-frequency stochastic content from the more predictable periodic and trend structure lets the learner fit each regime without one corrupting the other.
- **Conditions**: Holds for residential smart-meter load that is genuinely multi-scale (stochastic + periodic + trend), decomposed with an adaptive-noise ensemble method and forecast with per-component LSTM sub-models; demonstrated at hourly and daily granularity on 50 Irish users. Untested boundary: non-residential or non-load signals, other decomposition depths, and horizons beyond one step.
- **Sources**: [no load-bearing numbers in Statement; supporting values in Evidence basis]
- **Status**: supported
- **Falsification criteria**: On comparable non-stationary load data, a decomposition-then-recombine pipeline shows no RMSE/MAE reduction (or higher error) than the identical LSTM applied directly to the raw series.
- **Proof**: [E01, E02]
- **Evidence basis**: In both the hourly comparison (evidence/tables/table3.md) and the daily comparison (evidence/tables/table4.md), the decomposition-based model (CEEMDAN-LSTM) reports lower RMSE and MAE than the undecomposed LSTM baseline; the paper attributes this to decomposition distributing the signal's information among several relatively stable components without losing essential information (§5.2).
- **Tags**: signal-decomposition, load-forecasting, non-stationary, LSTM

## C02: Adaptive-noise ensemble decomposition separates load components more cleanly for forecasting than plain EMD, by suppressing mode mixing
- **Statement**: Replacing a plain EMD front-end with an adaptive-noise complete ensemble decomposition (which injects controlled white noise at each stage) yields components that preserve physical meaning better, and a forecaster built on those components achieves lower error than one built on EMD components — the mechanism being suppression of mode mixing, the coupling by which EMD assigns content from different time scales to the same IMF (or splits one scale across IMFs).
- **Conditions**: Holds when the front-end difference is EMD vs CEEMDAN with the same downstream LSTM and evaluation; shown on residential load at hourly and daily scales. Boundary: the paper does not vary the noise amplitude or ensemble size to map where the advantage disappears, and does not test EEMD as an intermediate front-end in the prediction comparison.
- **Sources**: [no load-bearing numbers in Statement; supporting values in Evidence basis]
- **Status**: supported
- **Falsification criteria**: An EMD-based decomposition front-end matches or beats the CEEMDAN front-end on the same data and network, or the CEEMDAN components exhibit the same mode-mixing artifacts as EMD components.
- **Proof**: [E01, E02]
- **Evidence basis**: CEEMDAN-LSTM reports lower RMSE and MAE than EMD-LSTM in both evidence/tables/table3.md (hourly) and evidence/tables/table4.md (daily); §3.2 establishes the mode-mixing failure mode of EMD and CEEMDAN's near-zero-reconstruction-error rationale.
- **Dependencies**: C01
- **Tags**: CEEMDAN, EMD, mode-mixing, ablation

## C03: The decomposition front-end improves accuracy and stability jointly, indicating a representational gain rather than a metric-specific tradeoff
- **Statement**: The advantage of the decomposition-based forecaster appears simultaneously in an error-magnitude metric and an error-dispersion metric and is preserved across two different temporal aggregations, which indicates the improvement comes from a better signal representation rather than from trading one error characteristic against another or from tuning to a single evaluation setting.
- **Conditions**: Holds for the two metrics used (MAE for accuracy, RMSE for stability) across hourly and daily prediction on the same 50-user cohort; the ordering among all four models is the comparison basis. Boundary: only two metrics and two time scales are examined; no statistical significance test across users is reported.
- **Sources**: [no load-bearing numbers in Statement; supporting values in Evidence basis]
- **Status**: supported
- **Falsification criteria**: The decomposition model wins on one metric but loses on the other, or wins at one time scale but loses at the other, on the same cohort.
- **Proof**: [E01, E02]
- **Evidence basis**: Across evidence/tables/table3.md and table4.md the model ordering (CEEMDAN-LSTM best, then EMD-LSTM, LSTM, RNN varying) holds for both RMSE and MAE at both hourly and daily scales; the qualitative overlays in evidence/figures/figure9.md and figure10.md show the CEEMDAN-LSTM trace tracking the actual load.
- **Dependencies**: C01, C02
- **Tags**: robustness, RMSE, MAE, evaluation

## C04: Decomposition can only separate trend from periodicity if the analysis window spans multiple periodic cycles
- **Statement**: For window-based decomposition of a load series to recover distinct trend and periodic components, the window must be large enough to encompass the periodic and trend scales of the signal; sizing the window to the neural network's input-sequence length instead conflates trend and periodic content, so window sizing must be driven by the decomposition objective rather than by the forecaster's input length.
- **Conditions**: Stated and applied for residential load with a 60-day window moved at step size 1, extracting a fixed-length segment from the rear of the window. The small-window failure mode is asserted as design rationale and demonstrated only indirectly (the large window does produce clean trend/periodic components); it is not run as a controlled small-window ablation.
- **Sources**: 60-day window ← evidence/figures/figure6.md / §5.1 «The sliding window encompasses a 60-day data period, and the window is moved by a uniform step size of 1» [input]
- **Status**: supported
- **Falsification criteria**: A window sized to the network input length (or otherwise too short to span the periodic/trend scale) separates trend from periodic components as cleanly as the large window on the same data.
- **Proof**: [E03]
- **Evidence basis**: §3.3 and §5.1 argue the window must be sufficiently large to encompass periodic and trend components; the CEEMDAN decomposition under the 60-day window produces components with clearly distinct trend/periodic/stochastic roles (evidence/figures/figure7.md), i.e. the large window achieves the intended separation.
- **Dependencies**: C05
- **Tags**: sliding-window, decomposition, endpoint-effect, design-rationale

## C05: CEEMDAN components of residential load map onto distinct physical roles, enabling interpretable per-component modeling
- **Statement**: Adaptive-noise ensemble decomposition of a residential load series produces an ordered set of components whose frequency bands align with distinct physical roles — the highest-frequency components behave as stochastic user behavior, mid-frequency components carry the load's periodicity, and the lowest-frequency component with the residual carry its trend — so each component can be modeled by a dedicated forecaster matched to its regularity.
- **Conditions**: Demonstrated on one representative Irish user's hourly load decomposed into 8 IMFs plus a residual (RES) with adaptive noise at 0.1× the data's standard deviation and 200 noise realizations; the role assignment (which IMF indices are stochastic vs periodic vs trend) is specific to this signal and depth and is read qualitatively from the decomposition plots.
- **Sources**: 8 IMFs ← evidence/figures/figure7.md / §5.1 «the number of IMF components is set to 8» [input]; noise 0.1× std ← §5.1 «The white noise was added with an amplitude of 0.1 times the standard deviation of the original data» [input]; 200 noise sets ← §5.1 «a total of 200 sets of white noise was added in CEEMDAN» [input]
- **Status**: supported
- **Falsification criteria**: The decomposed components show no consistent frequency-to-role separation (e.g. periodicity spread arbitrarily across all IMFs, or no monotonic frequency ordering), so that per-component modeling has no principled basis.
- **Proof**: [E03]
- **Evidence basis**: In evidence/figures/figure7.md, IMF1–IMF3 are high-frequency with no apparent regular pattern (stochastic), IMF4–IMF7 show significant periodicity (periodic), and IMF8 with RES show prominent trend characteristics (trend), matching the text of §5.1.
- **Tags**: interpretability, IMF, frequency-bands, decomposition
