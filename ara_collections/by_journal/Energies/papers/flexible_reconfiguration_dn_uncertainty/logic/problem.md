# Problem Formulation

## Observations

1. **High renewable penetration increases operational uncertainty**: Distribution networks with high penetration of wind and solar generation face significant uncertainty due to the intermittent nature of these resources. Wind speed follows a Weibull probability distribution, while solar irradiance follows a Beta distribution.

2. **Load variability compounds operational difficulty**: Customer load demand varies throughout the day and follows a normal (Gaussian) probability distribution, adding another layer of uncertainty to distribution network operation.

3. **Dynamic reconfiguration outperforms static approaches**: Most existing reconfiguration methods use static (single-period) or decomposition (multi-period) approaches that do not fully capture the time-varying nature of loads and renewable generation.

4. **Existing DR methods often neglect uncertainty**: Many dynamic reconfiguration studies either ignore uncertainty altogether or use simplified deterministic models for renewable generation and load.

5. **Complete dynamic reconfiguration has high computational burden**: Full 24-hour dynamic reconfiguration requires solving a large combinatorial optimization problem with many variables across multiple time periods.

6. **Metaheuristic algorithms are widely used but solution quality varies**: The choice of optimization algorithm significantly impacts the quality of the reconfiguration solution, and there is no guarantee of global optimality.

## Gaps

1. **Lack of integrated uncertainty-aware DR framework**: Few studies combine scenario-based uncertainty modeling with complete dynamic reconfiguration (considering all 24 hourly periods simultaneously).

2. **Incomplete cost objective functions**: Most DR formulations minimize power losses and switching costs but neglect voltage deviation costs, renewable generation costs, and upstream power purchase costs in a unified framework.

3. **Limited validation on real-world systems**: Many DR methods are validated only on small test systems (e.g., IEEE 33-bus) without demonstration on larger, realistic distribution networks.

4. **COA not previously applied to DR**: The Coati Optimization Algorithm, a relatively new metaheuristic, has not been explored for distribution network reconfiguration problems.

5. **Reliability impact of DR not well-characterized**: The effect of dynamic reconfiguration on system reliability metrics (e.g., EENS) is underexplored in the literature.

6. **Comparison with alternative metaheuristics insufficient**: Few studies provide head-to-head comparisons of COA with established algorithms like PSO specifically for the DR problem.

## Key Insight

A flexible, complete dynamic reconfiguration framework that considers load and renewable generation uncertainty through a scenario-based probabilistic approach, solved using the Coati Optimization Algorithm, can minimize the total operational cost of distribution networks by jointly optimizing power losses, voltage deviation, switching operations, upstream power purchases, and renewable generation costs on an hourly basis.

## Assumptions

1. **Probability distributions are known**: Wind speed follows Weibull distribution, solar irradiance follows Beta distribution, and load follows Normal distribution, with parameters derived from historical data.

2. **Scenario independence**: Combined load-wind-PV scenarios are formed by multiplying individual scenario probabilities, assuming independence among the three uncertain quantities.

3. **Fixed power factor for DGs**: Wind-DGs operate at a lagging power factor of 0.85, and PVs operate at unity power factor.

4. **Remote-controlled switches (RCSs)**: The network is equipped with RCSs that enable remote switching operations without manual intervention.

5. **Maximum switching limit**: Each RCS is limited to a maximum of 4 switching operations per 24-hour period.

6. **Radial topology constraint**: The network must maintain a radial structure at all times during reconfiguration.

7. **Constant energy prices**: Electricity prices from the upstream network, PV-DG, and wind-DG are known and follow the profiles shown in the paper.

8. **Voltage limits**: Bus voltages must remain within 0.95-1.05 p.u. at all times.
