# P3 Stage-4 候选评审（p3_v2_s04_frozen_experiment_protocol）

**日期：** 2026-09-05
**候选分支：** `paper-harness/mintou_p3_samode_distribution_planning/v2-p3_v2_s04_frozen_experiment_protocol`
**评审基准：** 15 号契约 §4–§6 + 08 号执行计划 §4
**结论：** **建议接受，无必改项**

## 一、对照 15 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §4 Rugged/Nominal 条件 | 固定配置面板：DER-excluded、load 1.3x、budget 0.82x / 1.20x（紧预算=rugged 档）；配置为固定面板、不接受有利调参 | ✅ |
| §2 2×2 四臂 | 四臂全冻结（Fixed-Fixed / AdaptiveParam-FixedStrategy / FixedParam-AdaptiveStrategy / Full），实现语义精确（F=0.5/CR=0.9、jDE 重采样 0.1、rand/1 固定策略、成功驱动池、可遗传控制、独立标注流）；估计量 = 两门主效应 + DiD 交互；Full vs Fixed-Fixed 仅作联合对比 | ✅ |
| §5 主指标预注册 | **unclipped analytic-normalized HV 为主**（15 号契约的关键改动——消除指标钓鱼面）；次指标 IGD+（共同归一化后的非支配并集）、前沿规模、可行比例 | ✅ |
| §3 公平性 | 等目标行预算；任何对照不得获得额外调用/动作信息/AC 结果；标注子流隔离初始化/参数/策略；共享后处理不计入；墙钟=出处非公平预算 | ✅ |
| §2 action registry | `action_registry.json` 每坐标一行、目标网络+母线+容量绑定、`validate_complete_registry`；空注册表 = 显式阻塞项而非零候选 | ✅ |
| 边界 | `BLOCKED_ACTION_AND_AC_PROVENANCE / NO_RESULTS`——与作者的 registry 构建计划一致（s06 前物化） | ✅ |

## 二、候选质量

- 10 项方法契约单测 + 协议不变量 + 必需文件 + 协议验收命令全过；未动 `journal_submission/paper.tex`；无新结果。

## 三、推进计划

- **P3**：accept 后完成 s04；s05 pilot 待 registry 数据物化。
- **P2**：s04 可启动（14 号契约已注入；registry 同源数据）。
- **P1**：s05 候选裁决 + NERC 处置仍挂起。

## 四、建议

1. **接受** `p3_v2_s04_frozen_experiment_protocol`；
2. 启动 **P2 的 s04**（`p2_v2_s04_frozen_experiment_protocol`）——四篇 s04 全部完成后，剩余阻塞统一在 s05/s06 前解决（registry 物化、环境钉扎、NERC 处置）。
