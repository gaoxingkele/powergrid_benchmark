# Problem Specification

## Observations

### O1: DAM and ASM decisions are interdependent but modeled separately
- **Statement**: Most UC/ED mathematical models focus on either the DAM or the ASM, overlooking the fact that decisions made in the former heavily constrain the latter. In traditional redispatch modeling, generator on/off status is fixed by the DAM, allowing only already-operating units to adjust in real-time markets.
- **Evidence**: §1, page 3; citations [22].
- **Implication**: RES stochasticity makes this rigidity unrealistic; UC status must be re-evaluated during ASM.

### O2: European zonal markets neglect intra-zonal congestion
- **Statement**: European zonal markets neglect congestion within a zone during the DAM phase, necessitating subsequent generation redispatch to maintain network security.
- **Evidence**: §1, page 3; citation [29].
- **Implication**: A two-stage approach (zonally cleared DAM → nodally redispatched ASM) is necessary to achieve feasible operation.

### O3: The NREL-118 system has a highly RES-dominated generation mix
- **Statement**: The NREL 118-Bus system has 327 units with 40.5 GW total installed capacity, including 11.0 GW CC, 3.6 GW CT, 2.5 GW ST, 10.2 GW non-dispatchable hydro, 8.5 GW DH, 1.0 GW WF, 3.4 GW PV, and other technologies. RES accounts for 31.2% of yearly generation.
- **Evidence**: §3, pages 11–12; Table 1, Table 2.
- **Implication**: RES variability drives the need for redispatch and reserve procurement.

### O4: Load and RES forecast errors between DAM and ASM can be substantial
- **Statement**: Load forecast error reaches ~10% of peak load (max 2987.9 MW), PV error up to 1223.8 MW, WF error up to 411.95 MW. The net forecast error (NFE) ranges from −3667.76 MW to +3312.48 MW.
- **Evidence**: §3, Table 3, page 14.
- **Implication**: The ASM must handle significant forecast deviations from DAM schedules.

### O5: DAM without UC constraints causes branch overloads
- **Statement**: DCLF analysis of DAM outcomes shows 11 branches experience overloads, most frequently on branches 31 and 32 (close to the cheapest units).
- **Evidence**: §4.1, Figure 7, page 15.
- **Implication**: The ASM redispatch must solve these network violations.

## Gaps

### G1: No sequential DAM-ASM model with internal UC re-evaluation in the European framework
- **Statement**: Existing models either co-optimize DAM and ASM (American framework) or treat ASM as a fixed-commitment redispatch. No sequential procedure allows the ASM to re-evaluate unit commitment (start-up/shut-down) based on updated forecasts and network needs within the European zonal DAM → nodal ASM structure.
- **Caused by**: O1, O2.
- **Existing attempts**: [19] defines three optimization problems for consecutive markets but fixes unit states from DAM; [6] compares market configurations but does not model sequential bid adjustments.
- **Why they fail**: They fix commitment decisions from the DAM stage, losing the flexibility to start up or shut down units in ASM.

### G2: Unit technical limits are not reflected in DAM→ASM bid transition
- **Statement**: There is no established mechanism to adjust ASM bids based on DAM outcomes and unit technical constraints (minimum power, MUT, MDT). Without such adjustment, ASM bids may be technically infeasible or economically inefficient.
- **Caused by**: O1.
- **Existing attempts**: [7] describes the Italian market structure but does not model the bid adjustment mathematically.
- **Why they fail**: They describe market operation but do not operationalize the bid adjustment as part of the optimization.

### G3: Benchmark comparison lacking for sequential vs co-optimized approaches under high RES
- **Statement**: Existing evaluations compare market designs at high level, but no quantitative comparison exists between the proposed sequential approach and a DAM-with-UC-and-reserve benchmark on a year-long, high-RES test case with hundreds of units.
- **Caused by**: O3, O4.
- **Existing attempts**: [32,33] formulate UC with reserve but apply to smaller systems or shorter horizons.
- **Why they fail**: They do not evaluate on a year-long horizon with 327 units and multi-zonal structure.

## Key Insight
- **Insight**: The sequential DAM→ASM interaction can be captured through a four-stage framework: (1) zonal DAM without UC constraints, (2) bid adjustment that maps DAM results to ASM-compatible bids through five operational cases based on unit DAM schedule vs technical limits, (3) DCLF and PTDF calculation to evaluate network impact of DAM schedules and redispatch actions, and (4) NCUCER MILP that simultaneously handles UC re-evaluation, forecast updates, branch flows, and SR procurement.
- **Derived from**: O1, O2, O4.
- **Enables**: A practical tool that lets TSOs evaluate ASM needs with realistic unit constraints and network physics, with only ~2.5 min/day computational burden.

## Assumptions
- A1: Load demand is inelastic with respect to price in the DAM.
- A2: DAM uses a zonal market clearing with step-wise bids and interzonal power flow constraints.
- A3: ASM uses a nodal approach with DC load flow (PTDF-based sensitivity factors with distributed slack bus).
- A4: DH units bid 90% of daily inlet energy in DAM and hold 10% for ASM (sensitivity case tests 85%/15%).
- A5: Time-varying ASM bid factors are derived from historical Italian market data due to similarity in RES impact and market structure.
- A6: Secondary Reserve Requirement (SRR) is determined via [44] and must be met exactly (equality constraint).
- A7: RES curtailment and load shedding are permitted only as last-resort actions with high penalty costs.
- A8: The daily ASM optimization has inter-temporal MUT/MDT continuity enforced via algorithms that link consecutive days.
