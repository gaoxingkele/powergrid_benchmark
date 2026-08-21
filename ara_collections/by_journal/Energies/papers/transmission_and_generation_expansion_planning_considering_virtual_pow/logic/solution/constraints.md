# Constraints — Limitations and Assumptions

## Model Limitations

1. **L01**: The implementation of a real case in a transmission line was not part of the scope, so practical deployment challenges (regulatory, operational, communication) are not addressed.
2. **L02**: The AC power flow model uses a linearized AC-OPF approximation with second-order cone constraints, not a full nonlinear AC model. This introduces approximation errors.
3. **L03**: The model assumes that 25% of demand participates in demand response and 30% flexibility contracting in scenario S2.4; these values are assumed, not derived from empirical data.
4. **L04**: Historical data from Spain (2015-2023) is used for both test systems (Garver and IEEE RTS-GMLC), introducing geographic and economic mismatch.
5. **L05**: Only two test systems are used (Garver 6-node and IEEE RTS-GMLC); validation across more diverse systems is not performed.
6. **L06**: The static expansion plan (single-stage investment decisions) is assumed rather than fully dynamic multi-stage planning in some scenarios.
7. **L07**: ESS parameters (50 MW, 85% efficiency, 75 MWh) are fixed across candidate units; real ESS projects have heterogeneous specifications.
8. **L08**: The model does not consider transmission switching, FACTS devices, or other operational flexibility options as alternatives to VPL.
9. **L09**: The net demand model with four stages is a coarse discretization of the load duration curve, potentially missing intra-stage dynamics.
10. **L10**: The DDDRO approach assumes historical data stationarity; non-stationary behavior in renewable generation patterns due to climate change is not addressed.

## Assumptions

1. **A01**: Generation and transmission expansion are co-optimized within a single centralized planning objective (minimize total cost), which may not reflect market-based decentralized planning.
2. **A02**: Two types of demand exist: (1) centralized planning demand and (2) demand served by VPP-contracted generation. This division is assumed rather than empirically derived.
3. **A03**: Net demand = demand minus VRE injection. VRE injection is considered non-dispatchable with zero marginal cost.
4. **A04**: ESS round-trip efficiency remains constant at 85% across all operating conditions.
5. **A05**: Candidate line circuits have no more than `Line_MaxCirc` circuits per corridor (fixed maximum).
6. **A06**: The perpetuity financial model makes investment projects with different useful lives comparable by extending life to infinity.
7. **A07**: Reserve capacity contracted from VPPs is sufficient to handle all unforeseen fluctuations (no reliability constraints beyond reserve contracting).
8. **A08**: The discount rate dr is constant over the planning horizon.
9. **A09**: Flexibility contracts (upward/downward) are priced at constant rates OC_FxU and OC_FxD per MWh.
10. **A10**: The DDDRO confidence uncertainty set with dual norms (L1, L∞) adequately captures all relevant probability distributions.
11. **A11**: The planning horizon is divided into equal time periods (t), and each period has the same set of demand stages.
12. **A12**: VPL binary variables (charge/discharge status) are determined based on net demand stage and power flow direction, as described in Table 2.
