# P2 Stage-4 候选评审（p2_v2_s04_frozen_experiment_protocol）

**日期：** 2026-09-05
**候选分支：** `paper-harness/mintou_p6_bilonsga_project_review/v2-p2_v2_s04_frozen_experiment_protocol`
**评审基准：** 14 号契约 §4–§6 + 08 号执行计划 §4
**结论：** **建议接受，附 2 项 s06 前必须完成的协议修订**（四篇 s04 至此全部评审完成）

## 一、对照 14 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §4 四臂正交矩阵 | nds_only / forward_only / backward_only / bidirectional + DiD 交互估计量；forward→backward 冻结顺序、深度上限 2/2、backward_only ≠ 原子替换 | ✅ |
| §3 基线族 | 冻结 nsga2 + 已披露 PLS；**拒绝**未经审计/公平调参的 NSGA-III/MOEA/D/精确参照入组（声明为局限而非弱者证据）——诚实地消除了"弱基线"攻击面 | ✅ |
| §5 双协议 | 3,200 unique / 6,400 request 预算 + 0.20-s 等时间协议（墙钟不跨环境池化） | ✅ |
| §5 指标与多重性 | HV 主 + IGD+（共享归一化参考集）分级校正；两家族独立 Holm；配对符号检验 | ✅ |
| 失败/可见性/负结果 | 独立章节；失败运行与负结果政策冻结 | ✅ |
| 执行门 | NO-GO 待注册表/成本/边界/环境；**结果可见前** manifest 修订不得改动臂/种子/预算/指标规则/比较族/校正/失败政策 | ✅ |

## 二、发现的 2 项缺口（s06 前必须修订，协议本身允许结果前修订）

1. **Tight-B 先验紧预算条件缺失**（14 号契约 §4）：未找到按"可行种群比例 <0.5 的预算水平"先验分层。修订：在两任务族的 task-instance 面板中按预注册公式计算紧/松预算档并冻结分层标签。
2. **P2-7 解释性结果族缺失**（14 号契约 §5/§6 + R2 新增）：协议结果清单只有 HV/IGD+/可行性——缺跨情景入选项目 Jaccard 重叠率、组标签一致性、修订路径长度。修订：作为**描述性新增结果族**（协议已允许结果前修订描述性结果），不得进入主推断家族。

原因：s04 计划目标未含这两项（R2 规格在计划批准后才回写契约），执行器按计划目标冻结。修订路径 = 结果可见前的协议修订（协议 §5 自留的通道）。

## 三、四篇 s04 全景

| 论文 | s04 | 状态 |
|---|---|---|
| P1 | frozen confirmatory protocol | ✅ 已接受 |
| P3 | frozen 2×2 + AC protocol | ✅ 已接受 |
| P4 | frozen graph-geometry protocol | ✅ 已接受 |
| P2 | frozen orthogonal + matched-compute protocol | ⏳ 待裁决（本评审） |

## 四、建议

1. **接受** `p2_v2_s04_frozen_experiment_protocol`；
2. 把 §二 两项修订写入 s05 pilot 的输入（随 pilot 阶段或独立协议修订提交）；
3. s05 前的全局阻塞项清单：registry 数据物化（P2/P3）、环境钉扎（P1）、NERC 属性处置（P1，A/B/C 待用户答复）、Ausgrid 源清单（P4）。
