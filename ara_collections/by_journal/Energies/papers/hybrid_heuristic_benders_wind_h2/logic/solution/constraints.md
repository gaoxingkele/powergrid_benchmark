# Model Constraints

## Power Balance (Equation 13)
```
P_WT_{s,t} + P_FC_{s,t} + P_grid_buy_{s,t}
  = P_EL_{s,t} + P_grid_sell_{s,t} + P_load_{s,t} - σ_load_{s,t}
```
Real-time power equilibrium: generation + imports = consumption + exports - load shed.

## Hydrogen Mass Balance (Equations 14-16)
```
m_prod_{s,t}             = η_EL · P_EL_{s,t}
m_loss_{s,t}             = λ_loss · S_H2_{s,t-1}
S_H2_{s,t}               = S_H2_{s,t-1} + m_prod_{s,t} - P_FC_{s,t}/η_FC - D_H2_{s,t} - m_loss_{s,t}
S_H2_{s,0}               = S_H2_{s,24}  (cyclic boundary condition)
```
Hydrogen storage level evolution considering production, fuel-cell consumption, exogenous demand, and losses.

## Investment Capacity Bounds (Equations 17a-17d)
```
0  ≤ P_WT_{s,t}   ≤ ξ_wind_{s,t} · P_WT_rated · x_WT      (wind power availability)
0  ≤ P_EL_{s,t}   ≤ P_EL                                    (electrolyzer capacity)
0  ≤ S_H2_{s,t}   ≤ η_vol · E_H2                            (storage capacity)
0  ≤ P_FC_{s,t}   ≤ P_FC                                    (fuel cell capacity)
```
All operational variables bounded by installed capacities from Stage I.

## Variable Domains
- x_WT ∈ {0,1} (binary — wind farm construction)
- P_EL ∈ R_+ (electrolyzer capacity)
- E_H2 ∈ R_+ (hydrogen tank capacity in MWh, converted to Nm³ via η_vol)
- P_FC ∈ R_+ (fuel cell capacity)
- All operational variables ≥ 0

## Objective (Annualized)
```
Minimize: C_inv(x) + Σ_s π_s · Q(x, ξ_s)
```
where:
```
C_inv(x) = (1/L) · [ C_WT(x_WT) + C_EL(P_EL) + C_FC(P_FC) + C_H2(E_H2) ]
Q(x, ξ_s) = 365 · Σ_t [ λ_buy_t · P_grid_buy_{s,t} - λ_sell_t · P_grid_sell_{s,t} + ρ_shed · σ_load_{s,t} ]
```

## Hydrogen Tank Cost (Black-Box Benchmark)
```
C_H2(E_H2) = max( C_min, C_base(E_H2) + C_cyc(E_H2) )
C_base(E_H2) = { κ_H2 · (E_H2)^0.7            if 0 < E_H2 ≤ 50
               { (κ_H2 · (E_H2)^0.7) · 0.9     if E_H2 > 50
C_cyc(E_H2)  = κ_cyc · sin(E_H2 / 10)
```
With C_min = $1 × 10⁶, κ_H2 = $500 × 10³ /MWh, κ_cyc = $100 × 10³.

## Important Notes
- The cyclic boundary condition S_H2_{s,0} = S_H2_{s,24} enforces daily periodicity.
- Slack variable σ_load_{s,t} prevents infeasibility with high penalty ρ_shed.
- Hydrogen loss mloss is retained in the formulation but set to zero in the base case (λ_loss = 0).
- The annualization factor 1/L = 1/10 for L=10 years; longer horizons reduce the annualized cost burden.
- The emission extension adds ρ_CO2 · [e_grid · P_grid_buy - e_offset · P_grid_sell] to the operational objective.
