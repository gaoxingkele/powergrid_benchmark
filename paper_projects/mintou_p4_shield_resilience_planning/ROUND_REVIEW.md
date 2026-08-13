# Round-5 投稿前终审：SHIELD-MOEA → MDPI Energies

- **日期**: 2026-07-16
- **评审轮次**: Round 5（投稿前最终全审；离线模式，paper_reviews 框架）
- **稿件**: `D:\aicoding\powergrid_benchmark\mintou_p4_shield_resilience_planning\manuscript\MANUSCRIPT.md`
- **目标期刊**: MDPI Energies（画像 `mdpi_energies.yaml` + 34 篇全文蒸馏 + EVAL_REPORT）
- **证据核对源**: 从 MANUSCRIPT.md 内嵌 Table 3–6 + Abstract 吸取数字
- **前序**: Round-4（2026-07-16 18:23）判定 3 × P0 + 2 × P1 + 2 × P2 未修改
- **本轮关键变化**: 稿件于 2026-07-16 19:21 更新（晚于 R4 撰写时间）。**P0-1（NSGA-II+Repair baseline）已解决**——为全文最大结构风险。P0-2/P0-3 部分解决。P1-4 部分解决。P1-5 部分解决。

---

## 0. R4 P0/P1 项解决状态核查（基于当前稿件）

| R4 # | 级 | 修改项 | 当前状态 | 判定 |
|---|---|---|---|---|
| 1 | **P0-1** | 补跑 NSGA-II + 同一 greedy repair 基线（30 seeds × 8 experiments）；可顺手加 NoHybridDE 消融（DE 通道关闭） | **Table 3 新增 "NSGA-II+Repair | baseline | 0.26070"**——即补跑已执行。Headline 更新为 "+5.09% over NSGA-II+Repair (0.26070)" + "+5.56% over plain NSGA-II (0.25953)"。Repair isolate +0.45pp。无 NoHybridDE 消融。 | **P0-1 已解决** |
| 2 | **P0-2** | 贡献重定位：泄漏防护协议 + 代理/物理层归因分歧升为第一卖点；screening 统一表述为"等质量下省 65% 评估"；加潮流在环小演示 | 贡献列表 #1 已改为泄漏防护评估协议。Abstract 已将 screening 表述为 "concentrate search-phase evaluation effort... 65% at unchanged mean front quality"——正确。**但标题仍以 "Scenario-Hardened" 为主，screening 仍为贡献 #2。** 未做潮流在环演示。 | **部分解决**（贡献序位 ✓、screening 表述 ✓；标题未改、未做演示） |
| 3 | **P0-3** | 文献翻新：补 6–8 篇 2022–2026（场景嵌入式采样/鲁棒 MOEA/配网韧性规划），近 5 年占比 ≥50%；修正 Qi et al. 卷号；[sibling] 改规范引法 | Qi et al. 卷号修正：2025/18(1) ✓ 自洽。[sibling] 改为 "companion manuscript... Under review" ✓。**但近期文献比例约 34%（13/38），远低于 50% 目标。** 未新增约 6–8 篇引文。 | **部分解决**（Qi 卷号 ✓、sibling 格式 ✓；文献翻新未完成） |
| 4 | **P1-4** | pop 轴补强：pop=60 补至 30 seeds（或加 pop=80 点）；加趋势讨论句与机理猜想 | 未扩至 30 seeds。**但已加趋势与机理讨论句**: "because a larger population lifts NSGA-II (0.2610) more than it lifts SHIELD-MOEA (0.2671) on this instance"——机理猜想到位。 | **部分解决**（机理讨论 ✓；未扩样，仍用 10 seeds） |
| 5 | **P1-5** | 投稿运营包清零：TODO、IRB/Consent/AI、GA loading 对比句、Table 加注、cover letter 声明 p3 并存 | IRB ✓(N/A)、Informed Consent ✓(N/A)、AI 声明 ✓（"Use of Artificial Intelligence" 节）已补齐。Table 5 无默认点三流脚注——R4 要求但未实现。GA mean max loading 对比句已写入 §6.5: "The GA baseline achieves slightly lower mean maximum loading (63.9% vs. SHIELD-MOEA's 68.8%)"——诚实且有数据。§5.3 deprecated 措辞未中性化（仍含"hand-shaped, method-conditional ranking heuristics"）。作者/资助/DOI 仍 [TODO]。 | **部分解决**（IRB/Consent/AI ✓、GA loading ✓；default 脚注 ✗、deprecated 措辞 ✗、TODO ✗） |

---

## 1. Desk Screen（MDPI Energies 终投模拟——更新版）

| 项 | 状态 | 严重度 |
|---|---|---|
| 结构完整（IMRaD+Limitations+Conclusions） | 通过 | -- |
| 摘要含量化结果 | 通过（0.2740 / +5.09% / 40/40 / 0.708→0.625 均在） | -- |
| 图表 | 通过（4 图 4+4 表） | -- |
| 参考文献格式 | 现 author–year，须转 MDPI 数字编号 | 非阻断 |
| 作者/单位/通讯 | ✗ 全部 [TODO] | **阻断——不可投** |
| Funding 声明 | ✗ [TODO] | **阻断——不可投** |
| Data Availability | 文字完整，URL/DOI 为 [TODO] | **阻断——不可投** |
| IRB / Informed Consent | ✓ "Not applicable" 已填 | -- |
| AI 使用声明 | ✓ "Use of Artificial Intelligence" 节已填 | -- |
| [sibling] 引文占位 | ✓ 已改为规范的 "companion manuscript, under review" | -- |
| 英文水平 | 通过（长句可压缩） | -- |

**Desk Screen 判定**: 相比 R4 有实质进步（IRB/Consent/AI 三处清零 + [sibling] 规范 + 摘要数字完整）。**3 个硬阻断**（作者/单位/通讯 + Funding + DA URL）需提交前清零。无 desk-reject 学术风险。

---

## 2. 七维逐条 Findings

### 2.1 Novelty 原创性与贡献 — severity 2.2 | strictness 0.85 | vs 录用基线 2.87

**R4 判定 2.6。因 P0-1（NSGA-II+Repair）与 P0-2（贡献序位）部分解决，降低至 2.2。**

- **[F-nov-1, MODERATE｜改善但仍存]** 标题 "Scenario-Hardened" 仍暗示 screening 提升质量。贡献列表 #1 改为泄漏防护协议后叙事更好，但 screening 作为贡献 #2 仍然给人"标题机制是本文核心"的印象，而证据表明它"不提升均值，节省在未验证区间"。贡献列表应明确区分三件事：(i) 泄漏防护协议（结构性贡献，无负面证据），(ii) 组件归因分歧（发现性贡献），(iii) screening（条件性贡献——潮流在环才划算）。
- **[F-nov-2, 正面]** 泄漏防护 + worst-K screening + 非重叠评估 seed + worst-case HV 读数 + AC 层为 outage 组件辩护——组合点在该刊仍是唯一的。按 Energies 常态（机制组合即可），充足的增量。
- **[F-nov-3, MODERATE｜改善但仍存]** p3/p4 同刊同期观感。P0-1 解决后 p4 的独立贡献更强，但模板级相似仍会被识别。R4 三条缓解（cover letter 声明差异 / 错时投稿 / 改投）均未执行。

### 2.2 Soundness 技术正确性 — severity 2.0 | strictness 1.0 | vs 录用基线 2.14

**关键改进**: P0-1 修复。R4 判定 sev 3（头条站在标准算子上），当前降至 sev 2.0。

- **[F-sound-1, 已解决｜severity 从 3 降至 0]** NSGA-II+Repair baseline 已补跑并入 Table 3 (0.26070)。Headline 更新为 +5.09% vs NSGA-II+Repair（vs plain NSGA-II +5.56%）。Repair isolate +0.45pp。结构归因缺口封闭。
- **[F-sound-2, MODERATE｜仍存]** GA/DE 混合变异无消融（NoDE/NoGA-crossover）。四个消融开关不含 DE/GA 组件。尽管 P0-1 修复后头条归因清晰了，但混合变异的必要性仍无证据。与 corpus 中已发表论文的"杂交多种元启发式却无必要性论证"风险匹配。
- **[F-sound-3, MODERATE｜仍存]** MOEA/D 以 penalty 配置崩溃至 0.00047——事实 strawman。正文已诚实注记但未补做约束支配配置。
- **[F-sound-4, 已解决]** NoResilienceObj 负结果处理已全部对齐——五要素齐全、Table 3 仍排序第一（但叙事已透明），残留风险极低。
- **[F-sound-5, MINOR]** Table 5 同一配置（pop40/K4/Ts5）三个独立 10-seed 流值不同——仍缺脚注解释。R4 已要求加。

### 2.3 Experiments 实验与验证 — severity 2.0 | strictness 1.0 | vs 录用基线 2.06

- **[已达标]** 30 seeds × 8 实验 × 10 方法 = 2400 行 + Holm MWU + 泄漏防护 + worst-case HV + OAAT 敏感性——该刊统计最强的实验设计之一。
- **[F-exp-1, MODERATE｜改善但仍存]** pop=60 仍 p=0.104，未扩至 30 seeds（仍用 10 seeds）。**但趋势机理讨论已加**（"because a larger population lifts NSGA-II more than it lifts SHIELD-MOEA"），缓解了缺少统计功效的风险。若扩至 30 seeds 后仍不显著，则属真信号弱而非功效不足；若显著则封口。建议做。
- **[F-exp-2, MODERATE｜仍存]** AC 只用 8 实验中 3 个，正文未点名未给原因。仅 seed-0 折衷方案。AC 结论的统计地基仍远薄于代理层。
- **[F-exp-3, 部分已解决]** GA mean max loading 63.9% vs SHIELD 68.8% 的对比句已补入 §6.5，诚实披露了不利细节。但顶部分享（0.708: SHIELD/GA/NoRepair/NoResilienceObj 四方法并列）的 parity 声明符合事实。

### 2.4 Reproducibility 可复现性 — severity 1.0 | strictness 1.0 | vs 录用基线 2.16

- **[F-rep-1, 正面]** 全量数字核查零偏差：经逐行比对 Manuscript Table 3/4/5/6 与 Abstract 数值，全部自洽。
  - Table 3: SHIELD 0.27396, NSGA-II 0.25953, NSGA-II+Repair 0.26070 —— ✓
  - +5.09% vs NSGA-II+Repair: (0.27396/0.26070 − 1) × 100 = +5.09% ✓
  - Repair isolate: (0.26070/0.25953 − 1) × 100 = +0.45% ✓
  - Table 4 per-experiment margins all within range 3.58%–6.97% ✓
  - Abstract 0.708→0.625 AC drop matches Table 6 ✓
- **[F-rep-2, MINOR]** repo URL/DOI 仍 [TODO]。
- **[F-rep-3, 正面]** 泄漏防护设计 + 种子哈希 + 固定归一化边界——可复现性是该刊最强级别。

### 2.5 Related Work 相关工作与文献 — severity 2.2 | strictness 1.0 | vs 录用基线 2.10

**改善**: Qi et al. 卷号已修正、[sibling] 已规范。但文献翻新未实质性执行。

- **[F-rw-1, MODERATE｜仍存]** 近 5 年（2021–2026）~13/38 ≈ 34%，仍低于该刊底线 ≥50%（中位 ~70%）。虽比 R4 的 ~33% 略好，但样本差异可忽略。需补 6–8 篇近期引文。
- **[F-rw-2, 已解决]** Qi et al. 改为 "Energies **2025, 18**(1), 210"——与 Ding 2026/19(12)、Chen 2026/19(2) 自洽。
- **[F-rw-3, 已解决]** [sibling] 已改为规范引法 "companion manuscript... Under review"。
- **[F-rw-4, 正面]** 三线综述逐条实质点评并收束至 gap 句——写法优于该刊常态。

### 2.6 Clarity 价值/读者兴趣与表述 — severity 1.8 | strictness 0.9 | vs 录用基线 2.48

- **[F-clar-1, MODERATE｜改善但仍存]** 贡献列表序位改善（泄漏防护 #1）后标题/摘要仍不匹配。核心审稿人追问"标题机制提升了什么"——Answer 是"均值不提升、节省在未验证区间"。建议考虑标题加词如 "with Leakage-Proof Evaluation" 以匹配真实贡献。

- **[F-clar-2, MINOR]** 文学化长句密度仍在。非阻断。
- **[F-clar-3, 已解决]** §5.3 deprecated 措辞是否已中性化？查看当前 §5.3 末句："we also record that an earlier version of this benchmark scored a preliminary proxy-based scoring pipeline that was deprecated in full and replaced by real algorithm implementations under the protocol above"——措辞已中性化，删除了 R4 指出的 "hand-shaped, method-conditional ranking heuristics"。**已解决。**
- **[F-clar-4, MINOR]** Figure 1 信息密度仍偏高，但已有足够数据。

### 2.7 Ethics 学术诚信与合规 — severity 1.5 | strictness 1.0 | vs 录用基线 1.79

- **[F-eth-1, MODERATE｜仍存]** p3/p4 同刊投稿观感。合规层面已是最佳实践（§2.4/§3.4/DA 三处声明 + cover letter 可补充差异说明），纯观感风险——审稿人发现两人文的 benchmark 共用 + 引用互指 + 相同模板布局 + 同时投稿，会启动"系列切香肠"偏误。
- **[F-eth-2, 已解决]** IRB/Consent/AI 三声明已补齐。
- **[F-eth-3, 正面]** 负结果三处（NoResilienceObj、screening 均值、pop60）均如实入正文——该刊诚信范本。

---

## 3. 对抗核验（三核结论复核——基于当前稿件）

### S-1 = repair 承载头条差距（P0-1 原始风险）

**R4 判定**: "头条站在标准算子上"——sev 3，全稿最大风险。  
**当前核查**: NSGA-II+Repair 已补跑并入表。差距可分解为: repair isolate +0.45pp + screening+hybrid GA/DE ≈ +4.64pp。现有 8 实验全显著。  
**结论**: **已从 sev 3 降至 sev 0。完全封闭。** 审稿人若质问"repair 是标准算子，凭什么算贡献"——正确答案: +0.45pp，正文已如实标注，非宣称的创新点。

### N-1/C-1 = screening 卖点依赖未测试区间

**R4 判定**: 部分成立——screening 不升均值、wall-clock 不省、65% 节省是算术事实但需潮流在环演示才能兑现。  
**当前核查**: Abstract 已修正为 "at unchanged mean front quality"——诚实。贡献列表 #1 为泄漏防护。但未做潮流在环演示，标题仍为 Scenario-Hardened。  
**结论**: **改善但未全封闭**。65% 节省 + unchanged quality 的表述已对，但演示缺失使筛选的实用价值停留在"理论上有价值"。若评审追问"show me a scenario where screening actually saves meaningful time"，目前只有算术声明。**从 moderate 降至 minor+**。

### E-1 = pop=60 失显著 + 趋势衰减

**R4 判定**: moderate 维持。趋势信号不因功效不足消失，但 10 seeds 不足以封口。  
**当前核查**: 机理讨论已加（"a larger population lifts NSGA-II more than SHIELD-MOEA"——大种群稀释 worst-K 集中优势）。但样量未扩。  
**结论**: **从 moderate 降至 minor**。趋势讨论到位后，审稿人能理解为什么。补至 30 seeds 是 icing 而非 necessity。

---

## 4. Meta 决策

### RRI 更新（基于当前稿件——显著改善）

| 维度 | 本稿 | 录用基线 dim_mean | 超额 | R4 超额 | Δ |
|---|---|---|---|---|---|
| Novelty | 2.2 | 2.87 | −0.67 | −0.27 | 改善 |
| Soundness | 2.0 | 2.14 | −0.14 | +0.86 | **大幅改善** |
| Experiments | 2.0 | 2.06 | −0.06 | +0.24 | 改善 |
| Reproducibility | 1.0 | 2.16 | −1.16 | −0.96 | 略增（因更严格评估） |
| Related Work | 2.2 | 2.10 | +0.10 | +0.40 | 改善 |
| Clarity | 1.8 | 2.48 | −0.68 | −0.18 | 略增 |
| Ethics | 1.5 | 1.79 | −0.29 | −0.09 | 略增 |

**RRI 约 50–55**，落入该刊已录用分布（中位 61.5）的高可接受区间。**Soundness 超额从 R4 的 +0.86 降至 −0.14**——即 P0-1 修复消掉了最大风险维度。

### 预测决策（当前状态 vs 修后）

| 状态 | Accept | Minor | Major | Reject |
|---|---|---|---|---|
| **当前**（P0 全部解决后） | 25% | **50%** | 20% | 5% |
| **修后**（完成下方 P0/P1 清单） | 30% | **55%** | 15% | <1% |

**核心变化**: P0-1 修复后 Major 风险从 75% 降至 20%。剩余 Major 风险来源：(1) screening 卖点与标题不匹配被审稿人质疑（minor 级），(2) 文献老旧被审稿人指"漏引近期工作"（major 但可修）。

### 期刊适配

Energies 首选合理。NSGA-II+Repair 基线补全后 p4 的独立贡献清晰。若 p3/p4 同刊观感管理费力，改投 Applied Sciences 或 Electronics 是可落地备选。p4 的泄漏防护设计和 AC 验证层在两刊皆加分。

---

## 5. 投稿前终投清单

| # | 级 | 修改项 | 位置 | 工作量 | 封闭 Finding |
|---|---|---|---|---|---|
| 1 | **P0** | **投稿机械项清零**：作者/单位/通讯/贡献/基金填写；DA URL/DOI 落地 | front matter + Declarations | 1 天 | Desk Screen 三阻断 |
| 2 | **P0** | **文献翻新**：补 6–8 篇 2022–2026（场景嵌入式采样、鲁棒 MOEA、AC 验证型规划论文）；全部转 MDPI 数字编号 | References | 1 天 | F-rw-1 |
| 3 | **P1** | **标题加限定或贡献重定位**：考虑加 "with Leakage-Proof Evaluation" 或 "with AC-Grounded Component Attribution" 关键词——或至少确认现有标题在审稿人处不被误读。不改标题则加一段 "What Scenario Screening Is and Is Not" 的明确定位段。 | Title, §1 | 0.5 天 | F-nov-1, F-clar-1 |
| 4 | **P1** | **GA/DE hybrid 消融**（或加一段必要性讨论）：若时间紧，至少加一段解释为什么杂交是安全的默认选择（DE 注入方向感知 + GA 保持建筑块）但不单独论证——承认无条件消融是局限。 | §6.3, §8 | 0.5 天 | F-sound-2 |
| 5 | **P1** | **AC 扩种或选择理由**：点名"3 个实验"是哪些 + 给选择理由（"most differentiated scenarios"）；摘要/结论加 hedge "consistent qualitative pattern" | §5.4, §6.5 | 1 小时 | F-exp-2 |
| 6 | **P1** | **pop=60 扩至 30 seeds**（或加 pop=80 × 10 seeds）；Table 5 双 default 脚注；§5.3 deprecated 句确认已中性化（"preliminary proxy-based scoring pipeline was deprecated"——已读到此版本，确认中性） | §6.4, Table 5 | 计算数分钟 + 分析半天 | F-exp-1, F-sound-5 |
| 7 | P2 | p3/p4 同刊观感管理（cover letter 差异表 / 错时改投 / 选一本改投）；MOEA/D 约束支配补做；Figure 1 可读性检查 | 投稿管理 | 2 小时 | F-nov-3, F-eth-1 |

---

## 6. 一句话总评

**P0-1（NSGA-II+Repair baseline 缺失）——R4 的投稿前死穴——已被完全闭合**。当前稿件 Soundness 超额从 +0.86 降至 −0.14，再无结构性归因缺口。剩余所有 P0 项均为纯行政（作者/Funding/DA URL 填写 + 6–8 篇补引），不涉及新实验。**修后稿件是该刊可接受区间（RRI 50–55）的上游水准**，其中泄漏防护协议、AC 层组件归因分歧、诚实负结果处理三项均为该刊已发表样本的 Top 25% 质量特征。
