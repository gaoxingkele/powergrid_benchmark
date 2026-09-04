# P2 Stage-3/4 精细化实验设计契约

**日期：** 2026-09-04
**论文：** P2 — `Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization`（锁定标题）
**项目目录：** `paper_projects/mintou_p6_bilonsga_project_review`
**目标期刊：** MDPI Applied Sciences（Section：Energy Science and Technology 首选；EEC Engineering 备选）
**对接 harness 阶段：** `p2_v2_s03_method_data_implementation_contract` + `p2_v2_s04_frozen_experiment_protocol`
**前置：** Stage-2（`68cd1f233f9f`）接受合并。
**设计口径：** 公平调参 + 先验条件化正向结论 + 全结果可见。**本契约所有"条件定义"必须先于任何正式实验写入并冻结，不得根据结果回填。**

## 1. 主张分层登记（写入 s03）

| 层级 | 内容 |
|---|---|
| **已证实（legacy，保留）** | 等预算 3200 单位下 BiLo 0.16277 < NSGA-II 0.17213、8 场景 4 负 0 胜（Holm）；对已披露 PLS 配置全 8 场景显著领先；等时间 0.20-s 下 3 胜 2 负 3 未决；(D+,D-)=(2,2) 较注册 (8,4) 描述性 +4.29%；MTEP16/NERC 反测自限 descriptive |
| **待检验** | H1–H3 见 §4；公平调参后的相对关系；第二任务族（MTEP16）进入推断协议后的结果 |
| **不可主张** | 对 NSGA-II 的 superiority（红线）、替换算子对审稿人的有用性、真实投资回报（成本未校准）、项目 lineage |

**负结果保留条款：** "loses four of eight and wins none" 必须继续出现在摘要或结论（红线）；等时间协议的 2 负、替换算子全 8 场景无增益、(D+,D-) 敏感性中任何倒退格全部保留；旧档案只读，新命名空间 `p2_v2_s04_*`。

## 2. s03 契约补充：成本校准与第二问题族判定

1. **成本校准（最高优先级 NO-GO 判定）：** 预注册两种方案，按序尝试——
   - 方案 A：合成成本 → MTEP16 真实 2016 成本分布的分位数映射（变换函数先验冻结，报告原值 + 映射值双列）；
   - 方案 B：引入公开 LCC/NPV 文献参数对六类原型项目定价。
   - 两者均不可用 → 记录 NO-GO，摘要保留 "synthetic cost units"，门槛第 3 条保持"未满足"状态并写入 cover letter 处置方案。
2. **第二任务族：** MTEP16 池（1218 项目、真实 2016 成本、built/withdrawn/deferred 标签）从"描述性反测"升级为**完整协议的第二问题族**——跑同一 18 方法 × 30 配对种子冻结协议，built/deferred 分布一致性作为预注册的验证度量（descriptive）。
3. **精确参照（新增）：** 3 个小实例（30/40/50 项目、2 目标、预注册生成种子）用 DP/ε-constraint 求参考前沿；所有方法在小实例上与参考前沿的 HV 比值报告。
4. COI 与投稿字段：作者雇佣关系必须具名披露（诚信级），CRediT/Funding 用作者提供的信息填齐（作者已确认资料可用）。

## 3. 公平调参协议（先于正式实验，调参与评估分离）

**原则：每个方法获得同等的调参预算；调参场景/种子与最终评估不相交；全程记录。**

| 方法 | 调参空间（候选格） | 备注 |
|---|---|---|
| BiLo-NSGA | (D+,D-) ∈ {(2,2),(4,4),(8,4)}、组标签加成权重 ∈ {0.0, 0.5, 1.0}×、替换概率 p_sub ∈ {0.2, 0.5} | (2,2) 的 4.29% 是调参起点依据，不是结论 |
| NSGA-II | SBX η ∈ {15,20,30} × PM η ∈ {15,20} × 交叉率 ∈ {0.7,0.9}（当前库默认） | 关键公平性修复 |
| PLS | 邻域定义 ∈ {单翻转, 双翻转, 删除+插入} × 提案上限 ∈ {8,16}（当前 0.11626，疑欠调） | 若 PLS 调参后仍大幅落后，如实报告 |
| 其余确定性基线 | 不调 | — |

- **调参对象：** 场景 1–4 × 10 配对种子；**最终评估：** 全 8 场景 × 新 30 配对种子，等 3200 单位预算为主、等 0.20-s 时间为辅（沿用 legacy 双协议）。
- **调参判据（预注册）：** 池化 clipped HV（r=1.05）中位数，平局取预算更少者。
- 环境钉扎：pymoo 版本 + 平局规则冻结。

## 4. 先验条件化假设（s04 冻结内容）

**条件定义（先验，基于问题数据结构，不基于结果）：**
- **紧预算条件 Tight-B：** 预算水平使"全场景平均可行种群比例 < 0.5"的 B 值（由 legacy 档案的可行性分布先验计算，公式冻结，不进实验后再选）。
- **低依赖条件 LowDep：** LowDependencyDensity 场景族（legacy 已有该压力探针，直接沿用并预注册为主条件）。

| 假设 | 表述 | 主检验 |
|---|---|---|
| **H1（正向 headline 候选）** | BiLo-NSGA 对 PLS（公平调参后）在等预算主协议下显著领先 | 配对符号检验 + Holm |
| **H2（参数化贡献）** | (D+,D-)=(2,2) 相对注册 (8,4) 的增益在 Tight-B 条件下显著 | 条件内配对检验 |
| **H3（探索性，不得单独成为 headline）** | Tight-B 条件下 BiLo 对 NSGA-II 的差异方向 | 预注册方向性检验；无论结果如何全图报告 |

**说明：** H1/H2 是确认性假设（legacy 已有强先验）；H3 是"公平调参后负结果是否翻转"的诚实检验位——若翻转，升级需走 harness 的 claim 升级门禁并同时保留 legacy 负结果；若不翻转，红线维持。

## 5. 主指标预注册

- **主指标：** clipped HV（r=1.05）等预算协议。
- **次指标（同表同显著度）：** analytic HV、IGD+、可行前沿比例、成本指数（合成 + 校准双列）、MTEP16 验证度量、运行时间（等时间协议表）。
- **多重性：** 家族内 Holm；效应量 rank-biserial + bootstrap CI；匹配主协议的逐格效应量/CI **从补充包升入正文**（评分报告缺口项）。

## 6. 新实验矩阵（s04）

- **臂：** NDS-only、forward-only、backward-only、bidirectional（全量）、NoAtomicSubstitution、NoFeasibilityRecovery、RandomMutationOnly（修正变异率混杂后重做）。
- **基线：** NSGA-II、NSGA-III、MOEA/D、PLS（均调参后）、Greedy BCR、AHP-TOPSIS、Random Feasible。
- **任务族 × 条件：** 主池（8 场景 × Tight-B/LowDep 分层）+ MTEP16 池（预注册验证度量）+ 3 个精确小实例。
- **命名空间：** `p2_v2_s04_*`；legacy 只读。

## 7. 叙事重构预案与降级决策门

| 结果情形 | 叙事与行动 |
|---|---|
| **H1 通过、H3 仍负** | Headline = "项目词表局部搜索 + 等代价审计协议"：对 PLS 的显著优势 + 对 NSGA-II 的诚实非优势并列为主结论；标题的 "Bidirectional Local Search" 由 forward/backward 机制消融承载 |
| **H1 通过、H3 翻转** | 按 harness claim 升级门禁把 Tight-B 条件化优势写入摘要，**同时保留 legacy 全场景负结果**为预注册历史 |
| **H1 不通过** | 决策门：框架/审计叙事（等代价评估协议 + 事件摘要）仍可投 Applied Sciences，但需 cover letter 定位；或改投对负结果容忍度更高的 EAAI/Swarm EC benchmarking 栏目 |
| **任何情形** | legacy 4 负 0 胜结果保留；不删除 (D+,D-) 倒退格 |

**验收标准（对齐评分报告阻塞项）：** ① 条件定义与主指标预注册先于实验；② NSGA-II/PLS 公平调参且过程公开；③ 成本校准完成或 NO-GO 记录在案；④ MTEP16 第二族进入推断协议；⑤ 精确小实例参照完成；⑥ COI 具名披露雇佣关系；⑦ 摘要压回 ≤200 词；⑧ **P2-7（R2 新增）**：解释性结果族预注册并进入冻结协议——跨情景入选项目重叠率（Jaccard）、组标签一致性、替换算子开启时的修订路径长度；公式先验冻结；构成独立于 hypervolume 的潜在正向贡献位。
