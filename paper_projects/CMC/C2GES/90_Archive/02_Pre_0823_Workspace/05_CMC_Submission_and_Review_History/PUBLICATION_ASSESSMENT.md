# 投稿评估：C2GES（2026_c2ges_engineeringletters）— EI 现投 vs SCI 升级

- **日期**: 2026-07-17
- **评审模式**: 对抗式投稿前评审（对齐 mintou ROUND_REVIEW 方法：claim–evidence 核查 + 七维评分 + desk screen + 决策预测）
- **稿件**: `source/paper.tex`（15 页 PDF，`source/paper.pdf`）
- **当前目标**: Engineering Letters（IAENG，EI/Scopus 收录，非 SCI）
- **核验证据源**: `source/supplement/bm25_k_sensitivity/summary.json`（5567 行完整运行工件）、`source/supplement/bm25_k_sensitivity/metadata.json`、`source/code/main.py`、`source/REVISION_NOTE.md`、`source/OPTIMIZATION_PLAN.md`
- **不可用证据源**: 主 Executor 工件 `experiment_outputs/c2ges_role_selective_graph/`（summary.json、details.jsonl、cv_protocol.json、heldout_predictions.jsonl）**不在投稿包内**——正文多处路径引用它，但包里只有 BM25/K 敏感性补充工件

---

## 1. 论文内容与声明体系概述

### 这篇论文是什么

把电网可靠性报告（公开 NERC 扰动/教训报告及节选）的分析形式化为**因果角色条件化的证据句选择**任务：给定文档句子序列 + 一个角色化因果问题（trigger / root cause / propagation-response / impact / mitigation 五角色），输出 Top-K（K=3）证据句 ID。提出 **C²GES**：一个完全确定性的轻量重排器，Score = w_q·查询相关（TF-IDF 余弦）+ w_r·角色兼容（人工 cue 词典打分）+ w_g·角色门控链一致性（仅对 propagation/mitigation 两角色激活）。权重 (0.52/0.40/0.08) 由文档级 5 折协议在 7 个候选配置中选出。数据集为 40 文档 / 200 问题 / 608 证据句 ID，标签为 **agent 改写 + agent 校验的候选标签（无人工金标）**。

### 核心 claims

1. **主张 A（主结果）**: 全量 C²GES 在 K=3 达 0.2983 evidence F1，显著优于 TF-IDF 查询检索（+0.0861，文档簇 bootstrap p<0.001）、BM25（+0.0710，p<0.001）、SBERT（+0.1010，p<0.001）。
2. **主张 B（机制）**: 消融显示角色兼容是主要来源（去角色掉到 0.2295），图/链一致性只是小的角色选择性辅助信号（去图 0.2923，delta 仅 +0.0060，p=0.0254）。
3. **主张 C（基准定义）**: 定义了一个 NERC 因果角色证据选择 benchmark（40 docs / 200 qs / 608 IDs）。
4. **有界化声明**: 明确否认结构因果推断、图神经网络、电力系统反事实仿真、SOTA 摘要；"counterfactual" 仅指组件消融。

论文的声明体系经过一次"post-freeze"修正（REVISION_NOTE.md）：把原先图项为负/不显著的结果（0.2933 时代）替换为角色门控图项的小正效应（0.2983），标题也从 "Graph-Enhanced / Counterfactual" 降格为 "Causal-Role-Aware"。这个降格处理是诚实的，但也留下一个方法论问题（见 §3 Soundness）。

---

## 2. Claim–Evidence 核查（抽查 18 项）

核验基准：包内唯一完整工件 `supplement/bm25_k_sensitivity/summary.json`（含 K∈{1,3,5} 聚合、分角色、逐文档、配对 bootstrap 全量数据）。

| # | 论文数字/声明（位置） | 工件值 | 判定 |
|---|---|---|---|
| 1 | 全量 C²GES F1 = 0.2983（摘要、Table 3） | 0.29829 | ✓ |
| 2 | TF-IDF 0.2122 / BM25 0.2273 / SBERT 0.1972（Table 3） | 0.21219 / 0.22729 / 0.19724 | ✓ |
| 3 | 摘要 "+40.575% over TF-IDF" | 0.29829/0.21219 = 1.40575 | ✓（精确复算） |
| 4 | 摘要 "+51.231% over SBERT" | 0.29829/0.19724 = 1.51231 | ✓ |
| 5 | Table 5 K 敏感性 12 个单元格（K=1/3/5 × 4 方法） | 全部逐一匹配（如 K=1 C²GES 0.2133=0.21333；K=5 BM25 0.2208=0.22075） | ✓ |
| 6 | vs BM25 +0.0710，CI [0.0423, 0.1000]，p<0.001（Table 4） | 0.07100 [0.04226, 0.09998]，p=0.0 | ✓（精确） |
| 7 | K=5 vs BM25 +0.0643，CI [0.0331, 0.0961]（§6.2 正文） | 0.06427 [0.03313, 0.09607] | ✓ |
| 8 | K=1 时对 TF-IDF/BM25 的配对增益 CI 跨零（§6.2） | vs BM25 [−0.0153, 0.0675]、vs TF-IDF [−0.0078, 0.0757] | ✓（如实报告了不利结果） |
| 9 | vs TF-IDF +0.0861，CI [0.0581, 0.1145]（Table 4，**主比较**） | mean 0.08610 ✓；CI 补充工件为 [0.0583, 0.1146] | ✓/≈（均值精确；CI 第 3 位小数差异，因主工件 seed=202502、补充工件 seed=20260626 独立重采样，属正常） |
| 10 | vs SBERT +0.1010，CI [0.0629, 0.1388]（Table 4） | mean 0.10105 ✓；补充工件 CI [0.0614, 0.1389] | ✓/≈（同上） |
| 11 | 消融值 query-only 0.2152 / no-role 0.2295 / no-graph 0.2923（§6.2） | 0.21517 / 0.22952 / 0.29233 | ✓ |
| 12 | 图项 delta +0.0060（摘要、Table 4） | 0.29829 − 0.29233 = 0.00595 | ✓（聚合一致） |
| 13 | 图项 CI [0.0014, 0.0119]、p=0.0254；vs query-only CI [0.0541,0.1120]；vs no-role CI [0.0416,0.0972]；vs legacy +0.0403 [0.0178,0.0621]（Table 4 四行） | 补充工件**不含**这四组配对比较（只有 vs tfidf/bm25/sbert） | **⚠ 包内无法核验**——数据源是缺失的主 Executor 工件 |
| 14 | 分角色 Table（trigger 0.3114/0.2833/0.4000 … mitigation 0.3167/0.3167/0.3479，共 15 个数） | role_stratified 区块全部逐一匹配 | ✓ |
| 15 | 分角色 delta（vs TF-IDF +0.1006/+0.0470/+0.0436/+0.1438/+0.0955；vs NoRole +0.0723/+0.0475/+0.0281/+0.0988/+0.0971） | 复算全部匹配（误差 ≤0.0001） | ✓ |
| 16 | 图门角色分层表（prop +0.0083、mitigation +0.0214、其余三角色 0.0000） | 0.26107−0.25274=0.00833；0.31667−0.29524=0.02143；trigger/root/impact 全等 | ✓ |
| 17 | Table 3 其余五行（Lead 0.0545、TF-IDF centroid 0.0688、TextRank 0.0700、LexRank 0.0167、Causal trigger 0.1071） | 补充工件不含这五个条件 | **⚠ 包内无法核验**（主工件缺失） |
| 18 | 定性案例（nerc_014 impact F1 0.667、nerc_009 root_cause F1 0.0 等 4 个案例引用 details.jsonl） | details.jsonl 不在包内 | **⚠ 包内无法核验** |
| 19 | 方法常数（8000、(1,2)、0.08、8、0.45、0.55、1.0、0.8、0.25、cue 数 15/21/21/19/19、w=0.52/0.40/0.08） | 与 OPTIMIZATION_PLAN.md 实现事实、main.py 候选网格逐一一致 | ✓ |
| 20 | 数据集 40/200/608、标签 agent_verified_candidate、schema 0 错误 | 补充工件 dataset 区块完全一致（含 40 个 doc_id 清单） | ✓ |

**核查结论**：可核验的 16 项**全部精确命中**（包括两处百分比复算和 30+ 个表格单元格），且论文如实报告了 K=1 CI 跨零这类不利结果——数字诚信度在我评审过的稿件中属于最高一档。**但有 3 类数字（Table 3 五个弱基线行、Table 4 四个消融配对统计、全部定性案例）的原始工件不在投稿包内**，只能靠 REVISION_NOTE 的文字交叉印证。这不是造假信号（缺的恰好是"对自己有利程度最低"的部分，且补充工件与正文的一致率给了强先验），而是**证据包完整性缺口**——投 SCI 前必须把主工件补进复现包。

---

## 3. 七维评分（对齐 mintou 评审标准：severity 0–3，越高越差；conf = 判定置信度）

### 3.1 Novelty — sev 2.2 | conf 0.85

- **[正面]** 任务框架（角色条件化证据句 ID 选择 + NERC 领域 + 五角色 schema）有真实的问题独特性；"role ≠ topical relevance" 的动机论证清晰。
- **[F-nov-1, MODERATE]** 方法本体是 TF-IDF + 手工 cue 词典 + 指数邻近核的加权和——2026 年视角下技术新颖度很低，属于"透明基线工程"。论文自己也把卖点收缩到 auditable/lightweight，这在 IEEE Access/MDPI 的 soundness 审稿模式下可存活，但在任何 novelty 驱动的刊物（IEEE Trans、ACL 系）会被一票否决。
- **[F-nov-2, MINOR]** "定义 benchmark" 是三大贡献之一，但数据集未公开发布（只有路径引用）。不释放数据，benchmark 贡献不成立。

### 3.2 Soundness — sev 2.0 | conf 0.80

- **[正面]** 统计学处理超出同档刊物常态：预声明主比较、文档簇配对 bootstrap（尊重文档内相关性）、非主 p 值降级为诊断、CI 全报、单次执行的不确定性来源如实声明。文档级 5 折 + sha256 折分配防泄漏，权重选择非手调。
- **[F-sound-1, SEVERE｜最大科学软肋]** **标签循环性风险**：证据标签由 agent 改写+agent 校验产生，而角色 cue 词典也是人工/agent 针对同一语料构造的。给"impact"句打标签的 agent 与给"impact"句加分的 cue（MW、load shed、customer interruption）大概率共享同一表层特征偏好——F1 增益可能部分度量的是"cue 与 agent 标注偏好的重合度"而非真实角色判别力。论文承认"非金标"，但**未讨论 cue 词典构造是否见过全量数据集**（5 折协议只保护混合权重选择，不保护 cue 词典本身）。这是 SCI 审稿人最可能证伪的一击。
- **[F-sound-2, MODERATE]** 图门控是**看到图项为负之后**的 post-hoc 补救（REVISION_NOTE 明示从 0.2933/不显著 修到 0.2983/p=0.0254）。虽然通过 CV 候选网格选择做了程序化洗白、且论文把图项定位为"小辅助"，p=0.0254 在 garden-of-forking-paths 语境下证据强度应再打折。所幸该 claim 权重已被压得很低，不构成主张 A/B 风险。
- **[F-sound-3, MINOR]** role_gated_chain 的 G = minmax(R×chain) 里含角色分 R——"no-graph 消融"剥离的不是纯结构信号而是"角色×结构"交互项。公式已如实披露，但解释文字可再精确。

### 3.3 Experiments — sev 2.4 | conf 0.85

- **[正面]** 基线覆盖位置/词法/语义/图中心性/因果 cue 六族 + BM25 补充 + K∈{1,3,5} 敏感性 + 分角色分层 + 消融 + legacy 对照，在"轻量方法"框架内做满了。
- **[F-exp-1, SEVERE（对 SCI）]** **没有任何学习型/神经重排基线**：无 cross-encoder、无 bge/monoT5 reranker、无 LLM zero-shot 基线。2026 年审稿人第一问必然是"为什么不让一个 LLM 直接做这 200 道题"。Limitations 已列为 future work，但对 SCI 刊这是"缺席的大象"——尤其 SBERT（0.1972）弱于 TF-IDF（0.2122）这个反常结果暗示语义基线未调优。
- **[F-exp-2, MODERATE]** 规模：40 文档/200 问题、单数据集、单次执行。绝对 F1 仅 0.298（顶配下 K=3 每 3 句只命中 ~0.9 句），实用价值论证偏弱。
- **[F-exp-3, MINOR]** 分割敏感性、图窗口敏感性缺失（已在 Limitations 预声明）。

### 3.4 Reproducibility — sev 2.2 | conf 0.90

- **[正面]** 正文含完整确定性打分规范表（Table：所有常数、cue 数、权重、折协议），方法可"不读代码复现"——这达到了 OPTIMIZATION_PLAN 的验证目标。
- **[F-rep-1, SEVERE｜阻断级]** 复现包实际不可运行：`main.py` 依赖不在包内的 `verification_pilot/scripts/run_baselines.py`、`run_c2ges.py`、`three-pack/config.yaml` 和数据目录（含硬编码 fallback 路径 `/media/lenovo/data2/cja/GridMind/...`）；`requirements.txt` 只有 numpy（实际需要 rouge-score/sklearn/networkx/sentence-transformers）；本仓库 smoke run 已确认失败（`debug/initial_smoke.md`）。
- **[F-rep-2, MODERATE]** 数据集未公开；主 Executor 工件缺失（见 §2 第 13/17/18 项）。
- **[F-rep-3, MINOR]** `code/README.md` 标题仍是**旧标题**"Causal and Counterfactual Graph-Enhanced Extractive Summarization"——与已降格的新定位直接矛盾，审稿人看到会质疑修订完整性。

### 3.5 Related Work — sev 1.2 | conf 0.85

- 54 条参考文献，2022–2025 占比 ~67%，覆盖 QFS/抽取式摘要/图摘要/证据检索/因果 NLP/电力可靠性六个面，逐段有对比定位句（"In contrast to..."）。质量高于 EI 均值，达到 MDPI/Access 常态。
- **[F-rw-1, MINOR]** 无 2026 文献；LLM-based 检索/评估文献（RankGPT、LLM-as-judge 类）完全缺席，与 F-exp-1 呼应。

### 3.6 Clarity — sev 1.3 | conf 0.85

- **[正面]** 写作干净、声明边界控制是范例级（每个强数字旁边都有 scope 限定）；图表齐全（2 架构图 + 2 结果图 + 7 表）。
- **[F-clar-1, MODERATE｜目标刊错配]** 全文是 **IEEE Access 皮肤**：`\documentclass{ieeeaccess}`、`\history{}`、`\doi{10.1109/ACCESS...}`、正文 §4.3 明写 "intelligible to **IEEE Access readers**"。投 Engineering Letters 需换 IAENG 双栏模板并清除所有 Access 痕迹；这些残留说明稿件从未真正对齐过 EL。
- **[F-clar-2, MINOR]** 摘要同时给 Index Terms 和 keywords 两套关键词（Access 风格），EL 只要一套。

### 3.7 Ethics — sev 0.8 | conf 0.90

- 公开 NERC 报告文本，无隐私/双重投稿问题；agent 标注的来源与局限在正文、metadata、Limitations 三处一致披露——诚信正资产。
- **[F-eth-1, MINOR]** 作者行 "Anonymous" + email@example.com 占位；投稿前需补真实作者、单位、（视刊物）AI 辅助写作声明。

### RRI 汇总

| 维度 | Sev | Conf | 加权 |
|---|---|---|---|
| Novelty | 2.2 | 0.85 | 1.87 |
| Soundness | 2.0 | 0.80 | 1.60 |
| Experiments | 2.4 | 0.85 | 2.04 |
| Reproducibility | 2.2 | 0.90 | 1.98 |
| Related Work | 1.2 | 0.85 | 1.02 |
| Clarity | 1.3 | 0.85 | 1.11 |
| Ethics | 0.8 | 0.90 | 0.72 |
| **合计** | | | **10.34/28 = 36.9%** |

**RRI ≈ 37%**——与 mintou_p3 终审（34.5%，判定"实质学术水平适合 Energies 投稿"）同一档位。差异结构不同：本稿的 Soundness/统计链条更强，但 Novelty/Experiments（缺神经基线）与 Reproducibility（包不可运行）更弱。

---

## 4. EI（Engineering Letters）现状可投性

### Desk Screen

| 项 | 状态 | 严重度 |
|---|---|---|
| 模板 | ✗ ieeeaccess.cls + IEEE Access DOI/history 占位 + 正文 "IEEE Access readers" 字样，非 IAENG 模板 | **阻断——必改** |
| 作者/单位/通讯 | ✗ "Anonymous" + email@example.com | **阻断——必改** |
| 题目-内容一致 | 通过（降格后的题目与证据匹配良好） | -- |
| 摘要含量化结果 | 通过（0.2983 / +40.575% / +51.231%） | -- |
| 图表 | 通过（4 图 7 表，图注齐全） | -- |
| 参考文献 | 通过（54 条，bib/bbl 一致，无 TODO） | -- |
| 英文 | 通过（高于 EL 均值） | -- |
| 页数 | 15 页 Access 版式，转 IAENG 版式后需复查 | 低 |
| 附带代码/数据 | EL 不强制 | -- |

### 判定

**内容层面对 Engineering Letters 是显著过杀（over-qualified）**。EL 的实际录取门槛低于本稿的证据水平（EL 常见录用稿无 bootstrap、无消融、无预声明主比较）。当前唯一不可投的原因是两项纯行政阻断（模板转换 + 作者信息），合计 **1–2 人日**。修复后录用概率估 **70–80%**，desk-reject 风险主要来自模板不合规。

**但要指出机会成本**：这篇稿子最费钱的部分（统计链、消融矩阵、诚实定界）恰恰是 SCI soundness 型刊物付费认可、而 EL 不额外奖励的东西。投 EL 等于用 SCI 级证据链买一个 EI 出版物。

---

## 5. SCI 升级可行性

### 差距清单（按目标刊）

| 缺口 | 影响的刊 | 工作量 |
|---|---|---|
| **G1 数据集公开发布**（Zenodo/GitHub + DOI；否则删除 "defines a benchmark" 贡献句） | 全部 | 1–2 人日 |
| **G2 复现包修复**（补 verification_pilot 脚本 + 主 Executor 工件 + 完整 requirements + 删硬编码路径 + 改 code/README 旧标题） | 全部 | 1–2 人日 |
| **G3 神经/学习型基线 ≥2 个**（cross-encoder ms-marco-MiniLM、bge-reranker；强烈建议加 1 个 LLM zero-shot 基线）。200 题 × 平均几十句/篇，单卡数小时可跑完。风险：若 cross-encoder 胜出，需把故事改写为"透明性/成本/可审计 tradeoff"——按 K 敏感性表的差距（C²GES 领先 BM25 仅 0.07），被零样本 LLM 超越概率**偏高**，须预案 | IEEE Access 强需求；MDPI 可作加分项 | 3–5 人日（含改写） |
| **G4 人工金标子集 + IAA**（抽 50–100 题、双标注、Cohen's κ、报告 agent 标签一致率）——直接回应 F-sound-1 循环性 | IEEE Access/Electronics 审稿人大概率索要 | 3–4 人日 |
| **G5 cue 词典构造流程披露**（是否基于全语料迭代；加一段循环性讨论） | 全部 | 0.5 人日 |
| G6 作者信息/声明/模板按目标刊转换 | 全部 | 0.5–1 人日 |
| G7（可选）扩数据集至 60+ 文档或第二语料 | 冲更高档时 | 5–10 人日 |

### 目标刊逐一评估（画像来源：Paper_CCF journal 模块，2026-07 快照）

| 刊 | 契合度 | 理由 | 修后录用预测 |
|---|---|---|---|
| **IEEE Access**（IF≈4.2, Q2, APC≈$2,160, ~4 周首决, 二元决定） | **高** | soundness-not-novelty 审稿模式与本稿气质完全同构；**稿件本来就是按 IEEE Access 写的**（ieeeaccess.cls、工作区名 c2ges-*-ieeeaccess、正文 "IEEE Access readers"），模板转换成本≈0；蒸馏样本显示已录用 DL 论文"4–6 基线、零显著性检验"——本稿统计链远超该常态 | 完成 G1–G6 后 Accept ~50–60%（二元制无修改回旋，标签来源是最大风险点；G4 做完可到 ~65%） |
| **MDPI Electronics**（IF≈2.9, Q2, APC≈CHF 2,400, ~15 天首决, AI Section） | **高** | 蒸馏 15 篇电力样本显示"算法/IT 侧新颖性 + 应用为载体"即可、0/15 有显著性检验、0/15 开源——本稿超配；NLP-for-grid 放 AI 或 Computer Science & Engineering Section 合理 | 完成 G1/G2/G5/G6（G3/G4 可作 major revision 弹药）后 Accept/Minor ~60–70% |
| **MDPI Applied Sciences**（IF≈2.9, ~Q2, APC≈CHF 2,400） | 中高 | 兜底选项，标准与 Electronics 相近但更泛；Electronics 的 EE/CS 身份更对口 | 同 Electronics 略高 |
| MDPI Energies（IF≈4.0, Q2） | 中 | 领域是电网但贡献是 NLP 方法——Energies 审稿人会问"能源侧洞见在哪"；除非把分析重心改写为可靠性工程应用，否则错位 | 不首选 |
| CSEE JPES / PCMP（Q1） | 低 | PCMP 限保护/控制/故障/稳定，纯文本方法出界；JPES 要电力系统方法学贡献 | 不推荐 |
| NLP 类（LREC 资源赛道等） | 中 | benchmark 贡献对口，但要求人工标注质量证明（G4 变硬性）且是会议线，与"SCI 期刊"目标不符 | 备选路线 |

### 总工作量与值不值

- **最短 SCI 路线（MDPI Electronics）**: G1+G2+G5+G6 ≈ **4–6 人日**（不跑新实验，赌审稿人不逼 G3/G4，被逼则修改期内补）。
- **稳健 SCI 路线（IEEE Access 或 Electronics）**: G1–G6 全做 ≈ **9–14 人日**。
- **值不值**: 值。理由：(a) 稿件已是 IEEE Access 格式，投 EL 反而要多做模板转换；(b) 本稿的统计证据链在 soundness 型 SCI 刊是稀缺加分项，在 EL 是无人定价的沉没成本；(c) 主要缺口（G3/G4）都是天级而非月级工作。唯一支持投 EL 的情形是：**急需在 1–2 周内锁定一个录用**（EL 审稿慢于 MDPI，这点其实也不成立——MDPI 15 天首决更快），或作者对 APC（~2 万元人民币级）敏感（EL 版面费显著更低）。

---

## 6. 明确推荐

### 推荐：**改投 SCI（首选 IEEE Access，次选 MDPI Electronics），不建议按现状投 Engineering Letters**

决策理由压缩成三句：

1. **格式事实**：稿件本来就是一篇写好的 IEEE Access 论文（模板、DOI 占位、读者称谓），投 EL 的"省事"是幻觉——转 IAENG 模板的工作量不小于直接投 Access。
2. **证据质量**：可核验数字 16/16 精确命中 + 主动报告不利结果（K=1 CI 跨零），这条证据链的市场价值在 soundness 型 SCI 刊最大化。
3. **风险可控**：最大科学风险（agent 标签循环性、缺神经基线）用 G3+G4 共 6–9 人日可以对冲；即便 LLM 基线胜出，"透明可审计的确定性重排器 vs 黑箱 LLM"的 tradeoff 故事在 Access/Electronics 依然成立。

若时间/预算约束强 → 退而求其次的**两步走**：先花 4–6 人日走"最短 MDPI Electronics 路线"投出（15 天首决，快过 EL），被拒再降级 EL（EL 修复量已包含在 G6 中）。

### P0（任何投稿目标都必须，≈2–4 人日）

| # | 修改项 | 位置 |
|---|---|---|
| 1 | 作者/单位/通讯邮箱占位符替换（Anonymous / email@example.com / State Grid 占位地址核实） | paper.tex 头部 |
| 2 | 目标刊模板对齐：投 Access 保留现模板删占位 DOI；投 EL 转 IAENG 模板并**删除正文 "intelligible to IEEE Access readers"**（§4.3） | 全稿 |
| 3 | `code/README.md` 旧标题（"Causal and Counterfactual Graph-Enhanced..."）改为现标题；`requirements.txt` 补全 rouge-score/scikit-learn/networkx/sentence-transformers | source/code/ |
| 4 | **主 Executor 工件入包**：c2ges_role_selective_graph/{summary.json, details.jsonl, cv_protocol.json, heldout_predictions.jsonl}——当前 Table 3 五个基线行、Table 4 四组消融配对 CI、全部定性案例在包内无凭据 | source/supplement/ 或复现仓库 |
| 5 | `main.py` 删除 `/media/lenovo/...` 硬编码 fallback 路径，或补齐 `verification_pilot` 脚本使包可独立运行 | source/code/main.py |

### P1（SCI 投稿前强烈建议，≈6–9 人日）

| # | 修改项 | 说明 |
|---|---|---|
| 6 | 数据集公开发布（Zenodo DOI 或 GitHub release），Data Availability 落地 | 否则删除"defines a benchmark"贡献句 |
| 7 | 加 2 个学习型基线（cross-encoder + bge-reranker）+ 1 个 LLM zero-shot 基线；若被超越，将贡献叙事切换为透明性/成本/可审计 tradeoff 并给延迟/成本对比表 | 直接拆除最大审稿炸弹 |
| 8 | 人工金标子集（50–100 题双人标注 + Cohen's κ + agent 标签一致率），写入 §3 与 Limitations | 回应标签循环性 |
| 9 | 加一段 cue 词典构造流程与循环性讨论（cue 设计是否接触过全量标注；R×chain 交互对 no-graph 消融解释的影响） | §4.2/§7 |

### P2（锦上添花）

| # | 修改项 |
|---|---|
| 10 | 摘要中 "40.575%/51.231%" 保留 3 位小数显得伪精确，建议改 "≈41%/51%" |
| 11 | 补 2–3 篇 2025–2026 LLM 检索/重排文献（RankGPT 类）进 Related Work |
| 12 | role coverage 诊断指标正文化；错误类型（role-mismatch/近邻/隐式因）计数表 |
| 13 | 图门 p=0.0254 处加一句 post-hoc 修订来源披露（REVISION_NOTE 内容正文化一句即可） |

### 决策预测

| 路线 | 预计结果 |
|---|---|
| EL 现状直投（不修 P0） | Desk reject（模板+匿名作者） |
| EL 完成 P0 后投 | Accept ~70–80%，但机会成本高 |
| IEEE Access 完成 P0+P1 后投 | Accept ~55–65%（二元决定；剩余风险=标签来源） |
| MDPI Electronics 完成 P0 + P1#6/#9 后投 | Accept/Minor ~60–70%，首决 ~15 天 |

---

## 7. 一句话总评

**这是一篇"用 SCI 级证据纪律写成、却被错误地摆在 EI 货架上的小规模基准论文"**：可核验数字 100% 命中、统计链完整诚实，但复现包不可运行、缺神经基线、标签无人工金标三处硬伤决定了它的天花板与下限——修 2–4 人日可投 EL 稳收，修 9–14 人日投 IEEE Access/Electronics 更配得上它已经付出的证据成本；鉴于稿件本身就是按 IEEE Access 写的，推荐直接走 SCI 路线。
