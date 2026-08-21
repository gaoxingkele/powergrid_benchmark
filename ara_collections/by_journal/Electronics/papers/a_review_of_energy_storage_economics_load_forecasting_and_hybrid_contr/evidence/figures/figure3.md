# Figure 3: Proposed AC-coupled hybrid renewable energy microgrid architecture
- **Source**: Figure 3, Section 2 (page 9) in the review
- **Caption**: "Proposed AC-coupled hybrid renewable energy microgrid architecture."
- **Screenshot**: figure3.png (page 9; diagram occupies the upper half)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - **PV Modules** → **DC/DC (MPPT) Converter** → **DC/AC Inverter** → Microgrid AC Bus.
  - **Wind Turbine** → **Wind Generator (G)** → **AC-AC Converter** → Microgrid AC Bus.
  - **Battery Energy Storage System (BESS)** (containerized units) → **DC/DC Converter** → **Bidirectional DC/AC Grid-Tied Inverter (VSI)** → Microgrid AC Bus.
  - **Microgrid AC Bus** (central vertical bus bar).
  - **Energy Management Systems (EMS) Platform** box listing three functions: "Forecasting", "Optimisation", "Offline time-domain control"; a "Data" tag feeds it.
  - **Utility Grid** (transmission-tower icon) and **Local AC Loads** (load icon), both attached to the AC bus.
- **Connections**: solid lines = power flow from each generation/storage chain onto the common AC bus and out to Local AC Loads / Utility Grid; the BESS path is bidirectional (absorb excess or discharge). Dashed lines = telemetry/control signals between the EMS platform and the inverters, grid, and BESS ("Data").
- **Annotations**: every generation and storage asset connects through its **own** converter chain as an independent parallel node.
- **What it conveys**: the AC-coupled reference architecture in which the central EMS coordinates forecasting and offline time-domain control from telemetry, executing grid-aware dispatch based on rigorous SoE estimation — the physical embodiment of the planning↔control bridge (§2). Mirrored in `logic/solution/framework.md` (Physical microgrid architecture).

**Supports claims**: C01, C03, C07
