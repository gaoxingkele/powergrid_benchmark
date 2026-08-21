# Experiments

## E01: Bayesian BWM vs Traditional BWM Weight Comparison

**Verifies:** C01 (Bayesian BWM yields more stable weights), C04 (policy risks dominate), C05 (operational benefits dominate)

**Evidence:** Tables 6, 8, 12, 13; Section 5.1.2

**Run:** Scenario 2 (BWM-based indicator weighting) vs Scenario 0 (Bayesian BWM indicator weighting)

**Setup:**
- Five experts provide BO and OW vectors for 9 risk indicators and 9 benefit indicators
- Bayesian BWM: hierarchical Bayesian model estimates group-aggregated posterior weights
- Traditional BWM: individual BWM weights computed per expert, then averaged
- Dataset: same qualitative indicator scores (Table 4) and expert comparison vectors

**Procedure:**
1. Expert group determines best and worst risk indicators (Table 5) and benefit indicators (Table 7)
2. BO vector (AB) and OW vector (AW) constructed for each expert (matrices in Sections 4.2.1 and 4.3.1)
3. Bayesian BWM computes weights via multinomial probability distribution and hierarchical Bayesian estimation (Equation 8)
4. Traditional BWM computes weights per expert using standard BWM linear model
5. Weight ranges compared: max weight minus min weight for each method
6. Weight differences computed as percentage: (BWM range - Bayesian BWM range) / Bayesian BWM range

**Metrics:**
- Weight range (max indicator weight - min indicator weight) for each method
- Percentage reduction in weight extremeness achieved by Bayesian approach
- Ranking consistency between the two methods

**Expected outcome:** The Bayesian BWM weight range is narrower than the traditional BWM range, indicating more balanced weight distribution. Policy risk indicators (R11, R12) consistently rank highest regardless of method. Operational benefit indicators (B11, B13, B12) consistently rank highest.

**Baselines:** Traditional BWM without group decision-making (scenario 2a/2b in the paper)

**Dependencies:** A1, A2, A3, A4

---

## E02: Benefit-per-Unit-Risk vs Single-Objective Optimization Comparison

**Verifies:** C02 (benefit-per-unit-risk yields more balanced portfolios)

**Evidence:** Table 11; Section 5.1.1

**Run:** Scenario 0 (this paper's objective), Scenario 1a (risk minimization), Scenario 1b (benefit maximization)

**Setup:**
- Same 10 projects with same risk and benefit scores from Stage 1
- Same constraints: investment amount <= 1500, power demand >= 600, CO2 reduction >= 5000
- Three different objective functions tested independently

**Procedure:**
1. Scenario 0: maximize f = sum(i * Bi) / sum(i * Ri) (benefit per unit risk)
2. Scenario 1a: minimize total risk = sum(i * Ri) (single-objective risk minimization)
3. Scenario 1b: maximize total benefit = sum(i * Bi) (single-objective benefit maximization)
4. Each scenario solved using ILA solver with identical parameter settings
5. Results compared on: investment portfolio composition, total risk score, total benefit score

**Metrics:**
- Total risk = sum of comprehensive risk scores for selected projects
- Total benefit = sum of comprehensive benefit scores for selected projects
- Portfolio composition (which projects selected)
- Relative change in benefit: (benefit_scenario - benefit_scenario0) / benefit_scenario0
- Relative change in risk: (risk_scenario - risk_scenario0) / risk_scenario0

**Expected outcome:** Scenario 0 selects a mix of 5 projects balancing risk and benefit. Scenario 1a selects fewer projects (2) with very low total risk but substantially lower total benefit. Scenario 1b selects many projects (9) with high total benefit but substantially higher total risk. The benefit-per-unit-risk ratio for Scenario 0 is higher than for either single-objective scenario.

**Baselines:** Scenario 1a (risk minimization only), Scenario 1b (benefit maximization only)

**Dependencies:** A5, A6, A7

---

## E03: ILA Solver vs Genetic Algorithm Comparison

**Verifies:** C03 (ILA achieves superior results with less computation time)

**Evidence:** Table 14; Section 5.1.3

**Run:** ILA (Scenario 0) vs GA solver on the same PGI optimization problem

**Setup:**
- Same 10 projects, same risk/benefit scores, same objective function (benefit per unit risk)
- Same constraints: investment amount <= 1500, power demand >= 600, CO2 reduction >= 5000
- ILA: solver with parameters following Ref. [59] settings
- GA: MATLAB built-in GA toolbox with system default parameter settings

**Procedure:**
1. ILA solver applied to the PGI optimization problem
2. GA solver (MATLAB toolbox) applied to identical problem
3. Optimal value (f = benefit/risk ratio) recorded for each solver
4. Investment portfolio (selected projects) recorded for each solver
5. Computing time measured for each solver

**Metrics:**
- Optimal value (objective function f)
- Investment portfolio selected
- Computing time in seconds
- Percentage improvement: (ILA_value - GA_value) / GA_value
- Time reduction: (GA_time - ILA_time) / GA_time

**Expected outcome:** ILA achieves a higher optimal value (benefit/risk ratio) than GA and requires substantially less computation time. The portfolios selected may differ, with ILA selecting a portfolio achieving superior objective value.

**Baselines:** Genetic Algorithm (MATLAB toolbox)

**Dependencies:** A5, A6

---

## E04: Sensitivity Analysis of Investment Amount Constraint

**Verifies:** C02

**Evidence:** Figure 7; Section 5.2.1

**Run:** Investment amount upper bound (AMO0) varied from 300 to 1800

**Setup:**
- All other constraints fixed (power demand >= 600, CO2 reduction >= 5000)
- Upper limit of total investment amount adjusted incrementally
- Same 10 projects with same risk/benefit scores

**Procedure:**
1. Set AMO0 = 300, solve ILA optimization
2. Increment AMO0 to 600, 900, 1200, 1500, 1800
3. At each level, record which projects are selected and whether constraints can be met
4. Identify threshold where constraints become feasible/infeasible

**Metrics:**
- Investment portfolio composition at each budget level
- Feasibility (whether power demand and low-carbon constraints can be met)
- Investment amount threshold for constraint satisfaction

**Expected outcome:** At low budgets (300-900), it is infeasible to meet power demand or low-carbon constraints. At AMO0 = 1200, P7 and P9 (high benefit-risk ratio) are preferred despite P8's higher ratio (its investment amount is too high). At AMO0 >= 1500, the optimal portfolio stabilizes.

**Baselines:** Benchmark scenario (AMO0 = 1500)

**Dependencies:** A5, A6, A7

---

## E05: Sensitivity Analysis of Power Demand Constraint

**Verifies:** C02

**Evidence:** Figure 8; Section 5.2.2

**Run:** Power demand lower bound (D) varied from 300 to 1800

**Setup:**
- All other constraints fixed (investment amount <= 1500, CO2 reduction >= 5000)
- Power demand threshold D adjusted incrementally
- Same 10 projects with same risk/benefit scores

**Procedure:**
1. Set D = 300, solve ILA optimization
2. Increment D to 600, 900, 1200, 1500, 1800
3. At each level, record which projects are selected and whether constraints can be met

**Metrics:**
- Investment portfolio composition at each demand level
- Feasibility of meeting constraints
- Demand threshold where investment amount constraint becomes binding

**Expected outcome:** At low demand (300-900), P7, P8, P9 are essential investments, with P2, P3, P5 as alternatives. At demand >= 1200, the existing investment amount constraint (1500) becomes binding and infeasible.

**Baselines:** Benchmark scenario (D = 600)

**Dependencies:** A5, A6, A7

---

## E06: Sensitivity Analysis of Carbon Emission Reduction Constraint

**Verifies:** C02

**Evidence:** Figure 9; Section 5.2.3

**Run:** CO2 emission reduction lower bound (CER0) varied from 2000 to 7000

**Setup:**
- All other constraints fixed (investment amount <= 1500, power demand >= 600)
- CO2 reduction threshold CER0 adjusted incrementally
- Same 10 projects with same risk/benefit scores

**Procedure:**
1. Set CER0 = 2000, solve ILA optimization
2. Increment CER0 to 3000, 4000, 5000, 6000, 7000
3. At each level, record which projects are selected and whether constraints can be met

**Metrics:**
- Investment portfolio composition at each CO2 reduction level
- Feasibility of meeting constraints
- CO2 threshold where investment amount constraint becomes binding

**Expected outcome:** When environmental constraints are slack (CER0 <= 4000), P7, P8, P9 are stable PGI directions. When tight (CER0 >= 6000), P7 (which trades high investment for high environmental benefits) may be dropped. At CER0 = 7000, the existing investment amount constraint becomes binding and infeasible.

**Baselines:** Benchmark scenario (CER0 = 5000)

**Dependencies:** A5, A6, A7
