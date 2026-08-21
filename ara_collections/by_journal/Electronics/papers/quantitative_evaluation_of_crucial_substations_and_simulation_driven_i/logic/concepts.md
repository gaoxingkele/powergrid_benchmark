# Concepts

## Planned substation importance (criticality) score
- **Notation**: $score_i = \sum_{j=1}^{5} w_{ij} X_{ij}$ (Eq. 6)
- **Definition**: A composite scalar quantifying how critical a newly planned substation $i$ is to multi-voltage grid development, formed as the AHP-weighted sum of its five standardized (sum-normalized) evaluation indices. Higher score = more critical; used both to identify crucial substations and to prioritize construction sequencing.
- **Boundary conditions**: Defined relative to the set of $n_p$ substations participating in the scoring (indices are sum-normalized across that set, Eq. 7); scores are comparative, not absolute.
- **Related concepts**: AHP, Sum normalization, Substation evaluation indices

## Substation evaluation indices (the five criticality indicators)
- **Notation**: $x_{i1}=\sum q_i$; $x_{i2}=\sum n_i$; $x_{i3}=\max l_i$; $x_{i4}=\sum l_i$; $x_{i5}=\sum l_i / n_i$ (Eqs. 1–5)
- **Definition**: (1) Substation load level — aggregate served load demand; (2) Influence on low-voltage grid — number of 10 kV feeder lines connected; (3) Power supply coverage — distance to the farthest supplied load point; (4) Spatial influence — total length of connected 10 kV lines; (5) Load density — average distance between the substation and its connected loads.
- **Boundary conditions**: Computed from the network topology and load allocation of a given planning-year configuration (here the 2020 baseline).
- **Related concepts**: Planned substation importance score, Sum normalization

## Analytic Hierarchy Process (AHP)
- **Notation**: pairwise comparison matrix $C=[c_{ij}]$, $c_{ji}=1/c_{ij}$
- **Definition**: A multi-criteria decision-analysis method that decomposes a decision into objective/criteria/alternative layers, elicits pairwise importance judgments via the Santy scale, derives criterion weights (priority vectors) from the comparison matrix, verifies consistency, and synthesizes composite scores. Used here to weight the five criticality indices.
- **Boundary conditions**: Relies on expert pairwise judgments; validity is contingent on passing a consistency check.
- **Related concepts**: Santy scale, Consistency ratio, Planned substation importance score

## Santy scale
- **Notation**: values {1, 3, 5, 7, 9} with intermediates {2,4,6,8} and reciprocals $1/k$
- **Definition**: The 1–9 intensity scale used to express the relative importance of one element over another in AHP pairwise comparisons (1 = equally important … 9 = extremely more important), with reciprocals encoding the inverse comparison. (Table 1.)
- **Boundary conditions**: Applies to pairwise element comparisons within a hierarchical level.
- **Related concepts**: AHP, Consistency ratio

## Consistency ratio (CR)
- **Notation**: CR (threshold 0.1)
- **Definition**: A diagnostic for the coherence of AHP pairwise judgments; values below 0.1 indicate acceptable consistency. For this paper's indicator matrix, CR = 0.00726.
- **Boundary conditions**: Computed per pairwise comparison matrix.
- **Related concepts**: AHP, Santy scale

## Sum normalization (relative scoring)
- **Notation**: $X_{ij} = x_{ij} / \sum_{i=1}^{n_p} x_{ij}$ (Eq. 7)
- **Definition**: A normalization that rescales each raw index by the sum of that index over all participating substations, producing comparable relative scores and avoiding the subjectivity of fixed upper/lower score limits used in traditional normalization.
- **Boundary conditions**: Defined over the pool of $n_p$ substations being scored together.
- **Related concepts**: Substation evaluation indices, Planned substation importance score

## Multi-voltage level grid evolution model
- **Notation**: $\min C = C_{SUB220kV}+C_{SUB110kV}+C_{LINE110kV}+C_{LINE10kV}$ (Eq. 8)
- **Definition**: An evolutionary simulation that co-plans 220/110/10 kV networks by minimizing total per-horizon construction+operating cost, using the previous period's topology as the starting point and autonomously generating expansion (siting/sizing of 220/110 kV substations, 110 kV reconfiguration, 10 kV feeder provisioning). Run with and without a substation's delay to difference out the incremental impact.
- **Boundary conditions**: Subject to loading, feeder-capacity, routing, and radial dual-supply constraints (Eqs. 13–25); solved by a genetic algorithm.
- **Related concepts**: Automatic topology reconfiguration, Genetic algorithm solution, Incremental cost of delayed commissioning

## Automatic topology reconfiguration
- **Notation**: —
- **Definition**: A mechanism inside the evolution simulation that autonomously establishes optimal connections for newly built substations — including tee-off ('3T') breakout connections onto existing 110 kV infrastructure and provisioning of additional 10 kV feeders to the nearest under-loaded substation — so generated schemes reflect real expansion patterns.
- **Boundary conditions**: Triggered when load exceeds capacity thresholds or when loop-closure/overload constraints would be violated.
- **Related concepts**: '3T' connection scheme, Multi-voltage level grid evolution model

## '3T' connection scheme / two-terminal dual supply
- **Notation**: radial dual-supply topology (Eqs. 17–21; Figures 1–2)
- **Definition**: A 110 kV interconnection architecture combining a loop-network backbone with breakout ('3T'/tee) connections, giving each load point two independent supply paths while the traveling-salesman-type constraint (Eq. 21) prevents inadvertent loop closure. Line loading peaks in the two end sections (1a, 2k).
- **Boundary conditions**: Applies to 110 kV transmission routing; 10 kV uses an (n+1) redundancy (n main feeders + 1 standby).
- **Related concepts**: Automatic topology reconfiguration, Multi-voltage level grid evolution model

## Incremental cost of delayed commissioning
- **Notation**: (cumulative converted total for delay scenario − baseline) / baseline
- **Definition**: The relative increase in cumulative annual (discounted, converted) multi-voltage construction+operating cost caused by postponing a substation's commissioning by one planning horizon, measured against the on-schedule baseline plan. It is the economic quantity the framework attributes to a delay and correlates with the importance score.
- **Boundary conditions**: Cumulated across planning years (2020, 2025, 2035) and discounted (8%) to the initial year.
- **Related concepts**: Multi-voltage level grid evolution model, Planned substation importance score

## Genetic algorithm solution
- **Notation**: gene sequence $2\times(N+M)$ coordinates + $M$ topology genes
- **Definition**: The metaheuristic used to solve the constrained evolution model: 220/110 kV substation x/y coordinates and each new 110 kV substation's upstream connection are encoded as genes; constraint violations incur a large penalty in the fitness (total cost) function to enforce feasibility.
- **Boundary conditions**: Configured with max generations 200, population 800, crossover rate 0.5, mutation rate 0.5.
- **Related concepts**: Multi-voltage level grid evolution model
