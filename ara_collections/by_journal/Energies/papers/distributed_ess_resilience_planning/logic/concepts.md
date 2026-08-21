# Concepts

## 1. Distributed Energy Storage System (DESS)

- **Notation:** DESS
- **Definition:** A set of battery-based storage units dispersed across the distribution network at the node level, capable of bidirectional power exchange (charging/discharging) with dual "generation-load" characteristics and fast response times.
- **Boundary conditions:** Each DESS unit is characterized by rated power capacity (P_ess), rated energy capacity (E_ess), charging/discharging efficiency (ec_ss, edis_ss), and state-of-charge limits (SOC_min, SOC_max). Units are sited at individual distribution nodes within grid-based blocks.
- **Related concepts:** Sequential planning, priority index, node–block–grid evaluation
- **Source:** "With their dual 'generation-load' capabilities and fast response times, DESS offer vital services like dynamic power balancing, rapid frequency and voltage regulation, and post-fault recovery." (Section 1.1, p. 2)

---

## 2. Priority Index (H_pi)

- **Notation:** H_pi
- **Definition:** A scalar composite index that quantifies the relative urgency of energy storage deployment at a given node, calculated as the Critic-weighted sum of seven quality indicators (I1–I7) plus the efficiency indicator (matching degree). Higher values indicate greater demand.
- **Boundary conditions:** Defined for nodes within a grid-based partitioned distribution network. Requires normalized quality indicators and efficiency indicators. Weights sum to 1. H_pi is recalculated after each DESS deployment in the sequential planning process.
- **Related concepts:** Critic method, matching degree, quality indicators, sequential planning
- **Source:** "H_pi represents the priority index for supply areas, indicating that a higher priority index corresponds to a greater demand for energy storage configuration." (Section 3.3, p. 11)
- **Formula:** H_pi = Σ(a=1 to 7) ω_a * I_a + η, where ω_a are Critic weights, I_a are dimensionless quality indicators, and η is the efficiency indicator.

---

## 3. Improved Gaussian Mixture Model (GMM) for Scenario Generation

- **Notation:** GMM
- **Definition:** A probabilistic clustering model that represents wind and photovoltaic power output data as a mixture of K Gaussian distributions, with parameter initialization via K-means using the RV coefficient and optimal cluster count determined by the CH (Calinski–Harabasz) index.
- **Boundary conditions:** Applied to historical wind speed and solar irradiance data at the grid block level. Assumes multimodal distributions of renewable generation. The RV-coefficient-based K-means initialization preserves extreme operating scenarios better than random initialization.
- **Related concepts:** Scenario probability, typical output curves, CH index, RV coefficient
- **Source:** "GMM is selected because it can effectively describe multimodal distributions and stochastic fluctuations of renewable generation, while maintaining clear physical interpretability through explicit model parameters." (Section 1.2, p. 3)
- **Formula:** P(x) = Σ(k=1 to K) π_k * p_k(x), where p_k(x) is the Gaussian density of the k-th component with mean μ_k and covariance Σ_k.

---

## 4. Sequential Planning Strategy

- **Notation:** SPS (sequential planning strategy)
- **Definition:** An iterative DESS siting and sizing procedure in which at each iteration: (1) the node with the highest priority index is selected for DESS installation, (2) the multi-objective optimization model determines capacity and operating schedule for that node, (3) the generalized load curve and priority indices are updated, and (4) the process repeats until the budget constraint is reached.
- **Boundary conditions:** The number of DESS units is not an optimization variable but is implicitly determined by the budget constraint. Previous DESS configurations are retained in each iteration. The budget is specified by the utility.
- **Related concepts:** Priority index, multi-objective optimization, generalized load, budget constraint
- **Source:** "At each iteration, the node with the highest priority index is selected as the candidate site, and the optimization model is then applied to determine the corresponding storage capacity and operating schedule at that node." (Section 4.1, p. 16)

---

## 5. Node–Block–Grid Multi-Dimensional Evaluation Framework

- **Notation:** N-B-G framework
- **Definition:** A hierarchical assessment structure that evaluates DESS planning outcomes at three spatial scales: node-level (O1: optimization potential, O2: economic efficiency, O3: renewable integration), block-level (L1: matching improvement, L2: quality demand improvement), and grid-level (G1: high-quality demand improvement, G2: matching degree discreteness improvement).
- **Boundary conditions:** Requires the original physical distribution network topology and feeder-level data. Node-level indicators use power flow results; block-level indicators aggregate node characteristics; grid-level indicators measure system-wide coordination.
- **Related concepts:** Matching degree (η), node optimization potential (O1), economic efficiency (O2), renewable integration (O3)
- **Source:** "A node–block–grid multi-dimensional evaluation framework is introduced to assess resilience enhancement from node-, block-, and grid-level perspectives." (Abstract, p. 1)
- **Indicators:** O1 = (1/Z) Σ ω_z; O2 = F2/F1; O3 = reduction in curtailment rate; L1 = Σ (η'_w - η_w)/η_w; L2 = quality improvement ratio; G1/G2 = grid-level coordination metrics

---

## 6. Matching Degree (η)

- **Notation:** η
- **Definition:** A dimensionless metric that measures the degree of source-load balance in a grid block, calculated as the ratio of total generalized load energy to total DG output energy over the planning period. Values in [−1, 0] indicate load-dominant (high resilience need), values in [0, 1] indicate generation-dominant (curtailment risk), and η < −1 indicates strong self-adaptive capacity (low resilience need).
- **Boundary conditions:** Defined per grid block. Used in both efficiency indicator calculation and block-level evaluation. Based on aggregated generalized load and DG output over scenario time horizon T.
- **Related concepts:** Generalized load, generalized load retrieval model, source-load matching, block-level evaluation
- **Source:** "η is the distribution network type matching degree, used to measure the degree of source-load matching." (Section 3.1.1, p. 8)

---

## 7. Generalized Load (P_t^EL)

- **Notation:** P_t^EL
- **Definition:** The aggregated net power curve at time t, combining conventional load demand (P_t^base), aggregated demand response contributions (P_t^DR), and energy storage charging/discharging power (P_t^ess). Represents the net power that the distribution system must serve after considering flexibility resources.
- **Boundary conditions:** P_t^DR reflects peak-shaving and load-shifting under price/incentive mechanisms, not emergency curtailment. P_t^ess is positive for discharging and negative for charging. Used for planning-stage analysis, not real-time control.
- **Related concepts:** Matching degree, demand response, sequential planning
- **Source:** "P_t^EL = P_t^base + P_t^DR + P_t^ess" (Section 3.1.1, Formula 1, p. 8)

---

## 8. Critic Method (Objective Weighting)

- **Notation:** Critic
- **Definition:** An objective weighting technique that determines indicator weights by analyzing the internal variability (standard deviation) and inter-indicator correlation (Pearson correlation coefficient) of quality indicators. The information measure M_d = S_d * Σ(1 − r_de) captures how much unique information indicator d contributes.
- **Boundary conditions:** Requires a sample set of b nodes with p quality indicators. Applies to positive and reverse indicators separately via different dimensionless formulas (Equation 11). Weights are data-driven and may vary across different distribution networks.
- **Related concepts:** Priority index, quality indicators I1–I7, dimensionless processing
- **Source:** "The Critic approach, an objective weighting technique, allocates weights in a multi-indicator comprehensive evaluation by analysing the correlation and disparities among indicators." (Section 3.3, p. 11)
