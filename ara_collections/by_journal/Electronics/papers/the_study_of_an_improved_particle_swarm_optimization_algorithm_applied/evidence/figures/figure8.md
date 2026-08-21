# Figure 8: Multi-source microgrid structure

- **Source**: Figure 8, Section 5.1 (page 14)
- **Caption**: "Multi-source microgrid structure."
- **Screenshot**: figure8.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A common bus labelled "Generatrix" (busbar) at the top. Connected distributed sources and loads: PV, WT (left side); DG, ESS (center); "Residential living quarters" (two residential-load icons) and "Industrial parks" (industrial-load icon) on the right.
- **Connections**: PV, WT, DG, ESS and the residential/industrial loads all connect to the common Generatrix bus. Solid lines = main power feeders; dashed lines = branch/secondary connections to the residential and ESS nodes.
- **Annotations**: labels in orange; the bus ties generation (PV/WT/DG/ESS) and consumption (residential + industrial) together, representing a single-bus multi-source microgrid.
- **What it conveys**: the physical topology of the case-study microgrid — 10 PV units (10 kW each), WT (10 kW), one DG (1000 kW), and 2 ESS units (10 kW each) feeding residential and industrial loads over a 24-h horizon (per Section 5.1 text). Mirrored into `logic/solution/formulation.md` (system description).
