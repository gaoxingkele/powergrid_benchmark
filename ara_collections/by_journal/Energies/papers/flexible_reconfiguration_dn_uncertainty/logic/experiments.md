# Experiments

## Experiment E01: Four-Case Comparison of Reconfiguration Strategies on IEEE 33-Bus

| Field | Value |
|-------|-------|
| **Verifies** | C01, C03, C05 |
| **Evidence** | `evidence/tables/table04_comparison_cases_ieee33.png`, `evidence/tables/table07_hourly_loss_cost.png`, `evidence/figures/fig09_hourly_loss.png`, `evidence/figures/fig10_total_loss.png` |
| **Run** | Single run per case (deterministic for Cases 1-3, scenario-based for Case 4) |
| **Setup** | Modified IEEE 33-bus system, 12.66 kV, 3.525 MW / 2.3 MVar load, 37 branches (32 sectional + 5 tie-line). COA parameters: population size not specified, itermax not specified. MATLAB R2016b on Intel Core i3 1.9 GHz, 4 GB RAM. |
| **Procedure** | (1) Define four cases: initial config (Case 1), static reconfig no DG (Case 2), static reconfig with nominal DG (Case 3), dynamic reconfig with uncertainty (Case 4). (2) For Case 4, generate scenario probabilities for load, wind, and PV at each of 24 hours. (3) Initialize COA population with random switch configurations. (4) For each iteration, run power flow, evaluate objective function (Equation 20) with constraints (29)-(37), apply COA update phases (hunting and escape), and retain best solution. (5) Repeat until itermax. (6) Record open switches, total cost, and cost components for each case. |
| **Expected outcome** | Case 4 (dynamic reconfiguration) should achieve the lowest total operational cost. Case 4 should show lower power losses and upstream power purchases than Cases 1-3. Case 4 may incur higher switching costs than static cases due to multiple hourly transitions. |

### Results
- Case 1: Cost = USD 2799.20, Open switches S33-S37, No switching cost
- Case 2: Cost = USD 2635.45, Open switches S7,S9,S14,S32,S37, Switching cost USD 8
- Case 3: Cost = USD 2649.57, Open switches S7,S10,S14,S30,S37, Switching cost USD 8
- Case 4: Cost = USD 2626.39, Two configurations (1-14h: S6,S9,S34,S36,S37; 15-24h: S7,S9,S14,S32,S37), Switching cost USD 10
- Power loss reduction in Case 4: 26.31% vs Case 1, 2.14% vs Case 2, 4.66% vs Case 3

---

## Experiment E02: COA vs PSO Performance Comparison

| Field | Value |
|-------|-------|
| **Verifies** | C02 |
| **Evidence** | `evidence/tables/table08_coa_vs_pso.png`, `evidence/figures/fig13_coa_pso_voltage.png` |
| **Run** | Single comparative run |
| **Setup** | IEEE 33-bus system with same uncertainty modeling, same objective function, same constraints. Both algorithms run on MATLAB R2016b with same computational budget. |
| **Procedure** | (1) Implement both COA and PSO for the DR problem. (2) Configure both algorithms with the same population size and iteration count. (3) Run both algorithms under identical problem data (load, wind, PV scenarios, prices). (4) Record the best solution found by each algorithm in terms of total cost and cost components. (5) Compare the minimum bus voltage profiles throughout the 24-hour period. |
| **Expected outcome** | COA is expected to achieve lower total cost than PSO. COA should particularly demonstrate advantages in switching cost optimization (fewer unnecessary switch operations) and power loss minimization. Minimum bus voltage profiles should be similar between both algorithms. |

### Results
- COA total cost: USD 2626.39 (Closs: 466.73, CVD: 0.279, CSW: 10, Cupn: 1857.53, CPV: 60.518, CWind: 231.32)
- PSO total cost: USD 2634.58 (Closs: 466.85, CVD: 0.261, CSW: 18, Cupn: 1857.63, CPV: 60.518, CWind: 231.32)
- COA switching configurations: 1-14h (S6,S9,S34,S36,S37), 15-24h (S7,S9,S14,S32,S37)
- PSO switching configurations: 1-4h (S7,S11,S28,S34,S36), 5-11h (S7,S9,S28,S34,S36), 13-17h (S7,S11,S28,S34,S36), 18-24h (S7,S9,S14,S32,S37)
- COA uses 2 configurations per 24h; PSO uses 4 configurations per 24h

---

## Experiment E03: Reliability Impact Assessment via EENS

| Field | Value |
|-------|-------|
| **Verifies** | C04 |
| **Evidence** | `evidence/tables/table09_eens_values.png`, `evidence/figures/fig14_eens_variation.png` |
| **Run** | Single analytical evaluation using Equations (46)-(47) |
| **Setup** | IEEE 33-bus system. Branch failure rates and durations from reference [34]. Same load profile and DG placement for all cases. |
| **Procedure** | (1) For each of the four cases, determine the network topology. (2) For each branch, compute the contribution to EENS using its failure rate (lambda_j), average failure duration (r_j), and the load at buses affected by the branch outage (nb(i)). (3) Aggregate EENS across all branches for each hour. (4) Compute average and total EENS over the 24-hour period for each case. |
| **Expected outcome** | Case 4 (dynamic reconfiguration) should achieve the lowest average and total EENS. Static reconfiguration without DG (Case 2) should improve over baseline (Case 1). Case 3 (static with DG) may show higher EENS due to topology that does not account for time-varying conditions. |

### Results
- Average EENS: Case 1: 0.6192, Case 2: 0.5106, Case 3: 0.6245, Case 4: 0.5037 MWh/year
- Total EENS: Case 1: 14.8602, Case 2: 12.2543, Case 3: 14.9887, Case 4: 12.0879 MWh/year
- Case 4 improves EENS by 18.7% vs Case 1, 1.4% vs Case 2, and 19.4% vs Case 3

---

## Experiment E04: Validation on TPC 83-Bus Real System

| Field | Value |
|-------|-------|
| **Verifies** | C01, C05 |
| **Evidence** | `evidence/tables/table12_comparison_tpc83.png`, `evidence/figures/fig16_total_loss_tpc83.png` |
| **Run** | Single run per case |
| **Setup** | Taiwan Power Company (TPC) 83-bus distribution network, 11.4 kV, 28.35 MW / 20.7 MVar load, 96 branches (83 sectional + 13 tie-line). Same uncertainty modeling, load profile, and price data as IEEE 33-bus case. |
| **Procedure** | (1) Adapt the four-case framework to the TPC 83-bus system. (2) Place renewable DGs as specified in Table 10 (4 PV units at 500 kW each, 4 wind units at 500 kW each). (3) Run COA for each case with the same parameter settings as the IEEE 33-bus experiment. (4) Record open switches, total cost, and cost components. |
| **Expected outcome** | Case 4 should achieve the lowest total cost on the TPC 83-bus system, confirming scalability of the proposed DR method. The cost reduction magnitude may differ from the IEEE 33-bus case due to system size and topology differences. |

### Results
- Case 1: Cost = USD 18,751.93, Loss = 2223.8, Cupn = 15,861.9
- Case 2: Cost = USD 18,455.35, Loss = 1936.6, Cupn = 15,835.1
- Case 3: Cost = USD 18,574.61, Loss = 2054.5, Cupn = 15,846.1
- Case 4: Cost = USD 18,378.23, Loss = 1866.1, Cupn = 15,825.3
- Power loss reduction in Case 4: 16.08% vs Case 1, 3.64% vs Case 2, 9.17% vs Case 3
- Case 4 configurations: 1-19h (S7,S34,S39,S41,S55,S62,S72,S83,S86,S88,S89,S90,S92); 20-24h (S7,S14,S34,S39,S42,S55,S62,S72,S83,S86,S88,S90,S92)
