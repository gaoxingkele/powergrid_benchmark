# Mathematical Formulation

All equations transcribed from the paper (§III Problem Formulation, §III-D/E, §IV). Symbols follow
the paper's notation. Constraint formulations for shutdown cost, minimum up/down time, and active
power limits are referred by the paper to reference [27] and not re-printed there.

## Objective — total DA UC cost (Eq. 1)
$$C_{Tot} = \sum_{i=1}^{n}\sum_{t=1}^{T}\left(F_{i,t}\,u_{i,t} + StC_{i,t}\,u_{i,t} + SdC_{i,t}\,u_{i,t}\right)$$
Minimize the aggregation of fuel cost $F_{i,t}$, start-up cost $StC_{i,t}$, and shutdown cost
$SdC_{i,t}$ of all committed generators over the 24 hours of the next day. $u_{i,t} = 1$ for a committed
unit, 0 for a decommitted unit, for generator $i$ at hour $t$. Maintenance cost is neglected.

## Supply-demand balance (Eq. 2)
$$\sum_{i=1}^{n} u_{i,t}\,P_{i,t} = \sum_{t=1}^{T} D_{t}^{f}$$
Assuming DC power flow, total generation by all committed thermal generators equals the forecasted
load demand $D_t^f$ at hour $t$. $P_{i,t}$ is the generated power of unit $i$ at hour $t$.

## Generator fuel cost (Eq. 3)
$$F_{i,t} = \alpha_i\,P_{i,t}^{2} + \beta_i\,P_{i,t} + \gamma_i$$
Quadratic fuel-cost curve with cost coefficients $\alpha_i, \beta_i, \gamma_i$.

## Start-up cost (Eq. 4)
$$StC_{i,t} = StC_{i,t}^{Tbn} + \left(1 - e^{-\frac{hd}{Cb}}\right)StC_{i,t}^{Blr} + StC_{i,t}^{M}$$
Sum of turbine start-up cost $StC^{Tbn}$, boiler start-up cost $StC^{Blr}$ scaled by the boiler
cool-down term, and maintenance start-up cost $StC^{M}$. $hd$ (= $H_{d,i}$) is the number of hours a
unit is down; $Cb$ (= $B_{c,i}$) is the Boiler Cool-Down Coefficient.

## Ramp-up limit (Eq. 5)
$$\left(P_{i,t} - P_{i,(t-1)}\right) \le P_i^{RU,max},\quad \forall i, \forall t$$

## Ramp-down limit (Eq. 6)
$$\left(P_{i,t} - P_{i,(t-1)}\right) \ge P_i^{RD,min},\quad \forall i, \forall t$$

## Spinning reserve (Eq. 7)
$$R_t \ge (0.1 * R_i),\quad \forall i, \forall t$$
Generation reserve maintained at ten percent of the operating reserve (Case 1). In Case 2 the reserve
fraction is reduced stepwise to 8%, 5%, 0%.

## Available capacity for dispatch (Eq. 8)
$$P^{avl} = \sum_{i=1}^{n}\left(P_i^{max} - R_i\right),\quad \forall t$$
Total capacity available for DA UC after subtracting the operating (spinning) reserve. On IEEE RTS:
2795 MW at 10% SR (Base Case & Case 1), 2857 MW at 8%, 2950 MW at 5%, 3105 MW at 0%.

## Contingency Margin (Eq. 9)
$$M_{da}^{k} = \sum_{i=1}^{n} R_i^{k}$$
CM for contingency 'Cy', aggregating the spinning reserve $R_i^{Cy}$ of generator $i$ for the $k$-th
contingency. Values: 310.5 MW (10%), 248 MW (8%), 155 MW (5%), 0 MW (0%).

## LOLP maximum limit (Eq. 10)
$$LOLP_k \le LOLP_{max},\quad k \in [1, Cy]$$
$k$ indexes the assessed contingencies; $Cy$ is the contingency index.

## Per-hour, per-contingency LOLP (Eq. 11)
$$LOLP_{k,t} = Prob\left[D_{f,t} > \sum_{i=1}^{N}\left(P_{i,t}\,u_{i,t}\right)\right],\quad \forall t$$
Probability of load loss is non-zero when demand exceeds overall available generation for hour $t$.

## LOLP over all contingencies for an hour (Eq. 12)
$$LOLP_{t} = Prob\left[D_{f,t} > \sum_{k=1}^{Cy}\sum_{i=1}^{N}\left(P_{k,i,t}\,u_{k,i,t}\right)\right],\quad \forall t$$

## Aggregated 24-hour LOLP (Eq. 13)
$$LOLP = \left(\sum_{t=1}^{24} LOLP_{k,t}\right)$$
Sum of hourly loss-of-load probabilities over the next day, per the considered contingencies.

## Conditional LOLP definition (Eq. 14)
$$LOLP_{k,t} = \begin{cases} Prob\left[D_{f,t} > \sum_{i=1}^{N}(P_{i,t}u_{i,t})\right], & \text{if } P^{cap,avail} < D_f^{t};\ \forall t \\ 0, & \text{otherwise};\ \forall t \end{cases}$$
Hourly LOLP is non-zero only if available capacity is below the forecasted demand for that hour;
compiled in the Capacity Outage Probability Table (COPT).

## Operating margin (Eq. 15)
$$M_{da}^{o} = (LOLP_{max} - LOLP)$$
The system's residual capacity beyond committed reserves. Positive → headroom for additional load or
contingencies (system can withstand without collapse); negative → heightened probability of failure,
additional generation needed.

## Failure rate from MTTF (Eq. 16)
$$\lambda = \frac{1}{t_{FR}}$$
Failure rate $\lambda$ is the reciprocal of mean time to failure $t_{FR}$ (MTTF), used to build the
COPT generation-unavailability probabilities.
