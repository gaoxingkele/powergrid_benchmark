# Formulation — UC Objective with DLR and Transformer Life-Loss Constraints

All equation numbers refer to the published paper. Symbols follow the paper's Nomenclature.

## 1. Objective function (Eq. 22, §4.1)

Minimize total operating cost over the 24 h horizon (T periods, N thermal units):

```
min F = Ccoal + CTF + CW + CUD

Ccoal = Σ_{t=1..T} Σ_{i=1..N} ( a_i · P_{i,t}^2 + b_i · P_{i,t} + c_i )       (thermal generation cost)
CTF   = Cint · Σ_{i=1..N} ( D_i(TH) / D_t · t_i / T_L )                       (transformer life-loss cost)
CW    = γ_wind · Σ_{t=1..T} Q_wind,t                                          (wind-curtailment penalty)
CUD   = start-up/shutdown cost of thermal units
```

- a_i, b_i, c_i: unit consumption coefficients (Table 1).
- D_i(TH): per-condition transformer loss-of-life rate (Eq. 21).
- γ_wind: wind-curtailment penalty coefficient, base case 500 CNY/(MW·h).
- Q_wind,t: wind curtailment amount at time t.

## 2. Dynamic line rating sub-model (§2, Eqs. 1-10)

Thermal-balance components:
- Convective heat loss: `Qc = hc · As · (Tc - Ta)`  (Eq. 1); hc from Eq. 2 (max of two empirical forms).
- Radiative coefficient: `hr = 4 ε σ As (Ta + 273)^3`  (Eq. 3).
- Solar heat gain: `Qs = αs · G · As`  (Eq. 4).
- Ambient/solar rise: `T0 = β0 = Ta + µ0 Qs`, `µ0 = [π D (hr + hc)]^{-1}`  (Eq. 5).
- Resistive rise: `T1 = β1 · I^2`, `β1 = µ0 r^{tem}`  (Eq. 6).
- Higher-order radiative correction: `T2 = β2 · I^4`,
  `β2 = µ0 µ1 r^{max}(η r^{ref} - κ)`, `µ1 = [π D (hr + hc + κ(Tmax - Tamb))]^{-1}`  (Eq. 7).

Steady-state conductor temperature (Eq. 8):
```
θss = T0 + T1 + T2 = β0 + β1·I^2 + β2·I^4
```
Transient form (Eq. 9): `θ(t) = θss - (θss - θ0)·exp(-t/τ)`; for long time scales θ(t) ≈ θss.

Maximum allowable current given a steady-state temperature limit θmax (Eq. 10):
```
Imax = sqrt[ ( -β1 + sqrt( β1^2 - 4 β2 (β0 - θmax) ) ) / (2 β2) ]
```
Combined with system voltage, this yields the temperature-dependent capacity limit Pmax(Ta).

## 3. Transformer hot-spot & life-loss sub-model (§3, Eqs. 11-21)

Losses: no-load `P0 = S0 · wir · ES` (Eq. 11, ES ∈ [1.3, 1.5]); load loss
`PL = ΣPc + ΣPs + ΣPw + Pm` (Eq. 12).

Top-oil temperature: `TM = 1.2 θa + ∆τTM` (Eq. 13), with
`θa = Ka · qh^{0.8}` (Eq. 14) and `∆τTM = 0.028 e^{3.5 Kh} θa^{0.7}` (Eq. 15);
winding-over-oil rise `θQC = τqc + θa` (Eq. 16).

Ultimate hot-spot temperature (Eq. 17):
```
TH = Ta + ∆TM + ∆Tu
∆TM = ∆θTM-R · ( (1 + RH·KL^2) / (1 + RH) )^n         (Eq. 18)
∆Tu = FT · θQC · KL^{2m}                               (Eq. 19)
```
Life-loss cost (Eq. 20) and per-condition loss rate (Eq. 21):
```
CTF = Cint · Σ_{i=1..n} ( D_i / D_t · t_i / T_L )
D_i = exp( KA/383 - KA/(TH + 273) ) · 100%
```
Parameter settings (§3.2): OA/ONAN cooling → FT = 1.4, n = 0.9, m = 0.8; θQC = 22 C;
∆θTM-R = 56.3 C gives TH = 98 C at 20 C reference ambient; 98 C = rated life, +6 C doubles aging;
nominal life 30 years.

## 4. Operational constraints (§4.2, Eqs. 23-31)

1. Wind decomposition (Eq. 23): `0 ≤ P_w,t^act ≤ P̂wind_w,t`, `0 ≤ P_w,t^abn ≤ P̂wind_w,t`,
   `P_w,t^act + P_w,t^abn = P̂wind_w,t`.
2. Power balance (Eq. 24): `Σ_i u_{i,t} P_{i,t}^th + Σ_{w=1..2} P_{w,t}^act = D_t`  ∀t.
3. Generation limits (Eq. 25): `u_{i,t} P_i^min ≤ P_{i,t}^th ≤ u_{i,t} P_i^max`.
4. Ramp limits (Eq. 26): up/down ramp bounded by R_i, R_i^on (start-up), R_i^off (shutdown).
5. Spinning reserve (Eq. 27): positive/negative reserve ≥ α·D_t with α = 0.02 (per GB/T 38969-2020).
6. Line flow via GSDF (Eq. 28): `LFl,t = Σ_j Gl,j P_{j,t}^gen - Σ_n Gl,n P_{n,t}^load`.
7. Interface constraints (Eqs. 29-30): `Scr_{k,t} = Σ_{l∈TFk} ±LFl,t`, `-Smax_k ≤ Scr_{k,t} ≤ Smax_k`.
8. **Temperature-dependent transmission capacity constraint (Eq. 31)** — the DLR coupling:
   ```
   -Pmax_{i,t}( Imax_{i,t}(Ta) ) ≤ P_{i,t}^line ≤ Pmax_{i,t}( Imax_{i,t}(Ta) )
   ```
   where the line's capacity limit is a function of ambient temperature through the DLR sub-model.

## Model class
Mixed-integer program (binary commitment u_{i,t}, quadratic generation cost, DC-power-flow linear
network constraints, temperature-dependent capacity bound), solved with Gurobi 12.0.1.
