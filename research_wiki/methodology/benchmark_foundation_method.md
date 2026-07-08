# Benchmark Foundation Method

## Principle

电网 + 计算机 benchmark 的可信度来自三层一致性：

1. 数据集真实可得。
2. 任务定义稳定。
3. baseline 对比充分。

## Dataset Layer

数据源进入项目时先分层：

- source layer: 原始公开数据、报告、网架、时序、仿真环境。
- processing layer: 清洗、切分、字段标准化、文本抽取。
- label layer: 分类标签、证据句 ID、问题、答案、split。
- experiment layer: baseline 输入输出、指标、日志。

C2GES 的 NERC PDF 下载强化了这个分层：source layer 可以公开缓存，但 label layer 仍需恢复或重建。

## Task Layer

每个任务必须能回答：

- 输入是什么？
- 输出是什么？
- 评价指标是什么？
- 哪些 baseline 是最低要求？
- 是否有安全/可行性约束？

## Baseline Layer

baseline 不只是“对比方法”，而是论文可信度约束。

- 预测任务必须有 persistence/seasonal naive。
- OPF/PF 必须有物理求解器或 DC/AC baseline。
- 安全筛选必须关注 unsafe recall。
- 文本证据检索必须区分 lexical、semantic、position、centrality 和 task-aware reranking。

## Evidence Rule

任何论文思想进入项目时，都要落成：

```text
Paper Idea -> Dataset -> Task -> Baseline -> Evidence Gap -> Next Experiment
```
