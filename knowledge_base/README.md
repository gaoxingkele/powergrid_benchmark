# Powergrid Benchmark Global Knowledge Base

本目录是项目的全局知识库，用于沉淀电网 + 计算机方向 benchmark 的长期资产：公开数据集、经典实验任务、baseline 算法、近三年代表性论文、数据获取记录和每轮更新记录。

## 入口

- `wiki/index.md`: 总入口，按 Karpathy LLM wiki 风格维护可快速跳转的索引。
- `datasets/public_dataset_registry.md`: 公开数据集统一登记表。
- `tasks/task_taxonomy.md`: 电网实验任务分类。
- `algorithms/baseline_matrix.md`: 任务到经典 baseline 的矩阵。
- `literature/recent_2024_2026_literature_map.md`: 近三年代表性文献与任务映射。
- `sources/web_sources.md`: 本轮外部来源链接和访问记录。
- `updates/`: 每轮知识更新、决策摘要、论文更新和开放问题。

## 维护规则

1. 数据集先登记，再下载或记录访问限制。
2. 任何实验任务必须绑定至少一个数据集、一个传统 baseline 和一个可选 AI baseline。
3. 论文条目优先选择 IEEE Transactions、IEEE Open Access Journal of Power and Energy、SCI 期刊、高影响因子期刊、CCF 会议或公开 benchmark 论文。
4. 大体量数据、需要 token/API key 的数据，只保存元数据、访问脚本和获取说明，不默认全量下载。
5. “思维链更新”只记录可审计的决策摘要、依据摘要和开放问题，不保存隐藏推理过程。

## 当前优先级

1. 通用网架/OPF benchmark: MATPOWER, pandapower networks, PGLib-OPF, RTS-GMLC, SimBench, TAMU synthetic grids.
2. 运行控制/强化学习: Grid2Op/L2RPN.
3. 真实时序与市场数据: OPSD, EIA, ENTSO-E, PJM.
4. 可再生能源与天气: NREL NSRDB, PSML, large synthetic grid ML datasets.
5. 专题数据: ACN-Data, DGA, PMU/fault/disturbance datasets.
