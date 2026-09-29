# MA-SQLGrid 当前基准

更新日期：2026-09-15

## 用户指定的新基准（优先于以下Workspace历史）

当前正文为`../../revised/Information_0912_v3/paper_information.tex`，以0912人工润色Applied Sciences投稿包为基础，保留v2失败分解与BIRD回放，并加入冻结的同池合成选择器对照。

**2026-09-15 当前交付状态**：

- 正文 SHA-256：`83b98d0611a21621bb116d0081a07c9fb4721f4a7c090be961c7c949f22399bd`；PDF `57d9f792314195e7c11a3342fa87c9b7aec577bc24519e93f4773bdaa7f7f5e9`；**33 页**，0 错误 / 0 Overfull / 0 未定义引用。
- 投稿包：`revised/MA_SQLGrid_Information_0912_v3_submission.zip`（66 文件）。
- 补充材料：`revised/MA_SQLGrid_Information_0912_v3_supplementary.zip`（162 文件，`verify_supplement.py --run-tests` PASS）。
- **本轮新增**：11 条已核实引用（37→48）；§2.1/2.2/2.3 与 Table 1 扩写；L37 新颖性主张重写；L45 中心论断；**免训练 SQL-consensus 基线**（`analysis/consensus_baseline/`，随包分发，first-eligible 76 / consensus 107 / validation-only 99 / complete-witness 100 / best fixed 129）；去 AI 腔（数字多重集与全部 `\cite`/`\ref`/`\label` 键经独立 diff 验证未变）。
- 两路评审记录与合并意见：`../../revised/wiki/`（`REVIEW_SYNTHESIS.md` 为合并稿）。
- 未提交、未录用。外部效度缺口（无未见专家标注电网数据）仍未关闭，两路独立评审均指向此条。

**一处待作者确认的不一致**：本文件下方历史记录中通讯邮箱为 `yangyong1@sgepri.sgcc.com.cn`，而当前正文 `\corres{}` 为 `yangyong67@126.com`。投稿前须确认以哪个为准。

## 最新：Meta skill 评分—修订—复评分

- 当前主稿 SHA：`2261D07BB8FC23CD134DCB0CC11FB16703A2026C3387FBBB90B900A25A5F07A8`；PDF 30页。
- 评分与修改报告：`../02_Revision_and_QA/09_Meta_Skill_Loop/AFTER_REVIEW.md`。
- 本地咨询评分56.25→56.25/100；Results导读逻辑已改进，但没有新增科学证据，不上调实验/外部验证得分。
- 以下第三轮记录及ZIP为上一版本历史，不能当作此新SHA的完整包。未投稿、未录用。

## 当前进行中的重构：Information 第三轮

- 当前 `paper_information.tex` 已进行三轮实质修改、验证与咨询复评；不等于科学问题全部关闭或可录用。新增失败分解、叙事重构与统计主表/附录分离。
- 主稿 SHA-256：`05F0365C484C27AA91E8CA699D0FF4B8801A1BA0415E99264EE983B5EB5B3CDA`。
- 当前 PDF 编译为30页；视觉复核范围见第三轮记录。下方旧v1的28页不再代表当前版本。
- 计划与恢复入口：`../02_Revision_and_QA/08_Information_Iterations/ITERATION_PLAN.md`。
- 第一轮评审：`../02_Revision_and_QA/08_Information_Iterations/round1/REVIEW.md`；构建/数值/保留验证见同目录 `verification.json`。
- 第二轮评审：`../02_Revision_and_QA/08_Information_Iterations/round2/REVIEW.md`；数值保留与构建验证见同目录 `verification.json`。
- 第三轮评审：`../02_Revision_and_QA/08_Information_Iterations/round3/REVIEW.md`。本地ZIP独立解压验证219文件零变化，38测试及30页构建通过；包在项目根目录`Information_Candidate_R3_20260913/`。
- 下一步：核实跨候选池诊断所需的真实输入；公开版本绑定与作者最终确认仍未完成。未提交、未录用、未发表。

## 历史活动草稿记录：Information 改写 v1（已被第三轮覆盖）

- 目标期刊：MDPI *Information*；这是本地转投改写，尚未提交。
- LaTeX：`../01_Manuscript/LaTeX/paper_information.tex`
- PDF：`../01_Manuscript/LaTeX/paper_information.pdf`（28 页）
- 文献下载、全文蒸馏、差异及验收：`../02_Revision_and_QA/06_Information_Rewrite/INFORMATION_REWRITE_REPORT.md`
- 构建说明：`../01_Manuscript/LaTeX/BUILD_INFORMATION.md`
- 写作/编译/版面检查通过；不等于独立科学验证、作者批准或完整提交包就绪。
- 历史发布标签、投稿信和签核不自动绑定此新稿；旧主稿和实验材料保留不覆盖。

## 历史基准：Applied Sciences（保留溯源，不再是活动草稿）

以下为 2026-08-24 的历史记录；其中技术 PASS 仅适用于相应历史版本。

目标期刊：MDPI *Applied Sciences*

科学路线：路线 A（可审计协调与评价框架）

技术状态：`PASS`；投稿模式验证与最终 PDF 视觉检查均通过

### 历史版本入口

- LaTeX：`../01_Manuscript/LaTeX/paper_applsci.tex`
- 正文 PDF：`../01_Manuscript/LaTeX/paper_applsci.pdf`
- 投稿信：`../02_Revision_and_QA/05_Submission_Draft/COVER_LETTER_DRAFT_2026-08-23.md`
- 投稿元数据记录：`../02_Revision_and_QA/03_Package_QA/AUTHOR_APPROVAL_FORM_2026-08-24.md`
- 计划冻结标签：`cmc-2026-08-24-v3`

## 已落实的投稿元数据

- 作者：Bijing Liu；Chenglong Sun；Yong Yang。
- 三位作者均使用单位 1/2；Yong Yang 为通讯作者。
- 通讯邮箱：`yangyong1@sgepri.sgcc.com.cn`，来源为 0823 原始稿和一致的历史投稿材料。
- ORCID：三位作者均为 `NONE`；按 MDPI 模板规则不在 LaTeX 中创建 ORCID 命令。
- 基金、CRediT、利益冲突及 AI 披露沿用已有作者指示，并与正文声明一致。

## 当前边界

- 当前稿不主张五角色端到端优势、不主张优于最佳固定来源，也不主张广泛电力语义有效性。
- raw GridDB、BIRD 数据库和其他受限资产不进入公开包；公开代码没有显式开源许可证，按 `All rights reserved` 处理。
- 通讯作者仍须在 SuSy 中人工确认无一稿多投、全体作者批准、最终 PDF、审稿人字段及其他门户声明。这是投稿动作，不是本地包的技术失败。
