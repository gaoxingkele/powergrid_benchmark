# 闽投六篇论文 Harness

本目录是闽投六篇论文的当前流程入口，不复制正文、实验或数据。权威文件仍在
`paper_projects/mintou_p*`、`papers/mintou/mintou_p*/evidence`、`reviews/` 和
`deliverables/`；`profile.json` 只记录它们之间的依赖、门禁和校验哈希。

## 使用

在工作区根目录运行：

```powershell
./papers/mintou/harness/run.ps1 check
./papers/mintou/harness/run.ps1 status
./papers/mintou/harness/run.ps1 plan
./papers/mintou/harness/run.ps1 run-stage -Stage experiment_freeze_preflight
./papers/mintou/harness/run.ps1 run-stage -Stage experiment_freeze_preflight -Execute
```

最后一条只会执行已标为 `auto_safe` 的统计单元测试。实验重跑、PDF 重建和 ZIP
重打包均只显示命令，不会自动执行。

## 当前边界

- 科学内容、三轮评审和六个完整 ZIP 已完成并由配置中的哈希约束。
- `submission_admin` 仍是人工门禁，不能由脚本替代作者确认。
- 如果正文或证据发生有意修改，应新建发布目录、重做统计/图表/评审/QA，并更新
  profile；不得直接把旧 ZIP 的哈希改成新值而缺少变更记录。

完整流程回顾见 [WORKFLOW_RETROSPECTIVE.md](WORKFLOW_RETROSPECTIVE.md)。

## 新版 Paper Harness 接入

当前执行器位于 `D:/aicoding/Lib/paper_harness`。本目录保存论文组合层面的画像与
流程回顾；六篇论文分别维护自己的 `.paper_harness` 状态库、计划摘要、人工批准、
worktree 分支和证据时间线。

通用 Harness 检查之外，闽投项目增加两个确定性钩子：

- `scripts/mintou/harness_scientific_acceptance.py` 检查逐篇的主张—证据合同、伴随
  论文披露、证据树和 12 项共享实验回归测试；
- `scripts/mintou/harness_acceptance.py` 只重建指定论文的期刊规范 LaTeX/PDF，最终
  门禁会拒绝未解决的作者和基金占位符。

P3/P4 与 P5/P6 分别共享实验基础设施。共享代码发生变化时必须同时回归伴随论文，
但不得借此在两篇稿件中重复宣称同一项独立贡献。

Hard Gate 不可绕过：注册计划不等于授权执行。作者必须先核对完整计划及 SHA-256，
再运行 `approve`。
