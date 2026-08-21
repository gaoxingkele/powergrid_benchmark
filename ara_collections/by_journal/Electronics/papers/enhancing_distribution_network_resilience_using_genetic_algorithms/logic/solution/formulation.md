# Formulation — Resilience-Aware Multi-Objective Optimization

Source: §5 "Objective Function", p.9. The paper states the equations inline and does **not** assign
numbered equation labels; they are referenced here by §5 / page 9.

## Decision (control) variables
The GA determines the optimal configuration of control variables (§5, p.8–9):
- Reactive power injections of DER units (Q_DER,i), buses 2, 3, 4
- Real power injections of DER units (P_DER,i), buses 2, 3, 4
- Tap settings of voltage regulators
- Reconfiguration actions admissible within a radial structure

## Objective function
Minimize the scalarized weighted sum (§5, p.9):

    F = w1·f1 + w2·f2 + w3·f3

where:
- **f1 — voltage profile improvement**:  f1 = Σ_{i=1}^{6} |V_i − 1_pi|²
  (sum over all 6 buses of squared voltage deviation from nominal 1 pu)
- **f2 — power loss minimization**:  f2 = Σ_{k=1}^{5} I_k²·R_k
  (sum over the 5 lines of resistive loss; I_k = current of line k, R_k = resistance of line k)
- **f3 — resilience penalty**: "introduced by penalizing configurations that lead to voltage collapse
  or overloads during DER faults." The paper gives f3 as a penalty in words; its explicit functional
  form is **Not specified in paper**.
- **Weights**: (w1, w2, w3) = (0.4, 0.4, 0.2).

## Constraints (§5, p.9)
- **Voltage limits**:  0.95 ≤ V_i ≤ 1.05  (per unit, all buses)
- **Line thermal limits**: line currents bounded by the branch thermal capacity (Table 1: I_max =
  200 A for all lines L1–L5)
- **DER limits**:  0 ≤ P_DER,i ≤ P_max,i  and  |Q_DER,i| ≤ Q_max,i  (inverter apparent-power /
  capacity limits)
- **Radiality**: reconfiguration actions must preserve the radial network structure (§5, p.8).

## Notes on the fitness the GA actually used
The results section restates the operational fitness as "a weighted sum of the total power loss and a
penalty for voltage deviations outside the 0.95–1.05 pu range" (§5, p.9) — i.e. the loss term plus a
voltage/constraint penalty. This is consistent with F above, with the voltage term and constraint
handling folded into the penalty structure.

## Reflected structure
- The objective/constraint set drives `logic/solution/algorithm.md` (fitness evaluation) and
  `src/configs/ga_optimization.md` (weights and GA hyperparameters).
- The resilience penalty f3 is the paper's novel term linking steady-state optimization to the
  contingency assessment reported in Table 6 (see claim C04).
