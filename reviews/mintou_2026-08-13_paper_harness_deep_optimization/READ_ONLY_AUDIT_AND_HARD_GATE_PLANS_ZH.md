# 闽投六篇：Paper Harness 深度优化只读审计与 Hard-Gate 计划

日期：2026-08-13  
状态：六篇计划均已注册，尚未人工批准，未启动正文修改或新实验。

## 1. 从两篇 Applied Sciences 与闽投六篇蒸馏的规则

1. 正文首先讲问题、方法、主结果、机制解释和应用边界；版本、哈希、事故记录和完整测试矩阵退到补充材料。
2. 题目中的每个承重词必须在方法中可操作定义，并由直接实验支撑。品牌名不等于算法机制。
3. 每项主要贡献对应一个直接检验。实现活跃、结果改善、可追踪性、语义正确性和人工效用属于不同主张。
4. 同时移除多个机制的消融只能支持组合效应，不能拆成单组件贡献。
5. 负结果和零结果必须在摘要、结果、讨论和结论中保持同一方向与范围，不能通过调参或改写隐藏。
6. 历史候选池、代理数据、构造状态、开发集可见分析和描述性回测不能写成前瞻、因果、专家验证、生产部署证据。
7. 公平比较必须披露模型、数据可见性、调参、长度、候选池、调用、总评价次数、token、时间和硬件等实质预算差异。
8. 随机种子只描述固定数据上的训练随机性，不能替代时间、事件、系统或总体不确定性。
9. trace、日志、来源链接和接口覆盖不能自动推出解释质量、审核效率、安全性或人工接受度。
10. P3/P4 与 P5/P6 的共享代码和数据必须双向披露；共享回归测试不等于两篇可以重复宣称同一创新。

以上规则已写入 `D:/aicoding/Lib/paper_harness/resources/paper_experience_digest.json` 和
`reviewer_protocol.md`，并注入 planner、executor 和 reviewer 的执行提示。

## 2. Harness 本轮加固结果

- 修复 monorepo worktree 相对路径、跨阶段旧 HEAD、候选未提交、未跟踪正文遗漏和越界提交风险；
- 每次只运行一个 stage，上一候选未经人工 accept/reject 不会进入下一阶段；
- reviewer 按全文读取并记录稿件 SHA、覆盖范围、主故事、主结果、claim map、问题证据和验收条件；
- LaTeX 检查在正文真实目录编译，扫描 fatal、未定义引用、占位符、图路径、重复标签、PDF 文本和陈旧 Visual-QA 痕迹；
- 新增 `scripts/mintou/harness_scientific_acceptance.py`，要求每篇建立主张—证据合同，并运行闽投 12 项既有实验资产回归测试；
- Harness 自身 10 项 smoke 测试通过；闽投实验资产 12 项 pytest 回归通过。

## 3. 六篇全文只读审计

所有评审均读取当前完整 LaTeX 稿件，未以截断片段代替全文。自动 decision 是问题排序器，不是最终录用判断。

| 论文 | 全文字符 | 自动判断 | 最重要的待解决问题 |
|---|---:|---|---|
| P1 IEEE Access | 66,651 | Reject-level revision | 摘要/结论与 24 h 表格直接矛盾；预测信息门未定义；Ridge 数据可见性不公平；检索与 MAE 选权组合归因 |
| P2 Electronics | 61,160 | Major Revision | aggregation 消融同时改变输入与容量；所谓 curvature 实为固定 Poincare 距离尺度；24 h 点预测与 day-ahead trajectory 错配；固定切分种子统计 |
| P3 Energies | 73,598 | Major Revision | 混合电压组合代理与 distribution expansion 标题错配；AC 仅组合映射诊断；方法常数和修复定义不足；HV 参考界与裁剪敏感性 |
| P4 Energies | 83,495 | Major Revision | 方程与 DER/hosting 实现待核对；resilience 代理与物理验证边界；情景层统计单位；预算、场景数和系数敏感性 |
| P5 Energies | 78,826 | Major Revision | 98.6% trace 是事件共现而非完整 lineage；AHP/TOPSIS 单解与 MOEA front 不匹配；偏好层独立增益仅 0.17% 且未解决；HV 与参数敏感性 |
| P6 Applied Sciences | 78,212 | Major Revision | 1.12% HV 增益伴随额外评价和 2.74 倍运行时间；局部搜索/依赖/trace 定义越界；需要等总评价和等时间对照；HV 敏感性 |

已有优点会保留：六篇均有足量基线和消融、真实/公开派生数据资产、负结果披露、统计审计和期刊格式 PDF。优化目标不是强行制造 SOTA，而是消除可避免的证据错配，使真实贡献更清楚。

## 4. 逐篇实验与叙事补强重点

- P1：统一 fit/selection/calibration 数据门；若来源确有目标时刻预测则增加直接 policy-transform，否则明确为滞后代理预测；将 retrieval presence 与 selection objective 解耦；做 paired-seed 和必要的 cap sensitivity。
- P2：增加参数/头部/训练预算匹配的有效 cross-series context control；可保留 shared encoder 的独立贡献时才增加对应控制；用 rolling origin 作为外层单位；curvature 改为 distance-scale，除非真正实现曲率参数。
- P3：验证 HV 参考点支配性、裁剪和替代参考点；AC 若不能覆盖每个 seed 的预先选择 compromise，则降级为 illustrative composition diagnostic；配置而非 210 个运行作为外层解释单位。
- P4：先对齐方程与实现，再做预算紧度、场景数/独立抽样和关键 cost-effect/resilience 系数的边界分析；screening 目前只许可“节省 objective calls”，不许可质量增益。
- P5：实现真正 lineage/replay 或将 trace 降为 run-level intervention-event record；用统一 compromise 或等输出规模比较 deterministic 方法；补 HV 和偏好参数敏感性。
- P6：在相同总评价次数、相同 wall-clock 预算下比较 BiLo-NSGA/NSGA-II/PLS；将结果呈现为 quality-compute trade-off；依赖 bonus 和 trace 仅按实际机制命名；补 HV 与局部搜索参数敏感性。

## 5. 已注册的 Hard-Gate 计划

每篇均为 6 个顺序阶段：主张合同、方法合同、关键实验补强、结果与叙事重构、三轮科学闭环、人工投稿信息门禁。

| 论文 | plan | SHA-256 |
|---|---|---|
| P1 | `plan_v1.md` | `b56111b0d8e690f625136f02b3db7b5bea09166c42d0c4f9ba90e74ded3aae3a` |
| P2 | `plan_v1.md` | `2d5510599de938e05852e9ef056f9d485970665e8e5891a3f86662376b88b935` |
| P3 | `plan_v1.md` | `76c45a3872ac2db65db9e129ec379bec9340d35fe97f460addb88f579a35e49b` |
| P4 | `plan_v1.md` | `b27e0e6a29ec2e390ed5f1e1181a9c13730fcd108f623dc9a39d35bc65d046eb` |
| P5 | `plan_v1.md` | `0b3e1b6aa1c721c5be16fa9e2fbfeafc9f84e32f18b8fbe9f6852e06b544d21a` |
| P6 | `plan_v1.md` | `8fb0ab9fab2746678e62372d691add765aa3aa882f35ce820d266ac280e01803` |

六个执行预检均为 `tracked, clean baseline`。计划文件发生一个字节的变化，摘要即失效，必须创建新版本并重新批准。

## 6. 当前不可由代理关闭的 blocker

六篇均有作者确认类占位符；P1 还缺作者机构、通信信息、基金和 IEEE biographies。其他稿件至少缺 CRediT 和基金/APC 确认。Harness 的前五阶段允许这些占位保留并明确标记，最终第六阶段会因 `no_placeholders` 自动 BLOCKED，直至作者提供真实信息。

无法保证“一次投稿就录用”。本流程能做的是显著降低标题越界、表文矛盾、不公平对比、统计单位错误、共享资产未披露和投稿文件不完整等可避免的拒稿风险。
