# Round-3 投稿前自检评审：mintou_p4 / SHIELD-MOEA

- **日期**: 2026-07-16（round-3，投稿前自检；离线模式，遵循 paper_reviews 框架）
- **稿件**: `D:\aicoding\powergrid_benchmark\mintou_p4_shield_resilience_planning\manuscript\MANUSCRIPT.md`
- **目标期刊**: MDPI Energies（Smart Grids and Microgrids section），画像 `mdpi_energies.yaml` + `mdpi_energies_accepted_profile.md`
- **证据核对源**: `papers\mintou\mintou_p4_shield_resilience_planning\evidence\`（leaderboard / significance / sensitivity_sweep / ac_validation_summary / results 全量 CSV + `src/configs/real_simbench_planning_config.json`、`real_ac_validation_config.json`）
- **前情**: round-2（2026-07-13）判定 RRI 2.22、"Reject 倾向的 Major"。其 P0 项（Related Work 撰写、30 seeds 重跑、敏感性分析、基线表修复）在本稿均已落实，本轮为增量复审。

---

## 0. Desk Screen（编辑部初筛模拟）

| 检查项 | 状态 | 备注 |
|---|---|---|
| 结构完整（IMRaD + Limitations + Conclusions） | 通过 | 9 节齐全，Limitations 单列（该刊 ~3/4 论文有，属加分） |
| 摘要含量化结果 | 通过 | 0.2740 / +5.56% / 40 of 40 / 0.708→0.625 均在摘要 |
| 图表 | 通过（待人工目检） | 4 图 300 dpi PNG 已生成于 `manuscript\figures\`；Figure 1 信息密度偏高需目检可读性 |
| 参考文献格式 | **待办** | 现为 author–year 列表，须转 MDPI 数字编号（文内已留注释） |
| 作者/单位/通讯 | **阻断项** | 全部 [TODO] |
| Funding 声明 | **阻断项** | [TODO] |
| Data Availability | 半成 | 声明文字完整，repo URL/DOI 为 [TODO] |
| Institutional Review Board / Informed Consent 模板句 | **缺失** | MDPI 模板要求（本文填 "Not applicable" 即可），当前无此两节 |
| AI 使用声明 | 缺失 | MDPI 政策要求；已发表样本 0/34 有，提醒级、非拒稿项 |
| [sibling] 引文占位 | **待办** | p3 未接收前无法给出正式引文（见 ET-1/RW-3） |
| 英语水平 | 通过 | 高于该刊平均；个别长句与修辞化表达可收敛（C-2） |

**结论**: 无实质性 desk-reject 风险，但 5 个 TODO/缺失模板节在点击提交前必须清零。

---

## 1. 七维逐条 Findings（severity 0–4 × confidence 0–1 × fixability 0–1）

### 1.1 novelty 原创性与贡献（strictness 0.85）

- **N-1 | sev 3 | conf 0.80 | fix 0.7** — 命名机制与实证价值错位。算法名与标题主打 "Scenario-Screened"，但本文自己的消融证明 screening 对front 质量贡献为 −0.48%（0/8 显著），wall-clock 反而更慢（0.0733 s vs 关闭后 0.0655 s，leaderboard CSV 证实）；其全部价值主张（65% 评估节省）依赖"每次评估昂贵（潮流在环）"这一**从未在文中演示的部署区间**。65% 是解析算术（51,200→17,920，已复核无误）而非实测收益。诚实性无可指摘，但 Interest/Overall Merit 维度上"标题卖的东西"与"证据买单的东西"重心错位。
- **N-2 | sev 1 | conf 0.75 | fix —**（正面记录）组合点声明成立：2.1–2.3 三线文献梳理到位，"in-loop worst-K screening + disjoint-seed 评估 + worst-case HV 读数"的交集在所引文献中确无先例；按该刊常态（机制组合/框架集成即可，31 篇正样本全新算法 0 篇），增量性本身不构成风险（DORA）。
- **N-3 | sev 2 | conf 0.60 | fix 0.8** — 与 p3（CARS-MODE，同为 Energies 草稿）同刊同期：两文共用 SimBench 候选管线、相同证据文件命名、相同"最强基线 NSGA-II、+5–6%、42/42 与 40/40 Holm 全胜、AC 验证层、敏感性扫参"结构模板。内容不重叠且 2.4/3.4/DA 三处已声明——合规无虞，但编辑与共同审稿人观感上有"系列切香肠"联想空间（详见 ET-1）。

### 1.2 soundness 技术正确性（strictness 1.0）

- **S-1 | sev 4 | conf 0.85 | fix 0.9** — **头条差距的归因缺一个关键对照：NSGA-II + repair。** 消融链条（CSV 复核）：NoRepair 0.25176 **<** NSGA-II 0.25953 **<** NoScenarioScreen 0.27266 ≈ SHIELD 0.27396。即：去掉 repair 后提出法反输给 NSGA-II；关掉 screening 差距不变。故 +5.56% 的头条几乎完全由 (greedy repair + GA/DE 混合变异) 相对 pymoo 约束支配 NSGA-II 的实现差异承载，其中 repair 是主项（−8.10%，8/8 显著）——而 greedy budget repair 是教科书级标准算子，且未提供给任何基线。现有实验设计**无法排除"给 NSGA-II 加同一 repair 即抹平差距"的假设**。这是全文最脆弱的一根柱子。
- **S-2 | sev 3 | conf 0.90 | fix 0.9** — GA/DE 混合变异无消融。4 个消融开关（screen/repair/resilienceObj/outage）不含 NoDE/NoGA-crossover，混合变异的组件必要性未论证——恰是 accepted_profile 点名的真实漏网点"杂交多种元启发式却无组件必要性论证"。与 S-1 叠加后，"贡献在 scenario 接口而非优化器"的核心叙事（4.1 节 Rationale）失去实验支撑。
- **S-3 | sev 2 | conf 0.80 | fix 0.6** — MOEA/D 以 penalty 配置崩溃至 0.00047（组合规模 0.004 个动作），事实上是 strawman；正文已诚实注记"constraint-domination 变体可能更好"但未做。审稿人可能要求换用约束支配 MOEA/D 或从主表移除。
- **S-4 | sev 1 | conf 0.90 | fix —**（已知薄弱点①核查：**处理充分**）NoResilienceObj 微超 +0.26%：0/8 Holm 显著、per-experiment diff −0.0035~+0.0039（与 significance CSV 逐项一致）、符号不稳定、机制解释（survivability 与 reliability 经共享动作强相关）、保留理由（决策支持）与重设计路径（去相关的元件级 N-k 指标）五要素齐全，且 Limitations 第 5 条再次收录。按 DORA 画像这是加分而非扣分项。唯一残留风险：Table 3 按均值排序使**消融行列在提出法之上、位居榜首**——数字诚实但视觉上"第一名不是提出的方法"；可加表注"与 SHIELD-MOEA 差异不显著（0/8）"以免误读。
- **S-5 | sev 1 | conf 0.85 | fix 1.0** — 敏感性 Table 5 中同一默认配置（pop40/K4/T5）出现三次，均值分别 0.2674 / 0.2658 / 0.2687（CSV 证实为三条独立种子流），正文未解释三值为何不同；细心审稿人会当作不一致来问。加一句脚注即可。
- **S-6 | sev 1 | conf 0.70 | fix 1.0** — 公式与文字一致性：R(x) 不依赖 s、S 的 0.42(1−σ) 基线、L^e 耦合项均自洽；但 3.1 未说明五目标中成本项 Σk_i x_i 与场景无关却写在 E_s(...) 内（数学上无害，表述上可澄清）。

### 1.3 experiments 实验与验证（敏感性分析为该刊近硬性要求：**已满足**）

- **E-1 | sev 3 | conf 0.75 | fix 0.7**（已知薄弱点②核查：**呈现诚实但未封口**）pop=60 失显著（p=0.104，10 seeds，sweep CSV 证实）。更深的问题是趋势方向：NSGA-II 随种群 20→40→60 为 0.2360→0.2527→0.2610（持续上升），SHIELD 为 0.2583→0.2674→0.2671（已饱和）；外推交叉点可能在 pop≈80–100。正文报告了失显著这个"点"，未讨论"优势随种群规模衰减"这条趋势线，也未用 30 seeds 补足功效或延伸到 pop=80。审稿人顺着 Table 5 两列一减即可发现。
- **E-2 | sev 2 | conf 0.90 | fix 1.0** — AC 验证只用 8 个实验中的 3 个（config 证实为 deterministic_vs_scenario / outage_contingency / der_uncertainty），正文只写 "3 experiments" 既未点名也未给选择理由；且只用 seed-0 的 compromise 方案（单种子），AC 层结论的统计地基远薄于代理层。应点名 + 说明理由 +（理想情况下）多种子重复。
- **E-3 | sev 2 | conf 0.70 | fix 0.8** — AC 层顶部并列（0.708：SHIELD、GA、NoRepair、NoResilienceObj）已诚实声明 parity；但 CSV 显示 GA 的 mean max loading 63.9% **优于** SHIELD 的 68.8%（且 GA losses 0.466 < 0.484），正文引用 SHIELD 的 68.8% 时未提这一不利细节。诚实报告的完整性要求补一句。
- **E-4 | sev 1 | conf 0.90 | fix —** — 单基准族（一个 72 候选池）已列 Limitations 第 3 条；该刊常态（约 2/3 单算例）可接受，仅作建议。
- **E-5 |（正面记录）** 30 seeds × 8 实验 × 10 方法 = 2400 行 results CSV 齐全；Holm 校正 MWU、泄漏防护（disjoint seed + unseen-stress 不重叠区间，config 证实 [1.3,1.6]/[1.4,1.9]/[0.4,0.7]）、worst-case HV 读数、一次一因子敏感性——统计规范**显著超出**该刊常态（正样本 0/29 有显著性检验）。

### 1.4 reproducibility 可复现性

- **R-1 | sev 1 | conf 0.95 | fix 1.0** — repo URL/DOI 为 TODO；声明文字本身已达标（该刊底线是声明存在即可）。
- **R-2 |（正面记录）** 本轮全量数字核对**零不符**：Table 3 全行、Table 4 全 8 行（含 Holm p 值科学计数）、Table 5 全 9 行（均值/std/参照/p 值）、摘要与 6.3/6.4/6.5 的所有派生百分比（+5.56/+5.36/+24.60/−8.10/−0.48/−0.99/+0.26/65%/0.0061/5.0%/2.1%/0.6%）、AC 数字（0.708/0.625/0.500/0.962→0.974/90.8→68.8/82.3/103.6/0.542）逐一对上 CSV。deprecated 证据链保留并在 5.3 交代，可追溯性是全文强项。

### 1.5 related_work 相关文献（★近 5 年占比是该刊显式考核项）

- **RW-1 | sev 3 | conf 0.80 | fix 0.9** — 近 5 年（2021–2026）文献约 11/33 ≈ 33%，低于该刊底线 ≥50%（已发表中位 ~70%）。方法学经典（1997–2018：Storn/Deb/Zitzler/Zhang/Jin/Dupačová/Heitsch…）压舱过重。需补 6–8 篇 2022–2026 的场景约简/嵌入式采样、鲁棒 MOEA、韧性配网规划近文（2.2 节"in-the-loop screening 基本缺位"的说法也因此更稳）。
- **RW-2 | sev 1 | conf 0.70 | fix 1.0** — 引文错误：[Qi et al., 2025] 写作 "Energies **2025, 19**(1), 210"——Energies 2025 年为 vol 18，卷/年不符（Ding 2026=19(12)、Chen 2026=19(2) 均自洽，可对照）。逐条复核 DOI 后再转数字编号。
- **RW-3 | sev 2 | conf 0.85 | fix 0.8** — [sibling] 为 TODO 占位：p3 若未先接收则无可引；需改为规范的 "companion manuscript, under review"（MDPI 允许）并在 cover letter 说明，或引 preprint。
- **RW-4 |（正面记录）** 自引为零（除 sibling）；三线综述逐条实质点评并收束到 gap 句，写法优于该刊常态。

### 1.6 clarity 价值/读者兴趣与表述（strictness 0.9）

- **C-1 | sev 3 | conf 0.70 | fix 0.8**（已知薄弱点③核查：**撑得起一半**）标题与摘要把 "Scenario-Screened" 放在第一序位，而文内证据链的实际卖点是：(i) 泄漏防护评估协议（disjoint-seed + unseen-stress），(ii) 评估经济性（65%，未兑现为实测时间），(iii) 代理层与物理层对组件价值的**分歧**（outage-aware search 在代理层 −0.99% 几乎隐形、在 AC 层是唯一被区分的组件）——Discussion 已把 (iii) 说成 "one of the paper's useful outputs"，这判断是对的，但摘要/标题/贡献列表未把重心挪过去。"省评估不提均值"的定位可以撑起一篇 Energies 论文（DORA + 诚实负结果），**前提**是标题与摘要不再暗示 screening 提升了质量；当前标题写法会诱导审稿人用"screening 提升了什么"来审，然后在 6.3 发现答案是"nothing (mean)"。
- **C-2 | sev 1 | conf 0.80 | fix 1.0** — 文学化长句密度高（"survive conditions they were never planned for" / "fail unremarkably" / "keeps the lights on"），单句常超 50 词；对 ESL 读者与 MDPI 排版不友好，建议压缩 15–20% 句长。
- **C-3 | sev 1 | conf 0.60 | fix 0.9** — Figure 1 单图承载 8 实验 × 6 方法箱线 + pooled 双读数面板，排版后（Energies 双栏或通栏）可读性存疑；必要时拆分或将 4 个实验移附录。
- **C-4 | sev 1 | conf 0.75 | fix 1.0** — 5.3 自曝句 "an earlier version ... scored hand-shaped, method-conditional ranking heuristics" 措辞过于自我指控，可能引发不必要的诚信联想；建议中性化为 "a preliminary proxy-based scoring pipeline was deprecated in full and replaced by real algorithm implementations; deprecated artifacts are retained in the public evidence trail"（事实不变，语气去戏剧化）。

### 1.7 ethics 学术诚信与合规

- **ET-1 | sev 2 | conf 0.60 | fix 0.8**（已知薄弱点④核查）p3/p4 同刊同期投稿的编辑部观感：内容确不重叠（参数自适应 vs 场景暴露自适应；经济框架 vs 韧性框架；无共享实验主张），共享候选管线在 2.4、3.4、DA 三处披露——**合规层面已是最佳实践**。剩余为纯观感风险：同一 section 的编辑与审稿人池高度重叠，两文模板级相似（结构、图表布局、叙事节奏）会被一眼识别为同产线。缓解菜单（择一）：(a) cover letter 主动声明并存投稿、附两文差异表、建议不共用审稿人；(b) 错开 4–6 周投稿；(c) p4 改投 Applied Sciences/Electronics（两刊画像均在 Paper_CCF 技能内且本文的算法-验证范式契合）。**不建议**隐瞒并存事实——MDPI 编辑部内部可见同作者在投稿件。
- **ET-2 | sev 1 | conf 0.90 | fix 1.0** — 缺 AI 使用声明与 IRB/Informed Consent 模板节（填 Not applicable）；COI 已有。
- **ET-3 |（正面记录）** 无夸张百分比、无凑引、无自引堆叠；负结果三处（NoResilienceObj、screening 均值、pop60）均如实入正文与 Limitations——诚信画像在该刊正样本之上。

---

## 2. 对抗核验（对最严重 3 条 finding 以证据 CSV 试图反驳）

### 2.1 S-1（repair 承载头条差距，缺 NSGA-II+repair 对照）— **反驳失败，finding 成立并加强**

- 反驳路径 A："pymoo NSGA-II 的约束支配在功能上等价于 repair，故对照已隐含存在。" **驳回**：约束支配只是排序规则，不可行个体仍占据种群槽位；repair 直接把个体拉回可行域，是不同机制。且 leaderboard 显示 NoRepair(0.25176) 的可行前沿均值 39.65 与 NSGA-II 的 40.0 相近，差距在前沿质量而非数量——机制差异真实存在。
- 反驳路径 B："NoScenarioScreen(0.27266) 仍大幅高于 NSGA-II(0.25953)，说明差距不只 repair。" **部分成立但不解围**：NoScenarioScreen = kernel + GA/DE + repair，恰好证明差距由 (GA/DE + repair) 承载——两者都不是标题卖点，且 GA/DE 无消融（S-2），repair 是标准算子。核心质疑"新颖组件不承载头条差距"反而被坐实。
- 反驳路径 C："NoRepair 与 'NSGA-II 无 repair' 不对称（NoRepair 还带 screening 与混合变异），不能推出 NSGA-II+repair 会追平。" **成立但改变不了结论**：正因不对称，现有数据既不能证明也不能排除追平假设——这正是必须补跑对照的理由。
- **裁定**: sev 4 / conf 0.85 维持。修复成本低（一个 repair 挂钩 pymoo 的 30×8 重跑，按现有 0.08 s/run 量级约数分钟计算量），**投稿前必须完成**；若 SHIELD 仍显著胜出则头条免疫，若不胜出则趁早改叙事（比审稿人替你发现好得多）。

### 2.2 N-1/C-1（screening 卖点依赖未测试区间）— **反驳部分成功，降为"定位问题"而非"虚假主张"**

- 反驳路径 A："65% 是算术事实。" 复核：80×16×40=51,200；80×4×40 + 8×40×16=17,920；1−17,920/51,200=65.0%。**成立**——数字无误且论文明说 wall-clock 不省（0.073 vs 0.066 s）、明说兑现条件是昂贵评估区间。无任何过度主张。
- 反驳路径 B："审稿人不会在意未演示的部署区间。" **驳回**：该刊 Interest/Overall Merit 显式计分，而标题第一词的机制在文内所有实测口径（均值 HV、worst-case HV、wall-clock）上均无收益，唯一收益是一个外推。至少一位审稿人会要求"演示或降调"。
- **裁定**: sev 3 / conf 0.80 维持，但定性为 fixable 的定位问题：两条修复路线任选——(a) 做一个小型潮流在环搜索演示（哪怕 1 实验 × 5 seeds，用 pandapower 评估代替代理，实测时间节省），把 65% 兑现成分钟数；(b) 摘要/标题降调，把泄漏防护协议与代理/物理分歧升为第一卖点。

### 2.3 E-1（pop=60 失显著 + 优势随种群衰减趋势）— **反驳部分成功，维持中等严重度**

- 反驳路径 A："n=10 功效不足，失显著是样本量假象。" 用 sweep CSV 种子值核算：pop60 SHIELD 0.26709±0.0120 vs NSGA-II 0.26098±0.0056，margin +2.3% 且符号保持；10+10 的 MWU 在此效应量下确实功效有限。**部分成立**——失显著本身不足以判优势消失。
- 反驳路径 B："三条参照均值本就随轴不同（0.2674/0.2658/0.2687），0.104 只是抽样噪声。" **驳回**：NSGA-II 随 pop 单调上升（0.2360→0.2527→0.2610）而 SHIELD 饱和（0.2583→0.2674→0.2671）是趋势信号而非单点噪声；线性外推交叉在 pop≈80–100。文中"defaults sit in a flat region"对 SHIELD 成立，但对**差距**不成立。
- **裁定**: sev 3 / conf 0.75 维持。呈现已诚实（贡献列表第 6 条、6.4、Limitations 第 5 条三处披露，超出该刊常态），残余任务是补功效（pop60 至 30 seeds）或补边界（pop80），并在 6.4 加一句趋势讨论与机理猜想（大种群稀释了 worst-K 集中带来的选择压力优势）。

---

## 3. Meta 决策

**各维风险分（0–4，strictness 加权后）与已录用基线（dim_means）对照：**

| 维度 | 本稿 | 录用基线 | 超额 |
|---|---|---|---|
| novelty | 2.6 | 2.87 | −0.27 |
| soundness | 3.0 | 2.14 | **+0.86** |
| experiments | 2.3 | 2.06 | +0.24 |
| reproducibility | 1.2 | 2.16 | −0.96 |
| related_work | 2.5 | 2.10 | +0.40 |
| clarity | 2.3 | 2.48 | −0.18 |
| ethics | 1.7 | 1.79 | −0.09 |

- **RRI 估算 ≈ 58–63**，落在已录用分布 P25–P75（中位 61.5）区间内：绝对状态已与多数已发表 Energies 论文相当。录用风险的**唯一显著超额驱动是 soundness（+0.86）**，且几乎全部来自 S-1/S-2 这两个可用一次补跑封闭的归因缺口；related_work 超额（+0.40）为纯写作成本。
- **预测决策**: **Major Revision**（最可能），若 S-1 对照补跑结果利好且 RW-1/C-1 在投稿前完成，则有真实概率直接 **Minor Revision**。Reject 概率低（该刊 reject 门槛为"严重缺陷且无原创贡献"，本文两者皆不满足）。
- **相对 round-2 的位移**: round-2 的四个 P0（相关工作、30 seeds、敏感性、基线表）已全部落地且数字核对零误差；本轮新暴露的都是"下一层"问题——归因对照、文献新鲜度、贡献定位、同刊并存观感。

## 4. 优先级修改清单

| # | 项 | 封闭的 finding | 成本 | 性质 |
|---|---|---|---|---|
| **P0-1** | 补跑 **NSGA-II + 同一 greedy repair** 基线（30 seeds × 8 实验），可顺手加 **NoHybridDE 消融**（DE 通道关闭、纯 GA 变异）；结果并入 Table 3/4 与 6.3 | S-1, S-2 | 计算分钟级 + 半天分析写作 | **投稿闸门** |
| **P0-2** | 贡献重定位：摘要与贡献列表把"泄漏防护评估协议 + 代理/物理层组件归因分歧"升为第一序位，screening 表述统一为"等质量下省 65% 评估"；理想加做 1 个潮流在环小演示把 65% 兑现为实测时间；标题可保留但摘要首句不再暗示质量增益 | N-1, C-1 | 写作半天（演示另计 1–2 天） | 高 ROI |
| **P0-3** | 文献翻新：补 6–8 篇 2022–2026（场景嵌入式采样/鲁棒 MOEA/配网韧性规划），近 5 年占比提至 ≥50%；修正 Qi et al. 卷号；[sibling] 改为规范 under-review 引法；全部 DOI 复核后转 MDPI 数字编号 | RW-1, RW-2, RW-3 | 1 天 | 该刊显式考核项 |
| **P1-4** | pop 轴补强：pop=60 补至 30 seeds（或加 pop=80 点），6.4 加"优势随种群规模趋势"讨论句与机理猜想 | E-1 | 计算分钟级 + 两句写作 | 封口审稿人必问项 |
| **P1-5** | 投稿运营包：清零全部 TODO（作者/资助/URL）；补 IRB、Informed Consent（N/A）与 AI 使用声明；AC 节点名 3 个实验并给选择理由、补 GA loading 63.9% 一句；Table 3 加"消融与提出法差异不显著"表注；Table 5 加默认点三种子流脚注；5.3 deprecated 措辞中性化；**cover letter 主动声明 p3 并存投稿、附差异表、建议规避共同审稿人**（或错开 4–6 周） | Desk Screen 全部, S-4, S-5, E-2, E-3, C-4, ET-1, ET-2 | 1 天 | 机械但必须 |
| P2-6 | （可延后至审稿轮）第二基准族（IEEE 33/123）；MOEA/D 换约束支配配置；Figure 1 可读性目检与必要拆分；长句压缩 | E-4, S-3, C-3, C-2 | 2–4 天 | 备弹药 |

**一句话结论**: 数字层面这篇稿已经"审不倒"（全量核对零误差、统计规范超出该刊常态、负结果处理堪称范本）；真正的投稿前死穴只有一个——头条 +5.56% 目前站在一个没有对照的标准算子上（S-1），补一次 NSGA-II+repair 跑完再投。
