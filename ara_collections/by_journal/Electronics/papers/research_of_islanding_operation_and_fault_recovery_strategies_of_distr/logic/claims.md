# Claims

Falsifiable claims distilled from Yang et al., *Electronics* 2023, 12, 4230. Exact run numbers live
in `evidence/`; each claim's `Proof` points to `logic/experiments.md` (E01–E11).

## C01: Weight-driven partition makes critical-load islanding emerge from the objective, not from manual assignment
- **Statement**: In a DG-rich radial distribution network disconnected from the upstream grid,
  casting island division as weighted load-shedding minimization — with importance weights spanning
  orders of magnitude and explicit DG-membership and radiality constraints — drives every DG and
  every high-weight load into a self-supplying island, so coverage of critical loads is an emergent
  property of the weight structure rather than a hand-crafted island assignment.
- **Conditions**: Radial network whose aggregate DG capacity can carry the important loads (improved
  IEEE 33-node, 4 DGs totaling 3200 kW); extreme fault regime (upstream substation breaker trip plus
  an internal line fault); weight ratio 100/10/1 across load levels. Meshed networks and
  DG-deficient systems untested.
- **Sources**:
  - 3200 kW (sum 500+700+1000+1000) ← Table 1, §5.1 p.11 «6 Wind or photovoltaic power 500 0.85 / 13 Energy storage 700 0.9 / 24 Diesel generator 1000 0.8 / 31 Diesel generator 1000 0.9» [input]
  - 100/10/1 ← Table 2, §5.1 p.12 «Level 1 100 … Level 2 10 … Level 3 1» [input]
- **Status**: supported
- **Falsification criteria**: A solved instance in which the partition strands a DG outside every
  island, or leaves a level-1 (weight-100) load unsupplied despite feasible island capacity, would
  refute the mechanism.
- **Proof**: [E01]
- **Evidence basis**: Figure 6 — after the extreme fault (breaker trip + S28), the model splits the
  network into exactly two islands: Island 1 with two DGs and 12 loads, Island 2 with two DGs and
  11 loads; all 4 DGs and all important loads are inside islands. System data in Table 1/Table 2,
  topology in Figure 1.
- **Tags**: islanding, island division, load weight, radiality, distribution network

## C02: Distribution-based sampling plus clustering reduction compresses renewable uncertainty into a tractable, structure-preserving scenario set
- **Statement**: Representing wind/PV uncertainty by parametric distributions fitted to measured
  typical-day profiles (Weibull wind speed, normally distributed PV prediction error), then
  generating a large Latin-hypercube sample and reducing it by K-means clustering into a few
  weighted representative scenarios, preserves the ensemble's envelope and fluctuation structure
  while shrinking the stochastic program enough to re-solve every scheduling period.
- **Conditions**: Uncertainty expressible as random perturbation around a typical-day base profile
  (Hubei microgrid measured data, 96 points/day at 15-min intervals); sample scale 500 reduced to
  5 scenarios, augmented by two extreme (max-wind/min-PV, min-wind/max-PV) scenarios.
  Multi-day or spatially correlated weather regimes untested.
- **Sources**:
  - 500 ← §5.1 p.12 «500 distinct wind speed curves are generated to encapsulate the inherent variability of wind speeds» [input]
  - 5 ← §5.1 p.12 «these 500 wind speed curves are adeptly condensed into 5 representative curves using the restoration technique» [input]
  - 96 / 15 min ← §5.1 p.12 «wind speed readings are precisely captured at 15 min intervals, summing up to 96 data points for that day» [input]
- **Status**: supported
- **Falsification criteria**: Realized wind/PV output frequently falling outside the generated
  scenario envelope, or the 5-scenario (plus extremes) optimization producing materially different
  islanding/recovery decisions than the full 500-scenario problem, would refute the reduction's
  adequacy.
- **Proof**: [E02]
- **Evidence basis**: Figures 2–5 — the 500-curve generated ensembles and the 5-curve reduced sets
  for wind and PV; the reduced curves track the base profile and span the ensemble spread.
- **Tags**: uncertainty, scenario generation, Latin hypercube sampling, K-means, Weibull, photovoltaic

## C03: Short-horizon rolling re-optimization absorbs renewable prediction error before it violates island safety limits
- **Statement**: Driving island operation by rolling optimization — solving a joint multi-period
  model each scheduling interval but committing only the next step, with feedback correction — over
  the weighted scenario set keeps island node voltages inside the safety band and important loads
  continuously supplied across substantial renewable penetration, random output scenarios, and
  different storage initial states, because each short-horizon re-solve exploits the higher accuracy
  of short-term prediction and corrects drift before it accumulates.
- **Conditions**: Islands anchored by dispatchable DGs (diesel + storage) with wind or PV at one
  node; renewable share up to the tested maxima (34.09% wind, 48.65% PV); 5 analyzed periods,
  20 random wind scenarios; storage initial energy 50% and 80% of rated; scheduling interval
  ΔT = 15 min. Higher penetration, longer autonomy, or islands without dispatchable backbone
  untested.
- **Sources**:
  - 34.09% / 48.65% ← Abstract p.1 «the node voltage consistently remains between 1.08 pu and 1.1 pu when new energy achieves up to 34.09% and 48.65%» [result]
  - 20 ← §5.2 p.17 «randomly generates 20 wind power scenarios» [input]
  - 50% / 80% ← Abstract p.1 «when the initial energy levels of the storage are at 50% and 80%» [input]
  - ΔT = 15 min ← §2.1 p.4 «generally taking ∆T = 15 min» [input]
- **Status**: supported
- **Falsification criteria**: An island run inside the tested regime (renewable share ≤ the tested
  maxima, dispatchable backbone present) where rolling operation lets node voltage leave the
  allowed band or forces shedding of an important load would refute the claim.
- **Proof**: [E03, E04, E05, E06]
- **Evidence basis**: Figures 7–10 (per-period voltages and DG/load/loss balances, wind and PV
  cases: voltages within [1.0811, 1.1] pu), Figure 11 (20-scenario box plots, all within
  [1.08, 1.1] pu), Figures 12–13 (Island 1 at 50%/80% initial storage, max voltage 1.093/1.094 pu,
  losses ≈0.22–0.26% of load). Exact per-period numbers are filed with those figures.
- **Dependencies**: C02
- **Tags**: rolling optimization, feedback correction, voltage security, renewable penetration, energy storage

## C04: Post-restoration network reconstruction converts topology freedom into lower loss and higher minimum voltage
- **Statement**: Once the upstream grid returns, re-optimizing the switch topology (network
  reconstruction) inside the weighted recovery objective consistently reduces line active-power
  loss and raises the minimum node voltage relative to recovery without reconstruction, across
  structurally different fault placements — reconfiguration re-routes flow onto paths with better
  impedance and voltage support while radiality is preserved.
- **Conditions**: Improved IEEE 33-node system; three tested fault cases (S28+DG3, S28 alone,
  S9+S22); recovery solved as the scenario-weighted second-order cone program; gain magnitude
  depends on remaining DG availability (see C06). Larger systems and simultaneous multi-area
  faults beyond two branches untested.
- **Sources**:
  - 11.9% / 13.6% / 14.2% ← Abstract p.1 «the system shows significant power loss reductions of approximately 11.9%, 13.6%, and 14.2% in three respective cases» [result]
- **Status**: supported
- **Falsification criteria**: A tested fault case in which the reconstructed topology yields higher
  network loss or a lower minimum node voltage than the unreconstructed recovery would refute the
  claim.
- **Proof**: [E07, E08, E09]
- **Evidence basis**: Tables 3–5 (loss 49.3339→43.4675, 22.2987→19.2725, 39.5470→33.9117 kW; min
  voltage +0.0046, +0.0088, +0.0046 pu) with reconfigured topologies in Figures 14, 16, 18 and
  node-voltage before/after profiles in Figures 15, 17, 19.
- **Tags**: fault recovery, network reconstruction, power loss, minimum voltage, SOCP

## C05: Propagating island-stage supply history into the recovery weight removes satisfaction blind spots that a static weight leaves behind
- **Statement**: Adding to the static importance weight two penalty terms — one for changes in a
  node's island membership across scheduling periods, one for periods with no supply — makes the
  recovery optimization re-energize loads that endured intermittent supply during islanding,
  whereas the same recovery driven by the static weight alone (β = α) leaves such a node unpowered
  because switching cost then outweighs its restoration value. Coupling the two fault-handling
  stages through the load weight is what carries the island-stage experience into the recovery
  decision.
- **Conditions**: Recovery after prolonged islanded operation (20 h tested) with fluctuating wind
  driving island-membership churn at a boundary node; single tested fault (S28, wind at node 6);
  penalty coefficients ξ1, ξ2 are positive constants whose values are not specified in the paper.
- **Sources**:
  - 20 h ← §5.3.4 p.23 «assuming that the superior power grid resumes power supply within 20 h, that is, the distribution grid has to operate in isolation for 20 h» [input]
- **Status**: supported
- **Falsification criteria**: A membership-churn case where the history-aware weight fails to
  restore an intermittently supplied node that the static weight does restore, or where both weight
  designs produce identical restoration sets despite island-scheme changes, would refute the
  mechanism.
- **Proof**: [E10]
- **Evidence basis**: Figure 20 vs Figure 16 — under the comparison method (β = α) node 28 does not
  receive power; under the proposed β (Eq. 36) it is restored. The paper attributes this to the
  comparison method assigning excessive weight to switch actions and neglecting intermittent-supply
  history.
- **Dependencies**: C04
- **Tags**: load weight, user electricity satisfaction, stage coupling, fault recovery, ablation

## C06: Remaining dispatchable DG capacity conditions how much reconstruction can recover in economy and voltage
- **Statement**: The loss and voltage benefits achievable by recovery-stage reconstruction scale
  with the dispatchable DG capacity still in service: losing a DG together with a line fault leaves
  the reconstructed network with more than twice the loss and a visibly lower voltage floor than
  the same line fault alone, so DG placement/allocation acts as a lever on recovery-stage economy
  and stability rather than a fixed background parameter.
- **Conditions**: Same system and fault line (S28) contrasted with and without the DG3 outage
  (diesel, 1000 kW at node 24); single-DG difference; other DG mixes, sizes, and locations untested.
- **Sources**:
  - 1000 kW / node 24 ← Table 1, §5.1 p.11 «24 Diesel generator 1000 0.8» [input]
- **Status**: supported
- **Falsification criteria**: A case pair where removing an in-service DG from the recovery problem
  leaves post-reconstruction losses and minimum voltage essentially unchanged (or improved) would
  refute the claim.
- **Proof**: [E07, E08]
- **Evidence basis**: Table 3 vs Table 4 — with DG3 failed, post-reconstruction loss is 43.4675 kW
  and min voltage 1.0729 pu; with DG3 healthy, 19.2725 kW and 0.9824 pu (different pre-fault
  baselines; the paper's own reading: «the integration of DG3 can significantly reduce network
  losses in the distribution system and help to increase the minimum voltage of the nodes», §5.3.2).
- **Dependencies**: C04
- **Tags**: DG allocation, fault recovery, network loss, voltage support

## C07: The optimization strategy is executable as a real-time hardware control loop
- **Statement**: The islanding-operation/fault-recovery strategy ports from offline optimization to
  a closed hardware loop: a DSP controller reading power measurements from a real-time simulated
  network detects the fault, issues switch commands that reproduce the model's island partition,
  and the resulting islands hold voltage magnitude, phase spread, and frequency within stable
  operating ranges — indicating the optimizer's outputs are consumable as real-time control
  decisions, not only planning results.
- **Conditions**: OPAL-RT semi-physical platform standing in for the physical network; PV connected
  at node 6; S28 fault; three scheduling periods observed via oscilloscope with node 24 as phase
  reference. Not a field deployment; control latency and comms limits are not quantified in the
  paper.
- **Sources**:
  - 1.082–1.099 ← §6 p.25 «the voltages of each node range approximately from 1.082 to 1.099» [result]
  - −10.09° to 0° ← §6 p.25 «The phase angles of the nodes vary between −10.09 degrees and 0 degrees» [result]
  - ≈50 Hz ← §6 p.25 «the voltage frequency nearing 50 Hz is another indicator of the operational stability of Island 2» [result]
- **Status**: supported
- **Falsification criteria**: A semi-physical run in which the DSP-executed partition diverges from
  the model's partition, or islanded waveforms exhibit voltage/frequency excursions outside stable
  ranges, would refute the claim.
- **Proof**: [E11]
- **Evidence basis**: Figure 21 (OPAL-RT + DSP framework), Figures 22–24 (oscilloscope node-voltage
  waveforms for periods 1–3; partition matches Figure 6).
- **Dependencies**: C01, C03
- **Tags**: semi-physical simulation, OPAL-RT, DSP, hardware-in-the-loop, real-time control
