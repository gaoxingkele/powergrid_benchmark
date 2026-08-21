# Formulation — Bi-level Low-Carbon Economic Dispatch of IES

All equation numbers refer to the source paper. Notation follows the paper's Nomenclature (pages 22–24).

## Flexibility quantification (§2)

**Flexibility demand** (from net-load fluctuation), Eq. (1):
- P_u^t = max(P_NL^{t+1} − P_NL^t, 0)   (upward demand)
- P_d^t = −min(P_NL^{t+1} − P_NL^t, 0)  (downward demand)

**Flexibility supply margins**:
- Energy-conversion equipment, Eq. (2): S_u^t = Σ_j min(P^max − P^t, R^up); S_d^t = Σ_j min(P^t − P^min, R^down)
- Energy storage, Eq. (3): S_u^{S,t} = min(η_chr(S_BT^t − S^min), P_chr^max); S_d^{S,t} = min(η_dis(S^max − S_BT^t), P_dis^max)
- Load demand response, Eq. (4): S_u^{L,t} = (P_cut^{t.max} − P_cut^t) + (P_out^{t.max} − P_out^t); S_d^{L,t} = P_in^{t.max} − P_in^t
- EV clusters, Eq. (18): S_u^{EV,t} = N·ρ_i min(η_{EV.i.chr}(S_{EV.i}^t − S_{EV.i}^min), p_{e.EV.i.chr}^max); S_d^{EV,t} = N·ρ_i min(η_{EV.i.dis}(S_{EV.i}^max − S_{EV.i}^t), p_{e.EV.i.dis}^max)
- Total supply, Eq. (5): F_u^t = S_u^t + S_u^{S,t} + S_u^{L,t}; F_d^t = S_d^t + S_d^{S,t} + S_d^{L,t}

**Flexibility evaluation indicator** (per carrier c ∈ {e,h,q}), Eq. (6):
- F_c = (F_u^c + F_d^c) / (2 P_L^c)  — average of up+down supply normalized by supplied power; larger = more flexible.

## Upper-level model — IES operator (§3.1)

**Economic objective**, Eq. (7):
max F1 = F_s.yh + F_s.EV + F_gri − F_pe − F_em − F_GCT − F_CET

Term expressions, Eq. (8):
- F_pe = Σ_t (α_g^t P_g^t + α_e^t P_e^t)   — energy purchase (gas + electricity)
- F_em = Σ_i Σ_t C_i P_j^t                 — equipment O&M
- F_GCT = λ_GCT (Q_gs − Q_gd)              — green-certificate cost
- F_CET = λ_CET (E_O − E_C)                — carbon-trading cost
- F_gri = Σ_t α_se^t P_se^t                — sell to grid
- F_s.yh = Σ_t α_{i.se}^t · P_{i.load}^t    — sell energy to aggregators
- F_s.EV = Σ_t (α_EV^t · (P_{e.EV.chr}^t − P_{e.EV.dis}^t))  — sell electricity to EVs

Green-certificate quotas, Eq. (9): Q_gs = α_GCT Σ_t P_load^t; Q_gd = κ_GCT Σ_t P_ge^t.
Carbon-emission quotas, Eq. (10): E_O = σ1 Σ_t P_grid^t + σ2 Σ_t P_GT.g^t; E_C = σ3 Σ_t P_grid^t + σ4 Σ_t P_GT.g^t.

**Flexibility objective**, Eq. (11):
max F2 = ω_e F_e + ω_h F_h + ω_q F_q, with ω_e,ω_h,ω_q ∈ (0,1), ω_e+ω_h+ω_q = 1. (Concrete weights: Not specified in paper.)

Decision variables (upper): outputs of the various devices in the system (Figure 1).

## Lower-level model (§3.2)

**EV cluster aggregation**, Eq. (17): P_{e.EV.chr}^t = N_EV Σ_{i∈N_EV^i} ρ_i p_{e.EV.i.chr}^t (and analogously for discharge).

**EV objective (max self-utility)**, Eq. (19):
max F_EV = Σ_i ρ_i Σ_t (ω_EV^t·(η_{EV.chr} p_{e.EV.chr}^t − p_{e.EV.dis}^t/η_{EV.dis}) − α_EV^t(p_{e.EV.chr}^t − p_{e.EV.dis}^t))

**User-aggregator objective (min cost)**, Eq. (21)–(22):
min F^L = F_buy + F_com, with
- F_buy = Σ_t (α_{i.se}^t · P_{i.load}^t)
- F_com = Σ_t (C_tran·P_{i.tran}^t + C_cut·P_{i.cut}^t + C_re·P_{i.re}^t)

Decision variables (lower): power purchased by users; EV charge/discharge power (Figure 1).

## Constraints (see constraints.md for the full list)
Upper level: electric/thermal/cooling power balance Eq. (12)–(14); renewable output bounds Eq. (15); device output + ramping bounds Eq. (16).
Lower level: EV SoC dynamics + charge/discharge bounds Eq. (20); translatable-load bounds Eq. (23); reducible-load bound Eq. (24); substitutable-load bound Eq. (25).

## Coupling (§3.3)
Upper → lower: energy prices (α_{i.se}, α_EV). Lower → upper: purchased energy quantities and EV charge/discharge + SoC. Iterated between levels until convergence; TOPSIS selects a compromise from the resulting Pareto front, using operator profit (F1) and the flexibility index (F2) as the two criteria.

## Notes / source ambiguities
- Eq. (25) as printed is textually identical to Eq. (24) (both "P_{i.cut}^t ≤ k3 P_{i.pri}^t") though its surrounding text describes a *substitutable*-load / load-conversion constraint with a conversion ratio φ and variable P_ij^t. This appears to be a typesetting error in the source; transcribed verbatim and flagged. Recorded in constraints.md.
