# CMC 两篇论文修订历程与可复用模式

## 1. 结论

C2GES 与 MA-SQLGrid 的修订并不是普通的语言润色，而是一次从“历史投稿稿件”到“证据受限、版本冻结、可复现、适配 Applied Sciences 的投稿候选”的系统重建。最有价值的成果不是某一个段落，而是形成了如下稳定模式：

> 唯一基线 → 评审意见结构化 → 主张分级 → 口径/协议冻结 → 证据补强或主张降级 → 内容重写 → 表达保真优化 → 双完整性审计 → 编译与视觉 QA → manifest/hash → immutable tag → 通讯作者门户签核。

## 2. Git 时间线

| 时间 | Commit | 阶段 | 主要作用 |
|---|---|---|---|
| 2026-08-05 | 工作区记录 | 初次 Applied Sciences 重构 | 从 CMC 历史稿迁移到 MDPI 模板，识别应用定位、实验和作者输入缺口。 |
| 2026-08-23 23:20 | `840dcce5` | 唯一基线与目录重建 | 旧 Word/PDF/CMC 源进入 `90_Archive`；建立 `00_Status`、`01_Manuscript`、`02_Revision_and_QA`、`03_Reproducibility`；把 0823 LaTeX 定为唯一活动基线。 |
| 2026-08-24 01:03 | `69aa1d6a` | 主要科学与复现修订 | 153 个文件、17,236 行新增；完成 evaluator/统计/敏感性/消融/权利安全数据/公共验证器等主要证据工程。 |
| 2026-08-24 01:51 | `eaaa60ba` | 0824 候选收口 | 重编 PDF，补引用存在性审计、完整性审计、作者审批表、计划完成度和视觉 QA。 |
| 2026-08-24 01:59 | `ea74e68a` | 门禁语义纠正 | 修正 C2GES 中技术 PASS、声明边界和 scoped claims 的状态表达，避免把受限数据或外部研究误记为已完成。 |
| 2026-08-24 06:57 | `5e9cbe16` | 投稿元数据与附件 | 对齐作者、ORCID `NONE`、通讯信息、CRediT、Funding、COI、GenAI、Data Availability、cover letter 和投稿 checklist。 |
| 2026-08-25 00:27 | `d9de1bee` | 0823 意见复核与表达优化 | 再次逐项核对两份 0823 意见；优化摘要、贡献、讨论、结论、术语和图注；更新图谱 lineage、PDF、manifest/hash；冻结为 `cmc-2026-08-24-v3`。 |

## 3. C2GES 的修订逻辑

### 原始核心风险

- 路径删除组件改变大量分数与选择，却没有改善预定义主要终点；原稿容易把“机制被执行”写成“机制有效”。
- Full 与 Semantic-MMR/TextRank 的输出长度不匹配，等抽取单元比较不能直接支持公平性能优势。
- 报告来自有限的 NERC 技术报告代理语料；没有未见系列、专家结构标注或真实维护任务效用研究。
- LaTeX、补充材料路径、测试、PDF、manifest 和 checksum 一度不同步。

### 实际处理

1. 把路径项从“贡献优势”改为可审计的负结果：当前整合改变选择，但没有改善主要终点。
2. 将误导性的 `strict no-path-deletion` 改为更准确的 `unrenormalized coefficient-removal comparison`，明确相对尺度耦合。
3. 增加输出长度、匹配词数、截断、布局单元、平衡调参、normalized no-path、系列等权、exact sign、LOSO 等诊断。
4. 所有事后分析明确标为 retrospective/diagnostic，不升级为确认性结论。
5. 未完成的双专家结构评价、未见系列和工程效用研究保留为外部门禁；相应强主张从标题、摘要和结论删除。
6. 建立 rights-safe 40 行元数据、Python 3.12 环境、公共入口、测试、正文+补充材料构建、图表 lineage、release manifest 和 checksum。

### 最终科学定位

C2GES 现在主要支持：一个确定性、可追踪、可审计的结构化抽取框架，以及当前路径组件不产生预设性能收益的负结果。它不声称长度控制优势、真实维护效用或外部泛化。

## 4. MA-SQLGrid 的修订逻辑

### 原始核心风险

- 历史 `80/180` 与新生成表 `76/180` 混用，原因来自 evaluator 对空结果列形状的处理漂移。
- selector 只与固定首槽 C000 比较，忽略最强固定来源，容易形成选择性基线。
- 历史候选池、生成实验和五角色接口被混为一条“完整多智能体系统优势”证据链。
- 角色、constructed state、tie/order 和 GridDB 域有效性缺少前瞻性、预算匹配和专家验证。
- 数据库、模型输出、路径、清单和公开 release 的权利/版本边界不一致。

### 实际处理

1. 冻结统一 evaluator，逐题解释 Q104/Q107/Q110/Q140，并把旧 `80` 降为 evaluator-drift provenance；当前统一结果为 `76/180`。
2. 同一 evaluator 下重算八个固定槽、C000、两个 selector，共 1,620 次执行；把最强固定 Qwen F01 `129/180` 放回主比较。
3. 将生成实验、历史池选择和五角色实现审计拆成三条独立证据链。
4. 精确枚举 40,320 个全局顺序，报告 95--128 范围、130/180 top ties、154/180 重复 SQL、strict abstention 和错误分类。
5. 角色利用率与单项诊断只证明接口执行，不证明角色因果效果；constructed states 只作为自动证据，不冒充电力专家语义。
6. 选择路线 A：保留“可审计协调/安全执行/候选诊断接口”，删除完整五角色端到端优势、跨电力库泛化和部署效果。
7. 修复引用 TODO、统计依据、权利声明、相对路径、公共验证、图表 lineage、PDF、manifest 和 checksum。

### 最终科学定位

MA-SQLGrid 现在支持：执行与形状证据可以排除不合格或不一致候选，并使错误轨迹可见；它尚不能可靠地排序多个语义可行候选，也不证明五角色协调提升端到端准确率。

## 5. 写作文笔是否退化

以 `840dcce5` 的 0823 基线与 v3 当前 LaTeX 做机械文体比较：

| 论文 | 基线词数 | v3 词数 | 平均句长变化 | ≥40 词长句率变化 | 自动退化标记 |
|---|---:|---:|---:|---:|---|
| C2GES | 7,331 | 8,607 | 18.99 → 18.71 | 2.59% → 2.61% | 0 |
| MA-SQLGrid | 10,421 | 11,409 | 19.30 → 19.24 | 3.33% → 3.04% | 0 |

这些指标不是写作质量判决，但可以排除明显的句法膨胀。人工对照显示，最后一轮主要改善了三点：

- 从密集的限定条件堆叠改为“贡献—结果—边界”分句，摘要和结论更易读；
- 把抽象的系统自我描述改为具体证据对象，例如 fixed source、selector、path component 和 unified evaluator；
- 负结果与限制仍然保留，没有为了流畅性恢复被撤销的强主张。

因此，本轮文笔没有退化；可读性提高，同时证据保守性得到保留。数字和引用发生了实质变化，必须继续依赖 revision ledger 与完整性审计，不能仅凭句长指标判断正确。

## 6. 可复制的修改模式

### 模式一：主张门控，而不是意见门控

审稿意见不是一律照改。先问：该意见影响哪个主张？需要什么证据？能否在当前权利和时间约束内完成？不能完成时，正确动作通常是缩小主张，而不是制造“看似完成”的实验描述。

### 模式二：先解决口径，再解决数值

MA-SQLGrid 证明 evaluator 不冻结时，任何新数字都会增加版本混乱；C2GES 证明预算不统一时，排序差异不能直接解释为算法优势。修改必须从 estimand、evaluator、budget、split 和 dependency unit 开始。

### 模式三：三类证据不得互换

- 科学效果证据；
- 软件/实现审计证据；
- 事后诊断证据。

三者都可以有价值，但只有第一类在设计满足条件时才能支撑效果主张。

### 模式四：内容轮与表达轮分离

内容轮允许改数字、图表、引用和结论，但必须对账；表达轮只优化句法、组织和术语，不得悄悄改变 evidence level。这是防止“文笔变好、科学含义变坏”的关键。

### 模式五：技术 PASS 与投稿完成分离

代码、测试、编译和 checksum 可以自动 PASS；作者身份、资金名称、ORCID、原创性、一稿多投、全体作者同意、真实审稿人和最终上传只能由作者签核。

## 7. Applied Sciences 适配的升级结果

根据 Applied Sciences 当前官方作者说明，Research Article 应提供可复现的完整实验细节，使用 Word/LaTeX 模板，具有 Abstract、Keywords、Introduction、Materials and Methods、Results、Discussion 和 Conclusions 等结构；LaTeX 投稿应把全部源文件和图像放入一个可重编译 ZIP；cover letter 必须说明重要性与 scope fit，并声明无一稿多投及全体作者同意。期刊范围包含 `Computing and Artificial Intelligence`，该 Section 明确覆盖数据库、信息系统、信息检索、决策支持和多智能体系统。

本次代码升级：

- 新增只读 `scripts/papers/applsci_preflight.py`；
- 禁用含硬编码旧结论的 `build_applied_sciences_versions.ps1`；
- 新增基线写作回归、数字/引用 token conservation、模板/结构/声明/引用/图/PDF/复现/rights/QA/portal 门禁；
- 新增 `--run-project-verifier`，把期刊通用门禁与论文特定验证器组合；
- 新增标准库单元测试和本工作流文档。

官方核对入口：

- https://www.mdpi.com/journal/applsci/instructions
- https://www.mdpi.com/journal/applsci/about
- https://www.mdpi.com/journal/applsci/sections/computing_artificial_intelligence
- https://www.mdpi.com/authors/latex

## 8. 当前回归结果

2026-08-25 对两篇 v3 运行新预检器并调用论文自己的公共验证器：

- C2GES：19 项 PASS，0 项 FAIL，3 类 REVIEW；状态 `PASS_WITH_MANUAL_GATES`。
- MA-SQLGrid：19 项 PASS，0 项 FAIL，3 类 REVIEW；状态 `PASS_WITH_MANUAL_GATES`。
- 两篇 REVIEW 均来自合理边界：SuSy/通讯作者操作、claim--evidence 人工复核、相对 0823 基线的数字/引用变更对账。
- 两篇写作回归自动标记均为 0。

这说明升级后的链路能同时做到两件事：阻止确定性投稿错误，又不越权替作者作科学判断或门户签核。
