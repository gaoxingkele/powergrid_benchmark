# Figure 2: Workflow of the proposed procedure to model DAM/ASM sequential interaction

- **Source**: Figure 2, Section 2 (Methodology), p. 5
- **Caption**: "Workflow of the proposed procedure to model DAM/ASM sequential interaction."
- **Screenshot**: figure2.png (mid page 5)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components / data flow (top to bottom)**:
  1. Inputs: Unit technical limits, Unit availability, Unit DAM bids, RES & load forecasts, Interzonal flow bounds.
  2. "Day d" split into time steps 1, 2, … t, … N^T; each solved by a per-time-step "DAM t" block (chained with d−1 ← … → d+1 inter-day arrows).
  3. DAM output: "Unit DAM schedules / Market Clearing Price".
  4. Two parallel branches: "Bids Adjustment" (fed by Unit DAM bids, Unit technical limits, Unit availability, Unit MUT & MDT) producing "Unit ASM bids"; and "DC Load Flow" (fed by Power flow bounds) producing "DAM power flows / PTDFs". A "+" joins the two branches.
  5. "Updated forecasts" feed into the "ASM d" block (also chained across days d−1 → d+1).
  6. ASM output: "Unit ASM schedules / Redispatching costs".
- **Connections**: DAM schedules feed both Bids Adjustment and DC Load Flow; ASM bids + PTDFs + updated forecasts all feed the ASM optimization; day-to-day arrows carry inter-temporal state.
- **What it conveys**: The four-stage procedure (DAM model → unit bids adjustment for ASM → DCLF & PTDF sensitivity → nodal ASM optimization), solved ∀ d ∈ Ω^D. This diagram is the backbone of `logic/solution/method.md`.
