# Environment

- **Language/runtime**: MATLAB (MATLAB 2022a)
- **Framework**: MATPOWER 6.0 (DC power-flow solutions for TNEP constraint evaluation)
- **Hardware**: computer with a 3.30 GHz 11th Generation Intel Core i7-11370H CPU and 64 GB of RAM
  (stated for the TNEP test-system runs; hardware for the CEC benchmark runs not separately specified)
- **Data sources**:
  - CEC2020 benchmark suite [51] — dims 5, 10, 15, 20, 30, 50, 100
  - CEC2022 benchmark suite [52] — dims 10, 20
  - Garver 6-bus test system — data from ref [58]
  - IEEE 25-bus test system — data from refs [58], [64]
  - Colombian 93-bus test system — data from ref [58]
- **Key dependencies**: MATPOWER 6.0 (accessed Nov. 24, 2024 per ref [56]); MATLAB 2022a
- **Protocols**:
  - Benchmark termination: maxFEs = 10000 × Dim; population sizes 30, 50, 100
  - Benchmark statistics over 51 independent runs; Friedman and Wilcoxon tests
  - TNEP: 51 independent runs per case for cost tables; convergence curves over ~90 iterations
  - Stability analysis: 30 independent runs over 7 case studies (SR%, MIT, MST)
  - Dynamic case: base year 2002, annual interest rate I = 10%, 3 planning stages
- **Random seeds**: Not specified in paper

## Notes on artifacts
No source code, repository, or executable artifact is released with the paper. The only concrete,
losslessly-transcribable algorithmic content is the printed pseudocode (Algorithm 1), the flowchart
(Figure 7), and the equations (Eqs. 1–41). These are captured as a reconstructed stub in
`src/execution/fdbcoa_obl.py` (grounding: reconstructed). No third-party repo was provided, so
`src/artifacts.md` is intentionally absent.
