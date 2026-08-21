# Fault Recovery Formulation (§3)

Applies once the main network resumes power supply: outage loads are reconnected through
distribution lines, with network reconstruction, while island-stage history shapes priorities.

## Objective function (Eq. 35, weighted form after [26])

max F = Σ_{i∈N} Σ_{t∈T} β_i·w_i·P^H_{i,t}
        − ϑ_loss · Σ_{ij∈E} Σ_{t∈T} R_{ij}·I²_{ij,t}
        − ϑ_switch · [ Σ_{d∈ξ} (1 − z_d) + Σ_{d∈ζ} z_d ]

- Term 1: maximize restored load power P^H_{i,t}, weighted by the recovery-stage load weight β_i;
  w_i ∈ {0,1} marks whether node i's load is restored.
- Term 2: minimize post-recovery network losses (weight ϑ_loss).
- Term 3: minimize switching actions — ξ is the set of segmented (sectionalizing) switches
  (deviation from closed, z_d = 1 closed), ζ the set of contact (tie) switches (deviation from
  open). Weight ϑ_switch.
- ϑ_loss, ϑ_switch values: not specified in paper.
- Goal ordering stated in §3.1: load recovery first, then losses, then switching count.

## Stage-coupling load weight (Eq. 36) — the paper's key design

β_{i,k} = α_{i,k}
        + ξ1 · Σ_{t∈TIS} |y_{i,k,t} − y_{i,k,t−1}|
        + ξ2 · Σ_{t∈TIS} |y_{i,k,t} − 1|        ∀i ∈ N

- α_{i,k}: static island-stage importance weight (Table 2: 100/10/1).
- Second term: each change of node i's supply status between adjacent island-stage scheduling
  periods contributes 1 — penalizes island-scheme churn experienced by the load.
- Third term: each island-stage period with no supply (y_{i,k,t} = 0) contributes 1 — penalizes
  accumulated outage time.
- ξ1, ξ2: positive constants (values not specified in paper). TIS = the scheduling periods the
  island operation actually spanned.
- Effect: loads that endured intermittent or no supply during islanding get elevated recovery
  priority, protecting user electricity satisfaction. Setting β = α (comparison method, §5.3.4)
  removes the coupling and leaves such nodes unpowered (Figure 20 vs Figure 16; claim C05).

## Rolling scheme
Recovery also runs as rolling optimization with ΔT = 15 min; adjacent-period strategies are
connected and coordinated; the period-t plan solves the joint model over
T = {t, t+ΔT, …, t+τ_f·ΔT}.

## Constraints (§3.2)
- Radiality: Eqs. (6), (7), (10)–(12) still apply; Eqs. (8)–(9) are replaced by ϕ_{ij,t} ≥ 0 ∀i ∈ N
  (Eq. 37) since the main grid now participates.
- Safety and SOC branch flow: Eqs. (14)–(20).
- DG operating constraints: Eqs. (21)–(34).
- No de-restoration: w_i = 1 ∀i ∈ N_k, k ∈ Ω (Eq. 38) — loads supplied during islanding must stay
  supplied through recovery.
- Main-grid exchange capacity: Eq. (39) on tie lines E_S.
- Wind/PV uncertainty: handled by the scenario-weighted extension (Eq. 48) —
  see [uncertainty_method.md](uncertainty_method.md).

**Source**: §3.1–§3.2, pp. 7–9.
