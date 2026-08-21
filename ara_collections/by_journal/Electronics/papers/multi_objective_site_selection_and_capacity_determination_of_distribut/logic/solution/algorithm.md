# Solver: Multi-Objective Particle Swarm Optimization (MOPSO) Planning Flow

The three-objective siting/sizing model (formulation.md) is solved with a multi-objective
particle swarm optimizer (MOPSO). The abstract calls it "an improved multi-objective particle
swarm optimization algorithm", but the body of the paper does not detail any algorithmic
modification over standard MOPSO — the specific improvement is Not specified in paper.

## End-to-end planning flow (Figure A1, Appendix A)

Reconstructed from the paper's stated flowchart (see evidence/figures/figureA1.md); no code is
released, and no steps beyond the flowchart are invented:

1. **Start** — "Initialize the parameters of AND [ADN], PV and EV".
2. **DG-data thread** — "The Frank function is used to process WT and PV data" (scenario
   generation, method.md §1) → "Establish the MOPSO model".
3. **EV-data thread** (parallel input) — "Historical data on EVs is collected" → "The
   CNN-Bi-LSTM method is used for prediction" → "The predicted EV data is obtained"
   (method.md §2).
4. **Merge** — "Enter the relevant parameters and solve the calculation".
5. **MOPSO iteration loop**:
   - "Update the parameters of MOPSO"
   - "MOPSO is used to generate new fitness values"
   - "Call the MOPSO function and use cplex to solve the optimal ADN scheme based on multiple
     objectives" — i.e., CPLEX is invoked inside the loop to solve the ADN scheme for the
     candidate siting/capacity particles.
   - "Meet the convergence conditions?" — if No, loop back to the parameter-update step; if
     Yes → **End** (final EVS locations and capacities; in the case study: nodes 13 and 33,
     Figure 9).

## Fitness / objectives
Each particle encodes an EVS siting/capacity scheme; fitness is evaluated on the three objectives
f1 (node voltage fluctuation), f2 (network loss), f3 (storage capacity) defined in Eqs. (1)–(3).
Population size, inertia/acceleration coefficients, archive strategy, iteration budget, and the
convergence condition are Not specified in paper.

## Complexity / efficiency
No complexity analysis is given. The paper itself flags solver efficiency as a limitation (§5,
p.11): "the solution efficiency of MOPSO is slow and needs to be further improved" — improving it
is named as future work (§6).

## Bindings
- Verified by experiments E01 (four-scenario objective comparison), E02 (voltage surfaces),
  E04 (siting result).
- Supports claims C01, C02, C05.
