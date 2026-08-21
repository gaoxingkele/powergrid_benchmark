# Figure 2: Hierarchy structure of wolf pack in GWO algorithm

- **Source**: Figure 2, Section 3.1
- **Caption**: "Hierarchy structure of wolf pack in GWO algorithm."
- **Screenshot**: figure2.png
- **Location on page**: Page 7 (PDF page 7), middle of the page, above Table 2.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A four-tier pyramid. Top to bottom: Alpha (α) Wolf, Beta (β) Wolf, Delta (δ) Wolf, Omega (ω) Wolf.
- **Connections**: Strict dominance hierarchy — each tier leads the tier(s) below it.
- **Annotations**: Pyramid shape encodes decreasing rank and increasing population share from top (α, single leader) to bottom (ω, the bulk of the pack).
- **What it conveys**: GWO encodes its social leadership model as this hierarchy; during optimization the three best solutions are labelled α/β/δ and steer the ω individuals' position updates (Eqs. 16-19). Roles detailed in Table 2.
