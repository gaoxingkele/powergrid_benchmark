# mintou_p6 (BiLo-NSGA) 期刊投稿评审报告

评估日期: 2026-07-13。评估基准: `Paper_CCF` 期刊画像的 "Distilled review standards"（IEEE Access 4 篇全文 + 10 篇摘要语料；Energies 34 篇电力系统全文语料；Applied Sciences 11 篇电力/能源全文语料，均 as-of 2026-07）。所有 ARA 事实引自 `papers\mintou\mintou_p6_bilonsga_project_review\`。

---

## 一、论文概况

BiLo-NSGA 是在 NSGA 框架上加入**前向/后向双向局部搜索**（项目添加/删除/替换移动 + 审计轨迹）的多目标算法，面向**预算约束电网项目评审与组合排序**。当前证据（`evidence/tables/real_project_review_leaderboard.csv`）：在 RTS-GMLC + SimBench + NERC/C2GES 报告缓存派生的 120 个候选项目（72 RTS + 48 SimBench，`evidence/source/real_project_review_source_profile.csv`）基准上，BiLo-NSGA 的 mean hypervolume proxy 为 **1.70989680**，超最强基线 AHP-TOPSIS（1.64612807）**3.87%**，超最强消融 Ablation-ShallowLocalSearch（1.65100922）**3.57%**；8 个主实验场景 × 9 个消融 × 6 个基线，feasibility_rate=1.0，ranking_stability=0.8796。

三个必须直面的事实：

1. **proxy 评审任务是"构造"出来的**：候选项目由公开网架统计 + 可靠性报告元数据合成派生，**没有任何专家标注的评审结果**。`logic/claims.md` 自己写明 "Exact engineering-economic manuscript claims remain prohibited until expert labels, calibrated costs, and load-flow checks are added"。且评价指标经历了 v1→v3 演化（`trace/exploration_tree.yaml`）：v1 中 Random Feasible 反超 70.7%（指标奖励项目堆积），v2 仍落后消融 0.57%，直到 v3 "将 P6 目标与 move traceability、ranking stability、feasibility 对齐"后才领先——**指标是朝着 proposed 方法的固有优势（move_trace_completeness：proposed=1.00 vs 基线 0.56–0.73）调整出来的**，审稿人一旦看出复合指标含 trace completeness 分量，会质疑循环论证。同时分项上 BiLo-NSGA 的 reliability_benefit_proxy（1.334 vs 1.786）和 renewable_benefit_proxy（128.8 vs 162.4）**低于基线**，论文必须诚实呈现这个 trade-off。
2. **统计效力几乎为零**：`real_project_review_config.json` 写 repeats=4，但 `evidence/runs/real_project_review_results.csv` 中同一实验的 4 次 repeat 的所有指标值**逐位相同**（仅 runtime 不同）——算法链路是确定性的，有效样本量 n=1/场景，无方差、无法做任何显著性检验。
3. **p5/p6 高度同源，salami-slicing 风险实质存在**：p5（TRACE-MOEA，投 IEEE Access）与 p6 共用**同一数据管线**（`src/powergrid_benchmark/mintou_real_project_review.py` 的 `run_paper`，p5/p6 的 `run_real_project_review.py` 只差参数）、**相同的 3 个数据源目录、相同的 candidate_count=120、相同 repeats=4**、相同最强基线 AHP-TOPSIS、4 个共用基线（NSGA-II/MOEA/D/Greedy BCR/Random Feasible），实验场景亦有重叠（两者都有 renewable_accommodation_review，reliability_driven vs reliability_prioritized 仅措辞之差）。IEEE Access 与 MDPI 都跑 CrossCheck/iThenticate，且 IEEE Access 的官方红线正是 "not distinct from prior publication"。若两文文本模板化复用（当前两个 PAPER.md 的摘要/边界段已经近乎逐句同构），查重和"最小可发表单元"指控是现实风险。差异化的真实抓手在：**方法机制**（BiLo-NSGA 双向局部搜索 + 移动审计轨迹 vs TRACE-MOEA 协同进化 + 评审规则修复 + 偏好排序）与**问题设定**（p6 预算硬约束 + 预算敏感性 vs p5 可追溯性 + 投资有效性），但这两点目前只存在于 `logic/solution/method.md` 的三行 "Innovation Handles" 里，没有任何显式的对比论述。

---

## 二、期刊匹配度对比

### IEEE Access — Fit: **Medium-Low**

| 维度 | 评估 |
|---|---|
| 范围 | ✅ power & energy 是其最大领域之一，预算约束组合优化完全在 IEEE 兴趣域内 |
| 评审哲学 | ✅ soundness-not-novelty，组件组合式创新（"first bidirectional local-search NSGA for project review"）符合其 4/4 全文语料的"组合+场景适配"模式 |
| **统计规范** | ❌ **致命短板**。语料明确：metaheuristics 论文的社区规范是 **50+ 独立运行 + Wilcoxon/Friedman + 收敛曲线/箱线图**。p6 当前是 4 次逐位相同的确定性 repeat，有效 n=1，距离这条 bar 差了整整一个量级。审稿人按 metaheuristics 规范审，这是直接 reject 项 |
| 决策模型 | ⚠️ 二元 accept/reject、一次重投机会——proxy 指标构造 + 无统计检验这种"可修但没修"的问题在无 revision 循环的模型下代价最大 |
| 自我抄袭风险 | ❌ **p5 已定投 IEEE Access**。两篇同管线、同数据、同基线的论文进同一刊，CrossCheck 相似度 + 可能同一 Associate Editor 手上撞车，"not distinct from prior publication" 红线风险在所有选项中最高 |

结论：除非 p5 改道，否则 p6 不应投 IEEE Access；即便 p5 改道，也须先补齐 50+ runs 统计规范。

### MDPI Energies — Fit: **Medium**

| 维度 | 评估 |
|---|---|
| 范围 | ✅ 能源相关性强：电网项目组合/投资规划落在 "electrical power & energy systems / energy economics" section，techno-economic 分析是其明示范围 |
| 证据 bar | ✅ 对 p6 有利：0/29 接收论文做显著性检验、无 30-run 要求、单测试系统是常态（~2/3）、规划类论文靠 scenario self-comparison 即可过——p6 的 8 场景自比较 + 6 外部基线**超出**其语料下限 |
| 敏感性分析 | ⚠️ **近强制（缺失是第一大 major-revision 触发器）**。p6 有 budget_sensitivity 场景槽位和 loose_budget 消融，但没有系统的多预算水平曲线——这正是该刊审稿人必问的 |
| 硬性合规 | ⚠️ Funding/COI/Data Availability/Author Contributions 100% 必备；proxy 数据可用模板化声明过关 |
| 撞车风险 | ❌ 双重占位：**p3（CARS-MODE）和 p4（SHIELD-MOEA）都已定投 Energies**，再加 p6 就是同一编辑部三篇同组"MOEA + SimBench/RTS + hypervolume proxy"套路论文；且 **Energies 是 p5 的 backup journal**——若 p5 被 IEEE Access 拒后转投 Energies，与 p6 同刊同源正面相撞 |

结论：单看评审 bar，Energies 是三刊中对 p6 当前证据形态最宽容的；但组合层面的撞车/查重暴露风险使它不是好选择。

### Applied Sciences（当前目标）— Fit: **Medium-High，仍是最稳妥选择**

- ✅ **应用价值逻辑契合**：该刊 11 篇语料显示"真实案例 + 量化收益"可替代方法学基线，而 p6 反向拥有强方法学证据（6 基线 + 9 消融），远超其语料下限（4/11 零基线也能过）；需要补的是"beneficiary sentence"（谁用：电网规划/投资评审部门）。
- ✅ **敏感性分析是该刊的"应用可信度货币"**（6/11 有，审稿人问"结论能否扛住 ±20% 参数摆动"而非 p 值）——p6 的 budget_sensitivity 槽位天然对齐，做成多预算水平曲线即是加分项。
- ✅ **诚实的 limitations 与接收正相关**（8/11）——p6 ARA 的 proxy 边界声明直接转化为 Limitations 节即可，且 `constraints.md` 的证据保留纪律（v1/v2 弱证据留档）符合该刊候选人画像。
- ✅ **组合排布最优**：p6 留在 Applied Sciences 意味着 mintou 六篇分布为 IEEE Access(p1,p5) / Electronics(p2) / Energies(p3,p4) / Applied Sciences(p6)——p6 与同源的 p5 **分处 IEEE 与 MDPI 两个出版社**，CrossCheck 语料库虽互通（都用 iThenticate），但避开了同一编辑部对姊妹稿的直接感知，是六篇组合里对 p5/p6 同源风险的最优对冲。
- ⚠️ 注意其语料中 **metaheuristic 子领域正在抬 bar**（7–9 基线、30-run + Wilcoxon 协议 2026 年开始出现）——p6 有 6 基线，建议至少补 seeded 多次运行，把统计短板消掉一半。
- ⚠️ IF≈2.9 低于 Energies(≈4.0) 和 IEEE Access(≈4.2)，若单位考核看 IF/分区，这是保留 Applied Sciences 的唯一实质代价。

### 最终推荐

**保留 Applied Sciences 为第一目标**（Section 建议：Energy 或 Electrical, Electronics and Communications Engineering）。若追求更高 IF 且愿意补做 50+ runs 统计包、并确认 p5 时间线错开 ≥3 个月，IEEE Access 可作 backup；**不建议 Energies**（p3/p4 已占 + p5 backup 撞车）。

---

## 三、写作修改清单（对照期刊惯例）

1. **与 p5 的差异化必须显式成文**（无论投哪刊，这是 P0 级）：
   - 在 Related Work / Introduction 中加一段（若 p5 先发表则引用之，若未发表则在结构上彻底避开其表述）：**BiLo-NSGA 的双向局部搜索**（forward 添加 / backward 删除 / 替换移动，逐移动审计轨迹）**vs TRACE-MOEA 的协同进化 + 评审规则修复 + 偏好感知排序**——机制、算子、搜索结构三个层面写清区别；
   - 问题设定差异化贯穿全文：p6 是**预算硬约束下的组合选择**（budget as first-class constraint，配 budget_sensitivity / loose_budget 证据），p5 是**投资有效性与可追溯性**——标题、摘要、贡献列表、实验命名都要围绕"budget-constrained"锚定，删除与 p5 摘要同构的句式（当前两 PAPER.md 的 Abstract/Boundary 段近乎模板复制，直接触发 CrossCheck）；
   - 两文若共用候选池生成代码，应将其定位为"共享公开 benchmark"并在 Data Availability 中声明，而不是各自默不作声。
2. **指标命名诚实化**：`hypervolume_proxy` 是含 trace-completeness、ranking-stability 等分量的**自定义复合指标**，不是标准 hypervolume。必须给出精确数学定义、说明与标准 HV（含参考点）的关系，并（见实验清单第 3 条）报告剔除 trace 分量后的结果——否则 "metric 为方法量身定做" 是最易被抓的软肋。Energies 语料明确把"自定义指标上的夸大百分比"列为侥幸过关项，不要赌。
3. **贡献列表**：IEEE Access 惯例是 3–6 条编号贡献；MDPI 惯例是 gap statement + 组合式创新框架。两者都要求**每个混合组件有单独动机**（Energies 语料把"混合算法无分组件理由"列为审稿抓手）——forward search、backward search、dependency moves、feasibility recovery 各写一句"为什么需要"。
4. **Applied Sciences 特有**：加 beneficiary sentence（"grid planning departments / provincial power grid investment review boards can use..."）；面向多学科读者定义领域术语（非支配排序、hypervolume、预算约束组合）；诚实 Limitations 节（proxy 标签、无负荷流校验、单测试系统）。
5. **分项 trade-off 诚实呈现**：BiLo-NSGA 在 reliability/renewable benefit proxy 上低于基线（1.334 vs 1.786；128.8 vs 162.4），要在 Results 正文承认并解释（预算约束下的取舍），不能只报复合指标——审稿人会自己算。
6. **MDPI 硬性合规**：Data Availability Statement（公开数据源 + 生成代码链接）、CRediT 作者贡献、Funding、COI 一个不缺；MDPI 模板、~200 词摘要、3–8 关键词、编号引用；自引克制、文献覆盖近 3 年（`related_work.md` 目前只有一行指针，综述本体待写）。
7. **英文清晰度**：IEEE Access 把 English/clarity 列为显式接收标准；三刊评审窗口都短（MDPI 首决 ~15–17 天），投稿时必须已是近终稿。

---

## 四、实验设计缺口

1. **【最高优先】随机化 + ≥30（IEEE Access 则 50+）seeded 独立运行 + 统计检验**。当前 `real_project_review_results.csv` 中 4 个 repeat 逐位相同——算法无随机源或种子未生效，有效 n=1。需给 GA 初始化/变异注入受种子控制的随机性，跑 30–50 seeds，报告 mean±std、Wilcoxon 符号秩（vs 各基线）、Friedman + 事后检验（跨场景），配箱线图与收敛曲线。这是 IEEE Access metaheuristics 社区的准入线，也是 Applied Sciences 2026 metaheuristic 子领域正在形成的 bar；即使 Energies 不强制，做了就是跨刊通用资产。
2. **Ground truth 有效性——proxy 标签需专家子集回验**。当前"评审质量"完全由自定义 proxy 定义。最低要求：抽取 20–30 个候选项目做专家（或基于 NERC 事件报告的规则化外部标准）标注，报告 proxy 排序与专家排序的 Kendall τ / Spearman ρ；否则至少用 pandapower 负荷流对选中组合做可行性外部校验（`real_project_review_analysis.md` 的 Compliant Optimization Path 本来就列了这两条）。没有任何外部效度锚点时，3.87% 的增益只是"在自家尺子上量自家孩子"。
3. **指标分量敏感性**：复合 proxy 含 move_trace_completeness（proposed 恒为 1.0，基线 0.56–0.73）。必须报告**剔除该分量后的排名**——若 BiLo-NSGA 仍领先，循环论证质疑即被拆除；若不领先，这是必须在投稿前知道的事实。
4. **预算敏感性系统化**：现有 budget_sensitivity 场景 + loose_budget 消融不够。做预算水平扫描（如基准预算的 50%/75%/100%/125%/150%），画 hypervolume、feasibility、组合规模随预算变化曲线——这同时满足 Energies 的"近强制敏感性分析"与 Applied Sciences 的"±20% 参数摆动"审稿习惯，且正是 p6 区别于 p5 的问题设定卖点。
5. **9 个消融重组——并非都有信息量**：`loose_budget` 和 `low_dependency_density` 是**场景/数据变体而非组件消融**，应移入敏感性分析；真组件消融中 no_forward_search(1.5699)、no_dependency_moves(1.5668)、no_feasibility_recovery(1.5186) 数值扎堆且这三者的 reliability/renewable 分项与另一组完全不同（0.834/85.1 vs 1.786/162.4），提示消融实现可能改变了场景配置而不仅是组件开关——投稿前必须核查每个消融"只关一个开关"。保留 6–7 个干净组件消融即可，配"分量贡献归因表"（forward 贡献 vs backward 贡献不对称：去 forward 掉 0.140，去 backward 仅掉 0.067，这本身是值得讨论的发现）。
6. **标准多目标指标补充**：至少补标准 hypervolume（声明参考点）+ IGD 或 spacing，与自定义 proxy 并列报告。
7. **计算公平性声明**：BiLo-NSGA runtime 0.00086s vs 基线 0.00013s（≈6.6 倍）。IEEE Access 语料中"统一计算预算/公平性声明"出现在 2/4 接收论文中且读作加分项——给基线等量评估预算或在文中明确报告成本差。
8. **第二测试系统（P1 级）**：单系统在 Energies/AppSci 是常态可过，但补一个（本地已缓存 nrel118 或 tamu_test_cases 派生池）能显著加固，且天然与 p5 的候选池错开。

---

## 五、数据集缺口

1. **真实项目组合/预算决策公开数据基本不存在**：电网投资评审记录属于机构内部数据（对标文献中 ~25 篇用不可下载的匿名中国电网数据，见 `papers/literature/target_journal_related/dataset_coverage_analysis.md`）。p6 的"公开基准派生候选"路线是正确的替代，但必须在论文中**完整公开候选生成规则**（哪类网架元素→哪类项目、成本/收益如何合成、NERC 报告元数据如何映射为可靠性特征），并把生成代码纳入 Data Availability——否则"benchmark-derived"读起来像黑箱合成数据。
2. **与 p5 共用数据管线的复现与公开问题**：两文共用 `src/powergrid_benchmark/mintou_real_project_review.py` 与相同的 120 候选池。若各自承诺开源，重合立即可见。两个可选处理：(a) **差异化候选池**——p6 用不同 seed/不同 source 配比/不同池规模（如 200 候选 + 更高依赖密度，呼应其 dependency_constrained_review 场景），成本低且顺带回答"结论是否依赖特定候选池"；(b) 把管线发布为**单一命名公开 benchmark**，两文都引用它——更体面但要求两文时间线协调。二选一，不能不选。
3. **本地数据可用性良好**：`CACHE_STATUS.md` 确认 rts_gmlc、simbench、c2ges_nerc_reports 均已本地缓存（另有 matpower/pglib_opf/nrel118 可扩展第二系统，pandapower 可做负荷流校验）——所有 P0/P1 实验无需新增下载。
4. **专家标签获取路径**：若无法接触电网评审专家，替代方案是用 NERC 事件报告（已缓存 28 份 event reports）构造规则化"事后验证"标准（如：与真实可靠性事件区域/类型匹配的项目应被优先选中），作为半外部效度检验并在 Limitations 中如实定位。

---

## 六、优先级行动清单

### P0（不做即有实质退稿/学术诚信风险）
1. **注入受控随机性，跑 ≥30 seeded runs，补 Wilcoxon/Friedman + mean±std + 箱线图**（当前 4 repeats 逐位相同，n=1）。
2. **指标去循环化**：给复合 proxy 精确定义并改名（如 review-quality composite index）；报告剔除 move_trace_completeness 分量后的排名；补标准 HV（含参考点）。
3. **与 p5 全面差异化**：重写所有与 p5 PAPER.md 同构的文本；方法对比段（双向局部搜索 vs 协同进化）；问题锚定（预算硬约束 vs 投资有效性）；候选池差异化或共享 benchmark 二选一；确保两文投**不同出版社**（p6 留 Applied Sciences，p5 留 IEEE Access）且错开投稿时间。
4. **核查消融实现**：确认每个组件消融只切换单一开关（当前三个消融的分项指标数值模式异常，疑似连带改变了场景配置）。

### P1（决定评审走向 major revision 还是 accept）
5. 预算水平扫描曲线（50%–150%），作为独立敏感性小节（Energies 近强制、AppSci 货币、p6 卖点三合一）。
6. pandapower 负荷流可行性外部校验 + 专家/规则化子集回验（Kendall τ），给 3.87% 增益一个外部效度锚。
7. 消融重组：场景变体（loose_budget、low_dependency_density）移入敏感性；保留干净组件消融 + forward/backward 贡献不对称讨论。
8. 分项 trade-off 诚实呈现（reliability/renewable proxy 上低于基线）+ 计算成本公平性声明。
9. Related Work 本体撰写（当前只有一行指针），覆盖预算约束组合优化、电网投资规划、局部搜索增强 MOEA 三条线，近 3 年文献为主，自引克制。

### P2（投稿包完善）
10. 第二测试系统（nrel118 或 tamu 派生池）。
11. MDPI 模板 + Data Availability（含候选生成代码开源声明）+ CRediT/Funding/COI；beneficiary sentence；Limitations 节（proxy 标签、无专家标注、单/双系统边界）。
12. 收敛曲线、Pareto 前沿可视化、移动审计轨迹示例图（explainability 是 p6 的差异化证据，值得一张好图）。
13. 投稿前用 iThenticate 类工具对 p5/p6 终稿互查一次相似度；核对 Applied Sciences 当期 Section/Special Issue 列表与 APC（官方页面为准）。

---

## 进展更新（2026-07-13）

**P0-1、P0-2、P0-4 已完成**：与 p5 共用的 `mintou_real_project_review.py` 已重写为 v2 真实算法版（v1 保留为 `*_v1_deprecated_circular.*`）。BiLo-NSGA 为真实实现：NSGA-II 内核 + 前向插入/后向删除双向局部搜索 + 依赖感知移动加成 + 可行性恢复；全部 9 个消融是单一机制开关；30 seeds/方法/实验 + Mann-Whitney U + Holm（`tables/real_project_review_significance.csv`）；move 统计只作描述列。

**v2 真实结果**：BiLo-NSGA 池化平均 HV 0.17267，比最强基线 NSGA-II（0.17000）高 **1.57%**，48 组基线对比中 **44 组 Holm 显著、零显著败绩**——信号 `significant_public_signal`，是六篇中当前统计上最扎实的公开信号。**组件级发现（必须如实写）**：NoBackwardSearch 消融以 +0.16% 微超完整方法，即后向删除算子是轻微负贡献；建议要么改进该算子（如接受准则退火）、要么在消融讨论中直接呈现这一不对称性（前向插入是主要贡献源，NoForwardSearch 掉到 0.17171）。

**预算敏感性已部分内建**：实验轴现覆盖 0.75x/0.88x/1.0x/1.2x 四档预算（budget_sensitivity / budget_constrained_selection / 基准 / scalability），可直接汇成预算扫描小节（P1-5 的 50%–150% 全曲线仍建议补）。

**仍未完成的 P0**：与 p5 的文本/叙事差异化（P0-3，管线共享改为"共享公开 benchmark + 两种不同方法论"的显式声明后风险可控，但正文文本仍需重写）；外部真值回验同 p5。

---

## 进展更新（2026-07-14，NERC 规则回验 v1）

外部真值阶梯第一级已完成（`src/powergrid_benchmark/mintou_review_backtest.py`，证据：`evidence/tables/real_nerc_rule_backtest.csv` + `evidence/runs/real_nerc_rule_backtest_analysis.md`）。设计已规避构造循环：规则分 = NERC 报告主题的类型权重 ×（未经 NERC 调整的原始候选属性）压力分位。

结果（如实）：proposed 方法 priority capture 1.34–1.62（>1 = 组合向 NERC 记录的风险模式集中）——**一致性底线通过**；但 AHP-TOPSIS 对齐度最高（capture 1.6–2.3、Kendall τ 0.44–0.52 显著），这是偏好排序法直接加权可靠性属性的构造使然。**引用边界**：本回验只能作外部一致性证据，不能作方法优势证据；proposed 的 τ 不显著（多目标权衡会稀释单维对齐是预期行为，须如实写）。阶梯下一级 MISO MTEP 历史回验仍是投稿前的真外锚。
