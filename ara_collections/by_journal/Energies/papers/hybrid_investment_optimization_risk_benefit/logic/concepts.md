# Concepts

## Bayesian Best-Worst Method (Bayesian BWM)

**Notation:** Bayesian BWM

**Definition:** A probabilistic extension of the traditional Best-Worst Method (BWM) that uses Bayesian inference to estimate indicator weights from multiple experts' pairwise comparison vectors. Instead of averaging individual BWM weights, it models the BO (best-to-others) and OW (others-to-worst) vectors of each expert as multinomial probability distributions and uses a hierarchical Bayesian model to estimate the posterior distribution of the group-aggregated weights.

**Boundary conditions:**
- Requires at least 2 experts (K >= 2) to benefit from group decision-making capability
- Experts must agree on the best (CB) and worst (CW) indicators before providing comparison vectors
- Comparison values use a 1-9 scale where 1 = equal importance, 9 = extreme importance
- Assumes the multinomial probability distribution correctly models the comparison process
- The number of comparisons is 2n-3 per expert (vs n(n-1)/2 for AHP)

**Related concepts:** BWM (traditional), AHP, multinomial distribution, hierarchical Bayesian model, group decision-making, posterior distribution

---

## Technique for Order Preference by Similarity to an Ideal Solution (TOPSIS)

**Notation:** TOPSIS

**Definition:** A multi-criteria decision-making method that ranks alternatives based on their Euclidean distance from an ideal solution (best values for each criterion) and an anti-ideal solution (worst values for each criterion). The comprehensive score Ci = yi- / (yi+ + yi-), where yi+ is the distance to the ideal solution and yi- is the distance to the anti-ideal solution, with values closer to 1 indicating better performance.

**Boundary conditions:**
- Requires normalized decision matrix with quantitative or quantified qualitative values
- Assumes monotonic criteria (larger-is-better for benefit-type, smaller-is-better for cost-type)
- The Euclidean distance metric assumes criteria independence
- Weighted by pre-determined criterion weights (from Bayesian BWM in this paper)
- Each alternative's score is relative to the other alternatives in the set (ranking-type model)

**Related concepts:** MCDM, ideal solution, anti-ideal solution, Euclidean distance, MARCOS, VIKOR

---

## Benefit per Unit Risk (Objective Function)

**Notation:** max f = sum(i * Bi) / sum(i * Ri)

**Definition:** A composite objective function for PGI optimization that jointly considers both benefit and risk dimensions by taking the ratio of total comprehensive benefit (sum of Bi for selected projects) to total comprehensive risk (sum of Ri for selected projects), where i is a binary decision variable (1 = invest, 0 = do not invest). This formulation transforms a multi-objective problem (minimize risk, maximize benefit) into a single-objective ratio optimization.

**Boundary conditions:**
- All Bi values must be positive (benefit-type indicators, larger-is-better)
- All Ri values must be positive (cost-type indicators, smaller-is-better but generally non-zero)
- The ratio formulation implicitly assumes the decision-maker is risk-benefit neutral (linear trade-off)
- Cannot handle negative benefit or risk values
- The ratio is scale-invariant but sensitive to the normalization of Bi and Ri

**Related concepts:** Single-objective optimization, multi-objective optimization, Sharpe ratio, cost-benefit analysis, composite objective

---

## Incomprehensible but Intelligible-in-time Logic Algorithm (ILA)

**Notation:** ILA

**Definition:** A metaheuristic optimization algorithm inspired by human learning processes, comprising three stages: (1) Groupwork stage — intra-group optimization where experts (candidate solutions) improve fitness based on group knowledge; (2) Integration stage — inter-group optimization aggregating all groups; (3) Logic search stage — overall optimization using average collective knowledge. Each expert has three parameters: comprehensibility (COMk), degree (DEGk), and probability (PROk), which are normalized and used to update knowledge.

**Boundary conditions:**
- Designed for both constrained and unconstrained optimization problems
- Requires parameter tuning (1-9 random number ranges differ per stage)
- Groupwork stage: 1-2 are random numbers [-1.5, 1.5], 3 is [0,1]
- Integration stage: 4-5 are random numbers [-0.75, 0.75], 6 is [0,1]
- Logic search stage: 7-8 are random numbers [-0.25, 0.25], 9 is [0,1]
- The number of groups and experts per group are problem-specific parameters
- Decreasing random number ranges across stages reflect convergence from exploration to exploitation

**Related concepts:** Metaheuristic, genetic algorithm, particle swarm optimization, exploration-exploitation trade-off, knowledge-based optimization

---

## Comprehensive Risk Evaluation Index System for PGI

**Notation:** Risk Index System (R1-R4 with sub-indicators R11-R42)

**Definition:** A hierarchical indicator framework for evaluating the comprehensive risk of power-grid investment projects, comprising 4 dimensions and 9 indicators: Policy Risk (R1: project approval risk R11, energy/electricity policy adjustment risk R12), Management Risk (R2: feasibility study planning risk R21, engineering design risk R22, bidding risk R23), Technical Risk (R3: equipment installation risk R31, material transportation risk R32), and Environmental Risk (R4: geological unfavorable condition risk R41, natural disaster risk R42). Qualitative indicators are scored by experts on a 1-9 scale.

**Boundary conditions:**
- Designed specifically for Chinese power-grid investment projects
- Qualitative indicators rely on expert judgment (subject to expert bias)
- Assumes the four risk dimensions are comprehensive and non-overlapping
- The 1-9 scoring scale for qualitative indicators follows standard MCDM practice
- Does not explicitly model risk correlation or interaction effects

**Related concepts:** Risk assessment, indicator system, policy risk, management risk, technical risk, environmental risk, MCDM
