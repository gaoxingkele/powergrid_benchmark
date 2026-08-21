# Figure 3: Dynamic Adaptive Graph Convolution Module

**Source:** `evidence/figures/figure3.png`

**Caption:** "Structure of the dynamic adaptive graph convolution module."

**Figure type:** Diagram

**Extraction method:** Screenshot from PDF page 7

**Reading confidence:** High — the diagram shows a clear module-level structural view.

## Structured Visual Description

The figure shows the internal structure of the dynamic adaptive graph convolution module:

1. **Left branch — Physical Topology:**
   - Block labeled "Physical Topology" representing the static network connectivity graph.
   - Arrow to "Adjacency Matrix (A_phy)" block (predefined, fixed).
   - A_phy feeds into the "Adjacency Fusion" block.

2. **Right branch — Feature Similarity (MI-based):**
   - Block labeled "Load Features" (current hidden representations from attention module output).
   - Arrow to "MI Similarity Computation" block, with an inset showing the pairwise MI calculation between node feature pairs (Z_i, Z_j) using bilinear projection W_sim.
   - Outputs "Similarity Matrix (A_mi)" which feeds into the "Adjacency Fusion" block.

3. **Center — Adjacency Fusion:**
   - Block labeled "Dynamic Adjacency Fusion" with annotations showing the gated combination:
   - A_dyn = gate_1 · A_phy + gate_2 · A_mi (Eq. 10 reference)
   - Two gating parameters (gate_1, gate_2) from a small sigmoid network conditioned on load features.

4. **Bottom — Graph Convolution:**
   - Block labeled "Graph Convolution Layer" showing: Z' = ReLU(A_dyn · Z · W_gcn) (Eq. 11 reference).
   - Output block labeled "Updated Node Representations".

5. **Key annotations:**
   - The dynamic nature is emphasized with a label "Updated per Layer / per Time Step".
   - Equation references throughout: "Eq. (8)" for physical adjacency, "Eq. (9)" for MI similarity, "Eq. (10)" for fusion, "Eq. (11)" for convolution.

No data values, axes, or numerical results are present.
