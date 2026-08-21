# Algorithm

## Genetic Algorithm (GA) for Reinforcement Planning

### Chromosome Encoding
Each chromosome represents a candidate reinforcement plan and contains:
- **Tie line selection bits**: Binary flags for each candidate tie line (0=not installed, 1=installed).
- **NO switch placement bits**: Binary flags for each candidate NO switch location.
- **Feeder upgrade genes**: Integer values (0=no upgrade, 1=Alternative 1/250A, 2=Alternative 2/450A, 3=Alternative 3/900A) for each upgradeable feeder.
- **Substation upgrade genes**: Integer values for substation upgrade alternatives.
- **Timing genes**: Integer values (1, 2, or 3) indicating the stage when each investment is executed.

### GA Process
1. **Initialization**: Generate initial population of chromosomes randomly.
2. **Fitness Evaluation**: For each chromosome:
   a. Decode the reinforcement plan (which components, which upgrades, when).
   b. For each stage, for each contingency, for each operating scenario:
      - Perform N-1 contingency analysis.
      - Define Sequence-Path Set (SPi), Affected Bus Set (ABC), and Potential Restoration Solutions (PRC).
        - **SPi**: All elements on the series route from substation to bus i.
        - **ABC**: Buses impacted by the specific contingency.
        - **PRC**: Available restoration paths for the formed island.
      - Check Restoration (Mode 1):
        - Verify at least one restoration path exists.
        - Run forward/backward sweep load flow.
        - Check thermal limits, voltage limits, substation capacity, power balance.
      - If Restoration fails, check Islanding (Mode 2):
        - Verify total DG generation >= total load + 5% losses.
      - Compute success probabilities using indicator functions ISR and ISI.
   c. Calculate per-bus unavailability (Equation 27), SAIDI (Equation 28), ENS (Equation 31).
   d. Check reliability constraints (SAIDI <= 2.5 h/year, ENS <= 5 MWh/year per bus).
   e. Compute objective function: NPV of all costs + penalty for violated constraints.
3. **Selection**: Rank chromosomes by fitness (lower objective = better). Select top performers for reproduction.
4. **Crossover**: Combine genetic material from parent chromosomes to create offspring.
5. **Mutation**: Apply random mutations to maintain population diversity.
6. **Replacement**: Form new population from selected parents and offspring.
7. **Termination**: Repeat steps 2-6 until convergence criterion met (e.g., maximum generations or fitness stagnation).

### Reliability Assessment (Analytical)
1. For each contingency C and bus i:
   - Compute isolation probability P_isolated_i,c (Equation 22).
   - For each operating scenario s, check restoration (ISR) and islanding (ISI) success.
   - Sum weighted probabilities: P_SRSI_i,c = sum(Ps * (ISR + ISI)) (Equation 24).
   - Compute success probability: P_success_i = P_isolated_i * P_SRSI_i,c (Equation 23).
   - Compute unavailability: Ui = sum(lambda_C * r_C - P_success_i * NH) (Equation 27).
2. Compute system indices:
   - SAIDI = sum(Ui * Ni) / sum(Ni) (Equation 28).
   - ASAI = (sum(Ni*NH) - sum(Ui*Ni)) / (sum(Ni*NH)) (Equation 29).
   - ENS = sum(La(i) * Ui) (Equation 31).

### Forward/Backward Sweep Load Flow
Used for each network topology and operational scenario to verify:
- Voltage levels at all buses stay within limits.
- Feeder currents stay within thermal limits.
- Substation power injections stay within capacity.
- Power balance is maintained.

### Penalty Mechanism
A penalty constant Pf is applied when reliability constraints are breached (mu_c = 1 for each violated constraint), guiding the GA away from infeasible solutions.
