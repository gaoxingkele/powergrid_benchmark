# 第一轮理论与创新性跨论文总结

## 总体裁决

两篇论文均建议 **Major Revision**，但原因不同：

- **C²GES** 有一个形式上清楚、严格可消融的新路径删除通道，但该通道的效能假设在当前开发和测试证据中均未获支持；最大风险是把结构代理称为 causal/counterfactual。
- **MA-SQLGrid** 有较强的工程执行与审计架构，但五角色效应从未被端到端识别；最大风险是把模块化软件职责称为已验证 multi-agent，并以 robust 覆盖一个明显顺序敏感的 selector。

两稿共同的优点是没有隐藏负结果、事故、可见性污染和外部效度边界。共同缺点是**标题的科学语义强于实验 estimand**。增加免责声明并不能完全代替标题、定义、公式与实验之间的一致性。

## 共同优先级

| 优先级 | C²GES | MA-SQLGrid | 是否需要新数据 |
|---|---|---|---|
| P1 | 将 causal/counterfactual 限定为 structural proxy / node-deletion sensitivity | 将 multi-agent/robust 限定为 typed roles 与 safety-bounded mechanisms | 否 |
| P1 | 补全 edge-weight 公式、设计公理与路径性质 | 补全状态转移、adjudication 方程、tie/abstention 语义 | 否 |
| P1 | 将负消融重构为核心发现，禁止组件增益暗示 | 将高并列与 order sensitivity 重构为核心发现 | 否 |
| P1 | 以最接近算法而非期刊内主题文献证明增量创新 | 以 agentic Text-to-SQL/blackboard/metamorphic testing 功能矩阵证明增量创新 | 需要文献核验，不一定需要实验数据 |
| P2 | 从冻结图日志报告 role/edge/path coverage | 从冻结 ledger 报告各证据阶段的 tie-resolution coverage | 可用已有资产重新分析 |
| P1 新实验 | 等词数、对称调参、新 holdout、专家语义评价 | call-matched、order-independent、新生成、专家语义评价 | 是 |

## 创新性对比

### C²GES

创新对象比较集中：角色约束路径集合、加权路径强度和节点删除损失。其数学对象有可检验恒等式，strict no-CF 也隔离了唯一通道。问题不在“没有算法”，而在算法效能为负/不确定，且 causal/counterfactual 命名超过其理论语义。论文可以作为“可审计结构算法及其负组件结果”成立。

### MA-SQLGrid

创新对象比较分散：角色 contracts、append-only blackboard、executor、state critic、deterministic adjudicator、多个 inherited experiment。当前最强创新是系统工程和证据契约，不是新的 Text-to-SQL 生成算法。五角色没有对应的 matched estimand，完整 witness 只改变一项，selector 被 tie fallback 主导。论文必须明确它首先是一篇 auditable architecture/evaluation-boundary paper。

## 理论基础对比

- C²GES 已有公式，但启发式设计理由不足。下一轮应关注定义完备性、性质与对照，而不是继续在已揭示 test 上调参。
- MA-SQLGrid 有大量操作性描述，但缺少统一的形式系统。下一轮应把 blackboard、eligibility、coverage、score、tie、abstention 和 seal 写成一个完整状态机/决策函数。

## 领域价值对比

- C²GES 使用真实公开 NERC 技术报告，但与维护工单仍有体裁与决策场景差距。
- MA-SQLGrid 使用合成 GridDB 表达电网结构，BIRD 仅证明非电网可运行，RTS-GMLC/SimBench 仍是未专家核验的 silver assets。

因此，两篇论文都需要 title-concordant、独立合格专家评价。LLM 可以帮助整理或预标注，但不能被写成独立电网专家裁决。

## 建议的三轮修改逻辑

1. **第一轮：概念和理论闭合。** 修正标题/术语强度，补公式、定义、状态机、设计性质，重写创新声明和 claim--evidence map；只使用现有证据。
2. **第二轮：现有资产再分析与统计审计。** C²GES 报告图覆盖/退化与长度关联；MA-SQLGrid 报告逐层 tie resolution、风险—覆盖和顺序敏感性。所有新增分析保持 descriptive，不能追认 confirmatory status。
3. **第三轮：面向投稿的独立复审。** 核查每个摘要/标题/结论主张是否有唯一证据源；如果未完成新 holdout 和专家标注，则保持代理语料、描述性选择、无组件增益和无部署验证的明确限制。

## 禁止采用的“美化”策略

- 不得在已揭示 C²GES test 上继续寻找正 CF 权重并替换冻结结果。
- 不得因 MA-SQLGrid reverse-order gold 分数更高而改用反序规则。
- 不得把机制被执行、软件测试通过、结果可复算写成语义有效或部署稳健。
- 不得把 NERC proxy、synthetic GridDB、non-grid BIRD 或 machine-silver 数据改称 title-concordant expert validation。
- 不得以新增免责声明代替算法定义和实验识别。

## 本审稿席位的第一轮通过条件

进入第二轮前，至少应满足：

1. 两稿标题或紧邻标题的限定语与实际 estimand 一致；
2. C²GES 完整定义 edge weight 和路径设计性质；
3. MA-SQLGrid 完整定义 agent/state/adjudication/tie/abstention；
4. 两稿贡献列表不再暗示当前证据未识别的组件、multi-agent 或领域效能；
5. 现有不利结果在摘要、结果、讨论和结论中保持一致，且未被选择性替换。
