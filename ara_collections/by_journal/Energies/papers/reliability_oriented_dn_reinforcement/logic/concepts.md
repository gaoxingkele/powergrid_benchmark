# Concepts

## C01: N-1 Contingency Principle
A reliability assessment criterion requiring that the distribution system remains capable of supplying demand and maintaining service standards even if any single component (substation or feeder) becomes unavailable. The paper applies this principle as the foundation for evaluating system performance under fault conditions. Only substation and feeder outages are considered.

## C02: Network Restoration (Success Mode 1)
The first level of the operational hierarchy. When a fault occurs, protection devices isolate the affected section. If alternative restoration paths exist (via tie lines and NO switches), customers in the isolated section can be reconnected to the main source through switching operations, reducing downtime from full repair time to switching duration. Success requires: (a) at least one restoration path exists, (b) receiving feeder thermal limit is not exceeded, (c) substation is not overloaded, (d) bus voltages remain within limits, and (e) power balance is satisfied.

## C03: Intentional Islanding (Success Mode 2)
The second level of the operational hierarchy. When no restoration path exists or restoration fails, the isolated section may operate as an intentional island supplied by local DGs. Islanding succeeds if the total DG power within the island meets or exceeds the combined load and losses (assumed at 5% of islanded load). This mode enables continued service to customers even when grid reconnection is not possible, leveraging renewable and dispatchable DG resources.

## C04: Probabilistic Operating Scenarios
A comprehensive scenario matrix constructed by enumerating all possible combinations of discretized wind power output states, solar power output states, and load demand states. Each state's probability is the product of the individual component probabilities. These scenarios feed into the reliability assessment to evaluate expected performance under multi-source uncertainty, avoiding the computational burden of Monte Carlo simulation.

## C05: Sequence-Path Set (SPi)
A set containing every element on the direct series route linking the main substation to a specific bus i. A bus's operational status depends on the availability of components in this trajectory. If any element in the sequence path fails, the bus experiences downtime until the component is repaired. For example, Bus 6's sequence path is: S/S, Line 1, Line 2, Line 3, Line 4, Line 5, Line 6.

## C06: Genetic Algorithm (GA) Optimization
A metaheuristic used to solve the combinatorial reinforcement planning problem. Each chromosome encodes a potential solution as a digital map detailing the placement of NO switches, tie line configurations, and infrastructure upgrades. The decision vector uses binary values for component selection and integer values for investment timing. An external penalty mechanism handles non-compliant solutions. GA processes: initialization, fitness evaluation, ranking, and evolution over generations to minimize the objective function.

## C07: Reliability Indices (SAIDI, ASAI, ENS)
Quantitative measures of distribution system reliability:
- SAIDI (System Average Interruption Duration Index): Average outage duration per customer, calculated as sum(Ui*Ni)/sum(Ni). Target <= 2.5 h/year.
- ASAI (Average Service Availability Index): Fraction of time power is available, calculated as (sum(Ni*NH) - sum(Ui*Ni))/(sum(Ni*NH)).
- ENS (Energy Not Supplied): Total energy not delivered due to interruptions, calculated as sum(La(i)*Ui). Target <= 5 MWh/year per bus.

## C08: Affected Bus Set (ABC)
For each contingency, this set contains only the buses impacted by the specific fault. Protection devices isolate the faulty section, causing sustained interruptions for all downstream loads. The ABC ensures deterministic mathematical formulation aligned with the physical boundaries of the faulted segment, enabling precise quantification of reliability improvements from DG deployment and hierarchical restoration.

## C09: Potential Restoration Solutions per Contingency (PRC)
A set cataloging every possible recovery pathway for the formed island. Each path is assessed via forward/backward sweep load flow to check for feeder overloads, voltage drops, and substation overloading. If at least one path satisfies all operational constraints, restoration is deemed successful. Otherwise, the system transitions to intentional islanding evaluation.

## C10: Forward/Backward Sweep Load Flow
A load flow technique used for every network topology and operational scenario to determine critical system states: voltage levels at buses, power injections at substations, and individual feeder flows. This ensures that no operational thresholds are breached during restoration or islanding assessment, verifying thermal limits, voltage limits, and power balance.
