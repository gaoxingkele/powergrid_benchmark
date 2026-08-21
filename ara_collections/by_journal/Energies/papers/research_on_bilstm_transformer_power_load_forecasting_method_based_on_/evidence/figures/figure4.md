# Figure 4

**Source:** `evidence/figures/figure4.png`

**Caption:** Figure 4. Principle diagram of Dynamic Adaptive Fusion module.

**Figure type:** Diagram

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — detailed DAF module internal structure.

**Structured Description:**

The figure illustrates the internal architecture of the DAF module in detail, showing the two parallel evaluation pathways and the synergistic fusion operation:

**Left Pathway — Feature Channel Adaptive Unit:**
- Takes the combined feature representation [F_c; F_t] as input
- Passes through a weight generation network (W_c, b_c)
- Applies sigmoid activation to produce channel importance weights ω_c ∈ ℝ^{d_c}
- Each feature channel (load pattern, temperature influence, wind speed contribution) receives a context-dependent importance score
- Output: ω_c ⊙ F_c (channel-weighted features)

**Right Pathway — Temporal Contribution Evaluation Unit:**
- Takes the same combined feature representation [F_c; F_t] as input
- Passes through a separate weight generation network (W_t, b_t)
- Applies sigmoid activation to produce temporal importance weights ω_t ∈ ℝ^{d_t}
- Each time step receives a context-dependent relevance score
- Output: ω_t ⊙ F_t (temporal-weighted features)

**Central — Synergistic Fusion:**
- Combines the two weighted representations through element-wise addition
- Adds the nonlinear interaction term λ(ω_c ⊙ ω_t) for cross-dimensional coupling
- λ is a learnable scalar parameter
- Final output: F_out = ω_c ⊙ F_c + ω_t ⊙ F_t + λ(ω_c ⊙ ω_t)

The diagram uses distinct visual styling (different colors/shapes) for the channel and temporal pathways to emphasize the dual-path design.
