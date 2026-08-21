# Figure 1: The structure of the model (training flowchart)

- **Source**: Figure 1, Section 2, p3
- **Caption**: "The structure of the model."
- **Screenshot**: figure1.png (page 3; flowchart in lower half of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Start → Data preprocessing → Feature engineering → Dataset partitioning → Three-channel LSTM-CNN model → [Model training dashed box: "The model makes predictions in the training set" → "Calculate the prediction error" → decision "Whether the error meets the requirements" → decision "Whether the maximum number of training sessions has been reached" → "Optimal weights are derived"; with a right-hand loop "Updates to weights" → "Training repetitions +1" back into prediction] → "The model is predicted in the test set" → End.
- **Connections**: The error-check diamond: Y (met) → optimal weights; N → max-sessions diamond. Max-sessions diamond: Y → optimal weights; N → update weights → repetitions +1 → back to training prediction.
- **Annotations**: Dashed rectangle labeled "Model training" encloses the iterative loop.
- **What it conveys**: The end-to-end pipeline and the iterative train-until-converged-or-max-iters loop that produces the optimal weights before test-set prediction.
</content>
