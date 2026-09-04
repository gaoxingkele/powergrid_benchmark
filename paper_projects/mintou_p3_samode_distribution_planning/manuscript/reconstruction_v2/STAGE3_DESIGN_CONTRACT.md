# P3 Stage-3/4 精细化实验设计契约

**日期：** 2026-09-04
**论文：** P3 — `Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm`（锁定标题）
**项目目录：** `paper_projects/mintou_p3_samode_distribution_planning`
**目标期刊：** MDPI Energies（Section：F1 Electrical Power System 首选，A1 Smart Grids 备选）
**对接 harness 阶段：** `p3_v2_s03_method_data_implementation_contract` + `p3_v2_s04_frozen_experiment_protocol`
**前置：** Stage-2（`c49e16412e56`）接受合并。
**设计口径：** 公平调参 + 先验条件化正向结论 + 全结果可见。**本契约所有"条件定义"必须先于任何正式实验写入并冻结，不得根据结果回填。**

## 1. 主张分层登记（写入 s03）

| 层级 | 内容 |
|---|---|
| **已证实（legacy，保留）** | sampled/clipped HV 下 CARS-MODE +6.06% vs NSGA-II+Repair（等权）；analytic r=1.05 下两者 0.00043464/0.00043530 基本持平；common-ref IGD+ 排名第 5；FixedDE 三口径名义领先；修复与多样性保留实质效应 |
| **待检验** | H1–H4 见 §4；2×2 四臂拆分后的机制归因；action-aligned AC 映射的可行性证据 |
| **不可主张** | "Self-Adaption" 的通用优势（当前 unresolved）；规划决策的电气可行性（AC 为组合级映射）；成本为货币估计 |

**负结果保留条款：** FixedDE 名义领先、IGD+ 排名第 5、指标排名反转（Table 5/9）、NoDER 居首、高 DER 映射伪影全部保留；legacy 的 2940 行档案只读，新命名空间 `p3_v2_s04_*`。

## 2. s03 契约补充：2×2 拆分与 action-aligned 映射的实现语义

1. **2×2 四臂拆分（最高优先级，红线 1）：** 代码层面把联合开关拆为两个独立门——
   - **参数自适应门（ParamAdapt）：** jDE 式 F/CR 按个体自更新，**改为可遗传字段随个体进入子代**（当前按槽位驻留是 jDE 语义偏差，必须修正）；
   - **策略池门（StrategyPool）：** rand/1 + best/1 成功驱动选择池。
   - 四臂：Fixed–Fixed、AdaptiveParam–FixedStrategy、FixedParam–AdaptiveStrategy、Adaptive–Adaptive（= Full CARS-MODE）。两门的随机源独立预注册。
2. **action-aligned AC 映射（红线 2）：** 将组合级决策变量映射为**节点级动作**——预注册映射规则：储能候选 → 指定母线节点的储能容量增量；DER 候选 → 指定母线 PV 接入量；馈线加固 → 指定线路换线/并联。至少 1 个 SimBench MV 网络（rural 或 urban，预注册）、每个方法臂 5 个种子 × top-k（k=5）解映射、三条件并查（收敛、电压 [0.95,1.05]、载流 ≤100%）。成本/收益按映射后网络量计算（预注册公式）。若映射规则无法唯一确定 → 记录 NO-GO，AC 层维持 legacy 定性定位并写入 cover letter 处置。
3. 公平性修复（s03 一致性清单）：等目标调用预算且**认证**；全方法共享同一种子流；MOEA/D 权重/群体修复（legacy 35 vs 40 及"必然失败"配置必须修）；解码阈值统一 ≥0.5；pymoo 版本钉扎。

## 3. 公平调参协议（先于正式实验，调参与评估分离）

| 方法/臂 | 调参空间 | 说明 |
|---|---|---|
| CARS-MODE 四臂 | 每臂共享同一调参网格：初始 F/CR 均值、学习率、策略池窗口、修复顺序 | 四臂只在两个门上不同，其余参数同格 |
| FixedDE | 与 ParamAdapt 门关断配置同格扫描 | 保证"固定"臂获得同等调参机会 |
| NSGA-II / NSGA-II+Repair | SBX η × PM η × 交叉率（库默认 → 网格） | 关键公平性修复 |
| GDE3 / NSDE | 标准参数网格 | 若文献默认优于网格，取网格内最优并记录 |
| MOEA/D | 权重生成 + 群体规模修复后网格 | — |

- **调参对象：** 6 个规划配置中的 3 个（预注册）× 10 配对种子；**最终评估：** 全 6 配置 × 30 配对种子，等目标调用预算（预注册上限）。
- **调参判据（预注册）：** 池化 analytic HV（r=1.05）中位数，平局取预算更少者。**注意：调参判据用 analytic 而非 sampled/clipped——指标预注册的一贯性（见 §5）。**

## 4. 先验条件化假设（s04 冻结内容）

**条件定义（先验，基于问题数据结构，不基于结果）：**
- **rugged 条件 Rugged：** 高 DER 场景 × 紧预算档（legacy 中已存在的配置，预注册其组合为"景观更 rugged"的理论依据：二进制约束面更崎岖、可行域更紧）。进入正式实验前，用采样游走的自相关度量计算 legacy 各配置的景观 ruggedness 并**验证** Rugged 档位确实更 rugged（验证公式先验冻结；验证结果无论是否支持，Rugged 定义不变）。
- **nominal 条件 Nominal：** 其余配置。

| 假设 | 表述 | 主检验 |
|---|---|---|
| **H1（正向 headline 候选）** | Rugged 条件下 ParamAdapt 门开（相对关）显著提升 analytic HV | 条件内配对 + Holm |
| **H2（机制）** | StrategyPool 门开显著提升可行前沿比例/多样性 | 同口径 |
| **H3（保留未决）** | Nominal 条件下各门无显著效应（不得改写为已显著） | 原样报告 |
| **H4（工程）** | 各臂 AC 映射后的可行性率在预注册阈值之上 | 描述性 + 阈值比较 |

**说明：** legacy 中"自适应在紧预算/高 DER 下名义更好"的模式是 H1 的设计依据，但条件定义与指标全部先验冻结；若 H1 不通过，不得降级挑子集，走 §7 降级门。

## 5. 主指标预注册（本契约的关键改动）

- **主指标：analytic HV（r=1.05）**——替代 legacy 的 sampled/clipped 主位，理由：预注册 analytic 为主可消除"sampled/clipped 有利而 analytic/IGD+ 反转"的指标钓鱼攻击面。
- **次指标（同表同显著度）：** sampled/clipped HV（保留历史可比）、common-ref IGD+、可行前沿比例、AC 可行性率、电压/载流/损耗汇总、计算时间。
- **多重性：** 家族内 Holm；效应量 + bootstrap CI；每臂配对种子（shared stream）。

## 6. 新实验矩阵（s04）

- **臂：** 2×2 四臂 × **基线：** NSGA-II、NSGA-II+Repair、GDE3、NSDE、MOEA/D（均调参后）。
- **条件 × 配置：** Rugged（高 DER × 紧预算）与 Nominal 分层，6 配置 × 30 配对种子。
- **AC 层：** 1 个预注册 SimBench MV 网络 × 5 种子 × top-5 解/臂，节点级映射。
- **命名空间：** `p3_v2_s04_*`；legacy 只读。

## 7. 叙事重构预案与降级决策门

| 结果情形 | 叙事与行动 |
|---|---|
| **H1 通过、H3 保留** | Headline = "自适应参数控制在高 DER 紧预算等 rugged 规划条件下的条件化优势 + 2×2 机制归因 + action-aligned AC 筛查工作流"；"Self-Adaption" 由 ParamAdapt 门承载 |
| **H2 通过但 H1 不通过** | 卖点转为策略池/多样性的条件化贡献；"Self-Adaption" 词义由策略自适应承载（需 cover letter 说明），或触发标题豁免请求 |
| **H1/H2 均不通过** | 决策门（预注册触发）：① 向作者请求标题豁免（去掉 Self-Adaption）；② 或改投 MDPI Algorithms / Applied Sciences 以"可复现约束搜索审计"定位；③ 不得在 Energies 硬投原标题 |
| **任何情形** | FixedDE 名义领先、IGD+ 反转、NoDER 居首全部保留；"Self-Adaption" 拼写风险以 cover letter 一句话处置（标题锁定不修改） |

**验收标准（对齐评分报告阻塞项）：** ① 2×2 四臂代码拆分完成且两门随机源独立（红线 1）；② action-aligned AC 映射 + 种子复现完成或 NO-GO 记录（红线 2）；③ analytic HV 主指标预注册先于实验；④ 全方法等调用预算认证 + 共享种子流；⑤ MOEA/D 修复；⑥ 指标反转全景表保留；⑦ 摘要/结论与四臂结果严格对齐；⑧ **P3-7（R2 新增）**：性价比度量预注册——每臂"达到给定 analytic HV 阈值所需平均目标调用次数"（quality-per-evaluation）+ 墙钟；若自适应臂在 Nominal 条件性价比不劣，构成独立于精度优势的正当贡献位。
