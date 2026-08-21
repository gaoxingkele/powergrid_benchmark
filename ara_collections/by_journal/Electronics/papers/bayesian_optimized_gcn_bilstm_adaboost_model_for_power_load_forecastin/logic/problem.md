# Problem Specification

## Observations

### O1: Single deep-learning forecasters have inherent limitations on long, high-dimensional load series
- **Statement**: Traditional AI/time-series methods suffer information loss on long input sequences and are prone to gradient issues and overfitting; a single intelligent forecasting model has inherent boundary constraints on engineering applicability.
- **Evidence**: §1 (Introduction), citing [6], [11], [14].
- **Implication**: Motivates hybrid/ensemble modeling that combines complementary inductive biases.

### O2: Meteorological factors are the dominant, non-stationary driver of load
- **Statement**: Complex, variable meteorological factors are key elements with the greatest impact on load prediction; frequent extreme-weather events induce non-stationary abrupt changes in load curves.
- **Evidence**: §1–§2 introduction, citing [5].
- **Implication**: Spatial correlations *among weather features* (not just temporal history) carry predictive signal, and robustness at abrupt changes matters.

### O3: Spatial + temporal extractors are individually validated but usually used in isolation
- **Statement**: GCN shows superiority for topological/spatial feature extraction and BiLSTM captures bidirectional temporal dependency; combinations (e.g., GCN-LSTM, CNN-LSTM) have been shown effective.
- **Evidence**: §1–§2, citing [12] (Graves BiLSTM), [13] (GCN-LSTM), [16] (CNN-LSTM+attention).
- **Implication**: A GCN→BiLSTM composition is a plausible base learner for spatiotemporal load features.

### O4: Existing models lack adaptive weighting and uncertainty quantification
- **Statement**: Existing load models (1) inadequately capture spatiotemporal characteristics, (2) lack adaptive mechanisms to dynamically weight base learners — causing robustness decline during load fluctuation — and (3) struggle to quantify the impact of model uncertainty on outcomes.
- **Evidence**: §1 (three enumerated limitations).
- **Implication**: Ensemble weighting + a principled uncertainty estimate are the missing pieces.

## Gaps

### G1: No adaptive dynamic weighting of spatiotemporal base learners for robustness at load mutations
- **Statement**: Prior hybrids fix or heuristically set combination weights and degrade at abrupt load transitions.
- **Caused by**: O1, O4.
- **Existing attempts**: Combined forecasting [15]; metaheuristic weight search (GA/PSO) [17].
- **Why they fail**: Static or globally uniform re-weighting does not concentrate capacity on hard/mutation samples and ignores per-learner reliability.

### G2: Model/data uncertainty is not quantified nor fed back into the ensemble
- **Statement**: Point forecasts give no reliability signal and no mechanism to discount unstable learners.
- **Caused by**: O4.
- **Existing attempts**: Bayesian optimization for hyperparameters [25]; MC Dropout as Bayesian approximation [26].
- **Why they fail**: Used for tuning or standalone uncertainty, not integrated as a per-learner weight modifier inside a boosting ensemble.

### G3: Graph structure for weather-load GCNs is often built by similarity/learned/MI methods that overfit or hallucinate edges
- **Statement**: The choice of adjacency-construction rule strongly affects the GCN's spatial signal, but common choices introduce spurious edges or need heavy training.
- **Caused by**: O2, O3.
- **Existing attempts**: KNN graphs [28], learned graphs [29], mutual-information graphs [30].
- **Why they fail**: KNN uses raw numerical similarity (spurious edges); learned graphs need large data and overfit; MI is sensitive to distribution/sample size.

## Key Insight
- **Insight**: Compose a GCN-BiLSTM spatiotemporal *base learner*, ensemble ten copies with a modified AdaBoost that only up-weights hard (error > 0.3) samples, and use Monte Carlo Dropout to (a) prevent overfitting during training and (b) produce a per-learner predictive variance that attenuates the ensemble weight of unstable learners — so accuracy and robustness at abrupt load changes improve jointly, and a calibrated 95% interval falls out for free.
- **Derived from**: O2, O3, O4.
- **Enables**: A single pipeline delivering point forecast + uncertainty band + robustness at turning points for dispatch decisions.

## Assumptions
- A1: A Spearman |ρ| ≥ 0.8 threshold identifies "physically real" monotonic dependencies between weather features and yields a static adjacency good for the whole year.
- A2: Predictive variance from MC Dropout (100 samples) is a valid proxy for a weak learner's reliability.
- A3: An absolute per-sample error threshold of 0.3 (on normalized scale) separates "hard/mutation" samples from noise; the paper notes it must be tuned per application.
- A4: Ten weak learners is a sufficient ensemble size for the accuracy/robustness/runtime trade-off.
- A5: The regional 2018 hourly dataset is representative of the deployment distribution.
