# Knowledge Base Update Protocol

## 每轮更新

1. 在 `updates/decision_log/YYYY-MM-DD.md` 记录本轮做出的结构性决定。
2. 在 `updates/rationale_summary/YYYY-MM-DD.md` 记录可审计依据摘要。
3. 在 `updates/paper_updates/YYYY-MM-DD.md` 记录新增论文、数据集和任务映射。
4. 在 `updates/open_questions/YYYY-MM-DD.md` 记录仍需人工确认的问题。
5. 如果新增数据集，同步更新 `data/public_datasets/manifests/public_dataset_manifest.csv`。

## 数据集进入标准

- 必须有公开来源链接或明确的申请/API 入口。
- 必须有本地缓存路径或 metadata-only 路径。
- 必须说明适用任务、访问方式、体量风险和许可证/使用限制。
- 全量数据超过 1 GB、需要 token 或有注册门槛时，默认只保存元数据和脚本入口。

## 文献进入标准

- 近三年优先，即 2024-2026。
- 优先 IEEE Transactions、IEEE OAJPE、Nature/Scientific Data、Elsevier/Applied Energy/Energy AI、ACM/CCF/NeurIPS/ICLR/AAAI/IJCAI 等高质量来源。
- 必须绑定任务、数据集、方法类别和可复现实验线索。

## 隐私与推理记录

本项目不保存隐藏思维链。需要长期保存的内容使用：

- `decision_log`: 决策结果。
- `rationale_summary`: 可审计依据摘要。
- `open_questions`: 尚未解决的问题。
- `paper_updates`: 文献和证据更新。
