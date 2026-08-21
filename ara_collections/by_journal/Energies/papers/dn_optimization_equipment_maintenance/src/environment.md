# Environment

## Language/Runtime
- MATLAB R2021a
- YALMIP (version 0.9.7) for optimization modeling
- Custom MATLAB scripts for hybrid ACO-FHO-DE algorithm implementation

## Framework
- YALMIP optimization modeling framework
- Custom bilevel optimization framework with iterative feedback between upper (topology) and lower (dispatch) layers
- Disflow power flow with big-M convex relaxation

## Hardware
- Standard desktop computer
- Intel i7 CPU
- 32 GB RAM

## Data Sources
- Modified CPS62-node test system derived from a real-world medium-voltage grid in China [Source: Page 9]
- Historical wind, PV, and load data for scenario generation (origin not specified; sourced from the utility)
- Latin Hypercube Sampling for generating 500 uncertainty scenarios from historical distributions

## Key Dependencies
- MATLAB Optimization Toolbox (implicitly, via YALMIP solvers)
- YALMIP 0.9.7 [Source: Page 14]
- Hybrid ACO-FHO-DE algorithm (custom implementation):
  - Tent chaos mapping for population initialization
  - Adaptive weight mechanism for balance between global and local search
  - Ant Colony Optimization for initial solution construction
  - Fire Hawk Optimization for local refinement
  - Differential Evolution for mutation, crossover, and selection

## Protocols
- Distributionally robust optimization with comprehensive norm ambiguity set (joint 1-norm and infinity-norm)
- Confidence level alpha for ambiguity set construction
- K-means-like clustering for scenario reduction from M samples to K typical scenarios
- Bilevel iterative optimization with convergence checking

## Random Seeds
- Not specified in the paper
- Tent chaos mapping (mu = 0.5) used for pseudo-random population initialization
- Latin Hypercube Sampling likely uses unspecified random seed for scenario generation
