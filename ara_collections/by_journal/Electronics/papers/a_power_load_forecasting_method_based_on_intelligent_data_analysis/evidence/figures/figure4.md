# Figure 4: Comparison between a Standard Neural Network and a Dropout Neural Network

- **Source**: Figure 4, §4.2 (p.10)
- **Caption**: "Comparison between a Standard Neural Network (left) and a Dropout Neural Network (right)."
- **Screenshot**: figure4.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Location on page**: top of the page.

## Visual description
- **Components**: Two multi-layer perceptron schematics side by side.
  - **Left (Standard NN)**: fully connected layers — every neuron connected to all neurons in
    adjacent layers.
  - **Right (Dropout NN)**: same topology but several neurons are crossed out (marked with ⊗),
    indicating deactivated units; the remaining active neurons have a sparser connection pattern.
- **Connections**: Left = dense connectivity; right = reduced connectivity because dropped neurons
  (⊗) do not participate that iteration.
- **Annotations**: ⊗ symbols mark neurons whose information flow is randomly cut off.
- **What it conveys**: Dropout randomly deactivates a proportion of neurons during training so they
  do not update weights that iteration, giving a regularization effect and a simpler effective
  model. Mirrored into logic/solution/architecture.md (Dropout) and method.md (Stage 2).
