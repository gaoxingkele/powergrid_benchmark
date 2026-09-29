# P3 Stage-3 候选评审（p3_v2_s03_action_method_implementation_contract）

**日期：** 2026-09-04
**候选分支：** `paper-harness/mintou_p3_samode_distribution_planning/v2-p3_v2_s03_action_method_implementation_contract`
**评审基准：** 15 号契约 + 08 号执行计划 §4 + 17 号质量门
**结论：** **建议接受**（无 tex 改动、无需后续修复；附一条战略级提醒）

## 一、对照 15 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §2.1 2×2 四臂拆分（红线 1） | `scripts/p3_s03_method_contract.py`：独立 parameter/strategy 门、F/CR 随个体遗传、独立哈希随机流、四臂共享初始化/解码/修复/种子；legacy 联合开关经 `from_legacy(bool)` 兼容映射（明示"保持配置语义，非数值等价"） | ✅ 完成 |
| §2.2 action-aligned AC 映射（红线 2） | **NO-GO（本阶段）**：legacy `subnet::kind` 无唯一网络元素绑定；case-specific stress 排名非一一映射；编造元素 ID/成本将违反证据契约。已定义完整 action registry schema + `validate_complete_registry` 门（未来 GO 的路径） | ✅ 预注册 NO-GO 路径落定 |
| §3 公平性（s04 项） | 评估记账 6 项计数（含 AC 尝试/失败）、等种子共享、变压器负载准则须预注册 | ✅ 前移合理 |
| 负结果保留 | MANUSCRIPT.md 局限新增第 9 条（前瞻代码 ≠ 结果证据）；结论中 FixedDE 领先、IGD+ 第 5、NoDER 全部原样保留 | ✅ 范例级 |
| 验收检查 | 10 项单测全过；narrative/artifact/hygiene/literature 门全过；无新结果声明 | ✅ |

## 二、候选技术质量

- 四臂契约精确到"开关策略门不得消耗参数流"级别；联合对比被禁止用于单门归因——与契约的因果识别要求完全一致。
- AC NO-GO 的理由充分且可审计（不是偷懒，而是"不编造数据"原则的正确执行）。
- 候选未改动 `journal_submission/paper.tex`（无 P1 式转义缺陷风险）。

## 三、战略级提醒（接受前须知）

08 号执行计划 §4 对 P3 的硬条件：**"若动作映射与端到端 AC 不能成立，锁定标题下的 Energies 路线判为 NO-GO。"**

本次 s03 的 NO-GO 判定针对 **legacy 档案**。路线是否 NO-GO 取决于 s04 能否构建**全新 action registry**（SimBench 公共网络的母线/线路/变压器绑定 + 容量增量 + 成本出处）：
- **可构建** → AC GO 路径续行，四臂 + AC 验证照常；
- **不可构建**（无网络工程数据投入）→ 提前触发 15 号契约 §7 决策门：标题豁免或改投 Algorithms/Applied Sciences 的"可复现审计工作流"定位。

**建议作者现在就答复：是否有能力在 s04 前构建 SimBench 节点级 action registry？** 这决定 P3 的 Energies 路线是否继续，宜在 s04 启动前明确，避免烧掉四臂实验预算后才发现路线不通。

## 四、建议

1. **接受** `p3_v2_s03_action_method_implementation_contract`；
2. 作者答复 action registry 可行性（§三）；
3. 随后按资源顺序启动 **P4** 的 `p4_v2_s03_graph_data_model_implementation_contract`。
