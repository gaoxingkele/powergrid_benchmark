# 闽投六篇论文：学术叙事逻辑审核

**审核日期：** 2026-08-12  
**审核模式：** 只读、投稿前、证据链导向审核  
**审核对象：** 六篇当前 `manuscript/MANUSCRIPT.md` 版本  
**采用的 paper 系列 skill：** `academic-research-suite` / `academic-paper-reviewer`，并分别用 `ieee-access`、`mdpi-electronics`、`mdpi-energies`、`mdpi-applied-sciences` 校准目标期刊标准。

本轮没有改动六篇正文、实验数据或结论。审核重点不是篇幅和图表数量，而是检查每篇是否形成同一条可核验的链条：

> 题目 → 摘要 → 研究缺口 → 贡献 → 方法组件 → 实验对照 → 统计解释 → Discussion → Conclusion

严重程度采用：**Major**（会影响主结论、方法身份或审稿判断，投稿前应解决）、**Minor**（不改变核心结论，但影响表达可信度）和 **建议增强**（不阻止当前叙事成立，但能提高外部有效性）。

---

## 一、总体结论

六篇目前的问题已经不是“实验数量不足”或“论文写得太短”。主要风险集中在四处：

1. **算法名称或标题中的核心词，没有被独立实验结果支持。** P3 的“参数适应”和“策略池”被一个组合消融同时关闭；P4 标题中的 `Lookahead` 在方法和实验中没有对应机制；P6 用特殊定义维持 `Forward-Dominant`，但去除 forward 的配置在 pooled mean 上反而更高。
2. **负向消融已经诚实报告，但叙事仍把未获支持的组件放在方法品牌中心。** 这在 P2、P3、P4、P5、P6 都不同程度存在。负结果不是缺陷；真正的问题是题目、贡献和 Discussion 是否据此重新分配方法价值。
3. **统计显著性主要描述随机种子变化，不能替代时间、年份、网络或真实项目的不确定性。** P1/P2 尤其需要区分 seed-level variability 与 data-sampling / temporal-origin uncertainty；P3–P6 则需要区分 proxy optimizer 的稳定性与电气/投资应用有效性。
4. **“可追踪的软件产物”容易被外推为“真实决策支持价值”。** P5/P6 的 trace coverage 很高，但尚未进行人工审阅、解释充分性或投资评审效用验证。当前可以声称 trace production / inspectability，不能声称 review quality 已改善。

### 总体分级

| 论文 | 目标期刊 | 叙事链状态 | 期刊匹配 | 审核结论 |
|---|---|---|---|---|
| P1 DSTAR-GRU | IEEE Access | 基本闭合 | 高 | **Minor Revision** |
| P2 CSA-LoadNet | Electronics | 主结果成立，但叙事防御性强，统计外推较窄 | 高 | **Major Revision** |
| P3 CARS-MODE | Energies | 框架故事较强，但组件归因存在内部矛盾 | 高 | **Major Revision** |
| P4 SHIELD-MOEA | Energies | 实验充分，但标题—方法身份不一致 | 高 | **Major Revision** |
| P5 TRACE-MOEA | Energies | 优化与追踪两条主线尚未汇成一种被验证的应用价值 | 中等 | **Major Revision** |
| P6 BiLo-NSGA | Applied Sciences | 实验透明，但完整方法与“精简有效版本”身份拉扯 | 中高 | **Major Revision** |

这里的 Major Revision 不等于必须全部重跑实验。P3、P4 的首要问题可以通过准确重命名和重新限定组件归因解决；P2、P5、P6 如能增加高价值实验会更强，但叙事修正本身仍是第一步。

---

## 二、跨六篇的系统性叙事问题

### 2.1 论文不应写成“证据许可表”

六篇在此前严谨化过程中大量加入 `claim`、`frozen`、`archive`、`descriptive`、`not established` 等限定。严谨性本身是优点，但 P2、P5、P6 已出现明显的“回复审稿意见式”行文：正文持续解释不能声称什么，导致研究问题、机制发现和工程含义退到第二层。

建议统一采用三层边界：

- Introduction 末尾集中定义研究范围；
- Results 首次报告关键结果时保留必要限定；
- Limitations 集中说明外部有效性。

其余段落应正面陈述已经观察到的事实。与其反复写 “does not establish...”，不如使用精确名词，例如 “seed-level comparison on the selected proxy benchmark”。

### 2.2 “组件存在”不等于“组件带来性能增益”

当前六篇大多已经做了充分消融，但方法品牌仍容易把组件实现和组件收益混在一起。叙事中应严格区分三种结论：

1. **机制已实现且确实改变输出；**
2. **机制在某些条件下有显著增益；**
3. **机制在总体或目标应用上有普遍价值。**

只有第 2、3 类能够使用 `improves`、`benefit` 或 `dominant`。对于未获支持的组件，应写成 method descriptor、decision-support feature 或 unresolved design choice，而不是 accuracy mechanism。

### 2.3 统计单位与科学推广单位不一致

多次随机种子可以评价训练或搜索随机性，却不能自动回答：

- 换一个天气年份是否仍成立；
- 换一个时间起点是否仍成立；
- 换一个电网或候选池是否仍成立；
- 换一批真实投资项目是否仍成立。

因此，六篇结果中的 p 值应服务于所选数据上的 algorithmic variability，而不能承担跨年份、跨系统或真实工作流推广。P1/P2 的最有价值扩展是 rolling-origin / alternative-year validation；P3/P4 是独立网络上的优化与 AC 联动；P5/P6 是专家评审、校准成本和真实项目级效用。

### 2.4 共享资产不是问题，但版本与独立性必须一目了然

P3/P4、P5/P6 已披露共享候选生成或公共语料，这一点是正确的。当前仍有两项明确的版本不一致：

- P4 参考文献 42 仍把 P3 写成旧题目 `A Strategy-Adaptive...`，而 P3 当前题目为 `Constraint-Aware Repair and Strategy-Pool...`；
- P5 参考文献 28 仍把 P6 写成旧题目 `Bidirectional Local Search...`，而 P6 当前题目为 `Forward-Dominant Project-Level Local Search...`。

这两处必须在投稿前同步。对未公开的 companion manuscript，应准备供编辑和审稿人核查的稳定版本；正文只需一次说明共享资产与独立的研究问题、算法、运行记录和推断结论。

---

## 三、逐篇审核

## P1 — DSTAR-GRU

**题目：** *An Operating-State Retrieval Framework and Reproducible Curtailment-Risk Benchmark for Power System Decision Support*  
**目标期刊：** IEEE Access  
**判断：** 当前六篇中叙事闭环最好，建议 Minor Revision。

### 已闭合的证据链

- 研究缺口分成公开 onset benchmark 和 retrieval 跨 horizon 行为两部分，贡献与之逐项对应（`MANUSCRIPT.md:35–43, 77`）。
- 70% SNSP-type cap 被明确界定为 method-independent policy-derived proxy，而不是观察到的真实弃电记录（`25, 41, 87–100`）。
- 结果没有把提出方法写成全局赢家：Persistence 领先总体 MAE，Ridge 领先 24 h onset；论文把真正发现定义为 retrieval utility 的跨 horizon 反转（`328–336, 427–429`）。
- Discussion 将 retrieval 解释为 smoothing / persistence prior，同时明确这是与排序一致的机制假设，而非已证明的因果机制（`396–400`）。

### 叙事一致性检查

- **题目→摘要：通过。** 两者都把公开 benchmark 和 operating-state retrieval 作为双核心。
- **缺口→贡献：通过。** G1 对应 benchmark，G2 对应跨 horizon 机制分析。
- **方法→实验：通过。** matched removal/degradation controls 能直接检验 retrieval，而不是只比较不同模型家族。
- **结果→结论：通过。** 结论保留跨 horizon 反转，没有将提出方法写成总体最佳。

### 需要修改

1. **[Minor] `Siamese` 命名仍可能引起误读。** 论文已经说明只有共享 encoder，没有独立 contrastive loss（`198–205`）。建议首次定义时使用 `shared-encoder (Siamese-style) retrieval`，后文避免让读者预期标准孪生训练目标。
2. **[Minor] 删除宣传式复现句。** `Reproducibility is a one-command property, not an aspiration`（`268`）更像宣传语。改成客观报告命令、时间和产物即可。
3. **[Major evidence boundary, not narrative failure] 十个 seed 只描述训练随机性。** 当前单一时间切分不能给出年份或事件块不确定性。正文已承认这一点，应保证摘要和结论不把 Holm p 值外推为跨年份稳健性。
4. **[Minor] `decision support` 应始终由 benchmark/proxy 限定。** 目前题目可以保留，但 Featured/Application/Conclusion 不应从 proxy onset forecasting 推导实际调度收益。

### 最强反方意见

该目标由固定政策规则构造，而不是实际 dispatch-curtailment；NREL-118 固定 cap 又产生零正例。因此论文最可靠的贡献是公开 benchmark 与 horizon-dependent mechanism finding，而不是通用 curtailment predictor。

### 建议动作

- **必须：** 统一 `Siamese-style` 定义；去除宣传句；继续保持 proxy 限定。
- **建议增强：** 增加 rolling-origin 或不同 cap 的多切分统计，但当前中心故事不依赖新增实验才能成立。

---

## P2 — CSA-LoadNet

**题目：** *Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region Power Load Prediction*  
**目标期刊：** Electronics  
**判断：** 标题与当前可支持的 aggregation 贡献已经匹配，但需 Major Revision 重写叙事层次与统计解释。

### 已成立的主结果

- OPSD 24 h 中，full model 优于十 seed MLP 和 no-aggregation ablation；这是论文最清楚的正向结论（`28, 323`）。
- Poincaré、Euclidean 和 equal-weight 参数化未分离，论文没有继续把 hyperbolic geometry 写成优势。
- Ausgrid 被重建为真实层级后，DLinear + bottom-up 最准确；论文正确区分 forecast accuracy 与 hierarchy coherence（`28, 379`）。
- OPSD 1 h、SimBench 和 Ausgrid 的负向或未决结果均被保留，标题聚焦 day-ahead，方向正确。

### 叙事一致性检查

- **题目→摘要：通过。** 当前题目已不再以 hyperbolic geometry 为核心。
- **缺口→贡献：部分通过。** aggregation gap 清楚，但贡献被 p 值、筛选历史和边界说明占据。
- **方法→实验：部分通过。** no-aggregation ablation 很强；外部 baseline 的确认预算不完全对称。
- **结果→结论：通过但过度防御。** 结论边界准确，正文却反复解释“不能声称什么”。

### 需要修改

1. **[Major narrative] 贡献列表像“结果审计摘要”，不像研究贡献。** `A significance-backed positive result...` 等表述（`50`）把 p 值和筛选历史写进贡献。建议重构为：方法集成、组件识别设计、跨数据层级评价；具体显著性放 Results。
2. **[Major narrative] 删除作者期待与纠错过程。** `This section reports the result we did not want...`（`357`）不应出现在论文。改为中性报告几何变体不可区分，并讨论其机制含义。
3. **[Major narrative] `Evidence Hierarchy and Claim Calibration`（`423`）是审稿回复式标题。** 建议改成 `When Cross-Series Aggregation Helps` 或 `Interpretation Across Horizons and Hierarchies`。
4. **[Major statistical framing] 外部基线存在 preliminary screen 后再确认 MLP 的选择路径。** 其他四个模型只有三 seed screen，OPSD 主表中的“strongest external baseline”不能被读成完整的十 seed SOTA 比较（`46, 50, 323, 343`）。应明确是 targeted comparator，不是全面 baseline superiority。
5. **[Major statistical boundary] 单一 chronological split + 约一个 weather-year。** 十个 seed 不测量时间起点或天气年份敏感性（`142, 447–449`）。如果不补实验，主结论必须限定为 OPSD selected split 的 day-ahead aggregation effect。
6. **[Minor] 主分析使用 Mann–Whitney，而相同 seed 可形成配对。** 当前把 paired sign-flip 放为 post-freeze sensitivity（`286`）是诚实的，但 Methods 应解释为何独立样本检验是 primary，避免给人统计选择过程凌驾于 estimand 的印象。

### 最强反方意见

论文唯一明确的外部正向单元来自 preliminary screening 后选择的 MLP、单一时间切分和十个训练种子；在精确层级数据上，简单 DLinear 更好。因此论文应被理解为“在一个 day-ahead multi-region cell 中确认 aggregation 有用”，而不是一种普遍更好的 neural forecasting architecture。

### 建议动作

- **必须：** 重写贡献、负结果段和 Discussion 标题；消除“我们原本希望”的元叙事；把 MLP 定义为 targeted external comparator。
- **高价值增强：** rolling-origin / alternative weather-year 重复；在 OPSD 对主要外部模型进行同等十 seed 确认。

---

## P3 — CARS-MODE

**题目：** *CARS-MODE: Constraint-Aware Repair and Strategy-Pool Multi-Objective Differential Evolution for Distribution Network Expansion Planning*  
**目标期刊：** Energies  
**判断：** 框架结果、敏感性和 AC 有效性讨论较强，但组件归因存在一个必须修复的内部逻辑矛盾，建议 Major Revision。

### 已成立的主结果

- 在 proxy benchmark 上，完整框架稳定优于外部 baseline，包括 matched-repair NSGA-II、GDE3 和 NSDE。
- 论文没有掩盖 FixedDE nominally +0.60% 且全部未决，也没有把 adaptive controller 写成已获支持的准确率机制（`17, 404`）。
- AC 组合级检查显示 proxy ranking 不等于 electrical ranking；CARS-MODE 为 mid-pack，这一负向 transport finding 对 Energies 很有价值（`435–437, 496`）。
- repair 与 diversity 的强消融结果、预算敏感性和 AC 层构成完整的应用验证链。

### 叙事一致性检查

- **题目→摘要：通过。** 新题目已避免直接宣称 strategy adaptation 带来优势。
- **缺口→贡献：部分通过。** component attribution 是核心缺口，但现有 FixedDE 不能完成所声称的分离归因。
- **方法→实验：存在 Major 缺口。** 组合消融无法识别参数和策略两个开关。
- **结果→结论：基本通过。** proxy–physics disagreement 被正确提升为主要有效性发现。

### 必须解决的逻辑矛盾

1. **[Major] 论文声称组件可独立开关和 one-switch-per-run（`37, 58`），但 `Ablation-FixedDE` 同时做了两件事：固定 F/CR，并把 two-strategy pool 改为 single rand/1（`278, 404`）。** 这个实验无法分别识别 parameter adaptation 与 strategy-pool adaptation。

   可选解决方案只有两种：

   - 新增两个分离消融：`FixedParameters+AdaptivePool` 与 `AdaptiveParameters+SingleStrategy`；或
   - 不补实验，把所有 `strategy adaptation is neutral`、`each component independently switchable`、`one-switch-per-run` 改为 **combined adaptation bundle is unresolved**。

2. **[Major] Contribution 4 把组合消融写成 strategy adaptation 结论（`40`）。** 必须与上面的处理同步。
3. **[Minor] `runtime_scalability`（`142`）是内部场景名，却实际表示 1.20× loose-budget。** 主文改为功能名称，内部标签放补充材料。
4. **[Minor] repair 的作用存在 pipeline interaction。** 从 CARS 删除 repair 损失 6.84%，但给 NSGA-II 加 matched repair 只增加 0.11%。因此结论应是 repair 在 CARS pipeline 中 load-bearing，不能写成 repair 一般性提升所有 optimizer。

### 最强反方意见

完整框架的 proxy 优势可能主要由 repair 和 diversity 产生；被品牌化的参数/策略适应未显示收益，且当前消融不能分开两者。与此同时，proxy 优势没有转化为 AC 排名优势。

### 建议动作

- **必须：** 分离消融或统一改称 `combined parameter-and-strategy adaptation bundle`；同步修改摘要、贡献、Methods、Results、Discussion 和 Conclusion。
- **建议增强：** 多 seed/多 compromise 的 AC 映射或把 AC 可行性直接纳入搜索，但当前应用叙事在准确限定后仍可成立。

---

## P4 — SHIELD-MOEA

**题目：** *SHIELD-MOEA: Scenario Handling with Isolated Evaluation and Lookahead for Distribution-Network Resilience Planning*  
**目标期刊：** Energies  
**判断：** 实验强度、AC 扩展和负结果处理均较好；但标题—方法身份出现直接不一致，建议 Major Revision。

### 已成立的主结果

- 场景搜索与 final evaluation 使用 disjoint draws，能够避免直接 scenario reuse；这是可信的 protocol contribution。
- 框架优于外部 baseline，repair 是主要 load-bearing component。
- screening 降低 65% 的 objective-call count，但没有质量或 wall-clock 优势；dynamic re-screening 不优于 fixed worst-K，hybrid 不优于 DE-only，显式 resilience objective 也没有 HV 增益（`431–435`）。这些负结果报告充分。
- 六网络、1296 个 AC cases 显示方案优于 no-plan，但略低于 matched-repair NSGA-II，并揭示 outage exposure 的组成级电气差异（`469–504`）。这符合 Energies 对工程验证和敏感性的要求。

### 叙事一致性检查

- **题目→摘要：不通过。** `Lookahead` 没有可定位的方法定义或结果。
- **缺口→贡献：部分通过。** uncertainty-interface gap 清楚，但 adaptive re-screening 的独立收益未获支持。
- **方法→实验：通过。** targeted controls 与 AC checks 足以识别哪些组件有效、哪些未决。
- **结果→结论：通过。** 结论已经把贡献收窄为 workflow、repair、disjoint evaluation 和边界证据。

### 必须解决的问题

1. **[Major] 标题中的 `Lookahead` 只出现在标题，方法、伪代码、消融和结果均未定义 lookahead。** 当前实现是 population-dependent worst-K screening、periodic update 和 disjoint final evaluation，不是已明确实现的 lookahead mechanism。

   推荐题目方向：

   > *SHIELD-MOEA: Scenario Screening with Disjoint Evaluation for Distribution-Network Resilience Planning*

   如果坚持 `Lookahead`，必须给出形式化定义、算法位置、控制实验和结果；仅靠品牌解释不够。

2. **[Major narrative] 论文方法品牌仍强调 adaptive scenario exposure，但 periodic re-screening 对 fixed generation-1 worst-K 为 0/8 分离（`435, 537–541`）。** 主贡献应调整为 scenario-selective workflow + disjoint evaluation + resolved repair effect，而不是 adaptive update benefit。结论目前已经接近这一正确定位（`595`），题目和 Introduction 需同步。
3. **[Minor] `each mechanism can be switched off individually` 和 `one-switch-per-run`（`164`）应逐项核对 targeted controls 是否确实保持其他条件不变。** 如果 control 位于补充实验而非主 ablation table，需要在 Methods 中说明两类实验的关系。
4. **[Minor] 65% 是实现层 objective-call count，不是时间或能耗节省。** 论文目前已有明确限定（`249, 431, 523`），摘要/结论继续保持即可。

### 最强反方意见

SHIELD-MOEA 的主要可复现收益可能来自 repair 和严格 evaluation protocol；screening 只减少调用数，dynamic update、hybrid variation 和 resilience objective 均未显示 front-quality 增益。题目若继续使用 `Lookahead`，会被认为将未定义机制包装为核心创新。

### 建议动作

- **必须：** 删除或实证定义 `Lookahead`；把主线收束为 scenario screening、disjoint evaluation、repair 与 outage-aware composition evidence。
- **必须：** 将 P3 companion citation 更新为当前题目。
- **建议增强：** 在昂贵 simulator 上验证 screening 的实际时间收益；不属于当前投稿叙事成立的必要条件。

---

## P5 — TRACE-MOEA

**题目：** *TRACE-MOEA: Traceable Multi-Objective Evolution with Preference-Guided Ranking for Power Grid Investment Review*  
**目标期刊：** Energies  
**判断：** 优化实验充分、边界诚实，但期刊应用证据与中心价值仍偏弱，建议 Major Revision。

### 已成立的主结果

- 在七个 proxy review scenarios 和 30 seeds 上，框架相对 NSGA-II 有 0.89% pooled HV 优势，并进行了多 baseline、Holm 校正和 direct R-NSGA-II budget scan（`27, 381–478`）。
- preference-layer ablation 只有 0.17% 且未决，论文没有把总体优势归因于 preference adaptation（`27, 438`）。
- trace archive 与 objective/selection 隔离，98.6% 表示 returned-front projects 至少有 logged intervention，而非 explanation quality；这一边界写得正确。
- NERC/MTEP16 被明确写为 descriptive external consistency，而非真实 review performance。

### 叙事一致性检查

- **题目→摘要：部分通过。** 方法确实 traceable 和 preference-guided，但 `investment review` 的实际效用尚未验证。
- **缺口→贡献：部分通过。** 可追踪优化的缺口清楚；优化增益和人工审阅价值尚未通过共同 endpoint 连接。
- **方法→实验：通过。** preference ablation、direct comparator 和 quarantine invariant 均有对应检查。
- **结果→结论：通过但负荷偏重。** 边界准确，provenance/descriptive 说明重复过多。

### 需要修改

1. **[Major narrative] 优化和 trace 是两条并行故事，但尚未形成被验证的共同应用结果。** 0.89% HV 回答 proxy optimization；98.6% coverage 回答 software trace production；没有实验回答 trace 是否提高人工评审质量、速度、一致性或信任。中心故事应改为 **inspectable portfolio search**，而不是已验证的 investment review improvement。
2. **[Major venue fit] 对 Energies 而言，能源系统验证较弱。** 没有 AC/潮流层、校准成本、真实约束或专家评审。能源相关候选和公共记录足以支撑 scope，但若突出实际 investment review，需要至少一种真实效用验证。否则应更明确定位为 reproducible proxy study，或考虑 Applied Sciences / IEEE Access 一类更接受系统与复现贡献的目标。
3. **[Major narrative] `Preference-Guided` 可以作为方法描述，但不能被写成性能来源。** 当前 direct budget scan 支持完整方法优于 R-NSGAII，不能自动支持 adaptive preference layer，因为内部 removal contrast 仍未决。
4. **[Minor] provenance / archive / descriptive 限定出现过密。** 将 trace quarantine 定义一次、external consistency 限定一次、human-value limitation 集中一次，减少审计语气。
5. **[Minor] `individually switchable components`（`45`）需区分 search components 与 output-only instrumentation。** trace archive 不进入算法决策，关闭它不能形成 accuracy ablation；不要把它与 preference/repair 的性能消融放在同一因果层级。
6. **[Major version consistency] 参考文献 28 使用 P6 旧题目。** 必须更新为 P6 当前稳定标题或在两稿定稿后统一。

### 最强反方意见

不到 1% 的 proxy HV 增益和高 trace coverage 尚不能说明更好的投资评审；对真实记录的相关性检查包含构念重叠，且有简单 AHP/Weighted 方法在某些 alignment 指标上更好。论文最可靠的贡献是 quarantined trace architecture 与可复现 benchmark，而非实际 review superiority。

### 建议动作

- **必须：** 重写中心故事为 `traceable/inspectable portfolio optimization`；将人类评审价值明确留作未验证问题；压缩 provenance 元叙事。
- **必须：** 更新 P6 companion title。
- **高价值增强：** 小规模专家 blind review（可追溯性、解释充分性、审查时间）或至少一个电气/预算真实性验证。

---

## P6 — BiLo-NSGA

**题目：** *BiLo-NSGA: Forward-Dominant Project-Level Local Search for Budget-Constrained Power Grid Portfolio Review*  
**目标期刊：** Applied Sciences  
**判断：** 算法比较、消融和统计透明度满足应用型 metaheuristic 论文的基本结构，但方法身份与应用价值仍有拉扯，建议 Major Revision。

### 已成立的主结果

- 完整方法相对 NSGA-II pooled HV +1.12%，在多 stochastic baselines 和 direct Pareto Local Search 下有充分比较（`377, 522–528`）。
- runtime、front size、trace volume 和 coverage 同时报告，避免只展示精度（`398, 493–506`）。
- forward 与 backward 两类局部操作的负向/异质结果被完整保留：NoForward pooled mean 更高；NoBackward 和 legacy deletion 也 nominally 更高且未决（`420–422`）。
- NERC/MTEP16 只作为 descriptive consistency，广义与严格标签敏感性都被展示。

### 叙事一致性检查

- **题目→摘要：部分通过。** project-level local search 成立；`Forward-Dominant` 需要特殊定义才成立。
- **缺口→贡献：通过。** budget-aware project-vocabulary moves 与普通数值邻域的差异清楚。
- **方法→实验：通过。** forward、backward、repair、legacy rule 和 direct PLS 均有对应实验。
- **结果→结论：部分通过。** 负结果报告充分，但 full method 与 lean forward-only recommendation 尚未形成单一方法身份。

### 需要修改

1. **[Major title/identity] `Forward-Dominant` 依赖特殊定义。** Full 只在 3/8 primary scenario cells 中显著优于 NoForward，而 NoForward pooled mean 反而高 0.39%；论文把 dominant 定义成“resolved gains only occur on forward side”（`420`）。这一定义透明，但标题仍容易被审稿人理解为 forward insertion 总体占优。

   更稳妥的题目是：

   > *BiLo-NSGA: Project-Level Local Search for Budget-Constrained Power Grid Portfolio Review*

   若保留 `Forward-Dominant`，摘要必须立即给出异质性和 pooled counter-result，不能只在 Results 才解释术语。

2. **[Major method recommendation] 完整方法保留 atomic substitution，但其准确率收益未获支持；论文又推荐 forward-only 作为 lean implementation。** 应明确区分：

   - `Full BiLo-NSGA`：保留 project-substitution semantics 与 trace；
   - `Forward-only variant`：若只追求 proxy HV/效率，是当前更精简的候选实现。

   否则读者无法判断论文真正推荐哪个算法。
3. **[Major application evidence] 99.6% move coverage 不等于 explanation sufficiency 或 review utility。** Applied Sciences 可以接收应用框架，但标题中的 portfolio review 仍需要将真实价值限定为 project-vocabulary moves + inspectable history，而非评审效果。
4. **[Minor] 不同 budget scenarios 同时改变权重和 seed streams，不能作为受控 budget sensitivity。** 论文已经承认（`408`），图表和结论中统一叫 cross-scenario variation；不要简写为 budget sensitivity evidence。
5. **[Minor] P5/P6 的共享资产说明充分，但 P6 参考文献表没有正式列出 TRACE-MOEA。** 如果正文以 companion study 作为 gap/independence 论证，应提供稳定可核查的正式条目或补充材料入口；两稿处理应对称。

### 最强反方意见

完整算法的两个品牌化局部组件都没有 pooled accuracy advantage；forward-only 更快且精度相近/略高，atomic substitution 的价值目前只是语义和 trace。真实项目 backtest 又是弱描述性结果。因此完整 BiLo-NSGA 的必要性尚不能由性能证明，只能由 representation/inspectability 论证。

### 建议动作

- **必须：** 重新决定是否保留 `Forward-Dominant`；明确 full 与 lean variant 的推荐场景；不要把 substitution semantics 写成 accuracy gain。
- **高价值增强：** 专家对局部 move trace 的可理解性评价、校准成本或 load-flow/project constraint 验证。

---

## 四、按优先级的统一修改顺序

### P0：投稿前必须修复

1. P4 删除/定义标题中的 `Lookahead`。
2. P3 修复 `FixedDE` 组合消融与“独立开关/单组件归因”的矛盾。
3. P4→P3、P5→P6 的 companion paper 题目同步；P6 对 TRACE-MOEA 的引用处理与 P5 对称。
4. 六篇作者、单位、通讯作者、CRediT、基金与数据可用性中的占位项全部核对；这属于投稿阻断项，虽不属于叙事逻辑。

### P1：学术叙事重构

1. P2 删除“我们不希望得到的结果”、evidence hierarchy、claim calibration 等元叙事。
2. P5 把中心价值定为 inspectable portfolio optimization，避免把 trace coverage 写成人类评审效用。
3. P6 明确 full 与 forward-only lean variant 的身份；评估 `Forward-Dominant` 是否值得保留在标题。
4. 六篇都把限制集中到 Methods scope + Limitations，减少正文反复否定。

### P2：证据增强

1. P1/P2：rolling origins、不同年份或替代时间切分。
2. P3/P4：多 seed/multi-plan AC coupling 或独立系统优化。
3. P5/P6：专家评价、真实成本/约束、人工评审效用或电气验证。

---

## 五、最终编辑判断

六篇已经具备方法、实验、图表、消融和统计基础；当前主要不是“再堆更多结果”，而是让题目、算法身份和最终结论只承载实验真正支持的内容。

- **P1** 已基本达到 IEEE Access 对技术可靠性和完整证据链的要求。
- **P2** 具备 Electronics 可接受的组件研究，但要从“项目纠错叙事”转为“aggregation 在何时有效”的科学问题。
- **P3/P4** 具备 Energies 所重视的工程验证和敏感性；必须先修复组件归因和标题机制身份。
- **P5** 的能源应用效度是六篇中最弱的一项，建议收紧 review claim 或补真实效用证据。
- **P6** 的 Applied Sciences 方法实验基本够强，但要明确完整算法为何保留未获准确率支持的组件。

完成 P0 与 P1 后，六篇会从“证据很多但叙事偶尔与证据拉扯”，转变为“主问题清楚、负结果有机制意义、贡献边界稳定”的投稿版本。
