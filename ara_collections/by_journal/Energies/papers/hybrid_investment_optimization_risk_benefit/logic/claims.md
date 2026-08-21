# Claims

## C01: Bayesian BWM yields more stable indicator weights than traditional BWM by incorporating group decision-making

**Statement:** The Bayesian BWM method produces less extreme weight distributions across indicators compared to traditional BWM, because the probabilistic group decision-making framework mitigates individual expert bias and avoids mechanized weight averaging.

**Conditions:** When 5 or more experts provide BO/OW vectors for a set of criteria, and the Bayesian hierarchical model is used to estimate the posterior weight distribution rather than direct averaging of individual BWM results.

**Sources:**
- Section 5.1.2: "the weight difference between the most important and least important risk indicators is 0.2197 using the BWM method, which is 48.15% higher than the weight difference calculated using the Bayesian BWM method"
- Section 5.1.2: "the weight difference between the most important and least important benefit indicators is 0.2133 using the BWM method, which is 40.42% higher than the weight difference calculated using the Bayesian BWM method"
- Section 5.1.2: "Without considering group decision-making, extreme weight phenomena can easily occur via mechanized weight-averaging processing"

**Status:** Supported by evidence

**Falsification criteria:** A study comparing Bayesian BWM and traditional BWM on the same dataset that shows traditional BWM produces smaller or equivalent weight differences, or that the weight differences are not statistically distinguishable.

**Proof:** E01

**Evidence basis:** Comparison of indicator weights in Tables 12-13 showing weight ranges for risk (0.2197 BWM vs 0.1481 Bayesian BWM) and benefit (0.2133 BWM vs 0.1519 Bayesian BWM).

**Dependencies:** O4, G2, A1

**Tags:** bayesian-bwm, weight-stability, group-decision-making, mcdm

---

## C02: The benefit-per-unit-risk objective produces more balanced investment portfolios than single-objective optimization

**Statement:** Maximizing the ratio of total comprehensive benefit to total comprehensive risk yields investment portfolios that simultaneously control risk and capture benefit, unlike single-objective approaches (minimize risk only or maximize benefit only) which severely degrade the other dimension.

**Conditions:** When decision-makers must select from a finite set of candidate projects under investment amount, power demand, and low-carbon constraints.

**Sources:**
- Section 5.1.1: "if the decision-makers blindly reduce investment risks, the comprehensive investment benefit will decrease by 37.27% compared to scenario 0"
- Section 5.1.1: "if decision-makers focus more on investment benefits, the overall investment risk will increase by 89.86%"
- Section 6.1: "the investment portfolios proposed in this paper can enhance benefits by 37.27% and decrease risks by 89.86%, respectively"

**Status:** Supported by evidence

**Falsification criteria:** An empirical case where single-objective optimization (min-risk or max-benefit) produces a portfolio with higher benefit-per-unit-risk ratio than the proposed ratio objective, or where the degradation in the non-optimized dimension is less than 20%.

**Proof:** E02

**Evidence basis:** Comparison of scenario 0 (this paper) vs scenario 1a (risk min) vs scenario 1b (benefit max) in Table 11.

**Dependencies:** O9, A6, A7

**Tags:** objective-function, risk-benefit-tradeoff, portfolio-optimization, pgi

---

## C03: The ILA solver achieves superior optimization results with less computation time than genetic algorithm for PGI problems

**Statement:** The Incomprehensible but Intelligible-in-time Logic Algorithm (ILA) finds higher-quality solutions to the PGI constrained optimization problem (higher optimal value) while requiring significantly less computation time compared to a standard genetic algorithm implementation.

**Conditions:** When solving the binary (0-1) PGI project selection problem with investment amount, power demand, and low-carbon constraints, using ILA parameters from Ref. [59] versus MATLAB GA toolbox default parameters.

**Sources:**
- Section 5.1.3: "the optimal obtained results are 9.8% higher than traditional GA models, with a 61.57% reduction in computational time"
- Table 14: ILA optimal value = 1.0031, GA optimal value = 0.9135; ILA time = 7.25s, GA time = 18.87s

**Status:** Supported by evidence

**Falsification criteria:** A replication study where GA achieves an equal or higher optimal value than ILA, or where ILA does not achieve at least a 30% computation time reduction, on the same PGI problem instance.

**Proof:** E03

**Evidence basis:** Direct comparison in Table 14 showing ILA optimal value 1.0031 vs GA 0.9135, and computing time 7.25s vs 18.87s.

**Dependencies:** O5, A5, A6

**Tags:** ila-solver, genetic-algorithm, optimization-algorithm, computational-efficiency

---

## C04: Policy risks dominate the risk profile of power-grid investment projects

**Statement:** Among the four risk categories (policy, management, technical, environmental), policy risks — specifically project approval risk and energy/electricity policy adjustment risk — are the most influential factors in the comprehensive risk evaluation of PGI projects, as determined by expert weighting.

**Conditions:** When evaluating PGI projects using expert judgment from professionals in government, enterprise, and academia contexts within China's regulatory environment.

**Sources:**
- Section 4.2.1: "the weight of project approval risk (R11) is the highest, followed by the energy/electricity policy adjustment risk (R12)"
- Section 4.2.1: "policy risks are considered the most important risk factors affecting the PGI by the expert group"
- Table 6: R11 weight = 0.1955, R12 weight = 0.1891 (combined 0.3846 of total weight)
- Section 6.1: "policy and management risks are the most important risk factors that power-grid enterprises should pay attention to"

**Status:** Supported by evidence

**Falsification criteria:** A replication study with a different expert group or in a different regulatory environment where non-policy risks (e.g., technical or environmental) receive higher aggregate weight than policy risks.

**Proof:** E01

**Evidence basis:** Indicator weights in Table 6 show policy risk indicators (R11=0.1955, R12=0.1891) dominating all other risk indicators.

**Dependencies:** O7, A1, A2

**Tags:** risk-factors, policy-risk, indicator-weights, power-grid-investment

---

## C05: Operational benefits are the primary drivers of comprehensive benefit in power-grid projects

**Statement:** Among benefit categories (operational, financial, cleanliness, social), operational benefits — specifically electricity transmission capacity, load rate, and power supply reliability — receive the highest weights in comprehensive benefit evaluation, indicating their primary importance in PGI decision-making.

**Conditions:** When evaluating PGI benefits using expert judgment and when operational metrics (transmission volume, reliability, load rate) are available as quantitative indicators.

**Sources:**
- Section 4.3.1: "the weight of electricity transmission (B11) is the highest, followed by the load rate (B13) and power supply reliability (B12)"
- Section 4.3.1: "operational benefits are considered the most important benefit factors of the PGI by the expert group"
- Table 8: B11=0.1964, B13=0.1751, B12=0.1493 (combined 0.5208 of total weight)
- Section 6.1: "operational and financial benefits are the most important benefit factors"

**Status:** Supported by evidence

**Falsification criteria:** A replication study where financial, cleanliness, or social benefits receive higher aggregate weight than operational benefits, or where the ordering of benefit indicator weights differs substantially.

**Proof:** E01

**Evidence basis:** Indicator weights in Table 8 show operational benefit indicators (B11, B12, B13) collectively dominating all other benefit indicators.

**Dependencies:** O7, A1, A2

**Tags:** benefit-factors, operational-benefit, indicator-weights, power-grid-investment
