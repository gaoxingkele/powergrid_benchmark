# Problem Specification

## Observations

### O1: Metaheuristics dominate MGC economic dispatch but each carries a characteristic failure mode
- **Statement**: Across the metaheuristic families surveyed, GA needs precise parameter initialization and risks local optima; PSO converges fast but is "singular" and unstable in high-dimensional spaces; FA has strong global search but long iteration times and O(n^2) complexity; WOA converges fast with few parameters but still risks local optima and is sensitive to initial population quality. Classical LP/NLP are "no longer suitable for the increasingly complex structure of modern power systems", and deep-learning methods (RNN/LSTM/DRL) "demand substantial volumes of training data, extensive training periods, and computational resources".
- **Evidence**: §1 Introduction (paragraphs on LP/NLP, ML, and metaheuristics); §4.3.1 quantitative confirmation in Table 5 / Figure 7.
- **Implication**: There is room for a metaheuristic that keeps GWO's simplicity while curing its local-optima/slow-convergence weaknesses.

### O2: Traditional GWO is a strong but flawed base solver
- **Statement**: GWO is "renowned for its simplicity, ease of implementation, and strong global search capabilities" and balances exploration/exploitation well, but "has its limitations, including a propensity to get trapped in local optima and slow convergence speeds, especially in complex, high-dimensional problem spaces".
- **Evidence**: §1 and §3.2 (opening of the improved-GWO section).
- **Implication**: GWO is the right scaffold to enhance rather than replace.

### O3: Common MGC objective functions omit storage-degradation and power-quality factors
- **Statement**: The recent MGC literature "often constructs objective functions focusing on operational and environmental costs" [19-21], typically omitting explicit ESS loss costs and penalties for main-grid exchange excursions or start/end ESS energy imbalance.
- **Evidence**: §1 (objective-function paragraph); §2.3.
- **Implication**: A richer objective can jointly express economics, power quality, and equipment longevity.

### O4: Chaotic initialization accelerates only the early search
- **Statement**: When chaotic maps replace uniform random initialization in GWO, convergence is significantly accelerated in early iterations, but "its impact diminishes in the later stages"; different maps also differ markedly in early convergence speed.
- **Evidence**: §4.2 and Figure 6; §4.3.1 opening.
- **Implication**: Chaos alone is insufficient; a mechanism acting throughout the run (late stages) is needed.

## Gaps

### G1: No single solver is simultaneously fast, accurate, and stable on MGC dispatch
- **Statement**: Existing metaheuristics trade one desideratum for another (e.g., FA accurate but slow; WOA fast-per-iteration but many iterations and unstable), so MGC dispatch lacks a solver that jointly wins on iteration efficiency, precision, and run-to-run stability.
- **Caused by**: O1, O2
- **Existing attempts**: GA, PSO, FA, WOA, SA, traditional GWO; OBL/ROBL and chaotic-map GWO variants.
- **Why they fail**: local-optima entrapment, initialization sensitivity, high per-iteration cost, or high convergence variance.

### G2: Cost-only objectives cannot protect power quality and ESS lifespan
- **Statement**: An objective built only from operational + environmental cost gives the optimizer no incentive to bound main-grid exchange excursions or to return the ESS to its starting energy level, risking power-quality and battery-longevity problems.
- **Caused by**: O3
- **Existing attempts**: operational+environmental cost objectives [19-21].
- **Why they fail**: they omit the ESS loss term and the two penalty terms entirely.

### G3: The exploration-diversity loss of GWO's hierarchy is not fixed by chaos
- **Statement**: GWO's strong α/β/δ-driven exploitation limits search diversity and can hinder exploration; chaotic initialization helps early but decays, leaving late-stage local-optima escape unaddressed.
- **Caused by**: O2, O4
- **Existing attempts**: static opposition-based learning (OBL) exploring current + fixed-opposite positions.
- **Why they fail**: a static opposite does not adapt to the evolving search landscape across iterations.

## Key Insight
- **Insight**: The two GWO weaknesses act on different phases, so they need two complementary cures applied together: chaotic-map initialization to diversify the *start* of the search, and a *dynamic* opposition-based learning operator (with an iteration-varying nonlinear factor r = sin(t/T)) to keep injecting adaptive reverse solutions *throughout* the run. On the modelling side, folding ESS loss and two penalty terms into a single fitness function lets one optimizer trade economics against power quality and equipment life.
- **Derived from**: O2, O3, O4
- **Enables**: CDGWO (chaos + DOBL GWO) solving a penalty-augmented multi-objective MGC dispatch model.

## Assumptions
- A1: The MGC comprises exactly three microgrids, each with WT, PV, one dispatchable non-renewable unit (MT or DG), an ESS, and AC load, centrally coordinated by an EMC.
- A2: Scheduling is over a 24-hour daily cycle with 1-hour intervals (24 intervals).
- A3: Wind/solar/load for a typical day are obtained by forecasting from historical + ECMWF meteorological data for a low-latitude coastal region; forecasts are treated as the nominal inputs.
- A4: ESS SOC is constrained to [30%, 90%]; WT/PV are treated as emission-free and ESS pollution is neglected.
- A5: Operational revenue uses time-of-use (TOU) pricing; inter-MG trading uses a flat price.
- A6: Robustness is probed via a ±10% random disturbance applied to MG1 wind, MG2 PV, and MG3 load.
