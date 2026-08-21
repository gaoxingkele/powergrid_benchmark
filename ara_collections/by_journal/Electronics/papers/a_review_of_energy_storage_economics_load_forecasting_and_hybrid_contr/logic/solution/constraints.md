# Constraints, Assumptions, and Limitations

## Boundary conditions (scope of the review)
- **Domain**: Energy storage integration in renewable-dominated **AC microgrids** / active distribution networks. AC microgrids are treated as the dominant infrastructure; the review argues AC-specific stability must be solved with hybrid control rather than by migrating to DC microgrids (§1.1).
- **Three pillars**: The review structures the problem around (i) economic modelling + lifecycle degradation, (ii) deterministic forecasting under renewable uncertainty, (iii) optimization-based hybrid control (§1.2).
- **Validation modality**: **Offline time-domain simulation** (MATLAB/Simulink), not real-time hardware. Real-time Power-Hardware-in-the-Loop (e.g. OPAL-RT) and industrial protocols (Structured Text) are explicitly future work (§6).
- **Literature window**: 2012–2026, across IEEE Xplore, ScienceDirect, Scopus, Web of Science; PRISMA-informed (not a full systematic review of one narrow question) (§1.3).
- **Corpus**: 103 studies included after screening (Figure 1).

## Assumptions
- A1 (AC dominance): AC microgrids remain the dominant real-world infrastructure (§1.1).
- A2 (structural over monetary): The review deliberately assesses optimization frameworks on their ability to manage dynamic price structures (TOU ratios, peak-demand penalties) rather than fixed tariff values, because electricity prices are volatile and location-dependent — so no absolute monetary results are asserted (§3.1).
- A3 (deterministic scope): Forecasting and control are scoped to deterministic and structured (non-black-box) methods; stochastic/opaque approaches are noted but not the target regime.
- A4 (co-estimation): SoC and SoE are not directly measurable and are assumed co-estimated from current/voltage/temperature (§BMS).
- A5 (correlation stability): A stable positive quadratic SoC–SoE correlation is assumed to hold, enabling cross-referencing for error correction (Eq 11).

## Known limitations
- L1 (review, not experiment): The paper runs no original experiment; all quantitative figures are transcribed from surveyed studies. Reported numbers (e.g. THD 1.22%, SoE 5% capacity-error reduction, MAPE 0.8–2.6%) are single-study results cited as illustrative, not meta-analytic aggregates, and are stated without confidence intervals or shared benchmark conditions.
- L2 (tool-specificity): The proposed framework is anchored to specific commercial tools (HOMER Pro 3.18.4, PVsyst, Helioscope, MATLAB/Simulink R2025b, ETAP); generality beyond this toolchain is asserted but not demonstrated.
- L3 (HOMER dispatch rigidity): HOMER's built-in dispatch strategies (cycle charging, load following) and derivative-free optimizer are acknowledged to be too rigid / local-optima-prone; the framework relies on external optimization/dispatch to compensate (§3.4).
- L4 (physical fidelity gaps): Macro-economic modelling cannot represent shading, thermal loss, electrochemical degradation, or three-phase imbalance without meso/micro-scale coupling (§3.5, §4.4).
- L5 (no real-time validation): Because validation is offline, real-time robustness, communication-link vulnerability, and hardware constraints are not established (§6).
- L6 (degradation model simplification): Standard techno-economic modelling oversimplifies ageing; the review advocates but does not itself validate calendar-vs-cycle-ageing-aware models (§3.6).
- L7 (data availability): "The original contributions presented in this study are included in the article" — no dataset or code is released (Data Availability Statement, §6).
