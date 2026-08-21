# Related Work — Typed Dependency Graph

## RW08: Ali, 2019 — Short-Term Load Forecasting using Smart Meter Data
- **DOI**: 10.1145/3307772.3330157 (ACM e-Energy 2019)
- **Type**: baseline
- **Delta**:
  - What changed: uses AMI/smart-meter data for short-term forecasting; proposed method instead compares LSTM/GRU on regional aggregates.
  - Why: AMI captures detailed customer trends but faces privacy/complexity issues.
- **Claims affected**: C01
- **Adopted elements**: motivation that detailed consumption data improves accuracy (Table 7 baseline entry).

## RW12: Islam, Rasheed & Ahmed, 2022 — Review of STLF using DNNs and Metaheuristics
- **DOI**: 10.1155/2022/4049685
- **Type**: baseline
- **Delta**:
  - What changed: combines deep neural networks with metaheuristic optimisation; proposed method uses plain recurrent nets + forecast-driven control.
  - Why: metaheuristics improve short-term estimate accuracy but complicate grid-impact evaluation.
- **Claims affected**: C01
- **Adopted elements**: comparison point in Table 7.

## RW16: Ibrahim, Rabelo, Gutierrez-Franco & Clavijo-Buritica, 2022 — ML for STLF in Smart Grids
- **DOI**: 10.3390/en15218079
- **Type**: baseline
- **Delta**:
  - What changed: LSTM-based RNNs for electric load forecasting; this paper adds a GRU comparison and control layer.
  - Why: establishes LSTM-RNN accuracy in smart grids.
- **Claims affected**: C01, C02
- **Adopted elements**: LSTM-RNN forecasting formulation (Table 7 baseline).

## RW14: Chemetova, Santos & Ventim-Neves, 2016 — Load forecasting in MV distribution grids
- **DOI**: 10.1007/978-3-319-31165-4_33
- **Type**: bounds
- **Delta**:
  - What changed: tailored algorithms for medium-voltage networks; proposed method aims for cross-dataset applicability.
  - Why: infrastructure-specific algorithms are needed (a limitation the proposed work also inherits per its generalisation caveat).
- **Claims affected**: C01
- **Adopted elements**: motivation for customized algorithms (Table 7).

## RW18: Zhang, Jin, Shi & Chew, 2023 — Bayesian-optimized CNN-BiLSTM real-time model
- **DOI**: 10.3389/fenrg.2023.1193662
- **Type**: baseline
- **Delta**:
  - What changed: cognitive/Bayesian-optimized CNN-BiLSTM for real-time forecasting; this paper uses simpler LSTM/GRU with an explicit control strategy.
  - Why: cognitive algorithms are argued vital for efficient grid management.
- **Claims affected**: C01, C05
- **Adopted elements**: real-time forecasting framing (Table 7).

## RW02: Abdelaziz & Biswal — Load Forecasting Models in Smart Grid (Encyclopedia)
- **DOI**: encyclopedia.pub/entry/41526
- **Type**: baseline
- **Delta**:
  - What changed: survey comparing smart-meter-data-driven algorithms; proposed method contributes a concrete comparative LSTM/GRU study.
  - Why: guides model selection.
- **Claims affected**: C02
- **Adopted elements**: comparative framing (Table 7).

## RW20: Vazquez et al., 2017 — Adaptive Load Forecasting in a Smart-Grid Demonstration
- **DOI**: 10.3390/en10020190
- **Type**: baseline
- **Delta**:
  - What changed: adaptive forecasting in a demonstration project; proposed method proposes forecast-driven control instead of pure adaptation.
  - Why: shows practicality of adaptive methods.
- **Claims affected**: C04
- **Adopted elements**: adaptivity motivation (Table 7).

## RW11: Luo & Wang, 2016 — Cloud-computing smart-grid load-forecasting platform
- **DOI**: — (J. Hunan Univ. Nat. Sci. 2016)
- **Type**: baseline
- **Delta**:
  - What changed: cloud-based forecasting platform; proposed method avoids cloud-infrastructure dependency.
  - Why: cloud scalability improves accuracy but creates dependency.
- **Claims affected**: C01
- **Adopted elements**: comparison point (Table 7).

## RW21: Fotopoulou et al., 2024 — Review of ESSs of Non-Interconnected European Islands
- **DOI**: 10.3390/su16041572
- **Type**: imports
- **Delta**:
  - What changed: establishes ESS role in peak shaving / load balancing / renewable integration; imported as a control-strategy building block.
  - Why: ESSs are a critical resilient-grid component.
- **Claims affected**: C04
- **Adopted elements**: ESS-based peak shaving used inside the ICS.

## RW22: Esnaola-Gonzalez et al., 2021 — AI-Powered Residential Demand Response
- **DOI**: 10.3390/electronics10060693
- **Type**: imports
- **Delta**:
  - What changed: DR aligns demand with supply under intermittent renewables; imported as an ICS building block.
  - Why: DR is key for load balancing.
- **Claims affected**: C04
- **Adopted elements**: DR load-shifting used inside the ICS.

## RW27: Hochreiter & Schmidhuber, 1997 — Long Short-Term Memory
- **DOI**: 10.1162/neco.1997.9.8.1735
- **Type**: imports
- **Delta**:
  - What changed: origin of LSTM; the paper's LSTM equations (§3.4) are derived from it.
  - Why: foundational architecture.
- **Claims affected**: C01, C02
- **Adopted elements**: LSTM cell formulation (Eqs. 9–14).

## RW28: Cho et al., 2014 — RNN Encoder–Decoder (GRU origin)
- **DOI**: arXiv:1406.1078
- **Type**: imports
- **Delta**:
  - What changed: origin of GRU; the paper's GRU equations (§3.4) are derived from it.
  - Why: foundational architecture.
- **Claims affected**: C01, C02
- **Adopted elements**: GRU cell formulation (Eqs. 5–8).

## RW26: Patro & Sahu, 2015 — Normalization: A preprocessing stage
- **DOI**: arXiv:1503.06462
- **Type**: imports
- **Delta**:
  - What changed: basis for the min–max normalisation preprocessing (Eqs. 1–2).
  - Why: feature scaling.
- **Claims affected**: C01
- **Adopted elements**: normalisation formula.

## RW29/RW30: Willmott & Matsuura 2005; "Evaluating accuracy measures" 1995
- **DOI**: 10.3354/cr030079 (RW29); RW30 Am. Stat. 1995
- **Type**: imports
- **Delta**:
  - What changed: basis for the MSE/MAPE evaluation metrics (Eqs. 16–17).
  - Why: error-measure selection.
- **Claims affected**: C01, C02, C03
- **Adopted elements**: evaluation-metric definitions.

## Additional citations (brief)
- [1] Ahmad et al., 2022 (IEEE Access) — load-forecasting survey; background.
- [3] Khan et al., 2016 — load forecasting, dynamic pricing & DSM review; background.
- [4] Kuster et al., 2017 — critical review of electrical load-forecasting models; background.
- [5] Salehimehr et al., 2022 — STLF AI-methods survey; background.
- [6] Wang, Zhang & Ren, 2016 — L1-regularized CCRF customer-behaviour forecasting; background.
- [7] Ferreira et al., 2017 — short-term load/production prediction models; background.
- [9] Zheng et al., 2017 — LSTM-RNN electric load forecasting; background/baseline.
- [10] Roy et al., 2021 — LSTM demand forecasting; background.
- [13] Dhumale, 2010 — smart-grid experimentation plan (case study); background.
- [15] Lee et al., 2016 — trends in short-term renewable/load forecasting; background.
- [17] Habbak et al. — smart load-forecasting techniques; background.
- [19] Vazquez et al. (BiLSTM/Bayesian/CNN) — cited for advanced ML forecasting; background.
- [23] Rai & De, 2023 — two-level heterogeneous ensemble; motivates traditional-method shortfall.
- [24] Azeem et al., 2022 — deterioration of load-forecasting models (basis of the "DLPaM" framing); background.
- [25] Madrid & Antonio, 2021 — STLF with ML; background.
