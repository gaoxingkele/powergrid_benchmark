# Environment

- **Language/runtime**: Not specified in paper (Python implied by Keras). No version stated.
- **Framework**: Keras platform; LSTM training optimized with the **CuDNNLSTM** implementation
  (§5.2). No framework version stated.
- **Hardware**: Not specified in paper. CuDNNLSTM implies an NVIDIA GPU with cuDNN, but the GPU
  model, count, and memory are not reported.
- **Data sources**:
  - Actual measured smart-meter data from **Ireland** (§4.3, §5.2).
  - Decomposition analysis: data from **50 randomly selected users** (§5.1).
  - Prediction experiments: electricity consumption data from **50 users** (§5.2).
  - Sampling: hourly for next-hour prediction; daily for next-day prediction.
  - Daily-scale split: training set of **500 days**; sliding window of **180 days** (step 1) for the
    training set; **last 30 days** reserved as the test set (§5.2).
  - No dataset URL, license, or access instructions are given in the paper. (The description matches
    the commonly used Irish CER Smart Metering Project data, but the paper does not name or cite it.)
- **Key dependencies**: Keras (+ CuDNNLSTM / cuDNN). CEEMDAN and EMD/EEMD decomposition routines are
  described mathematically (§3) but no library is named. Versions: Not specified in paper.
- **Protocols**:
  - CEEMDAN noise: amplitude 0.1× the standard deviation of the original data; 200 white-noise sets.
  - Decomposition depth fixed at 8 IMFs (+ residual); endpoint effects handled by linearly extending
    extreme points; SD sifting criterion $0.1<SD<0.3$.
  - Sliding window 60 days, step 1; rear-of-window fixed-length segment extraction.
  - Forecast protocol: 48 historical IMF values → next IMF value (Table 2).
  - Training: mini-batch gradient descent; batch size 30; learning rate 0.005; dropout 0.5.
  - Metrics: RMSE (Eq. 20), MAE (Eq. 21), over 50 users.
- **Random seeds**: Not specified in paper.
- **Code availability**: No repository released. Data Availability Statement in the paper: "Not
  applicable." This ARA therefore documents the method from the paper; no `src/execution/` code
  files are provided because the paper prints no pseudocode or source code (only prose steps,
  equations, and diagrams).
