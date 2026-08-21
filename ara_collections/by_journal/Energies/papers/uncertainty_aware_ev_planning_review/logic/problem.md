# Problem Structure: Uncertainty-Aware EVCS-RES Planning in Distribution Networks

## Observations

### O1: EV adoption is accelerating and straining distribution networks
Global EV sales doubled to 6.6 million units in 2021, bringing the total to approximately 16.5 million, which is three times the 2018 figure. This growth presents challenges to the grid including increased peak load demand, shortened transformer lifespan, harmonic distortion, voltage drops, power imbalances, and power quality issues. [Source: Paper Section 1, lines 56-63]

### O2: EV charging demand exhibits high uncertainty
Factors such as user behavior, mileage, battery capacity, travel time, arrival/departure time, charging time, customer arrival patterns, and overall charging demand contribute to significant uncertainties in EV charging demand modeling. [Source: Paper Section 2.1, lines 303-306]

### O3: RES integration introduces additional intermittency
Renewable sources like PV and wind have inherent variability in generation. RES capacity grew from approximately 3100 GW in 2022 to 3360 GW in 2023 (8.4% increase), reaching 4448 GW by end of 2024 (15.1% increase in 2023). The variable power generation leads to frequency fluctuations, destabilizing power systems. [Source: Paper Section 3, lines 979-989]

### O4: Existing work prioritizes technical and economic objectives over environmental and reliability objectives
Statistical analysis from Table 5 shows technical criteria appear in over 99% of examined studies; about 70% consider economic factors; only 35% address environmental criteria (CO2 emissions); and just 18% address reliability requirements (SAIFI, SAIDI, ENS). [Source: Paper Section 3, lines 1094-1104]

### O5: AI-based forecasting methods are underutilized in EVCS planning frameworks
Most previous studies do not sufficiently examine or include advanced forecasting approaches in their planning and integration frameworks. They fail to explain how AI-based forecasting approaches might improve planning precision and efficacy, especially in uncertain settings. [Source: Paper Section 1.1, lines 191-195]

### O6: Deterministic optimization methods are insufficient for uncertainty-rich environments
Deterministic optimization techniques cannot solve network uncertainty problems introduced by intermittency. Modern power systems have challenges ranging from renewable energy uncertainties to load fluctuation that cannot be efficiently addressed using deterministic approaches. [Source: Paper Section 2.2.1, lines 788-792]

### O7: Metaheuristic algorithms are preferred for EVCS-RES planning
Metaheuristic algorithms are the superior choice for optimization problems in power systems due to their robustness, flexibility, and ability to address system uncertainties. Hybrid methods like BFOA-PSO and WOAGA demonstrate superior performance. [Source: Paper Section 2.2.1, lines 798-801; Section 4, lines 1258-1265]

### O8: Forecasting accuracy directly impacts planning outcomes
Forecast errors directly affect decisions about feeder loading, voltage magnitude profiles, load flow calculations, and investment sizing. Inflated forecasts cause unnecessary infrastructure expenditure while underestimated EV demand causes voltage dips and inadequate charging capacity. [Source: Paper Section 2, lines 281-295]

### O9: BESS plays a critical enabling role
Battery Energy Storage Systems (BESS) with coordinated active-reactive power control can mitigate voltage deviations, reduce losses, and enhance reliability under stochastic conditions. The growing penetration of RES and large-scale EV charging highlights BESS as an enabling technology. [Source: Paper Section 3, lines 989-993; Section 4, lines 1282-1287]

## Gaps

### G1: Lack of integrated forecasting-driven planning frameworks
Existing works separate forecasting from planning optimization. Future research should employ ensemble learning or deep learning for EV and RES demand prediction, incorporate probabilistic forecasting outputs into optimization models, and quantify forecast error effects using sensitivity analysis rather than using forecasting as a preprocessing step. [Source: Paper Section 4, lines 1361-1364]

### G2: Insufficient multi-objective formulations including environmental and reliability criteria
Most existing studies concentrate on technical issues such as power losses, voltage stability, and economic benefits, with limited attention to environmental impacts and long-term reliability. Comprehensive investigations integrating technical, economic, environmental, and reliability impacts with advanced forecasting are lacking. [Source: Paper Section 4, lines 1267-1272]

### G3: Need for multi-stage stochastic planning frameworks
The majority of current research uses static or one-period optimization models. Multi-stage stochastic planning frameworks that concurrently consider scenario-based RES generation uncertainty, probabilistic EV arrival/departure behavior, and load growth forecasts over medium- and long-term horizons should be developed. [Source: Paper Section 4, lines 1334-1340]

### G4: Limited policy and business model integration
Present research on EVCS and RES integration focuses on technical and economic optimization with very little attention paid to commercial models and policy frameworks. Large-scale adoption may confront obstacles in investment risks, stakeholder participation, and customer acceptability without proper governmental support. [Source: Paper Section 4, lines 1319-1326]

### G5: Separation of operational control from siting decisions
Current studies frequently separate operational control and siting decisions. Future models should incorporate network reconfiguration, coordinated active-reactive power regulation, BESS sizing and dispatch, and EVCS deployment in bi-level or hierarchical optimization frameworks. [Source: Paper Section 4, lines 1342-1346]

## Key Insight

The central insight synthesized by this review is that **predictive accuracy, uncertainty propagation, and multi-objective planning performance must be jointly addressed** for effective EVCS-RES integration. Methodological choices in forecasting (statistical vs. AI-based) have a cascading effect on the quality of siting and sizing solutions, yet most planning frameworks treat these as separate stages. An integrated analytical framework that connects forecasting accuracy with planning outcomes is the primary research direction needed to address the technical, economic, environmental, and reliability challenges of EVCS-RES deployment in distribution networks.

## Assumptions

1. EV adoption will continue to grow, making EVCS infrastructure planning increasingly critical.
2. RES penetration in distribution networks will continue to increase, amplifying uncertainty challenges.
3. Sufficient historical data exists or can be synthetically generated for training AI-based forecasting models.
4. Distribution network operators can implement advanced optimization algorithms in practice.
5. Policy frameworks will continue to evolve to support EV and RES integration.
