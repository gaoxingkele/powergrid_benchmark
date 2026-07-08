# Powergrid Benchmark Research Wiki

## Project Thesis

本项目的核心不是堆论文或堆数据，而是建立一个可持续演化的电网 + 计算机 benchmark 研究系统。每篇论文、每个数据集、每次调试都应沉淀到同一个研究记忆结构中：

1. 数据集是实验地基。
2. 任务分类是实验边界。
3. baseline 是论文可信度底线。
4. ARA 工程包是单篇论文可复现载体。
5. wiki 日志是方法论进化轨迹。

## Wiki Map

| 模块 | 作用 |
| --- | --- |
| `methodology/` | 记录 benchmark 建设和论文工程化的方法论演化 |
| `paper_ideas/` | 抽象每篇论文/数据源带来的思想价值 |
| `concepts/` | 保存可复用概念、术语、任务范式 |
| `logs/` | 每轮交互后的可审计思考摘要和行动日志 |
| `protocols/` | 规定何时自动更新 wiki、写什么、不写什么 |

## Current Method Version

`v0.3`: 从“论文工程复现”升级为“公共数据集池 + 任务分类 + ARA + 思想日志”的全局 benchmark 系统。

## Active Research Axes

1. 电网运行优化与 OPF/PF benchmark。
2. 电网可靠性文本证据检索与 causal-role evidence selection。
3. Grid database/text-to-SQL 类结构化电网知识问答。
4. 负荷/风光/市场时序预测。
5. 设备故障、DGA、PMU 事件识别。
