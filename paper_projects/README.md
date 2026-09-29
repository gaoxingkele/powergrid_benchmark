# Paper Projects

## 论文项目入口（2026-09-12）

按论文缩写进入项目，不再从期刊名或交付日期判断最新稿。实体迁移及历史材料入口见下表；旧目录是兼容联接，不是另一份可独立修改的论文。

| 原编号 | 项目缩写 | 总入口 |
|---|---|---|
| 闽投 P1 | GRU-LSR | [项目索引](GRU-LSR/PROJECT_INDEX.md) |
| 闽投 P2 | CSA-LoadNet | [项目索引](CSA-LoadNet/PROJECT_INDEX.md) |
| 闽投 P3 | CARS-MODE | [项目索引](CARS-MODE/PROJECT_INDEX.md) |
| 闽投 P4 | SHIELD-MOEA | [项目索引](SHIELD-MOEA/PROJECT_INDEX.md) |
| 闽投 P5 | TRACE-MOEA | [项目索引](TRACE-MOEA/PROJECT_INDEX.md) |
| 闽投 P6 | BiLo-NSGA | [项目索引](BiLo-NSGA/PROJECT_INDEX.md) |
| 原 CMC | C2GES | [项目索引](C2GES/PROJECT_INDEX.md) |
| 原 CMC | MA-SQLGrid | [项目索引](MA-SQLGrid/PROJECT_INDEX.md) |

闽投项目中，`manuscript/` 是现有正文与图表，`ARA/` 汇集此前分离的逻辑、数据证据与代码，项目原有 `experiments/`、`evidence/`、`checkpoints/` 等完整保留。CMC 项目的现行材料在各自 `Workspace/` 下，维持原有相对层级以保护复现入口。两类项目均用 `90_History_Links/` 和 `PROJECT_INDEX.md` 归类散落历史。

公共数据、共享实现、跨篇交付包和 Git 工作树不拆分或复制。独立投稿包仍使用相应论文的发布脚本；不要递归打包历史联接。联接不跨机器自动生效，其原始目标记录在 [机器可读清单](../docs/migration/paper_organization_20260912/catalog.json)。

其他项目核查范围及迁移校验见 [归类报告](../docs/migration/paper_organization_20260912/REPORT.md)。未确认独立作者主稿的研究基准、下载论文和论文设想不混入这 8 篇。

## 历史建项目说明（保留）

One directory per paper that needs implementation, reproduction, or GitHub integration work.

Start by copying `_template/` to:

```text
paper_projects/YYYY_short_title_author/
```

The matching ARA package should live at:

```text
ara_artifacts/YYYY_short_title_author/
```
