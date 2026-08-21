# Concepts

## Hybrid LSTM-XGBoost cascade
- **Notation**: $\hat{y}_{final} = f_{XGB}(\hat{y}_{LSTM})$ (Eq. 10)
- **Definition**: A two-stage forecasting pipeline in which an LSTM first produces a load prediction from the temporal sequence, and an XGBoost regressor is then applied to the LSTM output (together with engineered features) to produce the final forecast, refining the prediction by correcting non-linear residual error.
- **Boundary conditions**: Requires a base sequential prediction to refine; the paper describes the XGBoost stage as consuming the LSTM output. Note internal tension in the paper (see method.md / constraints.md) between "XGBoost learns the LSTM residual $e_t$" (Eq. 2, §3.2.3) and "XGBoost applied to the LSTM output" (Eq. 10, §3.6.3).
- **Related concepts**: Residual error correction, Ensemble learning, LSTM, XGBoost

## LSTM (Long Short-Term Memory)
- **Notation**: $h_t = \mathrm{LSTM}(x_t, h_{t-1})$ (Eq. 8)
- **Definition**: A recurrent neural network variant with memory cells and gating that retains long-term dependencies in sequential data; here configured as two LSTM layers of 50 neurons each with a dropout layer and dense output, sequence length 60.
- **Boundary conditions**: Strong at short- and long-term temporal dependency; the paper notes it "struggles during sudden spikes in demand" and high-amplitude fluctuations.
- **Related concepts**: RNN, GRU, Dropout, Sequence length

## XGBoost (Extreme Gradient Boosting)
- **Notation**: $\hat{y}_t = \sum_{k=1}^{T} \alpha_k f_k(x)$ (Eq. 9)
- **Definition**: An ensemble gradient-boosting method that builds a committee of decision trees, each correcting the errors of the previous, weighted-summed to a prediction; strong on non-linearity and high-order interactions.
- **Boundary conditions**: Handles non-linearity and missing values well but "cannot learn the temporal dependencies"; in this paper key hyperparameters (n_estimators, learning rate) tuned by grid search.
- **Related concepts**: Gradient boosting, Ensemble learning, Decision trees

## Residual error correction
- **Notation**: $e_t = y_t - \hat{y}_t^{LSTM}$ (Eq. 2)
- **Definition**: The difference between the observed value and the LSTM prediction at time $t$; used as the learning target/input for the downstream XGBoost stage so it models the error the sequence model leaves behind.
- **Boundary conditions**: Assumes residuals carry learnable non-linear structure; effective when the base learner's errors are non-random.
- **Related concepts**: Hybrid cascade, Boosting, Ensemble learning

## Ensemble learning
- **Notation**: —
- **Definition**: Combining multiple models' predictions to reduce variance and improve reliability; here the LSTM and XGBoost are combined so their complementary weaknesses cancel.
- **Boundary conditions**: Gains depend on the base models being complementary rather than redundant.
- **Related concepts**: Hybrid cascade, XGBoost, Robustness

## Feature engineering (lag & rolling-window features)
- **Notation**: $X_{lag_k}(t) = y(t-k)$ (Eq. 6); Rolling Mean/Std over window $N$ (Eq. 7)
- **Definition**: Derived predictors added to the raw load: datetime features (hour, day-of-week, month, weekday indicator), lag features (load at $t-1$, $t-2$, …), and rolling-window statistics (mean, median, std over the last $N$ periods).
- **Boundary conditions**: Window size $N$ and lag set are design choices; the paper does not enumerate the exact $N$/lags used.
- **Related concepts**: Preprocessing, Min-Max normalization, XGBoost

## Min-Max normalization
- **Notation**: $X_{norm} = \dfrac{X - \min(X)}{\max(X) - \min(X)}$ (Eq. 1)
- **Definition**: Linear rescaling of each feature to [0,1] (via scikit-learn MinMaxScaler) to keep values in a bounded range and aid training convergence, important especially for the LSTM.
- **Boundary conditions**: Sensitive to the min/max of the training set; outliers can compress the scale.
- **Related concepts**: Preprocessing, LSTM, Feature engineering

## Forecast error metrics (RMSE, MAPE, R2)
- **Notation**: $\mathrm{RMSE}=\sqrt{\tfrac{1}{n}\sum (y_i-\hat{y}_i)^2}$ (Eq. 3); $\mathrm{MAPE}=\tfrac{1}{n}\sum |\tfrac{y_t-\hat{y}_t}{y_t}|\times 100$ (Eq. 4); $R^2 = 1-\tfrac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}$ (Eq. 5)
- **Definition**: The three evaluation measures — root mean square error (absolute accuracy, MW), mean absolute percentage error (relative accuracy, %), and coefficient of determination (fraction of variance explained).
- **Boundary conditions**: R2 saturates near 1 on this data and thus poorly discriminates the models (see C02); MAPE is undefined/unstable when $y_t\to 0$ (the data contains near-zero readings, see Figures 2/3).
- **Related concepts**: Model evaluation, RMSE-saturation
