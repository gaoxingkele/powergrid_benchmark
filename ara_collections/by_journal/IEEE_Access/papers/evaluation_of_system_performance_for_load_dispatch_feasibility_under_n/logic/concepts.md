# Concepts

## Day-Ahead Unit Commitment (DA UC)
- **Notation**: $C_{Tot}$ (total cost objective)
- **Definition**: The optimal scheduling of turning generation units 'on'/'off' over the 24 hours of the next day to meet forecasted demand at lowest cost, subject to operational constraints. Objective (Eq. 1): $C_{Tot} = \sum_{i=1}^{n}\sum_{t=1}^{T}(F_{i,t}u_{i,t} + StC_{i,t}u_{i,t} + SdC_{i,t}u_{i,t})$, the aggregation of fuel, start-up, and shutdown costs of all committed generators.
- **Boundary conditions**: Formulated for thermal generators; maintenance cost neglected; DC power flow assumed. Solved here by Dynamic Programming.
- **Related concepts**: N-1 Generator Contingency, Spinning Reserve, Contingency Margin

## N-1 Generator Contingency
- **Notation**: contingency index $Cy$ (or $Cy_k$)
- **Definition**: The forced outage of a single generating unit at one time (a single-entity outage). N-1 analysis is distinguished from N-2 (two concurrent outages) and N-k (k outages). In this paper nine distinct generator contingencies are indexed $Cy_k = 1..9$ in ascending order of the bus number where generators are installed.
- **Boundary conditions**: Only one unit fails at a time; no simultaneous outages of differently-rated units; conditional probabilities between generators not modeled.
- **Related concepts**: Day-Ahead Unit Commitment, System Criticality, Contingency Index

## Contingency Margin (CM)
- **Notation**: $M_{da}^{k} = \sum_{i=1}^{n} R_i^{k}$ (Eq. 9)
- **Definition**: The reserve capacity that can be activated promptly to address unanticipated events, evaluated for contingency 'Cy' after aggregating the spinning-reserve contributions $R_i$ of all thermal generators. Serves as the implementation indicator of system performance. Values used: 310.5 MW (10% SR), 248 MW (8%), 155 MW (5%), 0 MW (0%).
- **Boundary conditions**: Tied to the spinning-reserve constraint $R_t \ge 0.1\,R_i$ (Eq. 7) in Case 1; reduced stepwise in Case 2.
- **Related concepts**: Spinning Reserve, Operating Margin, Available Capacity

## Spinning Reserve (SR)
- **Notation**: $R_t$, $R_i$
- **Definition**: The 'generation reserve' — unutilized generation capacity that serves as backup during power shortages or generator failures, typically maintained at ten percent of the operating reserve. Constraint (Eq. 7): $R_t \ge (0.1 * R_i)$.
- **Boundary conditions**: Swept 10%→8%→5%→0% across the case studies; not allocated in normal operation but reserved for contingency/forced outage.
- **Related concepts**: Contingency Margin, Available Capacity

## System Criticality
- **Notation**: —
- **Definition**: An assessment of system vulnerability identifying critical contingencies (generator outages that cause operational infeasibility or substantial cost increases) and the corresponding weak buses (most sensitive to associated failures). Weak buses are ranked by percentage rise in UC cost.
- **Boundary conditions**: Determined when DA UC is uneconomical/infeasible under an outage; weak buses connected to or impacted by failed units.
- **Related concepts**: System Robustness, Weak Bus, Critical Contingency

## System Robustness
- **Notation**: —
- **Definition**: The extent to which the system can withstand adverse events; quantified by identifying stable contingencies (outages that do not disrupt UC feasibility and/or do not increase cost significantly) and the corresponding robust buses (buses connected to generators under stable contingencies).
- **Boundary conditions**: Robust buses demonstrate the system's inherent ability to absorb disturbances without compromising operational integrity.
- **Related concepts**: System Criticality, Robust Bus, Stable Contingency

## Loss of Load Probability (LOLP)
- **Notation**: $LOLP_{k,t}$, $LOLP_t$, $LOLP$
- **Definition**: A probabilistic reliability index equal to the probability that forecasted demand exceeds available generation. Per-hour per-contingency (Eq. 11): $LOLP_{k,t} = Prob[D_{f,t} > \sum_{i=1}^{N}(P_{i,t}u_{i,t})]$; aggregated over 24 hours (Eq. 13): $LOLP = \sum_{t=1}^{24} LOLP_{k,t}$. Non-zero only when available capacity < forecasted demand for some hour.
- **Boundary conditions**: Assessed for forced outage of only one generating unit at a time; compiled in a Capacity Outage Probability Table (COPT). Maximum prescribed limit $LOLP_{max}$ (Eq. 10): $LOLP_k \le LOLP_{max}$.
- **Related concepts**: LOLP_max, COPT, Operating Margin

## LOLP_max (Maximum allowable LOLP)
- **Notation**: $LOLP_{max}$
- **Definition**: The regulatory maximum acceptable loss-of-load probability. Taken as 0.05 per the Central Electricity Authority (CEA) of India; the US Department of Energy specifies 0.002 (≈0.1/year) and the European Union 0.008. This study uses 0.05.
- **Boundary conditions**: Reference for computing the operating margin and for judging reliability.
- **Related concepts**: LOLP, Operating Margin

## Operating Margin
- **Notation**: $M_{da}^{o} = (LOLP_{max} - LOLP)$ (Eq. 15)
- **Definition**: A newly proposed metric measuring the system's additional capacity beyond committed reserves, capable of absorbing future contingencies. A positive margin indicates headroom for additional load/contingencies; a negative margin implies risk of dispatch failure/collapse.
- **Boundary conditions**: Computed from the aggregated 24-hour LOLP and the fixed LOLP_max; does not capture severity of any individual single contingency.
- **Related concepts**: LOLP, LOLP_max, Contingency Margin

## Capacity Outage Probability Table (COPT)
- **Notation**: —
- **Definition**: A table compiling, for each single-unit outage (contingency index), the total capacity available after the generator outage and the probability of generation unavailability, derived from failure rate and repair rate. Used to compute hourly LOLP.
- **Boundary conditions**: Built per case (Case 1: Table 7; Case 2: Table 8) for single-unit outages only.
- **Related concepts**: LOLP, Failure Rate, Mean Time To Failure

## Failure Rate and Mean Time To Failure (FR, MTTF)
- **Notation**: $\lambda$, $t_{FR}$; relation (Eq. 16): $\lambda = 1/t_{FR}$
- **Definition**: MTTF ($t_{FR}$) is the mean time to failure of a generating unit; failure rate $\lambda$ is its reciprocal. Per-capacity values are tabulated (Table 3) and used to compute generation-unavailability probabilities in the COPT.
- **Boundary conditions**: Referenced from reliability-evaluation literature; assigned by generator capacity class.
- **Related concepts**: COPT, LOLP

## Available Capacity for Dispatch ($P^{avl}$)
- **Notation**: $P^{avl} = \sum_{i=1}^{n}(P_i^{max} - R_i)$ (Eq. 8)
- **Definition**: The total system capacity available for DA UC / load dispatch, obtained by subtracting the operating (spinning) reserve from the maximum capacity of all units. On IEEE RTS: 2795 MW at 10% SR (Base Case & Case 1), 2857 MW (8%), 2950 MW (5%), 3105 MW (0%).
- **Boundary conditions**: Determined by the reserve policy; the reference against which post-outage feasibility and LOLP are judged.
- **Related concepts**: Spinning Reserve, Contingency Margin, LOLP
