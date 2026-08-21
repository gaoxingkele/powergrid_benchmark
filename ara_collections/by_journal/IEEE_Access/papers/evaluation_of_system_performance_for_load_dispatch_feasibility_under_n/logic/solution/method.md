# Methodology — Five-Step Performance Assessment and Three-Case Study Design

Reflects Fig. 1 (proposed methodology), Fig. 2 (criticality/robustness estimation), and Fig. 3
(methodological framework). The method is a decision pipeline, not an algorithm with novel pseudocode;
the DA UC itself is solved by Dynamic Programming (see formulation.md, environment.md).

## Five-step methodology (§II)

### Step 1 — Identification of critical N-1 generator contingencies
N-1 contingency simulations are conducted for each thermal generator to identify outages that
significantly impact DA UC feasibility or economic performance.
- Contingency Impact Assessment: a generator outage is **critical** if it causes operational
  infeasibility or a substantial cost increase in the DA UC solution.
- DA UC Modeling: DA UC is formulated and solved by DP for all contingency scenarios; severity is
  assessed by incurred operational cost or failure to meet load.

### Step 2 — Identification of weak buses associated with critical contingencies
Weak buses are those most sensitive to associated failures (susceptible to overloads/operational
stress under critical contingencies); generally connected to or impacted by the failed units. This
extends contingency analysis to the spatial dimension of the network.

### Step 3 — Estimation of system robustness and identification of robust buses
- Stable Contingency Classification: outages that do not disrupt UC feasibility and/or do not increase
  cost significantly are **stable**.
- Robust Bus Identification: buses connected to generators under stable contingencies are **robust** —
  they can absorb outages with minimal impact.

### Step 4 — Reliability estimation using LOLP
LOLP is computed for each scenario from the probabilistic modeling of generator unavailability
(COPT), reflecting the likelihood that the system fails to meet demand under given contingencies and
reserve conditions.

### Step 5 — Evaluation of the operating margin
The operating margin $M_{da}^o = LOLP_{max} - LOLP$ measures additional capacity beyond committed
reserves. Positive → headroom for additional load/contingencies; negative → risk of dispatch failure.

## Decision flow (Fig. 1 / Fig. 2)
Forced outage of a single unit → check DA UC feasibility (supply-demand metric):
- **Feasible & economic DA UC** → determine DA UC costs → identify stable contingencies → identify
  robust buses ⇒ **System Robustness**.
- **Relatively feasible but uneconomic DA UC** (higher costs) → identify critical contingencies →
  identify weak buses ⇒ **System Criticality**.
- **Critical system operation, DA UC not possible** → identify severe contingencies → identify weakest
  buses.
Then: System Reliability estimation (LOLP) → System Operating Reliability margin.

## Three-case study design (Table 1, §IV, §VI)
- **Base Case**: DA UC cost determination for IEEE RTS at forecasted load, without contingencies.
  Available dispatch capacity 2795 MW (10% SR reference).
- **Case 1**: DA UC cost determination in the presence of all possible N-1 generator contingencies
  with CM = 10% (CM 310.5 MW). Weak/robust buses identified; contingencies ranked by percentage cost
  rise (weak buses increasing, robust buses reverse).
- **Case 2**: DA UC costs with CM variation in steps from the reserve down to zero percent,
  incorporating all N-1 contingencies:
  - 2(a) 8% CM (248 MW), dispatch capacity 2857 MW
  - 2(b) 5% CM (155 MW), dispatch capacity 2950 MW
  - 2(c) 0% CM (0 MW), dispatch capacity 3105 MW (all generators loaded to full capacity)

## Two-stage analysis (Fig. 3)
1. Stage 1 — assess N-1 contingency-based DA UC (criticality + robustness) vs Base Case.
2. Stage 2 — validate via LOLP reliability + operating-margin evaluation over the 24 hours, for Case 1
   and Case 2(a),(b),(c).
The joint outcome determines load-dispatch feasibility for the next day and the corrective actions
(e.g., alternate generation installation, preferably at identified critical buses).

## Contingency indexing (Fig. 5)
Nine N-1 generator contingencies are indexed $Cy_k = 1..9$ in ascending order of the bus number where
the outaged generator sits: Cy1 = bus 1 (20 MW), Cy2 = bus 2 (76 MW), Cy3 = bus 7 (100 MW),
Cy4 = bus 13 (197 MW), Cy5 = bus 15 (12 MW), Cy6 = bus 18 (400 MW), Cy7 = bus 21 (400 MW),
Cy8 = bus 23 (155 MW), Cy9 = bus 23 (350 MW).
