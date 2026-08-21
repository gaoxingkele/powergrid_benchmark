# Concepts: TSTG Paper

## 1. TSTG (Transformer Spatio-Temporal Graph neural network)

An encoder-decoder deep learning model for short-term multi-energy load forecasting. Each encoder/decoder layer contains two novel modules — multi-head spatio-temporal attention (with MI augmentation) and dynamic adaptive graph convolution — that are co-trained end-to-end to jointly model temporal long-range dependencies, nonlinear feature interactions, and dynamic spatial relations.

## 2. Multi-head spatio-temporal attention

A dual-attention mechanism that operates in parallel over two axes: the time axis (modeling long-range temporal dependencies between time steps) and the feature axis (modeling nonlinear interactions between energy load types). Each head computes both temporal and feature attention independently and combines the results. Standard dot-product is augmented with a mutual information term.

## 3. Mutual Information (MI) attention augmentation

An additive term in the attention computation that estimates the mutual information between pairs of elements (time steps or feature dimensions) using a bilinear projection layer, then adds it to the scaled dot-product similarity. This allows the attention mechanism to capture nonlinear and asymmetric dependencies that linear dot-product similarity alone cannot detect. The MI term is computed in closed form from the Gaussian kernel of the projected representations.

## 4. Dynamic adaptive graph convolution

A spatial convolution module that constructs the adjacency matrix adaptively by fusing two sources: (a) a static physical topology adjacency based on known network connections, and (b) a data-driven similarity graph computed from the current load feature representations using MI as the similarity metric. The fused adjacency matrix is updated at each layer / each time step, allowing the model to capture shifting spatial dependencies as operating conditions change.

## 5. Physical topology

The pre-defined network connectivity of the IES (e.g., pipe/duct connections between buildings, electrical bus topology). Encoded as a static binary or weighted adjacency matrix A_phy that reflects the known infrastructure graph but does not capture real-time load-dependent spatial relationships.

## 6. Feature similarity

A data-driven measure of pairwise similarity between node (building/load) feature embeddings, computed using MI from the current hidden representations. Unlike physical topology, feature similarity captures functional coupling between loads that may not be connected physically but co-vary in operation (e.g., buildings with similar occupancy schedules).

## 7. Encoder-decoder architecture

A sequence-to-sequence framework where the encoder processes the input historical window of T_hist time steps and produces a compressed latent representation, and the decoder uses this representation to generate forecasts for T_pred future steps. In TSTG, both encoder and decoder share the same layer design (attention + graph convolution), and the full model is trained end-to-end with a joint loss.

## 8. Spatio-temporal joint optimization

The simultaneous training of both temporal (attention) and spatial (graph convolution) parameters via a single loss function that backpropagates through both modules in each layer. This contrasts with two-stage or pipeline approaches where spatial and temporal modeling are performed separately.

## 9. Multi-energy load coupling

The interdependent relationships between electric, cooling, and heating loads in an IES, arising from physical energy conversion equipment (e.g., combined heat and power, electric chillers, heat pumps) and complementary operation patterns. Jointly modeling these coupled loads improves forecasting accuracy compared to independent per-load models.
