# C²GES 第一轮独立审稿：算法理论、创新性与领域价值

## 审稿人定位

电力技术文本分析、图排序与可解释机器学习方向的领域审稿人。本报告只评价创新性、理论基础、定义精度、算法内在逻辑、组件可识别性、术语边界和电网领域价值；不将软件执行正确等同于方法有效性。

## 总体建议

**Major Revision（大修）**；信心 4/5。

稿件最可信的贡献是：建立了可审计的长技术报告抽取流程，给出了可复算的类型路径删除量，并用严格 no-CF 单因素消融保留了不利结果。稿件对证据边界的自我约束显著强于通常的算法稿。但是，标题中的 “Causal and Counterfactual” 仍会使读者预期结构因果模型、干预语义或反事实文本，而当前方法实际上是基于词汇角色的有向叙事代理图和节点删除路径中心性。其唯一可识别的新通道在测试集和开发集校准中均未显示 ROUGE 增益。因此，现有证据可支持“可审计的结构敏感性诊断”，不能支持“因果/反事实机制有效的摘要算法”，也尚不能支持“for Power Grid Maintenance Reports”的实证应用价值。

## 主要优点

1. **组件对比可识别。** strict no-CF 只将 $C_i$ 的系数由 0.15 置零，不重归一化、不改变候选、图、冗余项、预算或 tie rule；这使 Full--no-CF 成为稿件中最干净的组件对比。【证据：`paper_applsci.tex` L229--L235】
2. **路径删除量具有明确可复算恒等式。** $C_i=U(G)-U(G_{-i})=\sum_{p\ni i}\operatorname{strength}(p)$，并用合成示例和测试不变量解释；这足以证明其不是简单 weighted degree 的同义实现。【证据：L197--L225，Eq. (1)--(2)，Table `tab:toy-path`】
3. **没有隐藏反向消融。** Full 相对 no-CF 在两个预算均低约 0.0033，置信区间跨零；开发集后验校准在 12/12 folds 选择零权重。稿件将机制“被执行”与机制“有效”明确分开。【证据：L407--L425、L483--L499】
4. **证据层级和外部效度边界清楚。** 稿件反复说明 NERC 是技术报告代理语料，不是维护工单；ROUGE 不是安全性、事实充分性或工程效用。【证据：L39--L49、L112--L118、L525--L541】
5. **内部选择过程确定、可审计。** 五步选择、稳定源顺序 tie breaking、路径上限 fail closed、候选到页面定位链均被说明。【证据：L241--L245】

## 主要问题与可执行修改

### 1. “Causal/Counterfactual” 术语仍然超过数学对象

**严重性：Major。** 当前有向边来自词汇角色、源顺序、距离和 token overlap；稿件明确否认 SCM、处理、潜在结果和物理干预。节点删除量本质上是对预先构造路径集合的加权参与度/影响中心性，而不是反事实结果。【证据：L69--L75、L183--L206、L513--L521】

现有大量免责声明降低了误读风险，却不能完全抵消标题、方法名和 “causal role” 对读者预期的塑造。尤其 Eq. (2) 的恒等式说明删除操作没有生成替代世界，只是在固定图上汇总包含节点的路径权重。

**无需新数据可修复：**

- 在标题、摘要首次出现和方法小节标题中加入 `structural proxy` 或 `node-deletion sensitivity` 限定。若必须尽量保留原标题，可采用“Causal-Role and Counterfactual-Inspired Graph-Enhanced ...: A Structural-Proxy Evaluation ...”一类最小变化，而不是只在正文事后解释。
- 全文建立术语表：`causal-role cue`、`typed textual proxy edge`、`node-deletion structural sensitivity`；仅在方法名称中保留 counterfactual，并禁止将 $C_i$ 写成 causal effect。
- 将 $C_i$ 与加权路径中心性/路径参与度的关系明确写入 novelty paragraph，说明真正的新意是特定角色约束、路径范围和审计式消融的组合，而非反事实识别。

**需要新数据才能修复的更强主张：** 若作者希望保留无修饰的“causal/counterfactual”科学含义，需要专家验证的关系标注，或明确 SCM、干预变量、可识别假设和可检验反事实结果；当前语料与设计不能提供这些内容。

### 2. 理论构造可执行，但核心公式主要是启发式而非理论推导

**严重性：Major。** 路径强度使用边权几何均值乘以 stage span/4，路径限定 2--4 edges，边距 horizon 为 12，最终通道权重为 0.15。这些定义可复算，但稿件没有说明为什么该函数应与摘要效用单调一致，也没有证明所需性质，例如长度公平性、尺度稳定性、稀疏图退化行为或对单个错误 role 的敏感度。【证据：L183--L206、L229--L243】

**无需新数据可修复：**

- 增加“设计公理与性质”小节：非负性、节点删除单调性、路径长度归一化、stage-span 奖励、无合格路径时 $C_i=0$、对图同构/稳定顺序的确定性。
- 给出边权的完整公式，而不只说“combines distance, Jaccard and role confidence”；逐项给范围、归一化、零值与 tie 条件。【当前缺口：L183--L187】
- 解释几何均值与 stage span 的选择：几何均值避免路径长度带来的乘积衰减，但 span/4 又偏好跨阶段路径；说明两者是否会抵消或强化路径长度偏好。
- 增加复杂度上界的正式符号表达，区分固定 horizon 下的 edge checks 和受 cap 约束的路径枚举。

**需要新数据/实验：** 对 horizon、路径长度、span 因子和 edge-weight 分量做预注册消融；至少报告 role-only、degree-only、typed-path-without-span、不同 horizon 的独立影响。现有 147 配置只表明正 CF 权重没有胜出，不能回答每个结构设计是否合理。

### 3. 创新定位仍偏“所选 Applied Sciences 文献内的新组合”，不足以证明领域层面的新颖性

**严重性：Major。** Related Work 对句图、超图、MIS、技术报告和电力知识图谱进行了清楚分流，但 Table `tab:related-comparison` 主要覆盖作者选取的 Applied Sciences 邻近研究。稿件尚未系统回答：$C_i$ 与 path centrality、betweenness-like measures、graph deletion influence、discourse graph summarization 的最接近算法差异是什么。【证据：L53--L105】

**无需新数据可修复：**

- 以“表示—评分—选择—证据”四轴重写 novelty matrix：节点/边语义、路径函数、是否训练、是否有严格单通道消融、是否源链接、是否有领域专家验证。
- 对现有参考文献中的最近方法逐项说明“不可替代的算法差异”，避免以“不同数据集”代替算法创新。
- 将贡献强度定为“可审计的确定性组合与负组件证据”，不要写成新的因果摘要理论。

**需要额外文献核验：** 对路径中心性、节点删除影响和 discourse-graph summarization 做一次可复核的检索。若不能从已有本地文献证实优先权，应把“首次/novel”改为“we instantiate/we evaluate”。不要补入未核验引用。

### 4. 核心新通道没有效能证据，论文必须重新定义创新价值

**严重性：Major。** Full--no-CF 在 $K=5$ 和 $K=10$ 均为负，区间跨零；147 配置的开发校准中 zero-CF 12/12 folds 获胜。机制虽改变 28/30 个选择序列，却没有显示注册指标收益。【证据：L409--L425、L483--L499】

这不是应被“调参美化”的问题，而是组件效用假设被当前实验反驳。论文仍可成立，但价值应从“性能创新”转为“可证伪机制、严格消融和负结果”。

**无需新数据可修复：**

- 在贡献列表中明确区分：算法对象的新颖性、执行正确性、效能结果；把“不支持增益”提升为主结果，而非防御性限制。
- 删除任何暗示 counterfactual channel 提升整体摘要的措辞；系统高于外部基线不能归因于该通道。
- 讨论 $C_i$ 与 redundancy penalty 的潜在目标冲突：高路径参与节点可能偏长、偏通用或与已选内容重叠。

**需要新数据/实验：** 在全新 holdout 上测试重新设计的通道，并使用等词数预算及人类链覆盖指标；不得在已揭示 15-report test 上继续寻找有利设置。

### 5. RQ1 的系统级比较存在长度和调参机会不对称，不能承载算法优越性

**严重性：Major。** Full 比 Semantic-MMR/TextRank 长 54--63%，而 Full 经 144 个配置搜索、Semantic-MMR 系数固定 0.5。稿件已经披露这些问题，但摘要仍先给出 “exceeded” 数值，易被二次引用为性能优势。【证据：L257--L265、L370--L405】

**无需新数据可修复：** 在摘要和结论中将长度不匹配放在比较结论之前或同一句中；避免“outperformed”，只写“had higher equal-sentence ROUGE-L with substantially longer outputs”。

**需要新实验：** 全新冻结的 equal-word/equal-token budget；所有可调基线获得相同开发预算；报告效应量与报告层级不确定性。

### 6. 电网维护领域价值目前是合理动机，不是被验证的贡献

**严重性：Major。** 27 个保留报告来自一个公共机构；测试仅 15 报告；不存在维护工单、现场巡检记录、合格专家质量评分或 unsafe omission 评价。【证据：L39--L41、L531--L541】

**无需新数据可修复：** 将标题中的领域短语解释为 intended application 已经做得较充分，但建议在贡献列表中去掉任何“maintenance report benchmark”含义，统一称为 NERC technical-report proxy。

**需要新数据：** 至少一个 title-concordant 维护/巡检语料的外部 holdout；双人独立标注与裁决；评估 source faithfulness、cause/event/impact/mitigation coverage、unsafe omission 和导航时间/有用性。LLM 标注可以用于预筛，但不能替代 qualified expert validation。

### 7. role、edge 和 extraction-unit 误差没有定量验证

**严重性：Major。** 当前角色由 substring cue 唯一最大值决定，忽略否定、假设、引语、共指和语境；稿件只给未来 error taxonomy，没有现有误差率。【证据：L158--L187、L247--L253】

**无需新数据可修复：** 报告每类 role/abstention、edge、path 的覆盖率分布；这些可以从冻结图日志审计得到，不需要人工标签，但只能说明机制覆盖，不能说明语义准确率。

**需要新数据：** 对分层抽样的句子、边和路径进行盲法专家标注，报告 adjudication 前 agreement、精确率/召回率及否定/假设等分层误差。

## 内在逻辑核查

- 从 RQ2 到 Full--no-CF 的逻辑是成立的；该对比只能识别当前 $C_i$ 通道在当前 selector 中的增量作用，稿件对此界定准确。
- 从 Full 高于 Semantic-MMR/TextRank 到“图方法有效”不成立，因为 Full 与这些方法同时改变角色、图、权重、输出长度和调参机会。稿件多数位置已避免这一跳跃，但摘要呈现顺序仍需加强。
- 从 nonzero score difference/changed sequences 到“机制执行”成立；从机制执行到“机制有用”不成立，稿件已正确区分。
- 从 NERC proxy 到 power-grid technical-report behavior 可以有限成立；从 NERC proxy 到 maintenance workflow utility 不成立，稿件已承认。

## 标题与贡献主张裁决

当前标题**可作为保留历史连续性的工作标题，但不宜作为未经限定的科学结论标题**。若不愿大改，最低限度应在标题或副标题中出现 `structural proxy evaluation`。若标题完全不变，则摘要第一句、featured application 和结论中的限制虽能降低风险，但无法消除检索层面的过度承诺。

建议将核心贡献表述为：

> A deterministic, source-linked typed-role graph summarizer with an auditable node-deletion path-sensitivity channel, evaluated under strict leakage, ablation, and evidence-boundary controls.

不建议表述为：

> A causal/counterfactual method that improves maintenance-report summarization.

## 第一轮必须完成的修改清单

1. **P1/文字与公式审计：** 限定标题和所有 causal/counterfactual 术语；完整给出 edge-weight 公式、归一化和理论性质。
2. **P1/贡献重构：** 把创新定位从“性能提升”转为“可审计结构诊断 + 严格负消融”；删除可被误读的 superiority 语言。
3. **P1/文献定位：** 对 path centrality、node-deletion influence 和 discourse-graph summarization 做可核验的新颖性检索；无法核验则降低优先权措辞。
4. **P2/现有代码审计：** 从冻结日志补 role、abstention、edge、path coverage 的描述统计；不得将覆盖率称为语义准确率。
5. **P1/新实验：** 规划新 holdout 的等词数、对称调参比较，以及 title-concordant 专家评估。此项未完成前，不能升级维护有效性或组件效能主张。

## 给作者的问题

1. 若 $C_i$ 在开发和测试均不优于零权重，作者希望论文的首要算法贡献究竟是新评分函数，还是可审计地证伪该评分函数？
2. 路径几何均值、stage span/4、2--4 edges 和 horizon=12 分别对应哪些预先声明的设计原则？
3. 能否在不访问已揭示测试结果的前提下，从冻结开发资产报告 $C_i$ 与长度、degree、role、redundancy 的相关关系，以解释目标冲突？
4. 标题是否愿意增加 “structural-proxy” 限定，以使检索层面的承诺与正文证据一致？
