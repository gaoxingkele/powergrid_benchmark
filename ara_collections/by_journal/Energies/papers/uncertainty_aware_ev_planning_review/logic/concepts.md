# Concepts: Key Technical Terms in EVCS-RES Planning

## Concept 1: EV Charging Demand Uncertainty

**Notation:** Not explicitly notated as a single symbol; represented as a random variable with probability distribution P(D_ev) or via scenario set S = {s_1, ..., s_N}

**Definition:**
The stochastic nature of electric vehicle charging demand arising from variability in user behavior parameters including arrival time, departure time, starting state of charge (SOC), travel mileage, charging duration, and customer arrival patterns. This uncertainty is the primary challenge for EVCS planning and must be modeled probabilistically or via scenario generation rather than with deterministic point forecasts.

**Boundary conditions:**
- Captured through probability density functions (PDFs) for charging factors
- Modeling approaches differ between planning studies (probabilistic/scenario-based) and operational studies (real-time)
- Data scarcity for real EV charging patterns is a significant limitation
- The chosen parameters (arrival/departure time, SOC, charging duration) have "fundamental impact on the peak coincidence and temporal aggregation of charging loads" (Section 2.1)

**Related concepts:**
- Probabilistic forecasting
- Monte Carlo Simulation
- Scenario generation
- Load forecasting

---

## Concept 2: Learning-Based Forecasting Methods

**Notation:** Not standardized; architectures denoted by model family (ANN, CNN, RNN, LSTM, GRU, GNN, Transformer)

**Definition:**
Methods for EV charging demand prediction that learn patterns from historical data using artificial neural networks or machine learning algorithms, without requiring explicit pre-defined mathematical relationships. These are classified into non-NN-based models (Random Forests, SVM, K-NN, Gradient Boosting) and NN-based models (ANN, CNN, RNN, LSTM, GRU, GNN), with additional subcategories including Generative AI (GANs, VAEs, Transformers) and Reinforcement Learning.

**Boundary conditions:**
- Require large, high-quality historical datasets for effective training
- Computationally intensive, especially deep learning architectures
- Struggle with interpretability compared to statistical methods
- Hybrid approaches (e.g., CNN-BiLSTM, SARIMA-DL) combine strengths of multiple methods
- "Although advanced learning-based models... provide superior forecasting accuracy, their practical implementation is constrained by high computational requirements, large data dependency, scalability limitations, and reduced interpretability" (Section 2.1.2 Summary)

**Related concepts:**
- Non-learning-based forecasting (ARIMA, SARIMA, MCS, Markov Chain)
- Time series forecasting
- Supervised learning
- Generative AI

---

## Concept 3: EVCS Planning Algorithms (Deterministic vs. Stochastic)

**Notation:** Not standardized; algorithms denoted by acronym (MILP, SQP, DP, PSO, GA, GWO, TLBO, ACO, SOA, etc.)

**Definition:**
Mathematical optimization approaches for determining the optimal location (siting) and capacity (sizing) of EV charging stations in distribution networks. The review classifies these into two fundamental categories: (1) Deterministic/exact algorithms (linear programming LP, nonlinear programming NLP, mixed-integer linear programming MILP, sequential quadratic programming SQP, dynamic programming DP, alternating direction method of multipliers ADMM) that solve problems with known parameters and well-defined constraints, and (2) Stochastic/metaheuristic algorithms (particle swarm optimization PSO, genetic algorithm GA, grey wolf optimization GWO, teaching-learning-based optimization TLBO, ant colony optimization ACO, snake optimization algorithm SOA) that use population-based search strategies inspired by natural phenomena to find near-optimal solutions under uncertainty.

**Boundary conditions:**
- Deterministic methods are time-efficient and converge to local optima but "cannot solve network uncertainty problems introduced by intermittency" (Section 2.2.1)
- Metaheuristic methods are robust and flexible but may require hybridization for large-scale problems
- Hybrid algorithms (BFOA-PSO, WOAGA, HGWOPSO) combine advantages of multiple approaches
- "Metaheuristic algorithms are the superior choice for optimization problems in power systems due to their robustness, flexibility, and ability to address system uncertainties" (Section 2.2.1)

**Related concepts:**
- Multi-objective optimization
- Optimal siting and sizing
- Power system optimization
- Hybrid optimization algorithms

---

## Concept 4: EVCS-RES Multi-Objective Planning

**Notation:** Objective function space typically formalized as min{f_1(x), f_2(x), ..., f_n(x)} where each f_i represents a criterion dimension

**Definition:**
The simultaneous optimization of EVCS and RES allocation across multiple, typically conflicting, criteria: technical (active/reactive power loss Qloss/Ploss, voltage deviation VDevi, voltage stability index VSI, power supply Psup), economic (installation cost, investment cost, operational cost, maintenance cost), environmental (CO2 emissions), and reliability (SAIFI, SAIDI, ENS). The review identifies that technical and economic objectives dominate the literature, with environmental and reliability criteria significantly underrepresented.

**Boundary conditions:**
- >99% of studies include technical criteria; ~70% include economic criteria
- Only 35% include environmental criteria; only 18% include reliability criteria (Section 3)
- Multi-objective formulations typically use weighted sum, Pareto frontier, or epsilon-constraint methods
- Future research should "use a more holistic approach, incorporating reliability factors, as well as environmental and financial factors" (Section 2.2.2)

**Related concepts:**
- Pareto optimality
- Weighted sum method
- Techno-economic analysis
- Sustainability assessment

---

## Concept 5: Distribution Network Impacts of EVCS-RES Integration

**Notation:** Standard power system indices (SAIFI, SAIDI, ENS, VSI, voltage deviation in p.u., power loss in kW/kVAR)

**Definition:**
The measurable effects on distribution network performance caused by integrating EV charging stations and renewable energy sources. These include power quality issues (voltage drops, harmonic distortions, frequency fluctuations), increased peak load demand, transformer aging, power losses (active and reactive), voltage stability degradation, and reliability reductions (increased SAIFI/SAIDI, decreased ENS). The review emphasizes that "strategically placing RESs near EVCSs reduces grid dependence and alleviates grid stress during peak load hours" (Section 4).

**Boundary conditions:**
- Impacts vary with EV penetration level, charging patterns (controlled vs. uncontrolled), and RES intermittency
- "Coordinated active-reactive power control and intelligent storage dispatch can mitigate voltage deviations, reduce losses, and enhance reliability under stochastic conditions" (Section 4)
- Mitigation strategies include BESS integration, smart charging control, and optimal siting/sizing
- Impact assessment requires load flow analysis under various scenarios

**Related concepts:**
- Power quality
- Voltage regulation
- Grid reliability
- Harmonic distortion
- Load flow analysis

---

## Concept 6: Uncertainty Propagation in Planning

**Notation:** Not standardized in the review; described conceptually as the cascade of forecast error through objective functions and constraints

**Definition:**
The process by which uncertainty in input parameters (EV charging demand, RES generation, load variations) propagates through planning optimization models to affect output decisions (siting, sizing, investment). The review establishes that "forecast uncertainty penetrates through the objective functions and restrictions in planning frameworks" and that "calculations of power loss, voltage deviation indices, and system loading levels are all affected by changes in the anticipated demand for EV charging" (Section 2).

**Boundary conditions:**
- Forecast errors alter "Pareto-optimal solutions and can change the optimal bus locations for EVCS units" (Section 2)
- "Planning outcomes may not be reliable under real operational conditions if uncertainty modeling is ignored" (Section 1)
- Addressed via probabilistic forecasting, scenario generation, stochastic programming, or robust optimization
- "Optimization robustness should therefore not be evaluated solely by convergence speed or objective value improvement, but by resilience against renewable variability, EV demand fluctuations, and planning horizon uncertainties" (Section 4)

**Related concepts:**
- Sensitivity analysis
- Scenario-based optimization
- Robust optimization
- Stochastic programming
- Chance-constrained optimization

---

## Concept 7: Battery Energy Storage Systems (BESS) as Enabling Technology

**Notation:** BESS (Battery Energy Storage System); parameters include rated capacity (kWh/MWh), power rating (kW/MW), SOC limits, charge/discharge efficiency

**Definition:**
Energy storage systems that serve as a critical enabling technology for EVCS-RES integration by storing excess renewable generation during low-demand periods and supplying it during high-demand periods. The review highlights "coordinated active-reactive power control and intelligent storage dispatch" as means to "mitigate voltage deviations, reduce losses, and enhance reliability under stochastic conditions" (Section 4).

**Boundary conditions:**
- BESS sizing and dispatch must be jointly optimized with EVCS placement
- "Bio-inspired optimization techniques are used to coordinate BESS dispatch in AC microgrids, resulting in statistically validated reductions in operational costs, network losses, and emissions" (Section 1.1)
- Integration with EV batteries as distributed storage resources (V2G)
- "Such operational coordination is still insufficiently embedded within many planning models" (Section 4)

**Related concepts:**
- Vehicle-to-Grid (V2G)
- Energy management systems
- Active-reactive power control
- Renewable energy integration
- Smart grid
