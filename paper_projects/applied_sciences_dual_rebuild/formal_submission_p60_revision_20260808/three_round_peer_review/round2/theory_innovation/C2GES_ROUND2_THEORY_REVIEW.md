# C²GES 第二轮理论与创新性复审

## 复审结论

**建议：Major Revision（较第一轮明显改善，但尚未达到理论/创新席位的接收标准）。**

第一轮后，稿件已正确降低 RQ1 的优越性语气，补入固定图删除恒等式的性质，修正 toy example，并按冻结代码给出绝对句距、非文档顺序约束和精确边权公式；有限样本 composition interval、调参机会和实用意义不可识别也已明确。负消融继续完整保留。剩余风险已不主要是“隐瞒限制”，而是：标题和方法名仍以因果/反事实为核心，而可证理论只是固定文本图上的加权路径参与度；最近算法的新颖性定位不足；核心通道在开发与测试均无效能支持。编辑可能据此判断“实现和审计充分，但方法价值不足”。

## 第一轮问题逐项核验

| 第一轮问题 | 状态 | 严重度 | 第二轮证据与裁决 |
|---|---|---:|---|
| causal/counterfactual 超过数学对象 | **Partial** | Major | 摘要、引言和讨论已明确 textual proxy、非 SCM、非 do-intervention【TeX L19, L39--L43, L73--L75, L532--L540】；但标题仍为无修饰的 “Causal and Counterfactual”，关键词和组件名仍使检索读者预期因果推断。正文限定正确，标题层面的承诺仍未关闭。 |
| 路径删除理论性质不足 | **Partial** | Major | 新增非负性、nullity、path-additivity，并准确声明它是固定图记账恒等式而非 causal theorem【最新稿 L201--L214】。边权已按冻结代码完整定义为绝对句距衰减、Jaccard 与最小角色置信度的加权和，并声明 $w_{ij}\in[0,1]$【L183--L191】。命题和边构造现已可复核；仍未建立该函数与摘要质量、覆盖或维护效用的关系。 |
| toy path 算术不一致 | **Closed** | — | 路径强度和总和已改为 0.566964、0.741559、0.367423、0.542282，$U=2.218228$，root subtotal 1.308523；按 Eq. (1) 可复核【L197--L223】。 |
| 创新定位偏期刊内邻近文献，缺最接近算法比较 | **Open** | Major | Related Work 和 Table `tab:related-comparison` 仍主要比较 sentence graph/hypergraph、MIS、技术报告与电力 KG【L53--L105】；尚未直接处理 weighted path centrality、node-deletion influence、discourse graph centrality 与 $C_i$ 的关系。 |
| 核心 CF 通道无效能证据 | **Closed as a negative finding; Open as a positive-value claim** | Major | 稿件准确报告 Full 低于 no-CF、区间跨零、12/12 folds 选择零权重，并禁止将机制执行等同于有效【L426--L449, L510--L530, L570】。负结论已经关闭；若论文仍需“该通道有用”的正价值，则必须新实验，当前证据不能关闭。 |
| RQ1 长度与调参机会不对称 | **Closed for interpretation** | — | RQ1 已改为 equal-sentence descriptive comparison，显式包含 word-count imbalance【L37】；调参机会表把 no-CF 设为主要机制 comparator，外部 baseline 为 exploratory【L257--L282】；结果继续披露 54--63% 长度差【L410--L422】。 |
| 电网维护有效性未验证 | **Open—new data required** | Major | NERC proxy 与维护工单的边界反复说明【L39--L41, L544--L562】。诚实披露不能替代 title-concordant 维护语料和合格专家评价。 |
| role/edge 语义准确性未知 | **Open—new data required** | Major | 稿件列出否定、假设、共指、边连接等 failure taxonomy，但没有 role/edge/path 的专家 gold 错误率【L249--L255, L552】。 |
| 近重复/报告独立性 | **Partial** | Minor | 新增“未审计 revised editions/boilerplate/near-duplicates”的限制【L556】；问题被披露但未用现有文本 hash/minhash 或 metadata audit 定量检查。 |

## 理论命题核查

新增命题在其明确前提下是正确的：若删除节点只移除包含该节点的 qualified paths，且不重新计算剩余路径的边权，则

\[
C_i=U(G)-U(G_{-i})=\sum_{p\ni i}\operatorname{strength}(p).
\]

非负性要求所有 $w_e\ge 0$，nullity 要求节点不属于任何合格路径，additivity 来自对被删除路径集合的分解。稿件已经写明固定 role、coreference、discourse interpretation 和 surviving weights，这是必要限定【L208】。

但该命题属于**定义诱导的恒等式**，不能被作为以下命题的理论根据：

- $C_i$ 与 sentence importance 单调相关；
- 更大的 stage span 表示更高的工程信息价值；
- 节点删除近似文本反事实或物理干预；
- 将 $C_i$ 加入 $S_i$ 会提高 ROUGE 或专家质量。

稿件目前没有显式做这些越界推导，这是优点。仍应把“theoretical statement”称为“functional properties/accounting identity”，避免在 response 或 cover letter 中写成“theoretical guarantee”。

## 仍可能导致编辑拒稿的缺口

### 1. 核心方法价值与标题不匹配

**状态：Open；严重度：Major。** 标题把 causal/counterfactual 放在首位，但唯一对应通道在开发和测试均未显示注册指标收益；标题应用又是未经测试的 maintenance reports。即使正文完全诚实，编辑仍可能认为“标题承诺的两部分都没有正证据”。

**可执行修改：** 若必须最大限度保持原标题，至少增加副标题，例如 `A Structural-Proxy and Negative-Ablation Study on Public Power-System Technical Reports`；摘要第一句直接写 `Causal and counterfactual are names for textual-role and fixed-graph deletion proxies`。无需新数据。

**彻底关闭所需：** 新 sealed holdout、等词数对比、预注册重设计通道、maintenance-domain expert outcome。需要新数据。

### 2. 边定义已闭合，但 channel normalization 与效用依据仍不完整

**状态：Partial；严重度：Minor。** 最新稿已经精确给出

\[
w_{ij}=\operatorname{round}_{12}[0.45e^{-|\operatorname{pos}(i)-\operatorname{pos}(j)|/5}+0.30J_{ij}+0.25\min(r_i,r_j)],
\]

并明确 edge direction 来自 role transition，而非文档先后顺序【L183--L191】。这一修订关闭了实现与旧文字叙述不一致的风险。剩余缺口是 $Q_i,R_i,G_i,C_i,P_i$ 的具体 report-level normalization、全零退化和 numerical tolerance 尚未以统一符号表呈现【L231--L239】。

**可执行修改：** 保留现有边权公式，增加一张 channel 符号/范围表，明确各 channel 的 report-level normalization、全零退化和 numerical tolerance。无需新实验。

### 3. 新颖性仍未与最接近的图中心性对象正面对齐

**状态：Open；严重度：Major。** 当前“not reducible to weighted degree”只排除了一个简单 comparator，不等于排除 path participation/betweenness 类指标。该缺口会使审稿人把 $C_i$ 视为领域特定路径中心性的重新命名。

**可执行修改：** 对已有本地/已核验文献进行一次 search-bounded novelty audit，按节点类型、边语义、路径约束、删除定义、是否重算权重、选择器和证据审计逐项比较。若无法证明首创，贡献措辞应为 `instantiate and audit`，不写 `novel causal/counterfactual metric`。

### 4. 负结果论文的价值主线尚可更集中

**状态：Partial；严重度：Minor。** 贡献列表已把“不利消融与零权重校准”列为贡献【L49】；但结果和结论仍多次先说 Full “exceeded” 外部 baselines，再补长度不公平【L349, L430, L528, L568】。这容易使价值主线在“系统得分”与“负组件审计”之间摇摆。

**可执行修改：** 将 headline 统一为 `no-CF was the strongest graph condition; Full had higher equal-sentence but unequal-length overlap than two external baselines`。这不是改数据，只是消除叙事歧义。

## 第二轮通过条件

1. 保留最新的绝对句距/非顺序 edge 定义，并补全各 channel normalization 与退化情形。
2. 将新增命题准确称为固定图 functional identity，不作为效能理论。
3. 完成最接近路径中心性/删除影响方法的可核验 novelty audit，降低无法证实的优先权措辞。
4. 标题或副标题在检索层面显式出现 structural proxy / negative ablation / public technical-report proxy 之一。
5. 若不新增 title-concordant 数据，则继续将 maintenance value、expert semantic validity 和 CF benefit 标为未验证，不能在 cover letter 中升级。

## 第二轮最终评价

稿件的**内在逻辑和诚实度已明显改善**，理论恒等式也正确。尚未关闭的是“为何这一被当前结果否定的路径通道仍构成足以投稿的算法创新”。如果作者把论文明确定位为可审计的结构代理与负组件研究，并补全公式和最近方法定位，理论席位可在第三轮考虑从 Major 降为 Minor；若继续依赖原标题暗示因果、反事实和维护价值，则仍存在较高编辑拒稿风险。
