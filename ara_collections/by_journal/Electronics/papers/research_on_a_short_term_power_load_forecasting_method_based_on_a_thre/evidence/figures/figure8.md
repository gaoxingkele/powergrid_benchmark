# Figure 8: Convolution operation process

- **Source**: Figure 8, Section 2.3, p9
- **Caption**: "Convolution operation process."
- **Screenshot**: figure8.png (page 9; diagram in upper half of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A 3×n matrix of LSTM outputs $H_{1,1}\dots H_{1,n}$ / $H_{2,1}\dots H_{2,n}$ / $H_{3,1}\dots H_{3,n}$ (rows = the three channels), a column kernel $[W_{1,1}, W_{2,1}, W_{3,1}]$, and a 1×n output row $S_{1,1}\dots S_{1,n}$.
- **Connections**: The column kernel convolves across the three channel rows (per Eq. 8, $S_{(1,n)}=f(\sum_{i=1}^{3}\sum_{j=1}^{n}H_{(i,j)}*w_{(i,j)}+b)$), collapsing the three modalities into a fused feature row.
- **Annotations**: `*` denotes convolution between the H matrix and the W kernel.
- **What it conveys**: How the CNN fuses the three transposed LSTM channel outputs — the concrete mechanism of cross-modal correlation mining. Mirrored into method.md §4.
</content>
