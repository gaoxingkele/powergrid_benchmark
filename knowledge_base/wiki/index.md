# Powergrid Benchmark Wiki

本 wiki 是项目的“全局脑图”。它不替代原始论文、代码和数据，而是维护可复用的索引、判断标准和更新记录。

## Core Maps

- [公开数据集登记表](../datasets/public_dataset_registry.md)
- [实验任务分类](../tasks/task_taxonomy.md)
- [baseline 算法矩阵](../algorithms/baseline_matrix.md)
- [2024-2026 文献地图](../literature/recent_2024_2026_literature_map.md)
- [外部来源记录](../sources/web_sources.md)

## Update Streams

- [决策日志](../updates/decision_log/2026-07-06.md)
- [依据摘要](../updates/rationale_summary/2026-07-06.md)
- [论文更新](../updates/paper_updates/2026-07-06.md)
- [开放问题](../updates/open_questions/2026-07-06.md)

## Benchmark Spine

| 层级 | 作用 | 当前资产 |
| --- | --- | --- |
| 标准网架 | 统一拓扑和潮流/OPF 问题 | MATPOWER, pandapower, PGLib-OPF, TAMU, SimBench |
| 时序/市场 | 负荷、发电、价格、可再生出力 | OPSD, EIA, ENTSO-E, PJM |
| 天气/可再生 | PV/wind 预测与场景生成 | NREL NSRDB, PSML, Zenodo synthetic grid ML |
| 仿真/交互环境 | 控制、RL、拓扑切换、在线决策 | Grid2Op, SimBench, RTS-GMLC |
| 专题设备 | 设备故障、DGA、PMU、EV 充电 | ACN-Data, DGA/PMU candidates |

## Canonical Task Families

1. OPF/PF 近似与可行性保持。
2. N-1 安全评估与 contingency screening。
3. 负荷、风电、光伏、价格预测。
4. 配电网 Volt-VAR/DER/EV 协同控制。
5. 设备故障诊断、DGA、PMU 事件识别。
6. 电网运行代理和拓扑控制。
7. 网络安全、异常检测和 cyber-physical resilience。

## How To Use

新论文或新数据源进入项目时，先更新 `datasets/public_dataset_registry.md` 或 `literature/recent_2024_2026_literature_map.md`，再进入 ARA 工程目录。实验设计时优先从 `task_taxonomy.md` 和 `baseline_matrix.md` 选择可复用配置。
