# Figure 4: The principle of convolution operation

- **Source**: Figure 4, Section 2.2, p6
- **Caption**: "The principle of convolution operation."
- **Screenshot**: figure4.png (page 6; diagram in upper-middle of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A 4×4 input matrix, a 2×2 convolution kernel `[[1,0],[0,1]]`, and a 3×3 output matrix.
- **Connections**: Kernel slides over input (stride 1, no padding); each output cell = dot product of kernel with the overlapping input window. The highlighted (green) example: $3\times1 + 1\times0 + 5\times0 + 2\times1 = 5$.
- **Annotations**: Labels "Input", "Convolution kernel", "Output"; green cells mark the worked example.
- **What it conveys**: How the convolution dot-product produces feature-map values; input scale should exceed kernel scale. The paper uses 1-D convolution (Conv1D) for its actual model.
</content>
