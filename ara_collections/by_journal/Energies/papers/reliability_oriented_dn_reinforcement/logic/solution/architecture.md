# Architecture

## Two-Level Hierarchical Framework

The proposed reinforcement planning framework operates at two levels:

### Level 1: Long-Term Reinforcement Planning (Strategic)
- **Inputs**: System topology, load growth forecasts, DG capacities/locations, component reliability parameters, regulatory targets, cost data.
- **Decision Variables** (encoded in GA chromosome):
  - Selection of candidate tie lines (binary)
  - Placement of normally open (NO) switches (binary)
  - Feeder upgrade alternatives (integer: A1=250A, A2=450A, A3=900A)
  - Substation upgrade alternatives (integer: 13.3 MVA or 16.7 MVA)
  - Investment timing (integer: stage 1, 2, or 3)
- **Objective**: Minimize NPV of total investment + interruption costs subject to reliability constraints.
- **Solver**: Genetic Algorithm metaheuristic.

### Level 2: Contingency Management (Operational)
- **Mode 1 -- Network Restoration**: When a fault occurs, protection isolates the affected section. If alternative paths exist via tie lines, switching operations restore supply to isolated loads. Conditions: thermal limits, voltage limits, substation capacity, power balance.
- **Mode 2 -- Intentional Islanding**: When restoration is infeasible, the isolated section operates as an island supplied by local DGs. Condition: DG generation >= load + losses.
- **Assessment**: Forward/backward sweep load flow for each topology and scenario.

## System Architecture Diagram
```
+----------------------------------------------------------+
|            INPUT DATA                                     |
|  System Topology | Load/GEN Data | Reliability Params    |
|  Cost Data       | Regulatory Targets                    |
+----------------------------------------------------------+
                          |
                          v
+----------------------------------------------------------+
|     PROBABILISTIC SCENARIO GENERATION                    |
|  Load: Normal PDF -> discrete states                     |
|  Solar: Beta PDF -> discrete states                      |
|  Wind: Weibull PDF -> discrete states                    |
|  Scenario Matrix = all combinations x probabilities       |
+----------------------------------------------------------+
                          |
                          v
+----------------------------------------------------------+
|     GA OPTIMIZATION ENGINE                               |
|  Chromosome Encoding: tie lines, NO switches, upgrades   |
|  Fitness = NPV objective + penalty                       |
|  Selection | Crossover | Mutation                         |
+----------------------------------------------------------+
                          |
                          v
+----------------------------------------------------------+
|     RELIABILITY ASSESSMENT MODULE                        |
|  For each candidate solution:                             |
|  - Define SPi, ABC, PRC sets                             |
|  - For each contingency + scenario:                      |
|    - Check Restoration (Mode 1): thermal, voltage, etc.  |
|    - If fail, check Islanding (Mode 2): DG adequacy      |
|  - Compute SAIDI, ENS per bus per stage                  |
|  - Compare to regulatory thresholds                      |
+----------------------------------------------------------+
                          |
                          v
+----------------------------------------------------------+
|     OUTPUT: Optimal Reinforcement Plan                    |
|  Tie lines to install | NO switches to place             |
|  Feeders to upgrade | Substations to upgrade             |
|  Investment timing | NPV breakdown                       |
+----------------------------------------------------------+
```

## Data Flow
1. System parameters and historical data fed into probabilistic scenario generator.
2. Scenario matrix passed to reliability assessment module.
3. GA generates candidate reinforcement plans.
4. For each candidate plan, reliability module evaluates SAIDI/ENS under all contingencies and scenarios using the two-level hierarchy.
5. Fitness (NPV + penalties) computed and fed back to GA.
6. GA evolves population until convergence.
7. Optimal plan reported with full cost breakdown.
