# Methodology: Three Configuration Schemes

## System Model
The offshore wind farm equipped with energy storage follows the structure shown in Figure 1. The battery SOC evolves according to:

**Charging**: SOC(t) = SOC(t-1) + (eta_c * P_c * Delta_t) / E

**Discharging**: SOC(t) = SOC(t-1) - (P_d * Delta_t) / (eta_d * E)

where eta_c and eta_d are charging/discharging efficiencies, P_c and P_d are charging/discharging power, Delta_t is time step, and E is battery capacity.

## Objective Functions

### Investment Cost (C_a)
C_a = C1 + C2 + C3 + C4

- **C1** (Initial investment): k_p * P_es + k_q * S_es (power-related + capacity-related costs)
- **C2** (O&M cost): k_F * P_es + k_V * Q+_ann (fixed maintenance + variable discharge cost)
- **C3** (Replacement cost): Sum of discounted battery replacement costs over project lifespan
- **C4** (Waste disposal cost): Environmentally sound disposal at end of life (excluded from calculations due to regional variation)

### Power Fluctuation (sigma)
sigma = (1/P_N) * sqrt((1/N) * sum_{t=1}^{N} (P_t - mean(P))^2)

where N is number of sampling points, P_t is wind power at time t, and P_N is rated wind farm power.

## Three Schemes

### Scheme 1: Basic Cost-Volatility Trade-off
- **Objective 1**: Minimize C_a (investment cost)
- **Objective 2**: Minimize sigma (volatility)
- **Revenue**: None
- **Analysis**: Weekly (Dec 9-15) and annual optimization; battery life correction applied

### Scheme 2: Spot Market Participation
- **Objective 1**: Minimize (C_a - annual electricity sales revenue)
- **Objective 2**: Minimize sigma
- **Revenue**: Energy storage and wind power sell electricity at real-time spot prices
- **Note**: Negative net cost indicates annual revenue covers full lifecycle investment

### Scheme 3: Peak-Valley Arbitrage
- **Objective 1**: Minimize (C_a - arbitrage revenue)
- **Objective 2**: Minimize sigma
- **Strategy**: Charge batteries only during low-price periods (3:00-5:00 AM); discharge only during high-price periods (6:00-8:00 PM)
- **Additional benefit**: CNY 2.73M/year extra revenue vs Scheme 2 at same configuration

### Optional Switching
In actual operation, the wind farm can flexibly switch between Scheme 2 (when grid stability is needed) and Scheme 3 (when market participation is preferred).

## Selection Methods

### Inflection Point Method
Identifies the point of maximum curvature on the Pareto frontier:
- Gradient: nabla_f = Delta_y / Delta_x
- Curvature: kappa = |d^2y/dx^2|
- Best when objective weights are unclear

### Ideal Point Method (TOPSIS)
- Normalizes objectives: f'_i = (f_i - f_i_min) / (f_i_max - f_i_min)
- Calculates distance to ideal point: D+ = sqrt(sum(f'_ij)^2)
- Best when clear weight relationships exist between objectives
- Used for Scheme 2 (no clear inflection point)
