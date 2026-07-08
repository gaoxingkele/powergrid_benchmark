# Thought Capture Policy

## What We Capture

本项目需要长期保存的是可复盘、可审计、可执行的研究思路，而不是隐藏推理原文。

可以写入 wiki 的内容：

- 本轮为什么做这个动作。
- 从失败中学到的约束。
- 数据集/论文/算法对项目方法论的影响。
- 新增假设、验证计划和开放问题。
- 方法论版本变化。
- 对论文贡献结构的抽象理解。

## What We Do Not Capture

不写入：

- 隐藏思维链逐字记录。
- 未经验证的臆测。
- 无来源支撑的论文结论。
- 可误导为专家标注或 gold label 的自动生成内容。

## Replacement Format

用户说“思维链”时，本项目统一落为以下可审计格式：

```text
Observation -> Decision -> Rationale Summary -> Evidence -> Next Check
```

示例：

```text
Observation: C2GES 上传包缺少 verification_pilot/agent_audit_40doc。
Decision: 先下载 40 个 NERC 官方 PDF，标记标签层缺失。
Rationale Summary: 源报告公开可得，但 evidence sentence labels 未公开随包提供。
Evidence: C2GES summary.json 中 40 个 nerc_* doc_id；NERC 官方页面 PDF URL。
Next Check: 是否从 PDF 重建 nerc_*.json 和 200 个 causal-role questions。
```
