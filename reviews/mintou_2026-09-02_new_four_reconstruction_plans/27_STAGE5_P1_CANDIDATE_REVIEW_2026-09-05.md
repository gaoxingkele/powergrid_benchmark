# P1 Stage-5 候选评审（p1_v2_s05_pilot_activation_gate）

**日期：** 2026-09-05
**候选分支：** `paper-harness/mintou_p5_trace_moea_feasibility_review/v2-p1_v2_s05_pilot_activation_gate`
**评审基准：** 13 号契约 §6 + 08 号执行计划 §3.5
**结论：** **建议接受**（pilot 门按设计工作：机械检查通过、结果禁入论文、阻塞项如实记录）

## 一、pilot 门核验

| 检查项 | 结果 |
|---|---|
| 试运行规模 | Full TRACE + NSGA-II × 3 配对种子（6 单元），每单元精确 3,200 目标调用 | ✅ |
| 重放/预算可行性/哈希/schema/指标方向 | 全过 | ✅ |
| paper_use: false | ✅ 结果未解释、未晋升 |
| 验收命令（--phase pilot） | pass | ✅ |

## 二、正式执行阻塞项（fail-closed 记录，s06 前必须解决）

1. **环境漂移**：NumPy/SciPy 与 s04 冻结的 environment.json 不一致。处置：重冻结（钉扎实际安装版本并更新 environment.json，或安装冻结版本）——机械修复，可执行。
2. **NERC 元数据再分发**：代理池属性源自 NERC 公开文档元数据；NERC 法律政策不授予再分发权。处置选项（需用户决定）：
   - **A**：用开放许可来源（RTS-GMLC CC-BY / SimBench 开放数据）重新推导相关属性，替换 NERC 派生属性；
   - **B**：记录 NO-GO，仅保留 URL 引用、不派生再分发（代理池相关属性移除或降级）；
   - **C**：取得书面许可（时间成本高）。

## 三、推进计划

- accept 后 P1 停在 s06 前，等待 §二 两项处置；
- P4 的 s05 pilot 可启动（其阻塞：Ausgrid 源哈希/许可证据/runner/资源批准——执行器会按 fail-closed 判定）；
- P3/P2 s04 仍等待 action registry 答复。

## 四、建议

1. **接受** `p1_v2_s05_pilot_activation_gate`；
2. 用户答复 NERC 属性处置（A/B/C）；环境钉扎由 s06 阶段执行器按重冻结要求处理；
3. 启动 **P4 的 s05**（`p4_v2_s05_pilot_activation_gate`）。

## 五、作者决策记录（2026-09-05）

- **P1 s05 已接受**（`d3d57694`）。
- **NERC 属性处置：选 A**——用开放许可来源（RTS-GMLC CC-BY / SimBench 开放数据）重新推导相关属性，替换 NERC 派生属性。s06 正式执行前完成，替换过程与出处记录进 data_manifest。
