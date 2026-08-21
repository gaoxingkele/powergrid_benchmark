# Figure 1: Graphical abstract of study

- **Source**: Figure 1, §1 (page 2)
- **Caption**: "Graphical abstract of study."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Building/consumer icons (homes, offices, industry) → "Load Data" box → "Dataset Preprocessing" box → "Proposed Model" box → two parallel branches "LSTM" and "GRU" → "Load Forecasting" box.
- **Connections**: consumers → Load Data → Dataset Preprocessing → Proposed Model; Proposed Model fans out to LSTM and GRU (both green); both branches converge to Load Forecasting (orange output).
- **Annotations**: LSTM and GRU shown as the two alternative model choices inside the pipeline.
- **What it conveys**: end-to-end study pipeline — raw heterogeneous load data is preprocessed, fed to the proposed model, and forecast via either an LSTM or GRU branch. Mirrored into logic/solution/architecture.md (Overall pipeline).
