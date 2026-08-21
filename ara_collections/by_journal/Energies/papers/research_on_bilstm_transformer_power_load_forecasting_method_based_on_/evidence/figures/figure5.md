# Figure 5

**Source:** `evidence/figures/figure5.png`

**Caption:** Figure 5. Fitting performance of different models in the dataset.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — multi-panel comparison of predicted vs. actual load curves.

**Structured Description:**

This figure is a multi-panel plot (likely 3x3 grid) showing the fitting performance of all nine evaluated models against the actual load values over a representative time window. Each panel contains:
- **X-axis:** Time steps (0.5h intervals)
- **Y-axis:** Power load value (units: kW or MW)
- **Red/Blue lines:** Typically, one color represents actual load values and the other represents the model's predicted values

**Models displayed (one per panel):**
1. CNN
2. LSTM
3. GRU
4. TCN
5. CNN-LSTM
6. Transformer
7. TCN-GRU
8. TCN-LSTM-Attention
9. DAF-BT (proposed)

**Key visual observations:**
- The proposed DAF-BT panel shows the closest alignment between predicted and actual curves
- CNN and LSTM panels show more systematic deviations, particularly at peak and valley points
- Transformer shows improved global trend capture but local deviations remain
- The DAF-BT prediction curve tracks the actual load more tightly during sharp transitions and stable periods alike

This figure provides qualitative support for the quantitative metrics reported in Table 2.
