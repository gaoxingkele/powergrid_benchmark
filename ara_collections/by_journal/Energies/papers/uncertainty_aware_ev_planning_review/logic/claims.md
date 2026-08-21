# Claims: Synthesis Findings from the Review

## C01: AI-based forecasting methods provide superior accuracy over statistical methods for EV charging demand under uncertainty

**Statement:**
Learning-based forecasting methods (RNN, LSTM, GRU, GNN, Transformer) capture complex nonlinear and temporal patterns in EV charging demand more effectively than non-learning-based methods (ARIMA, SARIMA, Monte Carlo Simulation, Markov Chain), particularly under high-uncertainty conditions with stochastic user behavior and renewable variability. Therefore, AI-based methods yield more reliable inputs for EVCS planning optimization.

**Conditions:**
- Sufficient historical charging data is available for model training (large datasets required).
- The forecasting horizon is short-to-medium term (hourly to daily).
- Computational resources are adequate for training complex deep learning architectures.

**Sources:**
- "Non-learning-based techniques... struggle with nonlinearity and rely heavily on historical data." (Section 2.1.2, Summary)
- "Network-based models such as RNN, LSTM, and GRU excel in capturing complex temporal patterns and adapting to nonlinear relationships." (Section 2.1.2, Summary)
- "Traditional statistical and probabilistic forecasting approaches are extensively employed, but they frequently fail to capture the nonlinear and stochastic character of these uncertainties." (Section 4, lines 1296-1299)
- "NN-based models, such as LSTM and GRU, are effective for sequential data, while generative AI models like GANs and VAEs generate realistic synthetic data." (Section 2.1.2, lines 681-683)

**Status:** Supported by review of comparative studies in the surveyed literature.

**Falsification criteria:**
Demonstration of a scenario where ARIMA/SARIMA consistently achieves lower RMSE and MAPE than LSTM/GRU/Transformer for EV charging demand forecasting across multiple datasets, or evidence that the additional computational cost of AI methods never yields statistically significant accuracy improvements.

**Proof:** E01, E02

**Evidence basis:**
- Table 2 shows quantitative metrics (MAE, RMSE, MAPE) used across studies for both method types.
- Section 2.1.2 documents comparative results (e.g., GRU outperforming RNN and LSTM in [35]).
- Section 2.1.2 pages 13-14 summarize trade-offs between learning-based and non-learning-based methods.

**Dependencies:** O2, O5

**Tags:** forecasting, AI, machine learning, deep learning, uncertainty

---

## C02: Metaheuristic optimization algorithms are more effective than deterministic algorithms for EVCS-RES planning under uncertainty

**Statement:**
Metaheuristic algorithms (PSO, GA, GWO, TLBO, ACO, and hybrid variants) consistently outperform deterministic algorithms (LP, NLP, DP, MILP, SQP) for EVCS siting and sizing optimization problems in distribution networks with high uncertainty, because metaheuristic methods avoid entrapment in local optima, handle nonlinear constraints, and accommodate stochastic input variability without requiring derivative information.

**Conditions:**
- The optimization problem involves nonlinear objectives and constraints.
- Input parameters (EV demand, RES generation, load profiles) exhibit significant uncertainty.
- The planning problem is large-scale or multi-objective.

**Sources:**
- "Deterministic optimization techniques cannot solve network uncertainty problems introduced by intermittency." (Section 2.2.1, lines 788-790)
- "Metaheuristic algorithms are the superior choice for optimization problems in power systems due to their robustness, flexibility, and ability to address system uncertainties." (Section 2.2.1, lines 798-801)
- "Deterministic algorithms... are challenged with difficulty escaping local solutions, risk of divergence, handling complex constraints, and challenges in computing first or second-order derivatives." (Section 2.2.1, lines 783-785)
- "Hybrid optimization methods such as BFOA-PSO and WOAGA have demonstrated superior performance by combining the strengths of individual algorithms to achieve faster convergence, improved accuracy, and better exploration-exploitation balance." (Section 4, lines 1261-1265)

**Status:** Supported by review of planning algorithm literature.

**Falsification criteria:**
Evidence from a comparative study where MILP or SQP consistently finds better (lower cost, lower loss) feasible solutions for an EVCS-RES planning problem compared to PSO, GA, or GWO under equivalent problem formulations and uncertainty scenarios.

**Proof:** E02, E03

**Evidence basis:**
- Table 3 provides advantage/disadvantage comparisons of both algorithm categories.
- Section 2.2.1 discusses the classification and performance characteristics.
- Table 5 summarizes algorithms used in optimal siting and sizing studies.

**Dependencies:** O6, O7

**Tags:** optimization, metaheuristics, planning algorithms, EVCS siting

---

## C03: The existing literature on EVCS-RES integration disproportionately favors technical and economic objectives while neglecting environmental and reliability criteria

**Statement:**
The body of research on EVCS and RES integrated planning demonstrates a significant imbalance: technical objectives (power loss, voltage deviation, voltage stability) dominate at over 99% of studies, and economic objectives (installation, investment, operational, maintenance costs) appear in approximately 70%, while environmental criteria (CO2 emissions) are addressed in only 35% and reliability indices (SAIFI, SAIDI, ENS) in merely 18% of surveyed studies. This imbalance undermines the development of truly sustainable and resilient charging infrastructure.

**Conditions:**
- The analyzed studies focus on optimal siting and sizing of EVCS with RES in distribution networks.
- The period covers studies published through early 2026.

**Sources:**
- "The most commonly considered objectives are technical criteria, which appear in over 99% of the examined studies" (Section 3, lines 1094-1096)
- "Only 35 percent of the research addresses environmental criteria, including the reduction of CO2 emissions. Just 18% of the examined publications address reliability requirements." (Section 3, lines 1098-1104)
- "A review of EVCS planning objectives... finds a strong emphasis on technical and economic factors, with voltage stability, power loss, and installation cost being the most addressed elements." (Section 2.2.2, lines 899-901)
- "Environmental factors like emissions and CO2 reduction are less typically examined... the inclusion of reliability evaluation is significantly limited." (Section 2.2.2, lines 902-905)

**Status:** Supported by quantitative statistical analysis of Table 5 studies.

**Falsification criteria:**
A comprehensive survey of 50+ new EVCS-RES planning studies showing that >50% include environmental objectives or >30% include reliability objectives, contradicting the reported proportions.

**Proof:** E02, E03

**Evidence basis:**
- Table 5 summarizes the objective function categories for 20+ studies.
- Section 2.2.2 discusses objective functions in EVCS planning.
- The statistical analysis of Table 5 provides exact percentages.

**Dependencies:** O4

**Tags:** multi-objective optimization, environmental impact, reliability, research gap

---

## C04: Forecasting uncertainty in EV charging demand propagates through planning optimization and materially affects siting and sizing outcomes

**Statement:**
Errors in EV charging demand forecasting directly affect EVCS planning outcomes — including feeder loading, voltage magnitude profiles, load flow calculations, and investment sizing — such that inflated forecasts cause capital expenditure waste while underestimated demand results in voltage dips and insufficient charging capacity. In stochastic or scenario-based optimization, forecast variations can alter the optimal bus locations for EVCS units and shift Pareto-optimal solutions.

**Conditions:**
- The planning framework uses forecasted EV demand as input.
- Stochastic or scenario-based optimization is employed.

**Sources:**
- "Decisions about feeder loading, voltage magnitude profiles, load flow calculations, and investment sizing are all directly impacted by forecast errors." (Section 2, lines 282-284)
- "Forecast uncertainty penetrates through the objective functions and restrictions in planning frameworks." (Section 2, lines 290-291)
- "These forecasting variations affect the Pareto-optimal solutions and can change the optimal bus locations for EVCS units when stochastic or scenario-based optimization is used." (Section 2, lines 293-295)
- "Planning outcomes may not be reliable under real operational conditions if uncertainty modeling is ignored." (Section 1, lines 85-86)

**Status:** Supported by logical analysis in the review's framing framework.

**Falsification criteria:**
A study demonstrating that EVCS siting and sizing solutions remain invariant under a +/-30% variation in forecasted EV charging demand, or that forecast error has negligible impact on objective function values compared to other input parameters.

**Proof:** E01

**Evidence basis:**
- Section 2 discusses the linkage between forecasting and planning.
- Section 4 identifies this coupling as a key finding and future direction.

**Dependencies:** O1, O2, O8

**Tags:** uncertainty propagation, forecasting, planning, sensitivity

---

## C05: Integrated planning frameworks that combine advanced forecasting with multi-objective optimization remain underdeveloped despite being necessary

**Statement:**
The review establishes that frameworks jointly addressing forecasting accuracy, uncertainty propagation, and multi-objective planning (technical, economic, environmental, reliability) are critically lacking in the literature. Current approaches either optimize EVCS-RES allocation with simplistic deterministic demand models or develop sophisticated forecasting methods in isolation from planning optimization. This disconnect represents the most significant gap for future research.

**Conditions:**
- The framework must connect forecasting methodology choices (statistical vs. AI-based) with planning optimization outcomes.
- Multi-objective synthesis must include at least technical, economic, environmental, and reliability dimensions.

**Sources:**
- "Unlike previous surveys, which focused on optimization approaches and system planning methodologies, this evaluation presents an integrated analytical framework that integrates forecasting accuracy, uncertainty propagation, and multi-objective planning performance." (Section 1.1, lines 229-235)
- "Most previous studies [8,21] do not sufficiently examine or include advanced forecasting approaches into their evaluations of planning and integration frameworks." (Section 1.1, lines 191-193)
- "By combining forecasting methods (statistical, machine learning, and deep learning) with EVCS-RES allocation models, this study offers a structured examination of how predictive uncertainty affects voltage stability, system losses, economic cost, and reliability indices." (Section 1.1, lines 232-235)
- "Comprehensive investigations that integrate technical, economic, environmental, and reliability impacts with the application of advanced forecasting techniques and optimization algorithms are still lacking." (Section 4, lines 1268-1272)

**Status:** Supported as the review's central gap-identification claim.

**Falsification criteria:**
Identification of three or more published frameworks that (a) use AI-based EV demand forecasting as input, (b) optimize EVCS-RES allocation with stochastic programming, and (c) evaluate outcomes across all four dimensions (technical, economic, environmental, reliability) with uncertainty propagation analysis.

**Proof:** E01, E02, E03

**Evidence basis:**
- Table 1 shows the comparison with existing surveys, highlighting that no prior survey covers all features.
- Section 1.1 discusses the unique integrated framework contribution.
- Section 4 lists future research directions targeting this gap.

**Dependencies:** O4, O5, G1, G2

**Tags:** integrated framework, forecasting-driven planning, research gap, multi-objective
