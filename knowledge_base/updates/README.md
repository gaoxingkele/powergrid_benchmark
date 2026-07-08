# Update Streams

本目录保存每轮知识库更新记录。

- `decision_log/`: 本轮做出的结构性决定。
- `rationale_summary/`: 可审计依据摘要。
- `paper_updates/`: 新增或修订的论文/数据集/证据。
- `open_questions/`: 需要后续确认的问题。

使用脚本生成当天模板：

```powershell
python scripts/knowledge_base/new_update_round.py
```

可指定日期：

```powershell
python scripts/knowledge_base/new_update_round.py --date 2026-07-06
```
