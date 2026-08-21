# Formulation — Indices, Objective, and Constraints (Eqs. 1–25)

All equation numbers match the paper. Symbols transcribed from §2–§3.

## Criticality indices (§2.1)

- **Eq. 1** — Substation load level: $x_{i1}=\sum q_i$ — $x_{i1}$ is the load level of substation $i$; $\sum q_i$ the aggregate load demand it serves.
- **Eq. 2** — Influence on low-voltage grid: $x_{i2}=\sum n_i$ — $\sum n_i$ the number of 10 kV lines connected to substation $i$.
- **Eq. 3** — Power supply coverage: $x_{i3}=\max l_i$ — distance of the furthest load point supplied by substation $i$.
- **Eq. 4** — Spatial influence: $x_{i4}=\sum l_i$ — sum of the distances of the 10 kV lines connected to substation $i$.
- **Eq. 5** — Load density: $x_{i5}=\sum l_i / n_i$ — average distance between substation $i$ and all connected loads.

## Scoring (§2.2)

- **Eq. 6** — Composite score: $score_i=\sum_{j=1}^{5} w_{ij} X_{ij}$ — $X_{ij}$ standardized index $j$ of substation $i$; $w_{ij}$ its weighting coefficient.
- **Eq. 7** — Sum normalization: $X_{ij}=x_{ij}/\sum_{i=1}^{n_p} x_{ij}$ — $n_p$ = number of substations participating in the scoring.
- Weights (AHP, Table 3): $w = (0.385,\ 0.043,\ 0.120,\ 0.226,\ 0.226)$; consistency ratio CR = 0.00726 (< 0.1 threshold).

## Objective function (§3.1)

- **Eq. 8** — $\min C = C_{SUB220kV}+C_{SUB110kV}+C_{LINE110kV}+C_{LINE10kV}$.
- **Eq. 9** — $C_{SUB220kV}=\sum_{i=1}^{N}\{C_{SUB-i}[\,r_0(1+r_0)^{t_{ms}}/((1+r_0)^{t_{ms}}-1)\,]+C_{OP-i}\}$.
- **Eq. 10** — $C_{SUB110kV}=\sum_{i=1}^{M}\{C_{SUB-i}[\,r_0(1+r_0)^{t_{ms}}/((1+r_0)^{t_{ms}}-1)\,]+C_{OP-i}\}$.
- **Eq. 11** — $C_{LINE110kV}=\beta_{LINE110kV}\,\varepsilon\,[\,r_0(1+r_0)^{t_{110kVml}}/(r_0(1+r_0)^{t_{110kVml}}-1)\,]\,l_{110kV}$.
- **Eq. 12** — $C_{LINE10kV}=\beta_{LINE10kV}\,\varepsilon\,[\,r_0(1+r_0)^{t_{10kVml}}/(r_0(1+r_0)^{t_{10kVml}}-1)\,]\sum_{i=1}^{N+M}\sum_{j=1}^{m} d_{ij}l_{ij} + \alpha_{LINE10kV}\,\varepsilon\sum_{i=1}^{N+M}\sum_{j=1}^{m}(q_j/n_j)d_{ij}l_{ij}$.

**Symbols**: $N,M$ = number of new 220/110 kV substations; $C_{SUB-i},C_{OP-i}$ = investment/annual operating cost of substation $i$; $r_0$ = discount rate; $t_{ms}$ = substation depreciation life; $\beta$ = per-unit-length line investment; $t_{110kVml},t_{10kVml}$ = line depreciation lives; $\alpha_{LINE10kV}$ = 10 kV network-loss conversion factor; $\varepsilon$ = zigzag coefficient of the evolved area; $m$ = equivalent nodes; $l_{110kV}$ = total 110 kV line length; $q_j$ = load of equivalent node $j$; $n_j$ = number of 10 kV main supply lines at node $j$; $l_{ij},d_{ij}$ = $(N+M)\times m$ matrices of 10 kV line length and 0/1 connection between substation $i$ and node $j$.

## Constraints (§3.2–§3.3)

**110 kV substation loading (Eqs. 13–15)**
- **Eq. 13** — $n_j=\sum_{i=1}^{N+M} d_{ij},\ j=1,\dots,m$.
- **Eq. 14** — $p_i=\sum_{j=1}^{m} q_j d_{ij}/n_j,\ i=N+1,\dots,N+M$.
- **Eq. 15** — $p_i \le s_i\,\eta\cos\varphi,\ i=N+1,\dots,N+M$ — $p_i$ actual load; $\eta$ max allowable loading rate; $\cos\varphi$ power factor.

**10 kV primary feeder capacity (Eq. 16)**
- **Eq. 16** — $w_i \le n_j\sqrt{3}\,I_{max}U\cos\varphi,\ j=1,\dots,m$ — $I_{max}$ max safe feeder current; $U$ voltage level.

**110 kV transmission line routing (Eqs. 17–21)**
- **Eq. 17** — $l_{110kV}=3\sum_{i=1}^{N+M}\sum_{j=1}^{N+M} D_{ij}L_{ij}+3\sum_{i=1}^{N+M}\sum_{j=1}^{h} D'_{ij}L'_{ij}$.
- **Eq. 18** — $\sum_{i=1,i\neq j}^{N+M} D_{i,N+k}+\sum_{j=1}^{h} D_{kj'}=1,\ k=1,\dots,M$.
- **Eq. 19** — $\sum_{i=1,i\neq j}^{N+M} D_{N+k,j}+\sum_{j=1}^{h} D_{kj'}=1,\ k=1,\dots,M$.
- **Eq. 20** — $D_{ij},D'_{ij}\in\{0,1\}$.
- **Eq. 21** — $u_j \ge u_i-(D_{ij}-1)M+1,\ 1\le i\neq j\le M$ (traveling-salesman-type anti-loop constraint enforcing a radial dual-supply topology). $h$ = number of existing 110 kV lines; $u_i$ auxiliary series of length $M$.

**110 kV line loading — critical end sections 1a, 2k (Eqs. 22–23)**
- **Eq. 22** — $P_{1a}=\sum_{j=1}^{k} P_j L_j / L_\Sigma \le \sqrt{3}I_{max}U\cos\varphi$.
- **Eq. 23** — $P_{2k}=\sum_{j=1}^{k} P_j L'_j / L_\Sigma \le \sqrt{3}I_{max}U\cos\varphi$ — $L_j,L'_j$ transmission distances from the 220 kV substations to the $j$th substation; $L_\Sigma$ distance between the 220 kV substations.

**220 kV substation loading (Eqs. 24–25)**
- **Eq. 24** — $P_i=\sum_{j=1}^{m} q_j d_{ij}/n_j,\ i=1,\dots,M$.
- **Eq. 25** — $P_i+\sum_{j\in J_j} P'_{ij}\le S_i\,\eta\cos\varphi,\ i=1,\dots,N$ — $P_i$ 10 kV load on the $i$th 220 kV substation; $J_j$ set of its lines; $P'_{ij}$ load on the $j$th line.

## Case-study numeric parameters (§4)
- Discount rate $r_0$ = 8%; max loading factor $\eta$ = 75%; $I_{max}$ = 552 A (10 kV feeders), 718 A (110 kV lines).
- GA: max generations 200, population 800, crossover rate 0.5, mutation rate 0.5.
- Note: per-unit line costs $\beta$, depreciation lives $t_{ms}/t_{110kVml}/t_{10kVml}$, zigzag coefficient $\varepsilon$, network-loss factor $\alpha$, power factor $\cos\varphi$: **Not specified in paper** (only symbolically defined).
