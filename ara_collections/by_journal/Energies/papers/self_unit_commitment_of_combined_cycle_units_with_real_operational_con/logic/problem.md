# Problem Specification

## Observations

### O1: CCGTs are dispatched by heuristic codes that omit real operating constraints
- **Statement**: In Colombia, when given an initial dispatch by the ISO, CCGT plants (including TEBSA, the largest, with a 5 × 2 configuration = 5 gas turbines + 2 steam turbines) are operated from heuristic simulation codes that omit hot/warm/cold startup ramps, the minimum gas-turbine operating hours needed to start a steam turbine, the steam-to-gas unit-count relationship, load distribution among gas turbines, and supplementary fires.
- **Evidence**: §1.1 Motivation; Abstract.
- **Implication**: The dispatch handed to operators may be physically infeasible for the plant to follow.

### O2: Ignoring thermal-state startup constraints causes equipment damage
- **Statement**: TEBSA's operations often assume a hot startup condition or overlook the minimum number of gas units needed for steam turbine operation, leading to preventable equipment issues (blade erosion / thermo-mechanical fatigue).
- **Evidence**: §1.1; Figure 1 (blade erosion photographs); refs [4–7].
- **Implication**: Steam quality (temperature/pressure) must be guaranteed via correct startup sequencing to avoid rotor damage.

### O3: Deviations from the ISO program are financially penalized
- **Statement**: Per Colombian market rules [25], deviations exceeding five percent between the heuristic and actual generation are penalized; the modelled deviation implies daily penalties on the order of tens of thousands of USD per plant.
- **Evidence**: §3.1, §3.2 (Case I ≈ USD 60,957/day; Case II ≈ USD 66,093/day); refs [25].
- **Implication**: A dispatch the plant cannot follow imposes recurring, substantial cost and requires costly balancing reserves.

### O4: Existing UC models represent CCGTs either by mode/configuration or by individual components, but not the missing real constraints
- **Statement**: Literature models CCGTs either as configurations/modes [2,14–22] or as individual gas/steam components [8–13], capturing standard constraints (startup/shutdown, up/down ramps, sometimes supplementary fires) but typically omitting minimum gas-operating-hours-to-start-steam and load distribution.
- **Evidence**: §1.2 Literature Review.
- **Implication**: A hybrid model combining component and mode representations is needed to add the missing constraints.

## Gaps

### G1: No UC model captures the minimum gas-turbine operating hours required to start a steam turbine
- **Statement**: The temperature/pressure prerequisite that gas turbines must run a minimum number of hours before a steam turbine can start is, to the authors' knowledge, not previously included in UC models.
- **Caused by**: O1, O2, O4
- **Existing attempts**: Component models [8,9] capture GT–ST interdependence but not minimum startup hours or hot/cold differentiation.
- **Why they fail**: They omit the thermal-coupling timing constraint, so their dispatch can start steam turbines under invalid thermal conditions.

### G2: No UC model enforces load distribution among gas turbines
- **Statement**: Uneven gas-turbine loading produces uneven steam thermal characteristics through the common collector, causing rotor temperature gradients and long-term damage — but existing models do not constrain it.
- **Caused by**: O2, O4
- **Existing attempts**: None known for CCGTs.
- **Why they fail**: Aggregate/mode models cannot even express per-unit gas-turbine output differences.

### G3: Aggregate CCGT representations cannot yield a followable, unit-level dispatch
- **Statement**: Heuristic/aggregate models represent the CCGT output in bulk and cannot detail individual gas/steam turbine contributions, so the ISO cannot verify feasibility or grid support.
- **Caused by**: O1, O3, O4
- **Existing attempts**: Configuration/mode MIP models [2,14,18].
- **Why they fail**: They abstract away the per-unit coupling that determines real feasibility.

## Key Insight
- **Insight**: Modelling the CCGT as separate individual gas and steam turbine units — while embedding configuration-style coupling constraints (minimum gas units and minimum gas operating hours to start steam, hot/cold steam startup, load distribution, supplementary fires) — produces a self-unit-commitment MIP whose dispatch the plant can actually follow in real time.
- **Derived from**: O1, O2, O4
- **Enables**: A hybrid component+mode SEUC formulation that closes G1–G3 and avoids penalties/equipment damage.

## Assumptions
- A1: A constant steam-to-gas output factor (STF) is assumed (variable ratios left to future work). [§2.3.2]
- A2: Steam quality is maintained when the modelled operational constraints are met (HRSG supplementary fires assumed to preserve steam quality). [§1.2]
- A3: Reactive power is not directly modelled; only active power per unit is produced (usable downstream in power-system analysis software). [§1.1]
- A4: For the case studies, all NC gas turbines are identical and all NS steam turbines are identical. [§3]
- A5: Hourly dispatch resolution, matching the Colombian market. [§1.2]
