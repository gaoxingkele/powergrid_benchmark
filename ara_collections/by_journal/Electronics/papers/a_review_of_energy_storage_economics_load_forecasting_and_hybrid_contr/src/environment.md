# Environment

This is a review/survey paper. It has **no released code, dataset, or runnable artifact** — the work
is analytical (literature synthesis). This file documents the methodological environment for
reproducibility of the review itself.

- **Language/runtime**: analytical — none (no code released). "The original contributions presented in this study are included in the article" (Data Availability Statement).
- **Framework**: n/a (narrative/technical review). PRISMA-informed screening methodology (§1.3).
- **Hardware**: n/a.
- **Data sources**: Literature databases searched — IEEE Xplore, ScienceDirect, Scopus, Web of Science. Coverage window 2012–2026. Search keywords included: microgrid, energy storage system, distributed energy resources, non-network solutions, battery management systems, grid resilience, supercapacitors, pumped hydro storage, forecasting, optimization, techno-economic assessment, control, grid inertia, energy storage system optimization, battery degradation, forecasting uncertainty, hybrid metaheuristics, ESS economics, HOMER Pro, MATLAB/Simulink, PVsyst.
- **Corpus funnel (Figure 1, PRISMA)**: 186 records identified → 26 duplicates removed → 160 screened → 35 excluded → 125 sought for retrieval → 2 not retrieved → 123 full-text assessed → 20 excluded → **103 included**.
- **Tools referenced by the surveyed / proposed framework (not run as artifacts in this paper)**: HOMER Pro 3.18.4 (techno-economic sizing/dispatch), PVsyst (physical PV + electrochemical degradation modelling), Helioscope (BIPV physical yield), ETAP (physical system modelling), MATLAB/Simulink R2025b (offline time-domain dynamic control validation), MATLAB Link (external dispatch control). Future validation platforms named: OPAL-RT (real-time Power-Hardware-in-the-Loop), Structured Text (ST) on PLCs.
- **Key dependencies**: None (no computational pipeline released).
- **Protocols**: PRISMA-informed literature screening (identification → screening → retrieval → eligibility → inclusion); thematic grouping into ESS integration, forecasting, techno-economic assessment, optimization/control.
- **Random seeds**: n/a.
