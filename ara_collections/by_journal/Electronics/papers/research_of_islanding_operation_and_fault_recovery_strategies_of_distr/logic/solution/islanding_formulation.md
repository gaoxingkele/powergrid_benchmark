# Islanding Division and Operation Formulation (§2)

## Design principles (§2.1)
1. **Prioritize important loads** — loads are classified by importance and weighted; important
   loads are supplied first.
2. **Maximum load** — island load should match island DG supply capacity (use DG fully, avoid
   overload).
3. **Minimum network loss** — minimize island active-power loss for economic operation.

## Objective function (Eq. 1)

min Σ_{k∈Ω} Σ_{i∈N_k} Σ_{t∈T} α_{i,k}·P^s_{i,k,t} + µ_loss · Σ_{k∈Ω} Σ_{ij∈E_k} Σ_{t∈T} R_{ij}·I²_{ij,k,t}

- T = {t, t+ΔT, …, t+τ_f·ΔT} is the rolling-optimization solution window.
- First term: weighted load shedding — α_{i,k} drives important loads into islands and minimizes
  load removal (principles 1–2).
- Second term: line losses R_{ij}·I²_{ij,k,t} weighted by µ_loss (principle 3). µ_loss value: not
  specified in paper.

## Rolling optimization scheme (§2.1)
- At each scheduling period t, solve the joint model over T but issue only the next step's plan;
  when the next period arrives, repeat (feedback correction).
- ΔT = 15 min (generally); τ_f = rolling step size (value not specified in paper).
- Rationale: troubleshooting time is uncertain; short-term wind/PV prediction is more accurate than
  long-term, so a fixed look-ahead (e.g. 24 h) wastes accuracy. Rolling also improves solution
  efficiency and accuracy.

## Re-partition trigger (Eq. 2)
A new island partition is computed during period t only if, for some island k, the island-wise
absolute change versus the last partition period t1 exceeds a threshold:

- Σ_{i∈N_k} |P^L_{i,k,t} − P^L_{i,k,t1}| > σ^L, or
- Σ_{i∈N_k} |P^wind_{i,k,t} − P^wind_{i,k,t1}| > σ^wind, or
- Σ_{i∈N_k} |P^pv_{i,k,t} − P^pv_{i,k,t1}| > σ^pv.

Otherwise the period-t partition persists (avoiding frequent switching that shortens switch life
and lowers user satisfaction) and only DG dispatch is re-optimized each period. When the trigger is
not met, the switch-state and radiality constraints (Eqs. 3–12) are dropped from the rolling model.

## Constraint set
Full constraint families (Eqs. 2–34) are catalogued in [constraints.md](constraints.md):
island membership (3–5), radiality (6–12), island supply capacity (13), line-flow/voltage safety
(14–15), SOC branch flow (16–20), diesel (21–24), storage (25–34).

## Uncertainty coupling
P^DG_{i,t} for wind/PV nodes is uncertain; it enters via the scenario-weighted stochastic extension
(Eq. 48) described in [uncertainty_method.md](uncertainty_method.md).

**Source**: §2.1–§2.2, pp. 3–7.
