# Heuristics (design/tuning choices the paper states)

## H01: Place FDB selection in the exploration-phase update (Eq. 17), not the exploitation/ground update
- **Rationale**: FDB was inserted at several distinct position-update points of COA; the comparison
  identified the exploration tree-climbing update (Eq. 17 → FDBCOA1) as the best insertion for the
  exploration/exploitation balance, while inserting it in the ground update (Eq. 19 → FDBCOA2/3)
  gave worse scalability. FDB steers the search toward unexplored regions with the best solutions.
- **Sensitivity**: high — the three placements produce clearly different mean Friedman ranks (1/2/3)
  and FDBCOA3 shows "severe scalability problems."
- **Bounds**: only placements in Eqs. 17 and 19 were tested (Table 1); placement in the Stage-2
  escape update (Eq. 22) was not tested.
- **Code ref**: [src/execution/fdbcoa_obl.py]
- **Source**: §III-B, Table 1, Algorithm 1; Tables 2–7.

## H02: Seed the initial population with Elite OBL (best of 8 OBL schemes)
- **Rationale**: OBL seeding increases initial diversity and convergence speed; Elite OBL derives
  opposites from the best (elite) incumbents, so it balances exploration/exploitation and prevents
  premature convergence better than the other seven schemes (Classical, Quasi-Reflection, Quasi,
  Super, Random, Dynamic, Probabilistic).
- **Sensitivity**: high — the eight OBL variants (plus non-OBL FDBCOA1) span mean Friedman ranks
  1–7; OBL5 (Elite) ranks 1 while FDBCOA1-without-OBL ranks 7 of 10.
- **Bounds**: applied only during initial-population creation; if the elite opposite exceeds the
  variable bounds it is reset to a random in-bounds value (Eq. 35).
- **Code ref**: [src/execution/fdbcoa_obl.py]
- **Source**: §III-C, Tables 8–13, Figure 4.

## H03: System-specific penalty coefficients scaled to the objective magnitude
- **Rationale**: The equality/inequality penalty weights (ω₁, λ₁, λ₂, λ₃) are set several orders of
  magnitude large so any constraint violation dominates the (soft-constrained) fitness, forcing the
  search toward feasible line-addition plans; the magnitudes are scaled up as the system (and cost
  magnitude) grows from 6-bus to 93-bus.
- **Sensitivity**: Not specified in paper (values are given but no sensitivity sweep reported).
- **Bounds**: Garver 10^5/10^6/10^7/10^5; IEEE-25 10^8/10^9/10^9/10^7; Colombian 93 10^9/5×10^8/5×10^8/5×10^6.
- **Code ref**: Not specified
- **Source**: §IV (penalty coefficients list).

## H04: Run 51 times (benchmarks) / 30 times (TNEP stability) and report distributional statistics
- **Rationale**: The stochastic metaheuristics produce run-to-run variance (best vs worst cost can
  differ by 2–20×), so best/worst/average (51 runs) and SR%/MIT/MST (30 runs) are reported instead
  of a single run, to expose reliability rather than luck.
- **Sensitivity**: Not specified in paper.
- **Bounds**: 51 independent runs for CEC benchmark and TNEP cost tables; 30 independent runs for
  the stability (SR%/MIT/MST) analysis.
- **Code ref**: Not specified
- **Source**: §III (51 runs), §IV-B (30 runs stability).
