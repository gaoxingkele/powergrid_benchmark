# Methodology Evolution Path

## v0.1: Paper Workspace Organization

起点是把每篇论文作为独立工程目录处理，避免上传 zip、源码、PDF、实验输出混在一起。

形成规则：

- 一篇论文一个 `paper_projects/<paper_id>/`。
- 一篇论文一个 `ara_artifacts/<paper_id>/`。
- 论文源码、调试日志、复现计划分层保存。

## v0.2: ARA-First Reproducibility

项目采用 ARA 工程化模式，把论文贡献拆成：

- claims
- evidence
- experiments
- source environment
- trace

这一阶段的核心认知：论文不是 PDF，而是可追踪证据包。

## v0.3: Public Dataset Foundation

用户强调“数据集和经典算法任务是整个项目的基石”。因此方法论从单篇论文复现升级为全局 benchmark 地基建设。

形成规则：

- 先建公共数据集池。
- 按任务分类数据集。
- 为每类任务绑定 baseline。
- 区分 downloaded、metadata-only、API-ready、TB-scale。

## v0.4: Source Layer vs Label Layer

C2GES 暴露了一个重要模式：公开原始数据和论文实验标签不是一回事。

例子：

- NERC 官方 PDF 是 source layer，公开可下载。
- C2GES 的 sentence ID、causal-role question、evidence labels 是 label layer，上传包未提供。

形成规则：

- 下载到公共池时必须说明层级。
- 不把公开源文档误称为完整实验数据集。
- 缺失标签要作为复现阻塞明确记录。

## v0.5: Research Wiki as Method Memory

当前阶段引入独立 `research_wiki/`，把每轮有价值的思考转成可审计方法记忆。

形成规则：

- `knowledge_base/` 管事实。
- `research_wiki/` 管方法演化和思想抽象。
- 每轮交互后判断是否需要写 wiki。
- 下载论文/文章/数据集后提取核心思想价值。
