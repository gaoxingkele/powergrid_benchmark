# Concepts

## Three-Channel LSTM-CNN Model
- **Notation**: —
- **Definition**: A hybrid forecasting architecture with three parallel, independent single-layer LSTM channels — one each for historical-load, meteorological-environment, and time features — whose neuron outputs are concatenated, transposed, and fused by a two-layer 1-D CNN + max-pooling + fully connected head to output a full next-day load curve. The design gives each heterogeneous modality its own encoding pathway (late fusion) rather than a shared single-channel encoder.
- **Boundary conditions**: Requires the three modality groups to be separately available; historical-load channel uses same-hour prior-day values so each output corresponds to a same-time future point.
- **Related concepts**: LSTM, Convolutional Neural Network, Late Fusion, One-Dimensional Convolution

## Long Short-Term Memory (LSTM)
- **Notation**: forget gate $f_t=\mathrm{Sigmoid}(w_f\cdot[x_t,y_{t-1}]+b_f)$; input gate $i_t$; candidate $\tilde c_t$; cell $c_t=f_t\cdot c_{t-1}+i_t\cdot\tilde c_t$; output gate $o_t$; $y_t=o_t\cdot\tanh(c_t)$ (Eqs. 1–6)
- **Definition**: A recurrent network variant using memory cells and a three-gate mechanism (input, forget, output) to control information flow, alleviating vanishing/exploding gradients and capturing long-term temporal dependencies. The forget gate's Sigmoid output in [0,1] selects how much of the previous cell state to retain.
- **Boundary conditions**: Suited to sequential/time-series data; here one LSTM layer with 64 neurons per channel.
- **Related concepts**: Recurrent Neural Network, Gate Mechanism, Three-Channel LSTM-CNN Model

## Convolutional Neural Network (CNN)
- **Notation**: fusion $S_{(1,n)}=f\left(\sum_{i=1}^{3}\sum_{j=1}^{n}H_{(i,j)}*w_{(i,j)}+b\right)$ (Eq. 8)
- **Definition**: A feedforward network using local connection and weight sharing to extract abstract features; a typical CNN comprises input, convolutional, pooling, fully connected, and output layers. Kernel size, stride, and padding are its three convolution hyperparameters. Here it fuses the transposed three-channel LSTM outputs.
- **Boundary conditions**: In this paper only 1-D convolution (Conv1D) and 1-D max pooling (MaxPooling1D) are used on the LSTM output matrix.
- **Related concepts**: One-Dimensional Convolution, Max Pooling, Fully Connected Layer

## One-Dimensional Convolution (Conv1D)
- **Notation**: —
- **Definition**: Convolution applied along a single (temporal/feature) axis; used here for feature extraction over the concatenated, transposed LSTM channel outputs. Two Conv1D layers are stacked (8 kernels then 2 kernels) so the network mines correlation across the three modalities.
- **Boundary conditions**: Input matrix scale should exceed kernel size; smaller kernels extract fewer input features.
- **Related concepts**: Convolutional Neural Network, Max Pooling

## Late Fusion (independent encoding pathways)
- **Notation**: —
- **Definition**: A multi-modal learning strategy in which each modality is encoded separately and the modality representations are combined only at a later stage, preserving modality-specific characteristics while still enabling cross-modal interaction. It is the theoretical motivation (ref [17]) for the three-channel design, opposed to single-channel early fusion that entangles modalities.
- **Boundary conditions**: Beneficial when modalities are genuinely heterogeneous (periodic vs delayed vs trend/stochastic).
- **Related concepts**: Three-Channel LSTM-CNN Model, Multi-source Heterogeneous Features

## Multi-source Heterogeneous Features
- **Notation**: historical load $\{X_{t-24},X_{t-24*2},\dots,X_{t-24*m}\}$; meteorology $\{W^1_t,\dots,W^r_t\}$; time $\{T^1_t,\dots,T^e_t\}$
- **Definition**: The three distinct input modalities: (1) temporal metadata with strict periodicity but weak nonlinear weather interaction; (2) meteorological signals (temperature, humidity) with delayed load effects from building thermal inertia; (3) historical load sequences carrying both trend and stochastic components.
- **Boundary conditions**: Each has different statistical structure, motivating separate channels.
- **Related concepts**: Late Fusion, Three-Channel LSTM-CNN Model

## Leaky ReLU Activation
- **Notation**: negative-input slope $\alpha\in(0,1)$
- **Definition**: A rectifier variant assigning a small nonzero slope $\alpha$ to negative inputs, avoiding the ReLU dead-unit problem (weights unable to update on the zero branch) and the vanishing gradient of saturating activations, thereby giving the best model accuracy in the activation ablation.
- **Boundary conditions**: Chosen as the network activation for the three-channel model; comparison against Sigmoid, Tanh, ReLU.
- **Related concepts**: Activation Function, Gradient Vanishing

## Short-Term Load Forecasting (STLF)
- **Notation**: predicted point $X_t$
- **Definition**: Prediction of power load over a short horizon (here the next day, 24 hourly points), a key technology for optimizing generation plans and reducing grid operational risk. This model is an improved single-step predictor that produces a full consecutive-day curve via same-hour prior-day alignment.
- **Boundary conditions**: Next-day horizon; single-step design corresponded to same-time future points.
- **Related concepts**: Three-Channel LSTM-CNN Model, MAPE

## Forecast Error Metrics (RMSE / MAE / MAPE)
- **Notation**: RMSE, MAE (in MW); MAPE (in %)
- **Definition**: The three evaluation metrics reported for every model and ablation. MAPE (mean absolute percentage error) is the headline metric; the paper also reports RMSE and MAE in megawatts. Lower is better on all three.
- **Boundary conditions**: RMSE/MAE reported in MW even when residual plots use kW axes; MAPE in percent.
- **Related concepts**: Short-Term Load Forecasting
</content>
