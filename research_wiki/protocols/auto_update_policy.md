# Auto Update Policy

## Trigger

每一步交互后判断是否有写入价值。满足任一条件时更新 `research_wiki/`：

1. 新增或下载数据集。
2. 新发现论文、文章、benchmark、数据门户或算法思想。
3. 修正项目方法论、目录结构、任务分类或 baseline 策略。
4. 发现复现阻塞、路径问题、数据缺失或证据缺口。
5. 用户明确要求记录过程、思考、方法论或论文思想。

## Update Targets

- 每轮日志：`logs/YYYY-MM-DD.md`
- 方法论变化：`methodology/evolution_path.md`
- 论文思想：`paper_ideas/*.md`
- 概念沉淀：`concepts/*.md`
- 自动化协议变化：`protocols/*.md`

## Log Entry Template

```markdown
## HH:MM - Short Title

- Observation:
- Action:
- Rationale Summary:
- Evidence:
- Impact on Methodology:
- Next:
```

## Automation

使用脚本创建或追加日志：

```powershell
python scripts/wiki/log_research_event.py --title "event title" --observation "..." --action "..." --rationale "..." --evidence "..." --impact "..." --next "..."
```

后续每轮任务结束前，应执行：

1. 判断本轮是否有新增研究价值。
2. 有价值则写入 `research_wiki/`。
3. 如果新增数据/论文，也同步更新 `knowledge_base/`。
