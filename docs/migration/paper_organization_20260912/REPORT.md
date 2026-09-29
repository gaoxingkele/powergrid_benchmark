# 论文项目归类报告

日期：2026-09-12。实体仓库：`F:/aicoding/powergrid_benchmark`；`D:/aicoding/powergrid_benchmark` 是此前已存在的兼容入口。

## 已实施

- 8 篇论文使用缩写项目目录：GRU-LSR、CSA-LoadNet、CARS-MODE、SHIELD-MOEA、TRACE-MOEA、BiLo-NSGA、C2GES、MA-SQLGrid。
- 实际移动 14 个目录：六篇闽投工作目录、六篇对应 ARA 目录、两篇 CMC 现行工作区。目录内部文件原样保留，没有删除或覆盖稿件、数据、代码、旧 PDF、历史 ZIP。
- 每个移动文件均进行迁移前后完整 SHA-256 比较。完整逐文件清单为 `before.json`，每项迁移确认在 `completed.json`。
- 14 个旧路径保留永久 Windows Junction，旧脚本与文件引用仍可访问同一份内容。新旧入口不是双份副本。
- 明确归属的散落历史素材收录于各篇 `PROJECT_INDEX.md`，目录素材以 `90_History_Links` 联接进入；独立 ZIP、审查记录等文件用索引指向原件。完整分类与扫描范围在 `catalog.json`。
- 混合交付包保持原结构。公共数据集、共享 `src`、配置、模板及 paper harness 不按论文重复拷贝。
- 关联 Git 工作树保持原目录与分支，在能确认论文归属时列入各篇项目索引。

## 当前稿辨识

- MA-SQLGrid 当前入口为 `Workspace/01_Manuscript/LaTeX/paper_information.tex`，不是历史 Applied Sciences 主稿。
- C2GES 当前入口为 `Workspace/01_Manuscript/LaTeX/paper_applsci.tex`，当前 PDF 以 `Workspace/00_Status_and_Index/CURRENT_BASELINE.md` 为准。
- 闽投保留 `manuscript/journal_submission`、`submission_preview`、checkpoint 与冻结证据的区别；不凭修改时间将旧预览自动升级为已批准稿件。
- 项目缩写只用于存储归类，本次未修改锁定标题、作者、实验结果或投稿结论。

## 其他独立论文的核查边界

查看了本仓库 `paper_projects`、`papers/planning`、`paper`、`ara_artifacts`、交付目录与上传目录，并查看相邻 `D:/aicoding/papers`、`paper_sources`、`original_paper_reruns`、`IIA_benchmark` 的相关目录。

在这些范围内，未确认除上述 8 篇之外的新增独立作者主稿。`IIA_benchmark/ara/PAPER.md` 描述工业报警研究基准，其 `paper_exact` 文件是按作者年份命名的文献复现配置；不应把它们当作我们的新增独立论文。`papers/planning/2026_six_paper_portfolio.md` 是闽投六篇的早期设想，不是另外六篇。

这不是全磁盘搜索。归属不明的材料和仓库外未知稿件未擅自搬迁；不能声称已经整理所有磁盘中的所有论文。

## 使用与恢复注意

1. 从 `paper_projects/README.md` 进入各缩写项目。历史联接仅为归类入口，不改变来源材料的证据状态。
2. 不对 Junction 做递归清理；本任务没有设置清理作业。跨电脑使用时，根据 `catalog.json` 与 `completed.json` 验证路径后重建入口。
3. 本次没有提交、推送或重置 Git。后续提交迁移前，应审查新旧目录的索引策略，避免同时提交兼容路径和实体路径，尤其不要未经检查执行 `git add .`。
4. `organize_paper_projects.ps1` 是一次性迁移脚本；遇到既有目标会拒绝重复执行。部分失败时查看 `completed.json` 后人工按精确路径恢复，不要强制重跑。
5. 不重新运行昂贵实验，不更新冻结结果清单以伪装成新实验；仅做路径、内容完整性与适度运行检查。

## 最终验证

| 检查 | 结果 |
|---|---|
| 迁移原文件完整 SHA-256 | 3,041 个全部一致 |
| 旧路径永久联接 | 14 个有效 |
| 明确归属历史目录入口 | 88 个有效 |
| 分类历史素材（目录或独立文件） | 254 项，原址仍存在 |
| 各篇 LaTeX、PDF、状态入口 | 24 个均存在 |
| Git 工作树路径 | 主工作树与 17 个关联工作树均存在 |
| 基础 pytest | 5 passed（config_loader、metrics、applsci_preflight） |
| C2GES 公开验证 | `--check --route diagnostic --skip-latex`：PASS，non_mutating=true，0 failures |

结构化验证：`verification.json`。本次未重新编译 LaTeX；正文、PDF、图表及全部迁移原文件的内容哈希保持不变。未执行新实验，也不把目录校验解释为论文科学质量或投稿签核通过。

## 下次恢复入口

先读 `paper_projects/README.md`，再读指定论文的 `PROJECT_INDEX.md`。机器身份映射为 `catalog.json`，精确实体移动记录为 `completed.json`。不要再次执行实体迁移；如需复核，仅运行 `py -3.12 -X utf8 scripts/papers/verify_project_organization.py`。
