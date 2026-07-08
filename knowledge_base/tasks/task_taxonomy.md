# Powergrid Experiment Task Taxonomy

更新日期: 2026-07-06

## T1. PF/OPF 近似与可行性保持

- 目标: 用 ML/GNN/physics-informed 模型近似 AC/DC power flow 或 OPF，同时保持电压、潮流、发电上下限等约束。
- 数据集: MATPOWER, PGLib-OPF, TAMU synthetic grids, PFDelta benchmark, PSML.
- 经典 baseline: Newton-Raphson PF, MATPOWER OPF, PowerModels.jl, DC OPF, convex relaxation.
- AI baseline: MLP, GNN, typed GNN, physics-informed neural networks, learning-to-optimize, differentiable OPF.
- 核心指标: objective gap, feasibility violation, constraint violation rate, solve time, speedup, robustness under topology/load shift.

## T2. N-1 安全评估与快速筛选

- 目标: 对线路/机组故障后是否过载、失稳或违反约束进行快速评估。
- 数据集: MATPOWER, PGLib-OPF, TAMU, RTS-GMLC, Grid2Op.
- 经典 baseline: AC contingency analysis, DC screening, PTDF/LODF, rule-based ranking.
- AI baseline: Random Forest, XGBoost, MLP, GNN, physics-informed classifier, conformal risk screening.
- 核心指标: recall on unsafe cases, false negative rate, screening ratio, runtime, post-contingency violation magnitude.

## T3. 负荷、风电、光伏、价格预测

- 目标: 对短期/中期负荷、可再生出力、市场价格进行时间序列预测。
- 数据集: OPSD, EIA, ENTSO-E, PJM, NREL NSRDB, PSML, RTS-GMLC profiles.
- 经典 baseline: persistence, seasonal naive, ARIMA/SARIMA, Prophet, linear regression.
- AI baseline: Random Forest, XGBoost, LightGBM, LSTM/GRU, TCN, Transformer, TimesNet/Informer 类时序模型。
- 核心指标: MAE, RMSE, MAPE/sMAPE, pinball loss, CRPS, calibration, rolling-origin stability.

## T4. 配电网 DER/Volt-VAR/EV 控制

- 目标: 在配电网中控制无功、储能、EV 充电和 DER 协同，降低电压越限、网损和峰值负荷。
- 数据集/环境: SimBench, OpenDSS feeders, GridLAB-D, ACN-Data, Pecan Street candidates.
- 经典 baseline: rule-based Volt-VAR, OPF-based dispatch, MPC, droop control.
- AI baseline: DQN, PPO, SAC, multi-agent RL, GNN-RL, imitation learning.
- 核心指标: voltage violation, energy cost, peak reduction, control action count, comfort/charging delay, safety violations.

## T5. 电网运行代理与拓扑控制

- 目标: 在动态仿真中通过拓扑切换、redispatch 或 remedial action 维持安全运行。
- 数据集/环境: Grid2Op/L2RPN, RTS-GMLC, TAMU synthetic grids.
- 经典 baseline: do-nothing, rule-based topology action, OPF/MPC controller, expert heuristic.
- AI baseline: PPO/SAC/DQN, graph RL, imitation learning, offline RL, safe RL.
- 核心指标: survival time, reward, number of overloads, safety margin, action legality, generalization to chronics.

## T6. 设备故障诊断、DGA 与 PMU 事件识别

- 目标: 对变压器 DGA、PMU 波形、电能质量扰动、故障类型和故障位置做分类/定位。
- 数据集: Public DGA datasets, IEC TC10 references, synthetic PMU/fault datasets, distribution PMU candidates.
- 经典 baseline: IEC/IEEE/Duval/Rogers/Dornenburg rules, SVM, KNN, Random Forest.
- AI baseline: XGBoost, CNN, LSTM, Transformer, GNN, knowledge-enhanced ML.
- 核心指标: accuracy, macro-F1, recall per fault class, localization error, out-of-distribution robustness.

## T7. Cyber-Physical Security 与异常检测

- 目标: 识别 false data injection、通信攻击、异常测量和运行状态偏移。
- 数据集/环境: IEEE/MATPOWER cases with simulated attacks, Grid2Op, TAMU synthetic grids, PMU candidates.
- 经典 baseline: residual-based bad data detection, state estimation residual, rule thresholds.
- AI baseline: autoencoder, graph anomaly detection, temporal Transformer, robust GNN, adversarial training.
- 核心指标: detection rate, false alarm rate, attack localization, robustness, latency.
