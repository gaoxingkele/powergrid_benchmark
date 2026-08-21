# Related Work (typed dependency graph)

## RW01: Mirjalili, Mirjalili & Lewis, 2014 — Grey Wolf Optimizer [44]
- **DOI**: 10.1016/j.advengsoft.2013.12.007
- **Type**: extends
- **Delta**:
  - What changed: This paper takes the original GWO (leadership hierarchy + encircling/hunting position updates, Eqs. 16-19) as its base solver and augments it with chaotic initialization and dynamic opposition-based learning.
  - Why: GWO is simple with strong global search but prone to local optima / slow late convergence.
- **Claims affected**: C02, C04
- **Adopted elements**: The α/β/δ/ω hierarchy, coefficient vectors A/C, convergence factor a decreasing 2→0, and the position-update equations.

## RW02: Long, Jiao, Liang, Cai & Xu, 2019 — A Random Opposition-Based Learning Grey Wolf Optimizer [48]
- **DOI**: 10.1109/ACCESS.2019.2934994
- **Type**: extends
- **Delta**:
  - What changed: The paper advances opposition-based learning from static/random opposites to a *dynamic* opposition operator whose factor r = sin(t/T) varies nonlinearly with iteration (Eq. 20).
  - Why: A static opposite does not adapt to the evolving search landscape; the strong GWO exploitation limits diversity (cited via [48]).
- **Claims affected**: C02, C04
- **Adopted elements**: The opposition-based-learning-on-GWO idea; the observation that GWO exploitation limits search diversity.

## RW03: Opposition-Based Learning references — Ramadan et al., 2022 [50]; Bao, Jia & Lang, 2019 [51]
- **DOI**: 10.3390/electronics11030318 [50]; 10.3390/sym11050716 [51]
- **Type**: imports
- **Delta**:
  - What changed: Provides the base OBL concept (explore current + opposite positions to improve solution quality) that DOBL generalizes.
  - Why: Foundation for the dynamic-opposition enhancement.
- **Claims affected**: C04
- **Adopted elements**: Opposition-based candidate generation.

## RW04: Chaotic-mapping metaheuristics — Sayed, Tharwat & Hassanien, 2019 [47]; Varol Altay & Alatas, 2020 [49]
- **DOI**: 10.1007/s10489-018-1261-8 [47]; 10.1007/s10462-019-09704-9 [49]
- **Type**: imports
- **Delta**:
  - What changed: Establish that chaotic sequences can replace uniform random numbers in intelligent optimizers to improve global search efficiency and robustness; the paper selects among Tent/Sine/Chebyshev/Logistic maps for GWO initialization.
  - Why: Motivates chaotic initialization to diversify the initial population.
- **Claims affected**: C03, C04
- **Adopted elements**: Chaotic-map initialization strategy; the map expressions (Table 3).

## RW05: Amiri, Eskandari & Moradi, 2023 — Virtual inertia control via firefly, with GA/PSO/ABC/GWO comparison [34]
- **DOI**: 10.3390/en16186611
- **Type**: baseline
- **Delta**:
  - What changed: Representative of the comparative-metaheuristic tradition; this paper benchmarks CDGWO against FA, PSO, WOA, GWO, GA, SA on MGC dispatch.
  - Why: To position CDGWO against the standard metaheuristic panel.
- **Claims affected**: C04, C05
- **Adopted elements**: The comparison-against-standard-metaheuristics methodology.

## RW06: Classical LP / NLP dispatch — Tan et al., 2018 (LP) [22]; Patil et al., 2023 (NLP context) [23]
- **DOI**: 10.1109/TSG.2017.2778087 [22]
- **Type**: bounds
- **Delta**:
  - What changed: The paper argues LP/NLP, though simple, are "no longer suitable" for the increasingly complex structure of modern power systems.
  - Why: Justifies using a metaheuristic instead of exact mathematical programming.
- **Claims affected**: C04
- **Adopted elements**: None (positioned as superseded).

## RW07: Machine-learning / deep-learning dispatch — RNN/LSTM/DRL references [27-30]; Mu et al., 2024 (DRL interval dispatch) [19]
- **DOI**: 10.1109/TSG.2023.3323641 [19]
- **Type**: bounds
- **Delta**:
  - What changed: The paper notes DL methods (RNN, LSTM, DRL) autonomously learn dispatch strategies but "demand substantial volumes of training data, extensive training periods, and computational resources".
  - Why: Justifies a training-data-free metaheuristic approach.
- **Claims affected**: C04
- **Adopted elements**: None (positioned as data-heavy alternatives).

## Additional citation footprint (briefer entries)
- **MGC coordination & structure [1-12, 35-40]**: background on microgrid-cluster coordinated scheduling, EMC/operation architectures, and networked-microgrid reviews (e.g. Chen et al. 2024 Stackelberg [1]; Guan et al. 2022 MGC EMS overview [38]). Motivate the MGC problem and structure (Figure 1). Affect C07.
- **Power-balance / equipment / ESS constraints [13-18]**: sources for power-balance and thermal-output/ramping constraints and ESS charge/discharge/capacity/SOC limits (e.g. Mahmoodi et al. 2015 [14]; Hussain et al. 2018 [16]). Affect C07.
- **Objective-function construction (operational + environmental cost) [19-21]**: the cost-only objective tradition the paper enriches with ESS loss + penalties (e.g. Zhang et al. 2023 bacteria-foraging [20]). Affect C01.
- **ESS loss / storage economics [41-43]**: energy-storage characteristics and loss modelling underpinning the ESS loss-cost term (Ibrahim et al. 2008 [42]; Diaz-Gonzalez et al. 2013 [43]). Affect C01.
- **Other GWO variants [45, 46]**: modified GWO for global optimization [45] and modified binary GWO for intrusion detection [46] — cited to support GWO's convergence/global-search strengths. Affect C02.
- **Baseline-algorithm characterizations [31-34, 52-54]**: PSO instability [31-34], WOA uncertainty [52], FA complexity [53], PSO/GWO/FFA/GA feature-selection comparison [54] — cited when interpreting Table 5 behaviour. Affect C05.
