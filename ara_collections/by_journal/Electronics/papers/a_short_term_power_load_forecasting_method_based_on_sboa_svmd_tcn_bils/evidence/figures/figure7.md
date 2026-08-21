# Figure 7: TCN-BiLSTM model structure diagram

- **Source**: Figure 7, Section 3.3, p. 11 (lower half of page)
- **Caption**: "TCN-BiLSTM model structure diagram."
- **Screenshot**: figure7.png (same page as Figure 6; Figure 7 is the lower diagram)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (left→right): Input layer → TCN block → Hidden layer → BiLSTM block → Output layer.
- **Connections / annotations**: Input layer = IMF components from SVMD. TCN block = 1 residual unit (2 convolution units + multiple nonlinear mappings, ReLU activation). TCN output vector feeds the BiLSTM. Output layer = 1 fully-connected layer with 1 neuron producing the one-step-ahead load value.
- **What it conveys**: The per-component forecaster: TCN extracts multi-scale local features from each IMF, BiLSTM captures bidirectional temporal dependencies, and a dense layer maps to the load prediction.
