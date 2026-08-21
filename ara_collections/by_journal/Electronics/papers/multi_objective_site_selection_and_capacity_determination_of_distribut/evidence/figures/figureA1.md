# Figure A1: Flowchart of the algorithm in this article

- **Source**: Figure A1, Appendix A, page 12
- **Caption**: "Flowchart of the algorithm in this article."
- **Screenshot**: figureA1.png (flowchart at the bottom of page 12)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components / flow** (two input threads converging into the MOPSO loop):
  - Left thread (EV data): "Historical data on EVs is collected" → "The CNN-Bi-LSTM method is used for prediction" → "The predicted EV data is obtained".
  - Top thread (DG data): Start → "Initialize the parameters of AND [ADN], PV and EV" → "The Frank function is used to process WT and PV data" → "Establish the MOPSO model".
  - Both threads feed → "Enter the relevant parameters and solve the calculation".
  - MOPSO optimization loop: "Update the parameters of MOPSO" → "MOPSO is used to generate new fitness values" → "Call the MOPSO function and use cplex to solve the optimal ADN scheme based on multiple objectives" → decision "Meet the convergence conditions?" → N: loop back to update parameters; Y: End.
- **Connections**: sequential arrows as above; the decision diamond branches back into the update step on "N" and to End on "Y".
- **Annotations**: "cplex" is named as the solver called within the MOPSO scheme step.
- **What it conveys**: end-to-end planning pipeline — (1) predict EV cluster data with CNN-BiLSTM, (2) generate DG scenarios with the Frank copula, (3) build and iteratively solve the MOPSO multi-objective model until convergence. Mirrored in `logic/solution/algorithm.md`.
