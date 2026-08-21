# Claims

## C01: Dispatchable EV-fleet storage smooths DG-driven voltage deviation by charging at surplus and discharging at deficit
- **Statement**: In a DG-penetrated radial distribution feeder, siting dispatchable EV-fleet ("shared") storage at network-selected nodes suppresses local voltage deviation, because the storage charges to absorb surplus injection when DG output is high and discharges to compensate when DG output is low, holding node voltage nearer its reference across the diurnal cycle rather than letting DG fluctuation propagate to the voltage.
- **Conditions**: IEEE 33-node radial test feeder, single case study; DG fixed at wind nodes 20/14 and PV nodes 9/30; at most 2 nodes host EVS storage; MOPSO-selected sites (nodes 13 and 33 in the reported run); SOC held within its band during the high-DG window (~10:00–15:00). Untested boundary: only one topology and one load profile — deviation magnitudes at other nodes, feeders, or penetration levels are not established.
- **Sources**: ["9.4% / 40% ← evidence/figures/figure7.md (Fig 7, §5, p.9) «the voltage deviation of node 16 in scenario 3 is 9.4% compared with that of node 16 in scenario 1, and the voltage deviation of node 16 in scenario 2 compared with node 16 in scenario 1 is 40%» [result]", "29.5% / 21.5% ← evidence/figures/figure9.md (Fig 9, §5, p.11) «the average voltage of node 13 is reduced by 29.5% compared to the level before the consideration of EVS, and the average voltage of node 33 is reduced by 21.5% compared to the level before the consideration of EVS» [result]"]
- **Status**: supported
- **Falsification criteria**: Observe a DG-penetrated feeder in which adding SOC-band-constrained EV-fleet storage at optimizer-selected nodes leaves node voltage deviation unchanged or worse than the no-storage case across the diurnal cycle — i.e., the charge-at-surplus / discharge-at-deficit action fails to track DG and does not pull voltage toward its reference.
- **Proof**: [E01, E02, E03, E04]
- **Evidence basis**: Table 1 Target 1 (voltage) improves with storage vs DG-only in the operational sense; Figure 7 shows scenario-3 voltage surface smoother than scenario-2; Figure 8 shows the charge/discharge–SOC mechanism operating over 24 h; node-16 deviation drops from 40% (sc2) to 9.4% (sc3), and average voltage at the two sited nodes 13/33 falls 29.5%/21.5% vs the no-EVS case.
- **Tags**: EV storage, voltage stability, DG uncertainty, distribution network

## C02: EV-fleet shared storage can substitute for equal-role dedicated storage, trading committed capacity for better loss/voltage
- **Statement**: A mobile EV-fleet shared-storage resource can substitute for an equal-role dedicated stationary storage bank in a DG-rich feeder, delivering at least comparable voltage stabilization and lower network loss, because the fleet's charge/discharge availability coincides temporally with the DG output it must offset; the substitution trades a higher committed storage-capacity objective for better operational voltage and loss outcomes.
- **Conditions**: scenario 3 (DG + EVS storage) vs scenario 4 (DG + normal storage) on the 33-node case; "better/comparable" is measured only on the paper's three objective values (f1 voltage, f2 loss, f3 capacity); excludes lifecycle/degradation cost and EV-owner availability risk. Single case study.
- **Sources**: ["Target1 sc3 0.36345 < sc4 0.36784 ← evidence/tables/table1.md (Table 1, §5, p.9) «| Target 1 | 0.319736 | 0.369132 | 0.36345 | 0.36784 |» [result]", "Target2 sc3 1.170143 < sc4 1.268574 ← evidence/tables/table1.md (Table 1, §5, p.9) «| Target 2 | 1.657225 | 0.947059 | 1.170143 | 1.268574 |» [result]", "Target3 sc3 2.565299 > sc4 2.325875 ← evidence/tables/table1.md (Table 1, §5, p.9) «| Target 3 | / | / | 2.565299 | 2.325875 |» [result]"]
- **Status**: supported
- **Falsification criteria**: A DG-rich case in which equal-role dedicated stationary storage matches or beats EV-fleet shared storage on BOTH voltage fluctuation and network loss at equal or lower committed capacity — showing the temporal-alignment substitution advantage is illusory.
- **Proof**: [E01]
- **Evidence basis**: Table 1: scenario 3 beats scenario 4 on Target 1 (voltage) and Target 2 (loss) but requires larger Target 3 (capacity) — a genuine trade-off, not a free lunch.
- **Dependencies**: C01
- **Tags**: shared energy storage, storage substitution, multi-objective trade-off

## C03: A KDE + Frank-copula scenario generator preserves wind–solar joint dependence that independent-marginal sampling discards
- **Statement**: Fitting DG marginals by non-parametric kernel density estimation and coupling them with a Frank copula reproduces the negative correlation and complementarity between wind and PV output, so a reduced representative scenario set retains both the randomness and the joint dependence structure — information that independent-marginal or reliability-only sampling omits.
- **Conditions**: wind and PV each at two fixed nodes on the case system; Frank copula selected specifically because DG output "usually has a negative correlation and complementarity"; 500 generated scenarios reduced to 5 weighted representatives; validated qualitatively via scenario spread (Figures 4–5), not against a held-out goodness-of-fit statistic.
- **Sources**: ["500 ← logic/solution/method.md / §5 (p.7) «500 wind–solar complementary scenarios are generated» [input]", "5 reduced-scenario probabilities 0.214/0.196/0.222/0.198/0.17 ← evidence/figures/figure4.md (Fig 4 legend, §5, p.7) «Scenario 1 (0.214), Scenario 2 (0.196), Scenario 3 (0.222), Scenario 4 (0.198), Scenario 5 (0.17)» [result]"]
- **Status**: supported
- **Falsification criteria**: Show that copula-free independent-marginal sampling reproduces the same wind–PV joint dependence and scenario envelope, or that the Frank-copula scenarios fail to preserve the observed wind–PV anti-correlation — i.e., the copula adds no correlation information over independent sampling.
- **Proof**: [E05]
- **Evidence basis**: Figures 4 and 5 show five reduced scenarios retaining a spread/envelope (not a single mean curve), with wind ragged and PV single-humped (complementary shapes); text states the generated scenarios "more accurately generate the randomness and correlation of the DG unit output".
- **Tags**: copula, scenario generation, kernel density estimation, renewable uncertainty

## C04: Convolutional feature extraction before a bidirectional LSTM lowers EV-cluster state prediction error versus either component alone
- **Statement**: Prepending convolutional feature extraction to a bidirectional LSTM lowers the prediction error of EV-cluster state variables (arrival time, departure time, initial SOC) relative to a standalone CNN or a standalone Bi-LSTM, because convolution compresses local temporal features while the bidirectional recurrent pass conditions each estimate on both past and future context — neither of which the single components supply together.
- **Conditions**: 40-sample EV test set on the case fleet; error reduction reported as relative percentages against ordinary CNN and Bi-LSTM baselines; single dataset, no cross-validation reported; three predicted quantities only.
- **Sources**: ["10.2% vs CNN, 8.3% vs Bi-LSTM ← evidence/figures/figure6.md (§6 conclusion (2), p.11) «can further reduce the data error of EV, which is 10.2% higher than the ordinary CNN method and 8.3% higher than that of the Bi-LSTM algorithm» [result]"]
- **Status**: supported
- **Falsification criteria**: An EV-state prediction task in which CNN-BiLSTM error is equal to or larger than the better of standalone CNN or standalone Bi-LSTM — showing the combination provides no reduction over its components.
- **Proof**: [E06]
- **Evidence basis**: Figure 6 (a/b/c) shows the CNN-BiLSTM curve tracking the True-value curve more closely than CNN or BiLSTM across arrival time, departure time, and initial SOC; conclusion quantifies 10.2% / 8.3% error reduction.
- **Tags**: CNN-BiLSTM, EV prediction, uncertainty reduction, deep learning

## C05: A three-objective voltage/loss/capacity formulation exposes trade-offs a single-objective model cannot represent
- **Statement**: Casting ADN storage planning as the simultaneous minimization of node voltage fluctuation, network loss, and storage capacity exposes conflicts among these objectives — a configuration better on voltage and loss can demand more committed storage capacity — that a single-objective formulation cannot express, so the multi-objective model yields a more feasible planning scheme.
- **Conditions**: three objectives f1 (voltage fluctuation, Eq.1), f2 (network loss, Eq.2), f3 (storage capacity, Eq.3); solved with MOPSO on the 33-node case; the trade-off is evidenced by the scenario-3 vs scenario-4 objective values; "feasibility" is the paper's qualitative claim, not a separately quantified metric.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A single-objective ADN storage-planning optimum that is Pareto-equivalent to the multi-objective solution on all three objectives simultaneously — showing the added objectives are redundant and contribute no feasibility.
- **Proof**: [E01, E04]
- **Evidence basis**: Table 1 shows the objectives moving in opposition across scenarios 3/4 (better voltage+loss vs lower capacity), which a single scalar objective could not have surfaced; Figure 9 shows the resulting concrete siting scheme (nodes 13, 33).
- **Dependencies**: C01, C02
- **Tags**: multi-objective optimization, siting and sizing, MOPSO, feasibility
