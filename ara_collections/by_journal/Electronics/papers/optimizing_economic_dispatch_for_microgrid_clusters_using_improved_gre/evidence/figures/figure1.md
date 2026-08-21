# Figure 1: The structure of the microgrid cluster (MGC) system

- **Source**: Figure 1, Section 2.1
- **Caption**: "The structure of the microgrid cluster (MGC) system."
- **Screenshot**: figure1.png
- **Location on page**: Page 4 (PDF page 4), top half of the page, above Table 1.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Main Grid; Energy Management Center (EMC); three local buses hosting Microgrid 1, Microgrid 2, Microgrid 3. Microgrid 2 is drawn in detail with five AC/DC-coupled units on a Local Bus: Photovoltaic, Wind Turbine, Microturbine, Energy Storage System, and AC Load.
- **Connections**: Solid double-headed arrows = Power Flow; dashed red arrows = Communication Link. EMC communicates with the main grid and with all three microgrids; the main grid exchanges power with each microgrid. Each generation/storage unit connects to the Local Bus through an AC/DC converter.
- **Annotations**: MG1 and MG3 are described in the text as "essentially identical to MG2" except their non-renewable unit is a Diesel Generator (DG) rather than a Microturbine (MT). Legend distinguishes Power Flow vs Communication Link.
- **What it conveys**: The MGC is a centrally-coordinated (EMC) three-microgrid cluster where each MG bundles WT, PV, a dispatchable non-renewable unit (MT or DG), ESS, and load; energy can be exchanged MG-to-MG and MG-to-main-grid. This structure is mirrored in `logic/solution/architecture.md`.
