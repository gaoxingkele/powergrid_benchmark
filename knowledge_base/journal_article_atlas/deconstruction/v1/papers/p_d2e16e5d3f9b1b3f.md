# A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience

单助手全文解构 v1 · 2026-09-13。human_calibrated=false；待独立复核。

原件：D:\aicoding\papers\Energies\2026_A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience.pdf
SHA256：d2e16e5d3f9b1b3fab27c48bdabd9afef6391cfb4c60bb6ce44f5c4aa51e1c00
DOI：10.3390/en19020574；期刊：Energies；年份：2026。

已读物理页：1–28（正文、声明、参考文献全部文本）；图像复核页：6, 8, 11, 13, 14, 15, 16, 19, 20, 21, 23, 25。
逐章、逐编号公式、逐图逐表均有下列清单；并不等于全部字段校准完成。逐段重组/逐段标签仅partial，词句统计、未编号公式、完整表格转录、独立复核均未完成。

## 优先审查的问题

- 第 11 页｜critical｜Eq11正向归一化分母为min-min=0，原页视觉确认；不能直接实现原式（source_confirmed）
- 第 17, 18 页｜major｜Eq22最小化F2正收益，与正文最大化收益冲突；加权目标未给方向和权重（source_confirmed）
- 第 1, 17, 19 页｜major｜MILP/MINLP类型不一致，线性化及全局优化保证未交代（source_confirmed）
- 第 8, 18, 19 页｜major｜Eq1与25对储能重复计入风险；Eq26/28功率符号及周期平衡不一致需源码澄清（needs_independent_math_review）
- 第 8, 15 页｜major｜匹配式DG=0无定义而Case列块21/23无DG；分段缺等号、百分比与[-1,1]尺度不一致（source_confirmed）
- 第 21 页｜major｜预算写approximately后直接句号，数值缺失；三安装的最优性不可复现（source_confirmed）
- 第 22, 24, 26 页｜major｜频率和电压缺前值、馈线动态模型未充分给出；代理指标不能直接证明停电恢复韧性（evidence_gap）
- 第 21, 26 页｜major｜4%成本对应Case3/2而多数改进看似Case3/1；L2 0.0464→0.787却写+70%，存在数值/小数点冲突（needs_author_reconciliation）
- 第 15 页｜minor｜七CRITIC权重相加1.01，可能舍入但需说明（source_confirmed）
- 第 16, 20 页｜minor｜优先级式号3应10；流程结果表号错位（source_confirmed）

## 章节树与论证作用

| ID | 父节 | 章节 | 物理页 | 逻辑 |
|---|---|---|---|---|
| 1 | - | Introduction | 1, 5 | 从分布式波动到规划信息不完整，提出优先级+序贯规划+多尺度评价。 |
| 1.1 | 1 | Motivation | 1, 2 | 新能源负荷不确定性→储能与战术规划需求。 |
| 1.2 | 1 | Literature Review and Research Gaps | 2, 3 | 比较集群、敏感度、统计情景；区分战术部署与详细扩展规划。 |
| 1.3 | 1 | Contributions and Paper Structure | 3, 5 | 三贡献及总流程→后续指标、规划、评价。 |
| 2 | - | Evaluation Framework for Highly Resilient Active Distribution Networks | 5, 6 | 安全、可靠性/质量、效率需求→优先级评价原则。 |
| 3 | - | Methods for Grid Resilience Enhancement Using Distributed Energy Storage | 7, 15 | 指标定义、情景生成、CRITIC权重和案例输入。 |
| 3.1 | 3 | Construction of a Set of Demand Indicators | 7, 10 | 效率和质量两组需求→综合优先级输入。 |
| 3.1.1 | 3.1 | Efficiency Indicators | 7, 8 | 广义负荷与供需匹配函数→筛选失衡区域。 |
| 3.1.2 | 3.1 | High-Quality Performance Indicators | 9, 10 | I1–I7年度质量数据及典型日测量→节点需求。 |
| 3.2 | 3 | Calculation Extraction of Typical Scenic Output Scenes Based on Improved GMM Algorithm | 10, 11 | GMM、RV初始化、CH选K→风光典型情景。 |
| 3.2.a | 3.2 | GMM clustering model | 10 | 混合高斯+最大似然拟合。 |
| 3.2.b | 3.2 | Parameter initialisation | 10 | RV系数K-means初始化。 |
| 3.2.c | 3.2 | Optimal number of clusters determined | 11 | CH类内/类间指标选情景数量。 |
| 3.3 | 3 | Construction of Priority Indices | 11, 12 | 归一化→标准差相关性→CRITIC权重→优先级。 |
| 3.4 | 3 | Case Studies | 12, 15 | 真实供电网和分块输入建立实例。 |
| 3.4.1 | 3.4 | Basic Overview | 12, 13 | 浙江多负荷区域、分时电价、DR及DG限制。 |
| 3.4.2 | 3.4 | Typical Scenario Generation for Wind and Solar Power Output | 14 | 选5情景，图示曲线概率；没有外测拟合对照。 |
| 3.4.3 | 3.4 | Priority Index Construction Results | 15 | 给7权重，供后续排序。 |
| 3.4.4 | 3.4 | Matching Results for Each Block | 15 | 辨别极端源荷失衡区域，连接站址选择。 |
| 4 | - | Multi-Objective Energy Storage Planning Based on Sequential Optimisation | 15, 23 | 用优先级定址、优化定容、更新指数直至预算。 |
| 4.1 | 4 | DESS Sequential Planning Solution Process | 16 | 8步保留已部署储能，迭代更新广义负荷和优先级。 |
| 4.2 | 4 | DESS Multi-Objective Capacity Allocation Model | 16, 19 | 固定每轮站址，优化能量功率时序与状态。 |
| 4.2.1 | 4.2 | Objective Function | 17, 18 | 成本、收益、弃能、峰谷目标→归一化加权求解。 |
| 4.2.2 | 4.2 | Constraint Conditions | 18, 19 | 充放电互斥、功率平衡、容量SOC和预算；无完整馈线潮流约束。 |
| 4.3 | 4 | Case Settings and Results | 19, 23 | 遍历/一次优先级/序贯优先级3方案比较空间分散与收益。 |
| 5 | - | Multi-Dimensional Evaluation for Distribution Network Performance Enhancement | 23, 26 | 定义O/L/G评价指标，聚合前面同一方案结果。 |
| 5.case | 5 | Case Settings and Results (unnumbered) | 25, 26 | 3方案指标比较→优先级和序贯配置优势解释。 |
| 6 | - | Conclusions | 26, 27 | 总结规划贡献和指标提升；提出更细运行模型为未来。 |
| decl | - | Declarations | 27 | 资金、贡献、数据可询问、利益冲突。 |
| refs | - | References | 27, 28 | 37条引用，外部真实性未核。 |

## 框架、算法与假设

```json
{
  "pages": [
    10,
    19
  ],
  "task": "规划信息不完整下需求驱动DESS定址定容",
  "composition": "serial probabilistic clustering + multicriteria priority + sequential optimization + multiscale evaluation",
  "inputs": [
    "历史风光",
    "96点15分钟典型日负荷",
    "年度质量/投诉统计",
    "已有分块",
    "成本电价预算"
  ],
  "outputs": [
    "储能节点",
    "功率/能量容量",
    "充放电时序",
    "O/L/G指标"
  ],
  "modules": [
    "RV-Kmeans初始化GMM、EM拟合、CH选K",
    "CRITIC质量权重与匹配度",
    "最高优先级节点固定、Gurobi定容",
    "更新广义负荷与指数直到预算"
  ],
  "training_vs_decision": "GMM为无监督概率拟合；其余为多准则决策及数学规划，不是强化学习控制",
  "assumptions": [
    "同类DG统一出力曲线仅容量差异",
    "典型日+年度统计代表规划需求",
    "节点数据缺失按负荷/用户比例分摊",
    "历史源荷代表未来",
    "前次安装保持固定",
    "完整潮流网络未来可补入"
  ],
  "theory": "GMM混合分布、CRITIC赋权、资本年化、储能能量平衡；无形式化全局最优性或收敛证明",
  "optimizer": "Python3.9/Gurobi11.0",
  "complexity": "not_reported",
  "objective_weights": "normalization and weighted sum described but weights not_reported",
  "model_class_conflict": "abstract MILP;正文MINLP，二元连续乘积与比率未展示线性化"
}
```

## 逐编号公式清单

下列按实际审阅显示编号组登记，不由最大编号推算；方程转述是功能摘要，不是可执行修正式。单个公式的符号/量纲/实现映射仍为partial。

| 编号 | 页 | 分类 | 内容 | 功能与问题 |
|---|---|---|---|---|
| (1) | 8 | physical/energy/balance | 广义负荷=Pbase+PDR+Pess | 定义规划负荷 |
| (2) | 8 | evaluation/engineering/source_load_matching | 分段源荷匹配比 | 区域筛选；DG=0和等号情形未完备，百分比和区间尺度不一致 |
| (3) | 10 | statistics/probabilistic/mixture | GMM加权概率密度 | 情景建模 |
| (4) | 10 | statistics/probabilistic/Gaussian | 多元高斯密度 | 分量分布 |
| (5) | 10 | learning/training/likelihood | 对数似然最大化 | EM估计 |
| (6) | 10 | statistics/correlation/RV | 矩阵迹归一化相似度 | K-means初始化距离，RV命名与标准定义需核 |
| (7) | 11 | evaluation/clustering/CH | CH类间/类内比 | 选K |
| (8) | 11 | statistics/clustering/dispersion | 类内平方距离和 | CH分母 |
| (9) | 11 | statistics/clustering/dispersion | 类间加权距离和 | CH分子 |
| (10) | 11 | evaluation/multicriteria/priority | 加权7质量指标+效率指数 | 节点排序 |
| (11) | 11 | statistics/normalization/minmax | 正负指标归一化 | 原文正向分母min-min=0，视觉确认 |
| (12) | 12 | statistics/estimation/standard_deviation | 标准差 | CRITIC差异性 |
| (13) | 12 | statistics/estimation/correlation | Pearson相关系数 | CRITIC冲突性 |
| (14) | 12 | evaluation/multicriteria/CRITIC | 信息量SdΣ(1-r)及归一化权重 | 质量权重；一编号组两子式 |
| (15) | 17 | optimization/objective/cost | F1=CRF×资本与贴现O&M | 生命周期成本年化 |
| (16) | 17 | economics/discount/CRF | 资本回收因子 | 年化 |
| (17) | 17 | economics/cost/capital | 额定功率与能量单位成本和 | 建设成本 |
| (18) | 17 | economics/cost/maintenance | O&M贴现和 | 生命周期O&M |
| (19) | 17 | optimization/objective/benefit | F2=售电+节购电收益 | 收益目标 |
| (20) | 17 | optimization/objective/curtailment | 可用/实际出力差比 | 弃能率；分母时间量纲需核 |
| (21) | 17 | optimization/objective/load_smoothing | 峰谷差/峰值 | 负荷平滑 |
| (22) | 17 | optimization/objective/multi | min(F1,F2,F3,F4) | 与F2文字最大化冲突，需符号澄清 |
| (23) | 18 | optimization/constraint/power | 充放电上下界 | 运行限制 |
| (24) | 18 | optimization/constraint/integer | 两状态之和≤1 | 互斥 |
| (25) | 18 | physical/energy/balance | 上网交换+DG=广义负荷+储能 | 功率平衡；PEL已含Pess可能重复计入 |
| (26) | 18 | physical/energy/storage_dynamics | 效率加权充放电周期和为零 | 周期能量平衡；正负功率约定与式28不清 |
| (27) | 18 | optimization/constraint/capacity | 储能容量上下界 | 规划尺度 |
| (28) | 19 | physical/energy/storage_dynamics | 充电增能、放电减能 | SOC递推 |
| (29) | 19 | optimization/constraint/SOC | SOC比例×容量上下界 | 能量可行性 |
| (30) | 19 | optimization/constraint/budget | 所有已部署单元年化建设+O&M≤预算 | 序贯终止 |
| (31) | 24 | evaluation/engineering/node | O1节点质量均值 | 质量潜力 |
| (32) | 24 | evaluation/economics/ratio | O2=F2/F1 | 经济效益 |
| (33) | 24 | evaluation/engineering/renewable | O3原始源荷比减弃能率 | 新能源消纳 |
| (34) | 24 | evaluation/engineering/block | L1各储能块匹配改善率之和 | 区域平衡 |
| (35) | 24 | evaluation/engineering/block | L2储能节点质量与块全部质量比例 | 质量覆盖，求和下标需进一步复核 |
| (36) | 24 | evaluation/engineering/grid | G1已配置节点与全网质量比例 | 全局质量覆盖 |
| (37) | 25 | evaluation/engineering/grid | G2=1-配置后/前匹配离差平方和 | 全局均匀性 |

## 逐图清单

| 图 | 页 | 类型 | 内容 | 证据作用 |
|---|---|---|---|---|
| Figure 1 | 5 | framework | GMM、需求指标→优化→node/block/grid评估 | 总论证路线 |
| Figure 2 | 6 | framework | 综合需求→优先级→序贯规划→多维评价 | 方法模块输入输出 |
| Figure 3 | 6 | algorithm_flow | 需求维度、指标量化、归一化、CRITIC、排序 | 说明指数生成过程，与图1/2有重叠 |
| Figure 4 | 7 | hierarchy | 目标/方法/效率质量指标三层 | 需求分类组织 |
| Figure 5 | 8 | conceptual_time_series | 常规/广义负荷、DG、DR、储能调节阴影 | 解释源荷匹配概念，不是观测结果 |
| Figure 6 | 13 | map | 34分块、区域经纬距离和六类用户图标 | 空间案例背景，非详细馈线电气拓扑 |
| Figure 7 | 13 | time_series | 9负荷类型典型日归一化3D曲线 | 异质性输入展示 |
| Figure 8 | 14 | scenario_surface | PV/风各5情景日出力曲面 | 聚类代表性定性展示 |
| Figure 9 | 14 | bar | PV/风5情景概率 | 情景加权 |
| Figure 10 | 15 | bar | 34块源荷匹配类别和值 | 解释DESS预筛；DG=0块有限图值需公式处理澄清 |
| Figure 11 | 16 | algorithm_flow | GMM→匹配→排序→Gurobi→更新→停止 | 序贯规划核心；图中错引Eq3，实际优先级Eq10 |
| Figure 12 | 19 | system_topology | 风光、负荷、储能、逆变器、电池 | 概念电气系统，非案例完整拓扑 |
| Figure 13 | 20 | algorithm_flow | 优先级→定址定容→电气评估→方案比较 | 结果生成映射，表号与实际错位 |
| Figure 14 | 21 | scatter | 三轮node和block优先级散点 | 显示随部署更新的排序 |
| Figure 15 | 23 | stacked_bar | 三方案各3节点需求指标堆叠 | 对照选址需求覆盖 |
| Figure 16 | 25 | bar | Case1/2/3 O1 O2 O3 L1 L2 G1 G2 | 多尺度代理指标比较，不是恢复时间曲线 |

图中数值未全部数字化；无置信区间不能解释为无不确定性。

## 逐表清单

| 表 | 页 | 类型 | 内容 | 证据作用与限制 |
|---|---|---|---|---|
| Table 1 | 4 | literature_comparison | 文献组×网络尺度、优先级、策略、目标、不确定性、全局评价 | 定位研究缺口；文献分组与正文编号对应值得核查 |
| Table 2 | 9 | indicator_dictionary | I1可靠性差、I2关键负荷比、I3GDP/用电、I4频率不合格、I5电压偏差、I6峰谷、I7投诉 | 定义需求数据 |
| Table 3 | 20 | workflow_mapping | 阶段、输入、工具、输出、对应章节 | 复现路线但输出表4/5指向与实际表5/6不一致 |
| Table 4 | 21 | parameters | 容量2000、功率600、O&M10/90、效率0.95、SOC0.9/0.2、寿命12年 | 经济技术假设；容量单位写kW而非kWh |
| Table 5 | 21 | planning_result | 三方案节点、容量、块、关键负荷比、成本、收益 | Case3节点49/121/147，容量733/1166/1176kWh；经济收益865200CNY/year |
| Table 6 | 22 | electrical_metrics | 每方案3节点原/现峰谷差与频率、电压百分比 | 只峰谷有前后两列；频率/电压无前值，不能证实改进幅度 |

## 实验设计、消融与敏感性

### E1 · 典型风光情景和需求是否可分层

```json
{
  "id": "E1",
  "pages": [
    12,
    15
  ],
  "type": "scenario_construction",
  "question": "典型风光情景和需求是否可分层",
  "design": "一个浙江案例；CH选5情景并显示概率、块匹配",
  "result": "可见日周期/多峰及块差异",
  "limitation": "没有GMM基线、保真误差、尾部风险或外测比较"
}
```

### E2 · 优先级和序贯更新对配置的作用

```json
{
  "id": "E2",
  "pages": [
    19,
    23
  ],
  "type": "planning_comparison",
  "question": "优先级和序贯更新对配置的作用",
  "design": "Case1遍历排序；Case2一次优先级；Case3迭代优先级。各3安装但总容量/成本不同",
  "baselines": [
    "global traversal",
    "one-shot priority"
  ],
  "result": "Case3从157改147，避免同块集中；收益提升",
  "controlled_ablation": "非严格预算容量匹配消融；部署数相同不等资源相同"
}
```

### E3 · 同一配置在node/block/grid指标如何变化

```json
{
  "id": "E3",
  "pages": [
    24,
    26
  ],
  "type": "multiscale_evaluation",
  "question": "同一配置在node/block/grid指标如何变化",
  "design": "复用E2三方案，7指标评估",
  "result": "O2 Case3超过1，部分区域质量指标并非单调提升",
  "independence": "不是额外独立真实试验"
}
```

## 数据与统计核查

```json
{
  "data": {
    "pages": [
      9,
      15
    ],
    "name": "浙江供电网便利案例",
    "resolution": "96 samples/day,15min + annual aggregated indicators",
    "blocks": "Figure6/10 shows 34 blocks",
    "nodes": "完整节点清单及总数未在方法明确列明；不以图轴估算",
    "load_profiles": 9,
    "user_categories": 6,
    "scenario_count": 5,
    "dates": "not_reported",
    "raw_sample_count": "not_reported",
    "split": "not_reported;无监督情景构造未列holdout",
    "availability": "data upon inquiry;无可执行代码链接核验",
    "exogenous_parameters": {
      "discount_rate": 0.05,
      "lifetime_years": 12,
      "efficiency": 0.95,
      "DR": "10–20%,行政医疗教育排除",
      "export_tariff_CNY_kWh": 0.4153
    }
  },
  "statistics": {
    "independent_unit": "单网络规划比较，非3次随机重复",
    "seeds": "not_reported",
    "CI": "not_reported",
    "hypothesis_tests": "not_reported",
    "sensitivity": "not_reported for budget, weights, tariffs, failure rates",
    "ablation": "仅计划策略比较；GMM/CRITIC组件没有独立受控消融",
    "resilience_boundary": "主要为日常运行代理指标，未模拟明确灾害冲击-恢复时序",
    "powerflow": "叙述提及原始网络和潮流结果，但参数和频率动态模型不足"
  }
}
```

## 结论、证据边界与叙事

```json
{
  "conclusions": {
    "pages": [
      26,
      27
    ],
    "author_claims": [
      "4%成本增幅",
      "关键节点27%",
      "消纳0到48.8%",
      "块匹配88%、质量68%、网均匀324%"
    ],
    "supported": "案例内优先级导致不同空间配置并有更高报告收益",
    "limits": "改善分母与对照必须重算；不能将单网代理指标升级为灾害恢复验证或全局最优",
    "future": "更详细运行/扩展模型、层级源荷储协同"
  },
  "narrative": {
    "argument_chain": "规划数据不足→需求指标→情景与排序→定容/序贯更新→三尺度评价→规划建议",
    "paragraph_status": "partial: 无逐段边界重组及全量角色标注",
    "language_observations": [
      "多幅流程图重复相近管线，增加可读性也有信息冗余",
      "resilience/stability/reliability常混用，须按实际指标限制表述",
      "数字优势应明确Case基准与指标物理含义"
    ],
    "original_sentence_frames": [
      "在[预算与场景集合]下，序贯策略将第[轮]站址从[原节点]转移至[新节点]，同时改变[容量/成本]，故归因须控制资源差异。",
      "[代理指标]改善反映[规划层面能力]，不直接等价于[扰动后的恢复性能]。"
    ],
    "lexical_statistics": "not_assessed"
  }
}
```

## 六维难度（非质量、非录用概率）

```json
{
  "status": "provisional_single_assistant_not_quality_score",
  "vector": {
    "D_T": 2,
    "D_A": 2,
    "D_S": 1,
    "D_D": 2,
    "D_E": 2,
    "D_X": 2
  },
  "rationale": {
    "D_T": "指标改写和储能规划方程，无新增证明",
    "D_A": "聚类+赋权+序贯数学规划组合",
    "D_S": "概率聚类及描述比较，无推断设计",
    "D_D": "多类运营指标和历史源荷融合，但原数据缺失",
    "D_E": "带储能经济/能量约束离线规划，非现场试验",
    "D_X": "能源规划、聚类和多准则评价接口明确"
  },
  "evidence_pages": [
    9,
    19,
    26
  ],
  "uncertainty": "±1锚点级，非统计区间",
  "composite": null
}
```

## 未完成项

- 独立数学与电气审查
- 可执行模型和完整数据复现
- 公式11/目标方向/储能符号修复后的敏感性
- 逐段标签和词句统计
- 全图数值数字化
- 引文核验

本文件为来源约束的单助手分析；已发表不代表正确，篇幅和对象数量不构成质量分。

