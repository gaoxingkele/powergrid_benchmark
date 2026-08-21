# Figure 7: The flowchart of the FDBCOA-OBL algorithms

- **Source**: Figure 7, §III-C (p.35090)
- **Caption**: "The flowchart of the FDBCOA-OBL algorithms."
- **Screenshot**: figure7.png (top of page; full flowchart)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (top to bottom):
  1. Input information of optimization problem
  2. Set parameters of N and T; set t = i = 1
  3. Create the random initial population → Evaluate the objective function
  4. **OBL block** (pink, "The part where the Opposition Based Learning Strategies are applied"): Create an oppositional population according to OBL strategies (x̄, x̄_qr, x̄_q, x̄_SO, x̄_j^E, x̄_r, x̄_d, x̄_p) → Evaluate the objective function
  5. Compare the evaluated objective functions and determine the best population
  6. Update position of the iguana
  7. **FDB block** (yellow/green, "The part where the Fitness Distance Balance Method is applied"): decision `i > N/2`? — No branch: Calculate X_i^{P1} (FDB form of Eq. 17) → Update X_i via Eq. 20 (loop i = i+1); Yes branch → Generate iguana randomly (Eq. 18) → Calculate X_i^{P1} (Eq. 19) → Update via Eq. 20
  8. **Exploitation column** (right): decision `i < N` → Calculate X_i^{P2} via Eqs. 21–22 → Update X_i via Eq. 23 (loop i=i+1) → Set i=1 → Save the best candidate solution found so far
  9. Decision `t < T`? Yes → t = t+1, i = 1 (loop back to iguana update); No → Output the best solution found by FDBCOA-OBL
- **Connections**: two nested loops (inner over population index i, outer over stage t up to T); the OBL block feeds the "best population" determination only at initialization; the FDB block and exploitation block form the per-iteration update.
- **Annotations**: a "Guide" legend marks Phase 1 (yellow) and Phase 2; pink box = OBL; the FDB-applied region is highlighted.
- **What it conveys**: the two enhancement operators sit at distinct points — OBL only at initial-population creation, FDB only inside the Phase-1 position update — confirming they are independent, composable interventions. This structure is mirrored in `logic/solution/algorithm.md`. Supports C01, C02, C03.
