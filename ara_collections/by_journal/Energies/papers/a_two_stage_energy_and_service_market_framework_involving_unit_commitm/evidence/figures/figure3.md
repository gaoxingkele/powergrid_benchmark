# Figure 3: Bids' clearing order (DT unit bid adjustment cases)

- **Source**: Figure 3, Section 2.2, p. 7
- **Caption**: "Bids' clearing order: not cleared unit (a), unit cleared below the technical minimum (b), unit cleared at the technical minimum (c), unit cleared between the technical limits (d), unit cleared at the rated power (e)."
- **Screenshot**: figure3.png (upper half of page 7)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Five stacked-bar schematics (a)–(e), each spanning from 0 up to P_max_i,t with the technical minimum P_min_i,t marked. Legend maps colors to bid services: SU (orange), SD (light blue), UR (red), DR (blue), USR (yellow), DSR (green); an arrow marks the DAM cleared point P^D_i,t. Numbers 1,2,3(,4) denote the clearing order of bid steps.
- **Cases**:
  - (a) DT unit NOT cleared in DAM (P^D = 0): first clearable bid is SU, then first UR step, then USR; DSR only if above technical minimum; further UR steps only after the previous is used up.
  - (b) Cleared BELOW technical minimum: must clear SU (up to P_min) or SD (down to 0) — mandatory, unnumbered.
  - (c) Cleared AT technical minimum: may be shut down (SD) or provide upward services first.
  - (d) Cleared BETWEEN technical limits: can clear UR or DR plus both SR bids.
  - (e) Cleared AT rated power (P_max): first clearable are first DR step and DSR; further DR steps only after the previous is used up.
- **What it conveys**: How the DAM operating point of a DT unit determines which ASM bids (and in what order) can be cleared — the logic formalized by constraints (30)–(34) in the ASM model. Mirrored into `logic/solution/formulation.md` (bid adjustment) and `logic/solution/method.md`.
