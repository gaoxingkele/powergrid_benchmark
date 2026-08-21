# Related Work: Typed Dependency Graph

This maps the current review's relationship to key prior surveys and studies it cites or positions against.

## RW01: Foundation on Power Quality Challenges

**Source:** Ref. [16] — Harish & Surendra (2022)
**Type:** imports
**Delta:** [16] highlighted power quality challenges that RESs and EVs pose to DN operations, concluding that integration requires standards, regulations, and advanced technologies such as smart metering, AI, and smart ESS. The current review imports this as a foundational challenge and extends it with uncertainty-aware planning perspectives.

## RW02: EVCS Placement Survey Extension

**Source:** Ref. [17] — Ahmad et al. (2022)
**Type:** extends
**Delta:** [17] surveyed approaches for optimally placing EVCSs from DNO, CSO, and EV owner perspectives, evaluating charging procedures, control, management, and EV flow coordination. The current review extends this by adding uncertainty modeling of EV charging demand, AI-based forecasting taxonomy, and multi-objective synthesis dimensions not covered in [17].

## RW03: DG Allocation Survey Extension

**Source:** Ref. [18] — Tercan et al. (2023)
**Type:** extends
**Delta:** [18] surveyed optimal DG allocation studies analyzing optimization methods, objective functions, and performances. The current review extends this to combined EVCS-RES allocation with updated optimization taxonomies that include recent metaheuristic and hybrid algorithms.

## RW04: EV Charging Control Context

**Source:** Ref. [19] — Acharige et al. (2023)
**Type:** imports
**Delta:** [19] reviewed EV charging control and converter architectures, covering EV types, global standards, and semiconductor device recommendations. The current review imports the charging infrastructure design context but shifts focus to planning-level uncertainty and forecasting integration rather than hardware design.

## RW05: Critical Gap in AI-Based Forecasting

**Source:** Ref. [20] — Kim & Hur (2020)
**Type:** refutes
**Delta:** [20] included traditional forecasting techniques (probabilistic modeling based on MCS) for wind-powered EVCS planning but did not cover AI-based forecasting methods. The current review refutes the sufficiency of traditional-only approaches by demonstrating that "most previous studies do not sufficiently examine or include advanced forecasting approaches into their evaluations of planning and integration frameworks."

## RW06: Critical Gap in Forecasting-Driven Planning

**Source:** Ref. [21] — Almazroui & Mohagheghi (2025)
**Type:** refutes
**Delta:** [21] analyzed probabilistic power system performance under high PV and EV penetration using traditional probabilistic methods. The current review refutes the adequacy of this approach by identifying that prior work "fails to explain how AI-based forecasting approaches might improve planning precision and efficacy, especially in uncertain settings."

## RW07: ML-Based EVCS Planning Gap

**Source:** Ref. [8] — Dong et al. (2016)
**Type:** refutes
**Delta:** [8] used EVs for network design minimizing system loss and optimizing voltage profile but did not consider RES (PV) in the planning model. The current review explicitly addresses this gap by covering combined EVCS-RES integration as its core domain.

## RW08: BESS Coordination Import

**Source:** Ref. [22] — Lobos-Cornejo et al. (2025)
**Type:** imports
**Delta:** [22] demonstrated bio-inspired optimization (Grey Wolf Optimizer) for BESS dispatch coordination in AC microgrids, achieving operational cost, network loss, and emission reductions. The current review imports this as evidence for BESS-enabled uncertainty reduction in EVCS planning frameworks.

## RW09: Market and Policy Context

**Source:** Ref. [23] — Sadhukhan et al. (2022)
**Type:** imports
**Delta:** [23] analyzed carbon and electricity market interplay for EV integration, emphasizing coordinated market mechanisms. The current review imports this policy/regulatory dimension and identifies the lack of market and policy integration in techno-economic optimization models as a research gap.

## Key Distinction Mapping Through Table 1

The paper's Table 1 provides a feature-comparison matrix positioning the current review against six prior surveys:

| Feature | Ref. [8] | Ref. [17] | Ref. [18] | Ref. [19] | Ref. [20] | Ref. [21] | Current |
|---------|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:-------:|
| EVCS planning | Y | Y | - | Y | Y | - | Y |
| RES integration | - | - | Y | Y | Y | Y | Y |
| Traditional forecasting | - | - | - | - | Y | Y | Y |
| AI-based forecasting | - | - | - | - | - | - | Y |
| Uncertainty propagation | - | - | - | - | - | - | Y |
| Multi-objective synthesis | - | - | - | - | - | - | Y |
| Recent optimization algorithms | Limited | Limited | Limited | Limited | Limited | Limited | Comprehensive |

The current review is the **only one** that covers AI-based forecasting, uncertainty propagation analysis, and multi-objective synthesis simultaneously, establishing its unique contribution.

## Dependency Summary

```
imports:  Ref. [16], [19], [22], [23], [67], [135]
extends:  Ref. [17], [18]
refutes:  Ref. [8], [20], [21]
baseline: Ref. [8], [17], [18], [19], [20], [21] (via Table 1 comparison)
```
