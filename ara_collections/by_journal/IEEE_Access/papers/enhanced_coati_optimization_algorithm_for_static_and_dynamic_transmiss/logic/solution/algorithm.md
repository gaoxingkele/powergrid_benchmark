# Algorithm: FDBCOA-OBL (FDB + Elite-OBL enhanced Coati Optimization)

The method enhances the Coati Optimization Algorithm (COA) with two independent operators:
(1) Fitness-Distance Balance (FDB) selection injected into a position-update step, and
(2) Opposition-Based Learning (OBL) seeding of the initial population. The final algorithm is
FDBCOA1-OBL5 (FDB placed in the exploration update; Elite OBL for initialization).

## 1. Base Coati Optimization Algorithm (COA)

Population initialization (Eq. 16):
```
X_i : x_{i,j} = lb_j + r (ub_j − lb_j),   i = 1..N, j = 1..m
```
where N = number of coatis, m = number of decision variables, r ∈ [0,1] random, lb/ub bounds.

**Stage 1 — Exploration (hunting/attacking iguanas).** 50% of coatis climb trees to threaten the
iguana; the remaining wait on the ground. Tree-climbing update (Eq. 17):
```
X_i^{P1} : x_ij^{P1} = x_{i,j} + r (Iguana_j − I·x_{i,j}),   i = 1..N/2, j = 1..m
```
The iguana falls to a random ground position (Eq. 18):
```
Iguana^G : Iguana_j^G = lb_j + r (ub_j − lb_j)
```
Ground coatis update (Eq. 19):
```
x_{i,j}^{P1} = x_{i,j} + r(Iguana_j^G − I·x_{i,j})   if F_{Iguana^G} < F_i
            = x_{i,j} + r(x_{i,j} − Iguana_j^G)      else
            i = N/2+1 .. N
```
`Iguana_j` = optimal position (best) in dimension j; I ∈ {1,2} chosen randomly. Greedy accept (Eq. 20):
`X_i = X_i^{P1} if F_i^{P1} < F_i else X_i`.

**Stage 2 — Exploitation (escaping predators).** Local bounds shrink with iteration t (Eq. 21):
```
lb_j^{local} = lb_j / t,   ub_j^{local} = ub_j / t,   t = 1..T
```
Escape update (Eq. 22):
```
X_i^{P2} : x_{i,j}^{P2} = x_{i,j} + (1 − 2r)(lb_j^{local} + r·(ub_j^{local} − lb_j^{local}))
```
Greedy accept (Eq. 23): `X_i = X_i^{P2} if F_i^{P2} < F_i else X_i`.

## 2. Fitness-Distance Balance (FDB) selection

Given candidates P and their fitness F (Eq. 24), the Euclidean distance of each candidate to the
best is (Eq. 25):
```
D_{P_i} = sqrt( (x_{1P_i} − x_{1P_best})^2 + ... + (x_{mP_i} − x_{mP_best})^2 ),  P_i ≠ P_best
```
The FDB score vector (Eqs. 27–28):
```
SP_i = ω × normF_{P_i} + (1 − ω) × normD_{P_i}
```
selects a guiding candidate that is both high-fitness and far from the current best, preserving
diversity. ω is a weighting coefficient preventing F and DP from overshadowing each other (value
Not specified in paper).

**FDB placement variants (Table 1):**
- **FDBCOA1** — FDB replaces `x_{i,j}` with `x_{FDB,j}` in the Stage-1 tree-climbing update (Eq. 17).
- **FDBCOA2** — FDB replaces the *else* branch term in the Stage-1 ground update (Eq. 19): `x_{i,j} + r(x_{FDB,j} − Iguana_j^G)`.
- **FDBCOA3** — FDB replaces the *if* branch base term in the Stage-1 ground update (Eq. 19): `x_{FDB,j} + r(Iguana_j^G − I·x_{i,j})`.

Empirically FDBCOA1 is best (see claims C02); it is carried forward.

## 3. Opposition-Based Learning (OBL) seeding

Eight schemes generate an opposition population during initialization; the best incumbent is kept.
- Classical OBL (Eq. 29): `x̄ = lb + ub − x`
- Quasi-Reflection OBL (Eq. 31): reflects about the midpoint (mid = (ub+lb)/2) with random scaling
- Quasi OBL (Eq. 32): quasi-adverse between midpoint and opposite
- Super OBL (Eq. 33): extended contrast
- **Elite OBL (Eqs. 34–35)**: `x̄_ij^E = rand × (lb_j + ub_j) − x_i^E`; reset within bounds if out of range
- Random OBL (Eq. 36): `x̄_r = lb + ub − rand × x`
- Dynamic OBL (Eq. 37): `x̄_d = rand × (lb + ub − x)`
- Probabilistic OBL (Eq. 38): selects among the above by a random probability p in five bands

The eight seeded variants are FDBCOA1-OBL1…OBL8. Empirically Elite OBL (OBL5) is best (claim C03).

## 4. Pseudocode of FDBCOA (Algorithm 1, transcribed)

```
While (Termination criterion not met: up to maxFEs)
  Phase 1: Hunting and attacking strategy on the iguana (Exploration Phase)
    For i = 1 : N/2
      Compute distance of each solution candidate using Eq. (25).      // FDBCOA1
      Compute FDB score for each solution candidate using Eq. (27).    // FDBCOA1
      Calculate new position for the i-th coati:                       // FDBCOA1
        x_ij^{P1} = x_{FDB,j} + r·(Iguana_j − I·x_{i,j})
      Update position of the i-th coati using Eq. (20).
    End for
    For i = 1 + N/2 : N
      Generate position of the iguana randomly using Eq. (18).
      Compute distance of each solution candidate using Eq. (25).      // FDBCOA2, FDBCOA3
      Compute FDB score for each solution candidate using Eq. (27).    // FDBCOA2, FDBCOA3
      Calculate new position (FDBCOA2 uses x_{FDB,j} in the else branch of Eq. 19;
        FDBCOA3 uses x_{FDB,j} as the base in the if branch of Eq. 19).
      Update position of the i-th coati using Eq. (20).
    End for
  // Phase 2 (Exploitation) applies Eqs. (21)-(23) for all coatis (see Fig. 7 flowchart).
End while
End
```

## 5. Full FDBCOA-OBL flow (Figure 7)

1. Input optimization problem; set N and T; set t = i = 1.
2. Create random initial population; **also create an oppositional population via the OBL strategies
   (x̄, x̄_qr, x̄_q, x̄_SO, x̄_j^E, x̄_r, x̄_d, x̄_p)** and evaluate — keep the best population.
3. Compare evaluated objective functions and determine the best population.
4. Update position of the iguana.
5. **FDB part**: for i ≤ N/2 compute X_i^{P1} (FDB in Eq. 17) and update via Eq. 20; else generate
   iguana (Eq. 18), compute X_i^{P1} (Eq. 19), update via Eq. 20.
6. **Exploitation part**: for i < N compute X_i^{P2} (Eqs. 21–22), update via Eq. 23; save best.
7. If t < T, t = t+1, i = 1, loop; else output best solution.

## Complexity analysis
Not specified in paper (only maxFEs = 10000×Dim termination and 51 independent runs are stated).
