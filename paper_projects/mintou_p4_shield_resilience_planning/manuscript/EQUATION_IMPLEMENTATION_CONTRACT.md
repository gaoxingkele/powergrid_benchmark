# Equation--Implementation and Benchmark Contract

This document records the p4 equation-to-code trace inspected for stage `p4_s2_equation_implementation` and used to predeclare stage `p4_s3_boundary_experiments`. Stage 2 was narrative only. Stage 3 adds a separate local immutable boundary archive; it does not change the shared planning source or replace the historical run archives.

## Controlling Artifacts and Precedence

The current benchmark is controlled by:

1. `src/powergrid_benchmark/mintou_real_planning.py` for candidate construction, p4 proxy objectives, SHIELD-MOEA, baselines, held-out scoring, normalization inputs, optimizer seeds, and compromise export;
2. `papers/mintou/mintou_p4_shield_resilience_planning/src/configs/real_simbench_planning_config.json` for experiment labels/ranges and top-level run settings;
3. `papers/mintou/mintou_p4_shield_resilience_planning/src/configs/real_shield_mechanism_controls_20260810.json` for the GA-only, DE-only, and fixed-worst-$K$ control declarations;
4. `src/powergrid_benchmark/mintou_pandapower_validation.py` and `real_ac_validation_config.json` for the downstream composition mapping and AC cases; and
5. the current main, inference, mechanism-control, sensitivity, composition, and AC CSV archives for reported results.

Stage 3 is additionally controlled by `experiments/p4_s3_boundary_predeclared.json`, `experiments/p4_boundary_experiments.py`, the frozen 18-subnet profile under `evidence/source/`, and the run/table/hash-manifest files named `p4_s3_*` under this worktree's `evidence/`. These assets are p4-only and do not alter the shared p3/p4 runner.

The older `experiment_manifest.json` and `method_manifest.csv` describe a synthetic-smoke scaffold. Their old title, datasets, baselines, ablations, and `synthetic_smoke_v0` status are not the current benchmark contract.

These source/configuration/evidence artifacts were inspected in the surrounding isolated harness repository. They are not all contained in this manuscript worktree.

## Equation-to-Code Map

| Quantity | Implemented definition or path | Manuscript scope |
|---|---|---|
| DER-output multiplier $\delta$ | Generated as scenario column 2 by `make_scenarios`; consumed only by hosting diagnostic $H=\min(1,\sum h_ix_i/\max(1,H_0\delta))`. The p4 objective vector omits $H$. | Inactive for p4 search, held-out objectives, HV, and compromise choice. `der_uncertainty` is not DER-output evidence. DER stress is active only in the separate AC cases. |
| Hosting coefficient $h_i$ | `Candidate.hosting_gain`; enters $H$, repair score $b_i$, Weighted Sum ordering, and exported hosting diagnostics. | Not a p4 objective. Its indirect effect through repair/greedy baselines must not be described as a DER-output objective effect. |
| Reliability | $R(x)=\min(1,0.35+\sum r_ix_i/28)$; broadcast across scenarios. | Scenario invariant. Its screening contribution is a constant offset across scenarios. |
| Survivability | $S(x,s)=\min(1,0.42(1-\sigma)+\sum g_ix_i/24)$. Stage 3 predeclares $S_{\gamma}(x,s)=\min(1,0.42(1-\sigma)+\gamma_g\sum g_ix_i/24)$ at $\gamma_g\in\{0.75,1,1.25\}$. | Depends on outage severity, not load or DER output. `NoResilienceObj` removes $-S$ only from environmental selection; screening still uses all five objectives. The boundary scale changes only this objective term; the fixed repair score retains $g_i/2$. |
| Loss and voltage | $L=\max(0.015,L_0\lambda-\sum l_ix_i/120)$; $U=\max(0.005,U_0\lambda-\sum u_ix_i/10)$. | Depend on load multiplier only. `restoration_aware_evaluation` uses $L^e=L[1+0.30\sigma(1-S)]$ during both search and evaluation. |
| Hard constraint | $v_B(x)=\max(0,C(x)-B)/B$. | Budget is the only feasibility gate. Raw objective dominance is applied after filtering by this gate. |
| Screening score | Population mean of the equal-weight, *unclipped* affine sum of all five single-scenario objectives plus $10v_B$. Search-problem reference bounds are used. | No advertised $\omega_q$ vector is implemented. Cost/reliability are scenario-constant; $\lambda$ and $\sigma$ drive ranking; $\delta$ is inactive. |
| Screening schedule | Generations 1, 6, 11, 16, 21, 26, 31, and 36; $K=4$ of 16; active set held fixed between updates. | Eight ranking rounds. FixedWorstK runs only the generation-1 update. |
| Call-count quantity | $40\times80\times4+8\times40\times16=17{,}920$ versus $40\times80\times16=51{,}200$. | Static objective-row arithmetic implied by the code path. No runtime call counter is implemented; no wall-clock claim follows. |
| Held-out scoring | Search scenarios use seed 20260713; evaluation scenarios use 20260714 and never enter search. Final populations are re-evaluated on the fixed evaluation matrix. | Direct scenario reuse is prevented. This does not eliminate distributional overfitting. In the unseen label, only shifted $\lambda$ and $\sigma$ affect p4. |
| Front construction | Budget-feasible unique plans are filtered and non-dominated in raw mean-objective space. | Clipped normalized dominance is not implemented. |
| HV normalization/clipping | Reference plans: empty, every singleton, and 2048 seeded random budget-feasible plans; 5% span margin. Hypervolume helper clips affine values to $[0,1]$ and uses reference point $(1.1,\ldots,1.1)$. Mean and worst bounds are separate. Stage 3 records one bounds digest per setting and recomputes the same raw fronts without clipping at $1.1^5$ and with clipping at $1.2^5$. | Method outputs do not set bounds. Search scalarization and compromise choice do not clip. All 28 stage-3 comparison directions are stable across the three HV definitions, but 441/1050 fronts require low-side clipping and gap magnitudes change. Every singleton enters the bound sample even when infeasible, producing cost bounds near $[-32195,676102]$ against budgets 754.4--1104. |
| Sampled worst envelope | Applies componentwise scenario maxima to the plans from the mean-objective front, then evaluates HV under worst-specific bounds. | Not a separately optimized or separately constructed worst-objective front and not a tail bound. |
| Compromise | Equal unweighted sum of *unclipped* affine mean objectives on the held-out mean front; `argmin` returns the first array minimum. | Only action-kind counts from seed index 0 are exported for AC mapping; candidate identities and nodal locations are discarded. |

## Candidate Generation

Subnets with positive load and at least one line are ranked by $p_j+0.2\ell_j$; the first 18 yield four actions each. With $\tau_j=p_j/\max(0.2,\ell_j)$ and $q_j=\max(0,0.55p_j-e_j)$, the code uses the following exact fields and constants:

| Action | Cost | $(l_i,u_i,h_i,r_i,g_i,d_i)$ |
|---|---|---|
| reinforcement | $60+4.5\ell_j+7p_j$ | $(0.012\ell_j+0.020\tau_j,\ 0.020+0.006\tau_j,\ 0.06q_j,\ 0.018m_j,\ 0.016m_j,\ 0.20)$ |
| storage | $50+16\sqrt{p_j+1}$ | $(0.025\sqrt{p_j+1},\ 0.018\sqrt{\tau_j+1},\ 0.12q_j+0.08p_j,\ 0.055\sqrt{n_j+1},\ 0.070\sqrt{n_j+1},\ 0.80)$ |
| DER integration | $45+10\sqrt{p_j+1}$ | $(0.018\sqrt{p_j+1},\ 0.012,\ 0.18q_j+0.10p_j,\ 0.020\sqrt{n_j+1},\ 0.028\sqrt{n_j+1},\ 1.00)$ |
| automation | $38+1.8m_j$ | $(0.006m_j,\ 0.010\sqrt{\tau_j+1},\ 0.025q_j,\ 0.085\sqrt{m_j+1},\ 0.115\sqrt{m_j+1},\ 0.35)$ |

Here $p_j$ is active load, $e_j$ renewable capacity, $\ell_j$ line length, $m_j$ line count, and $n_j$ load count. Reactive load and the extracted average-loading field do not enter these formulas.

## Variation, Repair, and Baseline Operators

- SHIELD initializes population 40 at 3--18% Bernoulli density. When enabled, repair runs after each initial plan and after every offspring batch, before environmental selection.
- Repair repeatedly removes the selected action with minimum $b_i/c_i$, where $b_i=l_i/0.12+u_i/0.02+h_i/5+r_i/2+g_i/2$.
- The GA channel uses independently sampled parent indices, uniform bitwise crossover, and mutation probability $1/n$.
- The DE-style channel uses $z=x_{r_1}+0.5(x_{r_2}-x_{r_3})$, clips $z$ to $[0,1]$, and activates a bit with probability 0.90 when $z>0.5$ and 0.08 otherwise. Donor indices are sampled with replacement, so this is not canonical distinct-index DE/rand/1.
- Plain NSGA-II uses pymoo population 40, sparse Boolean sampling, two-point crossover, bit-flip mutation, budget constraint, and all 16 search scenarios.
- NSGA-II+Repair uses that same constrained search and applies SHIELD's drop rule only to the returned population. It is not repair-timing matched to SHIELD.
- MOEA/D uses 35 Das--Dennis directions for five objectives, not population 40, with two-point crossover, bit-flip mutation, neighborhood size 10, neighbor-mating probability 0.7, and $10^4v_B$ added to every objective.
- GA returns one point after tournament selection, uniform crossover, mutation $1.5/n$, and unclipped normalized-sum fitness plus $10v_B$; its returned point is repaired post hoc.
- Weighted Sum is a deterministic greedy fill ordered by $b_i$ (without dividing by cost). Deterministic Planning is a deterministic cost-ascending greedy fill.

## Seeds and Comparison Budget

The main archive stores seed indices, not the actual optimizer seeds. For paper `p4`, label $e$, method name $m$, and index $r$,

$$
\operatorname{seed}(m,e,r)=200000+7919r+
\left(\operatorname{int}(\operatorname{SHA1}(\texttt{p4}|e|m)_{1:6},16)\bmod4096\right).
$$

Method-specific hashes make samples unpaired. Stochastic methods have 30 invocations per label. Weighted Sum and Deterministic Planning ignore the seed and therefore contribute one effective point per label despite 30 stored provenance rows.

The eight labels correspond to five active p4 proxy configurations. `deterministic_vs_scenario`, `der_uncertainty`, `scenario_screening_efficiency`, and `pareto_quality` share the reference equations/ranges as far as p4 objectives are concerned and differ through optimizer seed streams. The pooled $8\times30$ summaries therefore weight the reference configuration four times.

Stage 3 instead uses seven explicitly distinct one-at-a-time settings and five methods for 1050 new invocations. Its seed is $310000+7919r+[\operatorname{SHA1}(\texttt{run\_id}|\texttt{setting}|m)_{1:6}]_{16}\bmod4096$. Search and evaluation draws use seeds 2026081301 and 2026081302. Method names remain in the seed hash, so comparison samples are independent. The installed boundary environment uses pymoo 0.4.1 for NSGA-II+Repair; this is an operator-contract-preserving supplementary rerun, not a replacement for the main archive produced by the newer shared runner.

## Reproducibility Gaps Preserved

- The isolated manuscript worktree now contains the compact stage-3 runner, frozen profile, new run/table evidence, and manifest, but not the full historical source/configuration/evidence tree used by the main and AC archives.
- The inspected source checkout imports the hypervolume/non-dominance helper from `mintou_real_project_review`, but that helper file is absent from the checkout even though the implementation exists in repository history.
- The GA-only, DE-only, and fixed-worst-$K$ method switches exist in `ShieldConfig`/`run_shield_moea`, and archived control records/configuration exist, but a dedicated script that regenerates the 720-row control archive was not found.
- A complete executable supplementary release and persistent URL/DOI remain unresolved human tasks. These gaps limit reproducibility claims; they do not authorize changing archived numerical outcomes.
