# 两篇论文第三轮终审综合

## 最终建议

| 论文 | 终审建议 | 内部逻辑 | 投稿阻断核心 |
|---|---|---|---|
| C²GES | **Major Revision** | 技术与统计回归基本通过 | 原标题的 causal/counterfactual 与 maintenance 需要改标题或新增语义/外部数据 |
| MA-SQLGrid | **Major Revision，接近 Minor** | 协议、版本、统计家族和负结果已闭环 | 五角色效益、真实电网语义与仓库最终化仍未完成 |

两篇都不建议 Reject。它们现在最可信的共同贡献是：可审计软件/数据对象、严格证据分层、事故和负结果保留，以及对未支持主张的明确界定。

## 第三轮回归结果

- C²GES 已修正边方向、绝对句距、精确边权、$O(n^2)$ 构图复杂度及 unrenormalized no-CF scale coupling；未再发现实现描述与结果表的实质冲突。
- MA-SQLGrid 已补齐组件统计家族、交换性条件、有效10/5/5裁决解释、零弃权原因和候选顺序不稳定性；未再发现 v3/FINAL 或 prospective/descriptive 反转。
- 两篇 Abstract—Methods—Results—Discussion—Conclusions 的限制语句总体一致，没有在结论中恢复被正文否定的性能主张。
- 剩余冲突主要是**标题普通含义强于正文许可的证据上限**。

## 可由文字关闭

1. 修改标题或加入限定副标题，使其直接反映 proxy/architecture/evidence-audit 研究身份。
2. C²GES 把 Full 明确写成 registered but unsupported integration；MA 把 counterfactual keyword 改为 metamorphic。
3. 投稿信、Highlights、Graphical Abstract、README 与正文使用同一 claim ceiling。
4. 进一步明确 MA 的 within-run gold isolation 与 study-process outcome exposure 区别。

## 必须新数据或外部动作

1. **C²GES：** 维护语料外部集、专家角色/边/链条与危险遗漏评价；若主张比较优势，还需等词预算和对称调参新冻结实验。
2. **MA-SQLGrid：** call-matched 五角色端到端实验、合格电网 question–SQL gold、真实/外部数据库评价。
3. **两篇：** GitHub 仓库同步、许可证、不变 tag/archive、fresh-clone 与哈希复核。

## 最终投稿门槛

- 如果作者接受收窄标题/副标题和 architecture/audit/negative-results 定位，两篇可在完成仓库外部动作后进入投稿前 Minor 检查。
- 如果原标题必须完全不变，则上述新数据不属于“可选增强”，而是标题—证据闭环所需的 Major Revision 工作。
- 不得用 LLM 标注替代合格专家 gold，也不得通过删除负消融、失败调用、高并列或顺序敏感性来制造表面优势。

