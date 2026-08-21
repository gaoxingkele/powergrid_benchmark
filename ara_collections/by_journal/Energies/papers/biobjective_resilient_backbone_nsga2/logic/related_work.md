# Related Work

## Pumped-Storage and Backbone-Grid Coordinated Planning
Existing research primarily focuses on economic and technical feasibility of pumped-storage planning, with insufficient attention to the resilience-support value under extreme conditions (Refs [9,10]). Current studies on resilience value modeling predominantly focus on functional implementation of pumped-storage equipment, discussing black-start control, emergency output regulation, and rapid load response (Refs [11-13]). However, quantitative models that explicitly characterize the contribution of pumped-storage units during post-fault system recovery are still lacking.

## N-1 Connectivity Constraints
Traditional methods have significant limitations in handling N-1 connectivity constraints:
- **Penalty function approaches** (Refs [14-16]): Essentially soft constraint designs that cannot strictly satisfy the rigid safety requirement of edge connectivity >= 2, especially in complex network topologies where they generate numerous infeasible solutions
- **Rigid constraint methods**: Few studies address rigid constraints, and those that do encounter issues with exponential computational complexity and convergence difficulties for large-scale backbone-grid planning

## Multi-Objective Evolutionary Algorithms for Grid Planning
Standard NSGA-II performs well for general multi-objective optimization due to elite retention, fast non-dominated sorting, and crowding distance mechanism (Ref [38]). However, it exhibits:
- Insufficient constraint handling for problems with strong engineering constraints (Ref [39])
- Randomness of crossover and mutation often generating infeasible solutions violating connectivity and N-1 constraints
- Reliance on penalty functions severely reducing optimization efficiency
- Lack of precise quantification and evolutionary guidance for N-1 connectivity
- Fixed elite-selection mechanism incompatible with incremental hierarchical constraints (Ref [40])

The proposed TER-NSGA-II addresses these gaps by introducing a three-stage framework and graph-theoretic validation.

## Power System Resilience Assessment
Grid resilience emphasizes maintaining critical services under extreme disturbances, differing from traditional reliability (Refs [31,32]). Existing studies show that resilience assessment needs to consider both structural and functional changes (Ref [33,34]). This paper extends existing approaches by coupling structural accessibility (recovery-distance) with functional support capacity (pumped-storage hub effect) in a multiplicative formulation.

## Positioning of This Work
This paper fills the gap at the intersection of:
1. Pumped-storage planning with explicit resilience quantification
2. Rigorous N-1 connectivity constraint handling
3. Multi-objective optimization under hierarchical constraints
4. Integration of graph-theoretic validation into evolutionary algorithms

The key differentiators are: (a) the resilience mismatch index incorporating pumped-storage hub effects, (b) the three-stage TER-NSGA-II with max-flow min-cut validation, and (c) periodic reverse learning for population diversity maintenance.
