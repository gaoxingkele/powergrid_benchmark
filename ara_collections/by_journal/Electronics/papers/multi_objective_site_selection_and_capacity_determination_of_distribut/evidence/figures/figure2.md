# Figure 2: Structure of CNN

- **Source**: Figure 2, Section 4.1 (Data Processing Process of EV Cluster), page 6
- **Caption**: "Structure of CNN."
- **Screenshot**: figure2.png (upper diagram on page 6)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Input layer → Convolutional layer (feature maps) → Pooling layer → Fully connected layer → Output.
- **Connections**: standard feed-forward CNN pipeline; red dashed lines depict the local-receptive-field / weight-sharing mapping from input patch to convolutional feature map and onward to the pooled and fully connected representation.
- **Annotations**: stacked rectangles represent multiple feature-map channels at the convolutional and pooling stages.
- **What it conveys**: the CNN front-end that extracts local features from raw EV-cluster time-series data via local connection and weight sharing (reducing parameter count) before the recurrent stage. Mirrored in `logic/solution/method.md`.
