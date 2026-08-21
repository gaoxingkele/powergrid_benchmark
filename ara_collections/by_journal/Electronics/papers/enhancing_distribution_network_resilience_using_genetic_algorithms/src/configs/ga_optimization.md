# Config — GA Optimization

Concrete hyperparameter and weight values used for the 6-bus case study. Source: §5 Objective
Function, p.9 (and §3 for GA mechanics). These are configuration values stated in the paper, not code.

## Population size (Ps)
- **Value**: 50 individuals
- **Rationale**: Not specified in paper
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5, p.9 ("a population size of 50 individuals")

## Crossover probability
- **Value**: 0.8
- **Rationale**: Not specified in paper
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5, p.9 ("a crossover probability of 0.8")

## Mutation rate
- **Value**: 0.05
- **Rationale**: Not specified in paper
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5, p.9 ("a mutation rate of 0.05")

## Number of generations
- **Value**: 100
- **Rationale**: Also serves as N_max termination cap; run may stop earlier on stagnation in mean
  error e_e
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5, p.9 ("run for 100 generations"); §3, p.6 (termination on N_max)

## Objective weights (w1, w2, w3)
- **Value**: (0.4, 0.4, 0.2) for (voltage profile f1, power loss f2, resilience penalty f3)
- **Rationale**: Equal priority to voltage and loss; lighter weight on the resilience penalty
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper (single fixed vector; no sweep reported)
- **Source**: §5, p.9 ("w1, w2, w3 weight factors equal to 0.4, 0.4 and 0.2, respectively")

## Voltage constraint band
- **Value**: 0.95 ≤ V_i ≤ 1.05 pu
- **Rationale**: Operational limit; deviations outside it are penalized in the fitness
- **Search range**: n/a (constraint)
- **Sensitivity**: Not specified in paper
- **Source**: §5, p.9 ("0.95 ≤ V_i ≤ 1.05")
