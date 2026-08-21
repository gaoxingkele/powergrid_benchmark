# Figure 6: DC-coupled HESS
- **Source**: Figure 6, Section 2.2.3 (page 13) in the review
- **Caption**: "DC-coupled HESS."
- **Screenshot**: figure6.png (page 13; diagram at the top, above Table 2)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: **Renewable Energy Sources** → **DC-DC Boost Converter**; **Battery Energy Storage Systems (BESS)** ↔ **Bidirectional DC-DC Converter**; **Supercapacitor** ↔ **Bidirectional DC-DC Converter**; a vertical **Common DC Bus**; a single **Grid-Forming Inverter**; **Grid** and **AC Loads** on the right (dashed AC links).
- **Connections**: RES feeds the common DC bus through a boost converter; the battery and supercapacitor branches each attach through their **own bidirectional DC-DC converter** (double-headed arrows); the grid-forming inverter is the single AC interface to Grid and AC Loads.
- **Annotations**: separate storage branches make the functional split explicit — batteries for sustained balancing, supercapacitors for transient buffering.
- **What it conveys**: the DC-coupled hybrid energy storage architecture in which supercapacitors buffer high-frequency PV/load fluctuations and batteries handle medium- to long-term exchange, reducing high-frequency battery stress and degradation while one centralized grid-tied inverter delivers stabilized power (§2.2.3; quantified contrasts in Table 2).
- **Numbering note**: §4.2 states "As illustrated in Figure 6, recent research demonstrates that the GWO-PSO hybrid significantly outperforms standalone algorithms…" — that sentence actually refers to the GWO-PSO workflow printed as **Figure 7** (see figure7.md). The object captioned "Figure 6" is this HESS diagram; the ARA files objects by their printed captions.

**Supports claims**: C02, C07
