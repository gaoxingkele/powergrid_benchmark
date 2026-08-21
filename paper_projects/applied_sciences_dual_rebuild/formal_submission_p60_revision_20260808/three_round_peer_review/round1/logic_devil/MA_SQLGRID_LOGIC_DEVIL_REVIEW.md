# MA-SQLGrid 第一轮反方审稿报告（逻辑与证据链压力测试）

## 审稿范围与判定原则

- 审稿对象：`MA_SQLGrid/paper_applsci.tex`（P60 revision）。
- 本报告只审查核心论点、内部逻辑、证据—主张匹配、替代解释和过度外推；不修改稿件，也不替代统计方法或领域审稿。
- 严重性按单项问题对核心结论的影响判定。以下 Critical/Major 均给出可定位锚点和可执行修复。

## 真实优点

稿件没有把历史 GridDB、BIRD、组件、multi-state 和 v3 离线结果强行合并成一个准确率，也明确保留了同题结果暴露、高并列率、顺序敏感性、事故运行和语义歧义。这些披露构成可信基础。核心问题是：最重要的“robust multi-agent framework”主张恰好不是这些实验直接估计的对象。

## 最强反方论证

最强反对意见是：MA-SQLGrid 的实证部分评估的是若干历史提示流程、两个模型产生的混合候选池、SQLite 执行边界和一个结果已暴露后的确定性选择器，而不是题目所称的 robust multi-agent Text-to-SQL framework。五个“agent”中，Analyst 和 Cartographer 是确定性骨架，Synthesizer 不生成 SQL 而只包装外部字符串，Validator 和 Adjudicator 是规则程序；没有一个新的、调用匹配的端到端实验比较五角色协调与单调用或非代理管线。论文自己承认这一点，但随后用“framework identity”解释标题，并把彼此不兼容的历史证据作为框架贡献集合。

更简单的解释是：这是一个可审计的 SQL 安全执行器、候选池后处理器和多来源实验资产整合，而不是已验证的多智能体方法。v3 的结果尤其不能补上缺口：相同题目的金标准派生结果已在冻结测试中被访问，两个选择器在 130/180 题出现最高分并列，平均并列约 5.4，反转候选顺序就把 101/180 提高到 117–118/180；所谓三 witness 相对 validation-only 只改变 Q039 一题，而且该题语义仍有歧义。因此 101/180 主要反映历史候选供给、执行过滤和任意顺序，而不是协调理论或稳健语义判断。

读者可以认可其软件工程与审计价值，但无法从当前证据推出标题级方法贡献。要保留现标题，必须补做全新未见、物理调用匹配、候选数匹配、端到端五角色实验，并预注册并列/弃权规则与合格领域语义审查；否则应把论文明确重定位为 audited architecture and retrospective evidence study。

## 问题清单

### CRITICAL

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| C1 | 核心论点/标题—实验错位 | 标题以“Robust Multi-Agent Framework”为核心，但没有端到端五角色新生成实验，也没有调用和候选预算匹配的单体对照。主体角色是确定性骨架、外部候选包装器和规则执行器；历史实验明确不是五智能体运行。把 multi-agent/robust 定义为“framework identity”只能限制解释，不能提供正面效用证据。 | text: Title, line 15；text: Introduction, lines 38–52；text: Materials and Methods, “Five-Agent Coordination Framework”, lines 192–215；text: Limitations, lines 627–633；absence: prospective matched five-role versus single/staged controls — expected direct test of title-level contribution; checked all Methods and Results subsections | 5/5：论文多处直接承认该实验缺失 | 保留标题时必须新增全新未见、调用数/候选数/模型/解码/数据均匹配的端到端比较，并报告语义正确率、弃权、风险—覆盖、成本和故障；否则修改标题和贡献，将其定位为 auditable architecture plus retrospective evidence integration，而不是已验证的 robust multi-agent method。 |

### MAJOR

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| M1 | 最简替代解释/选择器不可辨识 | v3 的两个 adjudicating selectors 在 130/180 题最高分并列，平均并列约 5.4；原顺序几乎总选 Qwen，反序后完整 witness 结果从 101 变为 117–118。现有 80/100/101 差异不能被稳定归因于协调或 witness 证据，更简约的解释是“执行过滤 + 历史候选顺序”。 | table: `tab:offline`, `tab:ties`, and `tab:sensitivity`；text: Results, lines 502–555；text: Discussion, lines 609–613 | 5/5：结果直接显示高并列和大顺序效应 | 在新数据上预注册并列弃权/澄清规则；以随机但冻结的多次候选排列、顺序不变选择器或对称投票评估稳定性，并把候选来源作为分层因素。当前稿中不得将 100/101 相对 80 表述为协调增益。 |
| M2 | 理论基础不足/任意权重 | 40/40/10/5/5 的裁决权重、pass threshold 和稳定顺序规则没有理论推导、独立开发校准或预结果证据；稿件还承认 v3 规则无法证明早于同题派生结果访问。高并列说明这些低带宽特征没有提供足够判别信息。 | text: Materials and Methods, “Deterministic Adjudication and Abstention”, lines 219–225；text: same section, “v3 does not establish that their design preceded access…”；table: `tab:ties`；absence: independent calibration objective or decision-theoretic utility — expected principled adjudication basis; checked Methods and Supplementary description | 5/5：规则和证据时间线均明示 | 在仅开发集上定义决策效用（错误回答、弃权、调用成本），校准权重与 margin/abstention threshold，冻结后在未见集测试；或把权重明确降格为示例策略，不将其作为算法创新。 |
| M3 | 版本混合/“robust”证据归属 | 资源边界表把 raw-cell-byte、total-result-byte、width 和 function controls 纳入本文 robustness evidence，但这些 FINAL 控制未用于产生 v3 的 5760 attempts 或 80/100/101；同一“framework”叙述把历史 v3 结果和后置 FINAL 工程修复并列，容易形成组合系统已被整体验证的错觉。 | table: `tab:robustness`, especially Resource boundedness row；text: Materials and Methods, lines 203–205 and 312；text: Discussion, line 617；text: Conclusions, line 637 | 5/5：版本适用边界明确可核 | 把 v3 与 FINAL 拆成版本化证据矩阵：每项控制标明版本、测试和是否进入实验；若标题中的 robust 指 FINAL，需用 FINAL 重跑预注册实验；若不重跑，结果只能支持 v3 的旧边界和 FINAL 的独立单元测试。 |
| M4 | 内部证据阶级矛盾 | v3 在 chronology、Methods 和 Discussion 中被定义为 outcome-exposed descriptive re-execution，但 `tab:offline` caption 仍称其为“New v3 offline selection”。这与稿件自设的 New/Diagnostic 分类冲突，且可能让读者误读为前瞻性新结果。 | table: `tab:chronology`, v3 row；text: Materials and Methods, lines 142–144 and 308–312；table: `tab:offline` caption, line 486 | 5/5：同稿件内直接矛盾 | 将 caption 的 “New” 改为 “Descriptive release-v3 re-execution”；全文检索 `New`, `prospective`, `prespecified`, `outcome-unseen`，仅对符合稿件定义的证据保留。 |
| M5 | 结果可核性/配对分母缺口 | Qwen value-evidence 效应称为 +0.1059 over 170 eligible questions（即 18/170），但展示表只给 V0 83/170 与 V1 105/180，读者无法从表中复算配对的 V1 eligible 子集或其 2×2 rescue/harm。表中未配对的原始比例差为 0.0951，而非 +0.1059。 | text: Results, lines 365 and 369；table: `tab:componentcounts`；absence: paired V1 result on the same 170 eligible items and discordant-pair counts — expected reproducible paired contrast; checked Component Results and numerical table | 5/5：分母与展示数值可直接计算 | 增加同一 170 项的 V1 correct count、四格配对表（00/01/10/11 或 rescue/harm）、结构簇数、原始与调整后检验记录；避免用 180 项 V1 行作为 170 项配对效应的唯一可见依据。 |
| M6 | witness 概念外推 | M1–M3 只检验无关表、存储/索引和 nullable-column extension 下的结果不变性；唯一改变选择的 M3 有意惩罚 `SELECT *`，且 Q039 的自然语言语义未裁决。因此“complete metamorphic coordination”不能作为反事实语义、业务鲁棒性或协调质量证据。 | text: Materials and Methods, lines 300–306；table: `tab:q039`；text: Results, lines 531–551；text: Discussion, lines 609–611 | 5/5：变换定义和唯一差异均完整呈现 | 将其统一称为 constructed metamorphic execution witnesses；加入能区分业务语义的预注册、prediction-blind、领域审查状态族，或将该模块限定为 SQL projection/storage robustness diagnostic。 |

### MINOR

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| m1 | 图件数量陈述不一致 | 稿件实际包含六个 `figure` 环境，但 Supplementary 和 Acknowledgments 写“All four figure artifacts/scientific figures”。 | figure: `fig:coordination`, `fig:cells`, `fig:components`, `fig:multistate`, `fig:offline-diagnostics`, `fig:evidence-map`；text: Supplementary, line 643；text: Acknowledgments, line 649 | 5/5：可机械计数 | 将“four”改为“six”，并核对打包清单确实含六图及各自 lineage。 |
| m2 | “robust”定义可读性 | 稿件在多个位置重新限定 robust 的含义，说明该词本身持续诱发超范围解释。 | text: Introduction, line 52；text: Table `tab:robustness`；text: Conclusions, line 641 | 4/5：修辞逻辑判断 | 在标题或副标题中直接限定为 “read-only and evidence-complete”，减少正文反复防御；若保留原题，在摘要首处给出一行固定操作定义。 |

## 被忽略的替代解释或路径

1. **安全执行器 + 候选后处理器解释**：当前实现最直接的贡献是 SQLite 边界、证据账本和确定性后处理，而非多智能体推理。
2. **候选供给解释**：固定池的正确率主要由八个历史候选是否含正确 SQL 决定；选择器不能估计 generation benefit。
3. **顺序先验解释**：高并列下的 178/180 Qwen 来源选择是候选顺序的机械结果，而非 adjudicator 学到的模型质量。
4. **投影偏好解释**：Q039 的一题变化来自 M3 对 `SELECT *` 的结构偏好，并非对自然语言中“scheduled”或日期边界的理解。

## 未检验前提

稿件隐含假设“把一个流水线拆成五个有类型的职责，就足以使 multi-agent 成为方法创新”。职责分离提高可审计性，但 multi-agent 的科学贡献通常应表现为角色间信息流对性能、可靠性、成本或失败恢复的可识别影响。当前证据尚未测量这种影响。

## 非缺陷观察

- 负结果、高并列、反序敏感性和事故运行被保留，这是研究诚信优点；它们不应为了“数据好看”而删除。
- 不把 BIRD 非电网结果外推为电网语义有效性、也不把安全执行等同正确 SQL，逻辑上是正确的。

