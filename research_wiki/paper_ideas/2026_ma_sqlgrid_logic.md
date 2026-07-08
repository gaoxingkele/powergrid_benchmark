# MA-SQLGrid Logic

## Core Idea

MA-SQLGrid 将电网维护数据库问答转化为 text-to-SQL / structured reasoning benchmark。它的价值不是电网物理仿真，而是把维护知识、设备表、故障记录和查询问题组织成可执行 SQL 任务。

## Dataset Logic

上传包自带完整本地数据集：

- SQLite database
- schema.sql
- questions.jsonl
- splits.json
- annotation protocol
- verification log

数据集位置：

`paper_projects/2026_ma_sqlgrid_cmc/source/data/griddb_maintenance_v2_v0_1`

## Task Logic

输入：

- natural-language maintenance question
- database schema
- optional domain context

输出：

- SQL query
- executable answer

核心指标：

- execution accuracy
- validator diagnostics
- condition-level comparison

## Method Logic

MA-SQLGrid 的可复用思想是把 prompt/context 条件分层比较：

- schema only
- full schema values
- generic SQL agent
- domain-context agent
- validated domain-context agent

这为后续电网数据库智能体提供了清晰 ablation 框架。

## Baseline Logic

该论文提醒项目：text-to-SQL 类任务不能只比较最终回答，还要比较：

- schema access
- value access
- domain context
- validator 修正
- query execution failure modes

## Evidence Gap

当前主要工程问题是路径包装：测试期望 `source/code/data/...`，实际数据在 `source/data/...`。

## Reusable Value

MA-SQLGrid 可作为结构化电网知识问答 benchmark 的种子，用来连接：

- 维护数据库
- SQL agent
- domain-specific validator
- ARA evidence trace
