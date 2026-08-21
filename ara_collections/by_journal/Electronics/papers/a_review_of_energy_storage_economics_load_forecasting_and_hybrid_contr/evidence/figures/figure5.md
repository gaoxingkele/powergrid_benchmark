# Figure 5: DC-coupled architecture
- **Source**: Figure 5, Section 2.2.2 (page 12) in the review
- **Caption**: "DC-coupled architecture."
- **Screenshot**: figure5.png (page 12; diagram in the middle of the page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: **Renewable Energy Sources** → **Renewable Energy Inverter** (DC/DC stage labelled "DC"); **Battery Energy Storage Systems (BESS)** ↔ **BESS Inverter** (bidirectional, labelled "DC"); a vertical **Common DC Bus**; a single **Grid-tied DC to AC** converter; **Grid** and **AC Loads** on the right (dashed AC links).
- **Connections**: RES and BESS connect to the shared **Common DC Bus** via dedicated DC–DC converters (BESS link bidirectional); one grid-tied DC-to-AC inverter interfaces the stabilized DC bus to the Grid and AC Loads.
- **Annotations**: DC labels on all bus-side links; AC only appears after the single grid-tied conversion stage.
- **What it conveys**: the DC-coupled topology — fewer conversion stages and direct PV-to-battery charging, improving system efficiency versus AC coupling (recent studies cited in §2.2.2 report approximately 3% higher efficiency for DC distribution), at the cost of increased control and protection complexity.

**Supports claims**: C07
