# Figure 2

**Source:** `evidence/figures/figure2.png`

**Caption:** Figure 2. Architecture of CNN-LSTM model.

**Figure type:** Diagram

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — standard CNN-LSTM hybrid architecture diagram.

**Structured Description:**

The diagram illustrates the CNN-LSTM hybrid architecture used as a baseline in the paper. The architecture follows a sequential two-stage design:
1. **CNN Layer:** 1D convolutional layers process the input time series to extract local temporal features through sliding convolutional kernels. Pooling layers may follow for dimensionality reduction.
2. **LSTM Layer:** The CNN-extracted feature maps are flattened or reshaped and passed sequentially to an LSTM layer, which models the temporal dependencies among the extracted features.
3. **Output Layer:** A fully connected layer maps the LSTM hidden state to the load prediction value.

The sequential CNN-to-LSTM flow is highlighted to motivate the paper's observation of approximately 25% information loss during cross-module feature transmission. The absence of any adaptive fusion mechanism between the two modules is a key architectural limitation that the proposed DAF module addresses.
