# Problem Analysis

## Observations

- **O1**: China's investment in power engineering construction exceeded CNY 1222 billion in 2022, with CNY 501.2 billion for power grids. Investors face various risks from technical, policy, management, and environmental factors during electrical infrastructure investment. (Source: Abstract, Section 1)
- **O2**: Existing PGI optimization studies primarily concentrate on financial aspects and have not adequately considered the risk and benefit factors together. Most focus on investment demand, capacity, financial hazards (VaR/CVaR), and financial benefits, with less attention to operational, social, and environmental benefits. (Source: Section 1, Table 1)
- **O3**: With a growing number of indicators, model computation time frequently increases and the ideal solution sometimes cannot be found. Converting various risk and benefit indicators into "comprehensive risk" and "comprehensive benefit" using MCDM models is more practical. (Source: Section 1)
- **O4**: The Bayesian BWM approach introduces probability distribution via Bayesian theory, more accurately capturing the process of numerous experts' collaborative decision-making and weighting in a group environment compared to traditional BWM. (Source: Section 3.1.1)
- **O5**: The ILA model has higher accuracy and reasonable computation time than 19 other algorithms when dealing with 73 constrained, unconstrained, small, and large problems. (Source: Section 3.2.3)
- **O6**: The empirical analysis involves 10 projects from a power-grid company's investment project database with 9 risk indicators and 9 benefit indicators. (Source: Section 4.1, Table 4)
- **O7**: Policy risks (project approval R11, energy/electricity policy adjustment R12) received the highest risk indicator weights. Operational benefits (electricity transmission B11, load rate B13, power supply reliability B12) received the highest benefit indicator weights. (Source: Sections 4.2.1, 4.3.1, Tables 6, 8)
- **O8**: The optimal investment portfolio under the benchmark scenario includes P2, P5, P7, P8, and P9. P7, P8, and P9 with high benefit-risk ratios are consistently included across different constraint conditions. (Source: Sections 4.4, 5.2)
- **O9**: Single-objective approaches (risk minimization only or benefit maximization only) produce inferior outcomes: risk-only reduces benefits by 37.27%; benefit-only increases risks by 89.86%. (Source: Section 5.1.1, Table 11)

## Gaps

- **G1**: Existing PGI studies lack a systematic framework that jointly evaluates both risk and benefit dimensions in a two-stage optimization pipeline rather than a single multi-objective formulation.
- **G2**: Traditional BWM does not account for group decision-making variability; mechanized weight-averaging produces extreme weight phenomena where some indicators become nearly decisive while others become meaningless.
- **G3**: There is limited sensitivity analysis on how varying investment amount, power demand, and low-carbon constraints affect the optimal PGI portfolio composition.

## Key Insight

A two-stage PGI optimization model that first computes comprehensive risk and benefit scores via Bayesian BWM-TOPSIS, then maximizes the benefit-per-unit-risk ratio under investment, demand, and carbon constraints, provides a more balanced and rational investment portfolio than either single-objective optimization or traditional weighting methods alone.

## Assumptions

- **A1**: The expert group of five (government regulator, enterprise practitioner, two power-grid employees, one professor) provides sufficient domain expertise for indicator weighting.
- **A2**: The nine risk indicators (policy, management, technical, environmental) and nine benefit indicators (operational, financial, cleanliness, social) comprehensively cover all relevant PGI evaluation dimensions.
- **A3**: Qualitative indicator performance is adequately captured via expert scoring on a 1-9 scale.
- **A4**: The Bayesian BWM multinomial probability distribution model correctly captures the indicator weighting process.
- **A5**: ILA solver parameters following Ref. [59] are appropriate for this PGI optimization problem.
- **A6**: The ten projects from the company database are representative of typical PGI decisions.
- **A7**: The three constraints (investment amount, power demand, low-carbon) are the binding constraints for PGI optimization.
