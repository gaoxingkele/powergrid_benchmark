# Constraints, Assumptions, and Known Limitations

## Mathematical Constraints (from Section 3.2.2)

### C1: Investment Amount Constraint
sum(i * AMOi) <= AMO0 for i = 1 to p
- AMOi = investment amount of i-th project (in CNY, values in Table 9)
- AMO0 = upper boundary of company investment amount (default = 1500)
- Binding constraint in sensitivity analysis (Figure 7)

### C2: Power Demand Constraint
sum(i * TPi) >= D for i = 1 to p
- TPi = transmission power of i-th project (in appropriate units)
- D = power demand threshold (default = 600)
- Binding constraint in sensitivity analysis (Figure 8)

### C3: Low-Carbon (CO2 Emission Reduction) Constraint
sum(i * CERi) >= CER0 for i = 1 to p
- CERi = carbon dioxide emission reduction of i-th project
- CER0 = lower boundary of emission reduction (default = 5000)
- Binding constraint in sensitivity analysis (Figure 9)

## Decision Variables
- i = binary variable for i-th project (1 = invest, 0 = do not invest)
- p = total number of candidate projects (10 in the empirical study)

## Objective Function
max f = sum(i * Bi) / sum(i * Ri)
- Bi = comprehensive benefit score from TOPSIS evaluation (Stage 1)
- Ri = comprehensive risk score from TOPSIS evaluation (Stage 1)

## Assumptions

**A1 - Expert Sufficiency:** Five experts (government, enterprise, university) provide adequate domain knowledge for comprehensive risk and benefit indicator weighting.
**A2 - Indicator Coverage:** The nine risk indicators (4 dimensions) and nine benefit indicators (4 dimensions) collectively cover all relevant PGI evaluation dimensions.
**A3 - Qualitative Scoring Validity:** Expert scoring on a 1-9 scale adequately captures qualitative indicator performance.
**A4 - Bayesian Model Correctness:** The multinomial probability distribution and hierarchical Bayesian model correctly represent the group decision-making process for indicator weighting.
**A5 - ILA Parameter Appropriateness:** ILA solver parameters from Ref. [59] are suitable for the PGI optimization problem.
**A6 - Project Representativeness:** Ten projects from one company's database are representative of typical PGI decisions.
**A7 - Constraint Sufficiency:** The three constraints (investment amount, power demand, low-carbon) are the binding constraints and adequately capture the real-world PGI decision context.
**A8 - Independence:** Projects are independent (no interaction effects in combined investment).
**A9 - Deterministic inputs:** All input parameters (AMOi, TPi, CERi, Bi, Ri) are known with certainty (no stochastic modeling).
**A10 - Linear constraint satisfaction:** The constraint satisfaction checking does not account for time dynamics or multi-period planning.

## Known Limitations (from Section 6.2)

**L1 - Small Sample Size:** Only 10 planned investment projects from a single power-grid company are analyzed. During the 14th Five Year Plan period, total national power grid investment is expected to be nearly CNY 3 trillion, far exceeding the investment amount analyzed.
**L2 - Limited Project Library:** A larger project library would yield more complex and potentially more optimal investment portfolios.
**L3 - Missing Investment Direction:** When sample size increases, investment direction (grid reinforcement vs. power supply vs. channel construction) must also be considered as a key factor.
**L4 - Single-period Optimization:** The model is a single-period static optimization, not a multi-period dynamic planning framework.
**L5 - No Uncertainty Handling:** Input data (costs, benefits, demand, carbon targets) are treated as deterministic; no stochastic or robust optimization is applied.
**L6 - Limited Comparative Validation:** Due to data limitations, the authors could not use external literature datasets for comparative analysis and relied on scenario analysis using their own dataset.
**L7 - Qualitative Subjectivity:** Risk indicators are qualitative, and their scoring depends on expert judgment which may vary across contexts.
