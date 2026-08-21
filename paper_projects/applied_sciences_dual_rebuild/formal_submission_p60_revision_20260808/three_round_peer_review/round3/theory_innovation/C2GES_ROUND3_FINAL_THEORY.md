# C²GES 第三轮理论与创新终审

## 最终建议

**理论内部一致性：通过。创新充分性：有条件通过。投稿建议：Minor Revision if title/positioning is revised; otherwise Major Revision remains.**

最新稿已经形成一个内部成立的窄叙事：C²GES 是确定性的 typed-role textual proxy graph；$C_i$ 是固定图上的 qualified-path participation/deletion accounting functional；Full--no-CF 是冻结的未重归一化系数置零对比，含与 redundancy penalty 的相对尺度耦合；该通道被执行但没有显示 ROUGE 增益。若论文仅主张“实例化、审计并报告这一结构功能及其负消融”，理论链条成立。它不能被升级为因果识别、反事实推断、有效摘要组件或维护工作流验证。

## 终审核验

### 1. 功能恒等式与边构造

**状态：Closed。**

边权已按冻结代码完整定义：绝对句距衰减、token-set Jaccard 和最小角色置信度的加权和，保留 12 位小数，并给出 $w_{ij}\in[0,1]$；边方向来自 role-stage transition，而非文档先后顺序【最新 TeX L183--L191】。复杂度也已纠正为实现实际执行的 $O(n^2)$ ordered-pair scan，而约 $24n$ 只约束通过距离门的局部 ordered pairs【L249】。

在固定 qualified-path set、非负边权且删除不重算 surviving path weights 的前提下，

\[
C_i=U(G)-U(G_{-i})=\sum_{p\ni i}\operatorname{strength}(p)
\]

及非负性、nullity、path-additivity 均正确【L201--L227】。稿件也准确说明这是 accounting identity，而非 causal-identification theorem 或 efficacy guarantee【L212】。

**残余 Minor：** $Q_i,R_i,G_i,C_i,P_i$ 的 report-level normalization、全零退化和 tolerance 仍可用一张符号表统一呈现；这不推翻当前理论叙事。

### 2. 路径参与功能的创新定位

**状态：Closed for claim restraint; Open for priority verification。**

贡献已经收缩为 `instantiate and audit a typed qualified-path participation functional`，并明确“不主张优先于所有 path-centrality measures”【L49】。这一措辞与现有文献证据相容，也避免把“不等于 weighted degree”误写成“首次路径中心性”。因此，**当前克制的创新叙事内部成立**。

但是，Related Work 仍只在 selected Applied Sciences studies 中断言未见相同组合【L89--L103】，没有完成 path participation、betweenness-like centrality、node-deletion influence 和 discourse graph 的 search-bounded novelty audit。故稿件只能声称领域特定、可审计的组合实例，不能声称首创或普遍新的图理论。

### 3. 负消融与组件可识别性

**状态：Closed, with one terminology cleanup required。**

最新方法正确承认：将 $C_i$ 从 0.15 置零后，positive-channel scale 从 1.00 降至 0.85，而 redundancy coefficient 保持 0.50；相对 penalty 变为 0.5882。因此该对比估计的是**冻结未重归一化评分规则下的 coefficient removal，包括 scale coupling**，不是纯信息通道隔离【L241--L245, L269】。这比前两轮的“strict single-channel ablation”表述理论上更准确。

负结果也保持一致：Full 在两个预算均低约 0.0033，区间跨零；开发校准 12/12 选择零权重；score/sequence changes 只证明通道 active，不证明 beneficial【L430--L472, L514--L534, L574】。

**残余 Minor：** 摘要、引言、Related Work、图注和多处结果仍使用 `strict no-CF` 或 `strict channel ablation`【L19, L45, L89, L195, L263, L290, L353, L430 等】。这与已经承认的 scale coupling 不完全一致。应统一改为 `registered unrenormalized coefficient-zero no-CF rule`；这是文字修复，不需要新数据。

### 4. 标题和因果/反事实边界

**状态：Partial；仍是主要投稿风险。**

摘要、featured application、Introduction、Discussion 和 Conclusion 均明确：图是 textual proxy，counterfactual 仅指 fixed-graph node deletion，NERC 是 maintenance proxy，真实维护有效性未测试【L19--L21, L39--L51, L532--L576】。因此正文没有把当前结果伪装成物理因果或部署有效性。

但原标题仍把 `Causal and Counterfactual` 与 `for Power Grid Maintenance Reports` 放在检索层首位，而当前通道没有效能增益、语料也不是维护工单。正文免责声明不能完全改变标题的读者预期。

## 现有证据下可以成立的最终贡献

1. 一个完全确定、源链接的 typed-role proxy graph summarizer。
2. 一个有精确定义、可测试恒等式的 qualified-path participation functional。
3. 对该功能执行情况、scale-coupled coefficient removal、长度不公平和负效能结果的可审计评估。
4. 一个 NERC public technical-report proxy 的泄漏、权利、冻结和重现链。

## 现有证据下不能成立的主张

- causal effect、SCM 或真实 counterfactual inference；
- $C_i$ 改善摘要质量或 ROUGE；
- 长度控制后的系统优越性；
- maintenance-report utility、safety 或专家有效性；
- 相对所有 path-centrality 方法的优先权。

## 只能通过特定外部动作关闭的项目

### 只能通过改标题关闭

- 检索层面的 causal/counterfactual 与 maintenance promise 过强。最低变化方案是增加 `Structural-Proxy and Negative-Ablation Study` 副标题；若标题完全不变，该风险保持开放。

### 只能通过文献检索关闭

- 相对 path participation、node-deletion influence、betweenness-like 和 discourse-graph summarization 的创新优先权。必须使用可核验来源完成 search-bounded comparison；未完成前维持 `instantiate and audit`。

### 只能通过新实验/新数据关闭

- $C_i$ 的正效能：需要新 sealed holdout 和预注册重设计，不能继续调已揭示测试集。
- 公平系统比较：需要 equal-word/token budgets 和对称调参机会。
- 维护价值与语义正确性：需要 title-concordant 数据、合格电网专家独立标注、adjudication 前 agreement、unsafe omission 和 practical utility endpoints。

## 最终裁决

从理论正确性看，稿件已经可以作为**结构代理功能的可审计负结果研究**成立；不存在必须推翻当前公式或冻结结果的理论错误。从创新与标题匹配看，仍不能作为“已验证的因果/反事实维护摘要方法”投稿。若完成 strict/no-CF 术语清理、补 channel normalization 表、维持克制 novelty 措辞，并调整标题或副标题，本席位建议 **Minor Revision**；若原标题完全不作限定，则维持 **Major Revision**。
