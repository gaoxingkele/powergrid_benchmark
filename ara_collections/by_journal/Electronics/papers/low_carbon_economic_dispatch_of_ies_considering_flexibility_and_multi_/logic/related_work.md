# Related Work

Typed dependency graph for the paper's 31 references. Works with a specific technical delta get full RW blocks; the remainder are captured briefly to preserve the citation footprint.

## RW03: Zhou et al., 2025 — Tiered carbon trading for IES dispatch
- **DOI**: China Electr. Power 2025, 58, 77–87 [CrossRef]
- **Type**: imports
- **Delta**:
  - What changed: Incorporates a stepped (tiered) carbon-trading cost into the carbon framework
  - Why: Demonstrates the tiered mechanism cuts emissions more than plain CET
- **Claims affected**: C04
- **Adopted elements**: Motivation for embedding a carbon-cost term in the operator objective

## RW05: Chen et al., 2025 — Green certificate + carbon trading joint model
- **DOI**: Integr. Smart Energy 2025, 47, 21–30 [CrossRef]
- **Type**: imports
- **Delta**:
  - What changed: Combines green-certificate trading (GCT) with carbon trading, exploiting their synergy/convertibility
  - Why: Higher renewable accommodation and lower emissions
- **Claims affected**: C05
- **Adopted elements**: The GCT-CET joint-mechanism concept used in the upper-level objective

## RW19: Zhang et al., 2023 — Two-stage EV charge/discharge via PSO
- **DOI**: ETransportation 2023, 18, 100262 [CrossRef]
- **Type**: baseline/extends
- **Delta**:
  - What changed: Two-stage EV charging/discharging optimization via PSO with demand response
  - Why: Enhances grid stability and EV-user economics
- **Claims affected**: C03
- **Adopted elements**: PSO-based EV scheduling and demand-response framing for EV flexibility

## RW22: Li et al., 2021 — Stackelberg-game IES scheduling
- **DOI**: Energy Convers. Manag. 2021, 235, 113996 [CrossRef]
- **Type**: extends
- **Delta**:
  - What changed: Stackelberg leader–follower game reconciling IES operator and users under uncertain renewables
  - Why: Coordinates operator–user interests
- **Claims affected**: C01, C02
- **Adopted elements**: Leader–follower (bi-level) structure between operator and demand side; this paper adds flexibility objective + EVs

## RW24: Wang et al., 2023 — EV + load-aggregator VPP configuration; TOPSIS
- **DOI**: Energy Rep. 2023, 9, 1093–1100 [CrossRef]
- **Type**: imports
- **Delta**:
  - What changed: VPP configuration with multi-entity participation of EVs and load aggregators; uses TOPSIS
  - Why: Low-carbon economy with improved reliability and reduced charging disorder
- **Claims affected**: C03, C07, C09
- **Adopted elements**: TOPSIS compromise-selection from the Pareto front (explicitly cited at §3.3); multi-entity EV + aggregator framing

## RW25: Zheng et al., 2024 — Stochastic-robust multi-stakeholder IES operation
- **DOI**: Appl. Soft Comput. 2024, 167, 112426 [CrossRef]
- **Type**: bounds
- **Delta**:
  - What changed: Stochastic robust optimization for EVs + user aggregators, multi-attribute decision support
  - Why: Handles EV/demand uncertainty, lowers system cost
- **Claims affected**: C02, C03
- **Adopted elements**: Multi-stakeholder operation framing; this paper is deterministic (uncertainty flagged as future work)

## RW26: Zhang et al., 2025 — Bi-level game dispatch of PIES with electricity-carbon markets
- **DOI**: Autom. Electr. Power Syst. 2025, 49, 45–59
- **Type**: bounds
- **Delta**:
  - What changed: Bi-level game dispatch for park IES with electricity-carbon market synergy; solved by improved ADMM
  - Why: Distributed optimization of coupled electricity-carbon decisions
- **Claims affected**: C01, C04
- **Adopted elements**: Bi-level park-IES + carbon-market framing; this paper uses PSO+CPLEX instead of ADMM

## RW27: Liu et al., 2025 — Hybrid game (operator vs RIES alliance), GA solver
- **DOI**: Electr. Power Autom. Equip. 2025, 45, 15–22
- **Type**: bounds
- **Delta**:
  - What changed: Hybrid game with energy-system operator as master and RIES alliance as slave; solved by Genetic Algorithm
  - Why: Coordinate operator and alliance under carbon-trading risk
- **Claims affected**: C01, C09
- **Adopted elements**: Master–slave hierarchy; GA is an alternative to this paper's improved PSO (not adopted)

## RW28: Liu et al., 2022 — Two-stage IES scheduling; PSO suitability
- **DOI**: IEEE Access 2022, 10, 83336–83349 [CrossRef]
- **Type**: baseline
- **Delta**:
  - What changed: Two-stage IES scheduling for renewable consumption; motivates PSO's suitability for IES
  - Why: PSO is concise and fast-converging for IES optimal scheduling
- **Claims affected**: C09
- **Adopted elements**: Justification for choosing PSO as the base solver (then improved here)

## RW29: Xie, 2025 — GCT-carbon joint trading dispatch (thesis)
- **DOI**: Master's Thesis, Yanshan University, 2025
- **Type**: imports
- **Delta**:
  - What changed: Green-certificate–carbon joint-trading low-carbon dispatch of park IES
  - Why: Source of the green-certificate quota and carbon-emission-quota formulas
- **Claims affected**: C04, C05
- **Adopted elements**: Green-certificate quota calc (Eq. 9) and carbon-emission-quota calc (Eq. 10) coefficients cited from here

## RW30: Du, 2025 — IES collaborative optimization with E/H/C demand response (thesis)
- **DOI**: Master's Thesis, Northeast Electric Power University, 2025
- **Type**: imports (data source)
- **Delta**:
  - What changed: Provides the numerical-case data
  - Why: Source of load/renewable forecast curves and device/EV parameters
- **Claims affected**: C01–C08 (all case results depend on this data)
- **Adopted elements**: Figure 4 forecast curves, Table 1 device parameters, Table 4 EV parameters

## RW31: Lu et al., 2025 — Dynamic carbon-green-certificate dispatch of multiple IES
- **DOI**: Autom. Electr. Power Syst. 2025, 49, 52–60 [CrossRef]
- **Type**: imports (data source)
- **Delta**:
  - What changed: Coordinated dispatch under dynamic carbon-green-certificate interaction
  - Why: Source of the TOU interactive electricity prices (Table 3)
- **Claims affected**: C02, C05
- **Adopted elements**: Time-of-use price data

## Brief citations (background / infrastructure / inline comparison — no distinct technical delta adopted)
- **[1] Zhong et al., 2024** (Proc. CSEE) — background on new power-system planning/operation/market.
- **[2] Huang et al., 2020** (Proc. IEEE) — multi-energy network modeling/low-carbon analysis; background.
- **[4] Fan et al., 2023** (Manag. Sci.) — carbon quota/trading policy effects; economic-efficiency vs low-carbon win–win.
- **[6] Li et al., 2024** (Power Syst. Prot. Control) — wind/solar/hydrogen IES with P2G + carbon capture; low-carbon dispatch background.
- **[7] Yang et al., 2025** (J. Mod. Power Syst. Clean Energy) — low-carbon community IES with resource flexibility + SOFC segmented control; flexibility-resource motivation.
- **[8] Mahmud et al., 2024** (Energy) — modular hydrogen-based nuclear-renewable IES; flexibility/profitability.
- **[9] Yuan & Zhang, 2024** (Proc. CSEE) — source-storage-load coordinated planning review; renewable-uncertainty motivation.
- **[10] Chicco et al., 2020** (Proc. IEEE) — defines IES flexibility (regulate supply/demand/flows).
- **[11] Mohandes et al., 2019** (IEEE TPS) — defines flexibility resources (units, storage, flexible loads, EVs).
- **[12] De et al., 2022** (Energies) — DR as flexibility measure; collaborative IES optimization.
- **[13] Zhou et al., 2023** (Energy Sources A) — electricity+gas DR multi-objective (cost + user satisfaction).
- **[14] Pan et al., 2023** (Trans. China Electrotech. Soc.) — multi-flexibility-resource effect on electric-heat IES.
- **[15] Shen et al., 2022** (J. Hydraul. Eng.) — flexibility-demand quantification via segmented renewable output.
- **[16] Zhang et al., 2023** (Electronics) — multi-agent DRL for safe distributed energy-hub scheduling under carbon cost + differential privacy.
- **[17] Nie et al., 2025** (Electronics) — low-carbon scheduling for multi-microgrids via multi-agent DRL.
- **[18] Arvanitidis & Alamaniotis, 2025** (IEEE TPEC) — security-constrained economic dispatch in nuclear IES (IEEE-30 bus).
- **[20] Jahic et al., 2022** (Energies) — flexibility quantification for electric-bus depots (up/down flexibility).
- **[21] Ma et al., 2021** (Smart Power) — electricity-gas IES coordinated planning via multi-agent benefits/game.
- **[23] Yang et al., 2023** (Sustain. Energy Grids Netw.) — non-cooperative game + multi-energy pricing for demand-side management.
