# MA-SQLGrid 0823 执行计划完成度审计

审计日期：2026-08-24

原始意见：`01_Incoming_Review/MA_SQLGrid_review_2026-08-23.md`

执行计划：`02_Working_Plan/DETAILED_REVISION_PLAN_2026-08-23.md`

路线决定：`02_Working_Plan/ROUTE_DECISION_2026-08-23.md` 的**路线 A（范围收缩）**。

## 结论

**本地技术执行完成；作者门禁未完成。** 当前版本已经把生成实验、历史候选池选择和五角色接口三条证据链分开，并以统一 evaluator、显式 artifact 边界和保守标题/摘要/结论闭环。作者元数据、通讯邮箱、声明、许可证、权利和投稿批准不能自动推断，保持 `OPEN`。状态为 `technical_status=PASS`、`submission_ready=false`。

## P0 核对

| ID | 状态 | 证据 / 处理 |
|---|---|---|
| M-P0-01 evaluator 口径 | COMPLETE | 统一协议冻结 T0、shape、empty、order、NULL、容差、错误和 normalized-SQL identity。 |
| M-P0-02 76/80 审计 | COMPLETE | C000 与 Qwen F00 的 180 条 normalized SQL 相同；Q104/Q107/Q110/Q140 的空行/列形状差异解释了旧 evaluator 漂移，统一结果为 76。 |
| M-P0-03 八槽与 selector | COMPLETE | 八槽、C000 和两个 selector 在统一 evaluator 下共 1620 次执行；完整计数、paired interval 和 Holm 均可重算，Qwen F01 为 129。 |
| M-P0-04 文本数字同步 | COMPLETE | 标题、摘要、贡献、方法、结果、讨论、结论和图表同步为 76/99/100/129，并报告 best fixed source、tie 和 order sensitivity。 |
| M-P0-05 引用 TODO | COMPLETE | TODO 清零；活动参考文献 37/37 通过存在性/身份和语境审计，0 dangling、0 orphan。 |
| M-P0-06 作者元数据 | **OPEN — AUTHOR** | `AUTHOR_APPROVAL_FORM_2026-08-24.md` 已建立；邮箱、ORCID、姓名/单位、CRediT、基金、冲突和投稿同意待作者填写。 |
| M-P0-07 数据权利与 release | **OPEN — AUTHOR/RIGHTS** | Rights inventory 与收缩后的 Data Availability 一致；公开包不含 raw GridDB/BIRD。作者仍须选择代码许可证并书面确认发布/审稿访问权限。 |
| M-P0-08 可移植复现 | COMPLETE | 项目相对单入口、35 项测试、核心数据/图/引用和临时干净 LaTeX 构建通过；受限原始库不冒充公开重生成。 |
| M-P0-09 发布包同步 | COMPLETE | `Package_Metadata/RELEASE_MANIFEST.json` 与 `FILE_SHA256SUMS.txt` 对当前布局重建；独立 `--check` 为零 mismatch/missing/unlisted。 |
| M-P0-10 投稿附件 | **OPEN — AUTHOR** | 路线 A cover letter 与 AI disclosure 已起草；审稿人/回避名单、通讯邮箱、许可证和全体作者逐字批准待提供。 |

## P1/P2 核对

| ID | 状态 | 结论 |
|---|---|---|
| M-P1-01 并列/去重/顺序 | COMPLETE AS RETROSPECTIVE DIAGNOSTIC | 40320 个全局槽位顺序、95--128 范围、130/180 top tie、154/180 含重复 SQL、unique-SQL 和描述性 AURC 均保留；未选择 outcome-best 顺序。 |
| M-P1-02 角色利用率/消融 | COMPLETE AS IMPLEMENTATION AUDIT | role utilization、query/shape/order/value/witness/schema 单项诊断和 trace/cost 已记录；未声称前瞻性角色因果效应。 |
| M-P1-03 预算匹配端到端 | NOT REQUIRED UNDER ROUTE A / **OPEN FOR ROUTE B/C** | 当前稿删除完整系统端到端优势；恢复该主张前必须做同模型、同预算、未见集的前瞻性调用。 |
| M-P1-04 未见电力集与专家 | NOT REQUIRED UNDER ROUTE A / **OPEN FOR STRONG VALIDITY CLAIMS** | 当前范围限于合成 GridDB、构造状态和 non-grid BIRD；无双领域专家语义审核。 |
| M-P1-05 风险—覆盖率/失败模式 | COMPLETE AT AUTOMATED LAYER | tie-size AURC、strict abstention、1980 行自动错误分类和 1620 次执行已报告；阈值非预注册且无专家复核的边界保留。 |
| M-P1-06 扩展 state 证据 | COMPLETE FOR AUTOMATED CONSTRUCTED STATES; **OPEN FOR EXPERT SEMANTICS** | 预测盲构造状态和实现测试完成；业务语义不变量与新外部变换仍需专家确认。 |
| M-P2-01 第二电力数据库 | **OPEN — EXTERNAL/RIGHTS** | 无跨库强主张；需第二个合法电力数据库才能扩展。 |
| M-P2-02 规模/复杂度 | **OPEN — EXTERNAL** | 当前仅报告历史 trace 成本，未冒充尺度曲线；新增规模、token、内存和超时实验未执行。 |
| M-P2-03 流程/案例可视化 | COMPLETE | Figure 1/6 有 lineage；Q039、错误表和证据流均保留，案例不替代统计或专家判断。 |

## 0824 新增收口

- 标题按路线 A 收缩为 `An Auditable Coordination and Evaluation Framework for Power-Grid Text-to-SQL`，cover letter 同步。
- 活动 BibTeX 从 49 条清理为 37 条；修正 `liu2022semantic` 作者姓氏和 Canay DOI `10.3982/ECTA13081`。
- 37/37 引用通过 DOI、官方 proceedings、出版社或记录化主来源核验；0 dangling、0 orphan；Crossref 错误作者字段用 ACL Anthology 主记录显式覆盖。
- Data Availability 绑定 `powergrid_benchmark` 冻结标签 `cmc-2026-08-24-v1`；旧 `ma-sqlgrid` 仓库明确不是本稿 release。
- 未经记录的“全体作者已批准”完成时态已删除；通讯邮箱保持占位。
- Rights inventory 中错误写成已完成的 manuscript agreement 改为 `OPEN`。
- 0823 PDF 已移入 `90_Archive/04_Pre_20260824_PDF/`；活动目录仅保留 0824 的 27 页 PDF。
- 逐页视觉检查覆盖 27 页；零空白页、裁切、重叠、未定义引用和 overfull box。

## 投稿前仍需作者执行

1. 完成并签署 `AUTHOR_APPROVAL_FORM_2026-08-24.md`，尤其是 Yang Yong 邮箱、作者顺序/ORCID、CRediT、基金/冲突、许可证和最终 PDF。
2. 逐字批准 cover letter，并提供建议/回避审稿人信息。
3. 若继续路线 A，不需要用未完成的新实验支撑已删除的强主张；若切换路线 B/C，必须重新预冻结、执行外部研究并发布新 tag，不能把本次事后诊断升级为确认性结果。
