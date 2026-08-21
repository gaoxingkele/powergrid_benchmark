# Constraints

## Assumptions

### A1 — Temporal Pattern Generalization
The model assumes that the statistical properties and temporal patterns present in the training data (commercial complex power load, January–December 2016) generalize to future load behavior. This is a standard supervised learning assumption for time series forecasting but introduces vulnerability to:

- **Non-stationary distribution shifts:** Policy changes (e.g., new energy efficiency regulations), infrastructure modifications (e.g., building expansion or renovation), or behavioral changes (e.g., occupancy pattern shifts) that alter the underlying load generation process.
- **Out-of-distribution events:** Extreme weather conditions, public health emergencies, or economic disruptions that create load patterns outside the training distribution.
- **Temporal autocorrelation decay:** The predictive value of historical patterns diminishes as the forecasting horizon extends beyond the seasonal cycles captured in the training window.

### A2 — Bidirectional Context Validity
The BiLSTM component assumes that access to both past and future context within each training window provides beneficial information. This is valid for:

- **Offline training:** Full sequence windows are available for parameter optimization.
- **Batch evaluation:** Test sequences are processed in complete windows.

This assumption does NOT hold for:

- **Online / real-time forecasting:** Strictly causal forecasting requires only past information. Using BiLSTM in such settings would require architectural modification (replacing with unidirectional LSTM or using masked bidirectional processing).

### A3 — Complementary Multi-Source Features
The feature set (historical load, temperature, wind speed) assumes each source contributes complementary predictive information and that all sources are available at consistent temporal resolution (0.5h intervals). This bounds the approach to:

- **Sensor-equipped environments:** Locations with adequate meteorological measurement infrastructure.
- **Data quality requirements:** Missing or corrupted sensor readings would require imputation or degrade performance.
- **Fixed feature set:** The model does not adapt to varying feature availability across deployment sites without retraining or fine-tuning.

## Limitations

### L1 — Single-Site Data
The model is evaluated on a single commercial complex dataset. Generalizability to other building types (residential, industrial, institutional), climate zones, or geographic regions is not established. Factors that may affect transferability include:

- Load profile shape differences across building types
- Different weather-load sensitivity patterns
- Varying data granularity and availability

### L2 — Linear Interpolation for Missing Data
The paper uses linear interpolation to handle missing values. While straightforward, this approach:

- Cannot capture complex non-linear dependencies in missing segments
- May introduce bias, particularly for consecutive missing periods
- Does not model the uncertainty introduced by imputation
- May mask sensor degradation or data quality issues

### L3 — No Domain Adaptation or Transfer Learning
The model is trained and evaluated on a single dataset without cross-domain validation. This limits understanding of:

- How model performance degrades when applied to unseen building types or regions
- Whether the DAF module's learned adaptive weights transfer meaningfully across domains
- The amount of fine-tuning data needed for acceptable transfer performance

### L4 — O(T^2) Attention Complexity
The Transformer component retains standard self-attention's quadratic complexity O(T^2) with respect to sequence length T. While the local enhanced mask reduces effective attention range, the theoretical complexity remains quadratic. This may become a practical constraint for:

- Very long sequence windows (e.g., multi-week forecasting at high resolution)
- Resource-constrained edge deployment scenarios
- Real-time applications requiring sub-millisecond inference

### L5 — Single-Step Forecasting Focus
The paper evaluates single-step prediction at 0.5h resolution. Multi-step forecasting performance (e.g., 24-hour ahead predictions) is not explicitly evaluated. Error accumulation patterns over extended horizons remain uncharacterized, limiting the assessment of model suitability for operational planning tasks beyond very short-term forecasting.
