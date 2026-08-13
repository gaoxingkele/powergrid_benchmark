# Related Work — mintou_p1 (Operating-State Retrieval Framework and Curtailment-Risk Benchmark)

Prepared 2026-07-16 for the IEEE Access submission. Every DOI below was verified against the
Crossref REST API (`api.crossref.org/works/<DOI>`): the Crossref-returned title, authors, venue,
and year match the entry as listed. No unverified citation appears in this file or in the
manuscript. Descriptions marked "(metadata + domain knowledge)" were written from Crossref
metadata plus knowledge of the paper because Crossref deposited no abstract for that record.

Three threads structure the review, mirroring the paper's three contributions: (a) the benchmark
fills a gap in the curtailment literature, (b) the framework evaluation fills a gap in the
retrieval/analogue literature, and (c) the evaluation protocol applies lessons the forecasting
methodology literature has repeatedly taught.

---

## Thread A — Forecasting and assessment of renewable curtailment and accommodation

The curtailment literature is rich in retrospective quantification and thin in operational
prediction, and it publishes essentially no reusable evaluation assets.

1. **Bird, L.; Lew, D.; Milligan, M.; Carlini, E.M.; Estanqueiro, A.; Flynn, D.; Gomez-Lazaro, E.;
   Holttinen, H.; Menemenlis, N.; Orths, A.; Børre Eriksen, P.; Smith, J.C.; Soder, L.;
   Sorensen, P.; Altiparmakis, A.; Yasuda, Y.; Miller, J.**
   Wind and solar energy curtailment: A review of international experience.
   *Renewable and Sustainable Energy Reviews* 2016, 65, 577–586.
   DOI: 10.1016/j.rser.2016.06.082 — VERIFIED.
   The canonical cross-system review of curtailment levels, causes (transmission constraints,
   oversupply, stability limits), and mitigation practice across the US, Europe, and Asia.
   Entirely retrospective; no forecasting task, dataset, or protocol. (metadata + domain knowledge)

2. **Luo, G.; Li, Y.; Tang, W.; Wei, X.**
   Wind curtailment of China's wind power operation: Evolution, causes and solutions.
   *Renewable and Sustainable Energy Reviews* 2016, 53, 1190–1201.
   DOI: 10.1016/j.rser.2015.09.075 — VERIFIED.
   Driver analysis of China's Three-North wind curtailment: grid bottlenecks, inflexible thermal
   mixes, resource/load geography, institutional factors. Policy-oriented; nothing predictive or
   reusable as an evaluation asset. (metadata + domain knowledge)

3. **Yasuda, Y.; Bird, L.; Carlini, E.M.; Eriksen, P.B.; Estanqueiro, A.; Flynn, D.; Fraile, D.;
   Gómez Lázaro, E.; Martín-Martínez, S.; Hayashi, D.; Holttinen, H.; Lew, D.; McCam, J.;
   Menemenlis, N.; Miranda, R.; Orths, A.; Smith, J.C.; Taibi, E.; Vrana, T.K.**
   C-E (curtailment – Energy share) map: An objective and quantitative measure to evaluate wind
   and solar curtailment. *Renewable and Sustainable Energy Reviews* 2022, 160, 112212.
   DOI: 10.1016/j.rser.2022.112212 — VERIFIED.
   Proposes an annual-granularity cross-system curtailment metric (curtailment rate vs. VRE energy
   share). Ex-post assessment; no operational early-warning dimension. (metadata + domain knowledge)

4. **Frew, B.; Sergi, B.; Denholm, P.; Cole, W.; Gates, N.; Levie, D.; Margolis, R.**
   The curtailment paradox in the transition to high solar power systems.
   *Joule* 2021, 5, 1143–1167. DOI: 10.1016/j.joule.2021.03.021 — VERIFIED.
   Capacity-expansion and production-cost modeling showing curtailment can be economically optimal
   at high solar shares. Planning-scenario simulation, not operational prediction.
   (metadata + domain knowledge)

5. **Newbery, D.**
   National Energy and Climate Plans for the island of Ireland: wind curtailment, interconnectors
   and storage. *Energy Policy* 2021, 158, 112513. DOI: 10.1016/j.enpol.2021.112513 — VERIFIED.
   Cost-benefit assessment of how Irish curtailment volumes scale with wind build-out and how
   interconnection/storage trade off against curtailed energy. Economic planning study.
   (metadata + domain knowledge)

6. **O'Sullivan, J.; Rogers, A.; Flynn, D.; Smith, P.; Mullane, A.; O'Malley, M.**
   Studying the Maximum Instantaneous Non-Synchronous Generation in an Island System—Frequency
   Stability Challenges in Ireland. *IEEE Transactions on Power Systems* 2014, 29(6), 2943–2951.
   DOI: 10.1109/TPWRS.2014.2316974 — VERIFIED.
   The foundational SNSP paper: frequency-stability limits cap instantaneous non-synchronous
   penetration on the all-island Irish system, underpinning EirGrid's operational SNSP limit
   (historically 50–65%, since raised toward 75%). Direct precedent for this paper's 70%
   SNSP-type reference cap. (metadata + domain knowledge)

7. **Cardo-Miota, J.; Trivedi, R.; Patra, S.; Khadem, S.; Bahloul, M.**
   Data-driven approach for day-ahead System Non-Synchronous Penetration forecasting: A
   comprehensive framework, model development and analysis. *Applied Energy* 2024, 362, 123006.
   DOI: 10.1016/j.apenergy.2024.123006 — VERIFIED.
   ML framework forecasting day-ahead SNSP trajectories for the Irish system — the closest
   existing work to operational curtailment-risk anticipation. Single system, bespoke pipeline,
   continuous-signal target; no public benchmark, no event/onset protocol, no seeded statistics.
   (metadata + search context)

8. **Hadian, H.; Naderkhani, F.**
   Deep Learning-Based Models for Wind and Solar Curtailment Forecasting.
   *Proc. 7th Int. Conf. on Energy Harvesting, Storage, and Transfer (EHST)* 2023, paper 120.
   DOI: 10.11159/ehst23.120 — VERIFIED (Crossref-indexed proceedings).
   Compares classical ML and deep models (SGD, kNN, SVR, trees, DNN, LSTM, GRU) for curtailment
   time-series forecasting; GRU best. Point-forecast comparison on one dataset; no benchmark
   release, no early-warning task, no statistical protocol. (metadata + proceedings abstract)

9. **Kaur, A.; Nonnenmacher, L.; Coimbra, C.F.M.**
   Net load forecasting for high renewable energy penetration grids.
   *Energy* 2016, 114, 1073–1084. DOI: 10.1016/j.energy.2016.08.067 — VERIFIED.
   Day-ahead/short-term net-load forecasting under high solar penetration (CAISO), showing how
   forecast construction changes error characteristics relevant to reserve and accommodation
   decisions. Continuous net-load target, never mapped to curtailment-risk events.
   (metadata + domain knowledge)

**Thread A takeaway.** Quantification and driver studies (1–5) are retrospective; the SNSP line
(6–7) motivates a penetration-cap view of curtailment risk and even forecasts the cap-binding
signal, but on private/system-specific data; the sole dedicated ML curtailment-forecasting entry
(8) is a model comparison without any reusable asset. None publishes a reproducible public
curtailment-risk early-warning benchmark, an onset-oriented evaluation slice, or a seeded
statistical protocol.

---

## Thread B — Case/analogue retrieval and metric learning in power system decision support

Retrieval from historical operating experience is one of the oldest ideas in power system
decision support, and it keeps being re-proposed at single tasks and fixed horizons.

1. **Rahman, S.; Bhatnagar, R.**
   An expert system based algorithm for short term load forecast.
   *IEEE Transactions on Power Systems* 1988, 3(2), 392–399. DOI: 10.1109/59.192889 — VERIFIED.
   Early formalization of "similar-day" operator reasoning (day type, season, weather) inside a
   rule-based 24-h-ahead load forecaster. (metadata + domain knowledge)

2. **Mandal, P.; Senjyu, T.; Urasaki, N.; Funabashi, T.**
   A neural network based several-hour-ahead electric load forecasting using similar days
   approach. *International Journal of Electrical Power & Energy Systems* 2006, 28(6), 367–373.
   DOI: 10.1016/j.ijepes.2005.12.007 — VERIFIED.
   Euclidean similar-day retrieval over weather/calendar variables feeding a neural corrector for
   1–6 h-ahead load: the canonical retrieve-then-predict pipeline. (metadata + domain knowledge)

3. **Lora, A.T.; Santos, J.M.R.; Exposito, A.G.; Ramos, J.L.M.; Santos, J.C.R.**
   Electricity Market Price Forecasting Based on Weighted Nearest Neighbors Techniques.
   *IEEE Transactions on Power Systems* 2007, 22(3), 1294–1301.
   DOI: 10.1109/tpwrs.2007.901670 — VERIFIED.
   Pure instance-based forecasting: weighted k-NN over lagged price-trajectory windows for
   next-day Spanish market prices, competitive with GARCH/ANN. (metadata + domain knowledge)

4. **Xu, T.; Wade, N.S.; Davidson, E.M.; Taylor, P.C.; McArthur, S.D.J.; Garlick, W.G.**
   Case-based reasoning for coordinated voltage control on distribution networks.
   *Electric Power Systems Research* 2011, 81(12), 2088–2098.
   DOI: 10.1016/j.epsr.2011.08.005 — VERIFIED.
   Full CBR cycle (retrieve–reuse–revise–retain) over network operating cases for voltage
   control, avoiding repeated optimization. Retrieval as decision support in operations proper.
   (metadata + domain knowledge)

5. **Delle Monache, L.; Eckel, F.A.; Rife, D.L.; Nagarajan, B.; Searight, K.**
   Probabilistic Weather Prediction with an Analog Ensemble.
   *Monthly Weather Review* 2013, 141(10), 3498–3516. DOI: 10.1175/mwr-d-12-00281.1 — VERIFIED.
   Foundational analog-ensemble (AnEn) method: retrieve past forecasts most similar to the
   current one and use their verifying observations as a predictive distribution. (Crossref abstract)

6. **Alessandrini, S.; Delle Monache, L.; Sperati, S.; Nissen, J.N.**
   A novel application of an analog ensemble for short-term wind power forecasting.
   *Renewable Energy* 2015, 76, 768–781. DOI: 10.1016/j.renene.2014.11.061 — VERIFIED.
   AnEn applied to probabilistic wind power forecasting (0–132 h), outperforming quantile
   regression and EPS-based approaches on an Italian wind farm. (metadata + domain knowledge)

7. **Alessandrini, S.; Delle Monache, L.; Sperati, S.; Cervone, G.**
   An analog ensemble for short-term probabilistic solar power forecast.
   *Applied Energy* 2015, 157, 95–110. DOI: 10.1016/j.apenergy.2015.08.011 — VERIFIED.
   AnEn for solar power (0–72 h, three PV plants), with plant-tailored predictor weighting.
   (metadata + domain knowledge)

8. **De Baets, L.; Develder, C.; Dhaene, T.; Deschrijver, D.**
   Detection of unidentified appliances in non-intrusive load monitoring using siamese neural
   networks. *International Journal of Electrical Power & Energy Systems* 2019, 104, 645–653.
   DOI: 10.1016/j.ijepes.2018.07.026 — VERIFIED.
   Siamese CNN learns an embedding of V–I trajectories in which same-appliance samples cluster;
   unknown appliances detected by distance-based reasoning in the learned space. Learned
   similarity metrics arriving in power applications. (metadata + domain knowledge)

9. **Zhu, R.; Gong, X.; Hu, S.; Wang, Y.**
   Power Quality Disturbances Classification via Fully-Convolutional Siamese Network and
   k-Nearest Neighbor. *Energies* 2019, 12(24), 4732. DOI: 10.3390/en12244732 — VERIFIED.
   Explicit "learned metric + k-NN retrieval" architecture for power-quality disturbance
   classification; strong in small-sample and noisy regimes. (Crossref abstract)

**Thread B takeaway.** From 1988 expert systems through 2013–2015 analog ensembles to 2019
Siamese metric learning, retrieval keeps being validated at *one task and one (or one narrow
band of) horizon at a time*, each on its own data. No work evaluates a retrieval mechanism
across forecast horizons on a common public benchmark against matched non-retrieval controls —
so whether retrieval helps or hurts as the horizon grows is undocumented. This paper's central
component finding (significantly beneficial at 1 h, significantly harmful for 24 h onset
warning) is exactly the kind of result that cannot exist without such an evaluation.

---

## Thread C — Naive baselines and benchmark design in time-series forecasting

The forecasting methodology literature has spent two decades documenting why evaluations
without strong naive baselines, scaled comparisons, and leak-free protocols mislead.

1. **Makridakis, S.; Hibon, M.**
   The M3-Competition: results, conclusions and implications.
   *International Journal of Forecasting* 2000, 16(4), 451–476.
   DOI: 10.1016/S0169-2070(00)00057-1 — VERIFIED.
   3003 series, 24 methods: sophisticated methods do not necessarily beat simple ones.

2. **Hyndman, R.J.; Koehler, A.B.**
   Another look at measures of forecast accuracy.
   *International Journal of Forecasting* 2006, 22(4), 679–688.
   DOI: 10.1016/j.ijforecast.2006.03.001 — VERIFIED.
   Shows standard accuracy measures degenerate on intermittent/near-zero data (directly relevant
   to sparse curtailment series) and proposes MASE, anchoring evaluation to the naive baseline.

3. **Makridakis, S.; Spiliotis, E.; Assimakopoulos, V.**
   Statistical and Machine Learning forecasting methods: Concerns and ways forward.
   *PLOS ONE* 2018, 13(3), e0194889. DOI: 10.1371/journal.pone.0194889 — VERIFIED.
   ML methods systematically beaten by simple statistical methods under honest out-of-sample
   evaluation; prescribes baseline discipline.

4. **Makridakis, S.; Spiliotis, E.; Assimakopoulos, V.**
   The M4 Competition: 100,000 time series and 61 forecasting methods.
   *International Journal of Forecasting* 2020, 36(1), 54–74.
   DOI: 10.1016/j.ijforecast.2019.04.014 — VERIFIED.
   Benchmark scored relative to a naive-2 reference (OWA); pure ML underperformed statistical
   benchmarks, hybrids won.

5. **Makridakis, S.; Spiliotis, E.; Assimakopoulos, V.**
   M5 accuracy competition: Results, findings, and conclusions.
   *International Journal of Forecasting* 2022, 38(4), 1346–1364.
   DOI: 10.1016/j.ijforecast.2021.11.013 — VERIFIED.
   Only a minority of 5507 teams beat the simple benchmark combinations, quantifying how hard
   naive baselines are to beat at scale.

6. **Hong, T.; Pinson, P.; Fan, S.; Zareipour, H.; Troccoli, A.; Hyndman, R.J.**
   Probabilistic energy forecasting: Global Energy Forecasting Competition 2014 and beyond.
   *International Journal of Forecasting* 2016, 32(3), 896–913.
   DOI: 10.1016/j.ijforecast.2016.02.001 — VERIFIED.
   The reference for benchmark-competition design in energy forecasting specifically (rolling
   setup, scoring against benchmark methods, leaderboards).

7. **Hewamalage, H.; Ackermann, K.; Bergmeir, C.**
   Forecast evaluation for data scientists: common pitfalls and best practices.
   *Data Mining and Knowledge Discovery* 2023, 37(2), 788–832.
   DOI: 10.1007/s10618-022-00894-5 — VERIFIED.
   Catalog of evaluation pitfalls: temporal leakage, missing naive baselines, inappropriate
   error measures, flawed CV for time series.

8. **Kapoor, S.; Narayanan, A.**
   Leakage and the reproducibility crisis in machine-learning-based science.
   *Patterns* 2023, 4(9), 100804. DOI: 10.1016/j.patter.2023.100804 — VERIFIED.
   300+ papers across 20+ fields whose ML advantages vanish under corrected evaluation; the
   standard citation for the ML-for-science reproducibility crisis.

9. **Yang, D.; et al. (33 authors)**
   Verification of deterministic solar forecasts. *Solar Energy* 2020, 210, 20–37.
   DOI: 10.1016/j.solener.2020.04.019 — VERIFIED.
   Community position paper mandating skill computation against standardized reference methods
   (e.g., smart persistence) and grounding event-oriented verification in the Murphy framework.

10. **Barrows, C.; Preston, E.; Staid, A.; Stephen, G.; Watson, J.-P.; Bloom, A.; Ehlen, A.;
    Ikaheimo, J.; Jorgenson, J.; Krishnamurthy, D.; Lau, J.; McBennett, B.; O'Connell, M.**
    The IEEE Reliability Test System: A Proposed 2019 Update.
    *IEEE Transactions on Power Systems* 2020, 35(1), 119–127.
    DOI: 10.1109/TPWRS.2019.2925557 — VERIFIED.
    RTS-GMLC: the open test system with time-synchronized load/wind/solar series that this
    paper's benchmark is built on; the model for how public power-system evaluation assets
    should be released.

**Thread C takeaway.** This literature supplies the design rules the proposed benchmark
implements — persistence/seasonal baselines as first-class methods, sparse-series-aware event
metrics, temporal leak-free splits, seeded multi-run statistics with multiplicity correction —
and it also supplies the interpretive frame for this paper's negative findings: a benchmark on
which persistence wins overall MAE is behaving exactly as the M-competition record predicts,
and reporting that outcome is evidence of protocol integrity, not framework failure.

---

## Gap statement

At the intersection of the three threads, two specific artifacts are missing. **(G1)** There is
no reproducible, public curtailment-risk early-warning benchmark: curtailment studies quantify
retrospectively (Thread A, 1–5) or forecast continuous proxies on private single-system data
(A7–A8), and none defines an event/onset evaluation slice for the operationally relevant warning
moments, publishes the full task-construction code, or applies a seeded statistical protocol.
**(G2)** Retrieval-based (similar-day/analogue/case-based) decision support, though repeatedly
proposed for power systems since 1988 (Thread B), has never been systematically characterized
across forecast horizons on a common public benchmark with matched non-retrieval controls —
whether retrieval helps or hurts is horizon-dependent and undocumented. This paper addresses G1
with a method-agnostic benchmark (full-year RTS-GMLC, fixed 70% SNSP-type reference policy,
onset-slice protocol, 10-seed Mann-Whitney/Holm statistics) and G2 with a complete
characterization of a learned-embedding Siamese retrieval framework on it, including
significance-backed evidence in both directions and honest negative findings, with the
evaluation discipline of Thread C built into the protocol.
