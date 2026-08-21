# Taxonomy of Energy Storage Economics, Forecasting, and Hybrid Control

The review's organizing taxonomy across its three pillars. Structured description synthesized from
§2–§5 and Tables 1–9. This is a classificatory framework, not an experiment.

## Pillar A — Energy Storage Technologies and Architecture (§2)

### A.1 Storage technologies (Table 1)
| Technology | Energy density | Response time | Lifespan | Role |
|---|---|---|---|---|
| Lithium-ion | High | < 1 s | 10–15 years | Peak shaving, energy shifting |
| Flow batteries (e.g. vanadium redox) | Low | Seconds | 10,000–20,000 cycles | Long-duration storage; decoupled power/energy sizing |
| Lead–acid | Low | Seconds | 5–15 years | Low-cost backup / off-grid |
| Supercapacitors | Very low | Milliseconds | Up to 1,000,000 cycles | Fast frequency support, transient buffering, synthetic inertia |
| Pumped hydro | Low | 15–30 s | 50–100 years | Bulk energy storage |
| Flywheels | Low | Seconds | Up to hundreds of thousands of cycles | Fast frequency support |
| Compressed air (CAES) | Low | Minutes | 20–40 years | Long-duration/bulk (40–70% round-trip efficiency) |
| Hydrogen / fuel cells | High | Seconds–minutes | ~10,000 operating hours | Long-term chemical storage |
| Thermal storage | Variable | Minutes | ~15 years | Heating/cooling load shifting |

Design axis: high-energy/moderate-response media for energy shifting/peak shaving; high-power/ultra-fast media for frequency/voltage support and intermittency mitigation. Suitability differs for AC microgrids vs utility-scale (C07).

### A.2 Integration topologies (§2.2, Table 2)
- **AC-coupled** (Figure 4): separate inverters onto common AC bus; modular, retrofit-friendly; multiple conversion stages → higher losses.
- **DC-coupled** (Figure 5): shared DC bus via DC–DC converters, single grid inverter; fewer stages, direct PV-to-battery charging, ~3% higher efficiency; more control/protection complexity.
- **Hybrid / HESS** (Figure 6): batteries (energy balancing) + supercapacitors (transient buffering) on a DC bus; multi-scale response, reduced degradation stress, extended lifetime.
- **Solid-state transformers** (§2.2.4): advanced multiport AC/DC interface; less mature, higher cost/complexity.

## Pillar B — Economics and Optimization (§3)

### B.1 Cost metrics and objectives
- Primary objectives: minimize NPC and LCOE/LCOS over project lifetime; CAPEX vs OPEX trade-off.
- Structural (not fixed-price) assessment: manage TOU ratios and peak-demand penalties, tariff sensitivity, feed-in-tariff dependence (§3.1).
- Tooling: HOMER Pro as primary techno-economic tool.

### B.2 Sizing–dispatch trade-off (Table 3)
- **External sizing optimization** [39]: targets component capacity (CAPEX); fixes HOMER's local-optima traps; lowers global LCOE; best in isolated/static-tariff networks.
- **External dispatch control** [40]: targets operational logic (OPEX); fixes HOMER's rigid built-in dispatch; reduces peak-demand charges; best in grid-integrated/dynamic-pricing networks (C06).

### B.3 Physical–economic tool coupling (Table 4)
- PVsyst/Helioscope (physical yield, electrochemical degradation) → HOMER Pro (NPC, replacement forecasting); ensures economics rest on realistic yield (C08).

### B.4 Degradation and operational trade-offs (§3.6)
- Distinguish calendar vs cycle ageing; DoD/high-frequency cycling accelerate fade; health-aware control balances stability vs replacement cost (C02).

### B.5 Site-specific hybridization (§3.2–3.3)
- Rural (Ecuador groundwater PV-battery), urban/campus (renewable fraction up to 72%), EV-fleet DSM, GIS-based siting of offshore wind/onshore solar; resource complementarity (solar+wind+hydro/biogas) reduces diesel dependency and battery size.

## Pillar C — Forecasting and Hybrid Control (§4–§5)

### C.1 Forecasting (Table 5) and preprocessing (Table 6)
- Statistical (ARIMA/SARIMA) → structured deterministic / ML (hybrid ensemble, clustering-enhanced DL, hybrid DL); evaluated via MAPE/RMSE/MAE/MSE (C05).
- Preprocessing: scaling (Min–Max, Z-score) for convergence; decomposition (EMD, VMD, WT) for noise isolation; PCA for redundancy; STL for seasonality.

### C.2 Hybrid metaheuristic control (§4.2, Figure 7)
- Objective functions: emissions (Eq 1), losses (Eq 2), autonomy/LPSP (Eq 3), cost (Eq 4), weighted total (Eq 5).
- GWO-PSO hybrid resolves exploration-exploitation; alternatives: Slime Mould, GA, PSO-GA-LADRC.
- Field deployment via Structured Text + PLCs.

### C.3 NNS integration and BMS (§5)
- NNS factors (Table 7): techno-economic feasibility, system health index, voltage stability, metaheuristic optimization, cost-reflective pricing.
- Planning studies (Table 8): GWO sizing, expansion planning, multi-stage/level planning, cost-reflective modelling, health-index deferral.
- BMS state estimation (Eqs 7–11): SoC (charge, Coulomb counting) vs SoE (energy, voltage-integral); co-estimation; SoE-priority dispatch (C03); Table 9 quantifies improvements.
- Coordination with STATCOMs for transient voltage stability (C09).
- Decentralized primary control: droop control and active power–frequency control for equitable load sharing and transient-stability mitigation without relying entirely on vulnerable communication links (§5); §6 flags droop-control optimization for strict frequency stability in low-inertia environments as future work.
- Securing digitalized NNS assets: group key management protocols for the communication frameworks controlling decentralized storage (§5, ref [76]).
