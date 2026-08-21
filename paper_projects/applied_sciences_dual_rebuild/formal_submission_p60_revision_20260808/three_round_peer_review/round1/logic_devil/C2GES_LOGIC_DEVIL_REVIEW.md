# C²GES 第一轮反方审稿报告（逻辑与证据链压力测试）

## 审稿范围与判定原则

- 审稿对象：`C2GES/paper_applsci.tex`（P60 revision）。
- 本报告只审查核心论点、内部逻辑、证据—主张匹配、替代解释和过度外推；不修改稿件，也不替代统计方法或领域审稿。
- 严重性按单项问题对核心结论的影响判定。以下 Critical/Major 均给出可定位锚点和可执行修复。

## 真实优点

稿件主动披露了负消融、输出长度不等、开发集已暴露、维护场景未验证、文本图不等于物理因果图等关键限制；这种证据分层比把所有指标包装成“成功”更可信。问题在于，这些限定并未完全解除标题和核心方法命名造成的更强科学承诺。

## 最强反方论证

这篇论文最有力的反对意见是：它把一个基于词汇触发、预设叙事阶段和节点删除的确定性图排序器命名为“Causal and Counterfactual”，但既没有建立因果变量、干预、潜在结果或结构因果模型，也没有以专家标注验证边的因果语义；更关键的是，唯一能隔离所谓反事实通道的实验结果对该通道不利。Equation (2) 中的 $C_i$ 只是包含节点 $i$ 的注册文本路径强度之和，因此可解释为一种高阶路径中心性或结构敏感度。它是否应被称为 counterfactual，不由数学等式本身推出。Table 6、Table 7、Results/RQ2 和 Conclusions 又共同显示 Full 比 strict no-CF 低约 0.0033，区间跨零，开发集校准在 12/12 折选择零权重。因而，最简约且更符合现有数据的解释不是“因果—反事实机制虽然暂未改善 ROUGE”，而是“一个手工类型化图特征被赋予了因果/反事实名称，但现有语义证据和效用证据均未支持该命名所暗示的贡献”。

这并不使全部工作失去价值：完整 PDF 构建、泄漏审计、定位账本、确定性选择和负结果仍可构成一篇透明的技术报告或基准论文。但若标题和主创新继续以 causal/counterfactual 为中心，现有证据不足以维持该核心身份。可接受的修复只有两类：显著降格命名与主张，把它定义为 typed-path structural sensitivity；或者增加与标题同义的语义验证和全新未见数据实验。重复强调“不是物理因果”不能替代这种修复，因为它承认边界，却没有为保留强名称提供正面理论依据。

## 问题清单

### CRITICAL

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| C1 | 核心论点/基础坍塌 | 标题和方法身份以“Causal and Counterfactual”为核心，但方法只定义了词汇角色、预设有向转移和图节点删除；没有因果识别，且严格消融没有显示该通道的增益。现有理论与实证共同支持“结构路径敏感度”，不支持更强的因果—反事实贡献身份。若不修复，标题、创新点和结论之间的核心链条不成立。 | text: Title；Materials and Methods, “Typed Path-Deletion Structural Perturbation”, lines 195–206；equation: Equations (1)–(2)；table: Tables `tab:contrasts` and `tab:signflip`；text: Results, “Answers to the Research Questions”, RQ2；text: Conclusions, paragraph 3, lines 547–549 | 5/5：直接依据稿件定义和自身负消融 | 二选一：（a）将算法核心统一改述为“typed-path structural sensitivity/perturbation”，同步弱化标题、摘要、贡献和关键词；或（b）补做独立专家角色/边关系标注、与非因果高阶中心性等价模型的对照、预注册新机制及全新未见集验证。不能只增加免责声明。 |

### MAJOR

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| M1 | 标题—样本—应用外推 | 标题声称“for Power Grid Maintenance Reports”，实际样本是从 40 篇 NERC 技术报告中按可检测摘要与提取质量保留的 27 篇，测试仅 15 篇；没有工单、巡检记录或现场维护叙事，也没有维护人员评价。把 maintenance 解释为“aspirational intended use”不能使标题成为已评估研究对象。 | text: Abstract, first sentence；text: Introduction, paragraphs beginning “The exact title retains continuity” and “The proxy is nevertheless informative”；dataset: Materials and Methods, `tab:resources` equivalent sampling description, lines 136–156；absence: title-concordant maintenance records and qualified-user outcomes — expected direct maintenance-report evaluation; checked Abstract, Materials and Methods, Results, Discussion, Conclusions | 5/5：样本类型和未测终点均由稿件明示 | 最优修复是补一个许可清晰、冻结且未见的维护工单/巡检报告外部集，并由合格电网人员评估忠实性、链条覆盖和危险遗漏。若不能补实验，应将标题改为 NERC technical-report proxy 或在标题中明确 “A Proxy-Corpus Study”，并从摘要首句起把维护场景降为 future application。 |
| M2 | 替代解释/比较公平性 | Full 对 Semantic-MMR 和 TextRank 的优势可由更长且含表格融合块的输出解释；Full 平均多 54–63% 的词，且存在 37 个超 100 词单元和 40 个含 “Table” 的选择实例。与此同时 Full 接受 144 配置开发搜索，而 Semantic-MMR 系数固定。RQ1 和结论虽然附带限定，仍首先呈现“exceeded”结果，容易把不公平比较当作系统优势。 | table: `tab:length-audit`；figure: `fig:length`；text: Results, lines 393–405；text: Materials and Methods, “Development Selection and Comparators”, lines 257–265；text: Conclusions, paragraph 2 | 5/5：数值差异和调参不对称均有明确记录 | 在新的冻结协议上进行等词/等 token 预算比较，加入版面感知分割，并给主要比较器相称的开发调参机会；在完成前，将摘要、RQ1回答和结论中的“exceeded”改成长度审计前的原始描述值，不能作为优势句的主干。 |
| M3 | 确认偏差/机制保留理由 | 144 配置开发搜索选出的 Full 已比 strict no-CF 低 0.00567（K=5），正式测试仍保留正反事实权重；事后更广的开发搜索又在 12/12 折选择零权重。稿件没有给出为何在开发证据已经不利时仍把该通道作为完整模型核心的先验理论或决策规则。 | text: Materials and Methods, “Development Selection and Comparators”, line 257；text: “Post-Unblinding Development-Only Calibration”, lines 289–293；text: Results, same subsection；absence: a preregistered retention criterion for a development-negative named component — expected component-retention rule; checked Introduction contributions and all Methods subsections | 4/5：时间线清楚，但早期协议动机可能存在于未展示文件 | 明确写出原冻结时的组件保留规则及其时间戳证据；若不存在，应把 Full 重新定位为“被证伪的预注册候选”，以 no-CF 作为当前经验基线，而不是继续暗示 Full 是推荐系统。任何新版性能结论须使用新封存数据。 |
| M4 | 逻辑闭环/语义循环 | 角色词典先把句子标成 cause/event/impact/mitigation，注册转移再规定这些标签按单调阶段形成路径，最后路径数量被用来支持“因果链”可审计性。由于没有独立角色或关系金标准，这一链条只证明算法遵循自身规则，不能证明它发现了文本中的真实因果链。 | table: `tab:taxonomy`；text: Materials and Methods, lines 160–187；absence: independent role and directed-relation validity estimates — expected blinded semantic validation; checked “Known Linguistic Failure Modes”, Results and Discussion | 5/5：稿件明确承认零专家标签 | 增加双人独立标注及裁决，分别报告单元有效性、角色、边支持和链条覆盖的一致性与误差；并加入不使用因果角色命名的路径/中心性对照，检验收益来自结构还是词典先验。 |
| M5 | 证据等级/纠正性数据 | 论文的测试集来自纠正重建，早期版本诊断时已经检查过相关总体，作者承认无法恢复 outcome-unseen confirmatory status。若仍以常规性能论文口吻提交，15 报告区间和精确符号翻转只能描述该有限集合，不能承担确认性算法结论。 | text: Materials and Methods, “Task, Scope, and Evidence Class”, lines 112–118；text: “Frozen Evaluation and Statistical Interpretation”, lines 269–277；dataset: 15 selected test reports from one public organization | 4/5：证据等级由稿件自行认定 | 全文将该研究明确归类为 corrective/descriptive mechanism study；删去任何“验证有效性”式表达。若期望确认性贡献，必须另立协议、冻结未见总体和主终点，并在新样本上重复。 |

### MINOR

| # | 维度 | 问题描述 | 证据锚点 | 置信度 | 可执行修复 |
|---|---|---|---|---|---|
| m1 | 交叉引用 | “Accordingly, Table~1” 似乎指角色/转移表，但在新增表格后硬编码表号可能已错误。 | text: Materials and Methods, “Known Linguistic Failure Modes”, line 249, “Table~1” | 5/5：可直接定位 | 改为 `Table~\ref{tab:taxonomy}`。 |
| m2 | 摘要焦点 | 摘要的大部分篇幅用于限定不支持什么，导致可复现的正贡献（完整 PDF 构建、泄漏审计、定位账本）没有形成清楚的主要成果句。 | text: Abstract, lines 16–17 | 4/5：写作逻辑判断 | 在不削弱负结果的前提下，以“可审计数据/算法对象 + 核心负消融 + 适用边界”的三段式信息顺序重写。 |

## 被忽略的替代解释或路径

1. **高阶中心性解释**：$C_i$ 的行为可由注册路径上的节点参与度解释，无需 causal/counterfactual 术语；这是更简约且与 Equation (2) 完全一致的解释。
2. **版面长度解释**：Full 对若干外部基线的 ROUGE 优势可能主要来自较长、融合表格的提取单元，而非图排序质量。
3. **词典先验解释**：图效果可能来自 cause/event/impact/mitigation 词汇先验，而不是路径删除；需要与相同词典但不同结构分数的对照。
4. **官方摘要风格解释**：ROUGE 可能奖励复述 NERC 摘要常用术语和长解释块，而非工程师需要的危险、因果链和措施覆盖。

## 未检验前提

稿件隐含假设“可审计的结构机制本身足以构成算法创新”。可审计性是重要工程属性，但它不能自动证明命名的新机制在理论上独特、在语义上有效或在结果上有增量价值。若机制效用为负且因果语义未验证，创新性需要从方法名称转移到纠正性基准、证据边界和可复现实验设计上。

## 非缺陷观察

- 保留 Full 对 no-CF 的不利结果是正确做法，负结果本身不是缺陷；缺陷是仍让不受支持的机制承担标题级贡献。
- 对 bootstrap sign-tail、事后 exact sign-flip、选定总体和输出长度的限定总体上诚实且逻辑一致。

