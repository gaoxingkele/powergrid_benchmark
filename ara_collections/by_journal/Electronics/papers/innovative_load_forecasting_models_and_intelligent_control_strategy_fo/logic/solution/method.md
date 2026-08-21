# Method — Forecasting Models + Intelligent Control Strategy

The method has two coupled parts: (A) two enhanced recurrent forecasting models (LSTM, GRU) that predict next-step hourly load, and (B) an intelligent control strategy (ICS) that dispatches grid assets using those forecasts to level distributed load.

## A. Data pipeline
- **Features** (Table 1): date/time, temperature (°C), load (MW, dependent variable), price (Cents/kWh). Datasets collected from Kaggle (energy providers / government agencies).
- **Preprocessing**: per-feature min–max normalisation to [0,1] (Eqs. 1–2). Normalisation and min–max scaling are applied independently to each feature to place all features on a comparable scale and speed convergence.

## B. Forecasting models

### B.1 Enhanced LSTM
- Input layer receives numeric energy-consumption histories with timestamps.
- LSTM layers (cells with input/forget/output gates) maintain a cell state (long-term memory) and hidden state (network memory).
- Fully connected layer → ReLU non-linearity → dropout (overfitting prevention) → output layer producing next-timestamp load.
- **Standard forward pass** (Eqs. 9–14): input gate $i_t=\sigma(W_i x_t+U_i h_{t-1})$; forget gate $f_t=\sigma(W_f x_t+U_f h_{t-1})$; candidate $\tilde{C}_t=\tanh(W_C x_t+U h_{t-1})$; cell update $C_t=f_t\odot C_{t-1}+i_t\odot\tilde{C}_t$ (Eq. 12); output gate $o_t=\sigma(W_o x_t+U_o h_{t-1})$; hidden $h_t=o_t\odot\tanh(C_t)$.
- **Claimed enhancement**: an added *attention mechanism* letting the network focus on the most relevant parts of the input sequence, and a "modification" to the cell-state update printed as Eq. 3: $C_t=f_t\odot C_{t-1}+i_t\odot\tilde{C}_t$. (Eq. 3 is identical to standard Eq. 12; no attention equations are given — see constraints.md.)

### B.2 Enhanced GRU
- Same input→layers→FC→ReLU→dropout→output structure, but GRU cells have only an update gate and a reset gate and a single hidden state.
- **Standard forward pass** (Eqs. 5–8): update gate $z_t=\sigma(W_z x_t+U_z h_{t-1})$; reset gate $r_t=\sigma(W_r x_t+U_r h_{t-1})$; candidate $\tilde{h}_t=\tanh(W_h x_t+r_t\odot(U_h h_{t-1}))$; hidden update $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde{h}_t$ (Eq. 8).
- **Claimed enhancement**: a *dynamic gating mechanism* that adjusts the importance of input features based on the current model state, and a "modification" to the hidden-state update printed as Eq. 4: $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde{h}_t$. (Eq. 4 is identical to standard Eq. 8 — see constraints.md.)

### B.3 Training / prediction loop (§3.3.2)
1. Feed historical consumption sequence; forward pass updates internal states each timestep.
2. Output layer estimates next-timestamp load.
3. Loss = difference between predicted and actual consumption; optimisation objective $J=\sum_{t=1}^{T}(L_t-\hat{L}_t)^2$ (Eq. 15).
4. Optimise via gradient descent + backpropagation; iterate.
5. Validate on held-out data; quantify with MSE (Eq. 16) and MAPE (Eq. 17).

## C. Intelligent Control Strategy (ICS) for load levelling (§3.3.3, §3.5)
Four components:
1. **Real-time load forecasting** — enhanced LSTM/GRU provide proactive predictions of future demand.
2. **Dynamic resource allocation** — adjust DER output (solar panels, wind turbines) to match predicted demand across grid regions.
3. **Advanced load balancing** — distribute load evenly, respecting DER capacity/availability and predicted load patterns.
4. **Grid-stability maintenance** — monitor voltage levels and frequency deviations in real time and adjust distribution to prevent instability/outages.

Load-levelling mechanisms:
- **Peak-load minimisation** — ESSs absorb excess energy in low-demand periods and discharge during peaks; DR shifts non-essential loads to off-peak; the strategy continuously monitors grid conditions and re-allocates.
- **Grid-stability improvement** — keep voltage within a narrow band, minimise frequency deviations, balance supply/demand via DER dispatch.

The novelty claimed over conventional ESS/DR is the *integration with predictive models*, enabling proactive real-time adjustment rather than reactive control.
