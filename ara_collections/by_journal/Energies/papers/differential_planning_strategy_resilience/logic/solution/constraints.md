# Boundary Conditions, Assumptions, and Known Limitations

## Boundary Conditions

### Scope Boundaries
1. **Disaster type**: The model "mainly applies to short-term, predictable natural disasters of a single type" (Page 6). Applicable to typhoons, floods, ice disasters, and seismic events with appropriate vulnerability curve parameterization.
2. **Planning horizon**: Pre-disaster hardening decisions are made before the disaster event; post-event restoration (repair, crew dispatch) is not modeled.
3. **Network scale**: Validated on IEEE 33-bus (small) and IEEE 123-bus (medium) distribution networks. Scalability to very large systems (>1000 buses) is not demonstrated.
4. **Time resolution**: Discrete time steps during the disaster period (hours). Sub-hourly dynamics are not modeled.

### Model Boundaries
5. **Line failure model**: Binary state (operational/failed), no partial availability, no degradation or repair during the event.
6. **Hardening levels**: Discrete (3 levels in the study), not continuous. Costs and coefficients are fixed per level.
7. **Ambiguity set**: l1-norm + l-infinity-norm. Other distance measures (KL divergence, Wasserstein) are not evaluated.
8. **EV behavior**: Voluntary V2G participation only. No mandatory dispatch. Initial SOC follows N(0.5, 0.05^2). Departure SOC is unrestricted during disasters.
9. **MEG deployment**: Static (pre-deployed, not mobile during the disaster). One MEG station in the base case.

### Algorithm Boundaries
10. **Solution method**: C&CG with finite-step convergence guarantee (convex polytope ambiguity set). Not applicable to non-convex ambiguity sets.
11. **Pruning criterion**: alpha_cut = 0.95 (fixed). The optimal threshold may vary by system.

## Assumptions

### Physical Assumptions
- A1: Vulnerability curves follow the exponential form in Equation (5) with hardening coefficient alpha_d.
- A2: No line repair during the disaster event.
- A3: Typhoon wind-speed scenarios are adequately represented by G random samples from historical data.
- A4: The initial probability distribution p_{k,0} from historical data is a reasonable center for the ambiguity set.

### Behavioral Assumptions
- A5: EV owners voluntarily participate in V2G when incentives/subsidies are provided.
- A6: EV SOC is constrained within safe operating range; battery degradation is not modeled explicitly.
- A7: Customers participate in demand response with interruptible load ratio 0.05 and transferable load ratio 0.1.

### Data Assumptions
- A8: M historical samples exist for calibration of ambiguity set bounds via Equation (4).
- A9: IEEE 33-bus and 123-bus parameters (line impedances, load profiles, etc.) are representative of real distribution networks.
- A10: The Monte Carlo sampling for fault state generation produces a sufficiently diverse set of failure scenarios.

### Optimization Assumptions
- A11: The tri-level problem is convex in the inner stages (linear constraints, convex ambiguity set).
- A12: The big-M formulation for power flow constraints uses a sufficiently large M for linearization.
- A13: All decision variables are binary for hardening and continuous for power flow.

## Known Limitations

### Technical Limitations
1. **Single disaster type**: Cannot handle concurrent multiple disaster types (e.g., typhoon + flood simultaneously).
2. **No cascading failure model**: The model samples independent line failures but does not explicitly capture cascading outage dynamics (e.g., overload-triggered sequential tripping).
3. **Deterministic EV arrival/departure**: EV connection timing is scenario-dependent but arrival/departure times are treated as known parameters (I^{arr,k,g}_{l,t} and I^{dep,k,g}_{l,t}).
4. **No stochastic EV behavior**: User behavior uncertainty (willingness to participate, actual SOC upon connection) is not modeled beyond the initial SOC normal distribution.
5. **Static MEG deployment**: MEGs are prepositioned and cannot be relocated during the disaster, reducing flexibility.

### Modeling Limitations
6. **Linearity**: The power flow model uses a linearized (distflow) approximation; full AC power flow with losses and voltage drop nonlinearities is not captured.
7. **Discrete hardening levels**: Continuous investment levels might allow finer optimization but are not supported.
8. **Ambiguity set form**: Only l1/l-infinity norm is used; the sensitivity of results to alternative ambiguity set geometries is not studied.
9. **No budget uncertainty**: The hardening budget is assumed known and fixed; uncertainty in budget availability is not considered.

### Validation Limitations
10. **Test system scale**: Primary results on IEEE 33-bus (33 nodes); scalability to very large systems not established.
11. **Real-world validation**: No validation on actual utility distribution network data or historical disaster events.
12. **Sensitivity to pruning threshold**: The alpha_cut = 0.95 value is chosen without a systematic optimization; operators would need to tune it.

### Generalization Limitations
13. **Typhoon-specific parameterization**: Wind-speed vulnerability curves (Equation 5) are typhoon-specific; reparameterization is needed for other disaster types.
14. **Geographic specificity**: The wind-speed data and cost parameters (CNY) reflect Chinese context; transferability to other regions requires recalibration.

## Future Work Directions (from the paper)
1. "The compensation mechanism for EV discharging requires deeper investigation, particularly regarding how pricing strategies and user behavior influence participation willingness under extreme disaster scenarios" (Page 21).
2. "The proposed DDU-based modeling framework is not limited to distribution networks; with appropriate adjustments... it can be generalized to transmission network expansion and differentiated hardening planning" (Page 21).
3. "Future research may also incorporate more sophisticated disaster evolution models—such as the formation mechanisms and propagation characteristics of secondary disasters" (Page 21).
