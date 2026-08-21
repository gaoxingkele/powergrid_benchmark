# Experiments / Analysis Blocks

## E01: Taxonomy and Comparative Analysis of EV Charging Demand Forecasting Methods

**Verifies:** C01, C04, C05

**Evidence:**
- Figure 2: Taxonomy of forecasting methods (learning-based vs. non-learning-based)
- Table 2: Quantitative metrics for forecasting evaluation
- Section 2.1: Detailed discussion of each forecasting category

**Run:**
This is the review's systematic classification and comparison of EV charging demand forecasting methodologies. The authors categorized methods into two primary branches (non-learning-based and learning-based), each with multiple subcategories.

**Setup:**
- Scope: Literature on EV charging demand forecasting published through 2025
- Classification framework: Two main categories (non-learning-based and learning-based) with hierarchical subcategories
- Non-learning-based: Non-probabilistic (ARIMA, SARIMA, ARMA) and Probabilistic (MCS, Markov Chain, Parametric/Non-parametric)
- Learning-based: Non-NN ML (RF, K-NN, SVM, Ensemble) and NN ML (ANN, CNN, RNN, LSTM, GRU, GNN), plus Generative AI (Transformer, GAN, VAE) and RL

**Procedure:**
1. Survey literature for EV charging demand forecasting studies
2. Classify each method into the taxonomy framework
3. Document advantages and limitations of each method category
4. Identify quantitative evaluation metrics (MAE, RMSE, MAPE, R²) used in the field
5. Summarize comparative findings on accuracy, computational cost, data requirements, and scalability

**Metrics:**
- Forecasting accuracy comparison (MAE, RMSE, MAPE) across method types
- Computational complexity (qualitative assessment)
- Data requirements (small vs. large scale)
- Suitability for uncertainty modeling

**Expected outcome:**
Learning-based methods (particularly LSTM, GRU, Transformer, and hybrid CNN-BiLSTM) demonstrate higher forecasting accuracy than non-learning-based methods, but with greater computational cost and data requirements. Non-learning-based methods remain suitable for small-scale applications with limited data. A trade-off exists between predictive performance and real-world implementation feasibility.

**Baselines:**
- ARIMA/SARIMA as traditional statistical baselines
- MCS as probabilistic baseline

**Dependencies:** O2, O5

---

## E02: Survey and Categorization of EVCS Planning Algorithms and Objective Functions

**Verifies:** C02, C03, C05

**Evidence:**
- Figure 3: Classification of optimization algorithms
- Table 3: Summary of EVCS planning algorithms with advantages and disadvantages
- Table 4: Summary of EVCS planning objective functions across studies

**Run:**
Systematic survey of EVCS planning algorithms in distribution networks, including deterministic and stochastic optimization methods, with a focus on their application to optimal siting and sizing.

**Setup:**
- Scope: EVCS planning studies in distribution networks
- Algorithm classification: Deterministic (LP, NLP, MILP, ADMM, SQP, DP) vs. Stochastic/Metaheuristic (SOA, PSO, GA, GWO, TLBO, ACO)
- Objective function categories: Technical (power loss, voltage deviation, VSI, supply power), Economic (installation, investment, operational, maintenance costs), Environmental (CO2 emissions), and Reliability (SAIFI, SAIDI, ENS)

**Procedure:**
1. Survey EVCS planning algorithm literature
2. Classify algorithms into deterministic and stochastic categories
3. Document advantages and disadvantages of each algorithm (Table 3)
4. Analyze objective functions used in planning studies (Table 4)
5. Quantify the proportion of studies addressing technical, economic, environmental, and reliability criteria

**Metrics:**
- Algorithm complexity (qualitative)
- Convergence properties (local vs. global optimum)
- Applicability to uncertainty-rich problems
- Proportion of studies covering each objective category

**Expected outcome:**
Metaheuristic algorithms are preferred for EVCS planning under uncertainty due to their robustness and flexibility. Technical and economic objectives dominate the literature (>90% and ~70% respectively), while environmental (~35%) and reliability (~18%) criteria are significantly underrepresented. This identifies a clear research gap in multi-objective formulations.

**Baselines:**
- LP/NLP/MILP as deterministic baselines
- Single-objective optimization as baseline for multi-objective comparisons

**Dependencies:** O4, O6, O7

---

## E03: Comparative Analysis of EVCS-RES Integration Studies

**Verifies:** C02, C03, C05

**Evidence:**
- Table 5: Summary of optimal location and sizing studies for EVCS-RES integration
- Table 6: Parameters related to EVCS and RES integration
- Table 7: Constraints related to EVCS and RES integration

**Run:**
Comprehensive survey of research on simultaneous EVCS and RES integration in distribution networks, including the optimization strategies, solution algorithms, and system parameters.

**Setup:**
- Scope: Studies addressing joint EVCS and RES allocation in distribution networks
- Parameters analyzed: Load parameters (balanced/unbalanced, residential/commercial/industrial), PV characteristics (rated capacity, uncertain generation), EVCS charging profiles (Level 1/2/3, slow/fast, power ratings)
- Constraints captured: Power balance, nodal voltage limits, thermal limits, SOC limits, charger capacity limits, BESS operation limits

**Procedure:**
1. Survey literature on joint EVCS-RES optimal allocation
2. Extract RES type, optimization algorithm, technical/economic/environmental/reliability objectives from each study (Table 5)
3. Document load modeling approaches and charging profiles (Table 6)
4. Catalog practical constraints considered (Table 7)
5. Perform statistical analysis on objective emphasis distribution across studies
6. Identify under-addressed areas in current research

**Metrics:**
- Algorithm type distribution (metaheuristic vs. deterministic)
- Objective function coverage across four dimensions
- RES types considered (PV, wind, hybrid)
- Charger level distribution (Level 1/2/3)
- Constraint coverage breadth

**Expected outcome:**
PSO, GWO, and hybrid algorithms (BFOA-PSO, WOAGA, HGWOPSO) are the most commonly applied. PV is the dominant RES type. Most studies use balanced residential load models with limited exploration of unbalanced systems. The statistical analysis confirms the technical-economic dominance with environmental and reliability criteria being understudied. Multi-stage stochastic planning frameworks that integrate uncertainty propagation remain underdeveloped.

**Baselines:**
- Single-objective optimization (technical only) as baseline
- Deterministic planning without uncertainty consideration

**Dependencies:** O4, O7, O9
