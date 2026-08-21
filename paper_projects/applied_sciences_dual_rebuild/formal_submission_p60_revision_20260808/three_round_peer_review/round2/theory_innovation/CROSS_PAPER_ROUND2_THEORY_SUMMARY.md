# 第二轮理论与创新性跨论文总结

## 总体判断

两稿第一轮修改均显著提高了证据边界、统计解释与内部一致性，但理论/创新席位仍建议 **Major Revision**。共同原因不是继续过度解释结果，而是：**被诚实披露为未验证的对象，恰好仍是原标题最核心的价值承诺。**

- C²GES：因果/反事实已在正文降为结构代理，但标题仍突出这两个术语；路径通道在开发和测试均无增益证据。
- MA-SQLGrid：multi-agent/robust 已在正文限定为 typed roles 和 bounded mechanisms，但没有 end-to-end five-role effect；selector 对候选顺序明显不稳健。

## 状态汇总

| 维度 | C²GES | MA-SQLGrid |
|---|---|---|
| 证据边界 | **Closed**：proxy、descriptive、长度与专家限制清楚 | **Closed**：各协议、可见性、版本和 claim ceiling 清楚 |
| 理论正确性 | **Partial**：固定图删除恒等式与最新边权公式正确；channel normalization 尚未统一形式化，且恒等式非效能理论 | **Partial**：invariants 正确；gate/score 未化简，缺完整决策函数 |
| 核心术语 | **Partial**：正文合格，标题仍有 causal/counterfactual 过度预期 | **Partial**：摘要限定 robust，但标题与 order sensitivity 冲突；agent 定义较弱 |
| 创新定位 | **Open**：缺 path-centrality/node-deletion 最接近比较 | **Open**：缺 agentic SQL/blackboard/metamorphic control 功能级比较 |
| 核心组件价值 | **Open as positive value**：CF channel 当前为负/不确定 | **Open**：five-role effect 未测试，complete witness 只改变 Q039 |
| 电网应用价值 | **Open**：NERC proxy 非维护工单，无专家质量结论 | **Open**：synthetic GridDB + machine silver，BIRD 非电网 |

## 已真正关闭的问题

1. C²GES toy arithmetic 已可复核，RQ1 已改为 equal-sentence descriptive comparison，调参与长度不公平已前置，负消融未被美化。
2. MA-SQLGrid 已明确 RQ1 是 conformance 而非 efficacy，master protocol table 和 version matrix 阻止跨实验拼接，Q039 已降为 constructed projection trace。
3. 两稿均未把 LLM 标注冒充 qualified expert gold，也未用 post hoc 较高结果替换冻结结果。

## 投稿前最重要的文字/理论修复

### C²GES

1. 保留与冻结代码一致的绝对句距、非文档顺序约束和精确 edge-weight 公式；补齐各 channel normalization 与退化情形。
2. 把 proposition 称为 fixed-graph accounting identity/function properties，不称 performance guarantee。
3. 对 path centrality/node deletion/discourse graph 做 search-bounded novelty audit。
4. 标题或副标题显式加入 structural proxy / negative ablation / public technical-report proxy。

### MA-SQLGrid

1. 把 safe/executable 作为 hard gate，从 score 中移除恒定 80 分，写出完整 piecewise adjudication function。
2. 在 robustness vector 中加入 candidate-order stability，并明确当前 descriptive evidence 不支持它。
3. 将 Counterfactual Critic 科学表述改为 Metamorphic-State Critic。
4. 对 agentic Text-to-SQL、blackboard architecture 和 metamorphic DB testing 做功能级 novelty audit。

## 需要新数据才能关闭的问题

- C²GES：全新 holdout、等词数/对称调参比较、专家 role/edge/path 与 maintenance utility 评价。
- MA-SQLGrid：call/candidate/token-matched five-role 对照、development-frozen tie/abstention policy、untouched multi-schema grid benchmark 与双领域专家评价。

## 编辑拒稿风险排序

1. **MA-SQLGrid：标题核心 five-role efficacy 没有对应实验。** 这是最高风险。
2. **C²GES：标题核心 CF channel 没有正效能，且数学对象不是因果反事实。**
3. **两稿：创新优先权相对最接近方法尚未充分核验。**
4. **两稿：真实 title-concordant 电网任务和专家语义价值未验证。**

## 第三轮理论席位的判定规则

第三轮不要求把缺少的新实验虚构为已完成。若作者在投稿前不执行新实验，则至少必须：

- 让标题、摘要、贡献和 cover letter 与 architecture/proxy/negative-result 的较窄证据完全一致；
- 补齐形式定义；
- 完成可核验的最接近方法比较；
- 保留所有负结果和外部效度限制。

满足这些条件可考虑将理论/创新意见降为 Minor Revision；若标题继续传递未被实验识别的 causal/counterfactual 或 robust multi-agent efficacy，则维持 Major Revision。
