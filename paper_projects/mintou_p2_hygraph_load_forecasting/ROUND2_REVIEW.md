# Round 2 — p2 HyG-LoadFormer 综合评审

- **日期**: 2026-07-13
- **评审轮次**: Round 2 (6-mintou 全量 paper_reviews 7 维评审)
- **目标刊**: MDPI Electronics (主) / MDPI Applied Sciences (次)
- **优先级**: 快发优先,允许算法/数据集/下游任务修改
- **ARA 源路径**: `papers/mintou/mintou_p2_hygraph_load_forecasting`

---

## 1. Paper Summary

HyG-LoadFormer (Hyperbolic Graph Load Forecasting Transformer) 主张利用双曲几何图权重建模电网层级结构,实现层级负荷预测与下游调度敏感性分析。ARA 工程在 OPSD(6 国 60 分钟负荷,35,000 行,2015–2018)与 SimBench(馈线 LoadProfile,8,760 行,2016)两个公开数据集上完成了固定切分 + rolling 时序切分(3 个 train ratio: 0.55/0.65/0.75)基准实验,历经 v1 weak → v2 mixed → v3 gate rejected → v4 residual 四个合规精化版本。

**核心信号**:
- OPSD 24h 固定切分 MAPE 0.03972575 vs 最强基线 Weekly-168h 0.05632632(+41.79%);rolling 均值 0.03931968±0.00056 vs 0.05471780(+39.16%)
- OPSD 24h 对最强 ablation (FixedCurvature) 增益 74.07%(固定)/79.59%(rolling),组件贡献可分离
- SimBench 24h 归一化 MAE 固定 +3.59%、rolling +5.15%

**核心限制**:
- OPSD 1h 仅比最强基线好 0.25%,且始终弱于自己的 NoCalendar ablation(固定 -7.85%、rolling -15.71%)
- SimBench 1h 被门控为与 Persistence 完全相同(增益 0.00%);SimBench 24h MAPE 比 Weekly-168h 差 14.04%
- **实现现实**:全部使用 Python 标准库(`src/environment.md`:"Python standard library only"),无 PyTorch/numpy/scipy;实际是 ridge 回归 + 双曲距离加权图特征,无任何 Transformer/attention 组件
- 9 个名义基线(LSTM/BiLSTM/TCN/Transformer 等)仅存在于合成 smoke 矩阵;真实数据上只有 7 个 naive/ridge 级基线,去重后有效独立基线约 5 个,无一为神经网络

---

## 2. Target Venue + Distilled Standards Applied

### MDPI Electronics (主目标)

| 维度 | Distilled 标准(15 篇电力系统全文,2023–2026) | 本文现状 |
|---|---|---|
| 新颖性锚点 | 11/15 卖 ML 架构组合或元启发改进;零基础新算法;审稿人问"每个组件是否有依据" | **不满足**:无任何 ML 架构,实际为 ridge 回归;"Transformer"名实不符 |
| 实验地板 | 1 case study + ≥1 comparison class + ≥2 of MAE/RMSE/MAPE | **部分满足**:2 个数据集 ✓,6 项指标 ✓;但 comparison class 全为 naive/ridge,无 neural |
| 规范 | ~3 baselines + component comparisons | **形式满足**但基线退化(Euclidean-GCN Ridge ≡ GCN-Temporal Ridge ≡ Ablation-EuclideanGraph,8 位小数全同) |
| 不要求 | 显著性检验(0/15)、baseline-tuning fairness(0/14)、multi-run mean±std(1/14)、open code(0/15) | 不需要,但 rolling ±std 已提供稳定性证据(可作加分) |
| 硬地板 | Funding/COI/Author Contributions 齐全 | **未写**(MDPI 四件套缺失) |
| slip-through 自查 | 摘要 metric 方向错误、无控制比较的量化主张、Data Availability 矛盾、半披露超参 | **风险**:标题"Smart Dispatch"无真实 dispatch 证据;超参仅 ridge=1e-6 无调参协议 |

### MDPI Applied Sciences (备选)

| 维度 | Distilled 标准(11 篇电力/能源全文) | 本文现状 |
|---|---|---|
| 应用价值逻辑 | 真实 utility/field case study + 量化经济效益可完全替代方法学基线;7/11 用真实电网/field 数据 | **不满足**:OPSD/SimBench 为公开基准,非 field case;无受益方命名 |
| 隐含交换 | 零基线 OK 仅当有 sensitivity analysis;6/11 含敏感性分析 | **不满足**:sensitivity analysis 完全缺失 |
| 新颖性地板 | 清晰 gap + 组合/适配框架;零新算法 | **可修复**:gap 陈述缺失(related_work.md 近空白),组合框架可写 |
| DL-forecasting 子领域 | 7–9 baselines、ablation、robustness、compute cost;30-run + Wilcoxon/Friedman | **远未达标** |
| 硬地板 | Funding/COI/Author Contributions/Data Availability 全(11/11);诚实 limitations(8/11) | **未写**,但 ARA v1→v4 负面证据链是诚实叙事资产 |

**结论**: Electronics 更匹配(方法学色彩 + CS/EE 读者 + 容错修改机制);Applied Sciences 需要补 sensitivity analysis + field case 叙事或大幅重构。两刊当前状态均不可直接投稿。

---

## 3. 7-Dimension Review

### 3.1 Novelty

**概述**: 本文主张的核心创新——双曲几何图权重建模电网层级结构用于负荷预测——在概念层面具有可命名的组合新颖性(hyperbolic graph + load forecasting 的组合在文献中确实罕见)。但实现层面存在致命的名实不符问题。

**Finding N1 — "Transformer" 名实不符**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious) |
| Confidence | 1.0 |
| Fixability | 0.8 |

- **证据**: `src/environment.md` 明确写 "Python standard library only";`src/configs/real_opsd_method_manifest.csv` 定义 HyG-LoadFormer 的 predictor 为 `hyperbolic_graph`,描述为 "Hyperbolic-distance graph aggregate plus temporal forecasting features"——这是 ridge 回归 + 图特征,不是 Transformer
- **影响**: Electronics distilled 显示 11/15 论文卖的是 ML 架构组合;审稿人问"每个组件是否有依据"。如果方法名暗示 Transformer 而实现中没有 attention/encoder-decoder 机制,这直接触发 soundness 质疑,不是 novelty 问题而是 credibility 问题
- **修复路径**: (a) 实现真实 Transformer/attention 组件(PyTorch);或 (b) 重命名为 "HyG-LoadForecast" 或 "HyG-RidgeForecast" 并如实描述方法

**Finding N2 — 组合创新未与文献建立差异化**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious) |
| Confidence | 0.95 |
| Fixability | 0.85 |

- **证据**: `logic/related_work.md` 仅两行指针("Comparator evidence source: ..."),无实际综述内容;无法确认"双曲图 + 负荷预测"组合是否真的无人做过
- **影响**: Electronics 要求"每个组件 justified",Applied Sciences 要求"clear gap statement + combination framing"。当前无法证明 gap 存在
- **修复路径**: 补三线综述(双曲表示学习/HGCN、时空 GNN 负荷预测、层级预测)并给出可命名的 gap

**Finding N3 — 基线强度不支撑 "+41.79%" 主张的证据等级**

| 属性 | 值 |
|---|---|
| Severity | 2 (moderate) |
| Confidence | 0.95 |
| Fixability | 0.7 |

- **证据**: OPSD 24h 最强基线为 Weekly-168h(MAPE 0.05632632)——这是一个简单的上周同小时复制,不是学习型模型。赢过 naive 季节基线 41.79% 与赢过 LSTM/PatchTST 3% 是完全不同的证据等级
- **影响**: Electronics floor 接受 self-only comparison,但 "+41.79%" 的 headline number 在缺少学习型基线对比时,可能被审稿人视为 inflated claim

---

### 3.2 Soundness

**Finding S1 — 基线退化/数值全同(技术缺陷)**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious) |
| Confidence | 1.0 |
| Fixability | 0.9 |

- **证据**: `evidence/tables/real_opsd_leaderboard.csv` 中:
  - 1h horizon: Euclidean-GCN Ridge、GCN-Temporal Ridge、Ablation-EuclideanGraph 三者所有指标(MAPE/MAE/RMSE/peak_load_error/sMAPE/nMAE)完全一致至 8 位小数(0.02250389/759.858453/1104.423455/1267.025034/0.02249442/0.00888464)
  - 1h horizon: AR-Calendar Ridge 与 Ablation-TemporalOnly 也完全一致(0.02275094/764.092653/1108.078541/1269.337012/0.02275382/0.00893414)
  - 24h horizon: 同样模式重复(Euclidean-GCN Ridge ≡ GCN-Temporal Ridge ≡ Ablation-EuclideanGraph;AR-Calendar Ridge ≡ Ablation-TemporalOnly)
  - SimBench 同样存在(Euclidean-GCN Ridge ≡ GCN-Temporal Ridge ≡ Ablation-EuclideanGraph)
- **影响**: 9 个名义方法去重后仅约 5 个独立比较点。这意味着:
  - "Euclidean-GCN Ridge" 和 "GCN-Temporal Ridge" 两个名称暗示不同的图结构,但产出完全相同的预测——要么图权重未生效(实现 bug),要么特征工程使得图结构差异在 ridge 回归中被消除
  - "Ablation-TemporalOnly"(移除所有邻居图特征)与 "AR-Calendar Ridge"(纯自回归+日历)产出相同——说明图特征在当前 ridge 框架中贡献为零
  - **这直接削弱了 ablation 的说服力**:如果 ablation 变体与基线数值全同,则无法分离组件贡献
- **修复路径**: 排查实现 bug(图权重是否在 ridge 特征中生效);确保每个 ablation/baseline 在数值上真正独立;若确实独立则解释数值巧合原因

**Finding S2 — 实现与声称方法的根本性不一致**

| 属性 | 值 |
|---|---|
| Severity | 4 (fatal) |
| Confidence | 1.0 |
| Fixability | 0.7 |

- **证据**: 全文标题含 "Graph Neural Forecasting"、方法全名 "Hyperbolic Graph Load Forecasting Transformer"、`logic/concepts.md` 定义 HyG-LoadFormer 为 "Hyperbolic Graph Load Forecasting Transformer"。但 `src/environment.md` 确认为 "Python standard library only",`real_opsd_config.json` 确认 ridge=1e-06 正则,`real_opsd_method_manifest.csv` 中所有方法(含 proposed)共享相同的 ridge 预测器框架,仅特征集不同
- **影响**: 方法的核心计算是 ridge 回归 + 手工特征工程(双曲距离加权邻居聚合 + 日历特征 + 滞后窗),不涉及任何梯度下降、反向传播、可学习参数(除 ridge 系数)、attention 机制或神经网络训练。称之为 "Neural"/"Transformer" 是技术性错误
- **修复路径**: (a) 用 PyTorch 实现真实的双曲图神经网络组件(Poincaré ball 上的可学习嵌入 + attention);(b) 或诚实地重新定位为 "hyperbolic graph-weighted feature engineering for ridge forecasting"

**Finding S3 — SimBench 1h 的门控退化**

| 属性 | 值 |
|---|---|
| Severity | 2 (moderate) |
| Confidence | 1.0 |
| Fixability | 0.6 |

- **证据**: `evidence/tables/real_simbench_leaderboard.csv`:SimBench 1h HyG-LoadFormer 与 Persistence 所有指标完全一致(MAPE 0.14812336,nMAE 0.04316202)——模型输出等于 persistence 复制,意味着门控机制将所有学习信号压制
- **影响**: SimBench 1h 作为第二数据集上的短时预测结果,完全失效。但这是已记录的 limitation,只要不在论文中主张即可

---

### 3.3 Experiments

**Finding E1 — 真实数据上零神经基线**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious) |
| Confidence | 1.0 |
| Fixability | 0.8 |

- **证据**: `logic/solution/method.md` 列出 9 个基线(ARIMA/XGBoost/LSTM/BiLSTM/TCN/Transformer/Euclidean-GCN/GCN-Transformer/CNN-LSTM),但这些仅出现在 `evidence/runs/synthetic_smoke_results.csv`(合成 smoke)。真实 OPSD/SimBench 基准中实际只有 Persistence、Seasonal-24h、Weekly-168h、MovingAverage-24h、AR-Calendar Ridge、Euclidean-GCN Ridge、GCN-Temporal Ridge 共 7 个基线——全部是 naive 或 ridge 级,无一为神经网络
- **影响**:
  - Electronics distilled 的 norm 是 ~3 baselines + component comparisons,floor 是 self-only comparison。形式上,7 个基线数量达标
  - 但 distilled 也显示 11/15 论文卖的是 ML 架构组合——如果 proposed 方法声称是 ML 架构,则 comparison class 应包含同代 ML 模型,否则无法验证"架构"的有效性
  - Applied Sciences DL-forecasting 子领域要求 7–9 baselines + ablation + robustness——远未达标
- **修复路径**: 在 OPSD + SimBench 真实数据上补充 LSTM、TCN(最低配)和 DLinear + PatchTST 或 Informer(达标配),统一输入特征与计算预算

**Finding E2 — Sensitivity analysis 完全缺失**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious for Applied Sciences); 2 (moderate for Electronics) |
| Confidence | 1.0 |
| Fixability | 0.85 |

- **证据**: 全部 evidence 文件中无曲率参数、邻居数 K、滞后窗长度、train ratio 的敏感性曲线。rolling 三个 ratio(0.55/0.65/0.75)提供了一定的 train ratio 稳定性证据,但不够独立成节
- **影响**:
  - Electronics:非强制,但加固 soundness 论证(当前实现仅 ridge=1e-6 一个超参,审稿人可能质疑该值的敏感性)
  - Applied Sciences:distilled 明确显示 sensitivity analysis 是该刊的"applied credibility 货币"(6/11 含),缺失是第一大修触发器
  - `JOURNAL_REVIEW.md` 第四节第 2 点已识别此缺口并列为 P0
- **修复路径**: 至少做曲率参数 ζ、邻居数 K、滞后窗 L、ridge 正则 λ 的扫描(单参数变化,固定其余),每个参数 5-7 个值,报告 OPSD 24h MAPE 响应曲线

**Finding E3 — 实验标题-证据不匹配(Smart Dispatch)**

| 属性 | 值 |
|---|---|
| Severity | 2 (moderate) |
| Confidence | 1.0 |
| Fixability | 0.95 |

- **证据**: 论文标题含 "Smart Dispatch Systems";`logic/experiments.md` 中 `dispatch_sensitivity` 实验状态为 "smoke-tested",证据仅有 `evidence/runs/synthetic_smoke_results.csv`——无真实调度实验
- **影响**: Electronics distilled 点名 "title–case-study mismatch" 风险;`JOURNAL_REVIEW.md` 已识别此问题
- **修复路径**: 删除标题中 "Smart Dispatch Systems" 或降级为 "toward dispatch-aware forecasting";若保留则补真实 dispatch 实验

**正面证据(可作为卖点)**:
- Rolling 时序切分 + `evidence/source/` 精确记录 train/test 边界(无 random split)——Electronics distilled 点名 "时序数据 random 90/10 切分泄漏" 是常见暗病,本文可反写为 soundness 卖点
- OPSD 24h rolling std = ±0.00055769(非常小)——稳定性证据强
- v1→v4 负面证据链完整保留——诚实叙事资产
- 多指标报告(MAPE/MAE/RMSE/sMAPE/nMAE/peak_load_error)——超过 Electronics ≥2 指标地板

---

### 3.4 Reproducibility

**Finding R1 — 超参披露接近零**

| 属性 | 值 |
|---|---|
| Severity | 2 (moderate) |
| Confidence | 0.9 |
| Fixability | 0.95 |

- **证据**: `real_opsd_config.json` 仅披露 ridge=1e-06;无曲率参数 ζ 值、邻居数 K 值、滞后窗长度、双曲嵌入维度、图构建阈值、特征工程细节。Electronics distilled 指出 "half-disclosed hyperparameters" 是 slip-through 风险
- **修复路径**: 将所有超参列表化(表或附录);引用 `evidence/source/*_source_profile.csv`;声明调参协议(仅在验证切分上做)

**正面证据**:
- 代码文件存在(`src/code/run_real_opsd_forecasting.py`、`src/configs/`)
- 确定性实现(ridge 回归 + 固定特征,无随机种子)——完全可复现
- 数据源精确记录(`evidence/source/real_opsd_source_profile.csv`:文件路径、行数、时间戳范围、国家列表、train_end_index/timestamp;SimBench 同理)
- Rolling 三比例切分方案完整记录

---

### 3.5 Related Work

**Finding RW1 — Related work 近空白**

| 属性 | 值 |
|---|---|
| Severity | 4 (fatal) |
| Confidence | 1.0 |
| Fixability | 0.85 |

- **证据**: `logic/related_work.md` 全文仅两行:"Comparator evidence source: `papers/literature/target_journal_related/comparison_analysis.md`." + "This project is project-original planned work and must remain separate from the external published-paper ARA collection."——无任何实际文献综述内容
- **影响**:
  - 两刊均要求 gap 陈述和文献定位。Electronics 审稿人需要确认"双曲图 + 负荷预测"的组合确实未被发表过
  - Applied Sciences 要求"clear gap statement + combination/adaptation framing"
  - 无法建立 novelty 主张的可信度(Finding N2 的根因)
- **修复路径**: 补写三线综述:
  1. **双曲表示学习/HGCN 谱系**: Nickel & Kiela 2017 (Poincaré embeddings)、Ganea et al. 2018 (Hyperbolic NN)、Chami et al. 2019 (HGCN)——建立双曲几何在图学习中的基础
  2. **时空 GNN 负荷预测**: STGCN (Yu et al. 2018)、MTGNN (Wu et al. 2020)、AGCRN (Bai et al. 2020)——建立 GNN 在负荷预测中的应用现状
  3. **层级/分层预测**: hierarchical reconciliation (Hyndman et al.)、coherent forecasting——建立层级预测的问题框架
  4. **Gap 陈述**: "No prior work combines hyperbolic graph representations with residual load forecasting for hierarchical grid structures"

---

### 3.6 Clarity

**Finding C1 — 主张边界未在论文中显式限定**

| 属性 | 值 |
|---|---|
| Severity | 2 (moderate) |
| Confidence | 0.95 |
| Fixability | 0.9 |

- **证据**: `logic/claims.md` 在 ARA 层面做了精确限定(C1/C2/C3 仅覆盖 day-ahead 24h,C4 为结构支撑);`PAPER.md` 的 Abstract 也写了 "1h forecasting remains a recorded limitation"。但 `logic/problem.md` 的下游任务仍写 "hierarchical short-term AND day-ahead power load forecasting"——short-term 包含了 1h
- **影响**: 如果论文正文(尤其 Introduction 和贡献列表)包含 short-term/1h 主张,将与证据矛盾
- **修复路径**: 摘要/贡献/结论严格限定为 day-ahead 24h;1h 进 Limitations 小节,措辞:"短时 1h 预测中,标准日历特征反而引入噪声(NoCalendar ablation 更优),本方法的层级图结构收益集中于日前尺度"

**Finding C2 — SimBench 指标选择的叙事风险**

| 属性 | 值 |
|---|---|
| Severity | 1 (minor) |
| Confidence | 0.85 |
| Fixability | 0.95 |

- **证据**: SimBench 24h 以 nMAE 为主指标(因为馈线近零负荷导致 MAPE 分母异常),但 MAPE 比 Weekly-168h 差 14.04%。`real_simbench_rolling_analysis.md` 已解释了 nMAE 选择的正当理由
- **修复路径**: 在论文中显式解释 SimBench 近零负荷分母导致 MAPE 不适用,同时在 Limitation 承认 MAPE 弱于 Weekly-168h

---

### 3.7 Ethics

**Finding Eth1 — 方法名暗示不存在的架构组件**

| 属性 | 值 |
|---|---|
| Severity | 3 (serious) |
| Confidence | 1.0 |
| Fixability | 0.8 |

- **证据**: "Transformer" 在全名和 "Neural" 在标题中出现,但实现中不存在。这不是数据造假(ARA 完整保留了负面证据链,`logic/solution/constraints.md` 明确禁止篡改),而是命名/定位的诚信风险
- **影响**: 如果被审稿人发现(在 Electronics 的 soundness 审查下概率高),会被视为 misleading representation,可能直接触发 reject
- **修复路径**: 同 Finding N1/S2——重命名或实现真实组件

**正面证据**:
- ARA 约束(`logic/solution/constraints.md`)明确禁止捏造或手动修改实验输出
- 完整的负面证据链(v1 weak、v3 gate rejected、SimBench v1 mixed、SimBench v2 gate rejected)全部保留
- 无数据篡改迹象(所有 CSV 文件为机器生成,数值链可追溯)

---

## 4. Aggregated RRI Estimate (0-100)

**RRI = 25 / 100**

计算逻辑(维度加权):

| 维度 | Weight (Electronics) | 当前达标度 | 加权得分 |
|---|---|---|---|
| Novelty | 0.15 | 20% (组合概念存在,但名实不符+无文献支撑) | 3.0 |
| Soundness | 0.25 | 15% (实现与声称严重不符+基线退化) | 3.75 |
| Experiments | 0.20 | 35% (2 数据集+rolling+多指标,但无神经基线+无 sensitivity) | 7.0 |
| Reproducibility | 0.10 | 55% (确定性+数据记录好,但超参披露不足) | 5.5 |
| Related Work | 0.10 | 5% (近空白) | 0.5 |
| Clarity | 0.10 | 45% (ARA 层面限定好,但论文层面有主张越界风险) | 4.5 |
| Ethics | 0.10 | 50% (命名诚信风险 vs 完整负面证据链) | 5.0 |
| **合计** | **1.00** | | **29.25 → 调整为 25** |

下调至 25 的理由:Finding S2(实现与声称方法的根本不一致)是一个系统性缺陷,影响 novelty/soundness/clarity/ethics 四个维度,存在维度间的级联风险。如果审稿人发现"Transformer" 名不副实,其他所有数字的可信度都会被连带质疑。

**P0 完成后的预估 RRI**: 55-65(可达 minor revision 区间)
**P0+P1 完成后的预估 RRI**: 70-80(accept 概率显著)

---

## 5. Predicted Decision

### 当前状态投稿 → **Reject**(两刊均)

- **Electronics**: reject 概率 ~85%。审稿人会在第一轮发现:
  1. "Transformer/Neural" 名称与实际 ridge 回归实现不符(soundness fatal)
  2. 零神经基线(experiments serious)
  3. Related work 空白或缺失(novelty unverifiable)
  4. 基线数值退化(技术 rigor 质疑)
- **Applied Sciences**: reject 概率 ~90%。额外触发:
  1. 零 sensitivity analysis(该刊"applied credibility 货币")
  2. 无 field case / 无受益方命名
  3. DL-forecasting 子领域要求 7-9 baselines

### 完成 P0 后投稿 → **Major Revision → Accept**(Electronics)

Electronics 有 1-2 轮修改机会(非 IEEE Access 的二元裁决),容错性更好。完成 P0(真实神经组件或重命名 + 神经基线 + sensitivity + related work + 主张边界)后,论文的核心主张(OPSD 24h +39-42% 改进)有了更强的证据支撑,符合 distilled 的 acceptance profile。

---

## 6. Top-3 Actionable Revisions (P0 / P1 / P2)

### P0 — 投稿前必须完成

**P0-1: 解决方法名-实现不一致 + 补神经基线(解决 S2/N1/E1)**

**具体行动**:
1. **二选一**(推荐选项 a):
   - (a) 用 PyTorch 实现真实的双曲图组件:Poincaré ball 上的可学习节点嵌入 + 双曲距离注意力/aggregation,替换当前 ridge 特征。保留 hyperbolic graph 的核心创新,但使其成为真实的可学习模块
   - (b) 重命名为 "HyG-LoadForecast"(删除 "Former"/"Transformer"/"Neural"),在方法节如实描述为 hyperbolic-distance-weighted feature engineering for ridge regression
2. **补真实数据上的神经基线**(最低配): LSTM(单/双层,hidden=64/128)、TCN 或 vanilla Transformer(标准库实现即可)
3. **达标配**: DLinear(Zeng et al. 2023)+ PatchTST(Nie et al. 2023)或 Informer(Zhou et al. 2021)——这些是负荷预测社区的当代基准
4. **统一 fairness**: 所有方法使用相同输入特征(滞后窗+日历+图特征如适用),相同 train/val/test 切分,报告训练时间和参数量
5. **神经运行 ≥3 seeds 报 mean±std**

**验证标准**: 基线表中至少包含 3 个学习型模型(非 naive/ridge),且 HyG-LoadFormer 在 OPSD 24h 上仍优于最强学习型基线

**P0-2: 修复基线退化 + 补 sensitivity analysis(解决 S1/E2)**

**具体行动**:
1. **排查基线退化根因**: Euclidean-GCN Ridge ≡ GCN-Temporal Ridge ≡ Ablation-EuclideanGraph 数值全同。检查:
   - 图权重矩阵是否在 ridge 特征构建中实际生效
   - 是否因 ridge 正则过强(1e-6 实际很小)导致图特征系数被压零
   - 特征工程中图特征列是否被其他特征线性覆盖
2. **确保每个方法在数值上独立**:若两个方法产出相同预测,要么合并为一行,要么修复实现使差异显现
3. **Sensitivity analysis**(至少 4 个参数):
   - 曲率参数 ζ ∈ {-0.1, -0.5, -1.0, -2.0, -5.0}(或 learnable curvature 的初始值)
   - 邻居数 K ∈ {3, 5, 10, 15, 20, 30}
   - 滞后窗 L ∈ {6, 12, 24, 48, 72, 168}
   - Ridge 正则 λ ∈ {1e-8, 1e-6, 1e-4, 1e-2, 1, 10}(若保持 ridge 框架)
   - 每个参数固定其余,报告 OPSD 24h MAPE 响应曲线(线图或表格)

**P0-3: 补 related work + 限定主张边界 + 修正标题(解决 RW1/C1/E3)**

**具体行动**:
1. **补写 related work 三线综述**(约 1.5-2 页):双曲表示学习、时空 GNN 负荷预测、层级预测;以可命名的 gap 收尾
2. **标题修改**: 删除 "Smart Dispatch Systems",改为如:
   - "Hyperbolic Graph-Based Day-Ahead Hierarchical Power Load Forecasting"
   - 或 "Day-Ahead Hierarchical Load Forecasting via Hyperbolic Graph Neural Networks"(若实现了真实神经组件)
3. **主张边界**: 摘要/贡献/结论只写 day-ahead 24h;1h 和 SimBench MAPE 进 Limitations 小节
4. **贡献列表**: 3-4 条编号贡献,soundness 框架措辞:
   - (1) 提出双曲图权重建模电网层级结构的 day-ahead 负荷预测方法
   - (2) 在 OPSD 6 国数据上实现 day-ahead MAPE 0.039(对最强学习型基线改进 X%)
   - (3) 通过 5 方向 ablation 分离组件贡献
   - (4) 提供完整可复现基准(公开数据 + rolling 时序切分 + 全证据链)

### P1 — 大幅降低大修概率

**P1-1: 扩展数据集**
- 补 Panama 负荷数据(已本地缓存,小时级+气象+官方预调度划分)——作为第 3 数据集,验证跨域泛化
- 补 Monash AEMO(已本地缓存,五州天然层级)——直接支撑 hierarchical 主张
- 预计工作量: 2-3 天

**P1-2: 统计加固**
- Diebold-Mariano 检验(Proposed vs 最强基线)——forecasting 论文低成本加固
- 若神经组件实现,加 ≥5 seeds mean±std + 显著性

**P1-3: MDPI 硬格式**
- Funding / COI / Author Contributions / Data Availability 四件套
- MDPI 模板 + IMRaD + 编号引用
- 自引克制

### P2 — 增强项,不阻塞投稿

- GEFCom2014 / ISO-NE 扩展实验
- 真实 dispatch sensitivity 下游实验(若保留调度叙事)
- 开源代码/数据包(MDPI Data Availability 直接引用)
- NSRDB 气象接入使 weather_aware ablation 落到真实数据

---

## 7. Allowable Modifications (fast-OA priority)

### 7.1 Algorithm framework changes

**允许范围**(保持"双曲图神经负荷预测"总方向):

| 修改 | 允许度 | 理由 |
|---|---|---|
| 从 ridge 回归升级为 PyTorch 可学习双曲图模块 | **强烈推荐** | 解决 S2/N1 致命问题;保持双曲图核心创新 |
| 添加 Transformer/attention 组件 | **推荐** | 使 "LoadFormer" 名实相符;符合 Electronics 11/15 ML 架构画像 |
| 替换为其他 GNN backbone(GAT/GraphSAGE) | **允许** | 保持图结构创新;双曲距离加权可叠加在任何 GNN 上 |
| 简化为纯 feature engineering 并重命名 | **允许但不推荐** | 降低 novelty 至 Electronics 地板边缘;但更快投稿 |
| 完全放弃双曲几何 | **不允许** | 偏离总方向 |

**推荐路径**: PyTorch 实现 Poincaré ball embedding + 双曲距离 attention/aggregation + residual forecasting head。这保留了全部创新 Handles(`logic/solution/method.md` 中的三个:hyperbolic geometry for hierarchy、ablation separation、dispatch link),同时使方法成为真实的 ML 架构。

### 7.2 Dataset changes

**允许范围**:

| 修改 | 允许度 | 理由 |
|---|---|---|
| 保留 OPSD + SimBench 为核心 | **必须** | 已有完整证据链 |
| 添加 Panama(已缓存) | **强烈推荐** | 小时级+气象+官方划分+外部基线 |
| 添加 Monash AEMO(已缓存) | **推荐** | 五州天然层级,支撑 hierarchical 主张 |
| 添加 ETTh1(已缓存) | **可选** | 社区熟悉基准,可换来可比性 |
| 替换 OPSD 为其他负荷数据 | **不推荐** | OPSD 6 国多层级是本文最强证据 |
| GEFCom2014 | **P2 增强** | 最权威竞赛基准,但需注册获取 |

### 7.3 Downstream task changes

**允许范围**:

| 修改 | 允许度 | 理由 |
|---|---|---|
| 限定为 day-ahead 24h 层级负荷预测 | **必须** | 唯一强信号范围 |
| 删除 dispatch sensitivity 叙事 | **强烈推荐** | 当前仅有 smoke 证据;标题中去掉 |
| 添加 probabilistic forecasting(置信区间) | **可选增强** | 若神经组件实现,MC dropout 或 ensemble 可低成本添加 |
| 改为 multi-horizon(1-24h 全报告) | **不推荐** | 1h 是 limitation,不应扩展 |
| 添加 peak load forecasting 专项 | **可选增强** | peak_load_error 已在指标中,可独立成表 |

---

## 8. Honest Boundary

**本评审不做以下事情**:

1. **不发明未记录的发现**:所有 finding 均引用 ARA 证据文件路径。未检查的文件(如 `evidence/figures/`、`evidence/runs/real_opsd_forecasting_results.csv` 逐行数据)可能包含未在本评审中反映的信息
2. **不预测具体审稿人行为**:RRI 和 predicted decision 基于 distilled 标准的统计规律,非个体审稿人画像。单篇稿件的结果受 Section Editor、Guest Editor、具体 reviewer 分配影响
3. **不替代投稿后的 revision 策略**:本评审聚焦投稿前缺口;实际审稿意见可能揭示未预见的问题(如特定 reviewer 对双曲几何的理论质疑)
4. **不评估写作英文质量**:未看到完整论文正文(仅有 PAPER.md 的 title/abstract/status),英文水平和学术写作规范需要在完稿后另行检查
5. **不保证 "+41.79%" 在补神经基线后保持**:当前 headline number 是对 naive Weekly-168h 基线的改进;补 LSTM/PatchTST 后改进幅度大概率大幅缩小(可能 3-10%)。这是证据等级的正常调整,不影响方法有效性——但需要在论文中如实呈现

**本评审的核心判断**:
- 论文的 **24h/day-ahead 信号是真实的、可防御的**(OPSD +39-42% 对最强 naive 基线,rolling ±0.00056 极稳定)
- 论文的 **证据诚实性是资产**(v1→v4 完整保留,失败变体记录在案)
- 论文的 **当前包装与实现存在系统性不一致**(命名、基线退化、related work 空白)——这些是可以通过 P0 修复的,但必须在投稿前修复

---

## 9. Fastest Path to Submission

**目标: 4-6 周内投稿 MDPI Electronics**

### Week 1-2: 核心重构(P0-1)

1. **决策**: 升级 PyTorch 实现(选项 a)还是重命名(选项 b)
   - 推荐选项 a:PyTorch Poincaré ball + 双曲距离 attention。约 5-7 天实现+调试
   - 若选 b:1 天内完成重命名+方法描述重写,但后续需要更多实验弥补 novelty 降低
2. **补神经基线**: LSTM + TCN + DLinear + PatchTST,统一输入,在 OPSD + SimBench 上运行。约 3-5 天
3. **修复基线退化**: 排查 Euclidean-GCN ≡ GCN-Temporal 根因。约 1-2 天

### Week 3: Sensitivity + 扩展(P0-2 + P1-1)

4. **Sensitivity analysis**: 4 参数扫描,OPSD 24h MAPE 响应曲线。约 2-3 天
5. **Panama 数据集**: 接入已缓存数据,运行 proposed + 基线。约 2-3 天
6. **Neural runs ≥3 seeds**: 均值±std 统计。约 1 天(并行训练)

### Week 4: 论文写作(P0-3)

7. **Related work 三线综述**: 约 2 天
8. **标题/摘要/贡献/limitations 定稿**: 约 1 天
9. **Method 节完整描述**(含超参表、切分协议、fairness statement): 约 2 天
10. **MDPI 四件套 + 格式**: 约 1 天

### Week 5: 内部审查 + 投稿

11. **全文英文润色**: 约 2-3 天
12. **内部一致性检查**(所有数字与 evidence CSV 对齐): 约 1 天
13. **投稿**: MDPI Electronics,Section: Artificial Intelligence 或 Power Electronics
14. **选 SI**: 检查当前 open Special Issues,找 on-scope 的 AI-for-power 类 SI

### 投稿后预期

- **首决**: ~15 天(MDPI Electronics 中位数)
- **预期结果**: Major Revision(概率 ~50%)或 Minor Revision(概率 ~30%)
- **修改轮**: 1-2 轮,每轮 ~10-14 天窗口
- **从投稿到 accept**: 预估 6-10 周(若顺利)
- **APC**: CHF 2,400(~$2,650)

### 若 Electronics reject → 改投路径

1. **Applied Sciences**(备选):需额外补 sensitivity analysis(若 P0-2 已完成则可直接改投)+ 添加 applied-value 叙事(命名受益方:"grid dispatchers can use…")
2. **MDPI Energies**:需 sensitivity analysis(必须)+ 更强能源叙事;注意 p3/p4 已投 Energies,避免同期扎堆
3. **IEEE Access**:仅在 P0+P1+P2 全完成、稿件近终稿时考虑(二元裁决,无修改机会)
