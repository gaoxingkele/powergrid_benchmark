# Constraints, Assumptions, and Limitations

## Boundary conditions (model + case)
- EVS SOC dynamics follow Eq. (6); end-of-horizon SOC must equal the expected value
  $S_T^{EVS} = S_{exp}^{EVS}$ (Eq. 7).
- SOC bounded: $S_{min}^{EVS} \le S_t^{EVS} \le S_{max}^{EVS}$ (Eq. 8); numeric bounds
  Not specified in paper (allowable ranges cited to Ref. [33]).
- Charge/discharge power bounded: $0 \le P_{cha} \le P_{cha,max}$, $0 \le P_{dis} \le P_{dis,max}$
  (Eq. 9); numeric bounds Not specified in paper.
- Siting bounds (§5): connectable node index range 2–33; at most 2 nodes may host EVS storage;
  maximum installed power 400 kW.
- Horizon: T = 24 h; objectives evaluated over all $N_{bus}$ nodes and all branches $E_{line}$.
- Case fixture: IEEE 33-node ADN, total load 3715 kW + j2300 kvar, rated voltage 12.66 kV;
  wind turbines fixed at nodes 20 and 14, PV units fixed at nodes 9 and 30 (DG siting is an
  input, not a decision variable).

## Assumptions
- A1: Each EV type has a fixed arrival/departure time $T_{arrive}/T_{leave}$ and initial SOC $S_0$
  drawn from the Table A1 distributions (normal for times, uniform for SOC and fleet counts);
  charging/discharging status "is determined using historical data" (§4.2).
- A2: Wind–solar joint output is adequately described by a Frank copula over KDE-fitted marginals,
  justified by DG's "negative correlation and complementarity" (§3); no goodness-of-fit comparison
  against other copula families is reported.
- A3: The multi-type EV cluster at a station (EVS) can be aggregated into a single dispatchable
  storage device (Eqs. 6–9) — individual EV behavior, owner willingness, and degradation are not
  modeled.
- A4: 500 generated wind–solar scenarios can be reduced to a small weighted representative set
  (5 shown per resource) without losing the randomness/correlation structure.
- A5: The IEEE 33-node system (parameters per Ref. [18]) is representative for validating the
  planning method.

## Known limitations (stated by the paper)
- **MOPSO efficiency**: "the solution efficiency of MOPSO is slow and needs to be further
  improved" (§5, p.11); improving it is future work (§6).
- **EV queuing ignored**: "the model does not take into account more practical issues such as EV
  queuing times, which will be left for further study" (§5, p.11); EV path planning combined with
  ADN networks is also deferred to future work (§6).

## Limitations evident from the artifact (not stated as such by the paper)
- Single test system, single load profile, one DG placement — no sensitivity across topologies or
  penetration levels.
- No released code or numeric dataset ("The data presented in this study are available in this
  article" — Data Availability Statement); hardware, solver settings, seeds, and hyperparameters
  are all unreported, so results are not independently reproducible.
- The "improved" MOPSO variant named in the abstract is never specified in the body.
- Storage-capacity objective f3 is compared only between scenarios 3 and 4; no monetary cost model
  (lifecycle, degradation, tariff) is included despite the economic motivation.
- Table 1's caption says "three scenarios" while the body reports four columns (transcription note
  in evidence/tables/table1.md).
- Scenario-reduction algorithm is cited ([30,34,35]) but not identified; KDE kernel and bandwidth
  are Not specified in paper.
