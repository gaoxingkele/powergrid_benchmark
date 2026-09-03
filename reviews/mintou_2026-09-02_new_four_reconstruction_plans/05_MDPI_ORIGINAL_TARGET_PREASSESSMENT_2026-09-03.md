# 闽投新四篇：原 MDPI 目标期刊预评估与相似论文检索

**评估日期：** 2026-09-03  
**状态：** `PREASSESSMENT / 非录用保证`  
**原 MDPI 映射：** 论文1 → Energies；论文2 → Applied Sciences；论文3 → Energies；论文4 → Electronics。  
**标题约束：** 四个锁定标题逐字不变。  

## 1. 结论摘要

四篇重构后都处于原 MDPI 期刊的正式范围内，而且均找到真实同刊先例。原 MDPI 路线整体比目前另定的 Expert Systems、Security and Communication Networks、Computers & Electrical Engineering 更贴近四篇的“电力应用 + 算法改进”证据形态。

| 论文 | 原 MDPI 期刊 | 范围适配 | 当前证据就绪度 | 完整执行重构后的预评估 | 建议 |
|---|---|---|---|---|---|
| 1 Hybrid MOEA 投资效益 | Energies | 高 | 低—中 | 中—高，有条件可投 | Energies 比 Expert Systems 更自然；优先补成本/AC/外部验证 |
| 2 NDS + 双向局部搜索 | Applied Sciences | 高 | 低—中 | 中—高，有条件可投 | 推荐回到普通电网投资版；无需为期刊强转网络安全 |
| 3 Self-Adaption MODE 配电规划 | Energies | 高 | 低 | 中—高，有条件可投 | 需完成 2×2 自适应归因和动作对齐 AC 规划 |
| 4 Hyperbolic GCN 负荷预测 | Electronics | 高 | 低 | 高适配、有条件可投 | Electronics 有直接 GCN 负荷先例；必须实现真实 HGCN |

“有条件可投”表示在范围和已发表文章类型上成立，不代表编辑或审稿人一定接收。录用仍取决于结果、完整性、重复发表风险、英文质量和编辑判断。

## 2. 官方范围核验

- [Energies Aims & Scope](https://www.mdpi.com/journal/energies/about) 明确覆盖 electrical power systems、smart grids/microgrids，以及 AI in energy-system design and control，并要求数值研究提供可复现细节与敏感性描述。
- [Energies F1: Electrical Power System](https://www.mdpi.com/journal/energies/sections/electrical_power_system) 适合论文1和论文3的规划/电力系统主线；[A1: Smart Grids and Microgrids](https://www.mdpi.com/journal/energies/sections/grids) 适合强调智能优化、DER、储能和配电网情景的版本。
- [Applied Sciences Electrical, Electronics and Communications Engineering](https://www.mdpi.com/journal/applsci/sections/electrical_electronics_communications_engineering) 接收电气工程、微电网、网络和通信方向应用研究；论文2的普通电网投资版和安全投资版都可进入范围，但前者重构风险较低。
- [Electronics Artificial Intelligence](https://www.mdpi.com/journal/electronics/sections/Artificial_Intell) 接收算法型深度学习及组合方法；[Computer Science & Engineering](https://www.mdpi.com/journal/electronics/sections/computer_science_engineering) 明确包含 ML、DL 和 smart grids，适合论文4。

## 3. 检索与判断口径

- 第一遍以锁定标题中的任务和方法词扩展检索：investment effectiveness、power-grid/distribution planning、hybrid/multi-objective evolutionary algorithm、NSGA-II、bidirectional/Pareto local search、self-adaptive differential evolution、graph convolution、hyperbolic/geometric graph、load forecasting。
- 期刊内检索以 MDPI 官方论文页为主，元数据用 Crossref/OpenAlex 交叉核对。
- 引用数为 OpenAlex 在 2026-09-03 的动态快照，仅用于识别传播情况，不作为论文质量或期刊接收依据。
- 相似论文只能证明“主题曾被该刊接收”，不能证明本稿新颖，也不能代替逐篇全文的 Related Work 差异分析。

## 4. 论文1 → Energies

### 4.1 条件性判断

- **范围：高。** 电网投资、组合规划、多目标优化均为 Energies 正常范围。
- **当前直接投稿：低—中。** 120 项目、7 场景、30 种子的计算实验充分，但成本、效益和风险主要是代理量。
- **完整重构后：中—高。** 若增加 action-aligned 测试系统，并完成成本校准或 AC/外部验证，证据形态与同刊论文接近。
- **建议 Section：** 首选 F1 Electrical Power System；若 DER/智能网和多场景成为主线，可选 A1。

锁定标题没有出现 power grid，是初筛风险。不能改标题时，必须在摘要首句、关键词、Section 和 cover letter 中连续使用 `power-grid investment portfolio optimization`。

### 4.2 同刊相似论文

| 论文 | 年份/作者/DOI | OpenAlex 引用 | 相似点 | 本稿必须补出的差异 |
|---|---|---:|---|---|
| [Optimisation Study of Investment Decision-Making in Distribution Networks of New Power Systems—Based on a Three-Level Decision-Making Model](https://www.mdpi.com/1996-1073/18/13/3497) | 2025; Wanru Zhao, Ziteng Liu, Rui Zhang, Mai Lu, Wenhui Zhao; `10.3390/en18133497` | 1 | 配电网投资规模、结构和项目优先级，直接讨论 investment effectiveness | 使用实际年份数据和案例验证；论文1需从代理池走向成本或外部验证 |
| [A Novel Optimization Method for a Multi-Year Planning Scheme of an Active Distribution Network in a Large Planning Zone](https://www.mdpi.com/1996-1073/14/12/3450) | 2021; Xuejun Zheng et al.; `10.3390/en14123450` | 5 | 大型项目库、依赖关系、优先级与投资组合 | 有多年滚动规划和真实配电网案例；论文1当前是静态代理组合 |
| [Comprehensive Evaluation of the Effectiveness of Power Grid Structure Renovation Based on a Hybrid Weighting Method Combining FAHP and EWM](https://www.mdpi.com/1996-1073/19/11/2542) | 2026; Bingjie Jin et al.; `10.3390/en19112542` | 0 | effectiveness、hybrid weighting、敏感性 | 使用电网仿真和多省级场景；论文1需物理有效性证据 |
| [Mid- to Long-Term Distribution System Planning Using Investment-Based Modeling](https://www.mdpi.com/1996-1073/18/14/3702) | 2025; Hosung Ryu, Wookyu Chae, Hongjoo Kim, Jintae Cho; `10.3390/en18143702` | 2 | 投资导向规划和技术约束 | 有实际基础设施、潮流、电压和容量约束 |
| [Multi-Objective Optimization of Hybrid Renewable Energy System Using an Enhanced Multi-Objective Evolutionary Algorithm](https://www.mdpi.com/1996-1073/10/5/674) | 2017; Mengjun Ming, Rui Wang, Yabing Zha, Tao Zhang; `10.3390/en10050674` | 107 | MOEA、偏好选择和成本—可靠性权衡 | 优化变量和能源系统具有物理语义；论文1需同等应用闭环 |
| [Multi-Objective Hybrid Optimization for Optimal Sizing of a Hybrid Renewable Power System for Home Applications](https://www.mdpi.com/1996-1073/16/1/96) | 2023卷; Md. Arif Hossain et al.; `10.3390/en16010096` | 25 | hybrid NSGA-II/GWO、多目标成本与可靠性 | 报告具体成本和失供电概率，不只报告 HV |
| [Multiobjective Approach for Medium- and Low-Voltage Planning of Power Distribution Systems Considering Renewable Energy and Robustness](https://www.mdpi.com/1996-1073/13/10/2517) | 2020; Diogo Rupolo et al.; `10.3390/en13102517` | 7 | 多目标配电规划、投资运行成本和鲁棒性 | 在中低压集成系统上验证并显式处理不确定性 |
| [Multi-Objective Collaborative Optimization of Distribution Networks with Energy Storage and Electric Vehicles Using an Improved NSGA-II Algorithm](https://www.mdpi.com/1996-1073/18/19/5232) | 2025; Runquan He, Jiayin Hao, Heng Zhou, Fei Chen; `10.3390/en18195232` | 6 | 改进 NSGA-II、投资—可靠性—网损目标 | 使用 IEEE 33-bus 和电力物理指标 |

### 4.3 最低接收门槛

1. 一个命名且有电气语义的测试系统，候选项目映射到线路、变压器、储能或自动化动作。
2. 成本校准、AC 后验校验、独立历史项目验证至少完成一项，最好前两项同时完成。
3. 除 HV/IGD+ 外报告投资成本、电压/过载/可行率、预算利用率和成本扰动稳定性。
4. 完成 Full、NoPreference、NoRepair、NDS-only 与 NSGA-II/R-NSGA-II/MOEA/D 的归因。
5. 保留偏好模块未解决和归一化改变排名的结果。

### 4.4 主要拒稿风险

- `Investment effectiveness` 只有无量纲代理含义。
- `Hybrid` 像组件拼接，偏好模块没有独立增益。
- 0.89% 左右的 HV 差异缺少工程效应解释。
- 与论文2共享项目池/生成器，存在重复发表或最小发表单元风险。

## 5. 论文2 → Applied Sciences

### 5.1 条件性判断

- **范围：高。** 电网项目配置、应用型多目标算法和局部搜索均有同刊先例。
- **当前直接投稿：低—中。** 等预算结果下 BiLo 未优于 NSGA-II，单一代理池也缺少独立应用价值。
- **普通电网投资重构后：中—高，推荐。** 增加第二问题族、真实成本/可靠性验证与方向消融即可形成 Applied Sciences 风格稿件。
- **安全投资重构后：中。** 范围仍合适，但数据干预和标题匹配成本更高；若选择 Applied Sciences，无需为了期刊而强制安全化。
- **建议 Section：** 普通版优先 Energy Science and Technology；安全版可选 Electrical, Electronics and Communications Engineering。

### 5.2 同刊相似论文

| 论文 | 年份/作者/DOI | OpenAlex 引用 | 相似点 | 关键差异 |
|---|---|---:|---|---|
| [Critical Cluster Mining and Optimal Allocation for Power Grid Projects Based on Complex Networks and Multidimensional Metrics](https://www.mdpi.com/2076-3417/15/16/9166) | 2025; Minghong Liu, Shuxu Chen, Xianing Jin, Wenxin Mu, Huan Zhang; `10.3390/app15169166` | 0 | 最直接的电网项目、投资有效性、多指标和项目配置先例 | 用复杂网络和聚类，未使用 NDS+双向局部搜索 |
| [Robust Dynamic Co-Planning of Distribution Feeders and Virtual Distribution Feeders Considering Emergency Rating and Battery Degradation](https://www.mdpi.com/2076-3417/16/9/4567) | 2026; Tao Lu, Yongjie Luo, Yuan Chi, Luona Xu; `10.3390/app16094567` | 0 | 多目标配电规划、投资成本、NSGA-II | 有 IEEE 33-bus、储能退化和多年约束 |
| [Optimal Placement of Multiple Feeder Terminal Units Using Intelligent Algorithms](https://www.mdpi.com/2076-3417/10/1/299) | 2020卷; Dan Lin et al.; `10.3390/app10010299` | 6 | 电网设备投资、生命周期成本与可靠性 | 是具体 FTU 和 RBTS Bus 5 工程算例 |
| [Capacity-Operation Collaborative Optimization for Wind-Solar-Hydrogen Multi-Energy Supply System](https://www.mdpi.com/2076-3417/13/19/11011) | 2023; Lintong Liu et al.; `10.3390/app131911011` | 14 | NSGA-II+LP、投资容量和多目标工程优化 | 连续容量—运行设计，不是离散项目组合 |
| [A Hybrid Multi-Objective Optimization Method and Its Application to Electromagnetic Device Designs](https://www.mdpi.com/2076-3417/12/23/12110) | 2022; Zhengwei Xie, Yilun Li, Shiyou Yang; `10.3390/app122312110` | 7 | hybrid multi-objective、全局/局部平衡 | 电磁设备应用，无投资预算语义 |
| [Pareto Local Search Guided by Archive Entropy](https://www.mdpi.com/2076-3417/16/2/964) | 2026; Shuangshuang Yao et al.; `10.3390/app16020964` | 0 | 多目标组合局部搜索、HV/IGD，与方法最接近 | 25 个基准、9 个强基线、21 次运行和 Friedman，显示算法稿的比较门槛 |
| [An Adaptive Multiobjective Genetic Algorithm with Multi-Strategy Fusion for Resource Allocation in Elastic Multi-Core Fiber Networks](https://www.mdpi.com/2076-3417/12/14/7128) | 2022; Zhanqi Xu et al.; `10.3390/app12147128` | 4 | 非支配算法、策略融合和通信资源分配 | 光网络资源配置，不是电网资本投资 |
| [A Multi-Objective Genetic Algorithm–Deep Reinforcement Learning Framework for Spectrum Sharing in 6G Cognitive Radio Networks](https://www.mdpi.com/2076-3417/15/17/9758) | 2025; Ancilla Wadzanai Chigaba et al.; `10.3390/app15179758` | 11 | NSGA-II、局部策略细化、网络多目标配置 | 实时频谱分配，不是离线投资组合 |

### 5.3 推荐改造路线

若回到 Applied Sciences，将原论文2计划中的安全重构改为可选分支。主线建议保留普通电网项目投资：

1. 保留现有 120 项目、8 场景、30 配对种子及全部负结果。
2. 增加一个独立设备/项目配置问题族，不能只是同一生成器换参数。
3. 成本使用 LCC、NPV 或有来源的归一化校准。
4. 增加 AC、可靠性、历史项目或专家排序中的一个真实验证层。
5. 比较 NSGA-II、一个分解式 MOEA、PLS、简单工程决策法；小实例尽量加入精确/ε-constraint 参照。
6. 隔离 NDS-only、forward-only、backward-only、bidirectional 和 NoAtomicSubstitution。
7. 等评价预算为主、等时间为辅，报告效应量、CI 和未解决结果。

### 5.4 主要拒稿风险

- 现有 BiLo 比 NSGA-II 低约 5.44%，八场景无平均胜场；如果无新机制解释或应用价值，算法贡献不足。
- 标题未出现 power grid，且 `Evolution Algorithm` 不如 `Evolutionary Algorithm` 常见；锁题时需靠摘要、关键词和 cover letter 补足。
- 论文1和论文2共享生成器、任务与部分实验，必须建立明确且可审计的科学差异。

## 6. 论文3 → Energies

### 6.1 条件性判断

- **范围：高。** 配电规划、DER/储能、智能优化和 adaptive DE 都有明确先例。
- **当前直接投稿：低。** 当前仍是 SimBench-derived portfolio proxy，自适应机制不可识别，AC 只是示意性组合检查。
- **完整重构后：中—高。** 2×2 机制归因、真实规划动作、至少一个/最好两个 AC 网络和多情景完成后可达到正常门槛。
- **建议 Section：** 真实配电规划主线投 F1；高 DER/储能/智能网主线投 A1。

### 6.2 同刊相似论文

| 论文 | 年份/作者/DOI | OpenAlex 引用 | 相似点 | 本稿启示 |
|---|---|---:|---|---|
| [Integration of Renewable Based Distributed Generation for Distribution Network Expansion Planning](https://www.mdpi.com/1996-1073/15/4/1378) | 2022; Mulusew Ayalew et al.; `10.3390/en15041378` | 33 | 配电扩展、DG 选址定容、规划情景 | 使用实际馈线、负荷预测和 ETAP 潮流；真实动作很重要 |
| [Optimal Allocation of Distributed Generators in Active Distribution Networks Using a New Oppositional Hybrid Sine Cosine Muted Differential Evolution Algorithm](https://www.mdpi.com/1996-1073/15/6/2267) | 2022; Subrat Kumar Dash et al.; `10.3390/en15062267` | 24 | 最接近：DE 变体、DG 配置和多目标配电问题 | 33/118/136 节点、多情景、潮流、算法比较和统计，构成直接实验参照 |
| [Active Distribution Network Expansion Planning Based on Wasserstein Distance and Dual Relaxation](https://www.mdpi.com/1996-1073/17/12/3005) | 2024; Jianchu Liu et al.; `10.3390/en17123005` | 4 | 主动配电扩展、DG/负荷不确定性和运行约束 | 不确定性和约束完整性高于当前代理模型 |
| [A Novel Optimization Method for a Multi-Year Planning Scheme of an Active Distribution Network in a Large Planning Zone](https://www.mdpi.com/1996-1073/14/12/3450) | 2021; Xuejun Zheng et al.; `10.3390/en14123450` | 5 | 多年规划、项目选择和优先级 | 若没有节点/线路/容量动作，难称 planning |
| [Distribution Power Loss Reduction of Standalone DC Microgrids Using Adaptive Differential Evolution-Based Control for Distributed Battery Systems](https://www.mdpi.com/1996-1073/13/9/2129) | 2020; Junli Deng, Yuan Mao, Yun Yang; `10.3390/en13092129` | 24 | adaptive DE 与电网/储能结合 | 有明确适应机制和 RTDS 验证，说明 adaptive 标签需要物理证据 |
| [Wind-Photovoltaic-Energy Storage System Collaborative Planning Strategy Considering the Morphological Evolution of the Transmission and Distribution Network](https://www.mdpi.com/1996-1073/15/4/1481) | 2022; Defu Cai et al.; `10.3390/en15041481` | 5 | 风光储、配电规划、经济—运行目标 | 同时建立 AC/DC 潮流与规划效果 |
| [A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience](https://www.mdpi.com/1996-1073/19/2/574) | 2026; Yitong Chen et al.; `10.3390/en19020574` | 4 | 储能选址定容、多情景、韧性 | 近期规划稿更重视不确定性和多层工程解释 |

### 6.3 最低接收门槛

1. 将现有共用开关拆为 parameter adaptation 与 strategy adaptation，完成 Fixed–Fixed、Adaptive–Fixed、Fixed–Adaptive、Adaptive–Adaptive 四臂实验。
2. 决策变量对应线路、变压器、DER/储能节点和容量等真实规划动作。
3. 至少一个明确 AC 网络；鉴于当前证据冲突，建议两个拓扑不同的网络。
4. 基准、峰荷、负荷增长、高 DER 至少四类情景；保留可靠性目标时增加故障/N-1 证据。
5. Full-SAMODE、Fixed-Fixed、GDE3/NSDE、NSGA-II 使用相同目标函数、初始种子和目标/潮流调用预算。
6. 同时报告 HV、IGD+、参考点、可行前沿比例、电压/热限、损耗、投资与计算代价；完整披露指标排名反转。

### 6.4 主要拒稿风险

- `Self-Adaption` 不是最常见英文形式，严格锁题会留下语言印象风险。
- FixedDE 当前名义更优，自适应贡献未识别。
- 组合到网络的二次映射不是 action-aligned planning。
- sampled/clipped HV 有利而 analytic HV/IGD+ 排名变化，容易引发指标选择质疑。

## 7. 论文4 → Electronics

### 7.1 条件性判断

- **范围：高。** Electronics 的 AI、Computer Science & Engineering 和 Systems & Control 版块均覆盖 ML、smart grids、预测与电气系统应用。
- **当前直接投稿：低。** 当前 CSA-Poincaré 距离注意力不是 GCN，与锁定标题直接矛盾。
- **完成真实 HGCN 重构后：高适配。** 期刊已有多篇 GCN 负荷/交通预测论文，也已发表使用双曲映射的 geometric graph learning 工作。
- **建议 Section：** 首选 Artificial Intelligence；若稿件突出图系统与 smart grid，可选 Computer Science & Engineering。没有控制闭环时不优先投 Systems & Control。

### 7.2 同刊相似论文

| 论文 | 年份/作者/DOI | OpenAlex 引用 | 相似点 | 本稿可形成的差异 |
|---|---|---:|---|---|
| [Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting](https://www.mdpi.com/2079-9292/14/16/3332) | 2025; Jiarui Li, Jian Li, Jiatong Li, Guozheng Zhang; `10.3390/electronics14163332` | 3 | GCN + 时序模型 + power-load forecasting，直接题材先例 | 使用相关图和欧式 GCN；论文4可用真实图和双曲/欧式匹配归因 |
| [GCN-Transformer-Based Spatio-Temporal Load Forecasting for EV Battery Swapping Stations under Differential Couplings](https://www.mdpi.com/2079-9292/13/17/3401) | 2024; Xiao Hu et al.; `10.3390/electronics13173401` | 11 | GCN、空间—时间负荷预测、图生成 | EV 换电站场景；论文4需证明双曲空间而非模型堆叠产生增益 |
| [Spatiotemporal Forecasting of Regional Electric Vehicles Charging Load: A Multi-Channel Attentional Graph Network Integrating Dynamic Electricity Price and Weather](https://www.mdpi.com/2079-9292/14/20/4010) | 2025; Hui Ding, Youyou Guo, Haibo Wang; `10.3390/electronics14204010` | 7 | 图网络、区域负荷、短期/24h、多源特征 | 论文4可以无泄漏物理/层级图与几何消融形成区别 |
| [Dynamic Spatio-Temporal Hypergraph Convolutional Network for Traffic Flow Forecasting](https://www.mdpi.com/2079-9292/13/22/4435) | 2024; Zhiwei Ye et al.; `10.3390/electronics13224435` | 10 | 图卷积、非欧式结构、时空预测 | 交通而非电力；是预测实验与图消融的邻近方法先例 |
| [Geometric Graph Learning Network for Node Classification](https://www.mdpi.com/2079-9292/15/3/696) | 2026; Lei Wang, Xitong Xu, Zhuqiang Li; `10.3390/electronics15030696` | 0 | Electronics 已接收 Poincaré 映射和双曲图特征学习 | 节点分类而非负荷预测；论文4需给真正时间外推和 HGCN |

本轮以 Electronics + hyperbolic/HGCN + load forecasting 的组合检索没有发现标题和任务同时完全重合的论文；这只能说明当前检索集未发现完全同题，不能宣称“首次”。一方面存在潜在差异化空间，另一方面审稿人会要求更强的 Euclidean GCN 匹配消融。

### 7.3 最低接收门槛

1. 实现真实图卷积和双曲映射/聚合，不得把 Poincaré 距离注意力改名为 HGCN。
2. 至少一个有物理或真实层级拓扑的数据集，最好两个不同结构的数据集。
3. HGCN 与 Euclidean GCN 使用相同图、时间编码器、调参预算和近似参数量。
4. 保留 persistence、DLinear、时序网络、Euclidean GCN、现有 CSA-Euclidean/Poincaré 基线。
5. 做 real graph/identity/random graph、fixed/learnable curvature、层数与维度的正交消融。
6. 多个 rolling origins 和多个预测跨度；统计单位不能是逐时间点。
7. 报告 MAE/WAPE/RMSE 等误差、参数量、训练/推理时间、显存与数值失败。
8. 完整保留当前 Poincaré 权重未解决和 DLinear 更优的旧结果。

### 7.4 主要拒稿风险

- 标题方法未真正实现，是当前最严重硬伤。
- 图由测试期数据构造或把跨区域相关性图称为物理拓扑。
- HGCN 只是扩大模型容量，未用匹配欧式消融隔离几何贡献。
- 只与弱基线比较，或隐藏 DLinear/Euclidean GCN 更优的结果。

## 8. 四篇转回 MDPI 后的执行调整

### 8.1 论文1

保留现有重构计划，但投稿叙事从“expert preference system”调整为“power-grid investment portfolio planning”。专家用户研究由强制项降为可选项，成本/AC 验证升为首要项。

### 8.2 论文2

将安全投资 Phase 0 从强制主线改为可选扩展。主线重新冻结为普通电网投资组合：第二独立问题族 + 真实成本/可靠性 + 双向机制归因。这样能够显著降低重构风险。

### 8.3 论文3

科学计划基本不变。Energies 对 action-aligned 配电规划适配很高，但必须完成 2×2 机制与 AC 多场景，不可只做措辞迁移。

### 8.4 论文4

科学计划基本不变。目标期刊改回 Electronics 后，模型/系统贡献比“专家系统”叙事更自然；仍必须完成真实 HGCN。

## 9. 推荐优先级

1. **论文1 → Energies：** 最接近可投稿，先补投资/电气验证。
2. **论文3 → Energies：** 代码开关拆分后推进 action-aligned AC 规划。
3. **论文4 → Electronics：** 完成实际 HGCN 和图数据门禁，训练成本较高。
4. **论文2 → Applied Sciences：** 先决定普通电网投资版；不要同时维护普通版和安全版两套主稿。

## 10. 最终预评估

- 原 MDPI 期刊 **都能接收这些研究类型**，同刊相似论文充分证明范围先例。
- 当前四篇仍不能直接投稿；问题集中在标题对应证据不足，而不是页数或模板。
- 完整执行现有重构计划并按第 8 节调整后，四篇均可进入正式 MDPI 投稿候选，其中论文1、3、4的原 MDPI 目标比目前另定期刊更自然。
- 论文2若回到 Applied Sciences，建议立即取消“为了期刊而安全化”的强制路线，保留安全方向为未来独立论文，避免主张、数据和代码同时失控。
