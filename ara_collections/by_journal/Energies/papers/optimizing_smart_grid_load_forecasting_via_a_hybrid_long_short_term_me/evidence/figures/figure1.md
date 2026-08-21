# Figure 1: Proposed Model

- **Source**: Figure 1, Section 3 (p.5)
- **Caption**: "Proposed model."
- **Screenshot**: figure1.png
- **Figure type**: diagram / pipeline flowchart
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A linear flowchart with six sequential blocks connected by directional arrows:

1. **Start** — rounded rectangle, labeled "Start"
2. **Load Raw Data** — rectangle: "Load Raw Data"
3. **Preprocessing** — rectangle: "Preprocessing (Cleaning, Scaling, Splitting)"
4. **LSTM Phase** — two sub-blocks in sequence:
   - "Build LSTM Model"
   - "Train LSTM on Time Series" -> "Generate LSTM Predictions"
5. **XGBoost Phase** — three sub-blocks:
   - "Prepare Data for XGBoost" (the source box has a typo: "Prediav Data for XGBoost")
   - "Train XGBoost Model"
   - "Predict Data for XGBoost" (again the label reads "Prediav Data for XGBoost")
6. **Evaluation** — rectangle: "Evaluation"
7. **End** — rounded rectangle: "End"

**Connections**: Arrow from Start -> Load Raw Data -> Preprocessing -> LSTM Phase -> XGBoost Phase -> Evaluation -> End.

**What it conveys**: The two-stage cascading pipeline: a sequential LSTM stage for temporal pattern extraction feeds into an XGBoost stage for residual correction / refinement, followed by joint evaluation. Mirrored in `logic/solution/architecture.md`.

**Note**: The flowchart labels contain typos ("Prediav" instead of "Predict") which are preserved in the source screenshot.
