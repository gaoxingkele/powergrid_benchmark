# Table 6: Post-Optimization Sensitivity

**Caption**: Post-optimization sensitivity.

**Content**:
| Scenario | Operating Setting | Finv (10^4 CNY) | Em (10^4 CNY) | Floss (10^4 CNY) | Rationale |
|----------|------------------|----------------|--------------|-----------------|-----------|
| S0 | Baseline (PV: Rc=Rr, Tc=25C; WT: v~0.8vr; ES: real-time) | 1175 | 51.0 | 2.50 | Optimal config at typical daily operating point |
| S1 | PV-cloudy (PV: Rc=0.6Rr; other same as S0) | 1175 | 58.5 | 2.85 | PV decrease -> grid compensation needed -> outages/losses increase |
| S2 | PV-winter (PV: Rc=0.75Rr, Tc=5C; other same as S0) | 1175 | 54.0 | 2.65 | Radiation weakened but temp reduced; impact moderate |
| S3 | WT-high (WT: v=0.9vr; other same as S0) | 1175 | 48.0 | 2.30 | Wind increase -> local supply enhanced -> reduced outages/losses |
| S4 | WT-low (WT: v=0.6vr; other same as S0) | 1175 | 61.0 | 3.20 | Wind decrease -> tidal backflow -> losses rise significantly |
| S5 | ES-ND (ES: night charge 0-6h / day discharge 10-16h) | 1175 | 52.5 | 2.55 | Fixed-period weaker than real-time; peak-valley alignment insufficient |
| S6 | ES-RT (ES: real-time voltage/marginal loss trigger) | 1175 | 49.5 | 2.35 | On-demand scheduling -> better voltage and loss characteristics |

**Page**: 14
**Type**: table
**Source**: Original paper, Section 5.3
