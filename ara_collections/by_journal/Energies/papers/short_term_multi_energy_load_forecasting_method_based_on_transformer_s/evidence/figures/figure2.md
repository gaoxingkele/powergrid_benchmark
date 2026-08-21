# Figure 2: Multi-Head Spatio-Temporal Attention Module

**Source:** `evidence/figures/figure2.png`

**Caption:** "Structure of the multi-head spatio-temporal attention module."

**Figure type:** Diagram

**Extraction method:** Screenshot from PDF page 6

**Reading confidence:** High — the diagram shows a clear module-level structural view.

## Structured Visual Description

The figure shows the internal structure of the multi-head spatio-temporal attention module:

1. **Input:** A block labeled "Input Features" at the top.

2. **Parallel branches (left and right):**
   - **Left branch — Temporal Attention:** Labeled "Multi-Head Temporal Attention" with an inset showing attention over time steps (T x T matrix visualization). Below this, a "Mutual Information Enhancement" block is connected, feeding into the temporal attention computation.
   - **Right branch — Feature Attention:** Labeled "Multi-Head Feature Attention" with an inset showing attention over feature dimensions (D x D matrix visualization). Below this, a "Mutual Information Enhancement" block is connected, feeding into the feature attention computation.

3. **Concat + Project:** The outputs of both temporal and feature attention branches merge into a "Concat" block, followed by a "Linear Projection" block.

4. **Output:** Labeled "Output Features" (d_model dimension).

5. **Mutual Information (MI) sub-block (bottom center):** A detailed inset shows the MI computation pipeline:
   - Input vectors (u_i, u_j) -> Bilinear Projection (W_mi) -> Nonlinear Activation (σ) -> MI score.

6. **Labels and annotations:**
   - Equation references: "Eq. (2)" next to MI calculation, "Eq. (3)-(4)" next to temporal attention, "Eq. (5)-(6)" next to feature attention.
   - Head count H is annotated for the parallel mechanisms.

No data values, axes, or numerical results are present.
