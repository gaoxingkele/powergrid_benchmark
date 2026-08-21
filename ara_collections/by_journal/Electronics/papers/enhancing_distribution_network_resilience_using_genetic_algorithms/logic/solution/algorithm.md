# Algorithm — Tailored Genetic Algorithm

Source: §3 "AI Techniques—Genetic Algorithms" (pp.5–7, general GA mechanics + Figure 2 flowchart) and
§5–§6 (the GA configuration applied to the 6-bus feeder). No formal numbered algorithm/pseudocode
block is printed; the flow below reconstructs the paper's stated loop (Figure 2 + §3 prose). The
exact fitness form is in `formulation.md`.

## Encoding
- Each candidate solution is encoded into a **binary chromosome** — a sequence of "0"s and "1"s (§3,
  p.6). The initial population Ps is generated randomly via a pseudo-random number generator.
- The chromosome encodes the control variables (DER real/reactive setpoints, regulator taps,
  reconfiguration actions). The exact bit-layout / gene mapping is **Not specified in paper**.

## Operators (§3, p.6)
- **Selection**: pairs of chromosomes are chosen as parents for reproduction. Natural selection
  retains only the Ps individuals with the lowest error (best fitness) from the expanded population
  of Ps + Nc·Ps/2 members. (The paper first writes this expanded size as "Ps + Nc·Ps/P, as each of
  the Ps/2 parent pairs contributes Nc children" and then as "Ps + Nc·Ps/2" — the "/P" appears to
  be a typo for "/2"; both variants are recorded here, per §3, p.6.)
- **Crossover**: parents exchange Np parts of their genetic material to form offspring; applied here
  with **crossover probability 0.8** (§5, p.9).
- **Mutation**: with small probability Pm individual bits flip (0↔1), injecting diversity; applied
  here with **mutation rate 0.05** (§5, p.9).
- **Evaluation / Replacement**: the objective F is evaluated for all new candidates; the new
  generation = parent population + offspring, then trimmed back to Ps by fitness.

## Applied configuration (§5, p.9)
- Population size Ps = 50 individuals
- Crossover probability = 0.8
- Mutation rate = 0.05
- Generations run = 100
- Fitness = weighted sum of total power loss + penalty for voltage deviation outside 0.95–1.05 pu
  (the operational restatement of F = w1·f1 + w2·f2 + w3·f3)

## Reconstructed control flow (from Figure 2)

```
START
  INITIALIZE POPULATION      # Ps random candidates
  ENCODE                     # binary chromosomes
  repeat:
      SELECTION              # pick parent pairs
      CROSSOVER              # exchange Np parts, prob 0.8
      (MUTATION)             # bit-flip, rate 0.05
      EVALUATE               # compute F for offspring
      REPLACE                # keep best Ps of parents+offspring
      if TERMINATION CRITERION MET:   # no significant improvement in mean error ee,
          break                       #   or generations exceed Nmax (= 100 here)
  STOP -> best individual
```

(Figure 2 shows MUTATION folded implicitly between CROSSOVER and EVALUATE; §3 prose states it
explicitly as a post-crossover step.)

## Termination
Terminates when either (a) there is no significant improvement in the mean error e_e across the
population, or (b) the number of generations exceeds the pre-defined maximum N_max (100 here). §3, p.6.

## Complexity analysis
Not specified in paper. (Population-based; per-generation cost dominated by Ps power-flow / fitness
evaluations, but no complexity statement is given.)
