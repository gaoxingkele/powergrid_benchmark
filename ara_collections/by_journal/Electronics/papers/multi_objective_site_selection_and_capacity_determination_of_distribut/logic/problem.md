# Problem Specification

## Observations

### O1: DG penetration widens the node load peak–valley difference and destabilizes voltage
- **Statement**: As distributed generation (DG) rises at the supply end of the active distribution network (ADN), each node's load peak-to-valley difference increases, and DG output — unlike coal — is highly uncertain, perturbing voltage stability, network loss, and power quality.
- **Evidence**: Introduction and §2 (pp.1–3); demonstrated on IEEE 33-node in Figure 7 (scenario 2 voltage surface is markedly rougher than scenario 1).
- **Implication**: Planning must explicitly account for DG output uncertainty, not just placement.

### O2: EV clusters have a time pattern complementary to wind/PV and can act as mobile storage
- **Statement**: EV ownership is growing and the EV group has a "relatively clear time pattern, which is consistent with the output of wind turbines and photovoltaic cells"; EVs can serve as mobile energy storage with more flexibility and lower cost than dedicated storage.
- **Evidence**: Introduction (p.2); EV sampling parameters in Table A1.
- **Implication**: EV fleets are a candidate "shared energy storage" resource to smooth DG uncertainty.

### O3: Conventional storage is costly and its siting is unsolved under uncertainty
- **Statement**: Up-front investment in dedicated energy-storage equipment during the early ADN planning stage is expensive, and where to place it is an open problem; existing storage-siting studies mostly ignore DG output uncertainty.
- **Evidence**: §2 (p.3); Introduction survey of refs [16]–[21].
- **Implication**: A siting/sizing model that co-optimizes storage capacity while accounting for uncertainty is needed.

## Gaps

### G1: Existing DG-uncertainty methods ignore storage siting/sizing (or vice versa)
- **Statement**: Prior work either handles DG uncertainty (scenario/robust methods) OR adds storage, but rarely couples uncertain-DG scenario modeling with the siting and capacity determination of storage.
- **Caused by**: O1, O3
- **Existing attempts**: Weibull/Beta reliability sampling (ignores DG time scale, cannot cost annually); day-ahead error sampling (prediction limitations); K-means wind-speed scenarios [12,13,18]; SVG voltage regulation [14,15]; two-layer chance-constraint OPF [16].
- **Why they fail**: They treat marginals independently (miss wind–solar correlation), or omit storage siting, or ignore the uncertainty when siting storage.

### G2: EV-cluster output is itself uncertain and biased by historical data
- **Statement**: Using EV clusters as storage requires accurate prediction of fleet state (arrival/departure/SOC), but EV historical data is biased and standard clustering/LSTM leaves residual error.
- **Caused by**: O2
- **Existing attempts**: EV-cluster dispatchable-potential models and bidding models [19,20,21]; unidirectional LSTM.
- **Why they fail**: Do not further process EV-cluster output uncertainty; unidirectional models miss future-context temporal structure.

### G3: Single-objective planning cannot balance voltage, loss, and storage cost together
- **Statement**: Optimizing a single variable cannot reflect the ADN's coupled trade-offs among voltage fluctuation, network loss, and storage capacity/cost.
- **Caused by**: O1, O3
- **Existing attempts**: single-target optimal-power-flow formulations.
- **Why they fail**: A single objective cannot express the conflict between minimizing voltage deviation, minimizing loss, and minimizing storage capacity simultaneously.

## Key Insight
- **Insight**: Model the EV fleet as dispatchable "shared energy storage" whose availability is temporally aligned with wind/PV output, generate correlated DG scenarios with a KDE + Frank-copula joint distribution, and co-optimize EVS siting and capacity against three conflicting objectives (voltage fluctuation, network loss, storage capacity) with a multi-objective solver.
- **Derived from**: O1, O2, O3
- **Enables**: Using EVs to substitute for costly dedicated storage while explicitly smoothing DG uncertainty at the planning stage.

## Assumptions
- A1: Each EV type has a fixed arrival/departure time and initial SOC drawn from the distributions in Table A1 (normal/uniform).
- A2: Wind–solar joint output is well described by a Frank copula (chosen for negative correlation/complementarity) over KDE-fitted marginals.
- A3: The IEEE 33-node system with total load 3715 kW + j2300 kvar at 12.66 kV rated voltage is representative for validation.
- A4: At most 2 network nodes may host EVS storage; maximum installed power per the case is 400 kW; connectable node index ranges 2–33.
- A5: The 500 generated wind–solar scenarios can be reduced to a small representative set (5 shown) with associated probabilities without losing the randomness/correlation structure.
