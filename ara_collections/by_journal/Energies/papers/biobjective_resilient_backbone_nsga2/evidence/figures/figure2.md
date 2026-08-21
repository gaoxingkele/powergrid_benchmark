# Figure 2: Overall Solution Process of the TER-NSGA-II Algorithm

## Source
Section 5.4, Page 12

## Content
Flowchart of the complete TER-NSGA-II solution process, showing:
1. Start
2. Initialization (input grid parameters, candidate set, random initial population)
3. Initial evaluation and feasibility check (connectivity repair and constraint preprocessing)
4. Stage determination and hierarchical constraint handling
5. Genetic operations (offspring generation)
6. Reverse learning trigger (if t mod Treverse = 0)
7. Reverse chromosome generation and repair
8. Constraint repair and objective recalculation
9. Environmental selection (non-dominated sorting + crowding distance + elite retention)
10. Termination check
11. Greedy post-processing of Pareto front
12. End

## Image
`figure2.png` (Page 12 of the PDF)
