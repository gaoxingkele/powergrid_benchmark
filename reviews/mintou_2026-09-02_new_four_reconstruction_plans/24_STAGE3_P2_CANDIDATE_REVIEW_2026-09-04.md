# P2 Stage-3 候选评审（p2_v2_s03_method_task_implementation_contract）

**日期：** 2026-09-04
**候选分支：** `paper-harness/mintou_p6_bilonsga_project_review/v2-p2_v2_s03_method_task_implementation_contract`
**评审基准：** 14 号契约 + 08 号执行计划 §4 + 17 号质量门
**结论：** **建议接受，无必改项**。四篇 s03 至此全部评审完成。

## 一、对照 14 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §2.1 成本校准（方案 A/B 或 NO-GO） | 合成成本公式化：`fixed_units + variable_units × 增量/长度`，系数为**配置输入而非实现编造**；"Synthetic benchmark units" 标签保留直至外部校准 | ✅ 务实路径，校准证据留待注册表冻结 |
| §2.2 第二任务族 | 定义两个 action-aligned 任务族构建器：`rts_transmission_reinforcement`（分支评级增量）与 `simbench_feeder_reinforcement`（馈线评级增量）——比 MTEP16 回测更强（动作级）；族间独立性条款完整（独立快照/种子/预算/命名空间，禁止无注册估计量池化） | ✅ 语义完备 |
| §2.2 输入注册表 | **NO-GO 记录在案**：正式执行需冻结源行 SHA-256、增量、成本系数出处、族预算——与 P3 的 action registry 同源的数据工作 | ✅ 诚实记录，GO 路径明确 |
| §2.3 精确参照（s04 项） | EXPERIMENT_PROTOCOL 预留 | ✅ 前移合理 |
| 原子替换语义 | 独立门控、先删后插、**接受或回滚**、无删除中间态被评估或保留——与 legacy"定义一次 delete-insert 提案"一致 | ✅ |
| 负结果保留 | 档案未动；无新数值；forward/backward/NDS 四臂语法与 legacy 结论对应 | ✅ |

## 二、候选技术质量

- 方法语义精确：违反量定义统一、修复确定性平局（ascending action_id）、move 语法（backward_only ≠ 静默替换）、严格接受、重复缓存与唯一评估计数、终止条件。
- 8 项实现测试全过；验收门全过；未动 `journal_submission/paper.tex`（无转义缺陷风险）；MiKTeX 未完成安装 → 未声称 TeX 构建成功（诚实披露）。
- 摘要 183 词（≤220 门槛；18 号 R1 的 172 词压缩版仍作为 Stage-7 选项）。

## 三、跨篇信号（重要）

P2 与 P3 的 s03 出现**同源阻塞**：action-aligned 注册表（源行绑定 + 增量 + 成本出处）在 legacy 档案中不存在，正式执行均 NO-GO 待真实源数据。这验证了 12 号评分报告的判断——P1/P2/P3 的共同缺口不是实验执行，而是"代理 → 动作/成本"的绑定数据。两条路：
- **投入构建注册表**（RTS-GMLC/SimBench 公开数据可支持）→ action-aligned 路线续行；
- **不构建** → P2 走 14 号契约 §7 框架/审计叙事 + PLS 优势；P3 走 15 号契约 §7 决策门。

## 四、建议

1. **接受** `p2_v2_s03_method_task_implementation_contract`；
2. 四篇 s03 全部完成后，进入 **s04 冻结实验协议** 阶段（P1 → P3 → P4 → P2 资源顺序），s04 启动前需作者答复注册表可行性（P2/P3 共用同一答复）。

## 五、作者决策记录（2026-09-05）

作者答复：**action registry 可以构建**。→ P3/P2 的 action-aligned 路线续行（Energies 路线保持）；s04 冻结协议将包含注册表 schema 与源数据要求，实际数据物化在 s06 正式执行前完成。
