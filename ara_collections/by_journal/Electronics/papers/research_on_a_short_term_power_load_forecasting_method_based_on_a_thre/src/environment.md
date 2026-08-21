# Environment

- **Language/runtime**: Python (via PyCharm Community Edition 2024.3.4). Exact Python version not specified in paper.
- **Framework**: Keras (deep-learning library) built on TensorFlow **2.6.0**.
- **Hardware**: Notebook computer; Intel Core **i5-8300H** CPU; NVIDIA **GTX 1050Ti** GPU; Windows 11.
- **Data sources**:
  - Tétouan (Morocco) distribution-network power dataset, full year 2017.
  - Electrician Cup competition dataset.
  - Availability: "The datasets presented in this article are not readily available" (Data Availability Statement) — no download link or license provided.
- **Key dependencies**: TensorFlow 2.6.0, Keras. Other library versions not specified in paper.
- **Protocols**:
  - Data split into training and test sets (ratio not specified in paper).
  - Pipeline (Figure 1): data preprocessing → feature engineering → dataset partitioning → build three-channel LSTM-CNN → iterative training with weight updates until error criterion or max iterations → predict on test set.
  - Features normalized before LSTM input; predictions inverse-normalized at output.
- **Model hyperparameters** (§3):
  - `batch_size` = 256
  - LSTM: 1 layer per channel, 64 neurons each (3 channels)
  - CNN: 2 convolutional layers (8 kernels in the first, 2 kernels in the second) + 1 pooling layer
  - Learning rate = 0.001
  - Loss function = MAE
  - Iterations (epochs) = 80
  - Activation = Leaky ReLU (selected via ablation; Table 1)
  - Optimizer = Adam (selected via ablation; Table 2)
  - Historical-load lookback = 1 day / same hour (selected via ablation; Table 3)
- **Random seeds**: Not specified in paper.
- **Code availability**: No source code released. The method is described in prose + equations only (no printed pseudocode), so no `src/execution/` transcription applies (Rule 14a).
</content>
