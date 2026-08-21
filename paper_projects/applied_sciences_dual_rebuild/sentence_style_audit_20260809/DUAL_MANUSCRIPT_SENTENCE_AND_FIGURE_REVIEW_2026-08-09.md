# 两篇 Applied Sciences 稿件逐句语言、逻辑与算法框图审校

审校日期：2026-08-09  
审校性质：只读评审；未修改两篇论文源文件  
审校对象：

- `three_round_peer_review/final/C2GES/paper_applsci.tex`
- `three_round_peer_review/final/MA_SQLGrid/paper_applsci.tex`

参照对象为本地 20 篇 C²GES 相近主题和 20 篇 MA-SQLGrid 相近主题的 Applied Sciences JATS/XML 正文。逐句清单覆盖摘要、Featured Application、全部正文和 MDPI 后置声明；表格单元格、公式和参考文献条目不作为普通英文句子处理。

## 1. 总体结论

两稿的英文已经达到可送同行评审的基本专业水准。当前主要问题不是语法错误，而是少数句子呈现出明显的“审稿回复式写法”：反复解释标题为何保留、哪些结论不能声称、哪些版本被撤回。必要的证据边界应保留，但更符合 Applied Sciences 研究论文风格的处理是“先陈述研究对象、方法和结果，再在固定位置集中限定外推范围”，而不是在多个章节反复以否定句自我辩护。

参照语料中，句长中位数均为 22 词，90 分位数为 38–39 词；段落中位数为 66 词、3 句。C²GES 当前句长中位数为 16 词，MA-SQLGrid 为 17 词，均不属于整体句子过长。相反，两稿存在较多短限定句，而少量方法句一次装入五个步骤、多个数字或多项版本信息。两稿正文段落中位数为 71–74 词、4 句，处于参照论文中位数略上，符合此前“中位数偏上”的篇幅目标。

| 稿件 | 核对句数 | 可保留 | 建议人工复核 | 优先修改 | 主要原因 |
|---|---:|---:|---:|---:|---|
| C²GES | 565 | 477 | 73 | 15 | 标题/证据边界的元话语、3个超长列举句、斜线数值对、少量跨句指代 |
| MA-SQLGrid | 607 | 502 | 96 | 9 | 5处历史术语未统一、框图说明带防御语气、2个超长资产/实验列举句 |

“建议人工复核”不等于必须重写。多数是 `This/These/It` 指代、`80/180` 一类压缩数值或 38–45 词的可接受长句；逐句表中已给出保留或修改方向。MDPI 的 Author Contributions、Funding、伦理和利益冲突固定句式已作为模板文本处理，不因分号多或句子长而误判为问题。

完整逐句记录：

- `C2GES_sentence_by_sentence_audit.csv`
- `MA_SQLGrid_sentence_by_sentence_audit.csv`
- `sentence_audit_summary.json`

## 2. C²GES：优先句式修改

以下定位对应逐句 CSV 的 `sentence_id` 和 LaTeX `source_line`。建议句是语言层面的推荐，不改变现有实验事实。

| 定位 | 问题 | 建议处理 |
|---|---|---|
| S0001，L19，摘要 | 以 “The title states...” 开篇，像给审稿人的解释，不像研究摘要 | 改为：`Using a selected corpus of public NERC technical reports, this study evaluates C²GES as a maintenance-oriented evidence-selection framework; transfer to operational maintenance records remains untested.` |
| S0040 + S0043，L39，引言 | “exact title”“aspirational”“title-concordant” 连续讨论标题本身 | 合并为研究范围句：`The evaluated corpus comprises public NERC reliability and event-analysis reports rather than utility work orders or field-maintenance narratives. Accordingly, the reported findings do not establish effectiveness or safety on operational maintenance records.` |
| S0049，L43，引言 | “withdrawn from the scientific claims” 带审稿回复口吻，且原因与前句分开 | 合并为：`Results from v0.1 and v0.2 are excluded because those versions used fixed excerpts, permitted Executive Summary leakage, and employed a degree-equivalent deletion quantity.` 建议移入“Corrective Study Chronology”方法段。 |
| S0121，L83，相关工作 | “title-concordant records” 不自然 | 改为 `Unlike the present proxy-corpus study, maintenance-specific studies use domain-concordant records and human semantic evaluation.` |
| S0129，L87，相关工作 | 相关工作段尾变成未来工作清单 | 改为一句 gap statement，详细评价项目移至 Future Validation：`This comparison identifies the need for a maintenance-specific evaluation combining controlled system comparison with qualified human assessment.` |
| S0145，L118，方法 | “must not be collapsed” 命令式、防御性 | 改为 `Each research question is evaluated using a distinct evidence set.` |
| S0260，L247，方法 | 66词、五个步骤通过分号串联 | 改成编号算法或两句。正文只保留：`Selection follows five deterministic stages summarized in Figure X.` 随后用 `enumerate` 或 Algorithm 环境列出五步。 |
| S0347，L306，方法 | 五类可复现资产挤在49词单句中 | 拆为两句：第一句说明 manifest/builder/freeze 的上游身份链；第二句说明 run/audit 的下游记录与复算。 |
| S0516，L558，讨论 | “cannot rehabilitate” 具有辩论色彩 | 改为 `Because the calibration was conducted after disclosure of the test results, it remains exploratory and does not alter the confirmatory status of v0.3.1.` |
| S0518，L558，讨论 | `It` 指代不稳，三个否定并列 | 改为 `The calibration used only development files and did not access the frozen test inputs or outputs. It therefore neither replaces v0.3.1 nor licenses evaluation on the disclosed test reports.` |
| S0524，L564，讨论 | “must not be labeled” 过于规训式 | 改为 `LLM-assisted annotations may be evaluated as a separate workflow condition, whereas expert validation requires judgments from qualified power-grid personnel.` |
| S0543，L576，结论 | “title-concordant holdout” 不自然 | 改为 `Future evaluation should use layout-aware units, equal word budgets, symmetrically tuned comparators, a sealed operational-maintenance holdout, and independent assessment by qualified power-grid personnel.` |
| S0546，L578，补充材料 | 62词的资产目录，不适合连续正文 | 改为 2–3 句，或把资产类别放入 Supplementary Manifest 表；正文只概括“transferable package”和“restricted-local package”。 |
| S0558，L583，Data Availability | 把投稿前待办事项写入正式声明 | 这是内容与投稿状态问题。仓库同步、许可、tag 和 fresh-clone 验证完成后，改为已完成时态并提供固定 tag/DOI；未完成前不宜提交。 |

另有一个应在摘要中直接修正的可读性问题：`103.0/214.5 and 110.7/199.9 more words` 容易使读者无法立即判断四个数分别对应哪个方法和哪个 K。建议改为：`At K=5 and K=10, Full selected 103.0 and 214.5 more words than Semantic-MMR and 110.7 and 199.9 more words than TextRank, respectively.` 结论中的同类句也应同步。

### C²GES 的跨句与章节逻辑

| 部分 | 判断 | 修改方向 |
|---|---|---|
| 摘要 | 方法—数据—结果—消融负结果—边界的顺序正确 | 开头改为直接研究陈述；把四个斜线数值展开；保留负消融结论，这是稿件可信度的重要部分。 |
| 引言 | 从维护文本困难到可审计抽取、相关方法、RQ 和贡献，主线完整 | “标题保留”“代理语料”“旧版本纠正”三组边界重复较多。每组只保留一个核心段，其余移到 Methods/Limitations。 |
| 相关工作 | 摘要技术、图方法和电网文本三条线齐全 | 结尾应落在“现有方法缺少何种组合证据”，不要提前展开未来专家评价方案。 |
| 方法 | 数据、角色、图、路径删除、打分、比较器和统计协议顺序合理，理论定义也足够 | 在方法前部先给整体框图；将五步选择流程改成 Algorithm/编号清单；减少“该设计不能证明什么”的重复句。 |
| 结果 | 完整性审计→总体结果→长度诊断→配对差异→计算诊断→RQ，逻辑最强 | 维持当前结果顺序。各结果段只保留一个最关键限制，避免表注、正文和段尾连续重复。 |
| 讨论与结论 | 对负消融、长度混杂和外部效度处理透明 | “title-concordant” 全部改为具体对象，例如 `operational maintenance records`；把后验校准的时间边界集中说明一次。 |

### C²GES 的术语规范

- 首次定义后统一使用 `typed textual proxy graph`，不要简化成可能被理解为物理模型的 `causal graph`。
- 机制名建议统一为 `path-deletion loss`；`node-deletion path utility` 可作为首次解释，不应与 `counterfactual score/path utility/deletion score` 无规则轮换。
- 第一次写全 `registered unrenormalized no-counterfactual (no-CF) ablation`，其后统一 `registered no-CF ablation`。
- `counterfactual` 只能表示注册的图节点删除扰动；涉及效应、识别或干预时必须带 `textual proxy` 或明确否定物理因果识别。
- `composition-sensitivity interval` 和 `report-composition bootstrap interval` 应选一个主称谓；不得在摘要中无修饰写成常规 population confidence interval。

## 3. MA-SQLGrid：优先句式修改

| 定位 | 问题 | 建议处理 |
|---|---|---|
| S0139，L98，相关工作 | `It` 指代整张表，且 “title-concordant” 生硬 | 改为 `Table X locates the contribution in typed role traces, database-enforced execution, and complete named-state eligibility; prospective evaluation on expert-reviewed power-grid queries remains necessary.` |
| S0187，L212，方法 | “rather than an aspirational free-form agent diagram” 像审稿辩护 | 改为 `Figure X summarizes the implemented information flow, trust boundaries, and deterministic control path.` |
| S0192，L217，图注 | 使用旧称 `counterfactual-required selection` | 改为 `when named-state evidence is required, eligibility requires complete coverage of the registered states`。 |
| S0242，L239，方法 | 使用旧称 `no-counterfactual mode` | 改为 `When named-state evidence is optional, the controller selects ...`；如该词是代码参数，仅首次括注历史名。 |
| S0308，L332，方法 | `counterfactual evidence as unavailable` 与 Metamorphic-State Critic 不一致 | 改为 `The Critic records named-state evidence as unavailable because the existing state-agreement labels are gold-relative.` |
| S0316，L338，方法 | `empty counterfactual mapping` 是实现细节式历史术语 | 改为 `validation-only ranks candidates without named-state evidence, whereas complete-witness selection requires all three reference-free metamorphic outcomes.` |
| S0335，L346，方法 | 55词资产清单加完整 SHA-256，阻断阅读 | 拆成两句；正文只写 21-artifact manifest 和短 hash，完整清单及完整 hash 放表或补充材料。 |
| S0562，L722，未来工作 | 四种实验条件以分号堆叠，且使用旧称 `no counterfactual evidence` | 改为编号列表，并使用 `without named-state evidence`。四个条件必须在候选数和物理调用数上明确 call-matched。 |
| S0597，L739，Data Availability | 把“必须同步和打 tag”写入正式声明 | 与 C²GES 相同：完成后改为已完成时态并给固定 release/tag/DOI；当前文字属于投稿前检查单，不属于最终 Data Availability Statement。 |

以下几类否定句虽然被列为“复核”，但不必机械改写：对 DKA-SQL 非复现、跨 backbone 未复制、事故运行未计入分母的限定均有实质证据作用。建议只保证每段最多保留一个集中限定句，避免相邻三句连续使用 `no/not/neither`。

数值写法建议统一：正文优先写 `80 of 180 questions (44.4%)`，表格内可保留 `80/180`；`raw/adjusted p` 应写成 `raw p = ...; Holm-adjusted p = ...`。多个协议的分母不同，第一次出现时必须随数字带上实验对象。

### MA-SQLGrid 的跨句与章节逻辑

| 部分 | 判断 | 修改方向 |
|---|---|---|
| 摘要 | 架构、四类证据、离线结果和结论边界完整 | 信息密度很高。可删去一部分资产规模细节，把摘要集中在架构、三项关键观察和证据上限。 |
| 引言 | 问题背景→五角色→证据分层→RQ→贡献，逻辑成立 | “不是自主多智能体实验”和“robust 的有限含义”重复出现；在引言末集中定义一次，后文只在必要处引用。 |
| 相关工作 | Text-to-SQL、schema linking、agent decomposition 和电网外部效度覆盖充分 | 末段从文献比较跳到作者缺失证据时，应以 Table X 为明确主语并缩短。 |
| 方法 | master protocol map 有效防止四类实验混用；角色、执行器、裁决和统计协议均可复现 | 架构部分应更早出现整体图；`counterfactual` 历史术语必须清理；五角色核心与继承实验的边界可在小节标题上进一步显式化。 |
| 结果 | 各协议分节报告，完整负结果和事故记录均保留，统计逻辑严谨 | 同一证据限制在表注、正文开头、正文结尾多次出现。每一小节保留“estimand + one limitation”即可。 |
| 讨论 | evidence map 将软件符合性、有限语料表现、非电网迁移和未完成验证分开，逻辑清楚 | 将多处 `not a five-role result` 汇总为一个总括段，随后分别解释机制含义。 |
| 局限性与结论 | 对历史候选池、先验结果暴露、tie rule 和专家语义缺失披露充分 | 未来四条件实验改为列表；结论中的多个 `80/180` 适当转成“n of N + percentage”。 |

### MA-SQLGrid 的术语规范

- 五个角色统一为：`Query Analyst`, `Schema Cartographer`, `SQL Synthesizer`, `Validation Engine`, `Metamorphic-State Critic`。
- `Counterfactual Critic` 只在首次定义历史名称时出现一次，后文不得再用 `counterfactual evidence`, `counterfactual-required selection`, `no-counterfactual mode` 或 `empty counterfactual mapping` 作为论文主术语。
- `SQL Synthesizer` 的固定定义是“packages externally supplied candidates”；不得使用暗示核心协议自行生成 SQL 的动词。
- `Validation Engine` 表示角色；`read-only executor` 表示数据库信任边界。避免在同一段交替使用 `Validator`, `database validator`, `executor` 而不区分层次。
- `multi-agent` 表示五角色软件分解，不表示五个自主 LLM；该定义在引言首次说明一次即可。
- `robust` 只对应已测试的 mutation denial、bounded execution、complete-evidence gating 和 constructed-witness behavior；结果句应点名维度，不单独使用 `robust system`。
- `constructed-state evidence`, `named-state evidence` 和 `metamorphic witness` 可分别表示证据类别、注册状态集合和具体测试变换，但应在首次定义时给出层级关系。

## 4. 两个新框图加入后的处理

两个新图不应作为额外重复图直接插入。两篇论文已经各有一个高层算法/协调图；最合理的处理是以新图的干净视觉风格重绘并替换现有框架图，然后把必要的机制细节作为同一图的第二面板或 inset。否则会出现两张图表达同一条流水线，而没有增加方法信息。

### 4.1 C²GES 新图

推荐位置：放在 Materials and Methods 的 `Task, Scope, and Evidence Class` 之后、数据和各模块细节之前，作为方法总览；不要等到 typed graph 小节结束后才出现。

建议新增正文承接句：

> Figure X summarizes the end-to-end deterministic pipeline. Sections X–X define candidate construction, lexical role assignment, typed graph construction, path-deletion loss, channel normalization, and redundancy-aware selection.

建议图注：

> Overview of the deterministic C²GES pipeline. Complete reports pass candidate and leakage gates; retained sentences receive lexical roles and form a typed textual proxy graph. The normalized Q, R, G, C, and P channels feed the same redundancy-aware selector. The registered no-CF ablation sets C to zero without renormalizing the other coefficients. The graph is a structural text proxy and does not identify physical causal effects.

图本身还需修正：

- 把 `Cause / Trigger` 改为与正文 taxonomy 完全一致的 `Root Cause / Trigger`。
- no-CF 虚线应从五通道打分框的 `C` 分支出来，再进入同一 selector；当前从下方直接指向 selection，容易被读成额外输入。
- 增加一个小型 zoom-in：`G → remove node i → recompute U(G\i) → C_i = U(G)-U(G\i)`，否则题目中的 Counterfactual 机制只剩一个标签。
- 图内底部 “not physical causal identification” 可以保留，但更适合移到图注，以减少图中审稿辩护式文字。
- 当前 clean PDF 是 PNG 封装的栅格 PDF，不是可复现矢量图；投稿版仍应按这一风格重绘为 SVG/原生 PDF。

### 4.2 MA-SQLGrid 新图

推荐位置：替换 `Five-Agent Coordination Framework` 小节开头的现有 Figure `fig:coordination`。

建议新增正文承接句：

> Figure X separates the five typed roles, the append-only evidence trace, the read-only execution boundary, deterministic adjudication, and the post-sealing evaluation boundary.

建议图注：

> Implemented MA-SQLGrid information flow. The Query Analyst and Schema Cartographer post question and schema records to an append-only blackboard, and the SQL Synthesizer packages externally supplied candidates. The Validation Engine records read-only execution evidence, while the Metamorphic-State Critic records complete named-state evidence when required. Hard gates precede the effective evidence score and deterministic tie rule. Gold or reference results are loaded only after the decision and board digest are sealed.

图本身还需修正：

- 增加 `Deterministic Controller` 控制条或外框；当前图遗漏了论文明确声明的协调器。
- 将 Analyst→Cartographer 的依赖显示出来，或明确 Cartographer 读取 Blackboard 中的 intent record；目前两者都像只直接读取原始请求。
- Blackboard 与 Validation Engine/Critic 的箭头应区分“读取候选/状态”和“append evidence”，当前方向容易误读。
- `10 Shape + 5 Order + 5 Value` 改为精确公式 `10 I_shape + 5 I_order + 5 V`，其中 `V∈[0,1]`。
- `Complete Required Evidence` 改为 `Complete Named-State Evidence (when required)`，避免暗示所有模式都强制三状态证据。
- 修正 `5.Metamorphic-State Critic` 的缺失空格。
- 底部 “not autonomous-agent superiority” 更适合放入图注，而不是作为图内结论。
- 与 C²GES 相同，当前 PDF 是栅格封装，最终应矢量重绘。

## 5. 是否需要“更详细的神经网络模块架构图”

结论：不需要，也不应画成神经网络结构图。两篇论文的核心创新都不是一个经过训练的神经网络。

- C²GES 的核心是候选构建、词法角色、typed textual proxy graph、qualified-path deletion、五通道确定性打分和冗余感知选择。MiniLM 只属于 Semantic-MMR 比较器。若给 C²GES 画 Transformer/GNN 层级图，会误导审稿人以为 C²GES 训练了图神经网络或端到端神经模型。
- MA-SQLGrid 的核心是五角色软件契约、append-only blackboard、read-only executor、named-state evidence、硬门控和确定性裁决。Qwen 与 Granite 是外部候选来源或既有实验 backbone，不是协调核心中的可训练模块。画神经网络层图会把软件架构错误包装成自主 LLM 多智能体系统。

但两篇都需要“更详细的算法机制架构”，建议以双面板方法图实现，而不是新增神经网络图：

1. C²GES：面板 (a) 使用当前干净总览；面板 (b) 画 role assignment → typed edges → qualified paths → node deletion → `C_i` → greedy selection 的机制放大图。
2. MA-SQLGrid：面板 (a) 使用五角色/Blackboard 总览；面板 (b) 画单个 candidate 的生命周期：external candidate → safety/read-only execution → named-state completeness → effective score → stable tie/abstain → seal → offline gold evaluation，并标出 controller 和 trust boundary。

这种处理与本地相近 Applied Sciences 方法论文的表达逻辑一致：总览图负责“模块关系”，细节图或子图负责“核心新机制”，公式、伪代码和实验表负责精确定义与证据。只有当作者提出并训练了新的神经网络时，才需要层级、张量尺寸、激活函数或注意力模块示意图。

## 6. 推荐修改顺序

1. 先统一 MA-SQLGrid 的五处历史 `counterfactual evidence` 术语，并修复两个 Data Availability Statement 中的投稿前待办式文字。
2. 修改两篇摘要和引言中的标题元话语，保留证据边界但改为直接研究表述。
3. 展开 C²GES 的斜线数值对，将两篇超长流程/资产句改为列表或两句。
4. 用新视觉风格重绘两张双面板矢量框图，并替换现有同类框图，不增加重复图。
5. 最后全局检查图中文字、正文术语、图注、Algorithm 和变量符号是否逐字一致，再重新编译 PDF 检查字号和跨页位置。

完成上述修改后，两篇论文不需要为了“看起来像深度学习论文”而添加神经网络结构图；相反，应让图准确体现各自真正的算法和软件创新。
