# P4 Stage-3/4 精细化实验设计契约

**日期：** 2026-09-04
**论文：** P4 — `Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting`（锁定标题）
**项目目录：** `paper_projects/mintou_p2_hygraph_load_forecasting`
**目标期刊：** MDPI Electronics（Section：Artificial Intelligence 首选；Computer Science & Engineering 备选）
**对接 harness 阶段：** `p4_v2_s03_method_data_implementation_contract` + `p4_v2_s04_frozen_experiment_protocol`
**前置：** Stage-2（`c138f7228c9e`）接受合并。
**设计口径：** 公平调参 + 先验条件化正向结论 + 全结果可见。**本契约所有"条件定义"必须先于任何正式实验写入并冻结，不得根据结果回填。**

> **红线声明（保留原文）：** 当前 CSA-LoadNet 是锁定标题重建的基线，不是 GCN/HGCN；"No GCN or HGCN experiment or result is reported" 的红线表述在真实 HGCN 实现并产出结果前必须保留在稿件中。本契约的执行目标就是解除这条红线——但解除的唯一途径是实现与匹配对照，不是改写措辞。

## 1. 主张分层登记（写入 s03）

| 层级 | 内容 |
|---|---|
| **已证实（legacy，保留）** | OPSD rolling-origin 主对照 null（MAPE Holm p=0.984）；三种权重形式不可分；fixed-scale 名义最优但 p=0.0625；Ausgrid 层级上 DLinear 显著更优（Holm p=0.000985）；lead-1 MLP 胜；SimBench 无结论 |
| **待检验** | H1–H3 见 §4；真实 HGCN 与匹配欧式 GCN 的相对表现 |
| **不可主张** | 双曲几何的通用优势（当前无曲率实现）；图结构 = 物理拓扑；对标题方法的任何结果（实现前） |

**负结果保留条款：** legacy 全部 null/负结果（Poincaré 权重未决、DLinear 更优、MLP lead-1 胜、SimBench 无分离）保留为预注册历史；旧档案只读，新命名空间 `p4_v2_s04_*`。

## 2. s03 契约补充：真实 HGCN 的实现语义（红线解除路径）

1. **HGCN 实现定义（验收级）：**
   - 图卷积：图拓扑上的邻域聚合（消息传递），**非稠密注意力**；
   - 双曲几何：切空间线性变换 + exp/log 映射（Poincaré 球或 Lorentz 模型二选一，预注册）；
   - 曲率参数：fixed {0, 1} 与 learnable 两种模式；
   - 时间编码器与预测头与匹配欧式 GCN **相同**；参数量差 ≤10%。
2. **图来源（预注册）：** 主图 = Ausgrid 精确 17 节点层级（树结构）；次图 = OPSD 区域相关图（相关性阈值预注册）；对照图 = identity、random（预注册种子）。**图全部只由训练可用信息构造，严禁用测试期数据建图**（前评估风险条款）。
3. **匹配欧式 GCN：** 同图、同编码器、同头、同调参预算、近似参数量——双曲几何贡献的唯一合法对照。
4. **基线补全：** 新增 persistence 基线（当前全稿缺失）；保留 DLinear、LSTM、TCN、PatchTST-lite、CSA-Poincaré/Euclidean（legacy）。
5. 投稿路由决策（作者已被告知）：若按语料路由提示转 Energies/Energy Reports/IEEE Access，需标题豁免——**本契约默认按 Electronics 执行，路由决策门在 §7**。

## 3. 公平调参协议（先于正式实验，调参与评估分离）

| 模型 | 调参空间 | 说明 |
|---|---|---|
| HGCN | 层数 ∈ {1,2}、隐维 ∈ {32,64}、曲率模式 ∈ {fixed 1, learnable}、学习率/正则网格 | 全部网格候选共享 |
| 欧式 GCN（匹配） | 与 HGCN 同一网格（曲率项除外） | 调参预算完全对齐 |
| DLinear / LSTM / TCN / PatchTST-lite | 各自文献网格 | 同等网格数 |
| persistence | 无参数 | — |

- **调参对象：** 8 个 rolling 块中的 3 个（预注册）× 3 种子；**最终评估：** 全 8 块 × 5 公共种子，种子在块内先平均（块为外层统计单位——沿用 legacy 协议）。
- **调参判据（预注册）：** 块级 WAPE 均值。
- **计算成本门（新）：** 先跑 §6 的 pilot（s05 阶段），按 pilot 实测的每模型训练/推理时长与显存，在正式实验前由作者确认总预算；超预算触发 §7 路由决策门。

## 4. 先验条件化假设（s04 冻结内容）

**条件定义（先验，基于数据结构，不基于结果）：**
- **层级条件 Hier：** Ausgrid 精确层级（树结构、高分支因子）——双曲几何的理论适用域（树状结构在欧式空间嵌入有失真，这是先验可辩护的）。
- **稠密条件 Dense：** OPSD 相关图（近似完全图）——先验预期双曲无优势（保留为"无优势假设"位）。

| 假设 | 表述 | 主检验 |
|---|---|---|
| **H1（正向 headline 候选）** | Hier 条件下 HGCN 的 WAPE 显著优于匹配欧式 GCN | 块级配对符号检验 + Holm |
| **H2（无优势保留位）** | Dense 条件下 HGCN 不优于欧式 GCN | 原样报告（未显著 ≠ 等价，legacy 已声明） |
| **H3（几何消融）** | 图 × 曲率正交消融中，real-hierarchy 图 + 双曲几何的交互项显著（Hier 条件） | 预注册对比组 |

**说明：** H1 的成立前提是"树状结构 + 双曲几何"的理论论证，该论证写入引言先行；若 H1 不通过，不得挑其他子集硬造正向（§7 降级门）。

## 5. 主指标预注册

- **主指标：** 块级 WAPE（lead-24，Ausgrid Hier 条件为第一家族；OPSD lead-24 为第二家族）。
- **次指标（同表同显著度，修复报告缺口）：** MAE、RMSE 进主表（当前缺失）；参数量、训练/推理时间、显存、数值失败计数（当前仅 manifest 层面）。
- **多重性：** 家族内 Holm；块为外层单位；种子块内平均后再推断。

## 6. 新实验矩阵（s04）+ pilot 门（s05）

- **模型：** HGCN、欧式 GCN、DLinear、LSTM、TCN、PatchTST-lite、persistence、CSA（legacy 参照）。
- **消融：** 图 ∈ {real hierarchy, identity, random} × 曲率 ∈ {fixed 0, fixed 1, learnable} × 层数 ∈ {1,2}（预注册正交表）。
- **条件：** Hier（Ausgrid）、Dense（OPSD）、SimBench（保留 legacy 无结论定位）。
- **pilot 门（先于正式实验）：** Ausgrid 单条件 × 2 种子，验证代码/数据血缘/图构造/显存/时长，pilot 结果不计入论文（paper_use=false），禁止按 pilot 调参。
- **命名空间：** `p4_v2_s04_*`；legacy 只读。

## 7. 叙事重构预案与降级决策门

| 结果情形 | 叙事与行动 |
|---|---|
| **H1 通过、H2 保留** | 红线解除：摘要改写为"双曲图卷积在层级结构负荷数据上的条件化优势（匹配欧式 GCN 消融）"；legacy CSA 审计降为预注册历史章节；Electronics 可投（AI Section） |
| **H1 不通过、H2 保留** | 决策门（预注册触发）：① 转纯负荷预测定位 → Energies / Energy Reports / IEEE Access + 标题豁免请求；② 或并入其他论文作为内部证据包；③ 不得以原标题投 Electronics |
| **pilot 显示资源超预算** | 提前触发决策门，不烧正式实验预算 |
| **任何情形** | DLinear 更优、Poincaré 未决等 legacy 结果保留；红线表述在实现前保留 |

**验收标准（对齐评分报告阻塞项）：** ① 真实 HGCN 实现并通过"图卷积 ≠ 稠密注意力"的自查清单（红线解除的唯一路径）；② 匹配欧式 GCN 对照参数量 ≤10% 差；③ 图构造零测试期信息泄漏；④ MAE/RMSE 进主表、显存与数值失败上报；⑤ persistence 基线补齐；⑥ 条件定义与主指标预注册先于实验；⑦ pilot 门与资源预算经作者确认；⑧ **P4-8（R2 新增）**：曲率定义先行条款——HGCN 方法章节必须显式定义模型、exp/log 映射、曲率参数语义与学习方式，并在消融中区分"双曲聚合贡献"与"图结构贡献"。
