# Environment

- **Language/runtime**: Not specified in paper. Runtimes reported to microsecond precision (Tables 4,
  5) imply a scripted numerical environment (MATLAB-style is typical for this class of GWO/economic-
  dispatch work), but the paper names no language, version, or solver framework.
- **Framework**: Not specified in paper.
- **Hardware**: Not specified in paper (no CPU/GPU/memory reported; runtimes are given but not the
  machine).
- **Data sources**:
  - Meteorological data: European Centre for Medium-Range Weather Forecasts (ECMWF).
  - Wind/solar power output and load: historical data from a low-latitude coastal region and the
    local grid; a typical-day forecast is derived from these.
  - Electricity tariff: region-specific time-of-use (TOU) purchase/sale prices (Figure 5); flat
    inter-MG trading price.
  - No public dataset or repository link is provided. Data Availability Statement: "The original
    contributions presented in the study are included in the article, further inquiries can be
    directed to the corresponding author."
- **Key dependencies**: Not specified in paper.
- **Protocols**:
  - Horizon: 1 day, 24 one-hour intervals.
  - Optimizer comparison uses repeated runs to compute convergence variance (Eq. 21); the number of
    runs N is not stated numerically.
  - Robustness protocol: add a ±10% random disturbance to MG1 wind output, MG2 PV output, and MG3
    load forecast, then re-solve.
- **Random seeds**: Not specified in paper.

## Note on code artifacts
No source code, pseudocode listing, configuration files, or run logs are released with the paper. The
method is given as mathematical equations (Eqs. 1-21) plus a printed Step 1-7 procedure and the
Figure 3 flowchart. These are transcribed into `logic/solution/algorithm.md` and
`logic/solution/formulation.md`. Per ARA rule 14(a), no `src/execution/` code stub is fabricated from
a prose/equation-only method, and key numerical hyperparameters (population size, total iterations T,
search bounds, penalty coefficients) are not specified, so a runnable reconstruction is not possible
from the paper alone.
