# Algorithm: Improved GWO (CDGWO)

CDGWO = traditional GWO + chaos-optimization initialization + dynamic opposition-based learning
(DOBL). Transcribed from §3.1-§3.2 and the printed Steps 1-7 / Figure 3.

## 1. Traditional GWO (base) — Eqs. (16)-(19)

Encircling prey (Eq. 16):
```
D = | C * X_prey(t) − X(t) |
X(t+1) = X_prey(t) − A·D
```
Coefficient vectors (Eq. 17):
```
A = 2·a·r1 − a
C = 2·r2
```
`r1, r2` ∈ [0,1] random vectors; `a` = convergence factor, linearly decreased from 2 to 0 over
iterations (governs exploration→exploitation).

Leader-guided update — the ω wolf follows α, β, δ (Eqs. 18, 19):
```
X1(t) = | X_α(t) − A1·| C1·X_α(t) − X(t) | |
X2(t) = | X_β(t) − A2·| C2·X_β(t) − X(t) | |
X3(t) = | X_δ(t) − A3·| C3·X_δ(t) − X(t) | |
X_ω(t+1) = (1/3)·Σ_{i=1..3} X_i(t)
```
α = best solution, β = 2nd, δ = 3rd; ω updated toward the average of the three leader-pulls.

## 2. Chaos optimization (enhancement 1)
Replace the uniform-random initial population with a chaotic sequence. Four candidate maps (Table 3):
Tent, Sine (a=4), Chebyshev (a=4), Logistic (a∈(0,4]). Qualitative analysis favours Logistic and
Chebyshev; the empirical study (Table 4 / Figure 6) selects **Logistic** (fastest runtime, near-best
fitness). Chaos widens initial diversity and speeds early convergence, but its benefit decays in
later iterations.

## 3. Dynamic opposition-based learning (enhancement 2) — Eq. (20)
```
r = sin(t / T)
X̃_i(t) = pop_max + pop_min − r·X_i(t) ,   i = 1..n
```
`pop_max, pop_min` = search-space bounds; `X_i(t)` = current position; `X̃_i(t)` = dynamic reverse
solution; `t` = current iteration; `T` = total iterations. The nonlinear, iteration-varying factor r
makes reverse-solution generation track the evolving landscape (vs. a static opposite), improving
late-stage diversity and local-optima escape.

## 4. CDGWO procedure (printed Steps 1-7; Figure 3)
1. **Step 1** — Initialize the parameters of the grey wolf population.
2. **Step 2** — Use chaotic maps to generate sequences as the initial positions for the wolf
   population (chaotic-map formulas in Table 3).
3. **Step 3** — Establish the fitness function, identical to the MGC objective (Eq. 8). Evaluate the
   fitness of the entire population.
4. **Step 4** — Identify the three grey wolves with the lowest fitness as the α, β, δ wolves; they
   guide the rest of the population.
5. **Step 5** — Perform dynamic opposition-based learning: search at both the current positions and
   their direct opposites (Eq. 20) to raise the chance of finding superior solutions.
6. **Step 6** — Update individual positions under α/β/δ guidance (Eqs. 18-19); update the global
   optimum.
7. **Step 7** — If termination (iteration limit) is met, output the optimal fitness value; else
   recompute fitness on the updated positions and iterate from Step 3.

(Minimization convention: lowest fitness = best, since the objective is a cost.)

## Complexity
Not specified in paper. (Only relative statements are given: e.g. FA is noted as O(n^2); CDGWO's own
complexity is not stated. Runtimes are empirical — see Table 5.)

## Grounding
Reconstructed from printed equations (Eqs. 16-20) and the printed Steps 1-7 + Figure 3 flowchart.
Numerical hyperparameters (population size, T, search bounds) are **not specified in the paper**, so
no runnable code stub is produced (see `src/environment.md`).
