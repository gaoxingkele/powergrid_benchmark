# Concepts

## Dynamic Line Rating (DLR)
- **Notation**: Imax, Pmax(Ta)
- **Definition**: A transmission-line rating that adaptively adjusts allowable line capacity from
  real-time meteorological conditions (ambient temperature, wind speed, solar irradiance) via the
  conductor thermal-balance equations, rather than from fixed worst-case assumptions. The maximum
  allowable current is Imax = sqrt[(-β1 + sqrt(β1^2 - 4β2(β0 - θmax)))/(2β2)] (Eq. 10), giving a
  temperature-dependent capacity limit Pmax(Ta).
- **Boundary conditions**: Assumes constant wind speed and solar irradiance over the period and the
  steady-state conductor temperature governing (long time scale, Eq. 9); parameters β0, β1, β2 vary
  with conductor physical/electrical properties and weather.
- **Related concepts**: Static Line Rating, Thermal Balance of Transmission Lines, Steady-State
  Conductor Temperature

## Static Line Rating (SLR)
- **Notation**: —
- **Definition**: Conventional line rating that fixes capacity from worst-case meteorological
  conditions to ensure secure operation, independent of real-time weather.
- **Boundary conditions**: Conservative by construction; reduces usable transfer capability and does
  not track actual heat-limited ampacity under extreme temperature.
- **Related concepts**: Dynamic Line Rating

## Thermal Balance of Transmission Lines
- **Notation**: Qc, hr, Qs, θss
- **Definition**: The steady-state energy balance in which conductor resistive (Joule) heating is
  offset by convective heat loss Qc = hcAs(Tc - Ta) (Eq. 1), radiative heat loss via hr (Eq. 3), and
  solar heat gain Qs = αs G As (Eq. 4). Steady-state conductor temperature θss = β0 + β1·I^2 + β2·I^4
  (Eq. 8), decomposed into ambient/solar rise, resistive rise, and a higher-order radiative
  correction.
- **Boundary conditions**: Steady-state (thermal-inertia term exp(-t/τ) neglected for long time
  scales); empirical convective/radiative coefficients from cited models.
- **Related concepts**: Dynamic Line Rating, Steady-State Conductor Temperature

## Hot-Spot Temperature
- **Notation**: TH (also Tu, ultimate hot-spot)
- **Definition**: The temperature at the hottest spot within the transformer winding, equal to
  ambient temperature plus top-oil temperature rise over ambient plus hot-spot rise over top-oil:
  TH = Ta + ∆TM + ∆Tu (Eq. 17), with ∆TM (Eq. 18) driven by load factor KL and ∆Tu = FT·θQC·KL^{2m}
  (Eq. 19). It is the dominant driver of insulation thermal aging.
- **Boundary conditions**: Cooling-method-dependent exponents n, m and factor FT; here OA/ONAN with
  FT = 1.4, n = 0.9, m = 0.8, θQC = 22 C; rated top-oil rise 56.3 C gives 98 C hot-spot at 20 C
  ambient.
- **Related concepts**: Top-Oil Temperature, Transformer Life Loss Cost, Load Factor

## Top-Oil Temperature
- **Notation**: TM, ∆TM, ∆θTM-R
- **Definition**: Temperature of the transformer oil near the hot spot, reflecting internal winding
  heat distribution; TM = 1.2 θa + ∆τTM (Eq. 13). Its rise over ambient at rated load ∆θTM-R feeds
  the hot-spot model. Driven by no-load loss (Eq. 11) and load loss (Eq. 12).
- **Boundary conditions**: Empirical regression constants (0.8, 3.5, 0.7) fit from experimental
  data; Ka ∈ [0.05, 0.15], Kh ∈ [0.5, 0.9].
- **Related concepts**: Hot-Spot Temperature, No-Load Loss, Load Loss

## Transformer Life Loss Cost
- **Notation**: CTF, Di
- **Definition**: Monetized insulation aging over the horizon, CTF = Cint · Σ (Di/Dt)·(ti/TL)
  (Eq. 20), where the per-condition loss-of-life rate Di = exp(KA/383 - KA/(TH+273))·100% (Eq. 21)
  follows Arrhenius kinetics in hot-spot temperature and is accumulated linearly (Miner's rule /
  IEEE-ANSI C57.91).
- **Boundary conditions**: 98 C hot-spot = rated life; +6 C doubles aging; nominal life 30 years;
  scaled by transformer initial investment cost Cint.
- **Related concepts**: Hot-Spot Temperature, Linear Damage Accumulation, Arrhenius Reaction Rate

## Generation Shift Distribution Factor (GSDF)
- **Notation**: Gl,j, Gl,n
- **Definition**: DC-power-flow sensitivity factors mapping generator outputs and nodal loads to
  line flows, LFl,t = Σ Gl,j·Pgen_j,t - Σ Gl,n·Pload_n,t (Eq. 28), used to linearize power-flow
  distribution inside the UC optimization.
- **Boundary conditions**: DC power flow assumption (lossless, linear); network topology fixed.
- **Related concepts**: Interface Constraint, Temperature-Dependent Capacity Constraint

## Linear Damage Accumulation (Miner's Rule)
- **Notation**: Σ (Di/Dt)·(ti/TL)
- **Definition**: The assumption that fractional insulation life consumed under successive operating
  conditions adds linearly, so total life loss is the weighted sum of per-condition loss-of-life
  rates over their durations — the basis for the transformer life-loss cost function.
- **Boundary conditions**: Assumes independent, additive damage; per IEEE/ANSI C57.91 and miner's
  rule (ref [22]).
- **Related concepts**: Transformer Life Loss Cost, Arrhenius Reaction Rate
