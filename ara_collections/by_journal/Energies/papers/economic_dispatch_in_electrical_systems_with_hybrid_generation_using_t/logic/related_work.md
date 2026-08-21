# Related Work

## Metaheuristic Hybrid Approaches
- **PSOGSA [8]**: Hybrid Particle Swarm Optimization with Gravitational Search Algorithm, combining PSO convergence (social/cognitive learning) with GSA exploration (gravitational attraction). Integrated into single-hybrid framework PSOGSA. Shown effective for complex, high-dimensional, constrained problems.
- **Hybrid DE with Cuckoo Search [17]**: Demonstrates DE's combinability with other techniques for economic dispatch; DE- CS improves process optimization quality.

## Mathematical Optimization Approaches
- **Two-stage stochastic MILP [10,11]**: Addresses wind uncertainty using mixed-integer linear programming for dynamic economic dispatch.
- **Convex bi-directional converter models [12]**: Enables efficient dispatch in hybrid AC/DC microgrids with steady-state convex formulations.
- **LP, MILP, convex optimization**: Offer optimality guarantees but suffer scalability limitations under non-convex or large-scale configurations.

## Forecasting Techniques
- **Grey Prediction Model (GPM) [13]**: Based on Grey System Theory, ideal for sparse/incomplete data. Uses Accumulated Generating Operation (AGO) to smooth sequences and first-order linear differential equations for trend modeling.

## Monte Carlo for Renewable Uncertainty
- **Stochastic scenario generation [14]**: Monte Carlo simulation with Weibull (wind speed) and Gaussian/Beta (solar irradiance) PDFs. Thousands of scenarios generated representing possible future resource behavior.

## Economic Dispatch with DE
- **Mean-guiding DE with valve-point effect [24]**: Thermal dispatch incorporating valve-point effects; improved DE mutation stage by adding ideal and best candidates from last generation to the mutant vector, increasing convergence rate.

## Deep Learning Forecasting Methods
- **LSTM networks [31]**: Effective for capturing temporal dependencies in time-series data (solar irradiance, wind speed) for short-term renewable generation forecasting.
- **Hybrid CatBoost with STL decomposition [30]**: Combines Seasonal and Trend decomposition with machine learning for improved forecasting accuracy with multi-year panel data.

## Hydrothermal Dispatch Studies
- **Dynamic programming for coupled hydro plants [18]**: Short-term hydrothermal economic dispatch applied on hydraulically coupled power plants.
- **Heuristic techniques evaluation [20]**: KPI-based evaluation of heuristic techniques for short-term hydrothermal scheduling.
