# Related Work — Typed Dependency Graph

## References and Their Relationship to This Paper

### Imports (uses methods/techniques from)

| Reference | Type | Relationship |
|-----------|------|--------------|
| [10] Zhang et al. (2021) | Extends | DDDRO for transmission expansion planning with contingency-constrained generation reserve optimization; the proposed model extends this approach by adding VPL, VPP, and flexibility |
| [12] Benders (1962) | Imports | Benders decomposition as reference decomposition method |
| [13] Conejo et al. (2006) | Imports | Decomposition techniques in mathematical programming |
| [16] Jabr (2013) | Imports | Three-level robust optimization modeling framework (min-max-min) |
| [17] Chen et al. (2014) | Imports | Robust optimization for TEP: minimax cost vs minimax regret |
| [18] Ruiz & Conejo (2015) | Imports | Robust transmission expansion planning formulation |
| [55] Fonseca et al. (2018) | Imports | Bottom-up approach to compute DER flexibility at TSO-DSO boundary |
| [56] Nguyen & Byrne (2021) | Imports | Evaluation of energy storage providing virtual transmission capacity |
| [57] IRENA (2020) | Imports | Virtual power lines — innovation landscape brief |
| [58] Baringo et al. (2021) | Imports | Holistic planning of virtual power plant with nonconvex operational model |
| [59] Ferreira et al. (2022) | Imports | Perpetuity financial model (PLANEL model) |
| [60] Ding et al. (2019) | Imports | Duality-free decomposition for data-driven stochastic SCUC |
| [61] Wang et al. (2020) | Imports | Data-driven distributionally robust economic dispatch for distribution networks |
| [62] Zeng & Zhao (2013) | Imports | Column-and-constraint generation method for two-stage robust optimization |
| [63] Erseghe (2014) | References | Distributed optimal power flow using ADMM |
| [68] Zhao & Guan (2016) | Imports | Data-driven stochastic unit commitment using L1 and L∞ norms for uncertainty set |
| [69] Bagheri et al. (2017) | Imports | Data-driven stochastic transmission expansion planning |

### Extends (builds upon or adds to)

| Reference | Type | Relationship |
|-----------|------|--------------|
| [7] Ranjbar et al. (2020) | Extends | Adds VPL and flexibility to their DER co-planning model |
| [8] Abushamah et al. (2021) | Extends | Extends distributed generation expansion planning by adding transmission-level VPL |
| [9] Ranjbar et al. (2021) | Extends | Extends resiliency-oriented planning with VPL and flexibility options |
| [20] Alvarez et al. (2022) | Extends | Incorporates local flexibility services in transmission expansion planning, extending their value/impact analysis |
| [22] Kristiansen et al. (2016) | Extends | Adds system flexibility to multinational transmission expansion planning |
| [31] Palmintier & Webster (2016) | Extends | Extends operational flexibility impact on generation planning to transmission planning |
| [34] Ramos et al. (2022) | Extends | OpenTEPES: extends open-source TGEP with VPL and flexibility modeling |
| [35] Dominguez et al. (2015) | Extends | Extends toward fully renewable electric energy systems with VPL support |
| [36] Baringo & Baringo (2018) | Extends | Extends stochastic adaptive robust optimization for GEP with VPL |
| [42] Toolabi Moghadam et al. (2023) | Extends | Extends stochastic flexible power system expansion with TSO-DSO flexibility |
| [52] Li et al. (2018) | Extends | Extends robust coordinated TGEP with ramping requirements and construction periods |

### Bounds (provides context/limitations for)

| Reference | Type | Relationship |
|-----------|------|--------------|
| [1] Matevosyan et al. (2021) | Bounds | Operational security context bounds the flexibility requirements |
| [2] Spyrou et al. (2017) | Bounds | Co-optimizing transmission and generation benefits bounds the scope |
| [3] Latorre et al. (2003) | Bounds | Classification of TEP publications and models provides bounding taxonomy |
| [4] Hemmati et al. (2013) | Bounds | Comprehensive review of GEP and TEP bounds the problem space |
| [5] Mahdavi et al. (2019) | Bounds | TEP literature review and classification |
| [11] Mohanapriya & Manikandan (2014) | Bounds | Congestion management using LMP bounds the pricing framework |
| [14] Romero & Monticelli (1994) | Bounds | Hierarchical decomposition bounds the exact method reference |
| [23] Tejada-Arango et al. (2020) | Bounds | Power-based generation expansion planning for flexibility requirements |
| [24] Dehghan et al. (2018) | Bounds | Multistage robust TEP bounds the robust optimization scope |

### Baseline (used as comparison benchmark)

| Reference | Type | Relationship |
|-----------|------|--------------|
| [72] Rider (2006) | Baseline | Garver 6-node test system data and base expansion solution |
| [73] Barrows et al. (2020) | Baseline | IEEE RTS-GMLC test system data and base expansion solution |
| [75] IRENA (2024) | Baseline | ESS investment and operation costs (current and projected) |
| [76] Zobaa et al. (2018) | Baseline | ESS cost reference at different voltage levels |

### Refutes (contradicts or identifies gap in)

| Reference | Type | Relationship |
|-----------|------|--------------|
| [6] El-Meligy et al. (2021) | Refutes gap | Their coordinated T&D expansion model does not include VPL or TSO-DSO flexibility services |
| [25] Zhang et al. (2013) | Refutes gap | Their AC network model for TEP does not consider VPL or flexibility |
| [26] Liu et al. (2018) | Refutes gap | ACOPF global solution does not address TGEP with VPL |
| [27] Bynum et al. (2019) | Refutes gap | ACOPF tightening approach does not incorporate VPL |
| [28] Ghaddar & Jabr (2019) | Refutes gap | SDP branch-and-bound for TEP does not include VPL |
| [29] Mehrtash & Cao (2022) | Refutes gap | Global solver for TEP with AC model does not consider VPL |
| [30] Mehrtash et al. (2024) | Refutes gap | Power flow representation comparison does not include VPL |
| [32] Chen et al. (2018) | Refutes gap | Capacity expansion with flexibility constraints does not model VPL |
| [33] Wendelborg et al. (2023) | Refutes gap | Intraday uncertainty in capacity expansion does not include VPL |
| [37] Moreira et al. (2017) | Refutes gap | Reliable renewable GEP does not include VPL or DSO flexibility |
| [38] Ahmadi et al. (2020) | Refutes gap | Dynamic robust GEP does not include VPL |
| [39] Moreira et al. (2021) | Refutes gap | Climate-aware GEP does not include VPL or TSO-DSO flexibility |
| [40] Backe et al. (2021) | Refutes gap | Stochastic capacity expansion does not include VPL |
| [41] Curty et al. (2023) | Refutes gap | Hydrothermal GEP soft-linking does not include VPL |
| [43] Garcia-Bertrand & Minguez (2017) | Refutes gap | Dynamic robust TEP does not include VPL |
| [44] Roldan et al. (2019) | Refutes gap | Robust TEP under correlated uncertainty does not include VPL |
| [45] Liang et al. (2021) | Refutes gap | Robust TEP with adaptive uncertainty set does not include VPL |
| [46] Liang et al. (2019) | Refutes gap | Probability-driven TEP does not include VPL |
| [47] Yin et al. (2023) | Refutes gap | Data-driven robust TEP does not include VPL |
| [48] Garcia-Cerezo et al. (2022) | Refutes gap | Dynamic robust TEP with inter-temporal constraints does not include VPL |
| [49] Garcia-Cerezo et al. (2023) | Refutes gap | Multi-year two-stage adaptive robust TEP does not include VPL |
| [50] Zhang & Conejo (2018) | Refutes gap | Coordinated investment in transmission and storage does not include DSO flexibility |
| [51] Verastegui et al. (2019) | Refutes gap | Adaptive robust power systems planning does not include VPL |
| [53] Yin et al. (2023) | Refutes gap | Flexibility-oriented robust TEP does not include DSO flexibility |
| [54] Ni et al. (2018) | Refutes gap | Global sensitivity analysis does not address VPL or TGEP |
