# Round 2 — p1 DSTAR-GRU 综合评审

- **日期**: 2026-07-13
- **评审轮次**: Round 2 (6-mintou 全量 paper_reviews 7 维评审)
- **目标刊**: IEEE Access (主) / MDPI Energies (次)
- **优先级**: 快发优先,允许算法/数据集/下游任务修改
- **ARA 源路径**: `papers/mintou/mintou_p1_dstar_gru_dispatch`

## 1. Paper Summary

DSTAR-GRU (Digital-twin Siamese Temporal Alignment and Retrieval GRU) 提出将历史运行状态相似度检索与 GRU 编码器耦合，用于多目标（成本/违约/弃风弃光/拓扑风险/运行时间）电力调度推荐。当前证据状态：在 RTS-GMLC 公开基准派生的调度代理实验（v3）上，固定切分综合调度得分 `0.73965420`，相对最强基线 Renewable-First ED (`0.74024403`) 增益仅 **0.08%**；rolling（3 窗口）增益 **0.07%** 且 std `0.0548` 比增益大 ~90 倍；唯一较亮信号是高新能源压力子集增益 **0.72%**（对最强消融 3.08%）；high_topology 与 ramp_stress 子集为 **0.00% 完全平局**。ARA 自身如实记录了 v1 为负增益（-0.12%）、v2 仅 0.01%。工程链路完整、证据链诚实，但 **主信号处于噪声量级，核心可行性验证（OPF/UC）缺位**，现状不足以通过任一目标期刊的实验底线。

## 2. Target Venue + Distilled Standards Applied

### IEEE Access — Distilled Review Standards (来源: `Paper_CCF/journals/ieee-access/SKILL.md`)

- **Soundness 是唯一闸门**，novelty 不是；组件组合 + 场景适配 pass。
- DL 类已发表论文 ship 4–6 baselines、零显著性检验、零 multi-run reporting。
- **红线**: 英语语法 / technical fatal / unfair comparison / retracted refs / not distinct / out-of-scope。
- **二元 Accept/Reject**，无 major/minor revision 轮次，仅一次重投机会。
- 已发表论文的 slip-throughs: random 90/10 时间序列泄漏、proxy 数据集-任务不匹配、近零超参数披露、evidence-free 结论外推。
- Incremental 不致命，但 "incremental 且未严格验证" 致命——本文当前恰好落在致命象限。

### MDPI Energies — Distilled Review Standards (来源: `Paper_CCF/journals/mdpi-energies/SKILL.md`)

- **Sensitivity analysis 近强制**；缺失是 top major-revision trigger。
- 单测试系统是常态（~2/3 已发表论文）；0/29 已发表论文要求统计检验。
- ≤5% 改进只要诚实报告即可过；0/31 研究论文引入全新算法。
- 硬性四件套 100% 必备: Funding / COI / Data Availability / Author Contributions。
- "Unvalidated simulation" 是桌拒触发器。
- "Self-defined metrics" 需权重敏感性分析正当化。

### Journal Selection Guide (来源: `Paper_CCF/resources/journal-selection-guide.md`)

- IEEE Access: ~4 周首决, IF ~4.2 Q2, APC US$2,160。
- MDPI Energies: ~16–17 天首决, IF ~4.0 Q2, APC CHF 2,600。
- 备选快刊: MDPI Electronics (~15 天首决, IF ~2.9); Energy Reports (Q1 但见刊 ~16 周)。

## 3. 7-Dimension Review

### 3.1 Novelty

**Score: 4/10 | Severity: 2 (moderate) | Confidence: 0.85 | Fixability: 0.70**

**Finding 1: 组件组合创新但命名过度承诺**

- **Issue**: DSTAR-GRU 将 Siamese GRU + 检索库 + 数字孪生 framing 组合用于调度推荐，属于"组件组合 + 场景适配"，符合 IEEE Access 和 Energies 的新意地板（两刊 distilled 语料均确认此类组合 pass）。但标题中的 "Topology Uncertainty" 和方法名中的 "topology-aware" 承诺了实际未兑现的能力——`high_topology` 压力子集 DSTAR-GRU 与所有方法完全平局 `0.88435443`（`evidence/tables/real_rts_dispatch_stress_leaderboard.csv` 行 30-42）。标题承诺与证据脱节是 novelty 叙述的核心缺陷。
- **Severity**: 2 (moderate)
- **Confidence**: 0.90
- **Fixability**: 0.75 — 可弱化标题/claims 中的 topology 承诺，或补 Grid2Op 拓扑实验（数据已缓存于 `data/public_datasets/rl_control/grid2op-datasets`）
- **Reviewer voice**: "The title promises topology uncertainty handling, yet the topology-stress results show identical scores across all methods. This overclaiming undermines the credibility of the novelty statement."
- **Evidence**: `evidence/tables/real_rts_dispatch_stress_leaderboard.csv` high_topology 行: 所有方法 `0.88435443`; `logic/claims.md` C3 "partially supported"
- **Journal sensitivity**: IEEE Access—"not distinct from prior publication" 是红线但 "not novel enough" 不是；关键在 claims 是否被证据支撑。Energies—"hybrid algorithms with no per-component justification" 是已发表 slip-through 自查项。
- **Fix suggestion**: (a) 标题改为 "Similarity-Aware Multi-Objective Dispatch under Load Uncertainty with High-Renewable Stress Advantage" 或类似弱化 topology 的表述; (b) claims C3 中的 topology 主张改为 honest limitation; (c) 若保留 topology 主张则必须补 Grid2Op 拓扑扰动实验。

**Finding 2: related_work.md 是空壳，gap statement 未落地**

- **Issue**: `logic/related_work.md` 仅一行指向外部文件，无实质综述内容。`logic/problem.md` 的 gap 陈述为 "must prove incremental value through stronger baseline coverage"——这是工程指令而非科学 gap。两刊都要求 "adequate, current literature review" + gap→contribution 叙事链。
- **Severity**: 2 (moderate) — 是写作侧最大硬伤
- **Confidence**: 0.95
- **Fixability**: 0.80 — 纯写作任务，无需新实验
- **Reviewer voice**: "The paper lacks a proper literature review. Without grounding in existing work on similarity retrieval, metric learning for power systems, and digital-twin dispatch, the claimed contribution cannot be assessed."
- **Evidence**: `logic/related_work.md` 全文仅 2 行; `logic/problem.md` gap 陈述
- **Journal sensitivity**: Energies—"inadequate literature review" 是桌拒触发器; Access—"adequate literature review" 是 soundness 闸门前置条件
- **Fix suggestion**: 写三条文献线: (1) 相似度检索/度量学习在电力系统的应用; (2) 数字孪生调度; (3) learning-assisted OPF/ED。每条 5–8 篇近 5 年文献，最终汇合到一句可命名的 gap statement: "现有调度学习方法不利用历史运行状态相似性 / 不显式建模新能源压力下的检索增强决策"。

### 3.2 Soundness

**Score: 2/10 | Severity: 4 (fatal) | Confidence: 0.95 | Fixability: 0.40**

**Finding 1: 主增益 0.08% 在统计上不可区分**

- **Issue**: Fixed-split DSTAR-GRU 综合得分 `0.73965420` vs Renewable-First ED `0.74024403`，绝对差 `0.00058983`，相对增益 `0.08%`。Rolling 3 窗口均值 `0.85295455` vs `0.85352723`，std `0.05477114`（`evidence/tables/real_rts_dispatch_rolling_summary.csv`）。增益绝对值 `0.00057268` 是 std 的 `~0.01` 倍——完全淹没在噪声中。更致命的是 v1 曾为 **-0.12%**（`evidence/runs/real_rts_dispatch_analysis_v1_weak.md`），v2 仅 **0.01%**（`evidence/runs/real_rts_dispatch_analysis_v2_marginal.md`），三次迭代从负到勉强正，趋势不稳定。
- **Severity**: 4 (fatal for IEEE Access binary gate)
- **Confidence**: 0.95
- **Fixability**: 0.30 — 需要 (a) ≥10 种子重复运行 + Wilcoxon 配对检验; (b) ≥10 rolling 窗口; (c) 或将主张完全收缩到高新能源子集（0.72%/3.08%），但这等于重写论文的卖点框架
- **Reviewer voice**: "The claimed improvement of 0.08% is statistically indistinguishable from zero given the reported rolling standard deviation of 0.0548. Without multi-seed replication and formal statistical testing, no credible claim of superiority can be made on the overall results."
- **Evidence**: `evidence/tables/real_rts_dispatch_leaderboard.csv`; `evidence/tables/real_rts_dispatch_rolling_summary.csv`; `evidence/runs/real_rts_dispatch_analysis_v1_weak.md`; `evidence/runs/real_rts_dispatch_analysis_v2_marginal.md`
- **Journal sensitivity**: IEEE Access DL 惯例虽无统计检验，但增益需肉眼可辨——0.08% 在 3 窗口 std 0.0548 下不满足此最低门槛。Access 二元闸门无 revision 救援，"补实验再审"不存在。Energies 虽不要求统计检验（0/29），但 "≤5% 改进" 需 "honestly reported"——当前 framing 将 0.08% 当主卖点本身不够 honest。
- **Fix suggestion**: **P0 级**。两种路径: (a) 补 ≥10 种子 + ≥10 rolling 窗口 + Wilcoxon 使 "overall 不劣化" 可统计陈述; (b) 完全重构主张: 主卖点改为高新能源压力子集 0.72%/3.08%，overall 改述为 "competitive parity with stress-scenario advantage"。

**Finding 2: OPF/UC 可行性验证缺失**

- **Issue**: `logic/experiments.md` 中 `opf_transfer` 槽位状态 "Not yet available / planned"。三份 analysis（`real_rts_dispatch_analysis.md`、`real_rts_dispatch_rolling_analysis.md`、`real_rts_dispatch_stress_analysis.md`）均写明 "does not prove AC feasibility or production-cost optimality"。当前实验是 "standard-library RTS-GMLC dispatch proxy"，不是 AC-OPF 或机组组合证明。Claims C3（压力下保持可行）在无 OPF 验证下站不住。
- **Severity**: 3 (serious) — 对 Energies 是 "unvalidated simulation" 桌拒线; 对 Access 是 "unsupported claims"
- **Confidence**: 0.95
- **Fixability**: 0.50 — PGLib-OPF (`data/public_datasets/opf_benchmarks/pglib-opf`)、MATPOWER (`data/public_datasets/grid_cases/matpower`)、pandapower (`data/public_datasets/grid_cases/pandapower`) 均已本地缓存，零下载成本; 但需编写 DC-OPF 校验层代码
- **Reviewer voice**: "The dispatch recommendations are generated by a proxy simulation without OPF feasibility verification. Claims about feasibility under stress conditions are unsupported without at minimum a DC-OPF validation layer."
- **Evidence**: `logic/experiments.md` opf_transfer slot; `src/configs/experiment_manifest.json` datasets list includes PGLib-OPF and MATPOWER but neither appears in evidence
- **Journal sensitivity**: Energies—"unvalidated simulation" 是 explicit 桌拒触发器; Access—"claims must be supported by baselines/validation"
- **Fix suggestion**: **P0 级**。使用已缓存的 PGLib/MATPOWER + pandapower 构建 DC-OPF 可行性校验层。对每个 DSTAR-GRU 输出的调度方案，校验 DC-OPF 可行性并报告 infeasible rate。这是两刊共同的最关键缺口。

**Finding 3: 基线名单 manifest 与实跑不一致**

- **Issue**: `logic/solution/method.md` 和 `src/configs/experiment_manifest.json` 声称 8 个基线 (DC OPF, AC OPF, GRU Direct, LSTM Direct, CNN-LSTM, Grid2Op Rule, PSO, GA)。但 RTS-GMLC 实跑 leaderboard (`evidence/tables/real_rts_dispatch_leaderboard.csv`) 中的基线为: Renewable-First ED、CNN-LSTM Proxy、GRU-Direct Proxy、PSO Dispatch Proxy、GA Dispatch Proxy、Reserve-Aware ED、Merit-Order ED——其中 DC OPF、AC OPF、LSTM Direct、Grid2Op Rule **未出现**，而 Renewable-First ED、Reserve-Aware ED、Merit-Order ED **未在 manifest 中声明**。Smoke benchmark (`evidence/tables/synthetic_smoke_leaderboard.csv`) 的基线名单则与 manifest 一致，说明 manifest 只在 synthetic 层面兑现。
- **Severity**: 3 (serious) — "claimed but not run" = unsupported claim
- **Confidence**: 0.95
- **Fixability**: 0.60 — 需在 RTS-GMLC 上实跑缺失的 DL 基线 (GRU/LSTM/CNN-LSTM) + DC-OPF + 规则型 ED
- **Reviewer voice**: "The manuscript claims 8 baselines including DC OPF and AC OPF, yet the actual RTS-GMLC leaderboard shows different methods. This discrepancy between claimed and executed baselines is a serious credibility issue."
- **Evidence**: `logic/solution/method.md` baseline list vs `evidence/tables/real_rts_dispatch_leaderboard.csv` method list; `src/configs/experiment_manifest.json` baselines array
- **Journal sensitivity**: Access DL 惯例 4–6 个 **真实跑通** 的基线; Energies 要求 external baselines 出现在 ~一半已发表论文中
- **Fix suggestion**: **P0 级**。在 RTS-GMLC 上实跑: (1) LSTM Direct Proxy; (2) DC-OPF (作为可行性下限); (3) 统一 manifest 与实际 leaderboard。当前实跑的 6 个 ED/proxy 基线 + 4 个消融已满足数量要求，关键是名单一致性。

### 3.3 Experiments

**Score: 2/10 | Severity: 3 (serious) | Confidence: 0.90 | Fixability: 0.50**

**Finding 1: 敏感性分析完全缺失**

- **Issue**: `evidence/` 目录中无任何参数扫描表。`composite_dispatch_score` 是自定义指标（包含 cost/violation/curtailment/topology_risk/runtime 五分量），但其权重分配无任何依据或敏感性验证。Energies distilled 标准明确: "sensitivity analysis near-mandatory; its absence is the top major-revision trigger"，且 "inflated percentages on self-defined metrics" 是已发表论文被点名的自查项。
- **Severity**: 3 (serious for Energies)
- **Confidence**: 0.95
- **Fixability**: 0.70 — 纯计算任务，无需新数据
- **Reviewer voice**: "The composite dispatch score is a self-defined metric with unspecified weights. Without sensitivity analysis showing how weight choices affect the ranking, the reported improvements could be artifacts of the metric design."
- **Evidence**: `evidence/` 目录全文搜索无 sensitivity 相关文件; `evidence/tables/real_rts_dispatch_leaderboard.csv` composite_dispatch_score 列
- **Journal sensitivity**: Energies—**top major-revision trigger**; Access—可借它正当化自定义指标（加分项）
- **Fix suggestion**: **P1 级**。三维敏感性扫描: (1) composite score 权重（如 cost 权重 0.2–0.6、其余等比调整）; (2) 检索库规模（已有 `small_reference_bank` 消融雏形）; (3) 相似度阈值。以热力图或折线图展示 ranking 稳定性。

**Finding 2: 消融证据停留在 smoke 级**

- **Issue**: `logic/experiments.md` 6 项消融全部标 "smoke-tested"，证据仅为 `evidence/runs/synthetic_smoke_results.csv`。`logic/solution/constraints.md` 明令 "Do not claim synthetic smoke benchmark numbers as final manuscript results"。在 RTS-GMLC 实跑 leaderboard 中仅出现 Ablation-NoTopology 和 Ablation-NoSiamese 两个消融变体（stress leaderboard），其余 4 个消融 (no_retrieval_bank, lstm_encoder, single_objective_layer, small_reference_bank) 在 RTS 上未实跑。Claims C2（组件贡献）只被部分消融窄支撑。
- **Severity**: 3 (serious)
- **Confidence**: 0.90
- **Fixability**: 0.60 — 需在 RTS-GMLC 上实跑全部 6 个消融变体
- **Reviewer voice**: "The ablation study is conducted only on synthetic data, which the authors themselves acknowledge is not suitable for manuscript claims. The component contribution claim (C2) is therefore unsupported on real power system data."
- **Evidence**: `logic/experiments.md` ablation table 全 6 项 status "smoke-tested"; `logic/solution/constraints.md` line 1; `evidence/tables/real_rts_dispatch_stress_leaderboard.csv` 仅含 NoTopology/NoSiamese/SmallBank/LSTMEncoder/NoRetrievalBank/SingleObjective 在 all 子集出现（注: 实跑 leaderboard 确实包含了全部消融，但 smoke 标签与 constraints 的矛盾仍在）
- **Journal sensitivity**: 两刊都要求消融支撑组件贡献主张
- **Fix suggestion**: **P0 级**。确认全部 6 消融在 RTS-GMLC 上实跑（注: fixed-split leaderboard `evidence/tables/real_rts_dispatch_leaderboard.csv` 实际已包含全部 6 消融变体: NoTopology, SmallBank, LSTMEncoder, NoSiamese, NoRetrievalBank, SingleObjective——但 `experiments.md` 仍标 "smoke-tested"，需更新状态标签并确保这些 RTS 实跑结果是被约束允许的 manuscript-level 证据）。

**Finding 3: 单测试系统 + 仅 3 rolling 窗口**

- **Issue**: 仅 RTS-GMLC 一个测试系统（`evidence/source/real_rts_dispatch_source_profile.csv`: 154 generators, 120 branches, 480 evaluated scenarios）。Rolling 仅 3 窗口（windows: 360, 480, 600，见 `src/configs/real_rts_dispatch_config.json`）。NREL-118 (`data/public_datasets/grid_cases/nrel118`) 已于 2026-07-12 缓存但未使用。
- **Severity**: 2 (moderate) — Energies 单系统是常态可接受; Access 无硬性要求但第二系统显著加固
- **Confidence**: 0.85
- **Fixability**: 0.65 — NREL-118 已缓存，适配工作量中等
- **Reviewer voice**: "A single test system limits generalizability claims. The rolling validation with only 3 windows provides insufficient temporal robustness evidence."
- **Evidence**: `evidence/source/real_rts_dispatch_source_profile.csv`; `src/configs/real_rts_dispatch_config.json` rolling_windows
- **Journal sensitivity**: Energies—单系统 ~2/3 已发表论文可接受; Access—第二系统是加分项
- **Fix suggestion**: **P1 级**。在 NREL-118 上复制 fixed-split 实验; rolling 窗口扩至 ≥10。

### 3.4 Reproducibility

**Score: 5/10 | Severity: 2 (moderate) | Confidence: 0.80 | Fixability: 0.70**

**Finding 1: 代码封装过深，超参数未披露**

- **Issue**: `src/code/run_real_rts_dispatch.py` 全文仅 3 行: `from powergrid_benchmark.mintou_real_dispatch import run_dispatch; run_dispatch()`。实际逻辑封装在 `powergrid_benchmark.mintou_real_dispatch` 模块中，该模块不在 ARA 源路径内，评审无法审阅核心算法实现。`src/configs/real_rts_dispatch_config.json` 给出了 scenario_limit/train_window/rolling_windows 但缺少: GRU 层数/隐藏维度、学习率、训练 epoch、相似度阈值、检索库构建策略、Siamese 损失权重等关键超参数。
- **Severity**: 2 (moderate)
- **Confidence**: 0.85
- **Fixability**: 0.75 — 需补充超参数表 + 确保核心模块可审阅
- **Reviewer voice**: "The core algorithm implementation is not accessible within the provided code. Critical hyperparameters (GRU architecture, learning rate, similarity threshold, training epochs) are not disclosed, making reproduction impossible."
- **Evidence**: `src/code/run_real_rts_dispatch.py` 全文; `src/configs/real_rts_dispatch_config.json`
- **Journal sensitivity**: Access distilled—"near-zero hyperparameter disclosure" 是已发表论文 slip-through; IEEE Access reproducibility initiative 显式加分
- **Fix suggestion**: **P1 级**。(a) 在 manuscript 中加完整超参数表: 检索库规模、相似度阈值、GRU 结构、训练设置; (b) 开源代码仓库（已有 `run_real_rts_dispatch.py` + config 基础）; (c) 确保 `powergrid_benchmark.mintou_real_dispatch` 模块可见或提供等效 pseudocode。

**Finding 2: 无图表 (figures)**

- **Issue**: `evidence/figures/README.md` 写明 "Figures will be generated after public benchmark result tables are upgraded beyond synthetic smoke tests"——即当前无任何可视化图表。两刊都需要至少: 方法框架图、实验结果对比图/表、消融图。
- **Severity**: 2 (moderate)
- **Confidence**: 0.90
- **Fixability**: 0.80 — 纯制作任务
- **Reviewer voice**: "The paper has no figures whatsoever. A method framework diagram and result visualizations are essential for any journal submission."
- **Evidence**: `evidence/figures/README.md`
- **Journal sensitivity**: Access—支持 graphical abstract; Energies—IMRaD 结构需要可视化
- **Fix suggestion**: **P1 级**。制作: (1) DSTAR-GRU 方法框架图; (2) Leaderboard 对比柱状图; (3) 压力子集热力图; (4) Rolling 窗口得分趋势图; (5) 消融贡献分解图。

### 3.5 Related Work

**Score: 1/10 | Severity: 3 (serious) | Confidence: 0.95 | Fixability: 0.85**

**Finding 1: related_work.md 是空壳**

- **Issue**: `logic/related_work.md` 全文仅 2 行: 一行指向 `papers/literature/target_journal_related/comparison_analysis.md`，一行声明 "project-original planned work"。无任何实质文献综述。
- **Severity**: 3 (serious)
- **Confidence**: 0.95
- **Fixability**: 0.85 — 纯写作任务
- **Reviewer voice**: "The related work section is essentially empty. This is unacceptable for any peer-reviewed journal submission."
- **Evidence**: `logic/related_work.md` 全文
- **Journal sensitivity**: Energies—"inadequate literature review" 是 explicit 桌拒触发器; Access—"adequate, current literature review" 是 soundness 前置条件
- **Fix suggestion**: **P1 级**。见 3.1 Finding 2 的详细修复方案。三条文献线各 5–8 篇，近 5 年占比 ≥60%，自引克制。

### 3.6 Clarity

**Score: 4/10 | Severity: 2 (moderate) | Confidence: 0.80 | Fixability: 0.75**

**Finding 1: Claims 与证据脱节**

- **Issue**: `logic/claims.md` 中 C1 "improves composite dispatch score" 被 v3 fixed 0.08% 窄支撑（v1 为负、v2 为 0.01%）; C3 "remains feasible under topology-risk proxy stress" 被 high_topology 0.00% 平局直接否定。PAPER.md 的 Abstract 未将主张重心放在高新能源子集（最强信号）上。
- **Severity**: 2 (moderate)
- **Confidence**: 0.85
- **Fixability**: 0.70 — 需重构 Abstract/Introduction 的主张层次
- **Reviewer voice**: "The claims as stated are not adequately supported by the evidence. C1 relies on a 0.08% improvement that is within noise, and C3 is contradicted by the topology-stress tie."
- **Evidence**: `logic/claims.md` C1/C3 vs `evidence/runs/real_rts_dispatch_stress_analysis.md`
- **Journal sensitivity**: 两刊共通—"claims must match evidence"
- **Fix suggestion**: **P0 级**。主张层次重构: (1) 主打高新能源压力子集优势 (0.72%/3.08%); (2) overall 结果述为 "competitive parity / non-degradation"; (3) topology 主张降为 limitation 或 future work; (4) 消融 C2 基于 RTS 实跑 leaderboard 数据（非 smoke）。

**Finding 2: Gap statement 过于泛化**

- **Issue**: `logic/problem.md` gap: "must prove incremental value through stronger baseline coverage, ablation isolation, and reproducible public data"——这是工程指令不是科学 gap。
- **Severity**: 1 (minor)
- **Confidence**: 0.90
- **Fixability**: 0.85
- **Reviewer voice**: "The gap statement reads as an internal project instruction rather than a scientific contribution gap."
- **Evidence**: `logic/problem.md` Target-Journal Gap section
- **Journal sensitivity**: 两刊共通
- **Fix suggestion**: 改写为: "Existing dispatch learning methods do not exploit historical operating-state similarity for retrieval-augmented decision-making under high-renewable stress conditions."

### 3.7 Ethics

**Score: 7/10 | Severity: 1 (minor) | Confidence: 0.80 | Fixability: 0.80**

**Finding 1: Manifest 基线名单与实跑不一致构成表面诚信风险**

- **Issue**: `src/configs/experiment_manifest.json` 声明 8 基线含 DC OPF/AC OPF/LSTM Direct/Grid2Op Rule，但 RTS 实跑中这些未出现。虽然 ARA 自身的 `constraints.md` 和 analysis 文件诚实记录了这一差距，但若 manuscript 按 manifest 名单声称而不标注实际运行情况，将构成"声称-证据不一致"的诚信风险。
- **Severity**: 1 (minor) — ARA 诚实记录 mitigates; 风险在 manuscript 层面
- **Confidence**: 0.80
- **Fixability**: 0.80 — 统一 manifest 与实际运行名单 + 在 manuscript 中诚实说明
- **Reviewer voice**: "The experiment manifest claims baselines that were not actually executed. While the internal documentation is honest, this discrepancy must be resolved before submission."
- **Evidence**: `src/configs/experiment_manifest.json` baselines vs `evidence/tables/real_rts_dispatch_leaderboard.csv`
- **Journal sensitivity**: Access—CrossCheck/iThenticate 审查; 两刊均不容忍 misleading experiment descriptions
- **Fix suggestion**: 更新 `experiment_manifest.json` 反映实际 RTS 运行基线; manuscript 中诚实标注哪些基线在哪个数据集上实跑。

**Finding 2: 数据集声称与实际使用不符**

- **Issue**: `logic/problem.md` 和 `experiment_manifest.json` 列出 5 个数据集 (RTS-GMLC, PGLib-OPF, MATPOWER, Grid2Op, OPSD)，实际仅使用 RTS-GMLC 1 个。OPSD 尤其与调度任务关联弱。
- **Severity**: 1 (minor)
- **Confidence**: 0.85
- **Fixability**: 0.85 — 删除未用数据集声明或明确标注 "planned/future"
- **Reviewer voice**: "Listing 5 datasets but using only 1 creates a misleading impression of the experimental scope."
- **Evidence**: `logic/problem.md` datasets list vs `evidence/source/real_rts_dispatch_source_profile.csv`
- **Journal sensitivity**: 两刊共通
- **Fix suggestion**: 在 manuscript 中: RTS-GMLC 标注 "primary experimental system"; PGLib-OPF/MATPOWER 标注 "planned for OPF validation layer"; OPSD 从列表中删除或明确用途; Grid2Op 标注 "planned for topology experiments"。

## 4. Aggregated RRI Estimate (0-100)

公式: RRI = Σ (severity × confidence × (1 - fixability) × risk_weight) per dimension

Risk weights: novelty 0.15, soundness 0.30, experiments 0.25, reproducibility 0.10, related_work 0.08, clarity 0.07, ethics 0.05.

| Dimension | Max Severity | Confidence | Fixability | Raw Risk | Weight | Weighted |
|---|---|---|---|---|---|---|
| Novelty | 2 | 0.85 | 0.70 | 0.51 | 0.15 | 0.077 |
| Soundness | 4 | 0.95 | 0.40 | 2.28 | 0.30 | 0.684 |
| Experiments | 3 | 0.90 | 0.50 | 1.35 | 0.25 | 0.338 |
| Reproducibility | 2 | 0.80 | 0.70 | 0.48 | 0.10 | 0.048 |
| Related Work | 3 | 0.95 | 0.85 | 0.43 | 0.08 | 0.034 |
| Clarity | 2 | 0.80 | 0.75 | 0.40 | 0.07 | 0.028 |
| Ethics | 1 | 0.80 | 0.80 | 0.16 | 0.05 | 0.008 |

**RRI = (0.077 + 0.684 + 0.338 + 0.048 + 0.034 + 0.028 + 0.008) × (100 / max_possible)**

Max possible = Σ (4 × 1.0 × 1.0 × weight) = 4.0 (all dimensions at max severity, zero fixability, full confidence)

**RRI = 1.217 / 4.0 × 100 = 30.4 / 100**

**解读**: RRI 30.4 处于中等偏高风险区间。Soundness 单项贡献了 56% 的总风险（0.684 / 1.217），且 fixability 仅 0.40——这是核心瓶颈。好消息是 related_work (fixability 0.85) 和 clarity (fixability 0.75) 高度可修；坏消息是 soundness 的修复（OPF 验证 + 统计检验 + 主张重构）工作量大且结果不确定（补做后信号可能仍然弱）。

## 5. Predicted Decision

### IEEE Access: **Reject** (confidence 0.85)

理由: 二元 Accept/Reject 闸门下，0.08% 噪声级主增益 + 无 OPF/UC 可行性验证 + 基线名单不一致 + 消融仅在 synthetic 上验证 = "insufficient rigor: weak experiments, unsupported claims"（Access explicit top rejection trigger）。无 major revision 救援轮次，一次重投机会极可能被浪费。**当前状态不建议投 IEEE Access**。

### MDPI Energies: **Major Revision** (confidence 0.75)

理由: Energies 有 1–2 轮修改机会。0.08% 增益虽弱但高新能源子集 0.72%/3.08% 可作主打（≤5% 改进 honest reporting pass）; 单测试系统是常态; 无统计检验是常态（0/29）。但敏感性分析缺失（top major-revision trigger）+ OPF 验证缺失（"unvalidated simulation" 桌拒风险）+ related work 空壳（桌拒触发器）三项叠加可能升级为 Desk Reject。**需至少完成 P0 全部动作后才可投**。

## 6. Top-3 Actionable Revisions (P0 / P1 / P2)

### P0-1: 主张重构 + 高新能源压力子集主打

- **Priority**: P0 (不做则两刊都过不了)
- **Issue**: 0.08% 主增益在噪声中; topology 主张被 0.00% 平局否定; 整体 claims 框架与证据脱节
- **Fix suggestion**:
  1. Abstract/Introduction 主打: "Under high-renewable stress conditions (≥50% renewable share), DSTAR-GRU achieves 0.72% improvement over the strongest baseline and 3.08% over the strongest ablation in composite dispatch score"
  2. Overall 结果改述为: "DSTAR-GRU maintains competitive parity with the best-performing baseline across all scenarios while demonstrating targeted advantage under renewable-stress conditions"
  3. 标题弱化 topology: 改为 "Similarity-Aware GRU for Multi-Objective Power Grid Dispatch with High-Renewable Stress Advantage"
  4. Claims C3 topology 部分改为 limitation/future work
- **Estimated effort**: 1–2 天 (纯写作)
- **Expected impact on venue**: 消除最易被攻击的 overclaiming; 使 claims 与 evidence 自洽——这是 soundness 闸门的前置条件

### P0-2: DC-OPF 可行性验证层

- **Priority**: P0
- **Issue**: 无 OPF/UC 验证 = "unvalidated simulation" (Energies 桌拒线) + "unsupported claims" (Access)
- **Fix suggestion**:
  1. 使用已缓存 `data/public_datasets/opf_benchmarks/pglib-opf` + `data/public_datasets/grid_cases/matpower` + pandapower
  2. 对 DSTAR-GRU 和所有基线的调度输出运行 DC-OPF 可行性校验
  3. 报告 infeasible rate / constraint violation severity / locational marginal price 对比
  4. 在 `evidence/tables/` 新增 OPF feasibility leaderboard
- **Estimated effort**: 5–7 天 (编写 DC-OPF 校验模块 + 运行 + 分析)
- **Expected impact on venue**: 消除两刊共同的致命/严重拒稿风险; 使 "dispatch recommendation" 主张具备物理可行性支撑

### P0-3: 统计稳健性补强

- **Priority**: P0
- **Issue**: 3 rolling windows + 0.08% gain vs 0.0548 std = 噪声; v1→v2→v3 不稳定
- **Fix suggestion**:
  1. 多种子 (≥10) 重复运行 DSTAR-GRU 和 Renewable-First ED
  2. 扩 rolling 窗口至 ≥10 (当前 `rolling_windows: [360, 480, 600]` 改为步长更密的 10+ 窗口)
  3. Wilcoxon 配对符号秩检验
  4. 若 overall 仍不显著 → 主张完全收缩到 high_renewable 子集（该子集 121 scenarios，增益 0.72% 更有可能在多种子下显著）
- **Estimated effort**: 3–5 天 (运行 + 统计计算)
- **Expected impact on venue**: 使 "competitive parity" 或 "non-degradation" 成为可统计陈述; 消除 Access reviewer 一眼可看穿的 noise-level gain 问题

### P1-1: 敏感性分析

- **Priority**: P1
- **Issue**: Energies top major-revision trigger; composite_dispatch_score 权重无依据
- **Fix suggestion**: composite score 权重三维扫描 + 检索库规模扫描 + 相似度阈值扫描
- **Estimated effort**: 2–3 天
- **Expected impact on venue**: 满足 Energies 近强制要求; 正当化自定义指标

### P1-2: Related Work 实质写作

- **Priority**: P1
- **Issue**: 空壳 = 两刊桌拒触发器
- **Fix suggestion**: 三条文献线 (相似度检索 in power, 数字孪生 dispatch, learning-assisted OPF/ED)
- **Estimated effort**: 3–5 天
- **Expected impact on venue**: 消除桌拒风险; 建立 gap→contribution 叙事链

### P1-3: NREL-118 第二测试系统

- **Priority**: P1
- **Issue**: 单系统泛化性受限
- **Fix suggestion**: 在已缓存 NREL-118 上复制 fixed-split 实验
- **Estimated effort**: 3–5 天
- **Expected impact on venue**: 加固泛化性主张; Access 显著加分

### P2-1: 开源代码仓库

- **Priority**: P2
- **Issue**: 两刊均不强制但加分
- **Fix suggestion**: 整理 `run_real_rts_dispatch.py` + config + 核心模块为可发布仓库
- **Estimated effort**: 1–2 天
- **Expected impact on venue**: Access reproducibility initiative 差异化优势

### P2-2: 完整图表集

- **Priority**: P2
- **Issue**: 当前零图表
- **Fix suggestion**: 方法框架图 + leaderboard 对比图 + 压力子集热力图 + 消融分解图 + rolling 趋势图
- **Estimated effort**: 2–3 天
- **Expected impact on venue**: 满足两刊基本可视化要求

## 7. Allowable Modifications (fast-OA priority)

### 7.1 Algorithm framework changes

**可改而保持大方向 (multi-objective dispatch with GRU + digital twin) 的部分:**

- **GRU 编码器可替换为 Transformer/LSTM**: 如果 GRU-Direct 在 leaderboard 上表现不如 CNN-LSTM Proxy (`0.75504976` vs `0.75039592`)，可考虑将时序编码器换为 CNN-LSTM 或轻量 Transformer，保留检索+相似度框架不变。标题相应改为 "DSTAR-Net" 或去除 GRU 特定命名。
- **相似度度量可优化**: 当前 Siamese 分支的度量学习方式未详细披露; 可尝试 contrastive learning (e.g., NT-Xent) 或 learned Mahalanobis distance，以拉大 high_renewable 子集的检索区分度。
- **检索策略可升级**: 当前 retrieval_hit_rate 0.646 (fixed) 表明 ~35% 的调度场景未命中检索; 可引入 soft-retrieval (top-k weighted combination) 或 attention-based retrieval 替代 hard threshold。
- **composite_dispatch_score 权重可学习化**: 将固定权重替换为 data-driven 权重（如通过 Pareto front exploration），可部分解决 sensitivity analysis 问题。
- **多目标层可替换**: 当前 "single_objective_layer" 消融得分 `0.76572147` vs full model `0.73965420`，差异 ~3.5%——多目标层确实有效。可尝试 NSGA-II 或 MOEA/D 替代加权求和。

**不可改的部分 (改了就偏离大方向):**
- 相似度检索 + 调度决策的耦合框架
- 数字孪生状态库概念
- 多目标 dispatch 问题设定

### 7.2 Dataset changes

**本地已缓存可立即使用的替代/补充数据集:**

| 数据集 | 路径 | 适用场景 | 改造成本 |
|---|---|---|---|
| **NREL-118** | `data/public_datasets/grid_cases/nrel118` | 第二测试系统 (泛化性验证) | 低: 与 RTS-GMLC 同为电力系统 case |
| **PGLib-OPF** | `data/public_datasets/opf_benchmarks/pglib-opf` | DC-OPF 可行性校验层 | 低: 标准 OPF benchmark |
| **MATPOWER** | `data/public_datasets/grid_cases/matpower` | OPF 校验 + case118/case300 等多规模测试 | 低: 成熟工具链 |
| **Grid2Op** | `data/public_datasets/rl_control/grid2op-datasets` | 拓扑扰动实验 (修复 topology 0.00% 平局) | 中: 需要适配 Grid2Op action space |
| **pandapower** | `data/public_datasets/grid_cases/pandapower` | Python-native OPF 校验 | 低 |
| **SDWPF KDD Cup 2022** | `data/public_datasets/renewable_weather/sdwpf_kddcup2022` | 若转为风电预测任务 | 高: 需重新定义下游任务 |
| **ENTSO-E Transparency** | `data/public_datasets/time_series_market/entsoe_transparency` | 真实欧洲负荷/新能源时序 | 中: 需匹配电网拓扑 |
| **OPSD** | `data/public_datasets/time_series_market/opsd_time_series` | 真实调度时序数据 | 中: 与当前 proxy 框架适配性待验证 |

**建议**: P0 使用 PGLib-OPF + MATPOWER + pandapower 构建 OPF 校验层; P1 使用 NREL-118 做泛化 + Grid2Op 做拓扑; OPSD 从声明中删除（与调度代理实验框架不兼容）。

### 7.3 Downstream task changes

**如果 dispatch framing 的证据始终不够强，同一 machinery (GRU + retrieval + digital twin) 可服务的相邻任务:**

1. **Learning-assisted OPF warm-starting**: 将 DSTAR-GRU 的输出作为 DC-OPF/AC-OPF 求解器的 warm-start 初值，主张 "加速 OPF 收敛" 而非 "替代 OPF"。这在 IEEE Access 和 Energies 都有已发表先例，且对增益幅度的要求更低（warm-start 加速 20–30% 即可发表）。PGLib-OPF 和 MATPOWER 已缓存。

2. **Renewable curtailment prediction + dispatch advisory**: 将任务从 "dispatch recommendation" 改为 "renewable curtailment risk prediction with dispatch advisory"。当前 high_renewable 子集的 curtailment_rate 差异最大（DSTAR-GRU `0.00052514` vs Renewable-First ED `0.00177049` vs Ablation-NoSiamese `0.01496402`——`evidence/tables/real_rts_dispatch_stress_leaderboard.csv`），这是最亮的信号。

3. **Dispatch state retrieval as a service**: 将核心创新（相似度检索）本身作为 contribution——"Operating-state retrieval for power system decision support"，定位为 framework/tool paper 而非 method superiority paper。这对 Access (framework/evaluation paper 有已发表先例) 和 Energies (system/modeling contribution type) 都可行，且对增益幅度的要求最低。

4. **风电功率预测 (wind power forecasting)**: 若使用 SDWPF KDD Cup 2022 数据 (`data/public_datasets/renewable_weather/sdwpf_kddcup2022`)，同一 GRU + retrieval 框架可转为短期风电预测任务。Energies 对 forecasting papers 有 ≥3 baselines + component comparisons + multiple metrics 的明确 bar，但数据量更丰富、结果可能更显著。

## 8. Honest Boundary

### 本文 **不能** 声称的:

1. **"DSTAR-GRU outperforms baselines in dispatch optimization"**: 0.08% 增益在统计上不可区分，v1 曾为负增益。最多可声称 "achieves competitive parity with the best-performing baseline overall, with targeted improvement under high-renewable stress conditions"。

2. **"Topology uncertainty handling"**: high_topology 子集完全平局 (0.00%)。标题/摘要/claims 中不得将 topology 作为已验证能力。

3. **"AC-OPF feasible dispatch"**: 无 OPF/UC 验证层。所有 dispatch 结果必须标注为 "proxy dispatch recommendation" 或 "dispatch agent output"，不得声称物理可行性。

4. **"Generalizable to other power systems"**: 仅 RTS-GMLC 一个系统验证。在 NREL-118 复制实验完成前，泛化性主张为 evidence-free generalization（Access 已发表 slip-through 自查项）。

5. **"Component X contributes Y% improvement"**: 消融仅在 synthetic smoke benchmark 上完整验证（constraints.md 明令不得用于 manuscript），RTS 实跑 leaderboard 中虽包含全部消融变体但 experiments.md 状态标签仍为 "smoke-tested"——需确认并更新状态后方可引用。

### 必须显式披露为 limitation 的:

1. 本实验是 standard-library RTS-GMLC dispatch proxy，不是 AC-OPF 或 unit-commitment solver
2. 仅使用 1 个测试系统 (RTS-GMLC, 154 generators, 120 branches)
3. 拓扑风险为 proxy 指标，非真实拓扑分析
4. 检索库规模与构建策略的敏感性未充分探索
5. 高 topology / ramp stress 子集无差异——需要在 discussion 中正面回应而非隐藏

## 9. Fastest Path to Submission

### 目标: MDPI Energies (首选，因其有 revision 轮次 + 对弱信号容忍度更高)

| 步骤 | 动作 | 时间 | 前置 |
|---|---|---|---|
| **Day 1–2** | **主张重构**: 标题/Abstract/Claims 改为 high-renewable stress 主打 + topology 弱化 + overall 改为 competitive parity | 2 天 | 无 |
| **Day 1–2** | **Related work 写作**: 三条文献线 + gap statement | 2 天 | 无 (与 step 1 并行) |
| **Day 3–7** | **DC-OPF 可行性验证层**: pandapower + PGLib-OPF, 对所有方法输出校验 | 5 天 | 无 |
| **Day 3–7** | **多种子重复运行**: ≥10 seeds × DSTAR-GRU + top-3 baselines + top-3 ablations | 5 天 | 无 (与 OPF 并行) |
| **Day 5–8** | **更新 experiments.md 消融状态**: 确认全部 6 消融在 RTS 实跑 + 更新标签 | 1 天 | Day 3 启动 |
| **Day 8–10** | **敏感性分析**: composite 权重 + 检索库规模 + 相似度阈值 | 3 天 | Day 7 (需要多种子结果稳定后) |
| **Day 8–10** | **统计检验**: Wilcoxon on multi-seed results, 扩 rolling 窗口 | 2 天 | Day 7 |
| **Day 10–13** | **图表制作**: 框架图 + leaderboard + stress heatmap + ablation + rolling trend | 3 天 | Day 10 |
| **Day 11–15** | **Manuscript 全文写作**: MDPI IMRaD 模板 + 四件套声明 + ~200 词 abstract + Data Availability | 5 天 | Day 10 (需要所有结果就位) |
| **Day 15–16** | **超参数完整披露表 + fairness statement** | 1 天 | Day 15 |
| **Day 16–17** | **内部评审 + 英语润色 + 格式检查** | 2 天 | Day 15 |
| **Day 18** | **Submission to MDPI Energies** (Section: Electrical Power and Energy Systems or Smart Grids) | 1 天 | Day 17 |

**总计: ~18 天到投稿** (若并行最大化可压缩至 ~14 天)

### 若坚持 IEEE Access:

在上述 18 天基础上 **额外** 需要:
- NREL-118 第二系统实验 (+3–5 天)
- Grid2Op 拓扑实验或彻底删除 topology 主张 (+3–5 天)
- 更严格的 fairness statement (参数量/算力预算对齐, +1 天)
- **总计: ~24–28 天到投稿**

### 最快备选路线 (如果 P0 补做后信号仍弱):

切换到 **7.3 节 Downstream task change #3** ("Operating-state retrieval for power system decision support" framework paper) 或 **#2** (renewable curtailment prediction + advisory)，可在 ~10 天内重新 framing 并投稿 MDPI Energies/Electronics——因为 curtailment_rate 差异是当前最亮的信号（high_renewable 子集中 DSTAR-GRU 0.05% vs Renewable-First ED 0.18% vs Ablation-NoSiamese 1.50%，差 ~30 倍），可能比 composite_dispatch_score 的 0.08% 更容易通过评审。
