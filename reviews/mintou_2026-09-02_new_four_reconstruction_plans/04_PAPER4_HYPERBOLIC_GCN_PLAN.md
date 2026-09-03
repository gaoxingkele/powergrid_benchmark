# 论文4重构计划：Hyperbolic Graph Convolutional Network for Load Forecasting

## A. 锁定信息与材料护照

- **锁定标题：** `Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting`
- **目标期刊：** Electronics（MDPI 主执行路线；栏目与最新投稿要求在提交前再次核验）
- **作者：** Zheng Jieyun（第一作者、通信作者），Zhang Linyao，Zhang Zhanghuang，Chen Zhuolin，Shi Ying
- **现有工程：** `paper_projects/mintou_p2_hygraph_load_forecasting`
- **现有主稿：** `manuscript/MANUSCRIPT.md`；`manuscript/journal_submission/paper.tex`
- **现有实验：** `experiments/p2_s3_identifiable_v1`
- **现有证据：** 24-step point forecasting、八个季度滚动块、五种子；当前 CSA 模型使用跨序列注意力与可选 Poincaré 距离权重；匹配比较中几何权重增益未解决，DLinear 在现有层级任务上更强。
- **验证状态：** 本计划不产生新模型结果。

## B. 现状诊断

### B1. 可保留资产

1. 多序列负荷数据清洗、滚动起点评估、五种子和匹配统计管线。
2. persistence、target-self、DLinear 等强/简单基线。
3. 现有跨序列注意力和 Poincaré 距离模型可作为重要对照。
4. 多预测跨度、计算开销和层级一致性分析基础。
5. 已明确披露的负结果，可防止新稿夸大双曲几何。

### B2. 标题—模型根本错位

- 现模型是稠密跨序列注意力，不执行邻接矩阵上的图卷积。
- Poincaré 距离只用于权重，不包含完整的双曲表示学习、指数/对数映射、Möbius 操作或双曲消息传递。
- 稿中已承认它不是 sparse graph attention，也没有 curvature-dependent graph convolution。
- 因而仅改题目、摘要或术语不能满足锁定标题；需要真正实现并评估 Hyperbolic GCN。

### B3. 不可主张

- 不把当前 CSA-Poincaré attention 改名为 HGCN。
- 不声称电力负荷天然呈树结构而无数据或图统计证据。
- 不从单数据集/单预测步推断普遍优势。
- 不使用测试期相关性构图，不把时间点当独立统计样本。
- 不隐藏 DLinear 或 Euclidean GCN 更强的结果。

## C. 重构后的科学问题与论证链

### C1. 研究问题

- **RQ1：** 在具有物理或层级图结构的多节点负荷数据上，双曲图卷积是否优于欧式 GCN 与非图时序基线？
- **RQ2：** 性能变化来自图结构、图卷积还是双曲几何？
- **RQ3：** 曲率、维度、层数和图构造对不同预测跨度与数据集是否稳健？
- **RQ4：** 双曲模型增加的计算复杂度是否换来稳定、统计可辨识的收益？

### C2. 暂定中心论点

> 论文构建一个在双曲流形上进行图消息传递的负荷预测模型，并通过欧式/双曲、真实图/伪图和时序/图组件的正交消融，检验层级结构是否带来可复现的预测收益。

结果允许为负：若 HGCN 不优于欧式 GCN，论文仍应给出结构适用边界，而不是选择性报告某个跨度。

### C3. 论证顺序

负荷序列存在跨节点依赖 → 图卷积利用拓扑但欧式空间对层级扩张可能低效 → 双曲空间是待检验假设 → 实现真实 HGCN → 用正交消融隔离图与几何 → 在滚动时间评估和跨数据集上检验 → 报告收益、成本与失败条件。

## D. 数据与图构造门禁

### D1. 优先数据层级

1. **SimBench 多节点负荷与物理拓扑：** 优先主数据，前提是负荷曲线能可靠映射到母线/支路。
2. **Ausgrid 等真实层级数据：** 可作为第二数据集，需核验 household/feeder/region 层级和许可。
3. **OPSD 跨区域数据：** 仅在可以用公开物理互联图或训练期构造的功能图时作为补充；国家/区域之间的稠密注意力不能冒充物理 GCN。

### D2. 图构造规则

- **物理图：** 由网络拓扑确定，边权可用线路参数但必须说明。
- **层级图：** household—feeder—region 等真实聚合关系。
- **功能图：** 只能用训练窗计算相关/互信息/kNN，验证和测试数据不得参与。
- 每个数据集至少提供节点数、边数、连通分量、度分布、层级/双曲性诊断。
- 随机图、度保持重连图和 identity graph 仅作消融，不能作为领域图证据。

### D3. 门禁通过标准

- 至少一个数据集有无泄漏的可解释图和足够长的节点级负荷序列。
- 欧式 GCN 在该图上能端到端训练，作为实现 sanity check。
- 图边与预测样本时间对齐且缺失值处理可复现。

若无法满足，锁定标题下的执行标记为 `NO-GO`。

## E. 模型重构方案

### E1. 建议架构

`Input features → temporal encoder → hyperbolic graph convolution blocks → temporal/graph readout → multi-horizon decoder`

可执行定义必须包含：

- 从欧式特征到双曲流形的映射（如 exponential map）；
- 在切空间或流形上的邻域聚合；
- 曲率固定或可学习的明确参数化；
- 数值稳定投影与距离计算；
- 映回切空间/欧式输出头预测负荷。

具体实现采用哪一种 HGCN 变体，须在核验原始论文和开源实现后冻结；不能只根据名称复刻公式。

### E2. 时间建模

- 时间编码器可采用轻量 TCN/GRU 或与现有线性编码对齐；所有图模型共享同一时间编码器，保证几何比较公平。
- 明确任务是一步、直接多步还是递归多步；建议直接预测 1/6/12/24 步或预定义多个跨度。
- 日历、天气等外生变量只有在所有数据集可获得并无泄漏时采用；否则保持简洁。

### E3. 复杂度与稳定性

- 记录参数量、训练/推理时间、峰值显存和失败运行。
- 对范数接近边界、NaN、梯度爆炸建立监控。
- 欧式极限/曲率趋零应有数值 sanity check，保证模型比较不是实现缺陷。

## F. 逐章节修改计划

### F1. 标题与首页

- 标题逐字锁定。
- 保持当前 Electronics/MDPI 模板系列；科学结果冻结后再同步最新模板版本和声明字段。
- 作者信息按锁定文本；工作稿按作者要求将未知 ORCID 标为 `NONE`，投稿表单不得将其冒充为真实编号。
- Electronics 路线要求模型贡献、计算实现与实际电力预测任务形成闭环；除模型新意外，稿件需呈现可解释图来源、稳健的实际负荷评价和可复现数据/代码，不能只做合成模型消融。

### F2. Abstract

最后写成：多节点负荷问题 → 双曲图卷积方法 → 数据/图与滚动评估 → 欧式 GCN/强非图基线 → 主要结果含负结果 → 适用边界。

- 必须出现“graph convolution”真实操作和至少一个真实/可解释图数据集。
- 不使用“significantly”除非对应预先冻结检验。
- 结果数字必须来自跨滚动块/种子的正式主表。

### F3. Introduction

建议 6 段：

1. 多区域/多节点负荷预测需要建模时间动态和节点依赖。
2. 非图模型忽略拓扑，欧式 GCN 能传播邻域信息但对层级/指数扩张结构的表示能力是潜在限制。
3. 双曲空间适合层级结构是理论动机，但在负荷预测中是否带来增益不能由表示直觉代替实验。
4. 现有研究常混合更复杂模型、不同图和评估设置，难以归因几何收益。
5. 提出共享时间编码器下的 Euclidean/HGCN 匹配设计、真实图与正交消融。
6. 贡献最多 3 点：真实 HGCN 实现、可归因评估、跨数据/跨度的边界证据。

### F4. Related Work

重写为四节：

1. **Power-load forecasting and strong simple baselines**：统计、线性、RNN/TCN/Transformer，说明为何 DLinear 等必须保留。
2. **Graph neural networks for spatiotemporal forecasting**：GCN、GAT、STGCN/MTGNN 等，区分预定义图与学习图。
3. **Hyperbolic representation learning and graph convolution**：Poincaré embeddings、hyperbolic neural networks、HGCN 的原始工作及数值实现。
4. **Evidence gap in hyperbolic load forecasting**：是否有直接同题工作、用何数据/基线，必须通过系统检索后下结论。

现有 CSA 跨序列文献保留为模型对照，不再充当标题方法的理论来源。

### F5. Data, Graph and Forecasting Task

- 描述每个数据集、许可、时间跨度、采样率、节点和缺失率。
- 单独给出图来源、边定义和训练期构图规则。
- 固定滚动起点、训练/验证/测试窗与归一化；归一化统计只能来自训练窗。
- 定义预测输入长度、跨度、输出形式与评价粒度。
- 说明层级聚合是否用于训练目标或只用于评估。

### F6. Hyperbolic GCN Method

章节顺序：

1. 欧式 GCN 对照与符号。
2. 双曲空间、曲率和映射的最少必要定义。
3. 双曲图卷积/消息传递公式。
4. 时间编码器与多步解码器。
5. 损失函数、优化与稳定投影。
6. 复杂度与欧式极限。

避免写成双曲几何教科书；每个数学定义必须直接服务模型实现。

### F7. Experimental Setup

- 至少 2 个结构不同的数据集；若只能完成一个，明确为 case study。
- 滚动起点评估，建议沿用至少 8 个外层时间块；种子数根据资源预估冻结，最低 5 个，主结论优先依赖外层时间块而非重复种子。
- 主要误差指标建议 WAPE/MAE 中选一个；MAPE 在近零负荷节点需说明处理。
- 统计单位为 rolling origin × dataset（或预定义汇总），不是每个时间点。
- 所有神经基线使用相同输入、调参预算和早停规则。

### F8. Results

1. 数据/图 sanity checks 与结构统计。
2. **主比较：** HGCN、Euclidean GCN、强非图基线，跨数据和跨度。
3. **几何归因：** 双曲 vs 欧式，其他组件完全一致。
4. **图归因：** 真实图、identity、随机/重连、训练期功能图。
5. **曲率与层数：** 固定/学习曲率，1–3 层、维度敏感性。
6. **层级/峰荷性能：** 聚合一致性、峰荷 MAE 等，仅在定义可靠时报告。
7. **效率与稳定性：** 参数、时间、显存、失败率。
8. **失败案例：** 哪些节点、季节或跨度 HGCN 更差。

现有 CSA-Poincaré 结果作为一个独立基线并完整报告其未解决对比；旧稿中 DLinear 的优势必须保留验证。

### F9. Discussion

- 若 HGCN 有效，区分是层级图、曲率还是容量带来的收益。
- 若只在某数据/跨度有效，以结构统计解释但不作因果断言。
- 若无优势，讨论负荷图可能不够双曲、时间误差占主导或欧式容量已足够。
- 讨论训练成本、图获取、动态图、天气外生量和分布漂移。
- 明确模型是离线点预测，不声称调度或安全收益。

### F10. Conclusion

按 RQ1–RQ4 回答：预测表现、几何贡献、稳健性、计算代价。  
不得把“使用双曲空间”本身写成贡献结果；结论必须依赖匹配欧式消融。

## G. 实验执行方案

### G0. 新路径

`paper_projects/mintou_p2_hygraph_load_forecasting/experiments/p2_s4_hyperbolic_gcn_v1/`

现有 `p2_s3_identifiable_v1` 保持只读，作为 CSA 基线。

### G1. Stage 0：数据与文献门禁

- 核验 SimBench/OPSD/Ausgrid 的许可、数据结构和图映射。
- 核验 HGCN 原始论文与一个可靠实现；建立公式—代码对照。
- 生成数据泄漏检查、图统计与资源预算。
- 决定主数据集、第二数据集和主预测跨度，写入冻结配置。

### G2. Stage 1：最小工作模型

- 一个小图/子集、一个预测跨度、3 个种子。
- 先跑 persistence、DLinear、Euclidean GCN、HGCN。
- 单元测试：邻接使用、曲率梯度、exp/log map 数值、shape、无测试构图。
- 欧式极限/identity graph 必须给出合理行为。

### G3. Stage 2：基线与调参

| 组别 | 方法 |
|---|---|
| 简单 | Seasonal persistence、线性/DLinear |
| 时序 | GRU/TCN 中一个资源可控强基线 |
| 图模型 | Euclidean GCN、GAT 或 STGCN 中至少一个 |
| 现有模型 | target-self、CSA-Euclidean、CSA-Poincaré |
| 提出模型 | Hyperbolic GCN |

- 使用验证窗给所有神经模型相近调参预算。
- 不要求堆满模型；优先强、可复现、能回答 RQ 的基线。

### G4. Stage 3：正式评估

- 至少两个数据/图；预测跨度建议 1、6、12、24 中预先冻结若干。
- 至少 5 个种子、多个 rolling origins；资源允许再扩大种子，不用种子替代时间外推。
- 保存每个 origin/seed/node/horizon 的指标和预测，不只保存均值。

### G5. Stage 4：正交消融

- Hyperbolic vs Euclidean（同图、同时间编码器、近似参数量）。
- Real graph vs identity/random/degree-preserving graph。
- Fixed vs learnable curvature；curvature→0 sanity。
- 1/2/3 graph layers、embedding dimension。
- No temporal encoder 或 No graph block，仅用于定位误差来源。
- 若采用 learned graph，严格比较训练期构图和物理图。

### G6. 统计与报告

- 冻结主要比较 `HGCN vs Euclidean GCN` 和主要指标/跨度。
- 按 rolling origin 配对，跨数据给分层结果；报告效应量、bootstrap/配对 CI 和 Holm 校正。
- 多节点指标先按预定义权重汇总，避免把节点数量当虚假样本扩张。
- 结果不一致时按数据结构/跨度报告，不给单一平均掩盖异质性。

## H. 图表蓝图

| 编号 | 内容 |
|---|---|
| Fig. 1 | 数据图—时间编码—双曲图卷积—多步输出架构 |
| Fig. 2 | 欧式与双曲消息传递的匹配比较示意 |
| Fig. 3 | 跨数据/跨度主效应森林图 |
| Fig. 4 | 真实图与伪图消融 |
| Fig. 5 | 曲率/层数敏感性与数值稳定性 |
| Fig. 6 | 代表性节点与峰值时段误差案例 |
| Table 1 | 数据、图、时间划分和许可 |
| Table 2 | 模型组件、参数量和调参预算 |
| Table 3 | 主预测结果与校正统计 |
| Table 4 | 几何/图/曲率消融 |
| Table 5 | 效率、稳定性和失败率 |

## I. 参考文献计划

### I1. 保留并核验

- 负荷预测、DLinear、图时序模型和滚动评估的现有直接文献。
- 当前数据集的官方/原始来源。
- 现有 CSA/Poincaré 距离相关文献仅用于基线定位。

### I2. 必须核验的核心线索

- Poincaré embeddings 的原始工作。
- Hyperbolic neural networks 的原始工作。
- Hyperbolic graph convolutional networks 的原始工作。
- 双曲图神经网络在时间序列/交通/能源预测中的最近邻研究。
- 电力负荷 GCN/STGNN 与 learned graph 的近年强基线。

当前本地审稿笔记中的 Nickel & Kiela、Ganea et al.、Chami et al. 只作为检索线索；题名、年份、版本、DOI 和具体支持内容核验后才可写入。

### I3. 删除/降级

- 把通用双曲表示优点直接外推到负荷预测的宣传性句子。
- 与实际模型未实现的 Möbius/流形操作文献堆叠。
- 只支持“注意力”但被用来证明“图卷积”的引用。

### I4. 引用验收

每个方法公式可追溯到原始来源或明确标为本文设计；每个数据/图有来源；相关工作中的“缺口”经过至少两库检索和去重，不使用未经核实的“first”。

## J. 内部篇幅计划

内部目标约 8,500–10,000 正文词：引言 800–1,000；相关工作 900–1,100；数据/图 1,000；方法 1,600–1,900；实验 1,100；结果 2,000；讨论/局限 900；其余约 600。该数值是内部控制线而非 Electronics 的固定硬限制；投稿前按最新指南核算。现稿约 11.2k 词，原 CSA 细节压缩为基线说明和附录。

## K. Go/No-Go

### GO

- 有至少一个无泄漏、可解释图数据集并成功运行 Euclidean GCN/HGCN。
- 模型包含真实图卷积和双曲映射/聚合，标题与实现一致。
- 几何、图和时间组件通过正交消融归因。
- DLinear、Euclidean GCN 和现有 CSA 基线公平且负结果未隐藏。
- 跨 rolling origins 和至少两个数据/结构完成评估，或明确降级为单案例。

### CONDITIONAL

- HGCN 不优于欧式 GCN：仍可作为严谨边界研究，但摘要和贡献不得写预测提升。
- 只有一个可靠图数据集：可形成 case study，不能声称跨系统普遍性。

### NO-GO

- 继续使用距离注意力冒充 HGCN；或图由测试数据构造；或只与弱基线比较；或标题方法未在代码中实现。

## L. 执行顺序

1. 冻结当前 CSA 稿件和 `p2_s3` 结果。
2. 完成数据/图许可、映射和 HGCN 原始实现核验。
3. 建立 Euclidean GCN 最小基线，再实现 HGCN；完成数值与泄漏测试。
4. 冻结主数据、跨度、指标、滚动起点、种子与调参预算。
5. 运行正式主比较、几何/图/曲率消融和效率评估。
6. 先重写数据图、方法、实验、结果；后写相关工作、引言、摘要和结论。
7. 完成引用审计、Electronics 模板同步、LaTeX/PDF 和投稿前复核。

**作者可能需要提供：** 如果有带母线/馈线拓扑的真实多节点负荷数据，价值最高；若无，先用公开 SimBench/层级数据完成，不能将跨国家相关性图称为真实电网拓扑。
