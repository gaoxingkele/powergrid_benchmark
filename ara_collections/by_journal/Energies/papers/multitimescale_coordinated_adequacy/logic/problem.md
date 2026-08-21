# Problem: Multi-Timescale Coordinated Planning Under Generalized Adequacy

## Observations

1. **Renewable energy penetration is increasing rapidly.** Global consensus supports large-scale integration of renewable energy into power systems [1--3]. Renewable generation is highly sensitive to extreme weather and exhibits pronounced seasonal variations [4].

2. **System inertia is declining.** As synchronous generators are displaced by inertia-free renewable sources, the system's ability to provide inertial support diminishes, elevating the risk of large-scale frequency excursions [5].

3. **Traditional adequacy metrics are inadequate.** Conventional planning ensures total installed capacity exceeds peak load by a predefined margin [23--25]. This capacity-based approach fails to capture flexibility constraints, ramping needs, and inertia requirements introduced by renewables.

4. **Extreme weather creates tail-risk events.** Low-probability, high-impact events (heatwaves, cold waves, droughts) can cause severe energy shortages (6x the expected annual EENS under worst-case scenarios -- Table 5).

5. **State-of-the-art treats adequacy dimensions in isolation.** Existing studies address power/energy adequacy, flexibility adequacy, and inertia adequacy separately without ensuring consistency in resource planning [7--13,16--18].

## Gaps

- **Gap 1: No unified adequacy framework.** No existing framework integrates power/energy, flexibility, and inertia adequacy into a single planning methodology with consistent metrics and resource coordination.

- **Gap 2: Planning models neglect inertia adequacy.** Most transmission and resource expansion models overlook dynamic frequency security constraints, leading to scenarios where operating inertia falls below safe thresholds (Figure 8, M2 vs. M3).

- **Gap 3: Extreme events excluded from planning.** Low-probability extreme meteorological scenarios are not embedded in the planning scenario set, leaving systems vulnerable to tail-risk supply shortages.

- **Gap 4: Scheme comparison lacks holistic adequacy metrics.** Post-evaluation of planning schemes does not typically incorporate multi-dimensional adequacy indicators alongside economic and environmental criteria.

## Key Insight

Generalized adequacy -- integrating power/energy adequacy, flexibility adequacy, and inertia adequacy with coordinated multi-resource planning -- can simultaneously improve supply reliability, frequency security, and extreme-event resilience while maintaining economic viability.

## Assumptions

1. The IEEE 24-bus system is a representative testbed for validating the proposed framework.
2. Historical meteorological data (recent 3 years) provides sufficient basis for constructing extreme scenarios.
3. Sequential Monte Carlo sampling with embedded extreme scenarios adequately captures system risk.
4. The temporal decomposition method [29] effectively separates intra-day and inter-day timescales.
5. Primary frequency regulation ramps linearly within TPFR seconds to cover a fraction alpha of the power imbalance.
6. A 10% load disturbance represents a credible worst-case frequency event for inertia adequacy verification.
7. Long-term energy storage is defined as having duration > 4 hours [32]; short-term storage <= 4 hours.
