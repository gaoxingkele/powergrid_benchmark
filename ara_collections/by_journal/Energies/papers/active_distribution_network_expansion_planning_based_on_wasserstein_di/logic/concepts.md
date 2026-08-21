# Concepts

## Distributionally Robust Optimization (DRO)
- **Notation**: $\min_{x \in X} \{ c^T x + \max_{\mathbb{P} \in \mathcal{P}} \mathbb{E}_{\mathbb{P}}[Q(x,\xi)] \}$ (Section 3)
- **Definition**: A decision-making framework under uncertainty that optimizes for the worst-case expected cost over an ambiguity set $\mathcal{P}$ of plausible probability distributions, bridging the gap between stochastic optimization (single known distribution) and robust optimization (worst case over a deterministic set).
- **Boundary conditions**: Requires an ambiguity set that contains the true distribution with high confidence but is not overly large; the Wasserstein ball is one such set. The inner worst-case expectation must be computationally tractable (via duality in this paper).
- **Related concepts**: Wasserstein distance ambiguity set, Stochastic optimization, Robust optimization

## Wasserstein Distance Ambiguity Set
- **Notation**: $\mathcal{P} = \{ \mathbb{P} : W(\mathbb{P}, \hat{\mathbb{P}}_N) \leq \varepsilon \}$ (Eq. 1–2, Section 3.1)
- **Definition**: The set of all probability distributions $\mathbb{P}$ whose Wasserstein distance $W$ to the empirical distribution $\hat{\mathbb{P}}_N$ of historical DG/load scenarios is at most $\varepsilon$, where $\varepsilon$ (the radius) controls the level of conservativeness.
- **Boundary conditions**: Requires a choice of $\varepsilon$; too small fails to cover the true distribution, too large causes excessive conservatism. The Wasserstein metric requires a ground cost function (typically Euclidean or L1 norm). The set contracts at rate $O(N^{-1/d})$ as sample size grows.
- **Related concepts**: Distributionally robust optimization, Empirical distribution, Wasserstein metric

## Soft Open Point (SOP)
- **Notation**: $P_{i}^{SOP} + P_{j}^{SOP} + A^{SOP}(|P_{i}^{SOP}| + |P_{j}^{SOP}|) = 0$ (Eq. 5–7, Section 2.1)
- **Definition**: A power-electronic device based on back-to-back voltage-source converters installed at a normally-open tie point between two distribution feeders, capable of continuously controlling active power flow between the feeders and independently providing reactive power support on each side.
- **Boundary conditions**: Investment cost 1000 CNY/kW, unit capacity 10 kW, max 1 MW per line, loss coefficient 0.02, O&M coefficient 0.01. Provides both active power transfer and reactive power compensation; more expensive than interconnection switches but offers continuous regulation.
- **Related concepts**: Interconnection switch, VSC (Voltage Source Converter), Active distribution network

## Interconnection Switch
- **Notation**: Binary variable $\mu_{ij}^{sw} \in \{0,1\}$ (Section 2.1)
- **Definition**: A mechanical switching device installed at a tie position between two distribution feeders that can open or close the branch, providing discrete (on/off) interconnection control without continuous power regulation capability.
- **Boundary conditions**: Investment cost 100,000 CNY each, O&M coefficient 0.05. Cheaper than SOP but provides only binary switching; cannot control power flow continuously or provide reactive support.
- **Related concepts**: SOP, Tie switch, Network reconfiguration

## Second-Order Cone Programming (SOCP) Relaxation
- **Notation**: $\| [2P_{ij}, 2Q_{ij}, V_i - l_{ij}] \|_2 \leq V_i + l_{ij}$ (Eq. 18, Section 4.2)
- **Definition**: A convex relaxation of the nonconvex AC optimal power flow constraints that replaces the quadratic equality relating voltage, current, and power with a second-order cone inequality; exact when the network is radial and certain conditions hold.
- **Boundary conditions**: Exact on radial distribution networks with no reverse power flow at the substation; may introduce a relaxation gap on meshed networks. The relaxed problem is convex and can be solved by commercial solvers.
- **Related concepts**: MISOCP, AC power flow, Convex relaxation, Optimal power flow

## McCormick Relaxation
- **Notation**: $w \geq uv_L + u_L v - u_L v_L$, $w \geq uv_U + u_U v - u_U v_U$ (Section 4.4)
- **Definition**: A convex relaxation technique that replaces bilinear terms $w = uv$ in an optimization model with linear over- and under-estimator constraints based on the variable bounds $[u_L, u_U]$ and $[v_L, v_U]$, producing a mixed-integer linear or second-order cone approximation.
- **Boundary conditions**: Tightness depends on the width of variable bounds; tighter bounds yield tighter relaxations. The relaxation may be iteratively refined via bound tightening. In this paper, applied to bilinear terms arising from the product of dual variables and uncertainty parameters in the Lagrange dual formulation.
- **Related concepts**: Bilinear programming, Convex relaxation, Lagrange duality, Bound tightening

## Lagrange Duality (for Wasserstein DRO inner problem)
- **Notation**: $\max_{\mathbb{P} \in \mathcal{P}} \mathbb{E}_{\mathbb{P}}[Q(x,\xi)] = \min_{\lambda \geq 0} \{ \lambda \varepsilon + \frac{1}{N} \sum_{n=1}^N \max_{\xi \in \Xi} [Q(x,\xi) - \lambda \cdot d(\xi, \hat{\xi}_n)] \}$ (Section 4.3)
- **Definition**: A technique that converts the inner maximization over probability distributions (over an infinite-dimensional space constrained by the Wasserstein ball) into a finite-dimensional minimization over a scalar Lagrange multiplier $\lambda$ and a finite sum of per-scenario maximizations, making the DRO problem tractable.
- **Boundary conditions**: Requires strong duality (holds for Wasserstein DRO with convex ground cost and measurable cost function); introduces a scalar parameter $\lambda$ that depends on the Wasserstein radius $\varepsilon$.
- **Related concepts**: Wasserstein distance ambiguity set, Duality theory, Distributionally robust optimization
