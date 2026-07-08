# Recent Literature Map: 2024-2026

更新日期: 2026-07-06

本表按任务归类近三年对公开数据集和 benchmark 有直接参考价值的论文、benchmark 或综述。后续进入 ARA 的论文应从这里抽取并补全 BibTeX、PDF、代码和实验配置。

| 年份 | 主题 | 来源/质量标签 | 数据集/平台 | 任务 | 方法线索 | 项目用途 |
| --- | --- | --- | --- | --- | --- | --- |
| 2025 | Open power system datasets and simulation engines survey | IEEE Open Access Journal of Power and Energy | MATPOWER, PGLib, Grid2Op, PyPSA, OPSD 等 | 数据集/平台综述 | 资源分类与可复现标准 | 数据集 registry 的综述入口 |
| 2025 | PFDelta: large-scale power-flow benchmark | ICLR/Climate Change AI workshop/OpenReview | PFDelta benchmark | PF 近似 | ML surrogate, benchmark protocol | PF/OPF 任务扩展候选 |
| 2025 | PGLearn: power-grid representation learning benchmark | arXiv/preprint | power-grid graph datasets | 表征学习, 图学习 | GNN representation learning | 图学习 benchmark 候选 |
| 2025 | RL2Grid benchmark | arXiv/OpenReview | Grid2Op style environments | RL grid operation | RL benchmarking | Grid2Op/L2RPN 扩展候选 |
| 2025 | Graph reinforcement learning for power grids | Energy AI / SCI | Grid operation environments | 拓扑控制, 安全运行 | graph RL | 运行代理算法线索 |
| 2025 | Large synthetic dataset for machine learning in power grids | Nature Scientific Data / Zenodo | 4.6 TB synthetic grid ML data | PF/ML surrogate, weather-grid coupling | large-scale data generation | 只保留 metadata，后续按子集下载 |
| 2024 | OPF with physics-informed typed graph neural network | IEEE Transactions on Power Systems | PGLib/MATPOWER style cases | OPF approximation | typed GNN, physics-informed constraints | OPF GNN baseline 线索 |
| 2024 | Physics-informed graphical representation-enabled DRL for robust voltage control | IEEE Transactions on Smart Grid | distribution systems | Volt-VAR/robust voltage control | graph representation + DRL | 配电控制方向高质量参考 |
| 2024 | Grid2Op topology action comparison | Energy AI / SCI | Grid2Op/L2RPN | topology control | RL/heuristic comparison | Grid operation baseline 线索 |
| 2024 | PSML: multi-scale time-series dataset for ML in decarbonized grids | Scientific Data / dataset paper | PSML/open-source power dataset | renewable/load time-series ML | dataset construction | 时序预测和场景生成数据入口 |

## Literature Search Policy

1. 优先检索 `IEEE Transactions on Power Systems`, `IEEE Transactions on Smart Grid`, `IEEE Open Access Journal of Power and Energy`, `Applied Energy`, `Energy AI`, `Nature Scientific Data`。
2. 会议优先看 NeurIPS/ICLR/AAAI/IJCAI/KDD/WWW/CIKM/ICML 及 CCF A/B/C 会议中带公开 benchmark 或代码的电网论文。
3. 每篇候选论文进入 ARA 前至少确认：数据集、baseline、代码可得性、指标、复现实验门槛。
4. 综述论文用于扩展候选池，不直接替代原始实验论文。
