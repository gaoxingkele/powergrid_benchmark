# 第一轮独立审稿：逻辑、论证与写作一致性（P1--P6）

**审稿角色：** 逻辑/论证/写作审稿人  
**日期：** 2026-08-12  
**范围：** 六篇最新版 `MANUSCRIPT.md` 及 `reviews/mintou_2026-08-11_above_mean_enhancement/` 下的冻结协议和事故记录。  
**边界：** 本轮不重算实验、不修改稿件、不推断证据表以外的结果；不能由现有证据确认之处标为「待核实」。

## 总体判定

六篇稿件都已具备完整论文结构，并普遍主动披露负消融、外部验证边界和实现失败记录，论证诚实度高于常见“只报正结果”的算法稿。但目前不宜原样投稿。最可能引发拒稿或大修的共同问题是：

1. 将“不显著”写成“相同”“无损”或“可替代”，但没有等效性检验或预设等效界值；
2. 由单个折中解、组成映射或观察到的共现关系推断组件的因果机制；
3. 摘要、贡献列表、结果段对比较对象的限定不一致；
4. 伴侣论文实际共享的实验概念或外部回测被写成“仅一方拥有”或“分析完全独立”；
5. 多篇文稿存在乱码字符，属于编辑初筛即可发现的生产质量问题。

建议六篇均先作一次集中逻辑修订，再进入统计学和领域专家轮。分篇判定如下：P1 大修、P2 大修、P3 大修、P4 大修、P5 大修、P6 小修至大修之间（核心算法主张较克制，但跨文稿声明和预算扫描逻辑必须修正）。

---

## P1：Operating-State Retrieval / Curtailment-Risk Benchmark

**总体判定：大修。** 主结论本身较克制，外部 NREL-118 零阳性也被诚实披露；但“击败所有无/弱检索学习方法”的中心贡献表述与 TCN 的非显著结果直接冲突。

### Major comments

1. **随机种子范围在摘要和方法中不一致。** 摘要称“All methods ... ten seeds”，而实验设置明确说明仅随机方法运行十个种子，Persistence、Seasonal、Ridge 和 raw kNN 为确定性单行结果。读者会误以为所有基线都具有同等重复性。

   建议将摘要中的相关句替换为：

   > All stochastic methods are evaluated over ten fixed seeds, whereas deterministic baselines contribute one reproducible run per setting.

2. **“every learned method”与 TCN 结果冲突。** Introduction 的贡献列表声称框架显著优于“every learned method that lacks or degrades retrieval”，但 Results 说明 TCN 与 DSTAR 经多重校正后不可区分。该表述会使审稿人怀疑作者选择性概括结果。

   建议将贡献句改为明确枚举受支持的比较集：

   > DSTAR significantly exceeds the prespecified retrieval-removal or retrieval-degradation controls NoSiamese, NoRetrievalBank, SmallBank, LSTM, and MLP after Holm correction; the TCN control narrows the gap and is not statistically separated from DSTAR.

   Results 中“every configuration that removes or degrades retrieval”也应采用同一限定，不能让 TCN 在语义上时而被纳入、时而被排除。

3. **raw-retrieval 对比不足以“证明”编码器在做真实度量学习。** 当前 Discussion 由 raw retrieval 更差推导出 encoder “is doing real metric learning”。该对比仍混合了表示、预测头和融合方式，最多支持与目标相似性更一致的解释。

   建议替换为：

   > The raw-retrieval control is consistent with the learned embedding being better aligned with near-term target similarity; it does not by itself isolate the encoder from the prediction head or blending mechanism.

### Minor comments

- 将“establishes a horizon-dependent sign reversal”限定为“on the tested benchmark and horizons”。
- 在首次报告 24 h onset 的 Ridge 优势时，立即说明它与总体 MAE 排名回答的是不同问题，避免读者把事件起点指标和全样本误差指标视为矛盾。
- 「待核实」：若各随机方法共享同一组种子，统计轮应说明为何采用 Mann--Whitney U 而不是配对检验；至少不能使用“seed-paired inference”描述非配对检验。

---

## P2：Cross-Series Attention / Multi-Region Load Forecasting

**总体判定：大修。** 精度与层级一致性的双结论具有价值，但当前存在一个外部基线排名矛盾、一个被废弃图表仍参与当前论证的问题，以及对非显著差异的等效性过读。

### Major comments

1. **“MLP wins every other external comparison”与 Ausgrid 结果冲突。** Introduction 将 MLP 描述为赢得所有其他外部比较，但 exact-hierarchy Ausgrid 结果显示 DLinear Bottom-Up 为最佳，CSA-OLS 次之。

   建议替换为：

   > MLP is the strongest external baseline in the OPSD 24-hour comparison; the exact-hierarchy Ausgrid experiment yields a different ordering, led by DLinear Bottom-Up.

2. **当前跨设置排名图与其自称“已被取代”的 Ausgrid 列不能同时成立。** Results 对 Figure 7 一方面称其为完整的 current rank profile，另一方面说明其中 Ausgrid 列已被 Figure 5 的 exact-hierarchy 排名取代，仅为 provenance 保留。被取代的数据不能继续支撑当前综合排名。

   可执行修复二选一：

   - 重新生成 Figure 7，以 exact-hierarchy Ausgrid 结果替换旧列；或
   - 从 Figure 7 的综合排名中删除 Ausgrid，并在标题和正文明确该图只覆盖其余当前设置。旧列只保留在补充材料的 provenance 图中。

3. **“indistinguishable”被进一步写成“matter of indifference”。** Poincaré、Euclidean 和 equal weighting 的 Holm 检验不显著，只能说明本设计下未解析出差异；没有等效性检验时不能断言权重形式无关或 equal weight 捕获了“全部可测收益”。

   建议替换 Results 中相关两句：

   > No difference among Poincaré, Euclidean, and equal weighting was resolved under the present seeds, horizons, and multiplicity correction. Equal weighting therefore provides a simpler empirically competitive option, not a demonstrated equivalent of the learned weighting schemes.

### Minor comments

- 若原文出现“Holm p ≥ 1”，应改成“Holm-adjusted p = 1.000”；调整后 p 值不可能超过 1。
- Figure 6 的“seed-paired relative changes”应与实际推断方法一致。若正式检验为 Mann--Whitney U，可写“seed-index-aligned descriptive changes”，并明确配对仅用于可视化。
- P2 的首次后处理事故仅为 `OLS`/`OLS-Reconciled` 标签不匹配且未影响数据；正文和图表应统一使用冻结协议的最终方法名，并把事故说明留在 provenance，而非主结果叙事。

---

## P3：CARS-MODE

**总体判定：大修。** 代理层的对比强度和负消融披露较好，但论文目前把单个组成映射得到的 AC 结果提升成了自适应机制的电气因果价值，这是最主要的论证风险。

### Major comments

1. **由一个折中组合推断自适应机制的“真实功能”，超出证据。** Methods 说明 AC 层只取每个方法/实验的 seed-0 折中方案，并通过确定性组成规则映射到网络；Results 也承认 AC 层不是统计充分的第二比较。然而 Introduction、Results 6.3 和 Discussion 又写成“AC validation reverses the ablation verdict”“the eighth storage unit adds over-voltage”“we justify strategy adaptation on electrical grounds”。单个组成差异无法排除折中解选择、映射规则、其他算子交互或随机变化。

   建议统一替换机制归因：

   > The seed-0 FixedDE composition contains one additional storage action and attains lower mapped AC feasibility than the full method. This descriptive pattern is consistent with storage-heavy proxy optima creating voltage stress under the fixed mapping, but it does not identify self-adaptation as the causal source of the electrical difference.

   Introduction 的贡献 4 建议改为：

   > The AC mapping reveals a proxy--physics disagreement and a descriptive full-versus-FixedDE composition difference; it does not overturn the statistically null proxy ablation or establish an electrical benefit of adaptation.

2. **“规划层整体有效”表述过宽。** Results 6.3 先说“all methods that return a non-empty feasible front improve AC feasibility”，随后承认 Weighted Sum 与 No-Plan 相同，并在高 DER 情景中多种规划法反而不如 No-Plan。应改成限定的聚合描述。

   建议替换为：

   > Most non-empty planning configurations improve aggregate AC feasibility over the no-plan reference, although Weighted Sum is tied with no planning overall and several methods deteriorate under the high-DER mapping stress.

3. **代理增益的比较对象在关键段落中不明确。** 摘要与贡献列表的 6.22% 是相对 NSGA-II+Repair；Results 6.1 同时给出相对 plain NSGA-II 的 6.34%；Results 6.3 又写“a hypervolume gain of 6.34%”而不点名比较对象，容易被读作与摘要不一致。

   建议改为：

   > The 6.34% proxy-HV margin over plain NSGA-II (6.22% over NSGA-II+Repair) provides no guarantee of AC-ranking transfer.

### Minor comments

- “robust proxy optimizer”应改为“a consistently higher-HV proxy optimizer across the seven tested scenarios”，避免把单一 SimBench 派生家族推广为稳健性。
- 将“adaptation's main measurable effect is electrical”改成“an observed electrical difference accompanies the adaptation ablation”；当前实验没有支持“main effect”的归因。
- 修复正文中的乱码减号、破折号和百分号（如 `鈭?3.56%`、`鈥?`）；这会显著降低编辑对稿件成熟度的判断。

---

## P4：SHIELD-MOEA

**总体判定：大修。** 该稿对负机制结果披露充分，但“40 个比较”的比较对象写错，且“leakage-proof/certifying/incapable”等绝对性语言超过了 disjoint-seed 设计实际能保证的范围。

### Major comments

1. **“40 comparisons against plain NSGA-II”在计数上不成立。** 八个实验对 plain NSGA-II 只有八个比较；40 应是五个预设外部基线乘八个实验。摘要写“40 prespecified baseline comparisons”较合理，Results 6.1 却写成“All 40 baseline comparisons against plain NSGA-II”。

   建议替换为：

   > Across the five prespecified external baselines and eight experiments, all 40 SHIELD-MOEA comparisons are Holm-significant wins; the eight comparisons specifically against plain NSGA-II are reported in Table 4.

2. **disjoint seeds 不能“认证”不存在场景专门化，也不能称结构上绝对防泄漏。** 它阻断了最终评分场景的直接复用，但研究者仍知道分布、范围、评价方式和超参数开发过程。unseen-stress 也只是在一组冻结范围上的外推测试，不是证明方法“不可能”专门化。

   建议全稿将“leakage-proof”改为“direct-reuse-leakage-controlled”，将贡献 1 改为：

   > Final fronts are scored on scenario draws not used during search, which prevents direct reuse of the scored realizations. The disjoint-range experiment further tests, but does not certify, resistance to search-range specialization.

3. **非显著差异被写成“without loss/preserve quality/yes”。** NoScenarioScreen 与完整方法 8/8 不显著，并不证明等效；Table 8 的“Does screening preserve quality? yes”尤其容易被统计审稿人否定。

   建议改成：

   > No front-quality difference was detected between screening and no screening in the eight experiments; screening reduced recorded objective-call count by 65%. Equivalence within a prespecified tolerance was not tested.

4. **worst-case 样本诊断被过度解释为“not specialized”与“degrade gracefully”。** Limitations 已承认 worst-case HV 仅来自 16 个样本、不能界定真实极值，Results 6.2 却给出更强结论，内部逻辑冲突。

   建议替换为：

   > On the sampled evaluation scenarios, the worst-case-HV margin is similar to the mean-HV margin. This is evidence against an observed mean--tail trade-off in the frozen sample, not a bound on true worst-case behavior or proof of non-specialization.

### Minor comments

- Discussion 的“validated full pipeline”改为“evaluated full pipeline”。
- Introduction 对现有鲁棒规划“一律单一最坏情形并标量化”的概括过宽；改成“many formulations considered here...”并逐项由引用支撑。
- “outage-aware search matters electrically”应始终保留“composition-level descriptive check”的限定，不能在 Practitioner reading 中省略。
- 修复乱码范围和破折号（例如 `4.8鈥?.0%`）。

---

## P5：TRACE-MOEA

**总体判定：大修。** 主结果的 0.89% 增益和弱外部对齐边界写得较清楚，但稿件将“完整方法相对 NSGA-II 的三处显著胜利”误归因给了仅有一处显著消融支持的 preference-adaptive layer；伴侣论文描述也与 P6 现稿冲突。

### Major comments

1. **完整方法对 NSGA-II 的差异不能直接归因给 preference layer。** Results 6.1 称三个偏好较强情景中 preference-adaptive layer “converts that emphasis into front quality”，但 Results 6.2 明确显示去掉 preference ranking 后总体只差 0.17%，七个情景仅一个显著。完整方法与 NSGA-II 还同时相差 repair、ranking/selection 实现和 archive-producing operations，三处胜利不能单组件归因。

   建议替换 Results 6.1 末段：

   > The full method separates from NSGA-II in three preference-emphasized scenarios. However, the dedicated NoPreferenceRanking ablation isolates a significant preference-layer contribution in only one scenario, so the three full-method wins cannot be attributed to preference adaptation alone.

   Discussion 的“conditional amplifier”应改成待检验解释：

   > One hypothesis is that preference adaptation acts as a conditional amplifier under pronounced stakeholder weights. The current ablation resolves this effect in only one scenario, so broader confirmation requires a preregistered weight/cadence sweep.

2. **伴侣论文边界声明与 P6 冲突。** P5 写“external-validity ladder exists only on this side”以及 TRACE-MOEA “performs MTEP16 outcome backtesting”；但 P6 当前稿也包含 NERC 与 MTEP16 两级回测。该冲突会使同时审阅两稿的编辑质疑重复发表或资产披露不完整。

   建议 P5/P6 采用相同声明，并明确数据、代码和统计表是否独立：

   > Both companion papers apply separately frozen NERC and MTEP16 checks to their own selected portfolios. They share the candidate-generation pipeline and external source corpora, whereas the optimization operators, run archives, selected portfolios, and reported method comparisons are paper-specific.

   若后半句不能由文件级证据确认，应标为「待核实」，不得直接声称完全独立。

3. **“zero metric cost”含义混乱。** archive 被隔离只能保证 trace statistic 不进入目标/选择，不能保证零计算成本，也不能由现有消融证明零性能成本。

   建议统一改为：

   > The archive is quarantined from objectives, constraints, and selection; coverage is therefore an audit-output statistic rather than an optimization metric.

### Minor comments

- “Hypervolume certifies optimization quality”改为“Hypervolume quantifies front quality under the frozen proxy objectives and normalization”。
- Results 6.5 将 Random Feasible 放在“evolutionary baselines”列表中，分类错误；改成“tested stochastic baselines”。
- “exact portfolio methods do not scale”以及“records are essentially never published”均过于绝对，应改成“may become difficult at this scale under richer dependencies”和“are rarely publicly available”。
- 作者中文名、章节范围和参考文献页码大量乱码（例如 `Sections 4鈥?`、`1.34鈥?.55`）必须在下一版全部清除。

---

## P6：BiLo-NSGA

**总体判定：小修至大修之间。** 标题和主结论已经正确承认 forward-dominant 而非 bidirectional gain，负消融也进入摘要，是六稿中主张边界最稳的一篇。但预算扫描存在自相矛盾，且与 P5 的共享资产/外部回测声明必须联合修订。

### Major comments

1. **预算扫描是否“只改变预算”在文内自相矛盾。** Section 3.3 和 Results 6.2 开头称五个 full-pool 实验“differ only in budget”，随后同段又说“scenarios differ in more than their pooled labels”，因而不是因果证明。两句不能同时成立。

   可执行修复：先由配置文件核实五行除预算外是否完全相同。

   - 若完全相同，写：

     > Across the full-pool configurations, the frozen objective definitions and candidate pool are held fixed while the budget multiplier changes; the duplicated 1.00x settings provide descriptive replication. The trend remains benchmark-specific rather than a universal causal law.

   - 若还存在其他差异，删除“controlled budget scan”和“differ only in budget”，改称“budget-indexed cross-scenario comparison”，并列出混杂项。

2. **伴侣论文“场景与分析独立”表述过强。** P5/P6 均使用同一 candidate generator，且当前两稿都使用 NERC 与 MTEP16 回测，并共享若干场景概念。可以声称方法、运行和结果资产分离，但不能笼统称“scenarios and analyses are independent”而不给文件级说明。

   建议与 P5 使用统一替换句：

   > The papers share the versioned candidate generator and external source corpora. Their optimization operators, frozen run archives, selected portfolios, and method-specific comparisons are separate; overlapping scenario labels and backtest sources are disclosed explicitly.

3. **LooseBudget 的结果被写成“confirming ... must”。** 单一代理基准上的 6.35% 差异支持当前实现中硬约束处理的重要性，但不能推出所有搜索必须如此。

   建议替换为：

   > The 6.35% deficit of Ablation-LooseBudget supports enforcing the budget during search in this benchmark and implementation; it does not establish a universal constraint-handling rule.

### Minor comments

- “real review lists essentially never published”“routinely exceeds one hundred”等行业事实应给直接来源或软化为研究动机，不要用无引用的普遍断言。
- “Every competent method improves with budget headroom”带有价值判断，改为“All evaluated non-degenerate methods show higher mean HV with additional budget headroom”。
- MTEP broad-label结果应始终与 unresolved-as-negative 假设相邻；摘要已有“weak-form”，正文和结论也应保留。
- 作者中文名和若干引号/破折号存在乱码，必须清除。

---

## 跨六篇的可执行修改顺序

1. 先修所有硬矛盾：P1 的 TCN、P2 的 MLP/Ausgrid 图、P4 的 40-comparison 对象、P6 的预算扫描定义。
2. 全局检索并替换未经支持的强词：`prove`、`certify`、`incapable`、`without loss`、`equivalent`、`unambiguous`、`real function`、`must`；逐句改为与设计相称的 `supports`、`was not resolved`、`is consistent with`、`within the tested settings`。
3. 将 P3、P4 的 AC 层统一定义为 composition-level descriptive validation，除非后续提供多种子/多折中解统计推断。
4. 联合修订 P5/P6 的共享资产声明，附一张内部资产矩阵：候选生成器、配置、run archive、外部源、映射/选择、统计表、图脚本分别是否共享。投稿正文只写经该矩阵核实的事实。
5. 修复六稿全部乱码并自动检查摘要、贡献列表、主表、结果和结论中的数字/比较对象一致性。

## 第一轮结论

现有主要数值结果不需要为了本轮逻辑问题而重跑；优先工作是准确限定比较对象和证据层级。只有下列情况需要在统计轮决定是否补实验：希望把“不显著”升级为“等效”；希望把 P3/P4 的 AC 组成差异升级为组件效应；或希望把 P5 的 preference layer 定义为稳定的条件增益机制。若不补相应实验，就必须采用本报告给出的克制措辞。
