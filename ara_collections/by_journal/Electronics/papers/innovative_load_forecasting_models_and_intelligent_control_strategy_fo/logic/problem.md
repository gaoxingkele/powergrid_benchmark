# Problem Specification

## Observations

### O1: Short-term load forecasting is the core enabler of smart-grid operation
- **Statement**: Accurate short-term load forecasting is required to manage electricity distribution efficiently in smart grids; AMI data can improve forecasting accuracy but raises data-quality, privacy, and computational-complexity issues.
- **Evidence**: Introduction and Related Work (§1, §2), citations [1], [2], [8].
- **Implication**: A forecasting method must be both accurate and deployable on heterogeneous, high-volume metering data.

### O2: Recurrent networks (LSTM/GRU) capture temporal load structure
- **Statement**: LSTM and GRU networks are widely used for time-series/power-consumption forecasting because their gating mechanisms model long-range temporal dependencies in sequential data.
- **Evidence**: §1, §3 (Materials and Methods); background references [4], [5], [7], [16].
- **Implication**: These architectures are natural candidates for dynamic load prediction.

### O3: Conventional load-levelling tools lack predictive foresight
- **Statement**: Energy-storage systems (ESSs) and demand–response (DR) are effective for peak shaving and load balancing, but their traditional implementation lacks the predictive foresight for optimal operation.
- **Evidence**: §2, references [21], [22].
- **Implication**: Coupling accurate forecasts to ESS/DR/DER dispatch could improve peak shaving and stability over reactive control.

### O4: Forecast errors propagate into operational decisions
- **Statement**: When predicted load deviates from actual demand, resource allocation degrades — under-forecasting risks blackouts/brownouts, over-forecasting causes economic and environmental waste.
- **Evidence**: §4.3 Discussion.
- **Implication**: Forecast accuracy has direct grid-reliability and economic consequences, motivating careful error measurement (MSE, MAPE).

## Gaps

### G1: Insufficient integration of forecasting with control in resilient grids
- **Statement**: There is insufficient joint treatment of accurate load forecasting AND intelligent control strategies for resilient smart grids; traditional forecasting methods fall short under ever-changing consumption patterns.
- **Caused by**: O1, O3, O4.
- **Existing attempts**: AMI-data models, deep networks with metaheuristics, cloud platforms, adaptive forecasting (refs [8], [11], [12], [20]).
- **Why they fail**: Resource-intensive computation, infrastructure demands, limited generalisation, and no tight forecast-to-control loop.

### G2: Model-selection guidance for LSTM vs GRU under diverse consumption profiles
- **Statement**: It is unclear whether LSTM or GRU should be preferred across heterogeneous regional load datasets, or on what basis (accuracy vs compute) to choose.
- **Caused by**: O2.
- **Existing attempts**: Prior single-model studies of LSTM or GRU in isolation.
- **Why they fail**: They rarely compare both architectures head-to-head on the same diverse dataset collection with consistent metrics.

## Key Insight
- **Insight**: A forecast-in-the-loop control strategy — using the trained LSTM/GRU predictions to proactively dispatch ESS, DR, and DERs — can flatten the peak load curve and stabilise voltage more effectively than reactive ESS/DR use alone, while a head-to-head LSTM/GRU comparison on diverse datasets reveals whether architecture choice can be decoupled from accuracy.
- **Derived from**: O2, O3, O4.
- **Enables**: The proposed intelligent control strategy (ICS) and the comparative forecasting study.

## Assumptions
- A1: Historical hourly consumption is sufficiently informative to forecast the next-step load (no exogenous weather/price inputs are used in the reported experiments, though the paper suggests adding them later).
- A2: Min–max normalisation to a common scale is an appropriate preprocessing for these features.
- A3: MSE and MAPE adequately characterise forecasting quality for load-management decisions.
- A4: The control-strategy simulation environment (ESS/DR/DER dynamics) is representative enough for the reported peak-load and voltage-fluctuation improvements to be meaningful.
