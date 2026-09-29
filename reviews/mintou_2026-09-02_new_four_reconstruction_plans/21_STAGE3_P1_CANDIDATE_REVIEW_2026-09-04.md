# P1 Stage-3 候选评审（p1_v2_s03_method_data_implementation_contract）

**日期：** 2026-09-04
**候选分支：** `paper-harness/mintou_p5_trace_moea_feasibility_review/v2-p1_v2_s03_method_data_implementation_contract`
**评审基准：** 13 号契约（P1 实验设计契约）+ 17 号质量门 + 12 号评分报告阻塞项
**结论：** **建议接受（附 1 处必改项，accept 合并后立即修复）**

## 一、对照 13 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §2.1 成本校准 NO-GO 判定待定 | `METHOD_DATA_IMPLEMENTATION_CONTRACT.md`：**NO-GO**（无来源级许可记录、无候选-成本映射、无货币/基年变换） | ✅ 判定落定，理由充分 |
| §2.2 AC 后验 NO-GO（本阶段） | **NO-GO**（组合位是原型代理，非母线/线路/发电机/拓扑/调度动作） | ✅ 与契约预判一致 |
| §2.3 MTEP16 描述性限定 | **GO, DESCRIPTIVE ONLY**（保留 source reuse、标签不平衡、组合依赖局限） | ✅ |
| §2.4 事件记录语义 | 明确"计数与池位共现 ≠ lineage/replay"，8×40 事件不变量写入契约 | ✅ |
| §3 公平调参（s04 项） | EXPERIMENT_PROTOCOL.md +16 行预对齐 | ✅ 前移合理，s04 冻结时细化 |
| 主张边界 | 摘要/结论无升级；新增 NO-GO 声明句加强 claim 边界 | ✅ |
| 负结果保留 | 历史配置与结果未改动；0.89%/0.17%/归一化反转条款未触碰 | ✅ |

## 二、候选技术质量

- **方法契约文档**：目标/单位/预算、修复与平局规则、双重归一化分离（代际局部 vs 报告超体积）、偏好注入、评估记账（n_eval 未存档 → 明示"非等调用预算证据"）、事件语义、规范伪代码、跨产物一致性表、可执行校验器——这正是 s03 目标要求的"消除公式/伪代码/配置/代码漂移"。
- **验收检查全过**：narrative_structure（摘要 160 词 ≤220）、artifact_consistency（8 图引用、50 标签唯一）、manuscript_hygiene、literature 自定义门、`git diff --check`。
- **诚实声明**：PDF 未能重编译（MiKTeX 在隔离环境未初始化），执行器明确"不声称 TeX 构建成功"——与本阶段验收清单（不含 latex_build）一致，风险移交 s04 之后的构建门。

## 三、发现的缺陷（1 处，必改）

`paper.tex` 约第 169 行新增句末：

```latex
The complete decision record is 	exttt{reconstruction_v2/METHOD_DATA_IMPLEMENTATION_CONTRACT.md}.
```

`\texttt` 被写成了制表符 + `exttt{`，LaTeX 将渲染为字面 "exttt{...}" 文本。应改为：

```latex
The complete decision record is \texttt{reconstruction\_v2/METHOD\_DATA\_IMPLEMENTATION\_CONTRACT.md}.
```

**处置方案：** accept 合并后，在 main 上以一行修复提交立即改正（不触发 retry，避免为单字符缺陷重跑整个 codex 阶段）。

## 四、建议

1. **接受** `p1_v2_s03_method_data_implementation_contract`；
2. 合并后立即应用 §三 的一行修复（提交 `fix(p1): repair \texttt in stage-3 NO-GO sentence`）；
3. 随后按资源顺序启动 **P3** 的 `p3_v2_s03_action_method_implementation_contract`（15 号契约已注入其项目输入）。
