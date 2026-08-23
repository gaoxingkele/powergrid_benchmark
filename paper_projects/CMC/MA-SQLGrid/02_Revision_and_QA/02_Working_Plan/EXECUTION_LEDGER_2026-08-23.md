# MA-SQLGrid 修订执行证据台账

更新日期：2026-08-23
基准提交：`840dcce5835423a5cdc3ee9f84eccfc601a6f4f6`
当前路线：路线 A（范围收缩）；技术包 `PASS`，`submission_ready=false`。

| ID | 状态 | 执行证据 | 尚未关闭的边界 |
|---|---|---|---|
| M-P0-01 | 已验证 | `MA_SQLGRID_EVALUATOR_PROTOCOL_2026-08-23.md` 冻结 T0、shape、empty、order、NULL、tolerance、错误和 SQL identity 口径及哈希 | 无 |
| M-P0-02 | 已验证 | C000 与 Qwen F00 180 个 normalized SQL 全同；Q104/Q107/Q110/Q140 为 empty-row 但列数不符；统一 evaluator 得 76 而非历史 80 | 历史值仅保留为 evaluator-drift provenance |
| M-P0-03 | 已验证 | 八槽+C000+两个 selector 同一 evaluator：1,620 次执行；完整 counts/paired interval/Holm；Qwen F01=129 | 无 |
| M-P0-04 | 已验证 | 摘要、贡献、方法、结果、讨论、结论、Figure 5/6 同步为 76/99/100/129 | 无 |
| M-P0-05 | 已验证 | citation TODO 清零；37 个引用 key 全部存在，LaTeX 无未定义引用 | 无 |
| M-P0-06 | 待作者输入 | 作者/邮箱/ORCID/CRediT/基金/冲突/投稿同意门禁表已建立 | 通讯邮箱占位符仍保留，禁止推断 |
| M-P0-07 | 待作者输入/权利 | rights notice 与收缩的 Data Availability 已一致 | GridDB/BIRD/模型/仓库 release 的公开授权需作者关闭 |
| M-P0-08 | 已验证 | 项目相对单入口；35 tests；核心数据、图、引用和临时干净 LaTeX 构建通过 | 受限原始数据库和模型输出不由公开验证器再生成 |
| M-P0-09 | 已验证 | 当前布局 Package_Metadata manifest/checksum 已重建；独立 `--check` 要求零 missing、unlisted 和 mismatch | 修改任何 release 文件后必须重新冻结 |
| M-P0-10 | 待作者输入 | `COVER_LETTER_DRAFT_2026-08-23.md` 已按路线 A 起草；AI disclosure 已在正文 | 审稿人/回避名单、邮箱和全体作者批准不能推断 |
| M-P1-01 | 已验证（事后诊断） | 精确枚举全部 40,320 全局槽位顺序，范围 95--128；130/180 top ties；154/180 池含重复 SQL；unique-SQL 与风险覆盖/AURC 已报告 | 未选择 outcome-best 顺序；未来 tie/abstention 规则仍需未见数据校准 |
| M-P1-02 | 已验证（实现审计） | 角色利用率、query/shape/order/value/witness/schema 单项诊断、消息/执行/失败/SQL hash/零模型调用成本记录 | Schema Cartographer 在历史池为 recorded-only；未声称前瞻性角色因果效应 |
| M-P1-03 | 待外部研究 | 路线 A 已删除端到端优势主张 | 缺同模型、同预算、未见集前瞻调用 |
| M-P1-04 | 待外部研究 | 正文限制为单一合成 GridDB 与 non-grid BIRD | 缺合法未见电力库及双领域专家 |
| M-P1-05 | 已验证（自动层） | tie-size risk--coverage、strict abstention、描述性 AURC；1,980 行自动错误分类/1,620 执行 | 阈值非预注册且无专家语义复核，正文明确诊断性质 |
| M-P1-06 | 待外部研究 | 自动 constructed-state 制品和实现测试保留 | 缺专家确认的业务语义不变量及新变换 |
| M-P2-01 | 待外部研究 | 无跨库强主张 | 缺第二个合法电力数据库 |
| M-P2-02 | 待外部研究 | 历史池已有 3,960 messages、5,760 attempts、839ms recorded aggregate；不冒充规模曲线 | 缺新增规模/复杂度和 token/内存/超时实验 |
| M-P2-03 | 已验证（可视化层） | Figure 1/6 与 lineage 覆盖角色流和证据流；Q039 轨迹与自动错误表已报告 | 案例不替代统计或专家判断 |

## 最终技术验收

- 公共验证报告：`02_Revision_and_QA/04_Build_Reports/MA_SQLGRID_PUBLIC_VERIFICATION.json`，技术状态 `PASS`。
- PDF：27 页、6 图、12 表；逐页渲染和 contact sheet 检查通过。
- 路线决定：`ROUTE_DECISION_2026-08-23.md`。当前稿不主张完整五角色端到端优势或广泛电力语义有效性。
