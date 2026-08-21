# C²GES 第二轮独立逻辑复审

## 复审结论

第一轮的统计措辞、交叉引用、调参不对称披露和有限总体解释已经明显改善；但是标题级核心问题没有被新证据关闭。修订稿证明了路径删除分数的一个固定图记账恒等式，却仍未证明该量具有因果/反事实语义或增量效果。第二轮判定：**核心标题问题 Partial，仍是 Critical residual；维护场景与专家语义验证 Open。**

## 第一轮问题关闭矩阵

| Round-1项 | 状态 | 当前严重度 | 第二轮核验与精确锚点 | 仍需修复 |
|---|---|---|---|---|
| C1 causal/counterfactual 标题身份缺乏理论和实证支持 | **PARTIAL** | **CRITICAL residual** | 修订稿新增固定路径集下的 non-negativity/nullity/additivity 命题，并明确其为“accounting identity”，见 Materials and Methods, “Typed Path-Deletion Structural Perturbation”, lines 197–210, Equations (1)–(2)。这关闭了数学定义不清，却没有为 causal/counterfactual 命名提供语义依据；Results RQ2 lines 518–522 与 Conclusions lines 566–572 仍显示 no-CF 更优、零权重校准获胜。Title line 12 保持不变。 | 必须在“降格命名/标题”与“新增同义证据”之间作实质选择。保留标题则需要独立角色/边/链条语义标注、非因果高阶中心性对照和全新封存集的机制验证。免责声明与恒等式不能单独关闭。 |
| M1 maintenance 标题与 NERC proxy 样本错配 | **OPEN** | **MAJOR** | Abstract line 19 仍称 maintenance 为 aspirational；Introduction lines 39–43、Discussion lines 544–548、Conclusions line 566 均确认没有工单或巡检记录。No title-concordant maintenance evaluation exists. | 补全新维护报告/工单外部集和合格用户评价；否则标题中加入 proxy-corpus 限定，并把 “for maintenance reports” 明确降为 future application。 |
| M2 与 Semantic-MMR/TextRank 的长度和调参不公平 | **PARTIAL** | **MINOR residual；若声称 superiority 则 MAJOR** | RQ1 已改成 equal-sentence descriptive comparison（Introduction line 37）；新增 `tab:tuning-opportunity` lines 267–280；Results lines 418–420 和 composition-interval caption 明确长度与调参限制。Abstract line 19、RQ1 answer line 516、Conclusions line 568 仍以 “exceeded” 作为结果主句，但紧接不构成 length-controlled superiority。 | 当前作为描述值可以保留。若摘要或投稿信使用“outperforms/superior”，则必须补等词预算、版面感知切分和对称调参实验。建议把摘要主句改为“had higher unadjusted equal-sentence means”。 |
| M3 开发证据不利时仍保留正 CF 权重，缺少预设保留规则 | **OPEN** | **MAJOR** | Development Selection line 259 仍报告所选 Full 比 no-CF 低 0.0056652；post-unblinding calibration lines 508–512 仍是 12/12 折选零权重。新增理论命题没有解释为什么开发阶段应保留 0.15。No preregistered component-retention criterion is shown. | 展示原始冻结协议中保留该通道的事前决策规则；若不存在，把 Full 明确定位为“被检验且未获支持的预注册候选”，并停止把 Full 当作推荐配置。 |
| M4 词汇标签—预设转移—因果链的语义循环 | **OPEN** | **MAJOR** | `tab:taxonomy` 与 Methods lines 160–187 仍由词典和注册转移自行定义链；Known Linguistic Failure Modes lines 249–255 明确无专家 gold。新增命题只证明固定文本图上的代数性质，不验证角色或边。 | 双人独立标注 extraction unit、role、directed edge、chain coverage 与 unsafe omission；报告裁决前一致性，并与不使用 cause/event 命名的结构基线比较。 |
| M5 corrective/已检查总体却承担确认性算法结论 | **CLOSED（按描述性论文口径）** | — | Methods lines 112–118、286 onward、Results composition interval、Discussion lines 528–530 和 Limitations lines 552–556 已一致称为 corrective finite-set/descriptive，并明确 report dependence 未审计。 | 维持该措辞；投稿信不得重新称 confirmatory validation。新确认性结论只能来自新封存集。 |
| m1 `Table~1` 硬编码 | **CLOSED** | — | line 251 已改为 `Table~\ref{tab:taxonomy}`。 | 无。 |
| m2 摘要以限制为主、正贡献焦点弱 | **PARTIAL** | **MINOR** | 摘要证据边界准确，但核心正贡献仍主要是 framework description；负消融占据主要结果空间。 | 将正贡献限定为 audited dataset/traceability/negative component test，不要用更强机制效益填补篇幅。 |

## 修改引入或暴露的新问题

### N1 — “理论基础已补足”的表述强于实际内容

- **状态：OPEN；严重度：MAJOR。**
- **锚点：** Materials and Methods lines 208–210；Equation (2) 已直接写出 $C_i=\sum_{p\ni i}\operatorname{strength}(p)$。
- **问题：** 新增命题基本重述 Equation (2) 在“删除不改变剩余路径权重和路径资格”假设下的代数结果。它说明实现一致性，却没有解释为何路径长度 2–4、12句窗口、阶段跨度除以4、几何均值或角色顺序是适合摘要质量的理论选择。若回复信称“novelty/theoretical foundation accepted and closed”，会把记账性质夸大为算法理论。
- **修复：** 将其命名为 Lemma/implementation invariant，而非理论创新；另给出每个设计量的任务假设、可证推论或独立消融。没有新增证据时，创新点应落在 auditability 和 falsifiable structural diagnostic。

### N2 — 标题保留理由仍是“连续性”，不是科学证据

- **状态：OPEN；严重度：MAJOR。**
- **锚点：** Introduction line 39 onward；Conclusions line 566：“title's maintenance setting remains the intended application direction”；Discussion line 534：“The title must therefore be read together with these boundaries.”
- **问题：** 读者不应依赖正文限定来纠正标题的普通含义。标题的可识别性/连续性不是维持科学术语的证据。
- **修复：** 在投稿前由作者作标题裁决；若业务上必须保留原标题，应在副标题加入“Structural Proxy Study on Public NERC Reports”。

### N3 — 最新边构造修正后出现跨章节“叙事顺序”漂移

- **状态：OPEN；严重度：MAJOR。**
- **锚点：** Related Work line 75 称边“encode a monotone narrative order”；最新 Materials and Methods lines 183–191 则以 $d_{ij}=|\operatorname{pos}(i)-\operatorname{pos}(j)|$ 明确边不要求 source-role sentence 在文档中更早，方向只来自角色转移；同处给出精确边权 $w_{ij}=\operatorname{round}_{12}[0.45e^{-d_{ij}/5}+0.30J_{ij}+0.25\min(r_i,r_j)]$。
- **问题：** 最新方法描述与冻结代码一致，关闭了早先“强制文档前向”的错误；但 Related Work 的“monotone narrative order”仍容易被读成时间/文档顺序。实际是 role-stage monotonicity，且边可逆着文档 chronology。这一差异直接影响对 causal chain 的解释，不是纯措辞问题。
- **修复：** 将 line 75 改为“monotone registered role-stage progression independent of document chronology”；同步核对 Figure `fig:algorithm`、caption、Supplement 和代码 README 是否仍画成/写成前向文档边。把“source order”只用于最终输出恢复，不用于边方向。

## 第二轮可投稿性判断

稿件已从“潜在过度声称的算法性能论文”改善为透明的纠正性机制研究，但在原标题下仍存在编辑初筛风险。若不补新实验，最可辩护的投稿身份是 **audited proxy-benchmark and negative component study**，不是 causal/counterfactual effectiveness study。C1、M1、M3、M4 以及最新出现的 N3 未关闭前，不建议把它标记为无重大逻辑障碍。
