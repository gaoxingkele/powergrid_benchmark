# mintou_p5 (TRACE-MOEA) 期刊投稿差距评估与修改完善方案

评估日期: 2026-07-13
基准: IEEE Access / MDPI Energies 期刊画像中的 "Distilled review standards"
ARA 源: `papers\mintou\mintou_p5_trace_moea_feasibility_review\`

---

## 一、论文概况

TRACE-MOEA（Traceable Review-Aware Coevolutionary Multi-Objective Evolution）面向"可追溯电网可行性评审与投资有效性优化"任务。任务本身是**自构造的代理评审基准**：从 RTS-GMLC（72 个候选）与 SimBench（48 个候选）的网架统计量合成 120 个虚拟投资项目候选，再叠加本地缓存的 40 份 NERC/C2GES 公开可靠性报告元数据（其中 28 份事件报告）作为"评审证据特征"（见 `evidence\source\real_project_review_source_profile.csv`）。在 7 个评审场景 × 4 次重复 = 28 次运行上，TRACE-MOEA 的 hypervolume proxy 均值 1.74461503，超过最强基线 AHP-TOPSIS（1.72349050）**1.23%**，超过最强消融 Ablation-SingleObjective（1.68212661）**3.71%**。此前 v1/v2 弱结果（Random Feasible 反超 -70%/-39%）与 v3 near-miss（落后 AHP-TOPSIS 0.12%）均已在 evidence 链保留；最终版是在"trace-review metric weighting 与任务对齐"后转正的。**expert labels 全程缺失**——`claims.md` 明确记录"在补充专家标签、成本校准、潮流校核之前禁止提出确切工程经济结论"，即当前没有任何外部真值来支撑"评审有效"这一核心声明。

## 二、必须先说的代码级发现（比 ground truth 更靠前的硬伤）

对 `src\powergrid_benchmark\mintou_real_project_review.py` 的审读表明，当前证据链存在比"无专家标签"更根本的问题，**两刊任何一位打开代码的审稿人都会将其判为 fatal**：

1. **所有方法（含 NSGA-II、MOEA/D、AHP-TOPSIS）都不是真实算法实现**，而是同一个"排序+装包"启发式的参数化代理：每个方法用 5 个手工赋值的质量常数刻画（第 59–75 行），如 TRACE-MOEA `(search=0.94, repair=0.95, trace=0.97, ...)` vs NSGA-II `(0.78, 0.72, 0.52, ...)`。不存在真实的种群演化、Pareto 前沿或 AHP 判断矩阵。
2. **评价指标直接消费这些手工常数，构成自证循环**：`trace_completeness = 0.34 + 0.44 × method.trace_quality + ...`（第 554 行），`ranking_stability` 依赖 `method.preference_quality/repair_quality`（第 558 行），而 p5 的 hypervolume proxy 又乘以由二者构成的 `review_quality`（第 568–572 行）。即"提出方法赢 1.23%"在相当程度上由构造预置。
3. **针对基线的特判**：Random Feasible 被单独乘 0.62 惩罚（第 570–571 行）且 `max_items` 被限为 5（其余方法为 10，第 448–450 行）——这正是 v1/v2 中 Random Feasible 获胜后加入的；TRACE-MOEA 另享独占的 `target_min=8` 补装步骤（第 473–480 行）。
4. **指标命名失实**："hypervolume_proxy" 并非超体积，而是属性乘积式自定义综合分；方法名中的 "Coevolutionary" 在代码中没有任何协同演化机制对应。
5. **消融结果雷同暴露实现问题**：leaderboard 中 Ablation-NoReliabilityFeatures 与 Ablation-NoScheduleRisk 全列数值逐位相同，Ablation-NSGA2Only 与 NSGA-II 的 hypervolume 逐位相同——审稿人会据此质疑消融是否真的改变了任何东西。

结论：当前 1.23%/3.71% **不能进入任何投稿稿件**。ARA 自己的 `constraints.md` 也仅允许"合规优化"，而第 2、3 条已越过"metric 与任务对齐"的合规边界，进入结果预置区。这是本评估所有 P0 项的根源。

## 三、期刊匹配度对比：IEEE Access vs MDPI Energies

### IEEE Access

**Fit: Low（现状）→ Medium（完成 P0+P1 后）**

- **有利面**：电力与能源是 Access 高产领域；"组件组合+场景适配"式创新恰是其接收论文的常态（画像：4/4 全文均为组合式创新）；诚实的 limitations 与公平性声明（2/4 出现）是加分项；不设新颖性门槛，1.23% 的小增益本身不致命。
- **致命面（soundness 单一闸门）**：Access 是**二元 accept/reject**，无大修回旋余地，且评审唯一标准是"correct, complete, reproducible"。本文属**元启发式社区**，该社区惯例是 **50+ 独立运行 + Wilcoxon/Friedman + 收敛曲线/箱线图**——本文只有 28 runs（7 场景 × 4 重复）、零显著性检验，1.23% 的差距在无统计检验下站不住。Access 鼓励代码共享（reproducibility initiative），一旦附码，第二节所有问题即刻暴露；不附码，"proxy dataset–task mismatch"也在其画像明列的审稿盲点自查项中。
- **ground truth 有效性问题在 Access 视角下**：审稿人问的第一句将是"评审质量的真值是什么？"——本文的回答只能是"作者自定义的综合分"，且该综合分部分由方法自身的手工参数决定。在 soundness-only 的评审框架下，这不是"局限"，而是"claims 未被证据支撑"，直接触发 reject（画像 desk-reject 项："insufficient rigor — unsupported claims"）。

### MDPI Energies

**Fit: Low（现状）→ Medium-High（完成 P0+P1 后）**

- **有利面**：电网投资组合规划是 Energies 电力系统版块的典型题材；其 distilled 标准显示 **31/31 接收论文都没有全新算法**、≤5% 增益诚实报告即可通过、**0/29 要求统计显著性检验**、单测试系统占 2/3、规划类论文仅靠场景自比较即可通过——对本文的 28 runs 和 1.23% 增益宽容得多。AHP-TOPSIS 作基线也贴合能源 MCDM 文献传统。
- **不利面**："incremental, unvalidated simulation" 是 Energies 明列的 desk-reject 触发器，其 evidence bar 要求"validation（experimental, numerical, or **against real data**）"。本文特征来自真实公开数据，但**标签/目标函数完全自定义**，属于"未经验证的仿真"边缘。**敏感性分析是近乎强制项（缺失即最高频大修触发器）**——本文完全没有（预算水平、权重、候选池规模均未扫描）。Data Availability Statement 等四件套为硬性门槛，目前 ARA 未准备。
- **ground truth 有效性问题在 Energies 视角下**：Energies 审稿人（应用能源专家）更可能问"这个评审结果对实际电网公司有什么用"，对代理标签的容忍度高于 Access 的方法学审稿人——其画像显示"自定义指标上的百分比增益"甚至是已发表论文的常见逃逸项。但前提是仿真本身可信：第二节的自证循环一旦被看出，在任何期刊都是 integrity 级问题而非宽容度问题。

### 最终推荐

**修复 P0 后主投 Energies，IEEE Access 降为备选**（与当前 PAPER.md 的主备设置对调）：

1. 本文证据形态（单一自建测试系统、场景自比较、无统计检验、小增益、规划/评审应用导向）与 Energies 已发表论文的实证画像几乎逐条吻合，与 Access 元启发式社区的 50-run+Wilcoxon 惯例逐条冲突。
2. Access 二元决策无大修机会，Energies 有 1–2 轮修改可以消化"补敏感性分析"类意见。
3. 若坚持 Access，必须补齐 P1 全部统计协议（50+ runs、Wilcoxon+Holm、收敛/箱线图），工作量显著更大。
4. 两刊共同前提：完成 P0（真实算法实现 + 指标去循环 + 外部真值），否则两刊皆为 Low 且有 integrity 风险。

## 四、写作修改清单

1. **诚实框定 "proxy benchmark" 定位**（最重要的框架决策）：
   - 标题/摘要不得出现暗示真实评审有效性的措辞；建议将贡献重心改写为"**一个由公开数据构造的可复现电网项目评审代理基准 + 在其上的可追溯 MOEA**"，即把"基准构造"本身列为贡献之一（Access 画像显示纯框架/评估类论文可凭内部场景比较通过）。
   - 明确三层声明边界：(a) 在代理基准上的优化性能——可以声称；(b) 追溯性/稳定性指标改善——可以声称但须说明指标定义；(c) 真实评审决策质量——**不可声称**，只能作为 future work（与 `claims.md` 的禁止条款一致）。
   - 设独立 Limitations 小节：无专家标签、成本未校准、无潮流校核、候选项目为合成——Access 画像明示"honest limitations win"。
2. **与 AHP-TOPSIS 等比较的公平性声明**（两刊画像均视为加分项）：统一候选池、统一预算约束、统一评价次数/计算预算；披露 AHP 判断矩阵与 TOPSIS 权重的来源及调参方式；说明各基线的实现库（如 pymoo）与超参数设定（Access 画像点名"near-zero hyperparameter disclosure"是常见盲点）；声明未对任何基线做削弱性配置——这要求先完成 P0-1，否则该声明写不出来。
3. **指标更名与定义**：若不计算真超体积，"hypervolume proxy" 必须更名（如 composite review-quality index）并给出完整公式；建议直接在真实目标向量上计算标准 hypervolume（固定参考点）以对齐 MOEA 社区语言。
4. **方法名与机制对齐**：要么实现真正的协同演化（如项目组合种群与评审规则/权重种群协同），要么从名称中去掉 "Coevolutionary"——名实不符是审稿人最易抓的把柄。
5. **贡献列表**：Access 惯例为编号式 3–6 条贡献（近乎硬性）；每条对应一个可核验的实验证据。
6. **negative evidence 转化为卖点**：v1→v3 的失败-修正轨迹（随机可行解暴露指标缺陷 → 预算感知修正 → 指标对齐）可写入"benchmark 设计迭代"叙事，但必须重述为"指标设计的合理性论证"而非"调到我们赢为止"，并补充最终指标的独立合理性检验（见 P1-4）。
7. **期刊格式**：Access 用专用 LaTeX 模板 + ORCID；Energies 用 MDPI 模板 + IMRaD + ~200 词摘要 + 3–8 关键词 + Data Availability / Author Contributions / Funding / COI 四件套（Energies 100% 硬门槛）+ 适度自引。

## 五、实验设计缺口

| # | 缺口 | 现状（ARA 事实） | 要求 |
|---|---|---|---|
| 1 | **真实算法实现** | 所有方法为手工参数化代理（第二节） | 用 pymoo 等实现真实 NSGA-II/MOEA/D/NSGA-III；真实 AHP 判断矩阵 + TOPSIS；TRACE-MOEA 本体的演化算子、修复算子、追溯记录器须为可执行代码 |
| 2 | **运行数与统计检验** | 28 runs（7×4，`real_project_review_config.json: repeats=4`），零检验 | Access：每场景 ≥30（社区惯例 50+）独立随机种子，Wilcoxon 符号秩 + Holm 校正或 Friedman + 事后检验，收敛曲线 + 箱线图；Energies：可放宽，但 ≥10 重复 + 方差报告仍属自保 |
| 3 | **label 有效性验证** | 无任何外部真值；指标自定义且含方法自身参数 | 至少其一：(a) 专家标注子集——邀请 ≥2–3 名电网规划工程师对 ≥60–120 个候选做可行性/优先级标注，报告一致性（Kappa），验证代理指标与专家排序的相关性（Spearman）；(b) 历史项目结果回验——用真实项目"批准/建成/撤回"结果做外部校验（数据源见第六节） |
| 4 | **指标独立性** | hypervolume proxy 消费 method.trace_quality 等（循环） | 评价指标只允许依赖解（组合）本身的属性，禁止依赖方法身份或方法参数；对最终指标做权重敏感性扫描，证明 TRACE-MOEA 的优势不依赖某个特定权重点 |
| 5 | **成本参数校准** | 候选成本由网架统计量合成，未校准 | 用公开造价基准校准（NREL ATB、EIA 电源资本成本报告、MISO Transmission Cost Estimation Guide），并做成本扰动敏感性 |
| 6 | **工程可行性校核** | `analysis.md` 自认缺 AC/潮流校核 | 对入选组合在 SimBench 上跑 pandapower AC 潮流、在 RTS-GMLC 上跑 OPF（PGLib/MATPOWER 已缓存），至少验证 Top-N 组合不违反网络约束 |
| 7 | **消融覆盖两大核心组件** | traceability：有（NoPreferenceRanking、NSGA2Only 间接覆盖 trace-aware 部分）；**coevolution：无**——8 个消融中没有任何一个隔离协同演化机制（因代码中根本无此机制）；且 NoReliabilityFeatures 与 NoScheduleRisk 结果逐位相同、NSGA2Only 与 NSGA-II 相同 | 实现协同演化后补 `no_coevolution` 消融；增设 `no_trace_recorder`（只关追溯记录、不动搜索）以单独隔离 traceability；修复雷同消融，保证每个消融确实改变了行为 |
| 8 | **敏感性分析（Energies 近强制）** | 无 | 预算水平 ±20%、目标权重网格、候选池规模（SmallProjectPool 可升级为系统性扫描）三维敏感性 |

## 六、数据集缺口

1. **真实项目评审/投资决策公开数据**：不存在带专家可行性标签的现成公开数据集，但存在可用于**结果回验**（第五节 #3b）的真实项目结局数据，建议核实并接入（本地 `CACHE_STATUS.md` 均未缓存）：
   - **LBNL "Queued Up" 互联队列数据**：数万个发电/储能项目的进入-撤回-建成结局，是"可行性评审预测 → 真实结局"回验的最贴合公开源；
   - **EIA Form 860/860M**：计划机组的 proposed → operational/cancelled 状态迁移；
   - **MISO MTEP / PJM RTEP / CAISO 输电规划报告**：逐项目的批准/推迟/取消清单（输电侧，与本文候选类型最接近）；
   - **World Bank 能源项目 PAD + IEG 结局评级**：带独立事后有效性评级的真实投资项目。
   任选其一构造"历史结局回验子集"，即可把 C1 从"proxy 支撑"升级为"外部校验支撑"。
2. **NERC 报告缓存的可复现性与可公开性**：`c2ges_nerc_reports`（40 份文档）为公开报告的本地缓存，报告本身公开可得，但 NERC PDF 的再分发权利未经确认。建议：**不随论文分发 PDF**，改为发布"manifest（标题 + 官方 URL + SHA-256）+ 自动抓取脚本 + 特征抽取脚本"，使第三方可从官方源重建全部特征；当前从报告到 `evidence_score` 等特征的抽取过程若含手工步骤，必须脚本化，否则 C4（可复现性声明）不成立。
3. **已具备的部分**：rts_gmlc、simbench、pglib_opf、matpower、pandapower、grid2op 均已本地缓存（`CACHE_STATUS.md`），第五节 #6 的潮流校核无数据障碍。

## 七、优先级行动清单

### P0（不完成不得投任何期刊）
1. **重写实验管线为真实算法实现**：删除 `Method` 手工质量常数、Random Feasible 的 ×0.62 惩罚与 max_items 特判、TRACE-MOEA 独占补装步骤；基线用 pymoo/标准实现（`mintou_real_project_review.py` 需重构）。
2. **评价指标去循环**：指标只依赖解属性；改用真超体积 + 独立定义的 trace_completeness（基于解的证据链接覆盖率，而非方法参数）。
3. **接入外部真值**：专家标注子集（≥2 名标注人 + Kappa）或历史结局回验子集（LBNL Queued Up / EIA-860 / MTEP 三选一）。
4. 用新管线重跑全部 15 个方法；如新结果为负/弱，按 `constraints.md` 保留于 evidence 链并回到方法改进，而非调指标。

### P1（投 IEEE Access 的必要项；投 Energies 的强烈建议项）
5. 每场景 ≥30（Access 目标 50）独立种子 + Wilcoxon/Friedman + Holm + 收敛曲线 + 箱线图。
6. 三维敏感性分析（预算/权重/池规模）——Energies 缺此即大修。
7. pandapower AC / OPF 可行性校核 Top-N 组合；成本用 NREL ATB / EIA / MISO 指南校准。
8. 实现协同演化机制并补 `no_coevolution`、`no_trace_recorder` 消融；修复逐位雷同的消融行。
9. 基线公平性声明 + 全部超参数披露表。

### P2（投稿前打磨）
10. 重写摘要/引言为"公开数据代理评审基准 + 可追溯 MOEA"双贡献框架；编号贡献列表 3–6 条；独立 Limitations 小节。
11. NERC manifest + 抓取/特征脚本发布方案；代码仓库整理（Access reproducibility initiative / Energies Data Availability）。
12. 期刊模板落地（首选 Energies：MDPI 模板 + 四件套声明 + 匹配 Special Issue 筛选；备选 Access：专用模板 + ORCID + 图形摘要）；更新 `PAPER.md` 的主备期刊设置与 `portfolio_status.md`。
13. 自引与文献时效自查；对照两刊画像的"已发表论文逃逸项"清单做投稿前自检（时序泄漏、代理数据-任务错配、结论过度外推等）。

---
*本评估基于 ARA 证据链与实验代码的静态审读；所有行数引用以 2026-07-13 的 `src\powergrid_benchmark\mintou_real_project_review.py` 为准。*

---

## 进展更新（2026-07-13）

**P0-1、P0-2、P0-4 与 P1-5 已完成**：`mintou_real_project_review.py` 已整体重写为 v2 真实算法版：

- 手工 `Method` 质量常数、×0.62 特判、独占补装步骤全部删除；v1 产物保留为 `*_v1_deprecated_circular.*`。
- 基线：pymoo NSGA-II / MOEA/D（约束支配 / 罚函数，二进制编码 + 低密度初始化统一应用）、真实 AHP-TOPSIS（一致对儿比较矩阵 + 特征向量权重 + 贴近度排序）、Greedy BCR / Weighted Sum / Random Feasible（无任何惩罚）。
- TRACE-MOEA 真实实现：NSGA-II 内核 + 偏好向量协同进化（每 5 代基于最优响应分散度更新）+ 预算修复 + 决策档案；trace/decision-coverage 只作描述性列，不进排名。
- 评价：标准 hypervolume（固定种子参考集归一化边界 + 1.1 参考点，仅取可行非支配前沿）；30 seeds/方法/实验；Mann-Whitney U + Holm（`tables/real_project_review_significance.csv`）。

**v2 真实结果**：TRACE-MOEA 池化平均 HV 0.17425，比最强基线 NSGA-II（0.17270）高 **0.89%**，42 组基线对比中 **38 组 Holm 显著**；但最强消融 NoScheduleRisk 仅落后 0.13%，且在 traceability_evaluation 实验中显著反超（p_holm=0.022）——**偏好协同进化组件的净贡献弱**，投稿叙事应以"完整方法稳定显著优于全部外部基线"为主张，组件贡献如实呈现于消融讨论。信号：`positive_but_partially_significant`。

**仍未完成的 P0**：外部真值（P0-3，专家标注子集或 LBNL Queued Up / EIA-860 历史结局回验）——这是投稿前的最后一道硬闸。P1 剩余：敏感性分析成节、成本校准、收敛曲线/箱线图。

---

## 进展更新（2026-07-14，NERC 规则回验 v1）

外部真值阶梯第一级已完成（`src/powergrid_benchmark/mintou_review_backtest.py`，证据：`evidence/tables/real_nerc_rule_backtest.csv` + `evidence/runs/real_nerc_rule_backtest_analysis.md`）。设计已规避构造循环：规则分 = NERC 报告主题的类型权重 ×（未经 NERC 调整的原始候选属性）压力分位。

结果（如实）：proposed 方法 priority capture 1.34–1.62（>1 = 组合向 NERC 记录的风险模式集中）——**一致性底线通过**；但 AHP-TOPSIS 对齐度最高（capture 1.6–2.3、Kendall τ 0.44–0.52 显著），这是偏好排序法直接加权可靠性属性的构造使然。**引用边界**：本回验只能作外部一致性证据，不能作方法优势证据；proposed 的 τ 不显著（多目标权衡会稀释单维对齐是预期行为，须如实写）。阶梯下一级 MISO MTEP 历史回验仍是投稿前的真外锚。
