# C2GES Logic

## Core Idea

C2GES 把电网可靠性报告分析从普通文本摘要推进到 causal-role evidence selection：模型不是生成摘要，而是根据 causal role question 找到支持该角色的证据句 ID。

## Dataset Logic

C2GES 的数据集分两层：

- source layer: public NERC reliability/event reports。
- label layer: sentence segmentation、5 类 causal-role questions、evidence sentence IDs。

当前已恢复并缓存 source layer：40 个 NERC 官方 PDF。

当前缺口：上传包没有 `verification_pilot/agent_audit_40doc/`，因此缺失 label layer。

## Task Logic

输入：

- NERC 报告文本
- causal role
- role-conditioned question

输出：

- top-K evidence sentence IDs

核心指标：

- evidence precision
- evidence recall
- evidence F1
- selected evidence ROUGE-L

## Method Logic

C2GES 的方法思想是把普通 query relevance 拆成三类信号：

- query relevance
- role compatibility
- local causal-chain consistency

重要启发：在电网事件文本中，同一段话可能主题相关，但 causal role 不同。role-aware retrieval 比 generic retrieval 更贴近工程审查。

## Baseline Logic

C2GES 的 baseline 结构对后续 NLP benchmark 有复用价值：

- lead-k / positional
- TF-IDF query retrieval
- TF-IDF centroid
- TextRank / LexRank
- causal cue ranker
- SBERT query retrieval
- BM25 supplement

## Evidence Gap

公开 PDF 不等于完整实验数据集。需要补：

- PDF 文本抽取
- 句子切分
- question 生成或恢复
- evidence sentence ID 标注或恢复
- split 和 manifest

## Reusable Value

C2GES 可以作为“电网报告 NLP benchmark”的起点，用来支撑：

- reliability report evidence retrieval
- causal role labeling
- report-grounded QA
- event analysis assistant
- post-event review evidence tracing
