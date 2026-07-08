# 电力系统 AI 论文选题、数据、Benchmark、仿真环境与 Baseline 整合版

更新日期：2026-04-07

## 0. 使用方式

这份文档用于统一回答以下几个问题：

1. 电力系统、电网运行、电力设备、光伏和风电相关方向，适合写哪些 AI 论文题目
2. 这些题目通常可用哪些公开数据集、benchmark 或仿真环境
3. 有哪些常用仿真平台和 GitHub 代码库可以支撑实验
4. 该方向 baseline 应该至少覆盖哪些方法
5. 后续准备数据、baseline 与 research policy 约束时，应按什么顺序开展

本文整合了两部分信息：

1. 现有整理结果中关于 benchmark、simulation environment、baseline 约束与执行优先级的内容
2. 老师提供资料中关于风光预测、故障数据、仿真软件、GitHub 仓库与公开数据入口的补充内容

目标不是只列资源名称，而是形成一份能够直接指导选题和实验准备的总表述。

## 1. 建议优先考虑的论文方向

从公开资源可得性、baseline 完整性、实验可复现性和后续写作稳定性来看，当前最适合优先考虑的方向有 6 类。

### 1.1 电网运行优化与 OPF 近似

典型问题：

1. AC/DC OPF 近似求解
2. 多目标经济-环保调度
3. 含可再生能源的运行优化
4. 物理约束下的学习型最优潮流

适合原因：

1. 标准 benchmark 最成熟
2. baseline 体系最稳定
3. 可直接使用 MATPOWER、PGLib-OPF、PowerModels 等成熟生态

### 1.2 N-1 安全评估与快速筛选

典型问题：

1. 基于 physics-informed ML 的 contingency screening
2. 过载风险识别
3. 安全校核加速

适合原因：

1. IEEE 标准系统和 pandapower 案例可直接用
2. 传统物理 baseline 与机器学习 baseline 都很清楚
3. 叙事容易写成“加速 + 安全性不退化”

### 1.3 光伏/风电预测与可再生能源并网

典型问题：

1. 光伏短期功率预测
2. 风电短期/中期预测
3. 风光联合预测
4. 气象驱动的 renewable forecasting
5. 风光场景驱动的运行评估

适合原因：

1. 公开数据明显多于很多设备类方向
2. baseline 体系成熟
3. 可从站点级、区域级、国家级做不同粒度选题

### 1.4 配电网控制、DER 协同与 EV 充电

典型问题：

1. Volt-VAR control
2. 配电网拓扑控制
3. 分布式光伏/储能协同
4. EV charging 调度

适合原因：

1. SimBench、OpenDSS、GridLAB-D、ACN-Data 等资源支持较好
2. rule-based、OPF-based、MPC、RL baseline 都可以构成清晰对照

### 1.5 电力设备故障诊断与 DGA

典型问题：

1. 变压器 DGA 故障诊断
2. 知识增强设备故障分类
3. 图结构或规则结构与 ML 结合

适合原因：

1. 工程背景明确
2. 规则法 baseline 很成熟
3. 易写成“知识 + 模型”类论文

但需要注意：

1. 公开数据集分散
2. 标签空间一致性要特别小心

### 1.6 电网故障、保护与 PMU/扰动分析

典型问题：

1. 故障检测
2. 故障分类与定位
3. PMU/μPMU 事件识别
4. 电能质量扰动分类

适合原因：

1. 有一批波形类和仿真类公开资源可参考
2. CNN/LSTM/Transformer/GNN 都有空间

但需要注意：

1. 真实公开数据偏少
2. 很多工作仍依赖仿真生成数据

## 2. 资源准备的总体顺序

后续数据和 baseline 准备工作，建议按“先 benchmark、再真实时序、再专题数据”的顺序推进。

### 2.1 第一阶段：先固定通用 benchmark 与基础 baseline

优先级最高的资源：

1. MATPOWER case files
2. pandapower test cases
3. PGLib-OPF
4. SimBench
5. Grid2Op
6. TAMU synthetic grids

优先级最高的 baseline 工具链：

1. `scikit-learn`
2. `xgboost`
3. `lightgbm`
4. `pymoo`
5. `torch`
6. `torch_geometric`

这样做的原因是：

1. benchmark 最容易准备
2. baseline 工具链一旦稳定，可跨多个方向复用
3. 能最快让新 idea 收敛到可执行实验

### 2.2 第二阶段：补真实时序和市场数据

优先补：

1. EIA Open Data
2. Open Power System Data
3. NREL NSRDB
4. ENTSO-E Transparency Platform
5. PJM Data Miner 2
6. ACN-Data

这一阶段的重点不是“拿到文件”，而是建立：

1. 访问方式
2. 字段口径
3. 时间粒度
4. 空间粒度
5. 清洗流程

### 2.3 第三阶段：专题化数据与专业 baseline

按具体课题再补：

1. Public DGA datasets / IEC TC10 / IEEE DataPort DGA
2. Synthetic PMU Data (TAMU)
3. Distribution PMU Data Set
4. Pecan Street Dataport
5. 故障保护类 Mendeley / Kaggle 数据

## 3. 按方向整理的公开数据、Benchmark 与仿真环境

### 3.1 电网运行优化、潮流与 OPF

**优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| IEEE Standard Test Cases | 标准算例 | PF、OPF、ED、安全分析 | 低 |
| MATPOWER Case Files | benchmark case | 潮流、OPF、经济调度 | 低 |
| pandapower Test Cases | Python benchmark case | contingency、SE、PF、OPF | 低 |
| PGLib-OPF | benchmark library | OPF benchmark、学习型 OPF、求解器比较 | 低 |
| OPFData | AC-OPF 数据集 | 学习型 OPF、拓扑扰动泛化 | 中 |
| PFΔ / PF∆ | 潮流计算 benchmark | 学习型潮流、统一误差评测 | 中 |
| TAMU synthetic grids | synthetic benchmark | 大系统 OPF、拓扑变化、动态仿真 | 低-中 |
| Alberta Power Network case | 开放电网建模案例 | 图建模、拓扑恢复、图学习 | 中 |

**常用仿真/优化平台**

1. MATPOWER
2. pandapower
3. PYPOWER
4. PowerModels.jl
5. PyPSA

**常见 baseline**

1. NSGA-II
2. MOEA/D
3. MOPSO
4. NSGA-III
5. SPEA2
6. 传统 OPF 数值方法

**适合写的 AI 题目**

1. GNN 做 AC-OPF 近似求解
2. 物理约束 OPF 代理模型
3. 拓扑扰动下的鲁棒 OPF 学习
4. 知识增强多目标调度优化
5. 基于 OPFData / PFΔ 的统一 benchmark 比较

### 3.2 N-1 安全评估与快速筛选

**优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| pandapower Test Cases | benchmark case | AC PF、PTDF/LODF、N-1 标注 | 低 |
| IEEE 14/39/118-bus | 标准系统 | 小/中/大规模安全筛选 | 低 |
| TAMU synthetic grids | synthetic benchmark | 更大规模安全评估 | 低-中 |

**常用仿真/计算平台**

1. pandapower
2. MATPOWER
3. PowerModels.jl

**常见 baseline**

1. LODF linear screening
2. Random Forest
3. XGBoost
4. LightGBM
5. MLP
6. SVM

**适合写的 AI 题目**

1. Physics-informed residual learning for contingency screening
2. GNN 做结构化安全风险分类
3. 结合 PTDF/LODF 的快速过载判定

### 3.3 光伏/风电预测与可再生能源并网

这一方向需要区分站点级、区域级和国家级数据。

**站点级/场站级优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| SOLETE | 风光共址实测数据 | 光伏预测、风光联合预测、物理信息 ML | 中 |
| Synthetic PV & Wind Germany | 合成风光预测数据 | 多站点预测、迁移学习、预训练 | 中 |
| Chinese State Grid Renewable Competition Dataset | 中国风光实测竞赛数据 | 国内风光预测论文 | 中 |

**区域/国家级优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| Open Power System Data | 欧洲电力时序 | 风光/负荷联合预测、市场分析 | 中 |
| NREL / PERFORM / related regional datasets | 区域风光与负荷预测 | 多尺度预测、概率预测 | 中 |
| S2S4E Europe | 国家级中长期风光/负荷预测 | 中长期预测、气候服务 | 中 |
| France national wind-solar benchmark dataset | 法国全国风光数据集 | 国家级风光预测 benchmark | 中 |
| EIA Open Data | 美国能源统计和时序 | 可再生发电分析 | 中 |
| NREL NSRDB | 辐照和气象 | PV forecasting | 中 |

**常用仿真/辅助平台**

1. GridLAB-D
2. pandapower
3. PyPSA
4. OpenDSS

**常见 baseline**

1. Persistence
2. ARIMA
3. XGBoost
4. LightGBM
5. LSTM
6. TCN
7. Transformer

**适合写的 AI 题目**

1. 光伏短期功率预测
2. 风光联合预测
3. 物理信息时序模型
4. 风光预测驱动的运行风险评估
5. 国家级中长期风光预测与气候服务评估

### 3.4 配电网控制、DER 协同与 EV 充电

**优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| SimBench | benchmark with profiles | 配电网监测、控制、状态估计 | 低 |
| Grid2Op | simulation environment | sequential decision、控制、韧性 | 低 |
| OpenDSS feeder cases | feeder cases | QSTS、DER、Volt-VAR | 中 |
| GridLAB-D | 配电网和 DER 仿真 | 长时段配电网仿真 | 中 |
| ACN-Data | EV charging sessions | 充电调度、需求响应 | 中 |
| Pecan Street Dataport | 用户侧高分辨率数据 | 用户行为与 DER 协同 | 中-高 |

**常见 baseline**

1. rule-based control
2. OPF-based control
3. Volt-VAR heuristic
4. MPC
5. FCFS
6. uncontrolled charging
7. reinforcement learning

**适合写的 AI 题目**

1. 含分布式光伏的配电网电压控制
2. EV charging scheduling with real session data
3. 配电网风险评估与控制
4. RL 用于配网控制

### 3.5 电力设备故障诊断与 DGA

**优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| Public DGA datasets | 设备诊断数据 | 变压器故障分类 | 中-高 |
| IEC TC10 | DGA benchmark | 规则法对比 | 中 |
| IEEE DataPort DGA assets | 公开数据入口 | 多源 DGA 对照 | 中 |
| Mendeley DGA datasets | 国际公开 DGA 数据 | 跨数据集对比、规则法与 ML 对比 | 中 |

**常见 baseline**

1. IEC Three-Ratio
2. Duval Triangle
3. Rogers Ratio
4. SVM
5. Random Forest
6. XGBoost
7. MLP
8. GAT / GCN

**适合写的 AI 题目**

1. 知识增强 DGA 故障诊断
2. 图结构与规则法结合的设备分类
3. 少数类故障识别

**主要风险**

1. 标签空间不统一
2. 多源数据近重复
3. 传统规则 baseline 缺失会被质疑

### 3.6 电网故障、保护、PMU 与电能质量

**优先资源**

| 资源 | 类型 | 典型用途 | 准备难度 |
|---|---|---|---|
| Dataset for Testing Transmission Line Protections: Energy Transition Oriented (Mendeley) | 波形级仿真保护数据 | 故障检测、分类、定位 | 中 |
| Power System Faults Dataset (Kaggle) | 结构化故障日志 | 风险预测、故障类型分类 | 中 |
| Synthetic PMU Data (TAMU) | 合成 PMU 数据 | 事件检测、振荡分析 | 中 |
| Distribution PMU Data Set | PMU/μPMU 数据 | 配电网监测、事件检测 | 中 |
| Power Quality Disturbance datasets / repos | 扰动分类 | 电能质量分类 | 中 |

**常用仿真平台**

1. PowerFactory
2. MATLAB/Simulink
3. OpenDSS
4. ATP
5. ANDES
6. PSAT

**常见 baseline**

1. threshold-based detection
2. SVM
3. Random Forest
4. KNN
5. MLP
6. CNN
7. LSTM
8. Transformer

**适合写的 AI 题目**

1. 故障波形分类与定位
2. PMU 扰动识别
3. 电能质量扰动分类
4. 保护与扰动管理中的 ML

## 4. 主要仿真软件与环境总表

| 工具 | 类型 | 主要功能 | 适合方向 |
|---|---|---|---|
| MATPOWER | 开源稳态仿真/优化 | PF、OPF、ED | 运行优化、OPF、调度 |
| PYPOWER | Python 版 MATPOWER | 批量数据生成、Python 联动 | OPF、潮流学习 |
| pandapower | Python 电力系统库 | PF、SE、contingency、short-circuit | 安全筛选、配网分析、方法实验 |
| PowerModels.jl | 优化框架 | OPF 建模与求解器实验 | OPF、约束优化 |
| PyPSA / PyPSA-Eur | 规划与运行优化 | LOPF、SCLOPF、扩容规划 | 系统规划、跨能源 |
| OpenDSS | 配电网仿真 | QSTS、DER、feeder studies | 配电网控制、DER |
| GridLAB-D | 配电网与 DER 仿真 | 长时段配网、智能电表、DER | 光伏/风电接入、配网运行 |
| Grid2Op | 交互式电网环境 | sequential decision、RL control | AI 控制、拓扑控制 |
| ANDES | 开源动态仿真器 | 暂态稳定、小信号 | 动态稳定、TSA |
| PSAT | MATLAB/Octave 工具箱 | 动态仿真、稳定性分析 | 故障扰动、动态建模 |
| PSS/E | 商业平台 | transmission planning、动态 | 大电网规划与稳定 |
| PowerFactory | 商业平台 | PF、RMS、EMT、保护 | 故障、保护、综合仿真 |
| PSCAD | 商业 EMT 平台 | 电力电子、HVDC、EMT | 新能源并网、电力电子 |

## 5. 可直接参考的 GitHub / 开源代码入口

### 5.1 电网 AI 通用工具与数据结构

1. `bdonon/ml4ps`
   - 面向电力系统的机器学习工具包
   - 强调图结构数据与电网仿真的衔接
   - 适合 GNN、电网图学习方向

### 5.2 电网运行与 OPF 相关

1. `xuwkk/power_system_operation`
   - Python + CVXPY
   - 可用于电网运行优化、可再生场景变动、基础数据生成

2. `tamu-engineering-research/Open-source-power-dataset`
   - PSML 相关开放数据与基线
   - 适合做电网时序、事件检测、负荷和可再生预测

### 5.3 风光预测与专题数据

1. `DVPombo/SOLETE`
   - SOLETE 数据配套代码
   - 可快速复现实验后再替换成自己的模型

### 5.4 电能质量与故障分类

1. `Vishal-Prakash-1/Classification-Of-Power-Quality-Disturbances-Using-Deep-Learning`
   - 电能质量扰动分类完整 pipeline
   - 可直接作为故障/扰动方向 baseline

## 6. 各方向 baseline 最低配置建议

### 6.1 调度优化 / OPF

最低应包含：

1. NSGA-II
2. MOEA/D
3. MOPSO

可扩展：

1. NSGA-III
2. SPEA2
3. MODE

### 6.2 安全评估 / contingency screening

最低应包含：

1. LODF linear screening
2. Random Forest
3. XGBoost

可扩展：

1. LightGBM
2. MLP
3. SVM

### 6.3 风光预测 / 负荷预测

最低应包含：

1. Persistence 或 naive baseline
2. ARIMA 或简单统计模型
3. XGBoost 或 LightGBM
4. LSTM

可扩展：

1. Transformer
2. TCN
3. CNN-LSTM

### 6.4 DGA / 设备诊断

最低应包含：

1. IEC Three-Ratio
2. Duval Triangle
3. SVM
4. Random Forest

可扩展：

1. XGBoost
2. MLP
3. GAT / GCN

### 6.5 故障 / 保护 / PMU

最低应包含：

1. threshold-based method
2. SVM 或 Random Forest
3. 一种深度模型（CNN/LSTM）

可扩展：

1. Transformer
2. GNN

## 7. 写论文时需要特别注意的问题

### 7.1 不要把 benchmark、真实数据和 simulation environment 混成一个概念

例如：

1. `PGLib-OPF` 是 benchmark library，不是传统真实数据集
2. `Grid2Op` 是 environment，不是一般意义上的静态数据集
3. `OPSD`、`EIA`、`PJM` 才更接近真实运行数据源

### 7.2 选题时不要只看“有没有数据”，还要看 baseline 是否足够成熟

一个方向如果公开数据有，但 baseline 体系很弱，后面写作会很吃力。  
相反，如果 benchmark 稳定、baseline 完整，即使数据是 synthetic，也更容易形成扎实论文。

### 7.3 真实数据最难的部分通常不是下载，而是口径统一

尤其是：

1. 时间粒度
2. 空间粒度
3. 缺失值与异常值
4. 标签定义
5. 多源数据对齐

### 7.4 设备诊断和故障方向最容易踩标签与数据独立性的问题

例如：

1. 近重复数据被误当成外部泛化验证
2. 标签空间不完全一致
3. 不同数据源的故障类型名称不同但被强行合并

## 8. 当前最值得优先准备的一批资源

如果按投入产出比排序，最值得优先准备的是：

### A. 立即可形成方法论文基础盘

1. MATPOWER case files
2. pandapower test cases
3. PGLib-OPF
4. SimBench
5. Grid2Op
6. TAMU synthetic grids

### B. 真实时序数据的第二梯队

1. Open Power System Data
2. EIA Open Data
3. NREL NSRDB
4. ENTSO-E Transparency Platform
5. PJM Data Miner 2
6. ACN-Data

### C. 专题化高价值但准备成本更高的第三梯队

1. SOLETE
2. Chinese State Grid renewable competition dataset
3. S2S4E Europe
4. Public DGA datasets / IEC TC10
5. Transmission line protection datasets
6. PMU / μPMU datasets

## 9. 结论

电力系统 AI 论文的资源准备，不应只理解为“找一些公开数据集”，而应理解为建立“数据集 + benchmark + 仿真环境 + baseline + 代码库”的完整支撑体系。

从公开性、复用率、写作稳定性和实验可复现性来看，当前最稳妥的路径是：

1. 先以 IEEE 标准算例、MATPOWER、pandapower、PGLib-OPF、SimBench、Grid2Op、TAMU synthetic grids 为基础，覆盖电网运行优化、安全评估、控制与方法论文的主战场
2. 再补充 OPSD、EIA、NSRDB、ENTSO-E、PJM、ACN-Data 等真实时序和市场数据，用于负荷预测、风光预测、市场分析和用户侧研究
3. 最后按具体课题扩展 DGA、PMU、故障保护、SOLETE、中国国家电网风光竞赛数据等专题资源

如果按上述方式组织，后续无论是准备新论文 idea、写 research policy、筛选数据集、还是确定 baseline，都能直接从这份整合材料出发，不需要每次重新从头搜集。

## 10. 关键资源入口

### 10.1 Benchmark / 仿真环境 / 平台

1. MATPOWER: https://matpower.org/
2. pandapower: https://pandapower.readthedocs.io/
3. PGLib-OPF: https://github.com/power-grid-lib/pglib-opf
4. Power Grid Lib: https://power-grid-lib.github.io/
5. SimBench: https://simbench.readthedocs.io/en/stable/
6. Grid2Op: https://grid2op.readthedocs.io/en/latest/
7. TAMU Electric Grid Test Cases: https://electricgrids.engr.tamu.edu/electric-grid-test-cases/
8. OpenDSS: https://opendss.epri.com/
9. GridLAB-D: https://www.gridlabd.org
10. PyPSA: https://pypsa.org/

### 10.2 真实数据与专题数据

1. Open Power System Data: https://open-power-system-data.org/
2. EIA Open Data: https://www.eia.gov/opendata/
3. NREL NSRDB: https://developer.nrel.gov/docs/solar/nsrdb/
4. ENTSO-E Transparency Platform: https://www.entsoe.eu/data/transparency-platform/
5. PJM Data Miner 2: https://www.pjm.com/markets-and-operations/etools/data-miner-2/
6. ACN-Data: https://ev.caltech.edu/dataset.html
7. SOLETE repo: https://github.com/DVPombo/SOLETE
8. Synthetic PV & Wind Germany: https://daks.uni-kassel.de/entities/dataset/57ea0681-d8b2-4e76-b31d-578178961f87
9. Chinese State Grid Renewable Competition Dataset paper: https://www.nature.com/articles/s41597-022-01696-6
10. S2S4E Europe dataset paper: https://essd.copernicus.org/articles/13/2259/2021/
11. Dataset for Testing Transmission Line Protections (Mendeley): https://data.mendeley.com/datasets/9s58y9dkdt/1
12. Power System Faults Dataset (Kaggle): https://www.kaggle.com/datasets/ziya07/power-system-faults-dataset/versions/1
13. OPFData paper: http://arxiv.org/pdf/2406.07234.pdf
14. PFΔ benchmark overview: https://www.climatechange.ai/papers/iclr2025/67
15. SOLETE dataset paper: https://linkinghub.elsevier.com/retrieve/pii/S2352340922002578
16. France wind-solar benchmark paper: https://arxiv.org/abs/2504.16100

### 10.3 GitHub / 代码入口

1. ml4ps: https://github.com/bdonon/ml4ps
2. power_system_operation: https://github.com/xuwkk/power_system_operation
3. Open-source-power-dataset / PSML: https://github.com/tamu-engineering-research/Open-source-power-dataset
4. Power Quality Disturbance Classification: https://github.com/Vishal-Prakash-1/Classification-Of-Power-Quality-Disturbances-Using-Deep-Learning
