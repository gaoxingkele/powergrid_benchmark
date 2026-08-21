# Concepts

## Empirical Mode Decomposition (EMD)
- **Notation**: $x(t)=\sum_{i=1}^{n} c_i + r_n(t)$ (Eq. 5)
- **Definition**: An adaptive, data-driven method that iteratively extracts intrinsic mode functions (IMFs) from a signal by sifting: identify extrema, fit upper/lower envelopes by cubic spline interpolation, subtract the envelope mean $m(t)$ to form $h(t)=x(t)-m(t)$ (Eq. 1), and repeat until $h(t)$ satisfies the IMF conditions. The process is based on the signal's intrinsic time-scale characteristics and needs no predefined basis functions. It terminates when the residual becomes monotonic.
- **Boundary conditions**: Suited to nonlinear and non-stationary signals; not constrained by the uncertainty principle. Prone to mode mixing, spurious components, and endpoint effects.
- **Related concepts**: Intrinsic Mode Function, Standard Deviation stopping criterion, EEMD, CEEMDAN, Mode mixing

## Intrinsic Mode Function (IMF)
- **Notation**: $c_i$
- **Definition**: An oscillatory mode extracted by EMD that satisfies two conditions: (1) at any time point the mean of the envelope defined by the local maxima and minima is zero; (2) over the entire dataset the number of extrema and the number of zero-crossings are equal or differ by at most one.
- **Boundary conditions**: Physically meaningful only when mode mixing is absent; the paper caps the number of IMFs at 8 to avoid excessive components.
- **Related concepts**: EMD, Residual component, Mode mixing

## Standard Deviation (SD) stopping criterion
- **Notation**: $SD=\dfrac{\sum_{t=0}^{T}\left|h_{(k-1)}(t)-h_k(t)\right|^2}{\sum_{t=0}^{T}\left|h_{(k-1)}(t)\right|^2}$ (Eq. 2)
- **Definition**: A convergence criterion for the sifting process; $h_k(t)$ is the data after $k$ sifting iterations. When $0.1 < SD < 0.3$, sifting stops and the current $h_k(t)$ is accepted as the IMF component.
- **Boundary conditions**: SD is generally recommended to be set between 0.1 and 0.3.
- **Related concepts**: EMD, IMF

## Mode mixing
- **Notation**: —
- **Definition**: The phenomenon where IMF components from different time scales are mistakenly identified as the same IMF, or IMF components from the same time scale are decomposed into multiple IMFs; mathematically a coupling between different IMF components. It affects all IMFs and can produce physically meaningless components as iteration progresses.
- **Boundary conditions**: A limitation intrinsic to plain EMD; addressed by EEMD and CEEMDAN.
- **Related concepts**: EMD, EEMD, CEEMDAN

## Ensemble Empirical Mode Decomposition (EEMD)
- **Notation**: $X_n(t)=x(t)+\omega_n(t)$ (Eq. 6); $c_i(t)=\frac{1}{N}\sum_{n=1}^{N} c_{i,n}(t)$ (Eq. 8)
- **Definition**: An improved EMD that adds Gaussian white noise sequences to the original signal, performs EMD on each noisy realization, and ensemble-averages the resulting IMFs across $N$ realizations to cancel the added noise and reduce mode mixing.
- **Boundary conditions**: Reduces mode mixing but incurs computational cost and residual noise, and requires many averaging runs.
- **Related concepts**: EMD, Mode mixing, CEEMDAN

## Complete Ensemble EMD with Adaptive Noise (CEEMDAN)
- **Notation**: $\widetilde{IMF_1}=\frac{1}{I}\sum_{i=1}^{I} IMF_1^{i}$ (Eq. 10); $x(t)=\sum_{k=1}^{K}\widetilde{IMF_k}+r_K(t)$ (Eq. 15)
- **Definition**: An EMD variant that adds adaptive white noise (via operator $E_k(\cdot)$, the $k$-th EMD mode) multiple times at each decomposition stage, using a per-stage noise coefficient $\varepsilon_k$ to control the signal-to-noise ratio, achieving nearly 0% reconstruction error with fewer averaging runs than EEMD. Decomposition stops when the residual has fewer than 3 extreme points.
- **Boundary conditions**: Small-amplitude noise handles high-frequency-dominated signals; large-amplitude noise handles low-frequency-dominated signals; poorly chosen amplitude yields suboptimal decomposition. Advantages over EMD/EEMD: adjustable noise coefficients, complete and noise-free reconstruction, fewer runs.
- **Related concepts**: EEMD, EMD, IMF, Sliding-window decomposition

## Sliding-window sequence decomposition
- **Notation**: —
- **Definition**: A segmentation strategy in which a window large enough to encompass the periodic and trend components of the load is slid across the series (step size 1); CEEMDAN is applied within each window and a fixed-length component segment is extracted from the rear (posterior) of the window to form training/prediction sequences. Endpoint effects are handled by linearly extending the extreme points.
- **Boundary conditions**: Window must be sized by the decomposition objective (60-day window used), not by the network input length; step size 1.
- **Related concepts**: CEEMDAN, Endpoint effect

## Long Short-Term Memory (LSTM)
- **Notation**: cell state $c_t$, hidden state $h_t$; gate weights $W_f, W_i, W_c, W_o$
- **Definition**: A recurrent network built on RNNs that uses gated cell/hidden states to address the gradient-vanishing problem, enabling learning of long-range temporal dependencies. Here each LSTM sub-model uses the output at the last time step as a feature summarizing the whole input sequence, and predicts one IMF/residual component; sub-models run in parallel.
- **Boundary conditions**: Weight sharing keeps the number of weights independent of input length; training time grows linearly with parameters.
- **Related concepts**: RNN, Batch Normalization, Dropout

## Batch Normalization (BN)
- **Notation**: $\hat{x}_i=\dfrac{x_i-\mu_P}{\sqrt{\sigma_P^2+\varepsilon}}$ (Eq. 18); $y_i=\gamma\hat{x}_i+\beta$ (Eq. 19)
- **Definition**: A layer that normalizes each mini-batch to a common distribution by scaling and shifting, using batch mean $\mu_P$ and variance $\sigma_P^2$, then applying a learned scale $\gamma$ and offset $\beta$. It stabilizes hidden-layer input distributions, acts partly as data augmentation, and partially addresses overfitting.
- **Boundary conditions**: In this paper, given the small scale of the electricity data, the BN layer is placed after the LSTM layer (vertical BN before LSTM did not yield satisfactory results).
- **Related concepts**: LSTM, Dropout, Overfitting

## Dropout
- **Notation**: —
- **Definition**: A regularization technique that randomly deactivates a proportion of neurons' information flow during training so those neurons do not update their weights for that iteration, reducing overfitting and improving generalization; it also simplifies the effective training model.
- **Boundary conditions**: Doubles training time because weight updates become stochastic; dropout probability set to 0.5 here.
- **Related concepts**: Batch Normalization, Overfitting, LSTM

## RMSE / MAE (evaluation metrics)
- **Notation**: $RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$ (Eq. 20); $MAE=\frac{\sum_{i=1}^{n}|y_i-\hat{y}_i|}{n}$ (Eq. 21)
- **Definition**: Root Mean Square Error measures the stability of a prediction model (penalizing large deviations), and Mean Absolute Error measures accuracy (mean absolute prediction error); $y_i$ is the actual value and $\hat{y}_i$ the predicted value of the $i$-th test sample over $n$ samples.
- **Boundary conditions**: Classical load-forecasting indicators; both are reported over the 50-user cohort.
- **Related concepts**: —
