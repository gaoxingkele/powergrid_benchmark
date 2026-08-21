# Improved Genetic Algorithm (IGA) for IES Low-Carbon Operation

## Overview

The IGA is a multi-objective evolutionary algorithm that extends the NSGA-II framework [23] with three novel mechanisms: cyclic crossover, adaptive polynomial mutation, and constraint-prioritizing selection. It optimizes two competing objectives — total operating cost (Eq. 26) and total carbon emissions (Eq. 27) — subject to IES operational constraints (Eq. 1-10, 12-18, 28-30).

## Mathematical Formulation

### Objective Functions

**Objective 1 — Minimize total operating cost:**
min C = Cgrid + Cgas + Cco2(e) + Ccur

where:
- Cgrid = tiered electricity purchase cost (Eq. 19)
- Cgas = tiered natural gas purchase cost (Eq. 21)
- Cco2(e) = tiered carbon emission cost (Eq. 20)
- Ccur = renewable curtailment cost (Eq. 11)

**Objective 2 — Minimize total carbon emissions:**
min e = eCHP + eGB + egrid

where:
- eCHP = carbon emissions from CHP unit (Eq. 23)
- eGB = carbon emissions from gas boiler (Eq. 24)
- egrid = carbon emissions from grid-purchased electricity (Eq. 25)

### Decision Variables (per time slot t = 1..24)
- VCHP_t: natural gas volume consumed by CHP unit
- VGB_t: natural gas volume consumed by gas boiler
- PPV_t: photovoltaic power output
- PWT_t: wind power output
- Pgrid_t: electricity purchased from grid
- Pch_t: ESS charging power
- Pdch_t: ESS discharging power

### Constraints
- CHP power limits: PCHP,min ≤ PCHP_t ≤ PCHP,max (Eq. 3)
- CHP heat limits: 0 ≤ QCHP_t ≤ QCHP,max (Eq. 4)
- WHU recovery: QWHU_t = QCHP_t * ηWHU, 0 ≤ QWHU_t ≤ QWHU,max (Eq. 5-6)
- Gas boiler heat: QGB_t = VGB_t * ηGB * LNG, 0 ≤ QGB_t ≤ QGB,max (Eq. 7-8)
- PV limits: 0 ≤ PPV_t ≤ PPV,max_t (Eq. 9)
- Wind limits: 0 ≤ PWT_t ≤ PWT,max_t (Eq. 10)
- ESS SOC dynamics: SOCBE_t = SOCBE_{t-1} + ηch*zch_t*Pch_t*Δt/EBE - zdch_t*Pdch_t*Δt/EBE (Eq. 12)
- ESS charge/discharge exclusivity: zch_t + zdch_t ≤ 1, zch_t, zdch_t ∈ {0,1} (Eq. 17)
- ESS SOC bounds: 0 ≤ SOCBE_t ≤ 1, SOCBE_1 = SOCBE_24 = 0.5 (Eq. 16, 18)
- Power balance: PCHP_t + Pgrid_t - zch_t*Pch_t + ηdch*zdch_t*Pdch_t + PPV_t + PWT_t = Pload_t (Eq. 29)
- Heat balance: QCHP_t + QWHU_t + QGB_t = Qload_t (Eq. 30)
- Gas balance: Vgas_t = VCHP_t + VGB_t (Eq. 28)

## Pseudocode

```
1: Input: IES parameters (CHP limits, GB limits, ESS params, loads, prices, renewable profiles)
2: Initialize population X_0 with N individuals uniformly random within bounds (Eq. 31)
3: Evaluate objectives C(X_i) and e(X_i) for each individual X_i
4: for generation g = 1 to G_max do:
5:   # Parent selection (Section 3.2) — binary tournament with constraint priority
6:   MatingPool ← ∅
7:   while |MatingPool| < N do:
8:     Select two individuals a, b randomly from X_{g-1}
9:     Winner ← Compare(a, b) using three-tier constraint-prioritizing rule
10:    Add Winner to MatingPool
11:  end while
12:
13:  # Cyclic crossover (Section 3.3) — generate offspring
14:  Offspring ← ∅
15:  for each pair (p1, p2) from MatingPool do:
16:    o1, o2 ← CyclicCrossover(p1, p2)  // exchange genes along closed cycles
17:    Add o1, o2 to Offspring
18:  end for
19:
20:  # Polynomial mutation (Section 3.4) — introduce variation
21:  for each o in Offspring do:
22:    βm ← βmin_m + g  // update distribution index (Eq. 36)
23:    for each gene in o do:
24:      a ← UniformRandom(0, 1)
25:      ψ ← min((xp1 - xmin), (xmax - xp2)) / (xmax - xmin)  // Eq. 35
26:      if a ≤ 0.5 then:
27:        σ ← [2a + (1-2a)(1-ψ)^(βm+1)]^(1/(βm+1)) - 1  // Eq. 32
28:      else:
29:        σ ← 1 - [2a + (1-2a)(1-ψ)^(βm+1)]^(1/(βm+1))  // Eq. 32
30:      end if
31:      xp1 ← 0.5[x1 + x2 - γ(|x1 - x2|)]  // Eq. 33
32:      xp2 ← 0.5[x1 + x2 + γ(|x1 - x2|)]  // Eq. 34
33:      o.gene ← ApplyMutation(o.gene, σ)
34:    end for
35:  end for
36:
37:  # Evaluate offspring
38:  Evaluate objectives and constraint violations for each o in Offspring
39:
40:  # Selection between parents and offspring (Section 3.5)
41:  X_g ← ∅
42:  for each pair (parent, offspring) do:
43:    Winner ← Compare(parent, offspring) using same three-tier rule
44:    Add Winner to X_g
45:  end for
46:
47:  # Fast non-dominated sorting + crowding distance (Section 3.6)
48:  ParetoRanks ← FastNonDominatedSort(X_g, [C objective, e objective])
49:  CrowdingDist ← CalculateCrowdingDistance(X_g, ParetoRanks)
50:  X_g ← SelectByRankAndDistance(X_g, ParetoRanks, CrowdingDist, N)
51: end for
52:
53: # Weight-based Pareto solution selection (Section 3.7, Eq. 37)
54: ParetoFront ← ExtractRank1Solutions(X_{G_max})
55: for each solution k in ParetoFront do:
56:   sk ← w1 * o^k_1 + w2 * o^k_2  // w1 = w2 = 1
57: end for
58: return argmin_k sk  // Pareto-optimal solution with best weighted score
```

## Comparison Function (Three-Tier Constraint-Prioritizing Rule)
```
function Compare(a, b):
    if both a and b satisfy all constraints:
        return NonDominatedSortWinner(a, b)  // standard NSGA-II dominance
    else if exactly one satisfies all constraints:
        return the feasible individual
    else:  // both violate constraints
        return the one with smaller total constraint violation degree
    end if
end function
```

## Cyclic Crossover Procedure
```
function CyclicCrossover(p1, p2):
    n ← length of chromosome
    visited ← [false] * n
    o1 ← [null] * n
    o2 ← [null] * n

    // Find cycles and exchange
    for start = 0 to n-1:
        if not visited[start]:
            // Trace cycle starting at start
            cycle ← []
            idx ← start
            while not visited[idx]:
                visited[idx] ← true
                cycle.append(idx)
                // Find position in p2 that has same value as p1[idx]
                idx ← position of p2 where p2[idx] == p1[idx]
                idx ← position of p1 where p1[idx] == p2[idx]  // complete the mapping
                if idx == start: break
            end while

            // Alternate assignment: odd cycles → o1 gets p1, o2 gets p2
            // Even cycles → o1 gets p2, o2 gets p1
            for each index i in cycle:
                if cycle is odd-numbered:
                    o1[i] ← p1[i]; o2[i] ← p2[i]
                else:
                    o1[i] ← p2[i]; o2[i] ← p1[i]
                end if
            end for
        end if
    end for
    return o1, o2
end function
```

Note: The pseudocode for cyclic crossover is reconstructed from the paper's verbal description (Section 3.3) and the illustration (Figure 3). The exact implementation details (especially the cycle-tracing termination condition) may vary from the actual code implementation.

## Complexity Analysis
- Not specified in paper. The fast non-dominated sorting has O(MN^2) complexity for M=2 objectives and N=population size, as per NSGA-II [23]. Cyclic crossover adds O(n) per crossover operation where n = chromosome length (7 × 24 = 168 genes). Polynomial mutation is O(n) per individual.
