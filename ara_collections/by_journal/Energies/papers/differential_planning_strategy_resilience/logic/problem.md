# Problem Formulation

## Observations

### O1: Extreme natural disasters cause severe power outages in distribution networks.
- June 2020: Guangxi, China faced strong winds; >250,000 households experienced power outages; >100 distribution lines at 10 kV damaged [1].
- February 2021: Texas snowstorm; ~5 million users experienced power outages [2,3].
- Extreme weather disasters are low-frequency, high-impact events causing large-scale, long-term outages and cascading failures.

### O2: Line hardening reduces but does not eliminate failure probability under extreme weather.
- Reference [7] points out that hardening strategies can affect line failure probability but cannot reduce it to zero.
- "Even after hardening, there remains a certain probability of failure under high disaster intensity" (Page 4).

### O3: The failure probability of distribution lines during extreme weather depends on the hardening decision (decision-dependent uncertainty / DDU).
- "At the same disaster scenarios, the failure probability decreases gradually from the un-hardened level to higher hardening levels" (Page 3).
- "At the same hardening level, the failure probability increases exponentially with disaster intensity" (Page 3).

### O4: Existing models predominantly treat uncertainty as exogenous, ignoring the decision-dependent nature of failure probabilities.
- "Most existing studies on uncertainty consider exogenous uncertainty, where decision variables have no direct relationship with uncertainty" (Page 2).
- DDU is a type of endogenous uncertainty where the distribution of model parameters depends on decisions [17,18].

### O5: Distributionally robust optimization (DRO) balances risk and performance better than robust optimization or stochastic programming alone.
- "Distributionally robust optimization provides protection against distributional uncertainty while avoiding excessive conservatism" (Page 3).
- DRO uses norm-bounded ambiguity sets (l1-norm and l-infinity-norm) around the initial probability distribution.

### O6: The Sobol' global sensitivity analysis method decomposes output variance into contributions from individual inputs and their interactions.
- "GSA evaluates the overall influence of input variables while accounting for their interactions and nonlinear effects" (Page 10).
- First-order index Si measures direct contribution; total-effect index STi captures both direct and interaction effects.

## Gaps

### G1: Full-level hardening (binary yes/no) models are overly conservative and economically suboptimal.
- "Compared with full-level planning, differential planning improves the overall system resilience in a targeted treatment manner" (Page 2).
- Conventional hardening models treat all hardened lines uniformly, ignoring graduated hardening levels.

### G2: Integration of distributionally robust optimization with decision-dependent uncertainty under extreme natural disasters is lacking in the literature.
- "The integration of distributionally robust optimization with decision-dependent uncertainty under extreme natural disasters is still lacking" (Page 3).

### G3: Existing models lack interpretability regarding which reinforcement measures contribute most to system resilience.
- The paper identifies that global sensitivity analysis provides "a systematic and quantitative framework for evaluating the contribution and interaction of different reinforcement strategies" (Page 12).

### G4: The computational complexity of solving tri-level DRO with DDU and scenario-dependent operation variables is prohibitive without tailored solution algorithms.
- "The number of fault states has a significant impact on the difficulty and computation time of solving the system" (Page 9).
- Fault-state pruning and customized C&CG are needed to achieve tractability.

## Key Insight

When line hardening decisions influence the failure probability of those lines (DDU), the uncertainty set itself becomes decision-dependent. This creates a tri-level optimization structure (hardening -> worst-case probability -> operation) that can be solved via a customized C&CG algorithm with fault-state pruning. The Sobol' global sensitivity analysis then reveals the marginal resilience contribution of each hardened line, enabling planners to prioritize investments where they yield the greatest resilience improvement per unit cost.

## Assumptions

1. **Single disaster type per planning horizon**: The model "mainly applies to short-term, predictable natural disasters of a single type" (Page 6).
2. **No line repair during disaster**: "In this study, line repair after failure is not considered" (Page 5).
3. **Voluntary EV participation**: EV owners choose to participate in V2G, incentivized by subsidies; SOC is constrained within safe operating range.
4. **Known vulnerability curves**: The relationship between wind speed, hardening level, and failure probability follows the exponential model in Equation (5).
5. **Initial probability distribution available**: Historical data M samples exist to calibrate the l1/l-infinity ambiguity set bounds via the formula in Equation (4).
6. **Monte Carlo sampling sufficiently represents disaster scenarios**: G wind speed scenarios are generated through random sampling from historical data.
7. **Disaster coverage is wide-area**: Typhoon coverage is simulated as a wide-area event affecting multiple lines simultaneously.
8. **MEG deployment budget is fixed and known**: Total MEG budget Delta_MEG is set as a constraint.
