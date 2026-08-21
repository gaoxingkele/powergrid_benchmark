# Environment: Methodological Context of the Review

This file describes the methodological environment used in the review, not a software implementation. As a survey paper, the "environment" is the research methodology and literature base.

## Methodology Type
- Systematic literature review with comparative taxonomy development
- Narrative synthesis with quantitative statistical analysis (Table 5 objective distribution)

## Literature Database Sources (implicit)
- IEEE Xplore
- ScienceDirect (Elsevier)
- MDPI journals
- Springer
- Web of Science / Scopus (assumed)

## Coverage Period
- Studies published primarily from 2016 through early 2026
- Selected seminal earlier works cited for foundational methods

## Classification Framework
- Forecasting methods: Bifurcation into learning-based vs. non-learning-based
- Planning algorithms: Bifurcation into deterministic vs. stochastic/metaheuristic
- Objectives: Quadripartite (technical, economic, environmental, reliability)

## Key Dependencies (referenced literature base)
- ~135 references from peer-reviewed journals and conferences
- Predominantly from: Energies, IEEE Transactions on Power Systems, IEEE Access, Applied Energy, Energy, Journal of Energy Storage, Sustainable Cities and Society, eTransportation, and others

## Analytical Software/Methods Used by Reviewed Studies
- **Forecasting:** Python (TensorFlow, PyTorch), MATLAB, R
- **Optimization:** MATLAB (Optimization Toolbox, YALMIP), GAMS, CPLEX, Python (Pyomo, SciPy)
- **Load flow:** OpenDSS, MATPOWER, DIgSILENT PowerFactory, ETAP
- **Monte Carlo simulation:** Custom implementations in MATLAB and Python

## Protocols
- Review protocol: Narrative synthesis approach (not PRISMA-based systematic review)
- Classification: Hierarchical taxonomy development
- Quantitative analysis: Statistical proportion analysis of objective functions across surveyed studies

## Data Sources for Reviewed Studies
- Real-world EV charging datasets (various sources including Chinese energy service providers)
- Standard distribution test systems (IEEE 33-bus, IEEE 69-bus, radial distribution networks)
- Solar irradiance and wind speed historical data
- Transportation network data for coupled power-transport studies

## Evaluation Metrics (across surveyed literature)
- MAE, RMSE, MAPE, R² for forecasting accuracy
- Power loss (kW), voltage deviation (p.u.), VSI for technical performance
- Installation/investment/operational cost ($) for economic performance
- CO2 emission reduction (kg or %) for environmental performance
- SAIFI, SAIDI, ENS for reliability performance

## Random Seeds
- Not applicable to the review methodology itself; individual reviewed studies used seeds for stochastic simulations.

## Constraints on the Review
- Only English-language publications were considered
- Focus on distribution network level (not transmission or generation)
- Emphasis on grid-connected systems rather than microgrids or islanded operation
