# Figure 11

**Source:** `evidence/figures/figure11.png`

**Caption:** Figure 11. Individual load fitting curves for ablation study variants.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — multi-panel comparison of ablation variant predictions.

**Structured Description:**

This figure presents a multi-panel plot showing the load fitting curves for each ablation study variant over a representative time window. Each panel shows one variant's prediction against the actual load:

**Variants displayed (one per panel, likely 6 panels):**
1. BiLSTM (only)
2. Transformer (only)
3. BiLSTM + DAF
4. BiLSTM + Transformer (no DAF)
5. Transformer + DAF
6. Full DAF-BT (BiLSTM + Transformer + DAF)

**Each panel contains:**
- **X-axis:** Time steps
- **Y-axis:** Power load value
- Actual load curve (one color)
- Variant prediction curve (another color)

**Key visual observations:**
- BiLSTM-only and Transformer-only panels show the poorest fit, with visible deviations
- BiLSTM-DAF shows improvement over BiLSTM-only, demonstrating DAF's benefit
- BiLSTM-Transformer (no DAF) shows moderate improvement
- Transformer-DAF panels show notably better fit than BiLSTM-Transformer
- Full DAF-BT panel shows the closest tracking with minimal deviation

This figure provides qualitative support for the ablation metrics in Table 3 and is part of Experiment E03.
