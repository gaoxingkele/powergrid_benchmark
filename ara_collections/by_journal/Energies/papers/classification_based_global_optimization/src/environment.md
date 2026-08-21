# Environment

- **Language/runtime**: MATLAB 2022b
- **Framework**: Not specified beyond base MATLAB. Power flow analysis and optimization routines are implemented in MATLAB, but no specific toolbox (e.g., MATPOWER, PSAT) is mentioned.
- **Hardware**: Intel Core i7 3.2 GHz 8th generation processor, 16 GB RAM
- **Data sources**:
  - IEEE 33-bus radial distribution system: 33 buses, 32 branches, 12.66 kV, 10 MVA base
  - IEEE 69-bus radial distribution system: 69 buses, 68 branches, 12.66 kV, 10 MVA base
  - Network parameters, line impedances, and load data sourced from Refs [24–27] as cited in the paper
  - Specific topology diagrams shown in Figures 5 and 6
- **Key dependencies**: MATLAB 2022b (standard installation assumed — no additional libraries specified)
- **Protocols**:
  - Bus classification: branches ranked by active and reactive power demand
  - Optimization: deterministic iterative search within classified branch subset
  - Power flow: run after each candidate configuration to evaluate objective function and constraints
  - Constraint checking: voltage limits (0.95-1.05 p.u.), thermal limits (|Sij| <= Sij,max), DG/CB capacity limits
- **Random seeds**: Not applicable — the CGO method is deterministic (no random components)
- **Code location**: No source code is provided in the paper or linked externally. The algorithm is described procedurally (Section 2.3, Figures 1-4) but no MATLAB scripts, functions, or data files are included in the publication.
- **Reproducibility**: The paper claims results are reproducible using MATLAB 2022b with the described CGO methodology, but no code or exact parameter files are available to independently verify this claim.
