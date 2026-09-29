# P1 Stage-4 候选评审（p1_v2_s04_frozen_experiment_protocol）

**日期：** 2026-09-05
**候选分支：** `paper-harness/mintou_p5_trace_moea_feasibility_review/v2-p1_v2_s04_frozen_experiment_protocol`
**评审基准：** 13 号契约 §3/§4/§5 + 08 号执行计划 §5
**结论：** **建议接受，无必改项**

## 一、对照 13 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §3 调参与评估分离 | 4 个开发场景 × 10 种子（仅调参，640 运行 / 2,048,000 目标调用）与 3 个确认场景 × 30 配对种子（2,016,000 调用）**完全不相交**；开发场景/种子/试运行行/legacy 结果禁止进入确认分析与结果表；首个确认目标值可见后冻结一切方法配置 | ✅ |
| §3 公平调参 | 4 方法 × 4 配置网格，判据 = 中位数主指标；tuning freeze 条款防单方法偏调 | ✅ |
| §4 H-Pref 先验条件 | 偏好强度标签由**冻结的场景权重向量**计算（先验于结果） | ✅ |
| §5 主指标预注册 | 主指标 = 五维可行前沿 HV；次指标含 legacy clipped HV@1.1、可行前沿比例、预算利用率、成本指数、**工程换算表（入选数差/预算利用率差）** | ✅ |
| 统计协议 | 配对差异估计量（Full TRACE vs 6 个随机对手 × 3 确认场景），家族内 Holm α=0.05，原始 + 校正 + 配对 bootstrap CI；场景平衡池化与次指标仅描述性、不得替代失败的主分析 | ✅ |
| 负结果政策 | 独立 Failure and Negative-Result Policy 章节；>5% 单元格失败触发处置 | ✅ |
| 08 计划 §5 五件套 | config/data_manifest/environment/RUNBOOK/planned_vs_executed 全部产出 | ✅ |
| 边界 | 正式执行仍被数据哈希物化 + 许可核验 + pilot 验证阻塞（未跑实验，正确） | ✅ |

## 二、候选质量

- 未动 `journal_submission/paper.tex`；DEEP_REVISION_EVIDENCE 更新保留全部历史负结果标题。
- 协议验收门（--phase protocol）+ 方法契约一致性 + JSON schema + `git diff --check` 全过。

## 三、s04 阶段推进计划（供用户确认）

- **P1**：本候选 accept 后即完成 s04，下一步 s05 pilot 门。
- **P4**：s04 无注册表依赖 → 可立即启动。
- **P3 / P2**：s04 均被 action registry 数据阻塞 → 需用户答复注册表可行性后才能启动（插队等待）。

## 四、建议

1. **接受** `p1_v2_s04_frozen_experiment_protocol`；
2. 接受后启动 **P4 的 s04**（`p4_v2_s04_frozen_experiment_protocol`）；
3. P3/P2 的 s04 等待注册表答复。
