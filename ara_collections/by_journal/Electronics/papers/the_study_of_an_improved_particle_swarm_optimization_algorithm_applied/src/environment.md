# Environment

- **Language/runtime**: MATLAB 2020a (stated in Author Contributions: "software, MATLAB 2020a"). No source code released.
- **Framework**: Not specified in paper (MATLAB; no toolbox named).
- **Hardware**: Not specified in paper.
- **Data sources**: Typical summer-day operating data for a city in Jiangsu Province, China (subtropical monsoon climate): daily load (Figure 9), wind speed (Figure 10), temperature (Figure 11), solar irradiance (Figure 12), and time-of-use electricity purchase/sale prices (Table 4). Device operating parameters (Table 1) and pollutant emission/treatment parameters (Table 2). Per the Data Availability Statement: "Due to confidentiality, the raw data cannot be provided. Processed data can be obtained by contacting the corresponding author." — raw data is NOT publicly available.
- **Key dependencies**: Not specified in paper.
- **Protocols**:
  - Optimizer settings: population size 100, 50 dimensions/particle, 2000 iterations, scheduling period 24 h with 1-h steps.
  - Benchmark test protocol: 5 functions (Sum of Different Powers, Schwefel, Rastrigin, Rosenbrock, Levy), dimension 50, acceptance threshold 0.01, known optimum 0 (Table 3); comparison against PSO/CPSO/QPSO under identical settings.
  - No preregistration; single-run curves (no seed-averaging reported).
- **Random seeds**: Not specified in paper. (PSO uses r1, r2 = random in [0,1]; seed control is not reported.)

## Notes on artifacts
No code, configs, or runnable artifacts were released with this paper, so `src/` contains only this environment file. The method exists in the source as prose + equations + enumerated steps (§4), which are captured in `logic/solution/algorithm.md` rather than re-encoded as a code stub (no printed source code or formal pseudocode listing to transcribe). Run records/logs were not released (raw data confidential), so no `evidence/results/` or `evidence/logs/` files are created.
