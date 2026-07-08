# 电网公开数据集、Benchmark 与仿真环境整理

更新日期：2026-04-07

## 0. 后续工作开展方案

围绕后续新论文选题、实验设计和 baseline 约束，数据集与仿真资源的准备工作建议按“先易后难、先 benchmark 后真实数据、先通用 baseline 后专题 baseline”的顺序开展。

### 0.1 第一阶段：优先建立可立即复用的 benchmark 与基础工具链

第一阶段的目标不是把所有公开数据一次性下全，而是先建立一套能够稳定支撑大多数电网论文选题的基础资源池。优先级最高的资源包括：

1. `MATPOWER case files`
2. `pandapower test cases`
3. `PGLib-OPF`
4. `SimBench`
5. `Grid2Op`
6. `TAMU synthetic grids`

这批资源的共同特点是公开、稳定、复用率高、适合方法论文，而且下载和接入成本相对较低。实际工作中，应先把这些 benchmark 按统一目录缓存下来，记录来源、版本、下载时间和适用任务，作为后续所有选题的默认候选资源。

与此同步，应建立一套基础 baseline 工具链，优先覆盖以下几类：

1. 传统机器学习：`Random Forest`、`SVM`、`KNN`、`Logistic Regression`
2. GBDT 类：`XGBoost`、`LightGBM`
3. 深度学习：`MLP`、`LSTM`、`Transformer`
4. 多目标优化：`NSGA-II`、`MOEA/D`、`MOPSO`
5. 电网物理基线：`LODF/PTDF`、规则法、经典 OPF/PF 求解

第一阶段的核心交付物不是论文，而是：

1. benchmark 可直接调用
2. baseline 可以快速复用
3. 新论文 idea 出来后，能够立即完成 dataset whitelist 和 baseline whitelist 的收敛

### 0.2 第二阶段：补充真实时序与市场数据

在 benchmark 与基础 baseline 已经稳定之后，再进入真实数据准备阶段。优先补充的资源包括：

1. `EIA Open Data`
2. `Open Power System Data`
3. `NREL NSRDB`
4. `ENTSO-E Transparency Platform`
5. `PJM Data Miner 2`
6. `ACN-Data`

这一阶段的重点不只是“下载成功”，而是建立清晰的数据消费链，包括：

1. 访问方式：直接下载、注册、API key 或 token
2. 时间粒度：5 分钟、15 分钟、小时级、日级
3. 空间粒度：站点级、节点级、区域级、系统级
4. 字段口径：负荷、价格、出力、天气、设备状态分别如何定义
5. 清洗流程：缺失值、异常值、重采样、时间对齐

真实数据的主要难点通常不在下载本身，而在口径统一和可复现处理。因此，这一阶段应当把“原始数据缓存 + 清洗脚本 + 字段说明”视为一个整体准备，而不是只保存原始文件。

### 0.3 第三阶段：专题化数据与专业 baseline

对于设备诊断、PMU、DGA、配电网事件识别、EV 充电等专题方向，再按课题需要扩展专门资源。优先对象包括：

1. `Public DGA datasets`
2. `IEC TC10`
3. `Synthetic PMU Data (TAMU)`
4. `Distribution PMU Data Set`
5. `Pecan Street Dataport`

这类资源通常存在以下问题：

1. 标签空间不统一
2. 来源分散
3. 访问权限不完全一致
4. 论文里常用的 baseline 需要额外手工实现

因此，这一阶段应采用“按专题逐个攻克”的策略，而不是一次性大规模铺开。每进入一个新方向，都应同步明确：

1. 主数据集是否真实公开且可持续获取
2. 传统 baseline 是否存在
3. ML/DL baseline 是否能用现有工具链快速复用
4. 是否存在必须手工实现的行业规则法

### 0.4 建议的执行顺序

后续准备工作建议按以下顺序推进：

1. 先固定通用 benchmark：MATPOWER、pandapower、PGLib-OPF、SimBench、Grid2Op、TAMU
2. 再固定通用 baseline：sklearn、xgboost、lightgbm、pymoo、torch
3. 然后补真实开放时序数据：EIA、OPSD、NSRDB、ENTSO-E、PJM、ACN
4. 最后按专题补设备诊断、PMU、EV、用户侧等专门数据

这一顺序的原因在于：

1. benchmark 最容易准备，且对方法论文支撑最强
2. baseline 工具链一旦准备好，可在多个方向复用
3. 真实数据下载之后还需要较长的数据清洗和口径整理周期
4. 专题数据往往最分散，前置投入最大，不适合作为起步阶段的主战场

### 0.5 后续整理时应形成的固定资产

围绕每一类资源，建议最终沉淀以下固定资产：

1. 数据入口记录：官方链接、访问方式、版本、下载日期
2. 本地缓存路径：原始数据、处理中间文件、最终可用文件
3. 字段口径说明：变量含义、单位、时间粒度、标签定义
4. baseline 池：该任务方向下必须比较和可选比较的方法
5. research policy 约束模板：`dataset_whitelist`、`baseline_whitelist`、`selection_rules`

真正需要长期维护的不是单篇论文的临时资料，而是这套可以不断扩展的“公开资源底库”。

## 摘要

电网研究所依赖的公开资源并不只是狭义的数据集，还包括标准网络算例、公开 benchmark 库、交互式仿真环境、开源仿真平台，以及与其配套的市场、负荷、气象、用户侧和设备监测数据。实际论文写作中，如果只检索带有 `dataset` 关键词的资源，往往会遗漏最常用的实验基础设施，例如 IEEE 标准算例、MATPOWER/pandapower 案例库、PGLib-OPF、SimBench、Grid2Op、TAMU synthetic grids 和 PyPSA-Eur。本文围绕电网方向中最常见、复用度最高、公开可获取的资源，系统整理公开数据集、benchmark、仿真环境与代表性平台，并结合 2024-2026 年代表性论文，给出可直接用于后续选题、实验设计和 baseline 约束的资料底稿。

## 1. 整理口径

本文将公开研究资源划分为四类：

1. 公开数据集：真实运行、市场、气象、用户侧、设备监测与故障诊断数据
2. Benchmark 与标准网络算例：IEEE test cases、PGLib-OPF、SimBench、TAMU synthetic grids 等
3. 交互式仿真环境：Grid2Op/L2RPN 等面向控制与强化学习的环境
4. 仿真与优化平台：MATPOWER、pandapower、PyPSA、OpenDSS、ANDES 等

“公开”按实际可获取方式区分为：

1. 完全开放下载
2. 免费注册或 API key 后可访问
3. 有公开入口但带一定权限或条款限制

## 2. 公开数据集与 Benchmark 总览

### 2.1 标准网络算例与 benchmark 库

这类资源是电网方法论文中使用频率最高的实验基础设施。它们未必是真实运行数据库，但高度标准化、可复现、易比较，是算法论文最常见的实验载体。

| 资源 | 类型 | 系统层级 | 典型任务 | 特点 |
|---|---|---|---|---|
| IEEE Standard Test Cases | 标准算例 | Transmission | PF、OPF、ED、安全分析 | 14/30/39/57/118/300-bus 是最常见基准 |
| MATPOWER Case Files | 开源案例库 | Transmission | PF、OPF、ED、算法验证 | 电力系统研究最经典的开放入口之一 |
| pandapower Test Cases | Python 案例库 | Transmission / Distribution | PF、contingency、SE、OPF | 适合 Python 工作流，案例调用方便 |
| PGLib-OPF | OPF benchmark 库 | Transmission | AC OPF、松弛算法、求解器对比 | 当前 OPF 论文最常用 benchmark 之一 |
| Power Grid Lib | benchmark 组织 | 多层级 | benchmark 汇总与验证 | PGLib-OPF 只是其代表子库之一 |
| SimBench | benchmark + 全年 profile | Transmission / Distribution | 时序仿真、配电网监测、控制 | 从 LV 到 EHV，适合稳态与时间序列研究 |
| TAMU ACTIVSg / Electric Grid Test Cases | 合成电网 benchmark | Transmission | 大系统 OPF、动态分析、PMU 研究 | 覆盖数百到数万节点的 synthetic grids |
| Grid2Op / L2RPN Cases | 交互式环境数据 | Transmission | RL、拓扑控制、韧性研究 | 更适合作为 sequential decision benchmark |

这一类资源的共同价值在于：

1. 社区高频复用
2. 结果可对比
3. 获取门槛低
4. 非常适合做方法论文

### 2.2 运行、市场、负荷、气象与可再生能源数据

这类资源更适合做负荷预测、价格预测、新能源出力预测、电力市场分析和系统运行实证研究。

| 资源 | 区域 | 数据内容 | 典型任务 | 获取方式 |
|---|---|---|---|---|
| EIA Open Data | 美国 | 发电、负荷、燃料、电力统计 | 负荷建模、系统分析、能源统计 | API |
| ENTSO-E Transparency Platform | 欧洲 | 运行与市场透明度数据 | 价格预测、跨区运行、市场分析 | 注册/API |
| PJM Data Miner 2 | 美国 PJM | 市场与运行数据 | LMP、负荷、可再生出力、市场分析 | Web/注册 |
| Open Power System Data | 欧洲 | 负荷、电价、风光、机组数据 | 时序预测、市场研究、能源建模 | 直接下载 |
| NREL NSRDB | 全球/美国重点 | 辐照与气象时序 | 光伏出力预测、可再生能源并网 | API |
| DOE OEDI / OpenEI | 美国为主 | 多种能源数据与工具 | 开放能源建模、复现实验 | 数据门户 |

其中，`Open Power System Data` 在欧洲开放时序建模中非常重要，`EIA`、`ENTSO-E` 与 `PJM` 更适合做具有行业背景的实证型研究，`NSRDB` 是新能源与天气驱动建模的核心公开入口之一。

### 2.3 配电网、用户侧与电动汽车数据

这类资源主要服务于需求响应、住户能耗建模、EV 充电调度与配电网协同控制。

| 资源 | 类型 | 典型任务 | 特点 |
|---|---|---|---|
| Pecan Street Dataport | 住户侧高分辨率能耗数据 | DR、NILM、DER 行为建模 | 公开入口明确，但通常需注册或权限 |
| ACN-Data | EV charging sessions | 充电调度、站点运营、价格响应 | EV 充电研究中最具代表性的公开资源之一 |
| SimBench LV/MV feeders | benchmark feeder + profile | 配电网监测、状态估计、控制 | 标准化程度高，适合方法比较 |
| OpenDSS feeder cases | 配电网 feeder 数据 | QSTS、Volt-VAR、DER hosting | 常与 OpenDSS 平台一起出现 |

### 2.4 设备监测、PMU 与故障诊断数据

在设备诊断、事件识别和状态感知方向，公开数据普遍比 transmission benchmark 更稀缺，也更分散。

| 资源 | 类型 | 典型任务 | 备注 |
|---|---|---|---|
| Public DGA Datasets | 设备诊断数据 | 变压器故障分类、规则法/ML 对比 | 常分散在 GitHub、IEEE DataPort、论文附录 |
| Synthetic PMU Data (TAMU) | 合成 synchrophasor 数据 | 事件检测、振荡分析、异常识别 | 适合方法 benchmark |
| Distribution PMU Data Set | PMU/μPMU 数据 | 配电网监测、事件检测、状态估计 | 更适合 distribution monitoring |
| IEEE PES ISS Open Data Sets | 数据聚合入口 | 电力数据发现与复用 | 更像导航页，不是单一数据集 |

这一类资源整理时需要特别注意：

1. 区分真实数据与合成数据
2. 区分长期可复用 benchmark 与单篇论文附带数据
3. 明确标签空间、时间跨度与开放方式

### 2.5 合成电网与交互式环境

这类资源近几年增长很快。它们不直接对应单一现实数据库，但非常适合做可复现实验和控制研究。

| 资源 | 适合问题 | 特征 |
|---|---|---|
| TAMU synthetic grids / ACTIVSg | 大系统 OPF、动态仿真、PMU、韧性研究 | 大规模、无敏感真实基础设施信息 |
| Grid2Op / L2RPN | RL、电网控制、故障恢复 | 顺序决策标准环境 |
| PyPSA-Eur / PyPSA-USA | 规划、扩容、跨能源耦合 | 开放工作流与数据处理链 |
| SimBench | 配电网监测、控制、时序模拟 | 标准化网络 + 年度曲线 |

## 3. 仿真算法与平台整理

### 3.1 主要算法类别

| 算法类别 | 核心问题 | 常见输出 | 典型应用 |
|---|---|---|---|
| AC/DC Power Flow | 给定拓扑与注入求稳态运行点 | 电压、潮流、损耗 | 稳态分析、基态检查 |
| Economic Dispatch | 给定负荷分配机组出力 | 出力、成本、排放 | 调度优化 |
| Optimal Power Flow | 在物理约束下优化运行目标 | 最优调度、网络运行点 | 运行优化、求解器对比 |
| Security / Contingency Analysis | 评估 N-1 故障后系统安全性 | 越限、风险指标、过载信息 | 安全筛选、SCOPF |
| Dynamic / Transient Stability | 扰动后系统动态过程分析 | 电压轨迹、角差、转速 | 暂态稳定、小信号分析 |
| Distribution QSTS / Volt-VAR | 长时段配电网运行模拟 | 电压、无功、设备负荷 | DER 接入、调压、hosting capacity |
| RL / GNN / Hybrid Physics-ML | 学习控制策略或近似映射 | 控制动作、代理模型、策略 | 电网控制、加速仿真、辅助决策 |

当前研究趋势并不是单独使用某一类算法，而是将物理仿真与数据驱动模型结合。例如，先用潮流或 OPF 生成结构化样本，再用 ML 做快速近似，最后回到仿真平台验证。

### 3.2 代表性平台

| 平台 | 类型 | 强项 | 局限 |
|---|---|---|---|
| MATPOWER | 开源经典工具 | PF/OPF/ED 经典、文献覆盖广 | 更偏 transmission 和稳态 |
| pandapower | Python 工具链 | Python 生态友好、contingency/SE/time series 方便 | 大规模优化不如专门优化框架灵活 |
| PowerModels.jl | 优化框架 | OPF 建模灵活、适合 JuMP 生态 | 依赖 Julia 生态 |
| PyPSA | 开放规划与运行框架 | ED、LOPF、SCLOPF、扩容规划 | 更偏系统规划与线性优化 |
| OpenDSS | 配电网仿真平台 | DER、QSTS、feeder 研究高频 | 更偏配电侧 |
| DSS-Extensions | OpenDSS 跨语言生态 | 自动化批量实验方便 | 本身不是独立求解器 |
| Grid2Op | 交互式环境 | RL 与顺序决策 benchmark | 不是传统潮流/OPF 平台 |
| ANDES | 开源动态仿真器 | 暂态稳定、小信号、自动化研究 | 社区规模小于商业平台 |
| OpenIPSL | Modelica 模型库 | 动态元件建模规范化 | 更像组件库而非一体化平台 |
| PowSyBl | 欧洲互操作框架 | load flow、安全分析、CIM/CGMES 兼容 | 国内研究使用频率相对较低 |
| PSS/E | 商业工业标准 | Transmission 规划与动态研究影响大 | 闭源、授权成本高 |
| DIgSILENT PowerFactory | 商业综合平台 | PF、RMS、EMT、保护多功能 | 闭源、自动化批量实验成本高 |
| PSCAD | 商业 EMT 平台 | 电力电子、HVDC、并网 EMT 研究 | 更聚焦 EMT |

### 3.3 当前资源使用趋势

截至 2026 年 4 月，电网领域资源使用趋势可以概括为以下几条：

1. Transmission 优化论文越来越依赖 `PGLib-OPF + MATPOWER/PowerModels` 组合。
2. 配电网研究越来越依赖 `OpenDSS`、`pandapower`、`SimBench` 这类可脚本化平台。
3. 规划与跨能源系统研究明显向 `PyPSA-Eur / PyPSA-USA` 这类开放工作流聚集。
4. 强化学习与 AI 控制研究越来越把 `Grid2Op` 视为标准环境，而不是自建封闭环境。

## 4. 2024-2026 年代表性论文

下面列出的论文不是穷尽列表，而是说明这些公开资源在近三年仍处于活跃使用状态。

### 4.1 PGLib-OPF / OPF benchmark

1. Ruan and Shi, *An Enhanced Semidefinite Relaxation Model Combined with Clique Graph Merging Strategy for Efficient AC Optimal Power Flow Solution*, 2024  
   链接：https://arxiv.org/abs/2409.19609

2. Bugosen, Parker, Coffrin, *Applications of Lifted Nonlinear Cuts to Convex Relaxations of the AC Power Flow Equations*, 2024  
   链接：https://arxiv.org/abs/2404.17541

3. Hasanzadeh, Kargarian, Lavaei, *All-Pass Fractional OPF*, 2026  
   链接：https://arxiv.org/abs/2601.14468

### 4.2 Grid2Op / 强化学习电网控制

1. Peter and Korkali, *Robust Defense Against Extreme Grid Events Using Dual-Policy Reinforcement Learning Agents*, 2024  
   链接：https://arxiv.org/abs/2411.11180

2. Fabrizio et al., *Power Grid Control with Graph-Based Distributed Reinforcement Learning*, 2025  
   链接：https://arxiv.org/abs/2509.02861

### 4.3 SimBench / 配电网 benchmark

1. Grafenhorst, Förderer, Hagenmeyer, *Distribution grid monitoring based on feature propagation using smart plugs*, 2024  
   链接：https://link.springer.com/article/10.1186/s42162-024-00427-y

### 4.4 PyPSA-Eur / 开放规划模型

1. Glaum, Neumann, Brown, *Offshore power and hydrogen networks for Europe's North Sea*, 2024  
   链接：https://arxiv.org/abs/2404.09721

2. Gallego-Castillo and Victoria, *PyPSA-Spain: an extension of PyPSA-Eur to model the Spanish energy system*, 2024  
   链接：https://arxiv.org/abs/2412.06571

3. Lindner et al., *PyPSA-DE: Open-source German energy system model reveals savings from integrated planning*, 2025  
   链接：https://arxiv.org/abs/2510.09414

### 4.5 ACN-Data / 用户侧与 EV 调度

1. Nguyen, Pham, Do, *A Cost-Optimization Model for EV Charging Stations Utilizing Solar Energy and Variable Pricing*, 2025  
   链接：https://arxiv.org/abs/2509.12214

### 4.6 OpenDSS / 配电网控制

1. *A Multi-Area Architecture for Real-Time Feedback-Based Optimization of Distribution Grids*, 2024  
   链接：https://arxiv.org/abs/2401.09694

### 4.7 ANDES / 动态仿真与 AI

1. *LLM-Driven Transient Stability Assessment: From Automated Simulation to Neural Architecture Design*, 2025  
   链接：https://arxiv.org/abs/2511.20276

## 5. 不同研究方向的优先资源

### 5.1 调度优化与 OPF

优先资源：

1. IEEE Standard Test Cases
2. MATPOWER Case Files
3. PGLib-OPF
4. PowerModels.jl

常见 baseline：

1. NSGA-II
2. MOEA/D
3. MOPSO
4. NSGA-III
5. SPEA2

### 5.2 N-1 安全评估与安全筛选

优先资源：

1. pandapower Test Cases
2. IEEE 14/39/118-bus
3. TAMU synthetic grids

常见 baseline：

1. LODF linear screening
2. Random Forest
3. XGBoost
4. LightGBM
5. MLP

### 5.3 DGA 与设备故障诊断

优先资源：

1. Public DGA Datasets
2. IEC TC10
3. IEEE DataPort DGA 数据

常见 baseline：

1. IEC Three-Ratio
2. Duval Triangle
3. SVM
4. Random Forest
5. XGBoost
6. MLP

### 5.4 负荷预测与市场分析

优先资源：

1. EIA Open Data
2. ENTSO-E Transparency Platform
3. Open Power System Data
4. PJM Data Miner 2
5. Pecan Street Dataport

常见 baseline：

1. ARIMA
2. Linear Regression
3. SVR
4. XGBoost
5. LightGBM
6. LSTM
7. Transformer

### 5.5 光伏/风电预测

优先资源：

1. NREL NSRDB
2. Open Power System Data
3. EIA Open Data

常见 baseline：

1. Persistence
2. XGBoost
3. LightGBM
4. LSTM
5. TCN
6. Transformer

### 5.6 配电网控制与 EV 充电

优先资源：

1. SimBench
2. OpenDSS feeders
3. Grid2Op
4. ACN-Data
5. Pecan Street Dataport

常见 baseline：

1. rule-based control
2. OPF-based control
3. FCFS
4. uncontrolled charging
5. MPC
6. reinforcement learning

## 6. 结论

电网方向的公开研究资源具有非常明显的层次结构。

第一层是标准 benchmark 与网络算例，例如 IEEE test cases、MATPOWER/pandapower 案例、PGLib-OPF、SimBench 和 TAMU synthetic grids，这一层最适合方法论文与算法比较。  
第二层是真实运行和时序数据，例如 EIA、ENTSO-E、PJM、OPSD、NSRDB、ACN-Data 和 Pecan Street，这一层更适合预测、市场分析、用户行为和实证研究。  
第三层是仿真与优化平台，例如 MATPOWER、pandapower、PowerModels、PyPSA、OpenDSS、Grid2Op 和 ANDES，这一层决定了实验的实现方式与可复现性。

近三年文献表明，上述资源仍然处于活跃使用状态，并且已经形成相对清晰的“问题类型 - 公开数据 - benchmark - 平台 - baseline”对应关系。因此，在后续电网选题、实验设计和 research policy 约束中，应优先从这些高复用、可公开获取、社区认可度高的资源中选择数据集、benchmark 和 baseline。

## 参考链接

### 官方资源

1. MATPOWER: https://matpower.org/
2. Power Grid Lib: https://power-grid-lib.github.io/
3. PGLib-OPF: https://github.com/power-grid-lib/pglib-opf
4. pandapower test cases: https://pandapower.readthedocs.io/en/latest/networks/power_system_test_cases.html
5. pandapower contingency: https://pandapower.readthedocs.io/en/latest/contingency.html
6. SimBench: https://simbench.readthedocs.io/en/stable/
7. Grid2Op: https://grid2op.readthedocs.io/en/latest/
8. TAMU Electric Grid Test Case Repository: https://electricgrids.engr.tamu.edu/electric-grid-test-cases/
9. EIA Open Data: https://www.eia.gov/opendata/
10. Open Power System Data: https://open-power-system-data.org/
11. NSRDB: https://developer.nrel.gov/docs/solar/nsrdb/
12. ENTSO-E Transparency Platform: https://www.entsoe.eu/data/transparency-platform/
13. PJM Data Miner 2: https://www.pjm.com/markets-and-operations/etools/data-miner-2/
14. ACN-Data: https://ev.caltech.edu/dataset.html
15. PyPSA: https://pypsa.org/
16. PyPSA-Eur: https://pypsa-eur.readthedocs.io/
17. OpenDSS: https://opendss.epri.com/
18. DSS-Extensions: https://dss-extensions.org/
19. ANDES: https://docs.andes.app/en/latest/index.html
20. OpenIPSL: https://doc.openipsl.org/
21. PowSyBl: https://www.powsybl.org/pages/overview/
22. DOE OEDI / OpenEI: https://data.openei.org/
23. IEEE PES ISS Open Data Sets: https://site.ieee.org/pes-iss/data-sets/

### 近期代表论文

1. https://arxiv.org/abs/2409.19609
2. https://arxiv.org/abs/2404.17541
3. https://arxiv.org/abs/2601.14468
4. https://arxiv.org/abs/2411.11180
5. https://arxiv.org/abs/2509.02861
6. https://link.springer.com/article/10.1186/s42162-024-00427-y
7. https://arxiv.org/abs/2404.09721
8. https://arxiv.org/abs/2412.06571
9. https://arxiv.org/abs/2510.09414
10. https://arxiv.org/abs/2509.12214
11. https://arxiv.org/abs/2401.09694
12. https://arxiv.org/abs/2511.20276
