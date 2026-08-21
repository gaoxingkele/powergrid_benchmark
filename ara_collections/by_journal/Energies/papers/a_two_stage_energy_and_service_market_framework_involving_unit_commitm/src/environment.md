# Environment

- **Language/runtime**: Python (DAM and ASM optimization via Pyomo library)
- **Framework**: Pyomo optimization modeling [42]; Gurobi solver [43]
- **Hardware**: 12th Gen Intel Core i9-12900F CPU @ 2.40 GHz, 32 GB RAM, 16 physical cores (24 logical processors), up to 24 threads
- **Software**: DIgSILENT PowerFactory for DCLF and sensitivity analysis (via Python API for automation)
- **Data sources**:
  - NREL 118-Bus Test System [31,39]: load demand, WF and PV production for leap year (NT = 8784), costs, availability escalators, monthly DH energy availability
  - Italian GME market data [41]: time-varying bid factors from public domain bids
- **Key dependencies**: Pyomo, Gurobi, DIgSILENT PowerFactory Python API
- **Protocols**: Sequential daily procedure: DAM LP (Pyomo/Gurobi) → bid adjustment → DCLF (PowerFactory) → ASM MILP (Pyomo/Gurobi) → inter-day continuity (Algorithm 1–2)
- **Computational performance**: ~4 min/day total (~2.5 min for ASM MILP)
- **Random seeds**: Not specified in paper
- **Code location**: Not released publicly; implementation described in Section 4
