# Concepts

## Long Short-Term Memory (LSTM)
- **Notation**: gates $i_t$ (input), $f_t$ (forget), $o_t$ (output); states $C_t$ (cell), $h_t$ (hidden)
- **Definition**: A recurrent neural network cell with three gates and two states. Forward pass (paper Eqs. 9–14): $i_t=\sigma(W_i x_t + U_i h_{t-1})$, $f_t=\sigma(W_f x_t + U_f h_{t-1})$, candidate $\tilde{C}_t=\tanh(W_C x_t + U h_{t-1})$, cell update $C_t=f_t\odot C_{t-1}+i_t\odot\tilde{C}_t$, $o_t=\sigma(W_o x_t + U_o h_{t-1})$, hidden $h_t=o_t\odot\tanh(C_t)$. Used here for next-step hourly load forecasting.
- **Boundary conditions**: Suited to sequential data with long-range temporal correlations; the paper adds a ReLU-activated fully connected head and dropout.
- **Related concepts**: GRU, cell state, recurrent neural network, backpropagation

## Gated Recurrent Unit (GRU)
- **Notation**: gates $z_t$ (update), $r_t$ (reset); state $h_t$ (hidden)
- **Definition**: A streamlined recurrent cell with two gates and a single hidden state (paper Eqs. 5–8): $z_t=\sigma(W_z x_t + U_z h_{t-1})$, $r_t=\sigma(W_r x_t + U_r h_{t-1})$, candidate $\tilde{h}_t=\tanh(W_h x_t + r_t\odot(U_h h_{t-1}))$, hidden update $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde{h}_t$. An alternative to LSTM with fewer parameters and comparable performance.
- **Boundary conditions**: Same time-series forecasting regime as LSTM; no separate cell state.
- **Related concepts**: LSTM, update gate, reset gate, parameter efficiency

## Modified cell-state / hidden-state update (claimed enhancement)
- **Notation**: LSTM $C_t=f_t\odot C_{t-1}+i_t\odot\tilde{C}_t$ (Eq. 3); GRU $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde{h}_t$ (Eq. 4)
- **Definition**: The paper states it introduces a "modification" to the LSTM cell-state update and the GRU hidden-state update, described in prose as an added attention mechanism (LSTM) and a dynamic/context-aware gating mechanism (GRU) that reweights input features by current state.
- **Boundary conditions**: The printed "modified" equations (Eqs. 3, 4) are algebraically identical to the standard updates (Eqs. 12, 8); no attention/dynamic-gating equations are provided — see constraints.md.
- **Related concepts**: attention mechanism, dynamic gating, LSTM, GRU

## Intelligent Control Strategy (ICS)
- **Notation**: —
- **Definition**: A forecast-in-the-loop control scheme that dynamically allocates energy resources using real-time LSTM/GRU load forecasts. Components: (1) real-time forecasting; (2) dynamic resource allocation adjusting DER output to match predicted demand; (3) advanced load-balancing algorithms respecting DER capacity/availability; (4) grid-stability maintenance via voltage/frequency monitoring.
- **Boundary conditions**: Described qualitatively; simulated, not deployed. Peak shaving via ESS + DR; stability via DER dispatch.
- **Related concepts**: distributed load levelling, ESS, demand-response, DER, peak load shaving

## Distributed Load Levelling
- **Notation**: —
- **Definition**: Smoothing the grid load profile across time by shifting/absorbing energy so that peaks are reduced and troughs filled, distributed across grid assets (storage, controllable loads, distributed generation).
- **Boundary conditions**: In this paper achieved by forecast-driven ESS charging/discharging and DR load shifting.
- **Related concepts**: peak load shaving, ICS, ESS, demand-response

## Mean Squared Error (MSE)
- **Notation**: paper Eq. 16: $\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}\frac{(P_i-A_i)^2}{A_i}$
- **Definition**: Average of squared prediction errors used to assess forecasting accuracy; lower is better, 0 = perfect. (Note: the printed Eq. 16 divides the squared error by $A_i$, which departs from the textbook MSE definition; the text describes it as the standard mean of squared discrepancies.)
- **Boundary conditions**: Scale-dependent — grows with the absolute magnitude of the series (see C03).
- **Related concepts**: MAPE, optimization objective, regression error

## Mean Absolute Percentage Error (MAPE)
- **Notation**: paper Eq. 17: $\mathrm{MAPE}=\sum_{i=1}^{n}\frac{P_i-A_i}{A_i}\times 100$
- **Definition**: Average percentage deviation of predictions from actuals; scale-free, expressed as a percentage; lower is better. Paper refers to a symmetric MAPE. (Note: the printed Eq. 17 omits the absolute value and the $1/n$ averaging that the surrounding text describes.)
- **Boundary conditions**: Can be sensitive to outliers and to near-zero actuals; scale-free, enabling cross-dataset comparison.
- **Related concepts**: MSE, forecast accuracy, cross-dataset comparison

## Optimization objective for load prediction
- **Notation**: paper Eq. 15: $J=\sum_{t=1}^{T}(L_t-\hat{L}_t)^2$
- **Definition**: Minimise the sum of squared differences between actual load $L_t$ and predicted load $\hat{L}_t$ over horizon $T$, so predicted load closely matches actual and grid performance improves.
- **Boundary conditions**: Training/optimisation objective; horizon $T$ unspecified.
- **Related concepts**: MSE, backpropagation, load forecasting

## Min–max normalisation
- **Notation**: paper Eqs. 1–2: $X_{norm}=\frac{X-X_{min}}{X_{max}-X_{min}}$
- **Definition**: Rescales each feature independently to a common [0,1] range so all features carry equal importance and gradient-based training converges faster.
- **Boundary conditions**: Applied per feature; requires known/bounded input range. Eqs. 1 and 2 are identical in the paper.
- **Related concepts**: data preprocessing, feature scaling
