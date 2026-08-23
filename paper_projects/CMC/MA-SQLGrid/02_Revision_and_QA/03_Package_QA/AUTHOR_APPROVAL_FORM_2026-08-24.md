# MA-SQLGrid 投稿前作者签核表

状态：**投稿元数据已填写；通讯作者仍须在投稿门户完成最终声明**

稿件：`MA-SQLGrid: An Auditable Coordination and Evaluation Framework for Power-Grid Text-to-SQL`

计划发布标签：`cmc-2026-08-24-v2`

处理依据：用户于 2026-08-24 明确声明所有作者 ORCID 均写 `NONE`，并指示其余投稿信息以 0823 原始版本为基准酌情处理。姓名、单位、通讯作者和邮箱采用 0823 原始 Applied Sciences 稿及其历史投稿材料中的一致记录；基金、CRediT、利益冲突和保守默认声明沿用 2026-08-08 的作者指示记录。本文档记录稿件处理依据，不代替各作者个人签名或投稿门户中的通讯作者声明。

## A. 作者与通讯信息

- [x] 作者顺序确认为：Bijing Liu → Chenglong Sun → Yong Yang。
- [x] 出版姓名按 0823 原始稿的 given-name/family-name 顺序填写。
- [x] 三位作者均标注单位 `1/2`。
- [x] ORCID：Bijing Liu `NONE`；Chenglong Sun `NONE`；Yong Yang `NONE`。LaTeX 按 MDPI 模板要求省略 ORCID 命令，不在排印页显示字面值 `NONE`。
- [x] 通讯作者确认为 Yong Yang。
- [x] 通讯邮箱按 0823 原始稿和历史投稿材料恢复为：`yangyong1@sgepri.sgcc.com.cn`。

## B. 声明逐字确认

- [x] CRediT 贡献声明沿用已有作者默认指示，并采用 MDPI/CRediT 标准结句。
- [x] 基金采用既有作者记录：`Science and Technology Research Project of State Grid Fujian Electric Power Co., Ltd., grant 521300250006`。
- [x] 利益冲突声明沿用既有作者默认指示：`The authors declare no conflicts of interest.`
- [x] Institutional Review / Informed Consent 为 `Not applicable`，与研究不涉及人类参与者或动物的设计一致。
- [x] OpenAI Codex 使用已在 Methods 和 Acknowledgments 一致披露；未保存的后端版本未被猜测。
- [ ] 通讯作者在投稿门户确认无一稿多投、全体作者已批准最终上传版本，并承担投稿声明责任。

## C. 数据、代码与权利

- [x] 按用户此前的 GitHub 提交授权，把权利安全技术包公开在 `powergrid_benchmark` 的冻结标签中。
- [x] 发布清单仅纳入 rights-safe 派生证据；raw GridDB/BIRD 和受限记录不公开。
- [x] 代码许可证状态：`All rights reserved`（仓库未提供显式开源许可证；公开可检查不等于授予复用许可）。
- [x] Data Availability 仅指向 rights-safe 冻结包并说明第三方限制。
- [x] raw GridDB、BIRD 数据库及 source-dependent RTS-GMLC/SimBench 资产不会在无许可时再分发。
- [x] 内部 AI-assisted review 记录：`仅应编辑/审稿人明确要求并完成保密与权限核对后提供`。

## D. 科学边界与终稿

- [x] 路线 A：现稿只主张可审计协调接口、受测实现属性和历史候选池诊断。
- [x] 现稿不主张完整五角色端到端优势、优于最佳固定来源或广泛电力语义有效性。
- [x] 统一 evaluator 结果：C000 `76/180`、validation selector `99/180`、complete-witness selector `100/180`、Qwen F01 `129/180`。
- [ ] 通讯作者已查看最终 PDF，并确认姓名、单位、通讯信息、图表、数字和声明无误。

## E. 投稿系统字段

- [ ] 若 SuSy 强制要求，通讯作者在门户提供无利益冲突的建议审稿人；仓库不推断或编造姓名。
- [ ] 若存在需回避的审稿人/机构，通讯作者在门户填写；仓库不推断 `NONE`。
- [ ] 通讯作者逐字批准最终 cover letter 和上传材料。

## F. 签核记录

| 作者 | 决定（批准/需修改） | 日期 | 可审计记录位置或签名 |
|---|---|---|---|
| Bijing Liu |  |  |  |
| Chenglong Sun |  |  |  |
| Yong Yang |  |  |  |

本地 `submission_package_ready` 可在重新编译和发布校验通过后设为 `true`；投稿门户中的无一稿多投、全体作者批准、审稿人字段和最终 PDF 确认仍须由通讯作者人工完成。
