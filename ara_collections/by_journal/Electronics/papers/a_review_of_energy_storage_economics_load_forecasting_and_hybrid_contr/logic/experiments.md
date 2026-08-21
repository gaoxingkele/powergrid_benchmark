# Experiments

This is a review/survey; it runs no original experiment. The entries below are the review's
**comparison/analysis axes** — the structured syntheses it performs over the surveyed literature.
They are declarative and directional only; exact values live in `evidence/`. "Run" points at the
review section/table that performs the synthesis (no code artifact exists).

## E01: Cross-technology comparison of energy storage media
- **Verifies**: C02, C07
- **Evidence**: evidence/tables/table1.md
- **Run**: §2.1 (narrative) + Table 1 synthesis
- **Setup**:
  - Model: n/a (literature synthesis)
  - Hardware: n/a
  - Dataset: Surveyed storage-technology characteristics across the 103-study corpus
  - System: Comparison across lithium-ion, flow, lead-acid, supercapacitor, pumped hydro, flywheel, compressed air, hydrogen/fuel cell, thermal
- **Procedure**:
  1. Enumerate dominant ESS technologies reported in recent literature
  2. Compare on energy density, response time, lifespan, key applications
  3. Map each technology to grid-service suitability and degradation behaviour
- **Metrics**: Energy density (qualitative), response time, lifespan (years/cycles/hours), application role
- **Expected outcome**:
  - High-power/ultra-fast-response media (supercapacitors, flywheels) suit fast frequency support; high-energy media (lithium-ion, hydrogen) suit shifting/long-duration; no single medium dominates all roles
- **Baselines**: The technologies serve as mutual baselines
- **Dependencies**: none

## E02: Storage configuration comparison (battery-only vs SC-only vs HESS)
- **Verifies**: C07
- **Evidence**: evidence/tables/table2.md
- **Run**: §2.2.3 + Table 2 synthesis
- **Setup**:
  - Dataset: Surveyed configuration studies
  - System: Battery-only, supercapacitor-only, and hybrid (battery + supercapacitor) architectures
- **Procedure**:
  1. Contrast configurations on response time, energy capability, degradation stress, lifetime, primary use
  2. Assess how a HESS combines complementary characteristics
- **Metrics**: Response time class, energy capability, degradation stress, lifetime, use case
- **Expected outcome**:
  - HESS achieves multi-scale response and reduced degradation stress (SC buffers transients), extending battery lifetime relative to standalone battery
- **Baselines**: Battery-only and supercapacitor-only
- **Dependencies**: E01

## E03: Sizing-optimization vs dispatch-control approach comparison
- **Verifies**: C06
- **Evidence**: evidence/tables/table3.md
- **Run**: §3.4 + Table 3 synthesis (studies [39] vs [40])
- **Setup**:
  - Dataset: Two representative HOMER-based studies (external sizing [39]; external dispatch [40])
  - System: HOMER Pro with external optimization vs external dispatch control logic
- **Procedure**:
  1. Characterize each approach by primary cost focus (CAPEX vs OPEX) and critique of HOMER
  2. Identify the operating environment in which each dominates
- **Metrics**: Primary cost driver targeted, LCOE, peak-demand charge reduction (directional)
- **Expected outcome**:
  - External sizing optimization lowers global LCOE and dominates isolated/static-tariff networks; external dispatch control reduces peak-demand charges and dominates grid-integrated/dynamic-pricing networks
- **Baselines**: HOMER native sizing/dispatch strategies
- **Dependencies**: none

## E04: Alignment of physical vs economic optimization tools
- **Verifies**: C01, C08
- **Evidence**: evidence/tables/table4.md
- **Run**: §3.5 + Table 4 synthesis
- **Setup**:
  - System: Meso-scale physical tools (PVsyst, Helioscope) coupled to macro-scale HOMER Pro 3.18.4
- **Procedure**:
  1. Map each tool's primary function, battery-modelling role, and optimization goal
  2. Identify the integration advantage of layering physical fidelity into economic modelling
- **Metrics**: Function coverage, degradation-modelling fidelity, NPC optimization (directional)
- **Expected outcome**:
  - Physical modelling supplies realistic yield and electrochemical-degradation rates so HOMER schedules realistic replacement costs; economic models grounded in real yield rather than theoretical capacity
- **Baselines**: HOMER-only (macro-economic) modelling
- **Dependencies**: none

## E05: Forecasting-accuracy and dispatch-impact synthesis
- **Verifies**: C04, C05
- **Evidence**: evidence/tables/table5.md
- **Run**: §4.1 + Table 5 synthesis (studies [58,59,61,62])
- **Setup**:
  - Dataset: Recent AI-driven forecasting studies applied to renewable/load historical data
  - System: Hybrid ensemble learning, comprehensive AI review, clustering-enhanced deep learning, hybrid deep learning
- **Procedure**:
  1. Collect forecasting method, accuracy metric, and dispatch/economic impact per study
  2. Relate error-margin reduction to battery-dispatch efficiency and grid economics
- **Metrics**: Predictability coefficient, MAE/MSE/MAPE/RMSE reductions, curtailment/load-balancing impact (directional)
- **Expected outcome**:
  - Advanced clustering + deep learning reduce error margins, improving storage scheduling, load balancing, and curtailment reduction
- **Baselines**: Traditional statistical forecasting (ARIMA/SARIMA)
- **Dependencies**: none

## E06: Data-preprocessing technique comparison
- **Verifies**: C05
- **Evidence**: evidence/tables/table6.md
- **Run**: §4.3 + Table 6 synthesis
- **Setup**:
  - System: Min–Max, Z-score, EMD, VMD, Wavelet Transform, PCA, STL
- **Procedure**:
  1. Characterize each technique by primary function and best use case
  2. Distinguish scaling (convergence) from decomposition (noise isolation) roles
- **Metrics**: Function, best-fit data characteristic (qualitative)
- **Expected outcome**:
  - Scaling accelerates hybrid-algorithm convergence; decomposition (EMD/VMD/WT) isolates trends from severe signal noise; technique choice is dataset-dependent
- **Baselines**: Raw (unprocessed) time series
- **Dependencies**: none

## E07: NNS integration-factor synthesis for AC microgrids
- **Verifies**: C09
- **Evidence**: evidence/tables/table7.md
- **Run**: §5 + Table 7 synthesis
- **Setup**:
  - System: NNS deployment factors — techno-economic feasibility, system health index, voltage stability, metaheuristic optimization, cost-reflective pricing
- **Procedure**:
  1. Enumerate factors governing NNS integration
  2. Link each factor to the review's framework elements (Sections 3–4, Figure 2)
- **Metrics**: Factor coverage and framework linkage (qualitative)
- **Expected outcome**:
  - Successful NNS deployment requires jointly validating smart investment against infrastructure upgrades, asset health, voltage stability, near-optimal sizing/control, and fair cost allocation
- **Baselines**: Traditional network-reinforcement planning
- **Dependencies**: none

## E08: Planning/control studies summary for hybrid microgrids
- **Verifies**: C02, C09
- **Evidence**: evidence/tables/table8.md
- **Run**: §5 + Table 8 synthesis (studies [66–71])
- **Setup**:
  - Dataset: Six advanced planning/control studies
  - System: GWO, expansion-planning review, multi-stage/multi-level planning, cost-reflective modelling, health-index incorporation
- **Procedure**:
  1. Record approach, key objective, NNS type, and highlighted benefit per study
  2. Identify the residual gap (combining algorithms with physical AC-microgrid constraints)
- **Metrics**: Objective addressed, benefit category (directional)
- **Expected outcome**:
  - Algorithms like GWO reduce installation costs and grid dependence; health-index-aware planning defers capital expenditure and extends asset lifespan; a gap remains in coupling algorithms with physical AC constraints
- **Baselines**: Capital-intensive infrastructure improvement
- **Dependencies**: E07

## E09: SoC/SoE state-tracking and economic-operation synthesis
- **Verifies**: C01, C03, C04
- **Evidence**: evidence/tables/table9.md
- **Run**: §BMS (Battery Management Systems and State Estimation) + Table 9 synthesis (studies [66,99,63])
- **Setup**:
  - System: SoC tracking, SoE estimation, and hybrid GWO-PSO state tracking under offline time-domain simulation
- **Procedure**:
  1. Relate each state metric to its quantitative tracking improvement and economic/operational effect
  2. Link precise state estimation to reduced cell count, avoided shortages, and lower Total NPC
- **Metrics**: Tracking-performance improvement, capacity-estimation-error reduction, cost/import impact (directional)
- **Expected outcome**:
  - Improved SoC tracking reduces required cell count/capital; SoE prioritization prevents capacity overestimation and shortages; hybrid GWO-PSO state tracking lowers Total NPC and grid imports
- **Baselines**: SoC-only estimation; non-hybrid control
- **Dependencies**: none

## E10: PRISMA-informed literature screening and inclusion
- **Verifies**: C01, C08
- **Evidence**: evidence/figures/figure1.md
- **Run**: §1.3 + Figure 1 (PRISMA flow)
- **Setup**:
  - Dataset: IEEE Xplore, ScienceDirect, Scopus, Web of Science; literature 2012–2026
  - System: Identification → screening → eligibility → inclusion
- **Procedure**:
  1. Identify records; remove duplicates; screen by title/abstract; assess full texts; apply inclusion/exclusion criteria
  2. Group included studies into thematic categories (ESS integration, forecasting, techno-economic, optimization/control)
- **Metrics**: Record counts at each PRISMA stage (exact counts in evidence)
- **Expected outcome**:
  - A traceable, reproducible screening funnel yielding the final synthesized corpus grouped by theme
- **Baselines**: none (methodological)
- **Dependencies**: none

## E11: GWO-PSO hybrid control workflow analysis
- **Verifies**: C04
- **Evidence**: evidence/figures/figure7.md
- **Run**: §4.2 / §5 + Figure 7 (schematic workflow)
- **Setup**:
  - System: Hybrid GWO (exploration phase) → PSO (exploitation phase) for HRES control calculation
- **Procedure**:
  1. Trace the algorithm: GWO updates alpha/beta/delta search agents until iteration limit; top GWO solutions seed PSO particle velocities/positions; PSO iterates to convergence; output best solution (gbest) for HRES control
- **Metrics**: Workflow structure and convergence conditions (qualitative)
- **Expected outcome**:
  - GWO's global search seeds PSO's local refinement, producing a near-optimal HRES control solution balancing technical and economic constraints
- **Baselines**: Standalone GWO or standalone PSO
- **Dependencies**: E09
