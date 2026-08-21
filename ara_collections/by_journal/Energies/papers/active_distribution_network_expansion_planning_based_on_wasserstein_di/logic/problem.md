# Problem Specification

## Observations

### O1: Traditional ADN expansion planning treats lines and interconnection devices separately
- **Statement**: Existing distribution network expansion planning methods typically consider only line (feeder) construction as the primary expansion decision, ignoring the joint optimization of lines with flexible interconnection devices (SOPs) and rigid interconnection switches.
- **Evidence**: Section 1 (Introduction), Sections 2.1, 5.2.
- **Implication**: Siloed planning may lead to suboptimal investment: installing expensive new lines where existing feeders could be coupled by SOPs/switches at lower cost, or deploying SOPs where a simple switch suffices.

### O2: DG and load uncertainty is growing and cannot be ignored in planning
- **Statement**: The high penetration of distributed generation (especially wind and solar) introduces significant uncertainty in both generation and load profiles, requiring the planning model to account for a wide range of operational scenarios, not just a single forecast snapshot.
- **Evidence**: Section 1, Section 3.1 (ambiguity set), Section 5.1 (DG nodes list).
- **Implication**: Deterministic planning that assumes perfect foresight of DG/load yields unrealistic ("too ideal") results; stochastic or robust planning frameworks are needed.

### O3: Wasserstein distance provides a data-driven ambiguity set without parametric assumptions
- **Statement**: The Wasserstein distance metric defines a ball around the empirical distribution of historical DG/load scenarios; any distribution within that ball is considered plausible. This avoids assuming a specific parametric family (e.g., Gaussian) for the uncertain parameters and allows the radius to control conservativeness.
- **Evidence**: Section 3.1 (Wasserstein distance ambiguity set), Section 5.5 (Figure 9).
- **Implication**: The model's out-of-sample performance can be tuned via the Wasserstein radius, trading off between robustness (larger radius) and economy (smaller radius).

### O4: The full three-stage reformulation pipeline makes the problem tractable
- **Statement**: The original distributionally robust MINLP is transformed into a tractable MISOCP through (a) SOCP relaxation of AC power flow, (b) Lagrange duality of the inner worst-case expectation, and (c) McCormick relaxation of bilinear terms.
- **Evidence**: Section 4 (model transformation), Sections 4.2, 4.3, 4.4.
- **Implication**: The reformulation is exact under sufficient conditions (exactness of SOCP relaxation on radial networks); no heuristic approximations are introduced.

## Gaps

### G1: No existing planning model jointly optimizes lines + SOPs + interconnection switches under distributional ambiguity
- **Statement**: Prior work considers either (a) SOP-only planning, (b) tie-switch-only reconfiguration, or (c) line expansion with a single device type. None consider the collaborative selection of both SOPs and interconnection switches as alternative interconnection options under distributionally robust DG/load uncertainty.
- **Caused by**: O1, O2.
- **Existing attempts**: SOP planning models [5-8]; interconnection switch planning [9-12]; deterministic/stochastic line expansion [15-20]; robust optimization for ADN [22-25]. Each addresses only a subset of the full problem.
- **Why they fail**: By not considering both device types, prior work cannot determine the optimal mix of flexible (SOP) vs rigid (switch) interconnection devices for a given network, cost environment, and uncertainty level.

### G2: Distributionally robust ADN planning models are computationally demanding MINLPs
- **Statement**: Even with a single device type, distributionally robust ADN planning models are bi-level min-max-min MINLPs that are intractable for direct solution. Existing solution methods either use strong assumptions (small scenario sets, simplified network models) or heuristic approaches.
- **Caused by**: O2, O4.
- **Existing attempts**: [27-29] use various relaxation techniques but for simpler problems.
- **Why they fail**: The combination of Wasserstein-distance DRO, AC power flow, and discrete device choices produces a model that is both non-convex and combinatorial; a systematic reformulation pipeline is needed.

## Key Insight
- **Insight**: By casting the collaborative line/SOP/switch planning problem as a Wasserstein-distance-based distributionally robust optimization and applying a three-stage exact reformulation (SOCP + Lagrange duality + McCormick), the intractable MINLP is converted to a single-level MISOCP solvable by CPLEX. The collaborative approach yields measurably higher economic return than any single-device-type strategy, and the DRO formulation outperforms both deterministic (fragile) and traditional robust (overly conservative) approaches on out-of-sample metrics.
- **Derived from**: O1, O2, O3, O4.
- **Enables**: Practical joint planning of lines, SOPs, and interconnection switches under distributional ambiguity, with a rigorous convexity-preserving transformation that commercial solvers can handle.

## Assumptions
- A1: The radial (or weakly meshed) distribution network satisfies the SOCP exactness conditions (sufficient: radial topology, no reverse power flow at substations).
- A2: The Wasserstein distance radius epsilon can be chosen empirically (e.g., via cross-validation on historical data) to balance conservativeness and economy.
- A3: The 24-hour typical-scenario reduction adequately represents the annual DG/load variation for planning purposes.
- A4: A 20-year project horizon at 3% discount rate is a reasonable assumption for distribution network planning.
- A5: Device investment costs, O&M costs, and electricity prices are known and fixed over the planning horizon (no escalation modeled).
