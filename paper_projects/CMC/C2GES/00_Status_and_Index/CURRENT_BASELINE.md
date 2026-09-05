# C²GES 当前基准

更新日期：2026-09-06  
目标期刊：MDPI *Applied Sciences*  
版本性质：协议就绪稿 + 开发集实现验证 + E2 人工验证工具链  
技术状态：`PASS_FOR_PROTOCOL_SNAPSHOT`  
投稿状态：`NOT_SUBMISSION_READY`（E1/E2/E3 确认性证据尚未完成）

## 唯一活动版本

- LaTeX：`../01_Manuscript/LaTeX/paper_applsci.tex`
- LaTeX SHA-256：`74B6DE70BB4859E9DBCD7AFE31DD7AB6EB6FDB50D0123919007A3EC0E036A40B`
- PDF：`../01_Manuscript/PDF/C2GES_Applied_Sciences_2026-09-05_protocol_ready.pdf`
- PDF SHA-256：`4CE48AD0BB3E608E125F1A8496A3D224B36812D74AA095744E798C5A85BB6BB7`
- PDF 页数：24
- 补充材料：`../01_Manuscript/Supplementary/supplementary_materials.tex`
- 升级记录：`../02_Revision_and_QA/02_Working_Plan/C2GES_PROTOCOL_READY_UPGRADE_2026-09-05.md`
- 完整性增量审计：`../02_Revision_and_QA/03_Package_QA/INTEGRITY_DELTA_AUDIT_2026-09-06.md`
- 图表审计：`../02_Revision_and_QA/03_Package_QA/FIGURE_TABLE_AUDIT_2026-09-06.md`
- E1 协议：`../03_Reproducibility/Data/prospective_external_v1/EXTERNAL_PROTOCOL_FREEZE.json`
- E2 协议：`../03_Reproducibility/Data/human_structure_validation_v1/ANNOTATION_PROTOCOL.md`
- E2 执行入口：`../03_Reproducibility/Data/human_structure_validation_v1/HUMAN_VALIDATION_EXECUTION.md`
- E3 协议：`../03_Reproducibility/Data/component_factorial_v1/FACTORIAL_PROTOCOL.json`
- E3 开发试跑：`../03_Reproducibility/Code/prospective_v1/run_2/DEVELOPMENT_PILOT_REPORT.md`
- 布局候选开发试跑：`../03_Reproducibility/Data/prospective_external_v1/layout_dev_pilot_v2/LAYOUT_DEV_PILOT_REPORT.md`

## 基线身份

- 计划给出的 SHA-256 `224BCAC8E903882FB46CD0B5144E29B7726E1937EA81124C8202EDE35E1187E0` 在当前仓库及可见历史中未找到。
- 本轮升级前的活动稿 SHA-256 为 `998917E9AD77B563567A4DDA071680390F9D5B0D390A1E0CC4271E79807FC04B`。
- 未回退 2026-08-25 之后的活动稿修改。

## 已完成的内部质量门

- LaTeX 全流程编译通过：35/35 引用键解析，6 幅图、9 张表、17 个交叉引用均解析，无 overfull box；仅有窄表格造成的非阻断 underfull 提示。
- 6/6 论文图已纳入 `c2ges-figure-lineage-v3`；29 个输入、脚本和输出哈希全部匹配；稿件图与复现图逐一字节一致。
- Figure 6 已消除硬编码取数：正式 post-run 审计提供分数活动、选择活动和历史对比区间，开发校准决策提供 12/12 零权重结果。
- 参考文献当前为 35/35 已核对：34 条继承 2026-08-24 审计，新增 PacSum 论文由 ACL Anthology 官方 BibTeX 与 PDF 核验；0 条悬空引用，0 条幽灵文献。
- R1 已在无 `.git` 的独立 ZIP 解压目录重新验证：当前 231 个清单文件前后均为零缺失、零不匹配、零未登记；公共验证全部通过，验证过程未改写 checksum 或 manifest。
- E3 的 AB、RP 和 G 条件已在 12 份开发报告、6 个系列上完成 312 行实现试跑；该试跑只证明执行链可运行，不是确认性证据。
- 布局候选构建器 v2 已生成 3,782 个开发候选和 244 条无原文审计样本，并通过机械完整性检查；两名真人的边界有效性审计仍未完成。
- E2 已具备盲化表、管理员抽样表、预仲裁哈希锁、精确分歧仲裁检查、系列级区间和 claim-gate 输出；当前未收集任何真人标签，AI 不充当标注者。

## 尚未完成的投稿证据门

1. 冻结合法、未见、系列互斥的外部报告清单；当前 E1 记录仍为 `DRAFT_NOT_FROZEN`、`external_test_accessed=false`、`execution_allowed=false`。
2. 由两名独立真人完成布局边界和结构有效性标注；招募前取得适用的机构伦理审查或豁免认定。
3. 在冻结后一次性执行 E1 与确认性 E3，不得在看到外部结果后修改终点、预算、比较族或排除规则。
4. 按实测结果回填 Abstract、Results、Discussion、Conclusions、Supplement、图表和清单。
5. 若 E2 未达到预设阈值，必须将结构关系降级为 heuristic proxy，并重新评估题目中的 “Structure-Aware”。

在这些门禁完成前，不主张匹配长度下的系统优势、结构关系已经人工验证、真实维护文本泛化或工程任务效用。

## 下次恢复入口

先读取本文件、升级记录、完整性增量审计、Figure–Table 审计、E3 开发试跑报告、布局试跑报告和 E2 执行入口。优先补齐外部系列清单、布局候选冻结、标注者与伦理记录；不得把开发试跑或历史 retained-test 结果升级为新的确认性结论。
