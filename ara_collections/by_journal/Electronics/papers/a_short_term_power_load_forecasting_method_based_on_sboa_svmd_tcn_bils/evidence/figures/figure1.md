# Figure 1: SVMD Flowchart

- **Source**: Figure 1, Section 2.1, p. 4 (bottom half of page)
- **Caption**: "SVMD Flowchart."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (top→bottom flow): Start → Original data → Initialize SVMD parameters → Use SVMD to decompose the original data → Extract global signal feature values to obtain the modal center frequency → decision "Determine whether the modal center frequency component is lower than the intrinsic mode component" → (Y) Reconstruct the decomposed IMF components by summation → End.
- **Connections**: The decision node branches "N" back up to "Original data" (re-initialize + re-decompose loop); "Y" proceeds to reconstruction.
- **What it conveys**: SVMD is iterative — parameters are (re)initialized and decomposition repeats until modal center frequencies satisfy the intrinsic-mode-component condition, then IMFs are summed to reconstruct the signal.
