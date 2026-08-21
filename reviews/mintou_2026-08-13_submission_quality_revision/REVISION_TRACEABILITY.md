# 闽投六篇投稿质量提升：修订追踪表

日期：2026-08-13  
依据：`reviews/mintou_2026-08-12_paper_skill_narrative_audit/ACADEMIC_NARRATIVE_LOGIC_AUDIT_ZH.md`  
范围：六篇 `paper_projects/mintou_p*/manuscript/MANUSCRIPT.md` 及其确定性生成投稿文件。

## 修订约束

- 不修改既有实验数字、方向、样本量或显著性决定。
- 不删除不利结果，不把未显著改写成等效。
- 不把 seed-level variability 外推为跨年份、跨网络或真实项目有效性。
- 不把 trace coverage 外推为可解释性、人工审查质量或部署收益。
- 正文修改以最小必要补丁完成；证据表和原始运行资产只读。

## 关注项与处理

| ID | 论文 | 审核问题 | 严重度 | 处理 | 状态 |
|---|---|---|---|---|---|
| P1-1 | P1 | `Siamese` 容易被理解为带 contrastive loss | Minor | 首次定义改为 shared-encoder / Siamese-style，并明确无独立 contrastive objective | 已实施 |
| P1-2 | P1 | 复现句具有宣传语气 | Minor | 改为客观说明 released command 重建哪些产物 | 已实施 |
| P2-1 | P2 | Contribution 写成显著性与证据许可清单 | Major | 改为组件可识别方法、多设置评价、适用条件图谱三项贡献 | 已实施 |
| P2-2 | P2 | “result we did not want” 暴露项目预期与纠错叙事 | Major | 改为中性的 aggregation/weight-form comparison | 已实施 |
| P2-3 | P2 | `Evidence Hierarchy and Claim Calibration` 审稿回复腔 | Major | 改为 Aggregation, Weighting, and Hierarchical Coherence | 已实施 |
| P2-4 | P2 | preliminary screen 后仅对 MLP 十 seed 确认 | Major | MLP 统一称 targeted baseline，screen 与 confirmatory comparison 分层 | 已实施 |
| P3-1 | P3 | FixedDE 同时关闭参数和策略，不能支持独立归因 | Major | 全文改为 combined parameter-and-strategy adaptation bundle；删除独立开关和 one-switch 主张 | 已实施 |
| P3-2 | P3 | 组合消融被写成 strategy adaptation 结论 | Major | Abstract、Contribution、Results、Discussion、Conclusion 同步改为 joint effect | 已实施 |
| P4-1 | P4 | 标题 `Lookahead` 无方法、伪代码或实验对应 | Major | 题目改为 Scenario Screening with Disjoint Evaluation | 已实施 |
| P4-2 | P4 | main ablations 与 targeted controls 的归因层级混用 | Minor | Methods 区分 individual main switches 与 multi-option targeted controls | 已实施 |
| P4-3 | P4 | P3 companion citation 使用旧题目 | Major | 更新为 P3 当前题目 | 已实施 |
| P5-1 | P5 | trace 与优化两条主线没有共同的人类效用终点 | Major | 题目和中心故事改为 traceable portfolio optimization / inspectable search | 已实施 |
| P5-2 | P5 | trace 被与 search component 放在同一消融层级 | Minor | 区分 switchable search components 与 quarantined output channel | 已实施 |
| P5-3 | P5 | P6 companion citation 使用旧题目 | Major | 更新为 P6 当前题目 | 已实施 |
| P6-1 | P6 | `Forward-Dominant` 依赖特殊定义且 pooled mean 不支持 | Major | 从题目、摘要、章节标题和图中文字中移除，保留 scenario-dependent finding | 已实施 |
| P6-2 | P6 | full 与 lean variant 推荐关系不清 | Major | 明确 forward-only 为无需 atomic replacement records 时的 lean configuration | 已实施 |
| X-1 | 全部 | 限制和证据边界在多节重复，形成审计腔 | Minor | 压缩元叙事和内部版本词；保留 Methods 范围和 Limitations 集中边界 | 已实施 |
| X-2 | 全部 | 投稿 PDF/LaTeX 尚未同步本轮修改 | Major | 运行正式模板构建、预览构建、PDF QA、引用与标题扫描 | 已验证 |
| X-3 | 全部 | Markdown 的 H2 被错误生成为 LaTeX 子节，正式稿出现 `A. INTRODUCTION` 或 `0.1 Introduction` | Major | 正式模板与预览构建器统一将正文标题上移一级，并全量重编译 | 已修复并验证 |
| X-4 | P1/P4 | 作者、单位、通信作者或基金仍为明确占位符 | Submission blocker | 不猜测作者元数据；列入提交前人工确认清单 | 待作者输入 |

## 不在本轮擅自补写的内容

- 作者尚未确认的 CRediT 角色、基金编号、通讯作者或利益冲突信息。
- 需要真实专家参与的投资评审效用和解释充分性结论。
- 需要新增运行才能支持的 rolling-origin、独立网络优化或参数分离消融结果。

这些项目会作为投稿阻断项或剩余证据风险单列，不会以推测内容填入正文。
