# Figure 2: Proposed multi-layer framework for AC-microgrid energy storage integration
- **Source**: Figure 2, Section 1.3 (page 7) in the review
- **Caption**: "Proposed multi-layer framework for AC-microgrid energy storage integration."
- **Screenshot**: figure2.png (full render of page 7; Figure 2 is the lower block diagram — Figure 1 shares the same page, see figure1.md/figure1.png)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (5 labelled panels):
  1. **Input Data** — PV/Wind profiles, Load Demand, Tariffs & Market, Battery Data, Weather Data (each with an icon).
  2. **Physical Modelling** — "PVsyst/ ETAP": "PV yield, Shading, Losses, and Degradation profiles."
  3. **Techno-Economic Planning & EMS** — "HOMER Software": "NPC, LCOE, BESS size, SoC/ SoE Limits, Forecasting, and Dispatch."
  4. **Dynamic Control Validation** — "MATLAB/ Simulink" (MATLAB logo): "Frequency, Voltage, THD, Transients, and Converter Control."
  5. **Outputs** — Optimal BESS Size, Dispatch Strategy, Stability Indicators.
- **Connections**: Input Data → Physical Modelling (solid arrow); Physical Modelling and Techno-Economic Planning & EMS both feed down into Dynamic Control Validation (solid arrows merging); Dynamic Control Validation → Outputs (solid arrow); **dashed feedback arrow** from Outputs back to Input Data (operational results dynamically update system constraints and input parameters).
- **Annotations**: tool names anchor each layer to a concrete software environment; the dashed line distinguishes the iterative refinement loop from the forward data flow.
- **What it conveys**: the review's core structural claim — long-term planning objectives (NPC, LCOE, storage sizing) and short-term operational stability metrics (frequency response, voltage regulation, transient performance) are explicitly linked in one workflow, with MATLAB/Simulink results fed back to refine BESS sizing, dispatch strategies, and transient stability performance. Mirrored in `logic/solution/framework.md`.

**Supports claims**: C01, C08
