# Formulation: Multi-Level Topology + Time-Series Multi-Scenario Planning Model

## Part A — Multi-Level Network Topology Design (§2, physical level)

The physical-level design maps a data center's reliability tier to a flexible-DC supply
architecture around a 750 V DC busbar fed from 10 kV DC mains (and 10 kV diesel backup),
serving 380/220 V AC and 336/240 V DC equipment through load converters.

| Tier (GB50174 ↔ Uptime) | Architecture | Redundancy | Source |
|---|---|---|---|
| A ↔ Tier III/IV (fault-tolerant) | Dual independent 750 V DC buses (red/green), two hot-standby paths each carrying 50% | 2N or 2(N+1) UPS; critical load ≤ 90% of N | Fig 1, Table 1 |
| B ↔ Tier II (redundant) | Single supply path, second source = dual utility or utility + diesel | N+1 UPS/generator | Fig 2, Fig 3, Table 1 |
| C ↔ Tier I (basic) | Single supply path (optionally + diesel) | N (up to 100% of N per machine) | Fig 4, Fig 5, Table 1 |

Voltage-level selection drivers (§2.1): internal (economic — higher DC equipment cost but
≈1/3 footprint, ≈50% footprint reduction, ≈40% equipment saving; technical — fault
ride-through, phase/frequency-independent interconnection, 5-8% loss saving, MV-DC economic
when convergence radius > 5 km and capacity ≥ 10 MW) and external (socio-economic growth,
rising DC-load share). Reflected in evidence figures 1-5 and the reliability-tier claim C07.

## Part B — Objective Functions (§3.1)

The planning problem minimizes three objectives.

**(1) Annual economic cost — Eq. (1):**

    min f1 = C_DG + C_line + C_DG^conv + C_load^conv + C_line^conv

where the five terms are the annual investment+O&M cost of distributed generation, the cost
of line DC reconstruction/new construction, and the costs of converters at the DG
grid-connection, at the data-center load, and on the DC-system lines respectively.

**DG investment + O&M — Eq. (2):**

    min C_DG = Σ_{i=1..N_DG} α_i (C_{i,WTG} S_{i,WTG} η_{i,WTG} + C_{i,PVG} S_{i,PVG} η_{i,PVG})
             + Σ_{i=1..N_DG} Σ_{j=1..N_t} d_j Σ_{s=1..N_{s,j}} p_{s,j} Σ_{t=1..T} Δt · (D_{i,WTG} P_{ijst,WTG} + D_{i,PVG} P_{ijst,PVG})

N_DG = DG candidate nodes; α_i = fixed annual average cost coefficient; N_t = typical
time-series scenarios; d_j = days/year of scenario j; N_{s,j} = scenarios of j; p_{s,j} =
probability; T = daily time slots; Δt = slot duration; C = unit investment cost; S =
installed capacity; η = power factor; D = unit O&M cost; P = active output.

**Line DC modification — Eq. (3):**

    min C_line = Σ_{i=1..N_up} α_{l,i} x_i l_i C_l

N_up = lines to convert to DC; α_{l,i} = annual cost coefficient; C_l = per-length DC-line
cost; x_i ∈ {0,1} line-selection variable; l_i = line length.

**Grid-connected converters — Eq. (4):**

    min C_conv = Σ_{i=1..N_DG} α_c x_{i,g} Σ_{g=1..G_DG} C_conv S_{i,g} η_g
               + Σ_{i=1..N_node} α_c C_conv P_{L,i} (x_{lac,i} η_{i,ac} + x_{ldc,i} η_{i,dc})
               + Σ_{i=1..N_up} α_c x_i C_conv P_{i,conv}

α_c = annual converter cost coefficient; C_conv = per-capacity converter cost; S_{i,g} =
converter capacity; η_g = power factor; x_{i,g} ∈ {0,1} AC/DC-converter indicator.

**(2) Annual network loss — Eq. (5):**

    min f2 = Σ_{j=1..N_t} d_j Σ_{s=1..N_{s,j}} p_{s,j} Σ_{t=1..T} Δt · (P_{jst,conv} + P_{jst,line})

P_{jst,conv}, P_{jst,line} = converter and branch losses in slot t of scenario s.

**(3) Voltage stability — Eqs. (6)-(7):**

    L_ab = Σ_{j=1..N_t} (1/N_t) Σ_{s=1..N_{s,j}} p_{s,j} Σ_{t=1..T} (1/T) ·
           { a · [ (P_{b,jst} X_ab − Q_{b,jst} R_ab)^2 + (P_{b,jst} R_ab + Q_{b,jst} X_ab) U_{a,jst}^2 ] / U_{a,jst}^4 }

    min f3 = min L_VS,   L_VS = max{ L_1, L_2, ..., L_N }

R_ab, X_ab = line resistance/reactance; P,Q,U = active/reactive power and voltage at line
ends. DC branches are assigned index 0 (Eq. 6 defined for AC branches only). Source: ref [22].

## Part C — Constraints (§3.2)

**AC node power balance — Eq. (8):**

    P_i^ac = U_i^ac Σ_{j=1..N_node} U_j^ac (G_ij cosθ_ij + G_ij sinθ_ij)
    Q_i^ac = U_i^ac Σ_{j=1..N_node} U_j^ac (G_ij sinθ_ij − B_ij cosθ_ij)

**DC node power balance (data center) — Eq. (9):**

    I_i^dc − Σ_{j=1..N_dc} g_ij U_j^dc = 0
    P_i^dc = I_i^dc U_i^dc

**Voltage / branch / capacity limits — Eq. (10):**

    U_{i,min} ≤ U_i ≤ U_{i,max}
    P_ij ≤ P_{ij,max}
    0 ≤ S_{i,g} η_g ≤ P_{i,g,max}

Full boundary/assumption/limitation discussion is in constraints.md.
