# Algorithm: Improved Weighted Average Algorithm (IWAA)

## Type
Metaheuristic swarm intelligence optimization algorithm for multi-objective optimization.

## Base: Weighted Average Algorithm (WAA)

The WAA is inspired by the concept of weighted average position. It constructs a weighted average position of the entire population in each iteration to prevent individuals from becoming trapped in local optima.

### WAA Core Mechanism

1. **Population Initialization (Equation 36)**:
   ```
   X_n(i) = rand(N, D) * (ub_n(i) - lb_n(i)) + lb_n(i)
   ```
   N: population size, D: dimension

2. **Weighted Average Position (Equations 38-41)**:
   - Select top N_candidate individuals based on fitness
   - N_candidate = nP - ((nP - 4) / Maxit) * it
   - Compute Fitness_Sum = sum(Fitness(X_i))
   - Compute quality center X_miu (for minimization):
     ```
     X_miu = (sum(X_i * (Fitness_Sum - Fitness(X_i)))) / (Fitness_Sum * (N_candidate - 1))
     ```
   - Compute weighted position X_Miu:
     ```
     X_Miu = sum(X_i * Fitness(X_i)) / Fitness_Sum
     ```

3. **Phase Switching (Equation 42)**:
   ```
   f(it) = (alpha * rand - 1) * sin(pi * it / Max_it)
   ```
   Threshold = 0.5
   - f(it) >= 0.5: Exploitation phase
   - f(it) < 0.5: Exploration phase

4. **Exploitation Strategies**:
   - **Strategy 1** (Equation 43): Guided by global best, personal best, and weighted average
     ```
     X_i(t+1) = w11*(X_miu - X_GlobalBest) + w12*(X_miu - X_PersonalBest) + w13*X_miu
     ```
   - **Strategy 2** (Equation 44): Guided by personal best and weighted average (fast convergence)
     ```
     X_i(t+1) = w21*(X_miu - X_PersonalBest) + w22*X_PersonalBest
     ```
   - **Strategy 3** (Equation 45): Guided by global best and weighted average (balance)
     ```
     X_i(t+1) = w31*(X_miu - X_GlobalBest) + w32*X_GlobalBest
     ```

5. **Exploration Strategies**:
   - **Levy Flight** (Equations 46-49): Random walk with mostly small steps and occasional large jumps
     ```
     S = U / |V|^(1/beta)
     X_i,j(t+1) = X_GlobalBest_j(t) + S
     ```
   - **Random Repositioning** (Equation 50): Jump to random position in search space
     ```
     X_i,j(t+1) = rand * (ub_min - lb_min) + lb_min
     ```

## IWAA Enhancements

### Enhancement 1: Refraction Opposition-based Learning (Equation 51)

Applied to the second exploration strategy to enable the algorithm to escape local optima.

```
X_i'(t+1) = (ub + lb)/2 + (ub + lb)/(2*t) - X_i(t) / t    when r <= 0.5
X_i'(t+1) = (ub + lb)/2 - (ub + lb)/(2*t) + X_i(t) / t    when 0.5 < r <= 1
```

Where:
- X_i'(t+1): refraction opposition solution
- r: random value in [0, 1]
- t: current iteration
- ub, lb: upper and lower bounds

### Enhancement 2: Dynamic Crowding Distance (Equation 52)

Standard crowding distance:
```
I(x_i) = sum(|f_m(x_j) - f_m(x_k)| / f_m_max)  for m = 1 to n
```

**Improved Approach — Sequential Removal**:
1. Calculate crowding distance for all Pareto solutions
2. Sort in descending order of crowding distance
3. Remove the solution with the smallest crowding distance
4. Recalculate crowding distances for remaining solutions
5. Repeat until N solutions remain

This maintains better diversity and uniformity compared to conventional single-pass selection.

## IWAA Pseudocode (Algorithm 2 in paper)

```
Input: Population size N, Dimension D, MaxIter
Output: Optimal solution X_best

1: Initialize positions X_n(i) = rand(N,D) * (ub - lb) + lb
2: for t = 1 to MaxIter do
3:    Select best N_candidate solutions
4:    Compute quality center X_miu and weighted position X_Miu
5:    if f(it) >= 0.5 then  // Exploitation
6:        Apply Strategy 1, 2, or 3
7:    else  // Exploration
8:        Apply Refraction Opposition-based Learning
9:        Apply Levy Flight
10:   end if
11:   Calculate crowding distance for each Pareto solution
12:   Sort by descending crowding distance
13:   Remove smallest-distance solutions until |ParetoSet| <= N
14: end for
15: return X_best
```
