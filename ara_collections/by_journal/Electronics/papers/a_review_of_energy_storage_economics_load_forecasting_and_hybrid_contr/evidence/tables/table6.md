# Table 6 - Comparative analysis of data preprocessing techniques

**Source**: Table 6, Section 4.3 in the review. The table spans pages 20–21: caption and the first two rows (Min–Max Normalization, Z-Score Standardization) are at the bottom of page 20; the remaining rows (EMD, VMD, WT, PCA, STL) continue at the top of page 21.
**Caption**: "Comparative analysis of data preprocessing techniques."
**Screenshot**: table6.png (rendered from page 20, showing caption + first two rows; remaining rows continue on page 21)
**Extraction type**: raw_table

| Technique | Primary Function | Best Use Case |
| --- | --- | --- |
| Min–Max Normalization | Scales features to a fixed range (e.g., 0 to 1) | Accelerating algorithm convergence (e.g., GWO-PSO) |
| Z-Score Standardization | Transforms data to mean 0 and standard deviation 1 | Handling datasets with significant, unpredictable outliers. |
| Empirical Mode Decomposition (EMD) | Breaks non-linear signals into Intrinsic Mode Functions | Processing highly volatile renewable data (e.g., wind speed) |
| Variational Mode Decomposition (VMD) | Separates signals into band-limited modes | Isolating true signal trends from severe weather noise |
| Wavelet Transform (WT) | Multi-resolution time–frequency domain decomposition. | Denoising sudden transient events or severe weather spikes. |
| Principal Component Analysis (PCA) | Transform correlated variables into uncorrelated components. | Reducing feature redundancy in high-dimensional weather data |
| Seasonal-Trend Decomposition (STL) | Separates seasonal, trend, and residual components | Load forecasting scenarios with strong seasonal fluctuations |

**Supports claims**: C05
