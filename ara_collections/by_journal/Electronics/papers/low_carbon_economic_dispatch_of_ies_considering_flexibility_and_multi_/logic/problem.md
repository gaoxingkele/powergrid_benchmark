# Problem Specification

## Observations

### O1: High renewable penetration raises regulation difficulty
- **Statement**: As the renewable share grows, wind/solar output uncertainty and anti-peak-shaving behavior make the net-load curve fluctuate opposite to the load curve, amplifying regulation difficulty; concurrent load-side fluctuation increases supply–demand uncertainty (§1, §2.1).
- **Evidence**: §1 (refs [9]); §2.1 net-load / flexibility-demand discussion.
- **Implication**: The IES needs quantified flexibility (upward/downward margins) as a first-class scheduling objective, not just an afterthought.

### O2: Existing IES scheduling studies trade off one axis against the other
- **Statement**: Prior work either optimizes multi-entity economics while overlooking flexibility, or considers flexibility but prioritizes a single participant's interest (§1, end of Introduction).
- **Evidence**: §1 literature synthesis (refs [3]–[27]).
- **Implication**: A model is needed that jointly carries flexibility objectives AND multi-entity interest balancing.

### O3: PSO is convenient but prone to local optima on the IES problem
- **Statement**: PSO suits IES optimal scheduling for its concise implementation and fast convergence, but the IES model is nonlinear with many equality (balance) constraints, so particles easily fall into local optima and fail to reach the proper optimum (§1, ref [28]).
- **Evidence**: §1 paragraph on solution methods.
- **Implication**: PSO must be improved (search-diversity mechanisms) to avoid premature convergence.

### O4: Carbon and green-certificate mechanisms reduce emissions
- **Statement**: Stepped/tiered carbon trading and green-certificate–carbon joint trading have been shown to further cut emissions vs plain CET and to raise renewable accommodation (§1, refs [3][5]).
- **Evidence**: §1 review of carbon/GCT mechanisms.
- **Implication**: Embedding a GCT-CET mechanism into the operator's objective can drive low-carbon operation.

## Gaps

### G1: No joint flexibility + multi-entity low-carbon dispatch model
- **Statement**: There is no IES dispatch model that simultaneously quantifies flexibility supply/demand, balances multiple stakeholders' interests (operator, aggregator, EVs), and embeds a low-carbon (GCT-CET) mechanism.
- **Caused by**: O1, O2, O4.
- **Existing attempts**: Single-objective economic dispatch; Stackelberg / non-cooperative games for two entities (refs [21]–[23]); flexibility-only models (refs [13][14]).
- **Why they fail**: They drop either the flexibility objective or the multi-entity balance, so no single scheme trades economy against flexibility across all stakeholders.

### G2: Standard PSO cannot reliably solve the constrained multi-objective upper model
- **Statement**: Standard PSO converges slowly and to local optima on the heavily equality-constrained, multi-objective upper-level problem.
- **Caused by**: O3.
- **Existing attempts**: Plain PSO [28]; GA [27]; ADMM [26].
- **Why they fail**: Plain PSO lacks search-diversity control; particles cluster prematurely near the global-best under tight balance constraints.

## Key Insight
- **Insight**: Cast the IES dispatch as a bi-level (Stackelberg) problem — operator as leader optimizing revenue AND flexibility with a GCT-CET term (upper), aggregator cost + EV self-utility as followers (lower) — and solve the upper level with a diversity-enhanced PSO (adaptive inertia weight, sine-based learning factors, four sub-populations with distinct position-update rules) while CPLEX solves the linear lower level; couple the levels via prices (down) and quantities (up), and pick a compromise from the Pareto front with TOPSIS.
- **Derived from**: O1–O4.
- **Enables**: A single dispatch scheme that quantifiably trades economy for flexibility, balances three stakeholder classes, cuts carbon, and converges faster/closer than plain PSO/DBO.

## Assumptions
- A1: Park-level IES; typical-day (24-hour) deterministic forecasts for wind/solar and electric/heat/cooling loads (§4.1, ref [30]); no scenario-based stochasticity.
- A2: EVs are aggregated into 5 fixed categories with deterministic grid-connection windows, capacities, and proportions (Table 4).
- A3: The lower-level model is linear/convex enough for CPLEX 12.10 to solve to optimality each iteration.
- A4: Flexibility weights ω_e, ω_h, ω_q each in (0,1) and sum to 1 (Eq. 11); their concrete values are not specified in the paper.
- A5: Overall energy consumption of shiftable load is conserved within an operating cycle (§3.2.2).
