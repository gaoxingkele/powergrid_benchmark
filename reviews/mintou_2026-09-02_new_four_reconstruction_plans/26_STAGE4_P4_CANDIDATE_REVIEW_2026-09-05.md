# P4 Stage-4 候选评审（p4_v2_s04_frozen_experiment_protocol）

**日期：** 2026-09-05
**候选分支：** `paper-harness/mintou_p2_hygraph_load_forecasting/v2-p4_v2_s04_frozen_experiment_protocol`
**评审基准：** 16 号契约 §4–§6 + 08 号执行计划 §5
**结论：** **建议接受，无必改项**

## 一、对照 16 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §4 Hier/Dense 条件 | Ausgrid solar-home 层级 = Hier；OPSD 六国负荷 = Dense；data_manifest 为节点序/列/层级成员/边规则/源哈希的唯一权威 | ✅ |
| §5 主指标预注册 | 主指标 = 块级 WAPE（Ausgrid 叶/区域/根等权池化；OPSD 六节点池化） | ✅ |
| §6 消融正交表 | HGCN-Fixed1-Real（主臂）、HGCN-Learnable-Real、EuclideanGCN-Real（匹配）、Identity/Random 图消融格；DiD 对比固定曲率 HGCN vs 欧式 GCN | ✅ |
| §2 baseline 补全 | **Persistence 已入表**（确定性朴素基线）；CSA-LoadNet 重跑且"never called GCN/HGCN" | ✅ |
| rolling-origin 统计单位 | 3 个开发块（调参）与 8 个后续正式块不相交；块内 3 种子平均后取中位数 WAPE 为调参判据；正式评估用配对种子 {11,23,47,59,71}；开发种子/块禁止进入正式表 | ✅ |
| 资源报告 | 推理秒数、峰值主存/CUDA 显存、loss/梯度/状态计数、投影/切向裁剪计数、曲率统计 | ✅ |
| pilot 门 | pilot 只可确认可行性或触发 no-go，不得修改协议 | ✅ |
| 边界 | 正式执行仍被 Ausgrid 原始哈希、许可证据、处理数据哈希、runner、pilot、资源批准阻塞（未跑实验，正确） | ✅ |

## 二、候选质量

- 协议验收门（--phase protocol）+ Stage-3 合成不变量（NO_RESULTS）+ JSON/算术/种子不相交/必需文件检查全过；受保护前身未改动。
- 未动 `journal_submission/paper.tex`。

## 三、推进计划

- **P4**：accept 后完成 s04；s05 pilot 待数据哈希/runner 就绪。
- **P1**：s04 已接受；s05 pilot 门可尝试启动（若数据未物化，执行器将按 fail-closed 记录 BLOCKED 原因）。
- **P3 / P2**：s04 仍被 action registry 阻塞，等待用户答复。

## 四、建议

1. **接受** `p4_v2_s04_frozen_experiment_protocol`；
2. 接受后尝试启动 **P1 的 s05**（`p1_v2_s05_pilot_activation_gate`），由执行器判定数据就绪状态。
