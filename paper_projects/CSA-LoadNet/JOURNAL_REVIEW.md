# mintou_p2 (HyG-LoadFormer) 期刊评审与修改完善方案

评审日期: 2026-07-13。评审基准: IEEE Access / MDPI Energies 两刊 SKILL.md 中的 "Distilled review standards"，结合 mintou_p2 ARA 工程全部证据文件。

---

## 一、论文概况

HyG-LoadFormer 是一个用双曲几何图权重建模电网层级结构的负荷预测方法，在 OPSD（多国 60 分钟负荷）与 SimBench（馈线/负荷 profile）两个公开数据集上完成固定切分 + rolling 时序切分基准。**关键事实：24h/day-ahead 是强信号，1h 是弱项。** OPSD 24h 固定切分 MAPE 0.03972575 vs 最强基线 Weekly-168h 0.05632632（+41.79%），rolling 均值 0.03931968±0.00056 vs 0.05471780（+39.16%），且对最强 ablation 的增益达 74.07%（固定）/79.59%（rolling），组件贡献可分离；SimBench 24h 归一化 MAE 固定 +3.59%、rolling +5.15%。但 OPSD 1h 仅比最强基线好 0.25%（rolling 反而 -1.30%），且**始终输给自己的 NoCalendar ablation**（固定 -7.85%、rolling -15.71%，`rolling_limitation`）；SimBench 1h 被门控为与 Persistence 完全相同（增益 0.00%），SimBench 24h MAPE 比 Weekly-168h 差 14.04%（仅归一化 MAE 占优，因馈线 profile 存在近零负荷分母，nMAE 作主指标有正当理由但必须解释）。ARA 完整保留了 v1 weak（OPSD 24h 曾 -18.49%）、v2 mixed、v3 gate 被否（gate 损害 1h/固定切分）、SimBench v1 mixed（1h 曾 -36.70%）、v2 gate 被否（24h nMAE 曾 -12.43%）的负面证据链，这是诚实叙事的资产。

---

## 二、期刊匹配度对比

### IEEE Access — Fit: **Medium**（修复 P0 后可升 Medium-High）

- **有利**：范围完全命中（power & energy × AI 是 Access 最大体量领域之一）；soundness-not-novelty 标准下，"组合式创新（双曲图 + 时序预测）+ 完整实验" 正是其接受画像——distilled 显示 4 篇全文样本全部是组件组合/场景适配；已接收 DL 论文惯例为 4–6 个基线、零显著性检验、零多次运行，本文形式上可达标；rolling 时序切分 + `evidence/source/` 记录精确 train/test 边界，恰好避开 distilled 点名的"时序数据 random 90/10 切分泄漏"这一常见暗病，反而可以写成 soundness 卖点。
- **不利**：**二元 accept/reject、无大修回合**——论文必须投稿即近终稿，而当前证据链有硬伤：真实数据上零神经基线（详见第四节）、方法名 "LoadFormer/Transformer" 与纯标准库 ridge 级实现不符（distilled 指出评审看"方法是否正确完整可复现"，名实不符会直接触发 rigor 质疑）、超参披露目前为零（distilled 点名 near-zero hyperparameter disclosure 是暗病，自查项）。APC ≈ $2,160 也高于 MDPI Electronics。另外组合内 p1、p5 已投 IEEE Access，再加一篇会集中审稿风险。
- **结论**：现在投必被 reject（一次 reject 后仅剩一次 resubmission 机会）；完成 P0 后才值得考虑。

### MDPI Energies — Fit: **Medium-High**（scope 最好，但预测类专属门槛未满足）

- **有利**：能源相关性零疑问（层级负荷预测 + 调度应用），是 Energies 电力系统 Section 的正中心；distilled（34 篇电力全文）显示 novelty 地板是"可命名的机制组合 + gap 陈述"，≤5% 增益诚实报告即可通过——本文 OPSD 24h +39~42% 远超地板，SimBench +3.6~5.2% 也够；不要求显著性检验（0/29）、不要求开源代码（1/34）、不要求 30 次运行。
- **不利**：**distilled 明确写了预测类论文门槛更高：≥3 baselines + 组件对比 + 多指标 + sensitivity analysis（近强制，缺失是第一大修触发器）**。本文多指标（MAPE/MAE/RMSE/sMAPE/nMAE/peak_load_error）✓、组件对比（7 个 ablation 方向，真实数据上 5 个）✓、基线数量形式上 ✓，但**基线强度不够**（全是 naive/ridge 级，见第四节）且**sensitivity analysis 完全缺失**（曲率、邻居数、滞后窗、train ratio 均无敏感性扫描）——这一条在 Energies 是接近必挂的大修点。另外 Energies distilled 点名"title–case-study mismatch"是已发表论文的遗留毛病：本文标题含 "Smart Dispatch Systems"，而 `dispatch_sensitivity` 实验目前仅 smoke-tested（`evidence/runs/synthetic_smoke_results.csv`），投 Energies 前必须补真实调度敏感性实验或改标题。
- **组合考虑**：p3、p4 已投 Energies，同批次三篇同一 MDPI 期刊会放大编辑部关联审视。

### 现目标 Electronics 是否更合适 — **是，建议保留**

Electronics 面向 CS/EE 方法读者，"双曲几何 + 图神经预测" 这种方法学色彩的贡献在 Electronics 的 AI/computational-intelligence Section 比在 Energies（要求能源应用叙事优先）更自然；MDPI 共同模型下无二元一票否决，有 1–2 轮修改机会，容错优于 IEEE Access；APC 低于 Access；且保留 Electronics 维持组合的期刊分散（Access×2、Energies×2、AppliedSci×1、Electronics×1）。**最终推荐：保留 Electronics 为第一目标；若追求能源领域引用与影响，Energies 为改投首选（需先补 sensitivity analysis + 强基线）；IEEE Access 仅在 P0+P1 全部完成、稿件近终稿时作为选项。**Applied Sciences 继续作兜底备选。

---

## 三、写作修改清单

对照两刊惯例与 ARA 薄弱点：

1. **主张边界（最重要）**：全文主 claim 严格限定为 **day-ahead/24h 层级负荷预测**（对应 claims.md C1/C2/C3 的 supported 范围）。1h 结果写入 Limitations 小节，措辞建议："短时 1h 预测中，标准日历特征反而引入噪声（NoCalendar ablation 更优，rolling -15.71%），本方法的层级图结构收益集中于日前尺度；短时预测留待未来引入专门的短时特征/模型"。**绝不能**把 1h 写进贡献列表或摘要。SimBench 一律以 normalized MAE 陈述并解释近零分母导致 MAPE 不适用（`real_simbench_rolling_analysis.md` 已有依据），同时在 Limitation 承认 24h MAPE 弱于 Weekly-168h（-14.04%）。
2. **标题**：删除或降级 "Smart Dispatch Systems"（dispatch_sensitivity 仅 smoke 证据），改为如 "…for Day-Ahead Hierarchical Power Load Forecasting"，否则 Energies/Access 均有 title–evidence mismatch 风险。
3. **方法名与实现对齐**：当前实现是标准库 ridge 级双曲距离加权特征模型（`src/environment.md`: "Python standard library only"），却叫 "LoadFormer/Transformer"。二选一：(a) 补真正的 Transformer 训练实现；(b) 重命名/改写方法描述为 hyperbolic graph-weighted forecasting，删掉 Transformer 措辞。IEEE Access 的 soundness 审查下这是致命项，MDPI 下也是大修项。
4. **贡献列表**：按 Access 惯例写 3–6 条编号贡献；按 soundness 框架措辞（"系统评估/可复现基准/组件分离"），不写 "first time in literature" 式高调 novelty。
5. **related_work.md 目前近乎空白**（只有一行 comparator 指针）——必须补齐三线综述：双曲表示学习/HGCN 谱系、时空 GNN 负荷预测（STGCN/MTGNN 类）、层级/分层预测（hierarchical reconciliation），并明确 gap 陈述（Energies novelty 地板要求"可命名的组合确实没人做过"）。
6. **诚实叙事资产化**：把 v1→v4 的 residual 精化路径、被拒绝的 validation-gate 变体写进 Discussion（"我们尝试了全局验证门控，它损害了 24h 信号故被弃用"），两刊 distilled 都显示诚实的 limitation 陈述是加分项。
7. **超参与协议披露**：滞后窗、邻居数、曲率、ridge 正则系数、train/val/test 边界（引用 `evidence/source/*_source_profile.csv`）全部列表化；显式声明所有调参只在验证切分上做（constraints.md 已有此纪律，写进论文）。
8. **公平性声明**：仿照 Access distilled 中 2/4 论文的做法，加一段统一计算预算/特征输入对齐的 fairness statement。
9. **MDPI 硬地板**（若投 MDPI 系）：Data Availability / Funding / COI / Author Contributions 四件套齐全；自引克制；MDPI 模板 + IMRaD + 编号引用。

---

## 四、实验设计缺口

1. **神经基线缺失（最大缺口）**：`logic/solution/method.md` 列的 9 个基线（ARIMA/XGBoost/LSTM/BiLSTM/TCN/Transformer/Euclidean-GCN/GCN-Transformer/CNN-LSTM）**只存在于合成 smoke 矩阵**；真实 OPSD/SimBench 基准里实际只有 Persistence、Seasonal-24h、Weekly-168h、MovingAverage-24h、AR-Calendar Ridge、Euclidean-GCN Ridge、GCN-Temporal Ridge 共 7 个 naive/ridge 级基线——且 leaderboard 显示 Euclidean-GCN Ridge、GCN-Temporal Ridge、Ablation-EuclideanGraph 三者数值完全相同（8 位小数一致），AR-Calendar Ridge 与 Ablation-TemporalOnly 也相同，**去重后有效独立基线只有约 5 个，无一为神经网络**。Energies 预测类 "≥3 baselines" 形式满足但强度不够；Access DL 惯例 4–6 baselines 指的是同代神经模型。**必须在真实数据上补：LSTM、TCN/Transformer（最低配），DLinear + PatchTST 或 Informer（达标配）**。这也直接决定 "打赢 Weekly-168h +39%" 这一主数字的说服力——赢过 naive 季节基线 39% 与赢过 PatchTST 3% 是完全不同的证据等级。
2. **Sensitivity analysis 缺失**：Energies 近强制项（缺失=第一大修触发器）。至少做：曲率参数、邻居数 K、滞后窗长度、train ratio 的敏感性曲线；rolling 三个 ratio（0.55/0.65/0.75）可以并入但不够独立成节。
3. **时序泄漏自查（当前是优势，要显式写出）**：固定切分为时间顺序切分、rolling 为前向时序窗，`evidence/source/` 记录了精确边界——通过自查。需在论文中明确声明无 random split、归一化统计只用训练段拟合。这是 Access distilled 点名暗病的反面卖点。
4. **多 seed / 显著性**：当前 ridge 类实现是确定性的，rolling ±std 已是合格的稳定性证据（OPSD 24h ±0.00056 非常小，可作卖点）；但一旦补入神经基线/神经实现，需 ≥3–5 seeds 报均值±std，建议加 Diebold–Mariano 检验（两刊都不强制，但 forecasting 论文加 DM 是低成本加固）。
5. **Ablation 覆盖**：真实数据上 5 个 ablation 方向可用（FixedCurvature/EuclideanGraph/TemporalOnly/NoCalendar/EqualNeighbors），满足"组件对比"要求；但 no_weather_features、poincare_only、short_horizon_only 仍只有 smoke 证据，论文中不得引用。
6. **dispatch_sensitivity / cross_region_transfer / missing_node_robustness / weather_aware_extension 均仅 smoke**：要么补真实实验，要么从论文叙事中整体移除（尤其 dispatch，见标题问题）。

---

## 五、数据集缺口（含本地缓存核实）

**核实结果：用户记忆中 "p2 forecasting benchmarks missing locally" 已过时。** `CACHE_STATUS.md`（2026-07-12 更新）与 `data/public_datasets/time_series_market/load_forecasting_benchmarks/` 实测确认以下已本地缓存：

| 已缓存（2026-07-12） | 说明 |
|---|---|
| ETTh1.csv / ETTm1.csv | ETT 变压器数据，Informer/PatchTST 系标准基准 |
| uci_household_power_consumption.zip | UCI 法国单户 1-min 2006–2010 |
| uci_tetouan_power_consumption.zip | 摩洛哥 Tétouan 三区 10-min 含气象 |
| australian_electricity_demand_dataset.zip | Monash 版 AEMO 五州半小时负荷 |
| panama_load/ | 巴拿马全国小时负荷+气象+官方预调度预测（自带 train/test 划分） |
| elia_total_load_2022.csv | 比利时 Elia 15-min 全年 |
| psml、opsd_time_series、simbench | 早已缓存 |

**仍缺**：GEFCom2012/2014（负荷预测领域最权威竞赛基准，需注册获取，Energies/Access 审稿人最可能点名）、ISO-NE 公开负荷（zone 级层级结构与本文"hierarchical"主张天然匹配）、NSRDB 气象（仅 API-ready，weather_aware 实验需要）。

**建议**：从已缓存池中选 1–2 个补充数据集即可满足"≥2 数据集"以上的泛化性要求——首选 **Panama**（小时级、含气象、自带官方划分、且有官方预调度预测可作强外部基线）与 **Monash AEMO**（五州天然层级结构，直接支撑 hierarchical 主张）；ETTh1 可加做一个横向可比实验（社区对 ETT 上各 SOTA 数字熟悉，能免费换来可信度）。GEFCom 列为 P2 增强项，不阻塞投稿。

---

## 六、优先级行动清单

### P0（投任何一刊前必须完成）
1. 在 OPSD + SimBench 真实数据上补神经基线：LSTM、TCN/Transformer 最低配；DLinear + PatchTST（或 Informer）达标配；统一输入特征与计算预算并写 fairness 声明。
2. 解决方法名与实现的名实不符：补真实 Transformer 组件训练，或重命名并如实描述方法。
3. 补 sensitivity analysis（曲率、K、滞后窗、train ratio）——Energies 强制项、Access soundness 加固项。
4. 主张边界定稿：摘要/贡献/结论只写 day-ahead 24h；1h 与 SimBench MAPE 进 Limitations；标题去掉 "Smart Dispatch Systems" 或补真实 dispatch 实验。

### P1（大幅降低大修/拒稿概率）
5. 增加 Panama + Monash AEMO（已本地缓存）作为第 3、4 数据集；Panama 官方预调度预测作外部基线。
6. 神经运行加 ≥3 seeds 均值±std；加 Diebold–Mariano 检验。
7. 修复退化重复基线（Euclidean-GCN Ridge ≡ GCN-Temporal Ridge ≡ Ablation-EuclideanGraph 数值全同），使基线表每行真正独立。
8. 补写 related_work（双曲 GNN、时空 GNN 负荷预测、层级预测三线），给出可命名的 gap。
9. 超参、切分边界、调参协议全披露；引用 `evidence/source/` profile。

### P2（增强项，不阻塞投稿）
10. GEFCom2014 / ISO-NE 扩展实验；NSRDB 气象接入使 weather_aware 与 no_weather ablation 落到真实数据。
11. 真实 dispatch sensitivity 下游实验（若想保留调度叙事）。
12. 开源代码/数据包（Access reproducibility initiative 加分；MDPI Data Availability 直接引用）。

### 投稿决策树
- 完成 P0 → **投 Electronics（保留现目标）**；
- 完成 P0+P1 且希望能源领域影响 → 改投 **Energies**（注意选对 Section/SI，避开与 p3/p4 同期扎堆）；
- 完成 P0+P1+P2、稿件近终稿且接受二元裁决与 $2,160 APC → 才考虑 **IEEE Access**。

---

## 进展更新（2026-07-13）

**P0-神经基线已补齐**（`src/powergrid_benchmark/mintou_neural_forecasting.py`，`public_data_benchmark_v5_neural_baselines`）：MLP、LSTM、TCN、DLinear、PatchTST-lite 五个真实 PyTorch 基线，在与 stdlib 管线**完全相同**的 70% 时序切分与完整测试集上训练评估（per-series z-norm、Adam/MSE、时序早停、每模型 3 种子、逐种子结果保留）。合并排行榜见 `evidence/tables/real_{opsd,simbench}_combined_leaderboard.csv`，分析见 `evidence/runs/real_neural_baselines_analysis.md`。

**结果（决定性，必须如实面对）**：
- **MLP 在全部四个设置排第一**；HyG-LoadFormer 在 OPSD 24h（原主张场景）落后最优神经基线 **14.6%**、OPSD 1h 落后 55.6%、SimBench 1h/24h 各落后 21.2%/23.6%。
- 局部亮点：OPSD 24h 上 HyG-LoadFormer（rank 4/18）仍胜过 DLinear（-2.7%）与 LSTM；stdlib 家族内它仍是最优。
- 神经基线是 CPU 有限预算训练（有界 epochs + 训练采样步长），GPU 调参版只会更强——差距是下界而非上界。

**对投稿主张的直接后果**：原 24h "strong signal" 主张在神经基线面前不成立。两条出路（分析文件中已写明，不允许沉默省略）：
1. **方法升级（推荐）**：把 HyG-LoadFormer 从 ridge 实现升级为真实神经实现（双曲图注意力 + 时序编码器），在同一协议下重跑——这同时解决"方法名与实现不符"的 P0；升级后能否胜过 MLP/PatchTST 决定论文生死。
2. **重新定位**：改为"轻量可解释图特征方法"叙事，如实报告神经基线为性能上界参考——但 OPSD 24h 仅胜 DLinear 一档，该叙事的证据偏薄，desk-reject 风险仍高。

在方法升级完成前，**p2 不应投稿**；投稿决策树中"完成 P0 → 投 Electronics"的前提已更新为含本项。

---

## 进展更新 2（2026-07-13 晚，方法升级完成）

**HyG-LoadFormer 已升级为真实神经实现**（`src/powergrid_benchmark/mintou_hyg_neural.py`，`public_data_benchmark_v6_hyg_neural`）：Poincaré 球序列嵌入 + 目标自适应曲率（softplus 可学习）双曲图注意力 + 共享时序 MLP 编码器（与 MLP 基线同参数量级），5 个消融为该模型上的真实机制开关。协议与神经基线完全一致；ridge 旧实现保留在排行榜 stdlib 家族中以示透明。合并排行榜已重生成（`real_{opsd,simbench}_combined_leaderboard.csv`），分析见 `real_hyg_neural_upgrade_analysis.md`。

**外部竞争力已恢复（3/4 设置胜过全部外部基线）**：
| 设置 | 神经 HyG | 最优外部基线 | 差距 |
|---|---|---|---|
| OPSD 24h（主claim） | 0.03327 MAPE | MLP 0.03394 | **+2.04% 胜** |
| SimBench 1h | 0.03326 nMAE（rank 1/24） | MLP 0.03403 | **+2.33% 胜** |
| SimBench 24h | 0.05854 nMAE | MLP 0.05979 | **+2.14% 胜** |
| OPSD 1h | 0.01055 MAPE（rank 3/24） | MLP 0.00996 | -5.60% 负（维持 limitation 定位） |

**新的关键缺口（组件证据）**：双曲图注意力的组件贡献未被证明——OPSD 24h 上 NoCalendar 消融反超 5.07%、SimBench 24h 上 TemporalOnly（完全去图）反超 1.85%，多数消融与完整方法的差距在种子噪声（seed-std ≈0.0015-0.025）之内。3 种子不足以给组件下结论。**投稿前必须做**：
1. 种子扩到 10+，对 proposed vs 各消融跑显著性检验——若双曲组件仍无显著贡献，标题与贡献主张须降格（如从 "Hyperbolic Graph" 转向 "cross-series attention"）或换更能体现图结构价值的数据；
2. 推荐路径：接入本地已缓存的 **Ausgrid solar home（300 户，天然层级结构）** 作第三数据集——6 国/8 馈线的池太小，图聚合无从发力；层级客户聚合正是 "hierarchical power load" 标题承诺的场景；
3. 主张边界更新：24h day-ahead + SimBench 全 horizon 胜出为主 claim，OPSD 1h 维持 limitation。

**结论**：p2 从 "不可投" 恢复到 "外部基线达标、组件叙事待补"，距可投还差组件显著性证据（或叙事降格）。

---

## 进展更新 3（2026-07-14，v7 显著性 + Ausgrid 层级基准）

**已完成**（`mintou_hyg_significance.py`，`public_data_benchmark_v7_seed_significance_ausgrid`）：HyG 6 变体 + MLP 扩到 10 种子（OPSD/SimBench）；新增 Ausgrid solar home 层级基准（12 户最大用电完整客户 + 4 邮编区域聚合 + 系统总量 = 17 序列，3 年小时化 GC 数据，24h day-ahead，主指标 sMAPE——层级尺度差 100 倍，range-normalized MAE 会被大序列主导）；Mann-Whitney U + Holm 显著性表（`tables/real_p2_v7_significance.csv`）与分析（`runs/real_p2_v7_significance_analysis.md`）。

**10 种子最终裁决（如实）**：
1. **主 claim 幸存且升级为显著**：OPSD 24h 上 HyG 显著优于 MLP（p_holm=0.0085）且显著优于 TemporalOnly 去图消融（p=0.0011）——"跨序列聚合对日前国家级负荷预测有效"这一点站住了。
2. **双曲组件主张不成立**：在全部 5 个 数据集×horizon 设置中，双曲 vs 欧氏距离 vs 等权邻居 vs 固定曲率**全部不可分**（p_holm 全为 1 或接近 1）。有效的是"聚合"本身，不是双曲几何、可学习注意力或自适应曲率。
3. **层级数据集上更糟**：Ausgrid 24h 上 HyG 显著输给 DLinear（p=0.0044），与 MLP/TCN/PatchTST 不可分且均值趋势更差——为双曲几何设计的场景反而没有优势。
4. OPSD 1h 显著输 MLP（确认 limitation）；SimBench 两个 horizon 与 MLP 不可分。

**对投稿的最终结论（二选一，不允许拖着不选）**：
- **A. 主张降格重写（可较快投稿）**：论文改为"跨序列聚合的日前负荷预测"（cross-series aggregation），标题去掉 Hyperbolic，主 claim 锚定 OPSD 24h 的显著胜利，双曲/欧氏/等权的不可分结果作为诚实的组件分析呈现（这类"简单聚合即足够"的负结果在 Electronics/Energies 是可发的），Ausgrid 负结果写入 Limitations。novelty 变薄，目标刊 Electronics/Applied Sciences 合适，Energies 亦可。
- **B. 方法真重设计（周期长）**：让双曲几何真正接触层级结构——如用 Ausgrid 的客户→区域→总量树初始化/正则化 Poincaré 嵌入、跨层级一致性约束（hierarchical reconciliation）、层级对比学习。只有这个方向能救回 "Hyperbolic Graph" 标题，但等价于半篇新论文。

证据链完整：v5（ridge 全败）→ v6（神经版外部达标）→ v7（组件不可分）全部保留，任何一版结论都可复现。

---

## 进展更新 4（2026-07-14，路线 A 执行）

用户已拍板选择**路线 A（主张降格重写）**，ARA 逻辑文件与登记信息已全部改写完毕（**实验代码与 evidence 文件一律未动**）：

**改动清单**：
1. `papers/mintou/manifest.csv` p2 行：标题改为 **"Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region Power Load Prediction"**（去 Hyperbolic、去 Smart Dispatch、限定 Day-Ahead）；算法名 **CSA-LoadNet**（Cross-Series Attention Load Forecasting Network）。
2. `papers/mintou/.../PAPER.md`：frontmatter title/algorithm 更新，status 改 `route_a_claim_downgrade_v7`；Abstract 重写为跨序列注意力 + 共享时序编码器的日前多区域负荷预测定位。
3. `logic/claims.md`：主张体系重写——C1（主）：OPSD 24h 显著胜 MLP（10 种子，Mann-Whitney+Holm，p=0.0085）；C2（组件）：跨序列聚合显著贡献（vs TemporalOnly，p=0.0011）；C3（诚实负发现）：聚合权重形式（双曲/欧氏/等权/固定曲率）全设置不可分；C4：可复现性。附四条禁止条款：不得主张双曲优势、1h 短时优势、层级（Ausgrid 型）场景优势、"Smart Dispatch" 叙事。
4. `logic/problem.md`：下游任务限定为 day-ahead 24h 多区域预测。
5. `logic/solution/method.md`：算法名更新 + "Naming note (2026-07-14)" 说明改名原因与 v7 证据指针；创新点改为跨序列注意力聚合，Poincaré 嵌入降格为权重参数化选项之一。
6. `papers/mintou/portfolio_status.md`：p2 行与段落更新为 `route_a_executed_csa_loadnet`。

**如实修正一处**：v7 十种子下 SimBench 24h 均值实为 MLP 略优（0.05859 vs 0.06066，p=0.084 不显著），SimBench 1h 才是本方法均值略优——两个 horizon 均按"与 MLP 不可分"如实陈述，不作均值第一主张。

**保持不变**：工程目录名 `mintou_p2_hygraph_load_forecasting`、evidence 中的历史方法名（`HyG-LoadFormer (neural)` 等 CSV 行值）——它们是历史证据，新主张文件中已注明"方法在 v7 前的工作名为 HyG-LoadFormer"。

**目标刊维持 Electronics**（备选 Applied Sciences）。**剩余待办**：related_work 三线综述补齐、sensitivity analysis（邻居数 K、滞后窗、train ratio 等）、Panama 数据集可选补充、图件制作、MDPI 四件套（Data Availability/Funding/COI/Author Contributions）、正文成稿。
