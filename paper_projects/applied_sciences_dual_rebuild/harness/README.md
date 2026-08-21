# C²GES / MA-SQLGrid Applied Sciences Harness

本目录将两篇论文的写作、实验和发布流程绑定到唯一的当前版本。它不复制论文资产，
只保存配置、状态、门禁、命令入口和固定哈希。

## 当前权威版本

`formal_submission_reference_revision_20260809/` 是当前发布根；其中 C²GES 为 25 页、
6 幅图，MA-SQLGrid 为 28 页、6 幅图。`_archive_pre_current_audit/` 仅供追溯，不能
用于当前正文、Visual QA 或投稿包。

## 使用

在工作区根目录运行：

```powershell
./paper_projects/applied_sciences_dual_rebuild/harness/run.ps1 check
./paper_projects/applied_sciences_dual_rebuild/harness/run.ps1 status
./paper_projects/applied_sciences_dual_rebuild/harness/run.ps1 plan
./paper_projects/applied_sciences_dual_rebuild/harness/run.ps1 run-stage -Stage registry_integrity_preflight -Execute
```

最后一条仅运行 planning artifact 的只读验证。BIRD 正式运行、图表重建、release manifest
重写、邮件和投稿均不会自动执行。

完整流程和版本/事故边界见 [WORKFLOW_RETROSPECTIVE.md](WORKFLOW_RETROSPECTIVE.md)。

