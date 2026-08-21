# Method — Self-Unit Commitment (SEUC) for a CCGT Plant

## Pipeline overview

The method constructs a single-plant self-unit-commitment MILP that, given an ISO dispatch instruction and plant initial conditions, produces an hourly commitment and dispatch plan respecting real operational constraints.

1. **Hybrid component+mode model design.** Rather than using a pure aggregate/mode representation (which loses per-unit detail) or a pure component model (which may lack configuration-level couplings), the model represents each gas turbine (GT) and each steam turbine (ST) individually while embedding configuration-style coupling constraints via minimum-unit-count and output-ratio relations (Eqs. 7–10). This is the paper's distinguishing design choice.

2. **Plant topology.** A 5 × 2 CCGT configuration (Figure 3): 5 gas turbines each feeding a Heat Recovery Steam Generator (HRSG); the HRSGs supply a common steam header that feeds 2 steam turbines. Supplementary fire can be added at each HRSG to boost steam output independently of gas-turbine exhaust.

3. **Startup state machine (Figure 2).** Steam-turbine startups are classified as hot/warm/cold based on offline duration thresholds (Figure 2):
   - Hot: offline ≤ 16 h → shortest startup ramp (4 energy blocks, Table 2)
   - Warm: 16 < offline ≤ 30 h → intermediate ramp (5 blocks)
   - Cold: offline > 30 h → longest ramp (6 blocks)
   
   Each thermal state prescribes a specific block-sequence ramp that the steam turbine must follow (Table 2), modelled via energy-block variables (Eqs. 19–32).

4. **Minimum gas-hours gating (novel constraint 1).** Before a steam turbine may start, the gas-turbine group must have accumulated a minimum number of online hours:
   - For a cold steam start: ≥ KGC = 3 h of gas-turbine operation
   - The hot-start window closes after 9 h offline (KMH); beyond this, a cold start is forced
   - At least MUG = 2 gas turbines must be simultaneously online
   
   These are encoded in Eqs. (33)–(37) via temporal logic variables.

5. **Load-distribution penalty (novel constraint 2).** The objective includes a term DSC · Σ_{i<k} d_{i,k,t} where d_{i,k,t} is the absolute output difference between gas turbines i and k, active only when both are above technical minimum (Eqs. 41–46). This drives even loading, argued to reduce steam-rotor thermal stress.

6. **Supplementary firing and steam waste.** Steam-turbine output is linked to gas-turbine heat via the STF, with supplementary firing (PAF = 15 MW cap) providing an independent boost (Eqs. 14–15). Steam waste (σ_t) allows the model to vent excess steam when gas-turbine heat input exceeds what the steam turbines can use (Eq. 16).

7. **Case-study design.**
   - **Case I (Hot start, Table 5):** Initial state has GT1, GT5, and ST1 already online at t=0, with other units offline for varying durations. Demonstrates adding units to meet a rising dispatch.
   - **Case II (Warm start, Table 6):** All units initially offline; GT2, GT3, GT4 lead the startup. ST1 has a warm startup; ST2 requires a cold startup (→ KGC = 3 h gating). Demonstrates full-plant cold commissioning.

8. **Penalty quantification.** The heuristic model (which omits the real constraints) produces a dispatch differing from the SEUC output. Under Colombian market rule [25], deviations exceeding 5% are penalised at the PCC price. The daily penalty is computed as:
   - Case I: USD 60,957/day
   - Case II: USD 66,093/day

## Model class
Mixed-integer linear program (MILP) with binary commitment and startup variables, continuous output and difference variables. The paper does not specify the solver used or report solution times.

## Data flow
```
ISO dispatch            Plant initial conditions          Plant parameters
    │                         │                                │
    v                         v                                v
    ┌─────────────────────────────────────────────────────────────┐
    │  SEUC MILP (Eqs. 1–46)                                     │
    │  ┌───────────────────────────────────────────────────────┐  │
    │  │ Objective (Eq. 1): no-load + start-up + shut-down +  │  │
    │  │   load-distribution penalty (DSC, Eqs. 41–46)        │  │
    │  │                                                       │  │
    │  │ Constraints:                                          │  │
    │  │   • Power balance & plant limits (Eqs. 2–4)          │  │
    │  │   • Gas-turbine limits & ramps (Eqs. 5–6)            │  │
    │  │   • Gas–ST unit-count coupling (Eqs. 7–10)           │  │
    │  │   • ST output w/ supp. fire & waste (Eqs. 11–17)     │  │
    │  │   • Startup ramp blocks by thermal state (Eqs. 19–32)│  │
    │  │   • Min gas-hours gating (Eqs. 33–37) ← NOVEL       │  │
    │  │   • Min up/down time & sequencing (Eqs. 38–40)       │  │
    │  └───────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
                                │
                                v
            Hourly commitment + dispatch (per-unit)
            • GT1–GT5: on/off, g_{i,t} (MW)
            • ST1–ST2: on/off, s_{j,t} (MW)
            • Supplementary fires: f_{j,t} (MW)
            • Steam waste: σ_t (MW)
            • Plant output: P^plant_t (MW)
            • Load-distribution differences: d_{i,k,t}
```
