# Round-2 投稿前终审：C²GES → IEEE Access

- **日期**: 2026-07-19
- **评审轮次**: Round 2（对抗式投稿前终审；paper_reviews 框架，对齐 mintou_p3 ROUND_REVIEW 方法：claim–evidence 核查 + 内部一致性审计 + desk screen + 七维评分 + 决策预测）
- **稿件**: `source/paper.tex`（594 行；`source/paper.pdf` 为 2026-06-27 旧版，**未包含本轮修改**）
- **目标期刊**: IEEE Access（画像 `Paper_CCF/journals/ieee-access`，2026-07 快照：IF≈4.2 Q2、APC≈$2,160、~4 周首决、**二元 Accept/Reject + 一次重投上限**、soundness-not-novelty）
- **前序**: Round-1 `PUBLICATION_ASSESSMENT.md`（2026-07-17，RRI≈37%，推荐改投 IEEE Access）；两轮升级见 `SCI_UPGRADE_CHANGELOG.md`（07-17 手稿加固轮 + 07-19 包内补充证据开采轮）；待补清单 `MISSING_ARTIFACTS.md`
- **本轮核验证据源**: `source/supplement/bm25_k_sensitivity/summary.json`（原始运行工件，221 KB，git sha 08fd42f9，run 2026-06-26）——本评审**绕过**作者自产的 `derived_tables.json`，用独立脚本直接对原始 summary.json 复算；另核 `references.bib`、`paper.bbl`、`code/main.py`、`code/README.md`、`code/requirements.txt`、`code/prepared_baselines/`、`charts/`

---

## 0. Round-1 P0/P1/P2 项解决状态核查（逐项亲验，不信 changelog）

| R1 # | 级 | 修改项 | 本轮核验结果 | 判定 |
|---|---|---|---|---|
| P0-1 | P0 | 作者/单位/通讯占位符 | `\author{Anonymous}`、`email@example.com` 仍在（第 20/22 行）；地址行 "Dispatching and Control Center, State Grid Corporation" 亦待核实 | **未解决（USER，预期内）** |
| P0-2 | P0 | 假 DOI + "IEEE Access readers" 自指 | `\doi{}` 已置空（grep 全稿+bib 无 `10.1109/ACCESS`）；"IEEE Access readers" 字样已消失，§4.3 改为 venue-neutral 表述 | **已解决 ✓** |
| P0-3 | P0 | code/README 旧标题 + requirements 不全 | README 首行已是现标题；requirements.txt 含 numpy/scikit-learn/networkx/lexrank/rouge-score/sentence-transformers | **已解决 ✓** |
| P0-4 | P0 | 主 Executor 工件入包 | 包内仍只有 bm25_k_sensitivity 补充工件；缺口已在 MISSING_ARTIFACTS.md §3 精确收窄并在正文 Data Availability 如实分割披露 | **未解决（blocked，已诚实披露）** |
| P0-5 | P0 | main.py 硬编码 `/media/lenovo/` 回退路径 | grep 无 `media/lenovo`；已改 `--workspace` CLI + `C2GES_WORKSPACE` 环境变量 + 校验报错 | **已解决 ✓** |
| P1-6 | P1 | 数据集公开发布 | Data Availability 节已加，但 `[TODO: repository URL and archival DOI]` 未落地（blocked on 原工作区） | **未解决（blocked）** |
| P1-7 | P1 | 学习型/LLM 基线 | `prepared_baselines/` 四脚本（CE/BGE/LLM/common）在包，协议对齐；**无任何真实数字**；Discussion 新增 tradeoff 段、Limitations 声明 | **准备就绪未执行（blocked）** |
| P1-8 | P1 | 人工金标子集 + κ | 未执行；§4 循环性小节 + Limitations 已精确预声明（50–100 题双标注 + Cohen's κ + agent 一致率） | **未解决（blocked）** |
| P1-9 | P1 | cue 词典构造与循环性讨论 | 新小节 §4.4（`sec:cue_lexicon_construction_and_circularity`）：cue 作者身份不受 5 折保护、与 agent 标签共享表层偏好的循环风险、G=minmax(R×chain) 交互项对 no-graph 消融解释的影响——三点全部到位且与 Limitations 交叉引用 | **已解决 ✓** |
| P2-10 | P2 | 摘要伪精度 40.575%/51.231% | 摘要现为 "approximately 41%"/"approximately 51%"；复算 0.29829/0.21219−1=40.57%、/0.19724−1=51.23%，四舍五入正确 | **已解决 ✓** |
| P2-11 | P2 | LLM 重排文献 | qin2024pairwise（NAACL Findings 2024, pp.1504–1518, doi:10.18653/v1/2024.findings-naacl.97）、zhuang2024setwise（SIGIR 2024, doi:10.1145/3626772.3657813）、ren2025selfcalibrated（WWW 2025, pp.3692–3701, doi:10.1145/3696410.3714658）——bib 与 bbl 均已入，元数据与已知真实文献一致 | **已解决 ✓** |
| P2-12 | P2 | role coverage/错误计数正文化 | 以包内真实数字（分角色分层表 + 逐文档离散度）实质填补；但 §5.3 仍残留一句 "Role coverage is used as a diagnostic..." 而全文无任何 role coverage 数字（见 F-clar-2） | **实质解决/残留一句 ✓−** |
| P2-13 | P2 | p=0.0254 post-hoc 披露 | §6.2 Table 4 旁已加完整披露：门控源于 post-freeze 修订、冻结版全角色图项无可靠收益、p=0.0254 应读作 diagnostic 而非 confirmatory | **已解决 ✓** |

**小结**: Round-1 全部可在本机完成的项（P0-2/3/5、P1-9、P2-10/11/13）已完成且质量高；全部未完成项都被同一资源（原实验机工作区）阻塞，且**均已在稿内诚实披露**而非掩盖。

---

## 1. 数字核验（NUMBER VERIFICATION）

**方法**: 独立脚本直接读原始 `summary.json`（不经过作者的 derived_tables.json / analyze 脚本），对稿件数字做 4 位小数舍入比对 + 派生量复算（差值、百分比、Bonferroni 逻辑）。**自动核验 96 项 + 手工核验 13 项 = 109 项。**

### 1.1 新增数字（本轮升级新加，全部核验）

| # | 稿件声明（位置） | 工件值 | 判定 |
|---|---|---|---|
| 1 | 角色分层基线表 Table `role_strata_baselines` 15 个单元格：BM25 0.2250/0.2154/0.2289/0.2181/0.2490；NoRole 0.2392/0.2119/0.2330/0.2440/0.2195；Full 0.3114/0.2594/0.2611/0.3429/0.3167 | role_stratified['3'] 逐一匹配（如 BM25 root 0.21535714→0.2154） | ✓×15 |
| 2 | Full−BM25 delta 列：+0.0864/+0.0440/+0.0321/+0.1248/+0.0676 | 独立复算逐一匹配 | ✓×5 |
| 3 | 正文分析句 "no-role 在 mitigation (0.2195) 和 root cause (0.2119) 低于 BM25 (0.2490/0.2154)" | 0.2195<0.2490 ✓、0.2119<0.2154 ✓ | ✓ |
| 4 | 逐文档离散度：full C²GES 0.0800–0.5219，mean 0.2983，sample std 0.1092，无零文档 | 从 40 个 document_level 条目独立重算：min 0.08、max 0.52190、mean 0.29829、stdev 0.10921、n_zero=0 | ✓×5 |
| 5 | BM25 逐文档 0.0571–0.5000；SBERT 有 1 个零证据文档 | min 0.05714/max 0.5；sbert n_zero=1 | ✓×3 |
| 6 | 新配对比较：vs SBERT K=1 +0.0573 [0.0093, 0.1013] p=0.0182 | 0.05733 [0.00933, 0.10134] p=0.0182 | ✓×4 |
| 7 | vs SBERT K=5 +0.0808 [0.0387, 0.1208] p<0.001 | 0.08079 [0.03869, 0.12079] p=0.0 | ✓×4 |
| 8 | vs TF-IDF K=5 +0.0688 [0.0421, 0.0949] p<0.001 | 0.06881 [0.04212, 0.09492] p=0.0 | ✓×4 |
| 9 | K=3 SBERT precision +0.1067 [0.0683, 0.1467]、recall +0.0996 [0.0575, 0.1408] | 0.10667 [0.06833, 0.14667]；0.09958 [0.0575, 0.14083] | ✓×6 |
| 10 | "K=1 SBERT 结果不能存活对 9 个基线比较的保守校正" | 工件恰有 9 个基线比较；Bonferroni 0.05/9=0.0056 < 0.0182——判断正确 | ✓ |
| 11 | 数据谱系：25→40 docs、15 新文档、验证 6 pass/8 minor-repair/1 answer-narrowing、初次并行验证 5 批 HTTP 429 后串行重跑、schema 0 错误、每角色 40 题、1 个低多样性标记文档（2016 State of Reliability） | dataset.base_dataset=agent_audit_25doc；independent_verifier_summary={pass:6, pass_with_minor_repaired:8, fail_repaired_by_answer_narrowing:1, failed_verifier_batches_due_to_429:5}；annotation_summary={new:15, errors:0, flag:nerc_042_2016...[s036]}；role_stratified 每角色 questions=40 | ✓×8 |
| 12 | Data Availability："bootstrap 10000 samples, seed 20260626" | paired_comparisons.samples=10000, seed=20260626 | ✓×2 |
| 13 | Data Availability："TF-IDF/SBERT CI 端点与印刷 Executor 值一致性在 0.002 以内" | 实测最大差 0.0015（SBERT lower 0.0629 vs 0.06140），其余 0.0001–0.0002——声明保守、成立 | ✓ |

### 1.2 既有头条数字复核

| # | 稿件声明 | 工件值 | 判定 |
|---|---|---|---|
| 14 | Full C²GES 0.2983 ± 0.2409 / P 0.2950 / R 0.3325 / ROUGE 0.3732（摘要+Table 3） | 0.29829/0.24088/0.295/0.3325/0.37316 | ✓×5 |
| 15 | 摘要 ~41% / ~51% | 40.5745% / 51.2313% | ✓×2 |
| 16 | vs BM25 +0.0710 [0.0423, 0.1000] p<0.001（Table 4 + §6.2） | 0.07100 [0.04226, 0.09998] p=0.0 | ✓×4 |
| 17 | vs TF-IDF +0.0861、vs SBERT +0.1010（Table 4 均值） | 0.08610 / 0.10105 | ✓×2 |
| 18 | 消融 0.2152 / 0.2295 / 0.2923；消融均值差 0.0831/0.0688/0.0060（配对差=均值差，成立） | 0.21517/0.22952/0.29233；复算 0.08312/0.06876/0.00595 | ✓×6 |
| 19 | K 敏感性 12 格（K∈{1,3,5} × 4 方法）+ K=1 对 TF-IDF/BM25 CI 跨零 | 全部匹配；[−0.0078, 0.0757]、[−0.0153, 0.0675] 确实跨零 | ✓×14 |
| 20 | 图门分层表：prop +0.0083、mitigation +0.0214、其余三角色 delta=0，聚合 (0.0083+0.0214)/5≈0.0060 自洽 | 全部匹配 | ✓×10 |

### 1.3 核验结论

- **109/109 全部通过（100%）**。0 个数字错误、0 个方向性错误、0 个夸大舍入。
- 唯一的"不匹配"是已知且**已在稿内主动披露**的 4 个 CI 端点（Table 4 的 TF-IDF/SBERT 行印的是原 Executor seed 的 bootstrap CI，包内补充工件用独立 seed 20260626 复现到 ≤0.0015）——这是披露质量的正资产而非问题。
- 作者的 `analyze_supplement_evidence.py`（105/109 自查）与本评审的独立复算相互印证；本轮首次确认**补充工件本身就是论文主 K=3 运行**（7 条件全量），Round-1 认定的"包内无凭据"范围被真实收窄到：Table 3 五个弱基线行、Table 4 四组消融/legacy 配对 CI+p、fixed-legacy 条件、cv_protocol、§7 定性案例。
- 连续两轮 100% 命中 + 主动报告不利结果（K=1 CI 跨零、SBERT 弱于 TF-IDF、no-role 局部低于 BM25），数字诚信度维持最高档。

---

## 2. 内部一致性与叙事审计

### 2.1 循环性小节 ↔ Limitations：**对齐 ✓**

§4.4 的三个承认（cue 作者身份不受 5 折保护；agent 标签与人工 cue 可能共享表层词汇偏好；增益部分可能度量"两个标注式先验的重合"）与 Limitations 第 2 条逐句呼应并显式 `\ref` 交叉引用；计划的验证手段（50–100 题双人金标 + κ + agent 一致率）在两处表述一致。R×chain 交互项 caveat（no-graph 消融剥离的是角色×结构交互而非纯结构信号）同时出现在 §4.4 与 Table `scoring_specification` 的公式披露——Round-1 的 F-sound-1/F-sound-3 从"未讨论"变为"已充分披露、待数据验证"。

### 2.2 Data Availability 的包内/Executor 证据分割：**准确 ✓（逐项亲测）**

- 声称包内可证的 8 类：Table 3 四个查询行含全部 std ✓、消融聚合与均值差 ✓、K 敏感性全表 ✓、9 组配对 bootstrap（10000/seed 20260626）✓、三张角色分层表 ✓、逐文档离散度 ✓、数据谱系计数 ✓、seed 级 CI 调和（≤0.002，实测 ≤0.0015）✓。
- 声称包外的 6 类：弱基线五行、消融/legacy 的 CI+p、fixed-legacy 条件、cv_protocol、§7 案例——**亲验 summary.json 中确实不存在**（aggregate 仅 7 条件、comparisons 仅 9 个基线键、无 details.jsonl）。分割无一处夸大。

### 2.3 Transparency-tradeoff 框架是否越界：**未越界，但有一处软肋**

Discussion 的定位句写得克制："value proposition 不是预期在 F1 上支配学习型系统，而是透明性/可审计性/成本"；并明确"若 cross-encoder 或 LLM 在本基准上更高 F1，不会消除确定性可审计打分器的角色，而是锐化 accuracy vs traceable selection 的 tradeoff"；Limitations 明言"结果 deliberately not predicted here"。这是在无 LLM 基线数字条件下能写到的合规上限。**软肋**：该段承诺恰当的比较应"report accuracy alongside per-query cost, latency, and explanation fidelity"，而本文自身未给任何成本/延迟量表——审稿人可反问"你主张的 tradeoff 两端你都没量化"。跑完基线后必须兑现这张成本对比表（changelog 已列入待办）。

### 2.4 发现的次级不一致（本轮新记录）

1. **[F-cons-1, MINOR]** §5.3 定义了 role coverage 诊断指标，但全文与工件均无该数字（Executor 工件独有）。留一句无兑现的指标定义会引审稿人索要——删句或加"reported in the artifact"限定。
2. **[F-cons-2, MINOR]** Table 4 内 CI 的 seed 来源混合：BM25 行来自补充工件（seed 20260626），TF-IDF/SBERT/消融行来自 Executor（seed 202502）。Data Availability 有披露，但表格本身无脚注——建议在 Table 4 注中加一行来源说明，避免"同表异源"被误读。
3. **[F-cons-3, MINOR]** §6.1 正文说 "std ... about 0.24" 指 200 题级 std，紧接着逐文档段落说 "sample standard deviation 0.1092"——两个不同粒度的 std 相邻出现，已各自标注粒度，但排版上建议再强化（如"question-level"/"document-level"前缀），防止快读误会。

---

## 3. Desk Screen（IEEE Access 投稿模拟）

| 项 | 状态 | 严重度 |
|---|---|---|
| 模板 | ✓ `ieeeaccess.cls`，正版 Access 骨架（history/doi/keywords 宏齐全） | -- |
| 作者/单位/通讯/ORCID | ✗ `Anonymous` + `email@example.com`；无 ORCID；无作者简介（Access 惯例含 photo+bio） | **阻断——不可投** |
| Data Availability | ✗ `[TODO: repository URL and archival DOI]` | **阻断** |
| AI 使用声明 | 节已具备、内容合规（agent 标签来源 + LLM 辅助写作 + 作者负责声明），但 `[TODO: confirm final wording]` 残留 | **阻断（改一句即除）** |
| PDF 与源不同步 | ✗ `paper.pdf` 为 2026-06-27 版，**不含两轮升级的全部内容**；本机无 LaTeX 工具链，bbl 为手工追加——投稿前必须完整 `pdflatex→bibtex→pdflatex×2` 重建并复查版式 | **阻断** |
| 摘要 | ✓ 204 词（Access 上限 250 内），含量化结果 | -- |
| 关键词 | ⚠ 摘要末尾内嵌 "Index Terms---..." 一行 + 独立 `\begin{keywords}` 双份——Access 只经 keywords 环境排 INDEX TERMS，摘要内那行会重复打印 | 低（格式纠偏） |
| 数学排版 | ⚠ 32 处数学模式内 `\_`（`D\_i`、`w\_q`、`s\_j`、`\mathcal{R}\_g` 等）渲染为**字面下划线而非下标**，且与同一公式内正确的 `_{...}`（如 `s_{i1}`、`q_{i,r}`）混排——主打分公式即受影响 | 中（观感伤害，1 小时修） |
| §4.2 cue 列表引号 | ⚠ `` `\texttt{fault,'' }\texttt{trip,'' }...`` 引号方向/嵌套破损，渲染为错乱的引号串 | 低 |
| 图表 | ✓ 4 图（charts/ 下 4 个 png 均在）+ 7 表，图注齐 | -- |
| 参考文献 | ✓ 57 条，新增 3 条 LLM 重排文献 bib/bbl 双入且元数据可信；无 TODO、无假 DOI | -- |
| Graphical abstract | 未准备（Access 支持/鼓励，投稿系统会索要一张代表图——可复用 fig_2） | 低 |
| 页数 | 旧版 15 页 + 新增约 1 页，远低于建议 ~20 页上限 | -- |
| 双盲 | Access 单盲，无匿名化要求——现在的 Anonymous 反而是待填而非合规 | -- |

**Desk Screen 判定**: 4 个硬阻断（作者信息、DA-TODO、AI-TODO、PDF 重建），全部为行政/机械项，合计 ≤1 人日（在拿到仓库 URL 的前提下）。无学术性 desk-reject 风险。

---

## 4. 七维评分（vs Round-1；severity 0–3 越高越差，conf=判定置信度）

| 维度 | R1 Sev | R2 Sev | Conf | 加权 | 变化依据 |
|---|---|---|---|---|---|
| Novelty | 2.2 | **2.1** | 0.85 | 1.79 | 方法本体未变（TF-IDF+cue 词典+邻近核加权和）；LLM 文献定位与 tradeoff 叙事让"透明基线工程"的卖点更自洽；benchmark 贡献仍押在未发生的数据发布上 |
| Soundness | 2.0 | **1.6** | 0.80 | 1.28 | R1 最大软肋（F-sound-1 循环性）从"未讨论"变为"精确披露+预告验证方案"；F-sound-2（post-hoc 图门）已按 P2-13 正文披露且 p=0.0254 降级为 diagnostic；F-sound-3（R×chain 交互）已公式级披露。风险本体仍在（无金标），但 claim-evidence 对齐已无懈可击 |
| Experiments | 2.4 | **2.2** | 0.85 | 1.87 | 角色分层×3 表 + 逐文档离散度 + 9 组配对全披露 + 多重比较 caveat 增厚了证据密度；但**核心缺口未动**：0 个学习型/LLM 基线（harness 备好≠数字存在），SBERT<TF-IDF 的反常仍无解释性补强 |
| Reproducibility | 2.2 | **1.9** | 0.90 | 1.71 | main.py 去硬编码+CLI 化、requirements 补全、README 纠题、analyze 脚本+derived tables 提供机器可查证据链；但数据集与主 Executor 工件仍缺，包仍无法端到端重跑主实验 |
| Related Work | 1.2 | **1.0** | 0.85 | 0.85 | 57 条；LLM 重排三篇真实文献补齐了 R1 唯一指出的空白（RankGPT 类缺席） |
| Clarity | 1.3 | **1.0** | 0.85 | 0.85 | R1 的目标刊错配（F-clar-1）已消除——现在名实相符是 Access 稿；伪精度已修。新账：数学 `\_` 下标缺陷、cue 列表引号破损、摘要内 Index Terms 重复、PDF 未重建 |
| Ethics | 0.8 | **0.5** | 0.90 | 0.45 | AI 使用声明节 + post-hoc 修订披露 + 数据谱系（含 429 重跑、修复计数、低多样性标记）三处增透明——诚信披露密度超出该刊常态一个数量级 |
| **合计** | 10.34/28 = **36.9%** | | | **8.80/28 = 31.4%** | |

**RRI 从 ≈37% 降至 ≈31%**（好方向；下降 5.5 pp）。改善集中在 Soundness（−0.4）与 Ethics/Clarity/RW；**Experiments 仅 −0.2，因为唯一 SEVERE 项（无学习型基线）原地未动**——这也是剩余风险的全部重心。

---

## 5. 判定（VERDICT）

### 5(a) 科学完成度：**"披露完备"但非"证据完备"**

本稿达到了不新增实验所能达到的上限：每个数字可溯源、每个弱点被点名、每个缺口有预案。但三件事使它在科学上仍是 pending 状态：

1. **学习型/LLM 基线 = 0 个数字**（决定 Experiments 维度的天花板）；
2. **人工金标 = 0 题**（决定循环性风险能否被定量约束）；
3. **数据集与主工件未发布**（决定 benchmark 贡献句与 5 类包外数字的可验证性）。

三者被同一资源阻塞：原实验机工作区（`c2ges-causal-mechanism-ieeeaccess` + `c2ges-evidence-audit-krill`，已邮件索取）。

### 5(b) 关键战略问题：能否在 3 个基线跑完之前投 IEEE Access？

**结论：不建议，且严格说"现在投"是个伪选项。理由分三层：**

**第一层（机械）**：当前根本不可投——作者行、DA-TODO、AI-TODO、PDF 未重建 4 个硬阻断。其中 DA-TODO 的消除本身需要数据集发布，而数据集在被阻塞的原工作区里。**即"投稿的前置条件"与"跑基线的前置条件"是同一个资源**。一旦工作区到手，跑 3 个 CPU/API 级基线只增加约 3–5 人日——相对于已经等待的时间，边际成本极小。"抢在基线前投稿"节省不了实质时间，却把可预见的审稿炸弹带进一个**二元决定 + 仅一次重投**的评审制度。

**第二层（风险算术）**：Access 无 major-revision 回旋。2026 年一篇重排论文不带任何学习型基线，被至少一位审稿人点名的概率估 50–65%（该刊蒸馏样本显示已录用 DL 论文只有 4–6 个弱基线、零显著性检验——本稿统计链远超常态，但"缺 2023 年后的方法对照"恰是 soundness 审稿人也会挑的完备性问题，不是 novelty 问题）。被点名即 Reject，消耗掉唯一一次重投机会去补一个**早已备好 harness 的可预见项**，是最差的资源使用方式。反之，基线跑完后即便 C²GES 在 F1 上被超越（按 K 敏感性表的领先幅度判断，被零样本 LLM 超越概率偏高），Discussion 的 tradeoff 段已把叙事出口修好——加一张成本/延迟表即可，主张体系不塌。

**第三层（例外条款）**：唯一支持"无基线即投"的情形是**原工作区确认永久丢失**。届时数据无法发布、基线永远跑不了、5 类包外数字永远无凭据——那是另一个更严重的问题（benchmark 贡献句必须删除、DA 改为"available from authors on request"、接受 ~30–40% 的录取率），且更适合改投有修改回旋的 MDPI Electronics 而非二元制的 Access。只要工作区仍有找回可能，就应等待。

**推荐执行序**：等工作区 → ①数据集+工件入包/发布（1–2 天）→ ②跑 3 基线 + 成本表 + 若被超越则按预置叙事微调摘要一句（3–5 天）→ ③投稿。金标子集（3–4 天）可与审稿并行做、留作重投弹药，**不必等它**——循环性已披露且预告了验证方案，Access 审稿人更可能接受"declared future work"，而缺基线不同：harness 就在包里，"能跑而不跑"反而显得回避。

### 5(c) 硬机械阻断（当前逐项）

| # | 位置 | 内容 |
|---|---|---|
| 1 | paper.tex:20-22 | `\author{Anonymous}`、`Corresponding Author (email@example.com)`；单位行待核实；缺 ORCID 与作者简介 |
| 2 | paper.tex:581 | Data Availability `[TODO: repository URL and archival DOI, e.g., GitHub release plus Zenodo deposit]` |
| 3 | paper.tex:587 | AI 声明 `[TODO: confirm final wording against the target journal's AI-use policy at submission.]` |
| 4 | source/paper.pdf | 2026-06-27 旧版，不含两轮全部修改；本机无 LaTeX 工具链；bbl 系手工追加，需完整重编译并复查版式与引用编号 |
| 5 | （提交系统项） | Graphical abstract 未备；投稿元数据（Subject Area、Special Section 选择）未定 |

（paper.tex:15 的 `\history{...xxxx 00, 0000...}` 为模板标准占位，非阻断。）

### 5(d) 决策分布预测（完成 5(c) 机械项后投出）

| 状态 | Accept | Reject（附 resubmit 邀请） | Reject（终局倾向） |
|---|---|---|---|
| **现状投**（无基线、无金标；数据集已发布） | ~35–45% | ~45–55% | ~10% |
| **基线跑完后投**（含成本/延迟表；无论 C²GES 是否被超越，按预置 tradeoff 叙事收口） | ~55–65% | ~30–40% | ~5% |
| **基线 + 金标子集后投**（κ 与 agent 一致率可报告，循环性被定量约束） | ~65–75% | ~20–30% | ~5% |

注：Access 二元制下 "Reject+resubmit 邀请" 是常见轨道，但重投仅一次；三行之间约 20–30 pp 的差距全部由两个已备好方案的实验项贡献——这就是"等"的期望收益。

### 5(e) 行动清单

**P0（投稿硬门槛，工作区到手后合计 ≈2–3 人日）**

| # | 项 | 工作量 |
|---|---|---|
| 1 | 填作者/单位/通讯/ORCID/简介（paper.tex 头部+尾部） | 0.5 天 |
| 2 | 数据集 + Executor 五件工件入包并发布（GitHub release + Zenodo DOI），填 DA-TODO；按 MISSING_ARTIFACTS §3 路径落位 | 1–2 天 |
| 3 | AI 声明对照 IEEE 现行政策定稿，删 TODO | 0.5 小时 |
| 4 | 完整重编译（pdflatex→bibtex→pdflatex×2），复查引用重编号与版式；准备 graphical abstract | 0.5 天 |

**P1（投稿前强烈建议，≈4–6 人日）**

| # | 项 | 说明 |
|---|---|---|
| 5 | 跑 3 个 prepared baselines（CE/BGE/LLM zero-shot），入 Table 3 + 配对 bootstrap；补 Discussion 承诺的 per-query 成本/延迟/可解释性对比表；若被超越，摘要与结论按已预置的 tradeoff 叙事微调一句 | 3–5 天，harness 已 smoke-tested |
| 6 | 数学 `\_` 全量替换为 `_`（32 处，`D\_i→D_i` 等）；修 §4.2 cue 列表引号；删摘要内嵌 "Index Terms---" 行（保留 keywords 环境） | 0.5 天 |
| 7 | F-cons-1/2：删或限定 §5.3 role coverage 句；Table 4 加 CI 来源脚注（Executor seed vs supplement seed） | 1 小时 |

**P2（可与审稿并行 / 重投弹药）**

| # | 项 |
|---|---|
| 8 | 人工金标子集（50–100 题双标注 + Cohen's κ + agent 一致率），兑现 §4.4 预告 |
| 9 | SBERT 弱于 TF-IDF 的一句诊断性解释（checkpoint/域外词汇），拆掉"语义基线未调优"的质疑点 |
| 10 | 复现包端到端 smoke run 记录（工作区到手后），替换 debug/initial_smoke.md 的失败记录 |

---

## 6. 一句话总评

**这是一篇把"不新增实验所能做的一切"做满了的稿子**：109/109 数字核验全中、循环性与 post-hoc 修订自我披露到位、包内/包外证据边界划分精确诚实，RRI 从 37% 改善到 ≈31%；但它的两个决定性增量（3 个已备好 harness 的学习型基线、人工金标）与它的投稿硬门槛（数据发布、工件入包）被**同一个缺失的原工作区**阻塞——因此"赶在基线前投 IEEE Access"并不能提前投稿日期，只会把 ~20 pp 的录取率和唯一一次重投机会押在"审稿人恰好不问 2026 年为什么没有 LLM 基线"上。**等工作区、跑基线、再投**是期望值严格占优的路径；金标子集可留作与审稿并行的重投弹药。

---

*核验方法备注：本轮独立核验绕开作者自产的 derived_tables.json，直接以独立脚本比对原始 summary.json（scratchpad `verify_c2ges.py`，96 项自动 + 13 项手工）；作者脚本的 105/109 自查结果与本评审结论相互印证，4 处差异均为稿内已披露的 bootstrap seed 级 CI 端点差（≤0.0015）。*
