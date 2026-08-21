# MA-SQLGrid 第一轮独立审稿：算法理论、创新性与领域价值

## 审稿人定位

Text-to-SQL、可审计智能体系统、数据库安全执行与电力数据应用方向的领域审稿人。本报告重点检查“multi-agent”和“robust”的定义是否被实现与实验识别，及五角色架构、确定性裁决、多状态证据和电网应用之间的逻辑关系。

## 总体建议

**Major Revision（大修）**；信心 5/5。

稿件最强之处不是 Text-to-SQL 准确率，而是非常清楚地保存了执行安全边界、append-only trace、gold isolation、失败记录和结果的历史证据等级。该工程框架具有可复核价值。但是，当前五个“agent”主要是类型化软件职责：Analyst/Cartographer 是确定性 skeleton，Synthesizer 只封装外部历史候选，Validator/Critic 执行固定程序，Adjudicator 按固定分数和源顺序决策。已有 GridDB 与 BIRD 生成实验都不是五角色端到端运行；release-v3 又是对同一历史候选池、同一问题、已接触 gold-derived outcome 的描述性重执行。因此，现有证据不能识别多智能体贡献。与此同时，两个 adjudicating selector 在 130/180 问题上最高分并列，反序使 101/180 变为 117--118/180，完整 witness 只改变一个且语义有歧义的问题。这些结果直接限制“robust”标题的实证含义。

## 主要优点

1. **软件信任边界定义细致。** SQLite read-only URI、`query_only`、authorizer、禁用扩展、资源限制、失败保留与无隐藏重试形成多层执行控制；稿件也正确说明其不是身份认证、行级权限或进程隔离。【证据：`paper_applsci.tex` L201--L209】
2. **gold isolation 与证据等级诚实。** 参考结果在 board sealing 后才进入离线评价，并披露 frozen tests 曾访问同题 v2 gold-derived rows，因此 v3 被降级为 descriptive re-execution。【证据：L122--L132、L298--L312】
3. **不同实验不被错误合并。** GridDB factorial、component、multi-state、BIRD、retrospective replay 和 v3 的问题、可见性与结论上限被区分。【证据：L134--L190、L280--L310】
4. **不利诊断完整。** 130/180 高分并列、约 5.4 平均并列规模、178/180 原顺序选择来自 Qwen、reverse-order 大幅变化及 Q039 歧义均被保留。【证据：L511--L575】
5. **robustness 被拆成向量。** mutation safety、resource boundedness、evidence completeness、metamorphic invariance 和 semantic validity 被分开，且“not established”栏防止跨层升级。【证据：Table `tab:robustness`, L225--L244】

## 主要问题与可执行修改

### 1. “Multi-Agent” 当前更接近可替换的流水线角色，而非被验证的多智能体系统

**严重性：Major。** 五角色并未在现有主要实验中作为五个自主或交互生成体运行。Synthesizer 没有模型客户端，只封装外部候选；controller 顺序调用并做确定性选择。稿件已经承认 inherited GridDB/BIRD 不是 multi-agent execution。【证据：L38--L46、L192--L215、L627】

角色分解可以是软件架构贡献，但必须回答“agent”相对于 module/stage 的必要定义：自主性、局部状态、可替换策略、消息契约、允许的交互、停止条件和失败语义。目前只有职责和信息可见性，缺少正式状态机或组合语义。

**无需新数据可修复：**

- 在方法中给出 agent 定义，并坦率说明每个角色本次实例化为 deterministic、model-assisted 或 external-candidate wrapper。
- 给出黑板状态转移系统：状态、消息类型、前置条件、后置条件、不可变式、abstention 终态和 seal 操作。
- 将“five-agent benefit”从贡献中彻底移除，统一表述为“five-role agent-compatible architecture”或“typed multi-role coordination framework”。

**需要新实验：** 在相同模型、温度、候选数、物理调用和 token 预算下，对 single-call、staged single-candidate、multi-candidate validation、full state-aware coordination 做前瞻对照。没有该实验，multi-agent 只能是架构命名，不能是效能结论。

### 2. “Robust” 的标题含义与最关键的选择结果发生冲突

**严重性：Major。** 两个 adjudicating selectors 都在 130/180 问题上存在最高分并列；原顺序导致 178/180 选择 Qwen 槽位；反序将完整 witness 结果从 101/180 提高到 117--118/180。该 16--17 项变化说明决策对任意候选顺序高度敏感，而不是稳健。【证据：L511--L575】

稿件在正文中将 robustness 限定为向量，这是正确做法，但标题中的无修饰 “Robust” 容易被理解为整体语义或性能稳健性。

**无需新数据可修复：**

- 将标题最小调整为 “A Safety-Bounded and Auditable Multi-Agent Framework ...” 或增加副标题 “with Tested Read-Only Execution and Descriptive Selection Diagnostics”。
- 若坚持原标题，在摘要首句后立即定义：robust 仅指 mutation denial、bounded execution、complete evidence 和三 witness；同时明确“selection is not order robust”。
- 将 order sensitivity 提升为摘要的主要负结果，而不是只作为后半段数字。

**需要新实验：** 在 development-only 数据上冻结 order-independent tie policy（如 calibrated abstention、semantic margin、pairwise evidence），随后在 untouched questions 上测试风险—覆盖、顺序扰动和随机候选排列。不能从当前反序的较高 gold 分数选择规则。

### 3. 裁决评分缺少理论或经验依据，高并列率表明其信息量不足

**严重性：Major。** 默认评分为 safety 40、execution 40、shape 10、ordering 5、lexical value hits 5；正文说明这些是工程规则，并未证明先于同题 outcome-derived evidence。shape/value features 也不解释业务语义。【证据：L217--L225】

在所有 eligible candidates 都安全且可执行时，前 80 分可能相同；剩余低带宽特征不足以分离候选，这与 130/180 高并列直接一致。当前算法没有概率模型、效用函数、校准损失或最优性论证。

**无需新数据可修复：**

- 写出完整评分方程、各项取值域、缺失值处理、词汇命中计算和精确 tie semantics。
- 明确 40/40 并非统计学习权重，而是 eligibility evidence 的人为编码；解释为何安全/执行既作为资格门槛又获得分数，是否产生重复计算。
- 给出 score indistinguishability 分解：有多少问题在 eligibility、shape、ordering、value、witness 每一步仍并列。这可从现有 frozen ledgers 计算，但只作描述性诊断。
- 将稳定顺序称为 deterministic fallback，不称为 adjudication evidence。

**需要新实验：** 用开发集学习/选择 tie policy，在 sealed set 上评估；报告 calibration、selective risk、coverage、abstention、tie rate 和 order perturbation，而不仅是 accuracy。

### 4. 完整 witness 组件几乎没有可识别的语义增益

**严重性：Major。** validation-only 为 100/180，complete witnesses 为 101/180，只改变 Q039；该问题的“scheduled”与日期边界存在语义歧义，两条查询都可能不完整。M3 实际区分的是 `SELECT *` 与显式列投影。【证据：L531--L551】

因此，该组件当前支持“投影结构在 nullable extension 下有不同表现”，不支持 counterfactual reasoning、语义正确性或一般 robustness。三 witness 也不是部署状态的独立样本。

**无需新数据可修复：**

- 将 `Counterfactual Critic` 改称 `Metamorphic-State Critic`，至少在正文、算法和图中以此为科学描述；counterfactual 只作为历史模块名。
- 为 M1--M3 分别写出 metamorphic relation 的前提与保持量，明确 M3 不保持 wildcard projection 的 result schema。
- 将 Q039 定位为 construction-triggered projection trace，不再用 rescue 语言。

**需要新数据：** 预注册多 family 状态变换，并由数据库/电网专家验证哪些变换对每类问题保持语义；在新候选池上评估各 witness 的 incremental discrimination、false rejection 和 semantic rescue。

### 5. 架构创新与既有 Text-to-SQL/agentic 方法的差异尚未被充分证明

**严重性：Major。** Table `tab:literature-position` 覆盖 RGISQL、zero-shot、schema retrieval、DKA-SQL 等，但主要按“生成器 vs traced boundary”概括，尚未证明 append-only blackboard、deterministic adjudication、named-state gating 的组合相对最近 agentic Text-to-SQL 系统具有优先性。【证据：L56--L116】

**无需新数据可修复：**

- 建立功能级 novelty matrix：schema-grounding owner、candidate provenance、gold visibility、DB-enforced safety、failure retention、named-state completeness、deterministic tie handling、physical-call accounting。
- 明确创新类型是“可审计控制架构与证据契约”，而非新的语言模型、schema linker 或 SQL decoder。
- 避免用“其他工作关注生成”覆盖所有 agentic 系统；必须按现有核验文献逐项比较。

**需要额外文献核验：** 系统检索 multi-agent Text-to-SQL、execution-guided agents、blackboard coordination、metamorphic database testing。未核验优先权前，不使用 first/novel/unique。

### 6. 电网领域价值主要依赖小型 synthetic GridDB，标题外部效度不足

**严重性：Major。** GridDB 只有 1 个 DB、8 tables、98 rows、180 evaluation questions，evaluation partition development-visible；RTS-GMLC/SimBench/NERC 仅为 machine silver，0 human-reviewed、0 sealed；BIRD 是 non-grid。【证据：L134--L166、L621--L633】

现有结果能说明软件在一个合成 grid-shaped schema 和公共非电网数据上运行，不能说明真实电网数据库的语义、权限和工作流适用性。

**无需新数据可修复：** 将 domain contribution 限定为“power-grid-oriented case-study architecture”；避免“for Power Grid Databases”被写成部署验证。

**需要新数据：** 冻结至少一个 title-concordant 电网问题—SQL集，包含多个数据库/站点或 schema variants；由合格电网与数据库专家双盲复核 projection、units、time boundary、ordering、ties 和 result granularity；保留分歧和裁决记录。

### 7. 各实验的统计结论不能合并为框架效能，且没有框架级 primary estimand

**严重性：Major。** GridDB factorial、700-call component、25,920-row state study、BIRD 和 v3 使用不同候选、调用预算、可见性与 endpoint。稿件已说明不能合并，但文章结构仍围绕一个框架标题陈列大量互不等价结果。【证据：L280--L290、L582--L619】

**无需新数据可修复：** 在引言末给出一个 claim--evidence matrix，逐个 contribution 指向唯一实验和 estimand；将没有对应实验的“five-role benefit”明确标为 future hypothesis。

**需要新实验：** 预先定义框架级 primary endpoint，例如 call-matched strict execution accuracy 或 selective risk at fixed coverage，并指定 database/question cluster 为推断单位、multiplicity family 和 effect-size interval。

## 内在逻辑核查

- 从 executor adversarial tests 到“read-only mutation denial under stated assumptions”成立；到“safe/authorized for production”不成立，稿件已正确限制。
- 从 8-slot historical pool 的 selector 比较到“同一池内的 descriptive choice behavior”成立；到“multi-agent generation improves accuracy”不成立，稿件已承认。
- 从 M1--M3 invariance 到“passes registered metamorphic relations”成立；到“semantic correctness/robustness”不成立。
- 从 130/180 ties 和 reverse-order shift 到“evidence features discriminate poorly and tie fallback dominates”成立；该负结论应成为算法讨论中心。
- 从 BIRD 到“non-grid workflow portability”有限成立；到“power-grid external validity”不成立。

## 标题与贡献主张裁决

当前标题可保留为项目/框架名称，但**没有被当前实验充分证成**。最低限度应让标题或副标题出现 `auditable`, `safety-bounded` 或 `descriptive evaluation`。如果原标题完全不变，摘要和结论必须明确写出：

1. multi-agent 指 typed software roles，而非五个自主 LLM；
2. robust 不包括 semantic accuracy、candidate-order stability、production security 或 deployment validity；
3. 当前没有 end-to-end five-role superiority experiment。

建议核心贡献表述为：

> An auditable five-role coordination architecture with database-enforced read-only execution, append-only evidence traces, fail-closed named-state coverage, and a descriptive fixed-pool selection audit.

不建议表述为：

> A robust multi-agent system that improves Text-to-SQL accuracy in operational power-grid databases.

## 第一轮必须完成的修改清单

1. **P1/定义：** 给 agent、controller、blackboard、state critic、eligibility、robustness 写出形式定义与状态转移不变量。
2. **P1/标题与摘要：** 限定 multi-agent/robust；将 order sensitivity 和 high ties 提升为主结论。
3. **P1/理论：** 写出完整 adjudication 方程，解释双重 safety/execution gate 与 40/40 分数，明确所有 tie 与 abstention 语义。
4. **P1/现有数据分析：** 计算每个 evidence stage 的剩余 tie 数和分辨率；不新增 gold-driven 规则。
5. **P1/创新定位：** 用功能矩阵与已核验文献比较；不声称未核实的首创。
6. **P1/新实验：** 设计 call-matched、order-independent、untouched、expert-reviewed 的 title-concordant 前瞻实验；当前历史池不可转为确认性证据。

## 给作者的问题

1. 若每个角色可以是确定性函数，作者采用“agent”而不是“module”的最小判据是什么？
2. safety 和 execution 已经是 eligibility gate，为何又各贡献 40 分；该重复编码在所有 eligible candidates 上实际提供了多少区分度？
3. 如果遇到 130/180 unresolved top ties，为什么框架仍回答 180/180，而不是将“不确定”作为 robust behavior 的一部分？
4. 三个 witness 的构造家族如何对应实际电网 schema/value 演化，哪些保持关系将由领域专家确认？
5. 作者是否愿意把 `Counterfactual Critic` 的科学描述改为 `Metamorphic-State Critic`，以避免对反事实推理的过度承诺？
