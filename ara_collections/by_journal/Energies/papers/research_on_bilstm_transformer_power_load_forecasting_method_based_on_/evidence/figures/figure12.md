# Figure 12

**Source:** `evidence/figures/figure12.png`

**Caption:** Figure 12. Combined overlay of ablation prediction trajectories.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — overlaid comparison of all ablation variant predictions.

**Structured Description:**

This figure shows all ablation study variant predictions overlaid on a single plot for direct visual comparison against the actual load curve.

**Plot layout:**
- **X-axis:** Time steps over a representative evaluation window
- **Y-axis:** Power load value

**Traces:**
- Actual load curve (solid black or thick line)
- Each ablation variant in a distinct color/line style (6 variants total)
- The overlay allows direct visual comparison of relative fit quality

**Key visual observations:**
- The spread of predictions across variants is visible as a "band" around the actual curve
- BiLSTM-only and Transformer-only predictions deviate most from the actual curve
- BiLSTM-Transformer reduces the deviation but still shows systematic bias at certain points
- Transformer-DAF predictions are closer to the full model than to the non-DAF variants
- Full DAF-BT prediction is closest to the actual curve, often nearly overlapping

**Value of this visualization:**
- Directly supports Claim C06 (fusion dominance over layer stacking) by showing Transformer-DAF outperforming BiLSTM-Transformer visually
- Provides a clear hierarchical visualization: single components < cascade without fusion < fusion with simpler backbone < full model
- The visual hierarchy matches the quantitative hierarchy in Table 3

This figure complements Figure 11's individual panel view and is part of Experiment E03 (ablation study).
