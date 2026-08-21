# Method: Planning Solution (SABPSO) and Scenario Generation

## Solver overview (§4)
The multi-objective planning model is solved by a **hybrid chaotic binary particle swarm
optimization (SABPSO)** based on Pareto theory and a small-niching (small-habitat) sharing
technique. Particles are binary-coded — Eq. (11):

    C_code = { T1 S1, T2 S2, ..., T_{N_DG} S_{N_DG}, U1, U2, ..., U_{N_up}, N1 D1, N2 D2, ..., Nl Dl }

- T_i, S_i — grid-connected type and capacity of DG at candidate location i
- U_i — whether the i-th line is converted to DC
- N_i, D_i — access line number of expanded load point i and whether it is a DC line
- l — number of newly added load points

## Multi-objective machinery (§4.1)
- **Pareto dominance**: X_a dominates X_b if f_i(X_a) ≤ f_i(X_b) for all i and strictly < for some i.
- **Pareto rank**: non-dominated solutions = rank 1; remove them, next non-dominated = rank 2, etc.
- **Crowding degree — Eq. (12)**: n_d = n_d + (f_m(i+1) − f_m(i−1)) / (f_m^max − f_m^min); boundary
  individuals get infinite crowding, keeping the front spread even in objective space.
- **Elite retention**: parent C_i and child D_i merged into R_i; fill C_{i+1} whole-layer by
  ascending Pareto rank, then fill the last partial layer by descending crowding degree.

## Planning process (§4.2, Figure 6)
Random initial population of size N → first offspring via GA selection/crossover/mutation →
from generation 2, combine parent+offspring, fast non-dominated sorting + crowding, select new
offspring → repeat until stop → output compromise optimum via niche sharing.

### Detailed 14-step procedure (§4.2)
1. Input grid info, set parameters (Table 2 categories), encode/init population, I=1, max I=Imax.
2. Number particles k=1, population size kmax, time-series scenario n=1, daily slot t=1.
3. Compute probabilistic load flow at slot t under typical time-series case n.
4. If constraints violated, penalize fitness (f1/f4 → Cmax, f2/f3 → Cmax) and go to (8); else (5).
5. If t<48, t=t+1, go to (3); else (6).
6. If n<12, n=n+1, t=1, go to (3); else (7).
7. Compute adaptation from the lower-level objective.
8. If k<kmax, k=k+1, n=t=1, go to (3); else (9).
9. Select individual optimum by dominance before/after particle update (random tiebreak).
10. Merge new solution set with old Pareto non-dominated set; filter and de-duplicate.
11. If I<Imax, I=I+1, go to (12); else (14).
12. Select global optimum from the Pareto set via small-niching sharing.
13. Update all particles, return to (2).
14. Select the compromise optimum via fuzzy affiliation and variance assignment.

Note: the printed procedure references f4 and a "lower-level objective function," implying a
bi-level structure (upper: investment/topology; lower: operational load-flow fitness). The paper
lists only three objective functions f1-f3 explicitly; f4 is mentioned only in the penalty step
and is not defined — recorded as a gap.

## Scenario generation
- DG output and load are represented as **typical time-series scenarios**: N_t typical
  time-series scenarios (the procedure iterates n<12, i.e. 12 scenarios), each day discretized
  into T=48 time slots (procedure iterates t<48).
- Each scenario j carries a days-per-year weight d_j and each sub-scenario s a probability p_{s,j};
  all objective terms (Eqs. 2, 5, 6) are probability- and time-weighted sums over these scenarios.
- The exact scenario-clustering/generation algorithm (how the 12 typical scenarios and their
  probabilities are derived from raw DG/load data) is **not specified in the paper**.

## Compromise-solution selection
The final single plan is chosen from the Pareto non-dominated set by **fuzzy affiliation and
variance assignment** (step 14) combined with the **small-niching sharing** global-optimum
selection (step 12).

## Worked planning outcomes
- 13-node single-stage (Scenario 1 vs 2): Figure 7 — see E01, C01.
- 13-node multi-stage evolution 0-80%: Figure 8 + Table 3 — see E02, C01/C02.
- IEEE33 consider-DC: Tables 5-6, Figure 10 — see E03, C03/C05.
- IEEE33 exclude-DC: Table 7 — see E04, C05.
- Comparison + stability: Table 8, Figure 11 — see E05, C04/C08.
