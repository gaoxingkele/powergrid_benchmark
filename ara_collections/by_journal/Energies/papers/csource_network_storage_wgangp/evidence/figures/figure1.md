# Figure 1: Neural Network Architectures of the Generator and Discriminator

- **Caption**: Figure 1. Neural network architectures of the generator and discriminator.
- **Source Page**: Page 5 of the PDF
- **Type**: Neural network architecture diagram
- **Extraction Method**: Full-page PDF render at 2.5x resolution
- **Reading Confidence**: Medium — the diagram labels the layers of both networks including FC dimensions, transposed convolution parameters, convolution parameters, activation functions (Tanh, LeakyReLU), batch normalization (BN), and dropout. Some fine text details may be partially legible at the rendered resolution.

## Content Description
(A) Generator: Takes random noise vector Z (128 dimensions) → FC (256×6×6, BN) → 3×3 TCONV (256, stride=2, padding=1, BN) → 3×3 TCONV (128, stride=2, padding=1, BN) → 3×3 TCONV (64, stride=1, padding=1, BN) → 3×3 TCONV (1, stride=1, padding=1, Tanh)

(B) Discriminator: Takes INPUT (24×24) → 3×3 CONV (64, stride=2, padding=1, LeakyReLU 0.2) → 3×3 CONV (128, stride=2, padding=1, BN) → FC (512, Dropout 0.3) → FC (1) → Wasserstein Loss + GP
