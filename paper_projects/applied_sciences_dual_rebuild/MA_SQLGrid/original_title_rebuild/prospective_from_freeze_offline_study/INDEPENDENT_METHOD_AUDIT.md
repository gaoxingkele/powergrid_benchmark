# MA-SQLGrid R2 离线协调研究独立方法审计

## Material Passport

- **审计对象**：`ma_sqlgrid_agents.py`、`sqlite_readonly_executor.py`、`offline_coordination_study.py`、`tests/`、冻结件及 `run_a`/`run_b` 全部账本。
- **审计日期**：2026-08-08（Asia/Shanghai）。
- **访问级别**：本地原始代码与逐条 JSON/JSONL 结果，只读审计；未修改代码、冻结件或实验结果。
- **验证状态**：**ANALYZED**。重新执行了 20 个单元测试（20/20 通过），独立读取并重算了全部摘要；因本任务明确要求只读，未创建第三个完整实验运行，故不标记为 `VERIFIED`。
- **证据边界**：结论仅适用于冻结哈希 `4381f0301ff9b1383723ca412883e736400e58bb94737c8ae0f56e0f13f2112b` 对应的 180 题离线候选选择研究。它不是新模型生成实验，也不能估计自主多智能体生成收益。

## 总体判定

**FAIL（针对“严格金标准盲法、三个独立反事实状态、完整五角色协作获得增益”这一强方法主张）。**

冻结输入、候选顺序、只读执行器、失败保留、摘要重算和 A/B 决策输出重现均通过审计；但是有四项会改变论文解释的关键问题：

1. 金标准文件在所有黑板封存前已被读取：冻结阶段会解析包含 `gold_sql` 的完整 JSONL，`run()` 开始时的冻结校验又会读取该文件的全部字节计算 SHA-256。因此“金标准文件仅在全部黑板封存后才打开”不成立；成立的较窄表述是“金标准字段未进入选择视图，且金标准 JSON 仅在封存后被解析用于评分”。
2. 三个注册的 T1 文件具有完全相同的 SHA-256 `6f1919...14e39a`，逐表关系内容和无 `ORDER BY` 的返回顺序也相同。所谓“三个状态全覆盖”实际只有一个唯一 T1 数据库镜像的三次重复。
3. `full_coordination_complete_invariance` 与 `validation_only_no_cf` 在 180/180 题上选择完全相同，均为 100/180（55.56%）。本研究没有观察到反事实/不变性模块的增量选择或准确率收益。
4. 研究黑板记录了多个角色，但并非完整五角色端到端协作：候选 SQL 来自既有冻结池，不是本次 SQL 生成智能体生成；`SchemaCartographer` 的 grounding 只写入黑板，未进入验证或裁决；因此不能把结果归因于完整五角色框架。

在修正论文主张后，本研究仍可作为**冻结候选池上的、可审计的离线确定性选择研究**进入正文。

## 逐项审计

| 审计项 | 判定 | 证据与解释 |
|---|---:|---|
| 冻结先于金标准评分 | **PASS** | `study_config.json`/冻结件先于 `run_a` 结果生成；代码在写入 180 个 sealed blackboard、主选择账本和 pre-gold seal manifest 后，才构造 `gold_records` 并评分（`offline_coordination_study.py:313--326`）。冻结清单同时固定了代码、配置、问题、候选账本和状态文件哈希。文件系统时间只能证明当前本地工件顺序，不是外部可信时间戳。 |
| “金标准文件只在封存后打开” | **FAIL** | `selection_view_from_gold()` 在冻结阶段用 `load_jsonl()` 解析整个 `questions_with_gold` 文件（`:96--112`）；`verify_freeze()` 也会在选择前对该文件逐字节计算 SHA-256。`:325` 的注释仅是 `run()` 中第一次**解析用于评分**，不是第一次打开/读取金标准文件。 |
| 金标准字段不进入选择 | **PASS（数据流限定）** | `selection_inputs.jsonl` 恰有 180 行、180 个唯一 ID，字段集合仅 `{question_id, question}`，顺序与 `splits.json` 的 test 顺序完全一致；预金标准账本与黑板不含 `gold_sql`、`answer_shape`、`order_sensitive` 等禁止字段。静态数据流未发现金 SQL/正确性进入选择函数。该结论不等同于操作人员盲法，也不能由本地文件自证研究者此前从未看过标签。 |
| 180 题、8 槽、候选池与顺序 | **PASS** | Qwen 与 Granite 账本各 720 条且键 `(question_id, condition)` 唯一，全部状态为 `success`；每题严格 8 槽，顺序与配置一致：Qwen 的 F00/F01/F10/F11，随后 Granite 的 F00/F01/F10/F11。总槽位 1,440；实际只有 953 个唯一 SQL 哈希，且每题唯一 SQL 数分布为：1/2/3/4/5/6/7/8 个分别有 7/19/15/18/27/23/45/26 题。重复槽位被原样保留。 |
| T0 + 三个 T1 的等价判断不使用金标准 | **PASS（reference-free）** | 选择阶段仅把同一候选在 T0 与 T1 的结果进行比较；没有用 gold SQL 或 gold 输出。`result_equivalent()` 对有 `ORDER BY` 的候选按序比较，否则按多重行集合比较。 |
| 三个独立 T1 状态与 complete coverage | **FAIL** | 三个 T1 文件字节级 SHA-256 完全相同，且状态清单也记录相同哈希；独立逐表检查显示三个 T1 以及 T0 的关系内容相同，默认返回顺序也相同。`coverage_complete=True` 只表示三个名称均出现，不表示三个独立扰动。1,440 个候选的 CF 结果仅有 `3/3`（1,357 个）或 `0/3`（83 个），阈值 1/2/3 的结果因此完全相同。可报告为“一个唯一插入排列镜像的三次重复检查”，不可报告为“三个独立反事实状态”。 |
| CF complete-coverage fail-closed 实现 | **PASS（实现层）** | `CounterfactualCritic` 检查状态 ID 集合严格等于 expected set；`Adjudicator` 要求 coverage complete、状态数等于注册值且达到阈值，否则不合格/弃权。缺失覆盖、未知状态和全体不合格均有单元测试。数据设计的状态重复不否定 fail-closed 代码，但削弱其经验含义。 |
| SQLite 只读安全边界 | **PASS** | 执行器实际构造 `file:...?mode=ro&immutable=1` URI，启用并读取确认 `PRAGMA query_only=ON`，禁用扩展，安装 deny-by-default authorizer，并设置 opcode/time progress handler及 `max_rows+1` 行截断。20 个测试全部通过，其中覆盖 INSERT/UPDATE/DELETE/DDL/ATTACH/PRAGMA/多语句、危险函数、元数据、表列白名单、递归资源上限、行上限和数据库哈希不变。全部 5,760 次候选执行及 180 次 gold 执行的 trace 均记录 `query_only=true`、`read_only_uri=true` 和注册资源上限。`read_only_uri` 字段本身是实现常量，安全结论主要来自 URI 代码、SQLite 行为及负向测试，而不是该布尔字段单独自证。 |
| 所有尝试与失败留存 | **PASS（可审计性有保留）** | 每次运行有 5,760 = 180×8×4 条候选执行记录，其中 332 条失败（83 个失败候选×4 状态），失败种类均为 `sqlite_error`；另有 180 条 gold 执行且全部成功。代码无自动重试，运行目录拒绝覆盖。缺点是 execution trace 未显式写入 question ID、candidate ID 和 state name；T1 文件哈希又相同，三次 T1 尝试只能依赖固定循环顺序追溯，建议后续版本补充身份字段。 |
| run A/B 重现性 | **PASS** | 黑板、封存清单、选择、评分、敏感性、摘要和 reproduction manifest 均字节相同；官方比较文件所列四个 canonical outputs 也全部相同。原始候选/gold execution trace 因 `elapsed_ms` 不同而非字节相同，去除该非确定性计时字段后逐条完全相同。这应表述为“规范化决策与评分输出一致”，不可声称“所有原始文件逐字节一致”。 |
| 摘要数字 | **PASS，见下节限定修正** | 独立从 `evaluation_ledger.jsonl` 重算，与 `summary.json` 完全一致。 |
| first/validation/full 等候选预算 | **FAIL（操作预算）；PASS（同源冻结池）** | 三种方法共享同一 8 槽历史候选池和候选顺序，但 `first_candidate` 只取 C000，不检查其余 7 槽；validation/full 在 8 槽中裁决并依赖执行证据。执行账本把 8 槽×4 状态一次性生成后共享，所以没有记录每个方法独立的实际延迟/执行开销。可比较“固定池上的选择结果”，不可称为“等推理/等执行预算的端到端系统比较”。 |
| validation-only 是否真不使用 CF | **FAIL（代码语义），本数据数值无影响** | `validation_only_no_cf` 把完整 `counterfactuals` 传给 `Adjudicator.decide()`；即使 `require_counterfactual=False`，其 tie-break key 仍包含 CF pass rate 和状态数（`ma_sqlgrid_agents.py:430--438`）。独立按 validation score+原顺序重算时，180 题选择恰与现输出相同，因此本次数字无需更改，但方法实现/名称应修正，或显式传空 CF。 |
| full 是否真正使用五角色 | **FAIL** | 每题黑板有 22 条消息，角色标签包括 Query Analyst、Schema Cartographer、Frozen Candidate Provider、Validator、Counterfactual Critic、Adjudicator。可是候选由历史账本直接注入；本研究没有调用 `SQLSynthesizer`/LLM。grounding 的返回值只被记录，后续未引用。故只有 query intent→validation、execution validation、CF check、adjudication 对选择有因果数据流。 |
| 敏感性是否预注册且非 post-hoc | **PASS（工件顺序），解释需严格限定** | 三套权重、三个阈值和两个 tie rule 已写入冻结配置并哈希；3,240 条敏感性选择在 gold 评分前写入。它们仍是在同一 180 题 test set 上评分的 test-visible sensitivity，不是独立验证集。不得依据评分后观察到的 65.00%/65.56% 反向选择 tie rule，再把它称为主方法结果；只能完整报告全部 18 格或明确称探索性敏感性。外部时间戳/预注册库缺失，故无法从本地工件证明研究人员没有先验标签知识。 |

## 数值重算与必须修正的口径

### 主结果重算

| 方法 | Covered | Correct | Accuracy (all 180) | Robust-invariance 记录值 | 相对 first 的 rescue/harm |
|---|---:|---:|---:|---:|---:|
| first candidate | 180 | 80 | 44.44% | 179/180 | 0/0 |
| validation only（当前实现） | 180 | 100 | 55.56% | 180/180 | 22/2 |
| full coordination | 180 | 100 | 55.56% | 180/180 | 22/2 |

重算结论：

- full 相对 first 为 **+20/180 个正确答案，即 +11.11 个百分点**；配对变化为 22 个 rescue、2 个 harm。
- full 相对 validation-only 为 **0/180 个选择变化、0 个正确数变化、0.00 个百分点**。因此不能把 +11.11 个百分点归因于 CF/invariance 模块。
- 5,760 是物理执行尝试数，但只有 **2 个唯一数据库哈希**（T0 与一个唯一 T1）以及 **1,906 个唯一 `(SQL hash, database hash)` 组合**。将它写成“4 个独立数据库状态”或“3 个独立 T1 状态”会高估扰动强度。
- 1,440 个槽位不等于 1,440 个不同 SQL；共有 **953 个唯一 SQL 哈希**。
- 敏感性表中 reverse-order 的 117/180（65.00%）和 118/180（65.56%）均为冻结后的探索性敏感性结果，不应替代注册主结果 100/180。

审计另算的配对 exact McNemar 两侧 p 值为约 `3.59e-5`（22 对 2 个不一致方向），但该检验未见于冻结统计计划，故只能作为审计诊断，**不得在本轮直接升级为预注册验证性显著性结论**。

## 可进入正文的限定结论

以下表述与现有证据相容：

> 在一个预先冻结的 180 题 GridDB test split 上，我们对每题来自两个本地模型、四种既有生成条件的八个历史候选进行离线确定性选择。选择阶段仅接收问题文本、schema、候选 SQL 和 reference-free SQLite 执行证据；主选择账本在金 SQL 评分前封存。与固定取第一个候选相比，validation-based selector 将 execution accuracy 从 80/180（44.44%）提高到 100/180（55.56%），对应 22 个 rescue 和 2 个 harm。加入当前 complete-invariance gate 后，180 题的选择与准确率均未进一步变化。两次运行的规范化选择、评分和摘要输出完全一致。

必须同时披露：

> 本实验复用历史候选，不含新模型调用，不能估计多智能体生成收益；三个命名 T1 文件实际上是同一个唯一数据库镜像，因而不支持“三个独立反事实状态”的结论；schema grounding 未参与最终决策数据流；不同 selector 的有效执行成本不相等；金标准文件在冻结和哈希校验阶段已经被读取，但金标准字段未进入选择视图。

现有证据**不支持**以下表述：

- “完整五智能体协作使 accuracy 提升 11.11 个百分点”；
- “counterfactual critic 显著提高准确率或鲁棒性”；
- “通过三个独立反事实数据库状态验证”；
- “三种方法在相同端到端推理/执行预算下比较”；
- “65.56% 是注册主方法准确率”；
- “金标准文件在全部黑板封存前从未被打开或读取”。

## 11 类统计/方法谬误扫描（11/11 已检查）

| 类型 | 结果 |
|---|---|
| Simpson's paradox | **NOTE**：未分层报告模型/条件/问题难度，暂不能排除聚合掩盖异质性。 |
| Ecological fallacy | **PASS**：推断单位与题目级评分单位一致；不得外推到全部电网数据库。 |
| Berkson's paradox | **CAUTION**：研究仅覆盖两个模型×四条件均成功的冻结候选池，不代表所有生成失败情形。 |
| Collider bias | **NOTE**：未进行协变量控制；主要风险不是传统 collider，而是“候选可用”筛选边界。 |
| Base-rate neglect | **PASS**：指标为题目级 execution accuracy/coverage，不是诊断敏感度/特异度。 |
| Regression to the mean | **PASS**：无按极端基线选题后的前后比较。 |
| Survivorship bias | **CAUTION**：所有 1,440 槽位在该 test split 中均为 generation success；研究没有覆盖生成阶段失败的端到端风险。 |
| Look-elsewhere effect | **CAUTION**：18 格 sensitivity 若只突出最佳 65.56% 会形成选择性报告；必须完整报告。 |
| Garden of forking paths | **CAUTION**：本地冻结降低了本次运行内自由度，但缺少外部时间戳，且 tie rule 对结果影响大。 |
| Correlation != causation | **RED_FLAG（对强归因）**：full 与 validation-only 完全相同，不能把提升归因于 CF 或五角色协作。 |
| Reverse causality | **PASS/不适用**：无时间方向的观察性因果模型；主要限制是组件归因不足。 |

## 后续修复优先级（不属于本次代码修改）

1. **强制修复**：从不含 gold 字段的独立 question-only 文件生成 selection view；冻结校验也应将 gold 文件哈希校验放到 sealed boundary 之后，或使用由独立数据管理员提前发布的 digest。
2. **强制修复**：生成并验证三个内容/文件哈希均不同的查询盲扰动状态；coverage 应按唯一 state hash 计数并拒绝重复哈希。
3. **强制修复**：使 `validation_only_no_cf` 不接收 CF 对象；明确记录 full 与该干净基线的选择差异。
4. **强制修复（若维持五角色主张）**：让 schema grounding 进入候选约束或评分，并执行真实 SQL generation role；否则把研究名称降格为“offline deterministic candidate coordination”。
5. **建议修复**：在每条 execution trace 写入 `question_id`、`candidate_id`、`candidate_source`、`state_name`、`state_sha256`，保留 elapsed 原始值并另外定义排除 elapsed 的 canonical digest。
6. **建议修复**：分别统计 wall-clock、SQLite executions 和上游 generation calls，使候选预算、选择预算和端到端预算不再混用。

