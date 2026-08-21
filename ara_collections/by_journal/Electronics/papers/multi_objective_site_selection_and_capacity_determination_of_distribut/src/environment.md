# Environment

This is a modeling/simulation study; the paper releases no code, no configuration files, and no
numeric dataset, so `src/` holds only this reproducibility record.

- **Language/runtime**: Not specified in paper.
- **Framework**: Not specified in paper. The only tooling named is the solver "cplex", invoked
  inside the MOPSO loop ("Call the MOPSO function and use cplex to solve the optimal ADN scheme
  based on multiple objectives" — Figure A1, Appendix A).
- **Hardware**: Not specified in paper.
- **Test system**: IEEE 33-node ADN; "the detailed parameters are shown in Reference [18]"
  (Zhang et al., 2023 IEEE ITNEC). Total load 3715 kW + j2300 kvar; rated voltage 12.66 kV.
  WT at nodes 20 and 14; PV at nodes 9 and 30.
- **Data sources**:
  - Historical wind/PV output data used for KDE fitting — provenance Not specified in paper.
  - EV cluster sampling parameters: Table A1 (evidence/tables/tableA1.md) — arrival/departure
    times N(µ,σ), initial SOC U(a,b), per-station EV counts U(a,b) for 3 EV types.
  - Data Availability Statement (p.12): "The data presented in this study are available in this
    article." (i.e., nothing beyond the printed figures/tables is released.)
- **Key dependencies**: MOPSO implementation (variant/params not specified); CPLEX (version not
  specified); CNN-BiLSTM training stack (not specified).
- **Protocols**: planning flow per Figure A1 — CNN-BiLSTM EV prediction + Frank-copula DG scenario
  generation feed the MOPSO loop until convergence; EV data split into training/test groups
  (§4.1); 500 wind–solar scenarios generated then reduced to 5 weighted representatives (§5).
- **Random seeds**: Not specified in paper.
- **Funding/affiliation context**: State Grid Henan Electric Power Company Technology Project
  (5217C0240001).
