# Related Work — Typed Dependency Graph

## RW01: Graves & Schmidhuber, 2005 — Bidirectional LSTM
- **DOI**: 10.1109/IJCNN.2005.1556215 (IEEE IJCNN 2005, pp. 2047–2052)
- **Type**: imports
- **Delta**:
  - What changed: Adopts BiLSTM as the temporal extractor inside the base learner.
  - Why: Bidirectional context captures both historical patterns and future-influenced states (e.g., pre-holiday adjustments).
- **Claims affected**: C01
- **Adopted elements**: BiLSTM forward/backward concatenation (Eqs 8–10).

## RW02: Chen et al., 2023 — GCN-LSTM multifeature short-term load forecasting
- **DOI**: 10.1155/2023/8846554 (Int. Trans. Electr. Energy Syst.)
- **Type**: baseline / extends
- **Delta**:
  - What changed: The paper extends the GCN+recurrent combination by replacing LSTM with BiLSTM, wrapping it in modified AdaBoost, and adding MC-Dropout uncertainty weighting; GCN-LSTM is also used as a comparison baseline.
  - Why: To add ensemble robustness and uncertainty quantification beyond a single GCN-LSTM.
- **Claims affected**: C01
- **Adopted elements**: GCN-for-spatial + recurrent-for-temporal composition idea.

## RW03: Ma & Mei, 2022 — hybrid attention-based deep learning (CNN-LSTM)
- **DOI**: 10.1016/j.apenergy.2022.119608 (Appl. Energy)
- **Type**: baseline
- **Delta**:
  - What changed: CNN-LSTM+attention for spatiotemporal features; here CNN-LSTM/CNN-BiLSTM serve as comparison baselines instead of the proposed GCN route.
  - Why: Positions graph convolution against convolutional spatial extraction.
- **Claims affected**: C01
- **Adopted elements**: Spatiotemporal-feature-extraction framing.

## RW04: Bouktif et al., 2020 — LSTM-RNN with GA/PSO metaheuristics
- **DOI**: 10.3390/en13020391 (Energies)
- **Type**: bounds
- **Delta**:
  - What changed: Prior work tunes/combines via genetic algorithm and particle-swarm optimization; this paper instead uses boosting + Bayesian uncertainty for weight adaptation.
  - Why: Contrasts metaheuristic weight search with adaptive boosting/uncertainty weighting.
- **Claims affected**: C01, C02
- **Adopted elements**: Motivation for adaptive combination weights.

## RW05: Gal & Ghahramani, 2016 — Dropout as a Bayesian approximation
- **DOI**: (ICML 2016, pp. 1050–1059; arXiv:1506.02142)
- **Type**: imports
- **Delta**:
  - What changed: Directly imports MC Dropout as the Bayesian-approximation mechanism for uncertainty estimation.
  - Why: Provides posterior-predictive uncertainty without full Bayesian inference.
- **Claims affected**: C02, C05
- **Adopted elements**: Inference-time dropout sampling → predictive variance (Eq 17).

## RW06: Jin et al., 2021 — attention encoder-decoder with Bayesian optimization
- **DOI**: 10.3390/en14061596 (Energies)
- **Type**: imports
- **Delta**:
  - What changed: Cited as the Bayesian-methods reference for probabilistic inference in load forecasting.
  - Why: Grounds the "Bayesian method" framing.
- **Claims affected**: C05
- **Adopted elements**: Bayesian posterior framing for prediction/uncertainty.

## RW07: Bates & Granger, 1969 — The combination of forecasts
- **DOI**: 10.1057/jors.1969.103 (J. Oper. Res. Soc.)
- **Type**: imports
- **Delta**:
  - What changed: Foundational theory for combined/ensemble forecasting that the AdaBoost ensemble builds on.
  - Why: Establishes that combining models can beat single models.
- **Claims affected**: C01
- **Adopted elements**: Ensemble-forecasting principle.

## RW08: Ying et al., 2013 / Nirmal et al., 2024 — AdaBoost algorithm & applications
- **DOI**: 10.3724/SP.J.1004.2013.00745 (Acta Autom. Sin.); 10.1016/j.prime.2024.100452 (e-Prime)
- **Type**: imports
- **Delta**:
  - What changed: Imports the AdaBoost boosting framework, then modifies it (deep base learner, selective 0.3-threshold re-weighting, exponential-decay learner weight).
  - Why: Base ensemble machinery adapted to load forecasting.
- **Claims affected**: C04
- **Adopted elements**: Iterative weak-learner re-weighting and weighted voting.

## RW09: Chok, 2010 — Pearson vs Spearman vs Kendall correlation
- **DOI**: (PhD thesis, Univ. of Pittsburgh)
- **Type**: imports
- **Delta**:
  - What changed: Justifies choosing Spearman (rank) correlation for non-normal, non-linear feature relations.
  - Why: Supports the graph-construction rule.
- **Claims affected**: C03
- **Adopted elements**: Rank-correlation rationale.

## RW10: Sieranoja & Fränti, 2018 — KNN-graph construction
- **DOI**: 10.1145/3274895 (J. Exp. Algorithmics)
- **Type**: baseline / refutes
- **Delta**:
  - What changed: KNN graph used as a graph-construction baseline and argued inferior (spurious edges from raw similarity).
  - Why: Comparison in Table 2.
- **Claims affected**: C03
- **Adopted elements**: KNN adjacency as comparison.

## RW11: Peng et al., 2020 — learned graphs (graphical mutual information maximization)
- **DOI**: 10.1145/3366423.3380112 (WWW 2020, pp. 259–270)
- **Type**: baseline / refutes
- **Delta**:
  - What changed: Learned-graph baseline; argued to need large data and to overfit.
  - Why: Comparison in Table 2.
- **Claims affected**: C03
- **Adopted elements**: Learned adjacency as comparison.

## RW12: Wang et al., 2023 — graph structure learning via progressive strategy (mutual information)
- **DOI**: 10.1145/3580305.3599417 (KDD 2023, pp. 2337–2348)
- **Type**: baseline / refutes
- **Delta**:
  - What changed: Mutual-information graph baseline; argued sensitive to distribution/sample size.
  - Why: Comparison in Table 2.
- **Claims affected**: C03
- **Adopted elements**: MI adjacency as comparison.

## RW13: Wei et al., 2024 — spatial load forecasting via LDTW and GCN
- **DOI**: 10.1049/gtd2.13106 (IET Gener. Transm. Distrib.)
- **Type**: imports
- **Delta**:
  - What changed: Cited for the GCN spatial-forecasting formulation used here.
  - Why: Grounds GCN adoption.
- **Claims affected**: C01
- **Adopted elements**: GCN spatial-modeling formulation.

## RW14: Additional background citations (brief)
- **Kwilinski et al. 2022 [1]; Kumar et al. 2019 [2]** — smart-grid / renewable-integration context (motivation).
- **Shah et al. 2025 [3]; Rui et al. 2024 [4]; Fahad & Arbab 2014 [5]** — load-forecasting drivers and meteorological factors (motivation, O2).
- **Peng et al. 2022 [6]; Almalaq & Edwards 2017 [7]** — deep-learning-for-load-forecasting reviews (O1).
- **Li et al. 2017 [8] (CNN "everything is image"); Muzaffar & Afshari 2019 [9] (LSTM); L'Heureux et al. 2022 [10] (Transformer)** — single-model deep forecasters surveyed as prior art.
- **Han & Zeng 2024 [11]** — parallel BiLSTM / information loss on long sequences (O1).
- **Li & Chang 2018 [14]** — variable-weight combination model (motivation for hybrid/adaptive weighting).
- **Memarzadeh & Keynia 2021 [22]** — LSTM vanishing-gradient reference.
- **Yang & Wang 2022 [21]** — BiLSTM for time-series (LSTM origin citation).
- **Song et al. 2024 [19]; Wang et al. 2025 [27]** — GCN / GNN methodology references.
- **Type**: background/infrastructure — no specific technical delta adopted; retained for citation-footprint completeness.
