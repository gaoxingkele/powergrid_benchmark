# Related Work

## Typed Dependency Graph

### Adequacy Evaluation Frameworks

**[RW01] ESIG (Stenclik, 2024) [7]**
- **Type:** extends
- **Role:** Foundation for multi-metric adequacy; advocates replacing single LOLE 0.1 d/a with multi-metric framework including EENS and risk indicators. The paper adopts this direction, adding flexibility and inertia dimensions.
- **Specific delta:** The paper extends ESIG's multi-metric concept from power/energy to generalized adequacy.

**[RW02] Shariatkhah et al. (2016) [8]**
- **Type:** extends
- **Role:** Extended adequacy assessment by incorporating primary energy supply constraints and multiple energy carriers.
- **Specific delta:** The paper goes further by adding flexibility and inertia dimensions to adequacy.

**[RW03] Gong et al. (2018) [9]**
- **Type:** extends
- **Role:** Incorporated generator reserve capacity, transmission constraints, and wind ramping limits (RPL, RRL) into SOCP-based adequacy evaluation.
- **Specific delta:** The paper generalizes this to a full planning framework rather than evaluation-only.

### Flexibility and Inertia Evaluation

**[RW04] Lu et al. (2018) [10]**
- **Type:** aligns
- **Role:** Developed comprehensive flexibility assessment with shortage probability, expectation, duration, and quantile indicators.
- **Specific delta:** The paper transforms these evaluation-only metrics into planning-guiding constraints.

**[RW05] Lannoye et al. (2015) [11]**
- **Type:** extends
- **Role:** Defined IRRP and IRRE as probabilistic flexibility indicators.
- **Specific delta:** The paper proposes ramp capacity and ramp rate margin metrics tailored to planning.

**[RW06] Lin et al. (2021) [12]**
- **Type:** aligns
- **Role:** Introduced inertia security region (ISR) concept with metrics (aspect ratio, security margin, reserve coefficient).
- **Specific delta:** The paper proposes planning-oriented minimum inertia and inertia margin from RoCoF/nadir constraints.

**[RW07] Ju et al. (2021) [13]**
- **Type:** aligns
- **Role:** Proposed four frequency security assessment metrics with correlation to system inertia.
- **Specific delta:** The paper embeds these frequency metrics as planning constraints rather than post-assessment.

### Transmission and Resource Planning

**[RW08] Becerik & Karatepe (2018) [16]**
- **Type:** extends
- **Role:** Chance-constrained TEP accounting for load/wind uncertainty, optimizing economic-reliability trade-off.
- **Specific delta:** The paper adds flexibility and inertia dimensions plus extreme scenarios.

**[RW09] Hu et al. (2022) [17]**
- **Type:** extends
- **Role:** Distributed robust optimization for TEP cost minimization under uncertainty while maximizing renewable penetration.
- **Specific delta:** The paper replaces distributionally robust with iterative extreme-scenario embedding.

**[RW10] Yin et al. (2023) [18]**
- **Type:** extends
- **Role:** Enhanced BPSO algorithm for security-constrained TEP.
- **Specific delta:** The paper adds flexibility and inertia adequacy as explicit planning objectives.

**[RW11] Jiang et al. (2023) [29]**
- **Type:** imports (core methodology)
- **Role:** Temporal decomposition method splitting 8760 h into intra-day and inter-day timescales. The paper directly uses this method for modeling storage energy transfer across timescales.

**[RW12] Liang et al. (2024) [31]**
- **Type:** imports (parameter source)
- **Role:** Source for carbon price assumptions, load and renewable output profiles, network constraints, RoCoF and Nadir parameters, frequency response limits, and response times used in the case study.

**[RW13] Chen et al. (2025) [34]**
- **Type:** imports (parameter source)
- **Role:** Source for storage and renewable energy cost parameters.

### Multi-Criteria Decision Making for Planning Schemes

**[RW14] Garcia-Mercado et al. (2023) [19]**
- **Type:** aligns
- **Role:** Enhanced BPSO for deterministic TEP.
- **Specific delta:** The paper uses PROMETHEE-II rather than optimization for scheme selection.

**[RW15] Li et al. (2022) [20]**
- **Type:** imports (method component)
- **Role:** Entropy weight method for objective weighting. The paper uses this alongside AHP.

**[RW16] Zhang et al. (2014) [22]**
- **Type:** aligns
- **Role:** PROMETHEE-II for MCDM in power system context.
- **Specific delta:** The paper applies PROMETHEE-II specifically to generalized adequacy schemes with AHP-entropy combined weights.

### Citations Listed but Not Closely Used

- [1] Chen et al. (2025) — RL for TOU pricing (motivational citation for renewable integration)
- [2] Hansen et al. (2019) — 100% renewable in Germany (motivational)
- [3] Chang et al. (2023) — carbon trading and green certificates (motivational)
- [4] Borasio & Moret (2022) — deep decarbonization (motivational)
- [5] Liu et al. (2021) — dynamic state estimation (motivational for inertia concern)
- [6] Shuai et al. (2024) — extreme drought impact (motivational for extreme events)
- [14] Xu et al. (2022) — resilience enhancement (background)
- [15] Shafiei et al. (2024) — resilience with renewables/storage (background)
- [21] Xin et al. (2021) — BWM entropy TOPSIS (alternative MCDM, not used)
- [23] Borbath & Van Hertem (2024) — transmission representation for adequacy (background)
- [24] Grijalva & Visnesky (2006) — generation network security (background)
- [25] Bazmi & Zahedi (2011) — optimization modeling review (background)
- [26] Jebaraj & Iniyan (2006) — energy models review (background)
- [27] UK DESNZ (2023) — UK reliability standard metrics (background)
- [28] Amarasinghe et al. (2020) — KDE for renewable impact on adequacy (background)
- [30] Ahmadi & Ghasemi (2014) — linearized frequency stability constraints (method reference for Eq. 35 linearization)
- [32] Twitchell et al. (2023) — defining long-duration energy storage (term definition)
- [33] (cost parameter reference for storage/renewable costs, referenced indirectly in text)
