# Figure 2: Windowed CEEMDAN decomposition and IMF component extraction

- **Source**: Figure 2, §3.3 (p.8)
- **Caption**: "Windowed CEEMDAN decomposition and IMF component extraction."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Location on page**: upper-middle of page, below the paragraph on sliding-window design.

## Visual description
- **Components**:
  - Top row "Window data input": a sequence of boxes x(1), x(2), …, x(t−n), …, x(t), x(t+1)
    (the full sliding-window span of raw samples).
  - Middle arrow labeled "CEEMDAN decomposition".
  - Bottom block "Window interception data": a matrix of IMF component boxes — rows IMF1, IMF2, …,
    IMFk; columns aligned with the same time indices (1, 2, …, t−n, …, t, t+1). A dashed sub-box on
    the right marks the **rear/posterior segment** (columns around t−n … t+1) that is extracted.
- **Connections**: The raw windowed sequence is decomposed by CEEMDAN into k IMF component series;
  a fixed-length segment from the rear of the window is intercepted/extracted for training/prediction.
- **Annotations**: Dashed borders delimit the input window and the extracted interception region.
- **What it conveys**: The sliding-window strategy — decompose the whole (large) window, but only
  keep a fixed-length rear segment of each IMF, so trend/periodic components are captured while
  keeping the neural-network input short. Supports C04. Mirrored into logic/solution/method.md
  (Stage 1b).
