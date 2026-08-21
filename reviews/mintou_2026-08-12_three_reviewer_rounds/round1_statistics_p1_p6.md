# 第一轮独立审稿：方法学与统计学（P1--P6）

审稿日期：2026-08-12（Asia/Shanghai）  
审稿角色：方法学/统计审稿人  
处理方式：只读核查正文与冻结证据；未修改任何稿件或结果文件  
总体建议：**六篇均需 Major Revision 后再进入投稿终审**

## 1. 核查范围与判定原则

本轮逐项对照以下证据：

- `paper_projects/mintou_p1_*/manuscript/MANUSCRIPT.md` 至 `mintou_p6_*` 的当前正文；
- `papers/mintou/mintou_p1_*` 至 `mintou_p6_*/evidence/runs/` 与 `evidence/tables/` 中当前无历史后缀的 CSV；
- `reviews/mintou_2026-08-11_above_mean_enhancement/FROZEN_EXPERIMENT_PROTOCOL.md`。

带有 `weak`、`deprecated`、`near_miss`、`pre_*` 或旧版本后缀的文件不用于支持当前结论。审稿重点是样本量、种子设计、比较家族、多重校正、效应量、置信区间、外部有效性、负消融、可复现性和正文数字与当前 CSV 的一致性。

冻结协议第 5 条要求：主比较采用双侧 Mann--Whitney U、在声明的比较家族内作 Holm 校正，并在样本允许时同时报告效应量和置信区间。六篇均有足够的逐种子记录，但当前正文普遍只有均值、标准差、相对百分比和校正 p 值，**没有主效应的 95% CI，也没有 Mann--Whitney 对应的秩效应量**。因此六篇目前均未完整满足冻结协议自身的统计报告门槛。

## 2. 跨论文总览

| 稿件 | 当前证据规模 | 主要统计结论 | 第一轮判定 | 投稿前最高优先级修正 |
|---|---:|---|---|---|
| P1 DSTAR-GRU | 14 方法、2 horizon；208 行；随机方法 10 seeds | 1 h 检索有利、24 h onset 检索有害；NREL-118 冻结 cap 下零阳性 | Major | 将旧的 21-test 家族改为当前 27-test 家族并同步所有 p；利用同种子配对；补 CI/效应量 |
| P2 CSA-LoadNet | 非层级块主要为 10 seeds 决策集；Ausgrid 11 模型 × 10 seeds × 4 reconciliation | 只在 OPSD 24 h 支持窄幅聚合收益；Ausgrid 输给 DLinear；几何权重负结果 | Major | OPSD 的“四个其他神经基线仅 3 seeds”不能支撑“最强五基线”强表述；补配对推断、CI 和效应量 |
| P3 CARS-MODE | 14 方法 × 7 实验 × 30 seeds = 2940 行 | 代理 HV 胜多数基线；自适应消融无增益；AC 排名不转移 | Major | Table 6 Holm p 已落后于最新 13-comparison 家族；不可用 seed-0 AC 组成差异为自适应作因果辩护 |
| P4 SHIELD-MOEA | **11** 方法 × 8 实验 × 30 seeds = **2640** 行；另有机制控制 | 代理 HV 胜外部基线；repair 有效；动态筛选/混合变异为零结果；AC 不领先 | Major | 正文仍写 10 方法/2400 runs/40 baseline tests；应改为 11/2640/48，并更新旧 Holm p |
| P5 TRACE-MOEA | 16 方法 × 7 场景 × 30 seeds = 3360 行；预算扫描 270 行 | 对 NSGA-II 仅 3/7 场景显著；偏好层孤立效应很小；外部一致性弱式 | Major | 修正 Random Feasible 被误写为确定性；停止把重复 30 次的确定性输出当独立样本；外部 backtest 补置换/CI/多重校正 |
| P6 BiLo-NSGA | 18 方法 × 8 实验 × 30 seeds = 4320 行 | 对 NSGA-II 的 pooled 增益 1.12%；atomic substitution 无增益；forward 为条件性 | Major | 确定性基线伪重复、外部项目级伪独立和 raw p 未校正；“forward-dominant”需降为条件性表述 |

## 3. 跨论文共同 Major 问题

### M-C1. 效应量和 95% CI 缺失，违反冻结协议的报告要求

逐种子数据足以计算不确定性，但六篇的主表仍主要采用 `mean ± std + Holm p`。标准差描述运行波动，不是效应估计的不确定区间；相对均值百分比也不是秩效应量。

**确切修正：**

1. 每个主比较增加：绝对均值差、相对差、Mann--Whitney 对应的 rank-biserial correlation（或 Cliff's delta）及 95% CI。
2. 对同一组固定种子运行的 P1、P2，补逐种子差值的中位数/均值及 bootstrap CI；以配对置换检验或 Wilcoxon signed-rank 作为主推断，现有 MWU 作为冻结协议敏感性分析。若必须保留 MWU 为唯一主检验，至少解释为何主动丢弃 seed pairing。
3. 对 P3--P6 的独立方法种子流，保留 MWU，但用分层 bootstrap（先按实验/场景，再按 seed）给 pooled 描述量加 CI；不要把跨场景 pooled SD 当作单一随机过程的方差。

### M-C2. “每场景内 Holm”与跨场景机制结论之间缺少二级家族定义

当前 Holm 家族通常按“一个实验/场景内 proposed vs all opponents”定义。这能控制该场景内的 FWER，但稿件随后又跨 7--8 个场景筛选某一消融的显著单元格并形成机制结论。该第二层选择没有统一说明。

**确切修正：**预先写清两层问题：

- 性能家族：每场景内 proposed vs all stochastic opponents；
- 机制家族：对每个关键消融跨全部场景的 7 或 8 个检验再作 Holm，或报告一个跨场景分层/混合效应模型，单场景结果作为跟进分析。

如果不做二级校正，所有“在若干场景中有效”的句子均应明确为场景内控制后的探索性模式。

### M-C3. 确定性算法被复制成 30 行并进入 MWU，形成伪重复

当前 run CSV 中多种确定性算法在同一场景的 30 行 hypervolume 完全相同。例如 P3 的 Weighted Sum，P4 的 Weighted Sum 和 Deterministic Planning，P5 的 AHP-TOPSIS、Weighted Sum 和 Greedy BCR，P6 的 AHP-TOPSIS、Greedy BCR 及 weighted-ranking 控制。把同一个确定性结果复制 30 次不会产生 30 个独立样本，却会影响 U 统计量和同一 Holm 家族中其他 p 值。

**确切修正：**

- 确定性基线每场景按 `n=1` 描述，报告绝对/相对差，不进行 seed-level MWU；
- 主推断家族只包含真正独立的随机方法；据此重新计算 Holm；
- 若要对确定性规则作推断，随机化的单位必须改为独立问题实例、时间块、候选池 bootstrap 或明确的随机输入扰动，而不是复制输出；
- 正文、表注和总比较计数必须区分“随机推断比较”和“确定性描述比较”。

### M-C4. 外部 backtest 的项目级 p 值没有处理组合依赖和多重比较

P5、P6 的 MTEP16 结果把项目的 selection frequency 与二元结果作 point-biserial/MWU。项目是否被选中受同一预算和组合约束，项目观测并不独立；同一场景还报告多个方法、broad/strict 两种标签和两类检验，却没有声明外部验证的多重比较家族。当前 raw p 不能直接升级为方法间外部优越性。

**确切修正：**保留现有点估计，但将显著性改为预算约束下的置换检验：在不改变每次 portfolio size/成本带的前提下置换 outcome label 或生成匹配随机组合，得到 capture、point-biserial 的经验零分布；对“2 场景 × 2 标签定义 × 2 指标（或明确的主/次层级）”作 Holm。报告 bootstrap/permutation 95% CI。没有方法间差值检验时，只能写“名义值高于/低于”，不能写“exceeds baselines”作为推断性结论。

## 4. P1：DSTAR-GRU / Curtailment Benchmark

### 判定：Major Revision

### Major 1：正文仍使用旧的 21-test Holm 家族，当前 CSV 是每 horizon 27 项

`real_curtailment_significance.csv` 当前每个 horizon 有 27 行（3 metrics × 9 seeded opponents），不是正文 III-D、Table 3 所写的 21（3 × 7）。加入 DLinear、TCN 后，正文未完全同步校正结果。

已核实的当前值包括：

- 1 h curtailment MAE：NoRetrievalBank `p_holm=0.00401878`，NoSiamese/SmallBank `0.00172434`，LSTM/MLP/DLinear `0.00401878`；
- 1 h onset MAE：LSTMEncoder `0.0087426`，NoRetrievalBank `0.00401878`，LSTM `0.0238875`；
- 24 h onset F1：NoSiamese `0.00172434`，NoRetrievalBank `0.00393805`，LSTM `0.00383611`，MLP `0.0946992`；
- 24 h curtailment MAE 对 NoSiamese：`0.00172434`。

这些值与正文中多处 `0.0013/0.0027/0.0029/0.003/0.007/0.019/0.066` 不一致。摘要和结论的“Holm p <= 0.003”也不再成立；若概括当前显著单元，应写不超过约 `0.0041`，或逐项给值。

**确切修正：**从当前 significance CSV 自动生成正文所有 p 值、图注和摘要结论；将 III-D、Table 3 改为 27 tests per horizon。禁止手工复制旧版本数字。

### Major 2：同一十个固定种子构成配对设计，MWU 未利用配对信息

所有随机方法使用相同十个 seeds，且图 6 已计算 seed-paired effect。MWU 将两组视为独立样本，统计设计与数据生成结构不一致。

**确切修正：**增加 paired permutation 或 Wilcoxon signed-rank；报告逐 seed 差值 CI。保留 MWU 作为冻结协议敏感性分析并说明两者结论是否一致。

### Major 3：onset 结论缺少事件级不确定性

测试集只有 57 个 1 h onset 和 172 个 24 h onset。当前不确定性主要反映模型初始化，不反映同一年时间序列事件抽样误差；小时又具有时序相关性。

**确切修正：**增加按连续事件/周块抽样的 block bootstrap CI，至少覆盖 onset F1 与 onset MAE。若不补，应将“establishes a horizon-dependent sign reversal”收窄为“在该固定测试年和 seed 变异下观察到并通过预设检验”。

### Minor

1. NREL-118 冻结 cap 下 8784 小时零阳性是**适用性失败审计**，不是跨数据集预测验证；当前正文大体表述诚实，摘要中应始终保留这一限定。
2. `SmallBank` 在两 horizon 的 MAE 相同且 event F1 为零，建议明确这是退化预测诊断，不纳入“最优方法”排序口径。
3. 增加随机种子列表、软件版本、CPU 型号和从 run CSV 重建 significance CSV 的命令；当前“一命令复现”缺少环境锁文件引用。

## 5. P2：CSA-LoadNet / Hierarchical Load Forecasting

### 判定：Major Revision

### Major 1：OPSD 主结论并非对“五个神经基线”的同强度十种子确认

OPSD 24 h 的十种子推断家族只有五个 ablations 加 MLP；TCN、PatchTST-lite、DLinear、LSTM 的 OPSD 数字来自 3-seed v6。正文却多次写“outperforms the strongest of five neural baselines”。MLP 的确是现有 3-seed screen 中最强外部基线，但用小样本 screen 选出“最强”再仅对该方法做 10 seeds，会有 winner-selection 不确定性。

**确切修正（二选一）：**

- 将其余四个 OPSD 24 h 基线补到相同 10 seeds，并把五个外部基线定义为一个 Holm 家族；或
- 将摘要、贡献和结论改为“significantly outperforms MLP, the strongest observed compact baseline in the preliminary three-seed screen”，并明确其他四个方法没有同等统计确认。

### Major 2：固定同种子但使用非配对 MWU

非层级 v7 与精确 Ausgrid v8 均使用相同十 seeds；Figure 6 还展示 seed-paired relative changes。与 P1 相同，应利用配对差值作主推断或至少敏感性检验。

**确切修正：**对 OPSD/SimBench 以及 Ausgrid OLS 的 proposed--opponent 比较补 paired permutation/Wilcoxon 和差值 95% CI；并明确 v8 的两个家族分别为 5 external baselines、5 component ablations。

### Major 3：“协议足以检测 4% 效应”没有功效依据

正文从一个显著的 4.1% 观察值推断协议“strong enough to detect a 4% MAPE effect”。一次显著结果不是检验功效证明，尤其 n=10。

**确切修正：**改为“the protocol detected the observed 4.1% difference”，并报告差值 CI。若要保留检测能力表述，需用观察到的 seed 方差给出最小可检测效应/功效曲线，且标注为事后精度分析而非设计前功效。

### Minor

1. 当前 v8 数字与 `real_ausgrid_exact_hierarchy_v8_significance.csv` 一致：OLS 下对 DLinear `p_holm=0.0009845125`（loss），对 LSTM `0.000913359`（win），其余外部方法不分离。建议正文给精确值而非笼统 `<0.001`，便于审计。
2. reconciliation 是对同一 base forecasts 的确定性变换；如要比较 Base/Bottom-Up/OLS 的准确率，应使用逐 seed 配对差值和 CI。当前仅描述 coherence 时可以保持描述性。
3. 只有一个时间切分和一个确定性 Ausgrid 分组。外部有效性应限定为“三个公开数据源上的五个固定 setting”，不能扩展为一般 hierarchical forecasting 结论。
4. 几何权重的全面负结果报告充分；但“contribute nothing”宜改为“no detectable contribution under the present n, pool sizes and budget”。

## 6. P3：CARS-MODE

### 判定：Major Revision

### Major 1：Table 6 使用旧 Holm 数字

当前 `real_simbench_planning_significance.csv` 每个实验有 13 个 comparisons，Table 6 的多项 p 仍是扩充 GDE3/NSDE 等对照前的旧值。当前 CARS-MODE vs NSGA-II 的 `p_holm` 为：

- base `6.38562e-07`；constraint `3.9022e-09`；DER `0.00033825`；
- load growth `1.32615e-05`；pareto replicate `4.91645e-07`；
- runtime scalability `8.06613e-10`；storage `0.041573`。

正文的 `4.8e-7、2.9e-9、2.0e-4、2.9e-7、6.5e-10、0.033` 等已不是当前家族的校正值。显著/不显著方向未改变，但数字一致性不合格。

**确切修正：**由最新 CSV 重建 Table 6、摘要、结论和图标注；在统计方法中明确 `m=13`。

### Major 2：自适应机制的理论辩护超出 AC 设计可支持范围

FixedDE pooled HV 比 full 高 0.60%，七个场景均不显著。AC 层只使用 seed-0 compromise composition，经固定规则映射成 72 个相关 case；正文也承认不是统计供能的第二比较。由 `0.611 vs 0.569` 推断“自适应的真实功能被 AC 层揭示”或“一台额外 storage 导致该机制差异”，不能作因果归因，因为只比较了单个种子选出的组合，且 network/scenario case 共享结构。

**确切修正：**将 Section 6.3/7 中的机制因果句改为“与该假设一致的描述性 composition-level pattern”；不得据此保留“strategy-adaptive 提升物理性能”的结论。若要支持该结论，需对 30 seeds 的 compromise plans 全部作 AC 映射，按 seed 和 network 配对报告 CI/混合模型。

### Major 3：确定性 baseline 进入 30×MWU 家族

Weighted Sum 在每个场景的 30 个 HV 完全相同；将其当 n=30 推断会夸大有效样本量，并改变 13 项 Holm 家族。MOEA/D 的若干场景也退化成同一输出，但后者至少是 30 次算法运行后出现的退化结果，需和真正确定性规则区分。

**确切修正：**按跨论文 M-C3 重算 stochastic-only 家族。保留“Weighted Sum 返回单点，因此 HV 较低”的描述，不把其显著性计入“62/63 stochastic wins”。重新分列随机基线胜负和确定性规则点估计。

### Minor

1. `pareto_quality` 是同一 benchmark 定义上的内部复现实验，不是独立数据集复现；“independent replicate”应改为“independent seeded repeat under the same benchmark family”。
2. 参数敏感性 6 个 p 值没有声明校正家族；应标记 exploratory，或在两个 sweep axis 内分别 Holm。
3. 代理 HV 的相对提升和 AC 可行率排序相反，是有价值的负结果；摘要应明确“proxy optimizer”而非“planning-quality winner”。
4. 现有外部有效性仍为一个 SimBench 规划池和四个同源 AC 网络；无第二候选池，当前 Limitations 的边界正确。

## 7. P4：SHIELD-MOEA

### 判定：Major Revision

### Major 1：方法数、运行数、baseline 比较数均与当前证据不一致

当前主 run CSV 有 **2640 行 = 11 methods × 8 experiments × 30 seeds**。正文 Table 2 声称十方法并遗漏 `NSGA-II+Repair`，Section 5.2 仍写 `2400 runs`。当前 significance CSV 每场景 10 opponents，其中 6 个 baseline，因此 baseline 比较是 **48 = 6 × 8**，不是摘要、贡献、结果、结论反复出现的 40/40。

**确切修正：**Table 2 加入 NSGA-II+Repair；所有 10/2400/40 改为 11/2640/48。控制实验的 720 runs 继续单独报告，不能混入主 run 总数。

### Major 2：Table 4 部分 Holm p 仍是旧九对手家族

当前 SHIELD vs NSGA-II 的 `p_holm` 为：DER `6.56202e-10`、load `1.09737e-07`、outage `5.05227e-08`、restoration `5.13867e-06`、unseen stress `0.000746578`；正文分别仍出现 `5.5e-10、8.8e-8、4.0e-8、4.1e-6、6.0e-4`。其余显示值与当前四舍五入相容。

**确切修正：**用当前 CSV 自动重建 Table 4 与正文。统计方法明确主家族 `m=10`；机制控制 `GA-only/DE-only/fixed-worst-K` 是独立三对手家族，不与主家族混写。

### Major 3：AC 差异是 108 个相关 case 的描述，不是 108 个独立重复

每方法 108 cases 来自 3 个 seed-0 组合 × 6 网络 × 6 场景；同一 portfolio 在网络/场景间重复，且各方法 case 是匹配的。当前正文大体承认其为 qualitative composition-level check，但 Discussion 仍用“validated full pipeline”“outage exposure matter electrically”作较强机制表述。

**确切修正：**使用“descriptive matched-case difference”并给 network-family 分层比例；不要把 0.685 vs 0.574 当作独立重复的因果估计。若需正式支持，按多 seed portfolio × network 的层级设计重跑，或至少对匹配的 network-scenario block 做 cluster bootstrap CI。

### Minor

1. screening-off 比 full 运行更快（0.0792 vs 0.0889 s）；“65% objective-call reduction”只是调用计数，不是已证实的时间/能耗收益，当前正文已承认，摘要也应保留限定。
2. worst-case HV 与 mean HV 使用不同 normalization；可以比较各自在方法间的相对 margin，不能以数值接近证明“tracks closely”或无 tail fragility。建议删除绝对值接近的论证，只保留同一 worst-case 列内的比较。
3. CIGRE/IEEE 扩展验证的是固定 composition mapping 的转移，不是优化器在独立网络候选池上的外部复现；Limitations 应继续作为投稿主限定。
4. 动态 re-screening 与 fixed worst-K、hybrid 与 DE-only 均为 8/8 不分离，负结果报告充分；标题/摘要不能把“adaptive”本身写成已证实性能来源。

## 8. P5：TRACE-MOEA

### 判定：Major Revision

### Major 1：Random Feasible 的随机性叙述与 run CSV 矛盾

Section 5.2 把 AHP-TOPSIS、Weighted Sum、Greedy BCR、**Random Feasible** 都称为“deterministic ... identical across seeds”。但 `real_project_review_results.csv` 中 Random Feasible 每场景通常有 30 个不同 HV（例如 benchmark 30 个唯一值）；Table 3 也把它定义为 random-permutation greedy fill。

**确切修正：**只把 AHP-TOPSIS、Weighted Sum、Greedy BCR 归为确定性；Random Feasible 明确为 30-seed stochastic baseline。同步图 2 图注的 marker 规则。

### Major 2：确定性输出复制 30 次进入 MWU 和 105-comparison 家族

当前 105 行 significance 表是 15 opponents × 7 scenarios，其中上述确定性规则按 n=30 重复。由此产生的 p 值不具有 30 个独立运行的含义，也会改变 TRACE vs NSGA-II 等随机比较的 Holm 调整。

**确切修正：**主 inferential family 改为真正随机的 opponents，确定性规则只报点差；重算各场景 Holm 与“45 significant baseline wins”计数。即使结论方向大概率不变，也必须以重算后的真实计数为准。

### Major 3：从“偏好场景的 full-vs-NSGA-II 胜利”推断偏好层机制，内在逻辑不成立

Full method 对 NSGA-II 在三个偏好较强场景显著，但 NoPreferenceRanking 与 full 的孤立差只有 pooled 0.17%，仅 1/7 场景显著。前者是整套方法差，不能归因给偏好层。Section 6.1/7 把这一共现解释为偏好层“converts emphasis into front quality”属于超出消融证据的机制归因。

**确切修正：**将其改为探索性共现；机制结论以 direct ablation 为准：偏好层对 HV 的增益未获得普遍支持，其已证明作用是产生 preference-elite archive 记录。若要证明条件效应，预先定义 interaction（preference-strength × ablation effect）并对逐 seed 数据作分层模型。

### Major 4：MTEP/NERC 外部有效性缺 CI、置换零分布和多重校正

当前 TRACE 的真实点估计与 CSV 一致：MTEP broad capture 为 1.079479/1.069633，point-biserial r 为 0.168851/0.151092；严格标签只有 19 withdrawals。问题不是点估计，而是 p 值把预算约束下的项目 selection frequency 当作独立项目观察，并在多方法/多标签/多指标中直接引用 raw p。

**确切修正：**执行 M-C4。没有方法间比较检验时，将“exceeds every evolutionary baseline”改成“has a higher nominal broad-alignment point estimate than the listed evolutionary baselines”。保留 AHP/Weighted Sum 更高的 adverse result。

### Minor

1. 预算扫描的 HV 家族每 budget 有 2 个 comparisons，当前 p 与 CSV 一致；preference distance 明确为描述性是正确做法，但仍应给 seed-level CI。
2. “trace archive at zero metric cost”只能表示 trace 未进入目标函数，不能表示计算成本为零；建议改为“without entering the evaluation metric”。
3. pooled SD 同时混合场景差异与 seed 差异，Table 4 应另给 scenario-level mean range 或分层 CI。
4. 单一候选池、无 AC feasibility、无专家标签已在 Limitations 正确披露，必须保留在摘要/结论的最后限定句。

## 9. P6：BiLo-NSGA

### 判定：Major Revision

### Major 1：确定性基线重复与 17-opponent Holm 家族

主 significance 表为 17 opponents × 8 scenarios = 136 行。AHP-TOPSIS、Greedy BCR 和 weighted-ranking 控制在同一场景的 30 行输出完全相同，却按 n=30 进入 MWU。由此 52/56 baseline significant wins 的 p 家族受到伪重复影响。

**确切修正：**按 M-C3 重算 stochastic-only 家族，并将基线结论拆成“随机算法推断比较”与“确定性规则描述比较”。表 4 可保留全部点估计，但显著计数必须重算。

### Major 2：“forward-dominant”仍强于消融总体证据

NoForwardSearch pooled mean 0.17257，高于 full 0.17190；full 在 3/8 场景内显著胜出，另有多个名义损失。当前数据支持“forward insertion 在三个特定场景有可分离贡献”，不支持总体 forward dominance。Atomic substitution 的负结果更明确：NoBackward pooled 高 0.61%，8/8 均不分离；LegacyDeletion 也不分离。

**确切修正：**标题、摘要和结论统一改为“scenario-conditional forward contribution”或给“forward-dominant”作严格操作性定义，并增加对 8 个 NoForward 检验的跨场景 Holm/interaction 分析。不得把 archive semantics 当作性能创新证据。

### Major 3：MTEP 外部验证的独立性和比较措辞过强

当前点估计与 CSV 一致：budget scenario broad capture 1.071455、r=0.087763、p=0.004207、MW p=0.014676；reliability scenario broad capture 1.064185、r=0.077622、p=0.012836、MW p=0.055006。严格标签仍只有 19 withdrawals。

正文称 outcomes “completely independent of ... featurization”，但 2016 `appendix_status` 作为 feature 与后续 broad outcome 强相关，稿件自己也承认该重叠。标签没有被算法使用，并不等于外部检验与 feature construct 完全独立。此外，BiLo 对 baseline 的 capture 只做了点估计排序，没有直接差值检验。

**确切修正：**改为“outcome labels were not used in fitting, while decision-time appendix status remains a prognostic feature”；按 M-C4 做约束置换、CI 和多重校正；“exceeds external baselines”改为“nominally higher than”直至方法间差异得到检验。

### Major 4：matched 1600 evaluations 只是名义预算，不是等价计算预算

PLS 的 1600 neighbor evaluations 与进化法的 `40 × 40` 名义数量相同，但两者初始化、非支配排序、repair、局部操作和目标调用成本不同。现有运行时间显示 PLS 1.416 s、BiLo 0.219 s，这证明实现成本不同，但不能证明搜索努力严格匹配。

**确切修正：**称其为“matched nominal objective-evaluation ceiling”，并同时报告实际 objective calls、候选去重、可行性检查次数和 wall-clock；不要把单个 PLS 实现推广到 Pareto local-search family。

### Minor

1. Table 5 的 NSGA-II 数字及 p 与当前 CSV 一致；主结论应突出只有 5/8 场景显著，0.75x、0.88x 和 renewable 场景均未分离。
2. budget scan 将两个 1.00x 但场景内容不同的实验合并；图注已承认场景不只预算不同，不能将其称为纯受控单因素扫描。
3. 99.6% coverage 是日志完整性，不是解释质量；当前 Limitations 已正确披露，应在摘要避免将其称为可解释性验证。
4. 无 AC feasibility、无专家标签、单一候选池是外部有效性的实质边界，不应由 MTEP broad p 值抵消。

## 10. 建议的统一修订顺序

1. **先锁定证据版本并自动重建数字。** P1、P3、P4 先修正旧 family size、旧 Holm p、旧 run/method counts；建立 manuscript table <- current CSV 的自动检查。
2. **重做不需要新实验的统计分析。** 利用现有 run CSV 计算效应量、CI、paired sensitivity（P1/P2）、stochastic-only Holm（P3--P6）、跨场景关键消融校正。
3. **重做 P5/P6 外部 backtest 推断。** 使用预算/portfolio-size 约束置换和多重校正；保留 broad/strict 两种标签，不得删除不利 strict 结果。
4. **收窄机制语言。** P3 自适应 AC 因果、P4 动态筛选/混合变异、P5 偏好层条件增益、P6 forward dominance 均必须服从各自直接消融，而不是服从 full-vs-baseline 的共现模式。
5. **最后更新摘要、贡献、讨论和结论。** 所有数字、显著计数和外部有效性措辞由最终统计表回填；负消融继续保留。

## 11. 第一轮统计放行门槛

只有同时满足以下条件，建议进入第二轮内容/逻辑评审：

- P1、P3、P4 所有当前 CSV 与正文数字逐项一致；
- 六篇主比较均有预先声明的比较家族、效应量和 95% CI；
- 固定同种子的 P1/P2 给出配对敏感性结果；
- P3--P6 不再把确定性复制行当作独立 seed；
- P5/P6 外部 backtest 使用约束置换或明确降级为描述性；
- 所有 central-mechanism 结论与直接消融一致，且负结果在摘要与结论中不被淡化。

