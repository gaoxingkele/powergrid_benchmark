# Figure 1

**Source:** `evidence/figures/figure1.png`

**Caption:** Figure 1. Structure diagram of Transformer model encoder.

**Figure type:** Diagram

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — standard Transformer encoder architecture with multi-head self-attention, feed-forward network, add & norm layers, and positional encoding.

**Structured Description:**

The diagram depicts the standard Transformer encoder architecture as introduced by Vaswani et al. (2017). The input sequence first passes through an Embedding layer combined with Positional Encoding to inject sequence-order information. The embedded representation enters repeated encoder blocks, each consisting of:
1. **Multi-Head Self-Attention:** Computes attention scores across all positions using multiple parallel attention heads.
2. **Add & Norm (Residual Connection + Layer Normalization):** Skip connection around the attention sub-layer followed by layer normalization.
3. **Feed Forward Neural Network:** Two-layer fully connected network with ReLU activation.
4. **Add & Norm (Residual Connection + Layer Normalization):** Skip connection around the FFN sub-layer followed by layer normalization.

The output is a sequence of contextualized representations suitable for downstream tasks. This figure establishes the Transformer baseline architecture that the proposed model extends with local enhanced attention (mask M).
