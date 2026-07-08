# Baseline Algorithm Matrix

更新日期: 2026-07-06

| 任务 | 必选传统 baseline | 必选 ML baseline | 可选高级 baseline | 关键约束 |
| --- | --- | --- | --- | --- |
| PF/OPF 近似 | Newton-Raphson PF, MATPOWER/Pandapower OPF, DC OPF | MLP, Random Forest/XGBoost | physics-informed NN, GNN, typed GNN, differentiable OPF | 必须报告约束违反和 objective gap |
| N-1 安全筛选 | AC contingency, PTDF/LODF, rule ranking | Logistic Regression, Random Forest, XGBoost | physics-informed GNN, calibrated classifier | unsafe recall 优先于平均准确率 |
| 负荷/风光/价格预测 | persistence, seasonal naive, ARIMA | XGBoost/LightGBM, LSTM/GRU | Transformer/Informer/TimesNet, probabilistic forecasting | rolling split，避免未来信息泄露 |
| 配电网控制 | rule-based, OPF/MPC, droop control | DQN/PPO/SAC | GNN-RL, safe RL, multi-agent RL | 必须限制非法动作和越限风险 |
| Grid2Op 拓扑控制 | do-nothing, greedy/rule-based, OPF action | PPO/SAC/DQN | graph RL, imitation learning, offline RL | survival/reward 同时报告 |
| DGA/设备诊断 | IEC/IEEE/Duval/Rogers rules, SVM/KNN | Random Forest, XGBoost | CNN/Transformer, knowledge-enhanced model | 标签映射必须公开 |
| PMU/故障波形 | threshold/rule, SVM, Random Forest | CNN, LSTM | Transformer, GNN, contrastive learning | train/test 按事件或场景隔离 |
| Cyber-physical anomaly | residual-based BDD, state estimation residual | autoencoder, XGBoost | graph anomaly detection, robust GNN | false alarm 和 attack localization 必须报告 |

## Baseline Selection Rules

1. 每个任务至少包含一个物理/规则 baseline 和一个非深度 ML baseline。
2. 深度模型必须与简单模型比较，不允许只和同类深度模型比较。
3. 对电网运行类任务，平均误差不能替代安全指标。
4. 对预测任务，必须使用时间滚动验证或严格 chronological split。
5. 对分类任务，类别不均衡时必须报告 macro-F1、per-class recall 或 confusion matrix。
