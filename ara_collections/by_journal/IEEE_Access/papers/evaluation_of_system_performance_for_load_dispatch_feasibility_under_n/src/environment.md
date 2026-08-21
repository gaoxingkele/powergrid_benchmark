# Environment

- **Language/runtime**: MATLAB (version not specified in paper). DA UC optimization is implemented via
  coding in MATLAB.
- **Framework**: Custom Dynamic Programming (DP) implementation for day-ahead unit commitment; no
  external solver/library named.
- **Hardware**: Not specified in paper (no CPU/GPU, memory, or runtime reported).
- **Test system / data sources**:
  - 24-bus, 26-generator IEEE Reliability Test System (RTS). Topology in Fig. 4.
  - Generator data (bus, number of units, unit index, max capacity per unit, capacity per bus) in
    Table 2; total 26 units, total available capacity 3105 MW. Cited from refs [1], [2], [14], [15]
    and [30], [31], [32] (RTS-79/RTS-96 and the 2019 update).
  - Fuel-cost coefficients $\alpha_i, \beta_i, \gamma_i$, active-power limits, ramp up/down rates, hot
    & cold startup costs, cooling time constant, minimum up/down times: referred from [30], [31], [32]
    (exact per-unit values not reproduced in the paper text).
  - Mean time to failure (MTTF, $t_{FR}$) and failure rate (FR, $\lambda$) per generator capacity:
    Table 3; referred from [10], [11].
  - Hourly forecasted next-day demand: Fig. 6 (peak 2670 MW at hour 11).
  - LOLP_max = 0.05 from Central Electricity Authority (CEA), India [34] (US DOE 0.002 [35];
    EU 0.008 [36]).
- **Key dependencies**: MATLAB (unversioned). Constraint formulations for shutdown cost, minimum
  up/down time, active power limits reused from the authors' prior work [27].
- **Protocols**:
  - Three case studies (Base Case; Case 1 at 10% SR; Case 2 at 8%/5%/0% SR) — Table 1.
  - N-1 single-generator-contingency simulation; nine indexed contingencies (Fig. 5).
  - COPT construction (Tables 7, 8) → hourly LOLP (Tables 9, 10) → operating margin (Table 11).
  - DC power flow assumed; single-unit-outage assumption for LOLP.
- **Random seeds**: Not applicable / not specified in paper (deterministic DP optimization;
  probabilities from fixed failure-rate data).

This is a prose + mathematical modeling and simulation study. No source code, repository, or
executable artifact is released with the paper, and no printed pseudocode is given for the DP routine;
therefore `src/` contains only this environment description (no `src/execution/` stubs — the method is
described in prose/equations and lives in `logic/solution/`).
