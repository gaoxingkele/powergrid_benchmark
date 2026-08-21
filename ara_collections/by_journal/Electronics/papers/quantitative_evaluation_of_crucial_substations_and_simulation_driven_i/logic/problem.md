# Problem Specification

## Observations

### O1: Substation siting delays are endemic in fast-growing regions with scarce land
- **Statement**: In rapidly developing urban regions, high-voltage substation sites face significant implementation delays from constrained land resources and regulatory approvals; grid planning operates on a five-year cycle cascading high-to-low voltage, creating temporal interdependencies between upper and lower tiers.
- **Evidence**: §1 Introduction; §2.1 (paper narrative).
- **Implication**: When load growth outpaces the actual substation build schedule, distribution networks resort to suboptimal transitional infrastructure (extended lower-voltage lines from distant substations).

### O2: Delays and prematurity both generate investment waste, but the magnitude varies across the grid
- **Statement**: Delayed commissioning forces redundant infrastructure (waste on eventual overlap); premature construction causes prolonged underutilization (waste on idle assets). The impact magnitude of a delay depends on spatial distribution of existing substations, current operational status across all voltage levels, and regional load-growth dynamics.
- **Evidence**: §1; §2.1.
- **Implication**: A per-substation quantification of delay impact is needed; a uniform treatment mis-prioritizes construction sequencing.

### O3: Case-region load grows steeply through the near horizon
- **Statement**: Base-year (2020) aggregate demand is 2013.74 MW over 220 equivalent load nodes; forecast demand is 2734.83 MW by 2025 and 3316.22 MW by 2035 — a 35.81% rise over 2020–2025 and 21.26% over 2025–2035.
- **Evidence**: §4.1; Figure 3; §4.1 narrative (Figure 4 discussion).
- **Implication**: The front-loaded 2020–2025 growth makes delayed commissioning especially consequential in that window, providing a natural stress test.

## Gaps

### G1: No quantitative model of delay-induced multi-voltage investment impact
- **Statement**: Prior work lacks quantitative analysis/assessment modeling of how substation commissioning uncertainty propagates into actual investment across multiple grid hierarchies.
- **Caused by**: O1, O2.
- **Existing attempts**: Load-uncertainty-focused planning — deep learning joint siting/sizing [7], fuzzy load models [8,9], game-theory + robust optimization [10], robust optimization for forecast error [11]; multi-voltage joint planning [12–15].
- **Why they fail**: They optimize the *plan* but overlook the financial implications when actual construction deviates from the optimum; they do not quantify cascading effects of deviations on realized investment and long-term economics.

### G2: Evaluation indicator frameworks lack empirical validation
- **Statement**: Existing evaluation index systems select indicators from theoretical analysis or expert judgment, with limited empirical validation of practical accuracy across diverse scenarios.
- **Caused by**: O2.
- **Existing attempts**: Demand-guided multi-dimensional index systems [16]; coefficient-of-variation combination weighting + fuzzy evaluation [17]; AHP-entropy weighting for distribution networks [18].
- **Why they fail**: No mechanism ties the proposed indicators to an independently-measured downstream outcome (e.g., realized construction cost), so their criticality ranking is unverified.

### G3: No robust way to identify critical planned substations from an evolution perspective
- **Statement**: Methodologies to identify which planned substations are critical — accounting for their cascading effect on multi-voltage infrastructure development — remain insufficiently developed.
- **Caused by**: O1, O2, G1, G2.
- **Existing attempts**: Static evaluation systems (above).
- **Why they fail**: Static indices do not simulate how a delay reshapes downstream grid evolution and its cost.

## Key Insight
- **Insight**: Couple a cheap, static AHP criticality score with an expensive, dynamic grid-evolution simulation, then use the simulation once to *validate* that the score predicts delay-induced incremental cost. If the two agree, the score becomes a standalone screen for construction sequencing, and the demonstrated cost-scaling motivates deferring the least-critical substations.
- **Derived from**: O2, O3, G1–G3.
- **Enables**: A decision-support framework that both ranks substations and quantifies the economic cost of delaying any one of them, without simulating every candidate in operations.

## Assumptions
- A1: Five indices (load level, LV-grid influence, supply coverage, spatial influence, load density) sufficiently capture a substation's criticality.
- A2: AHP pairwise judgments (Santy scale) and their weights (validated by CR < 0.1) adequately encode planner preferences.
- A3: Minimizing per-horizon total construction cost is a faithful objective for realistic grid evolution.
- A4: A one-horizon deferral (commissioning postponed from 2020 to 2025) is a representative "delay" scenario.
- A5: The regional case (one grid, six new 110 kV substations) is representative enough to validate the score–cost relationship.
