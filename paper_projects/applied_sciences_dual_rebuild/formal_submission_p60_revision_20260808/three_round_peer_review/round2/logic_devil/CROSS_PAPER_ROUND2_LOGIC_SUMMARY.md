# 第二轮跨论文逻辑复审综合

## 总体判断

第一轮修改有效关闭了大多数“可通过正文修复”的问题，但没有关闭两篇都需要新证据才能解决的标题级缺口。

| 论文 | 真正关闭 | 仍为 Partial/Open | 第二轮最高风险 |
|---|---|---|---|
| C²GES | 描述性证据等级、composition interval 解释、调参不对称披露、表格引用、路径算术；最新方法已按冻结代码明确绝对句距、非文档顺序和精确边权 | causal/counterfactual 语义与增量、维护外部效度、组件保留逻辑、专家语义验证；Related Work 的“narrative order”尚未同步 | 标题仍把固定图路径记账恒等式提升为 causal/counterfactual 方法身份，且边方向描述有跨章节漂移 |
| MA-SQLGrid | 版本矩阵、170配对分母、v3 descriptive caption、六图、协议主表、权重降格 | 五角色效益、顺序/并列稳定性、电网语义有效性、标题中的 robust/multi-agent 强度 | 论文测试了软件合规和历史池行为，但未测试标题所暗示的端到端五角色效果 |

## 第一轮修改有没有“只用免责声明掩盖问题”

- **C²GES：仍有。** 新增命题只证明固定文本图的代数恒等式，不能为 causal/counterfactual 提供语义基础；标题问题仍依赖“aspirational”和“must be read together with boundaries”。
- **MA-SQLGrid：部分摆脱。** master protocol、version matrix 和 Results 首段实质改变了证据组织，不只是免责声明。但标题仍依赖“framework identity”，而端到端效益和真实电网语义仍无数据。

## 第二轮必须优先处理的事项

1. **C²GES：** 不得把 accounting identity 宣称为已补足算法理论；明确 Full 是未获增量支持的候选机制。将 Related Work 的“monotone narrative order”同步为“role-stage progression independent of document chronology”。标题不变时，需要新语义标注与维护外部集。
2. **MA-SQLGrid：** 保持 v3 descriptive；不要把 80/100/101 包装成 multi-agent gain。保留标题时，需要 matched-call end-to-end 实验和合格电网 gold。
3. **两篇共同：** 投稿信、Highlights、Graphical Abstract 和仓库 README 必须沿用正文证据边界，不能在外围材料恢复“outperforms”“validated causal”“robust multi-agent superiority”等措辞。
4. **第三轮复审门槛：** 若不新增实验，第三轮只能验证主张进一步收窄、标题/副标题调整和跨材料一致性；不能将待新数据事项机械标为 closed。

## 第二轮结论

- C²GES：仍有一个标题级 Critical residual 和三个 Major open issues。
- MA-SQLGrid：无新增致命数据矛盾；原 Critical 因主张降格可下调为 Major residual，但端到端效益与电网语义验证仍未关闭。
- 两稿都较第一轮更诚实、更可审计，但“可审计”尚不能替代标题所承诺的科学对象验证。
