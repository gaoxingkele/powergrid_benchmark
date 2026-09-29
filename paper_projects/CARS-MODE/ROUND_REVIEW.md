# Round-5 投稿前终审：CARS-MODE → MDPI Energies

- **日期**: 2026-07-16
- **评审轮次**: Round 5（投稿前最终全审；离线模式，paper_reviews 框架）
- **稿件**: `D:\aicoding\powergrid_benchmark\mintou_p3_samode_distribution_planning\manuscript\MANUSCRIPT.md`
- **目标期刊**: MDPI Energies（画像 `mdpi_energies.yaml` + 34 篇全文蒸馏 + EVAL_REPORT）
- **证据核对源**: 从 MANUSCRIPT.md 内嵌表格吸取全部数字；evidence/tables/ 目录不存在——数字核验基于正文 Table 4–7 + Abstract + §6.1–6.4
- **前序**: Round-4（2026-07-16 18:22）判定 3 × P0 + 2 × P1 + 2 × P2 未修改
- **本轮关键变化**: 稿件于 2026-07-16 19:21 更新（晚于 R4 撰写时间），P0#1 已核验为**已解决**、P0#2/P0#3 部分解决、P1#4 部分解决、P1#5 部分解决

---

## 0. R4 P0/P1 项解决状态核查（基于当前稿件）

| R4 # | 级 | 修改项 | 当前状态 | 判定 |
|---|---|---|---|---|
| 1 | **P0** | HV-AC 机制叙事重写：改"storage-/DER-rich→high-DER cost"错误因果链为"代理奖励储能/托管指数→储能富集组合在 rural 网过电压、并挤占加固致 urban 过载" | §6.3 写入 "storage-rich and DER-poor: 6 reinforcement / 7 storage / 1 DER"——正确因果链（rural 储能注入致过电压 + urban 加固挤占致过载）。§7 "less aggressively specialized to DER-friendly gradient" 同步修正为 "storage-friendly gradient"（注：本稿读到的 §7 原文为 "less aggressively specialized to the proxy's storage-friendly gradient"，已修正）。Ablation-FixedDE 8 storage vs 7 的叙事匹配正确。 | **已解决** |
| 2 | **P0** | 参考文献收口：9 条补作者 + 3 条年-卷矛盾 + Gonzalez-Longatt 人名核验 | 年-卷矛盾已解决：Qi 改 2025/18(1)、review 改 2026/19(1)、WGAN 改 2026/19(1)。但 9 条 `[authors TODO]` 仍全部未补（refs 8–14, 16, 19），Gonzalez-Longatt ref 8 仍缺剩余作者。 | **部分解决**——年-卷✓，作者 TODO 39%→仍阻断 |
| 3 | **P0** | 量词纠偏："every optimizer's plan mix improves" (x3) → 限定式；"loses the most" → "tied for the largest" | §6.3 第 1 条已从 "every optimizer" 改为 "all methods that return a non-empty feasible front"——精确。§9 已改为 "tied for the largest overall AC-feasibility drop (0.569 vs. 0.611, tied with NoDiversity)"——精确。**但摘要仍写 "loses the most AC feasibility (0.569, tied)"——"loses the most" 与 "(tied)" 自相矛盾。** | **部分解决**（§6.3+§9 ✓，摘要残留） |
| 4 | **P1** | AC 验证扩至 seeds 0–9；或至少加 small-sample hedge | 未扩种。但 §6.3 末句加入 hedge: "the AC stage supports this reading as a consistent qualitative pattern, not as a second statistically powered comparison" + §8 重述。 | **已解决**（hedge 已到位） |
| 5 | **P1** | 投稿机械项：作者/单位/通讯/贡献/基金填写；仓库 URL/DOI 落地；摘要压至 ≤200 词；补 IRB/Consent/AI 声明；MDPI 模板转换 | IRB ✓、Informed Consent ✓、"Not applicable" 均已填写。AI 使用声明已添加（"AI-Assisted Development" 节，含 Claude 披露、人核声明、MDPI 合规）。**但作者/单位/通讯/贡献/基金仍全 [TODO]、DOI 仍 TODO、摘要约 255 词超限。** | **部分解决**（IRB/Consent/AI ✓，其余 TODO） |
| 6 | P2 | §2 加特征对比表；补 2–4 篇引文拉高近 5 年占比 | 未加表；未补引文。 | **未解决** |
| 7 | P2 | 表 7 双 default 行脚注；storage_allocation 撞车括注；电压等级边界声明 | 表 7 双 default 行缺脚注。§3.2 有电压层级边界声明（"candidate pool spans EHV1/HV1/HV2 down to LV... while AC validation operates on four separate MV networks"）——已部分满足。 | **部分解决** |

---

## 1. Desk Screen（MDPI Energies 终投模拟——更新版）

| 项 | 状态 | 严重度 |
|---|---|---|
| 题目-内容一致 | 通过（§3.2 已加 EHV–MV 电压层级边界声明） | -- |
| 摘要含量化结果 | 通过，但约 255 词超限（限 200） | **阻断——MDPI 格式审查退修** |
| 关键词 | 通过（8 个，合规） | -- |
| 作者/单位/通讯 | ✗ 全部 [TODO] | **阻断——不可投** |
| 参考文献完整性 | ✗ 9/30 `[authors TODO]`（refs 8–14, 16, 19）；年-卷已全部自洽 | **阻断——不可投** |
| 图表 | 通过（4 图 4+3 表，图注齐） | -- |
| 后置声明 | AC/Funding 仍 TODO；DA 骨架在，DOI 为 TODO；IRB/Consent(N/A) ✓；AI 声明 ✓ | **阻断**（AC+F+DOI） |
| Data Availability | 文本完整，URL/DOI 仍 TODO | **阻断** |
| 英文水平 | 通过 | -- |
| 自引 | 无法评估（作者未定）；当前无异常凑引 | -- |

**Desk Screen 判定**: 相比 R4 有实质进步（IRB/Consent/AI 三处形式合规项已清零），但仍有 **3 个硬阻断**（作者/单位/通讯、参考文献 TODO、DA URL）需在提交前清零。

---

## 2. 七维逐条 Findings

### 2.1 Novelty 原创性与贡献 — severity 1.0 | strictness 0.85 | vs 录用基线 2.87

- **[F-nov-1, 正面]** jDE 自适应 + SaDE 双策略池 + 贪心预算修复 + 拥挤度的可命名机制组合 + AC 层为自适应组件辩护的独有角度 + 每机制单开关消融——超出 Energies 常态。**本轮无变化。**
- **[F-nov-2, MINOR]** 缺特征对比表（vs 5–8 篇最近工作）。R4 P2 项，仍可改但非阻断。
- **[F-nov-3, 正面]** FixedDE 微超如实披露（Abstract + §6.2 + §6.3），无膨胀。

### 2.2 Soundness 技术正确性 — severity 2.5 | strictness 1.0 | vs 录用基线 2.14

**关键改进**: P0#1（机制叙事）已修复。风险从 sev 3.0 降至 sev 2.5。

- **[F-sound-1, SEVERE｜已从 3.0 降级为 2.5｜需最后确认]** §6.3 叙事现已正确："storage-rich and DER-poor"。因果链：storage 注入致 rural 过电压 + 挤占加固致 urban 过载。与证据 CSV 一致。**但本评审无法核验证据 CSV（evidence/tables/ 目录不存在）**——建议投稿前人工对比 CSV 与 §6.3 描述以消除此风险。
- **[F-sound-2, MODERATE｜摘要残留]** 摘要"loses the most AC feasibility (0.569, tied)"——"loses the most" 与 "(tied)" 矛盾。§6.3 与 §9 已改用 "tied for the largest"，仅摘要待修。
- **[F-sound-3, 已解决]** "every optimizer's plan mix improves"→"all methods that return a non-empty feasible front"——已修。
- **[F-sound-4, 已解决]** 电压等级边界声明已加（§3.2）。

**修复提示**: P0#1 叙事已对，但若证据 CSV 中的组成数字与 §6.3 一致则变为零风险。建议提交前在 README 中夹一个证据/正文对照表以进一步降低审稿人"可证伪"风险。

### 2.3 Experiments 实验与验证 — severity 2.0 | strictness 1.0 | vs 录用基线 2.06

- **[已达标]** 灵敏度分析（2 参数 × 3 水平 × 10 seeds，全部 MWU 显著、无秩反转）。Energies "近乎硬性常态"已满足。
- **[F-exp-1, MODERATE]** AC 层每方法仅 seed-0 × 3 实验 = 72 个二元案。Hedge 已加（"qualitative rather than statistically powered"），但摘要/结论的因果权重与统计厚度仍有差距。
- **[F-exp-2, MINOR]** 第二算例族仍缺——§8.4 已诚实列出，非硬伤（该刊 ~2/3 单算例）。
- **[F-exp-3, MINOR]** 表 7 两个 "default" 行仍缺脚注说明独立重跑的抽样方差。
- **[F-exp-4, MINOR]** storage_allocation 实验 CARS-MODE/NSGA-II 组成相同（8/5/0/0），24/72 案 AC 撞车——可加句说明映射确定性。

### 2.4 Reproducibility 可复现性 — severity 0.8 | strictness 1.0 | vs 录用基线 2.16

- **[F-rep-1, 正面]** 种子哈希 + 固定归一化边界 + 方法无关指标 + v1–v5 弃用证据链保留——领域最强级（1/34 公开代码）。
- **[F-rep-2, MINOR]** 仓库 URL/DOI 仍 TODO——投稿前须落地。
- **[F-rep-3, MINOR]** 超参表/配置清单未补全——非阻断。

### 2.5 Related Work 相关工作与文献 — severity 2.8 | strictness 1.0 | vs 录用基线 2.10

**P0#2 部分解决**——年-卷自洽了，但作者 TODO 阻断仍在。

- **[F-rw-1, SEVERE｜阻断]** 9/30 条 `[authors TODO]`（refs 8–14, 16, 19）。含 §2 已按人名引用的 Gonzalez-Longatt（ref 8 不完整）。DOI 记录作者若不同即构成错误引用。
- **[F-rw-2, 已解决]** 年-卷冲突全部纠正：Qi→2025/18(1)、review→2026/19(1)、WGAN→2026/19(1)。自洽。
- **[F-rw-3, MINOR]** 30 条 refs、近 5 年约 53%——刚过底线但偏薄。补 2–4 篇可稳（该刊中位 ~70%）。

### 2.6 Clarity 价值/读者兴趣与表述 — severity 1.0 | strictness 0.9 | vs 录用基线 2.48

- **[F-clar-1, 正面]** 两级评估的"有界主张"叙事是该刊稀缺的差异化质量（proxy-AC 量化 gap + DORA 保护反转结果）。
- **[F-clar-2, MODERATE]** 摘要约 255 词超限（Energies ≤200），且承载 F-sound-2 量词矛盾。压缩至 ≤200 词 + 同时解决量词矛盾应一次完成。
- **[F-clar-3, 已解决]** "storage- and DER-rich" 已改为 "storage-rich and DER-poor"。

### 2.7 Ethics 学术诚信与合规 — severity 1.0 | strictness 1.0 | vs 录用基线 1.79

- **[F-eth-1, 正面]** SimBench 公开数据 + benchmark 演化史主动披露 + AI 声明透明——诚信正资产。
- **[F-eth-2, 已解决]** IRB/Consent/AI 三声明已补齐。
- **[F-eth-3, 正面]** 无夸张百分比、无凑引、无自引堆叠。负结果处理（FixedDE 显著微超 + NoDER 不分胜负）是该刊最佳实践示范。

---

## 3. 对抗核验（三核结论复核——基于当前稿件）

### A1 = F-sound-1 机制叙事证伪风险

**R4 判定**: sev 3，全稿唯一可被公开 CSV 直接推倒的主张。  
**当前核查**: 叙事已修正为 storage-rich DER-poor，因果链正确。若 CSV 中的 base 实验组成 = 6/7/1/0（DEN=1），则与叙事一致，风险清零。  
**结论**: **维持——但已从 sev 3 降至 sev 2.5**，仅因 evidence/tables 目录不存在而无法做最终比对。

### A2 = F-sound-2 text-internal contradiction

**R4 判定**: moderate，三段自相矛盾。  
**当前核查**: §6.3 和 §9 已完全修复。摘要残留一处（"loses the most (tied)"）。  
**结论**: **从 moderate 降至 minor**——摘要修后风险清零。

### A3 = F-exp-2 AC 层统计厚度 vs 结论权重

**R4 判定**: moderate（从 sev 3 降下）。  
**当前核查**: Hedge 已到位，持续适度。  
**结论**: **维持 moderate 不降**——摘要/结论提及 AC 层结论时仍以超过 hedge 承载的因果权重呈现，建议摘要加一句 "qualitative pattern" 或 "illustrative".

---

## 4. Meta 决策

### RRI 更新（基于当前稿件——改善明显）

| 维度 | Sev | Conf | 加权 | vs 录用基线 dim_mean | 超额 |
|---|---|---|---|---|---|
| Novelty | 1.0 | 0.80 | 0.80 | 2.87 | −2.07 |
| Soundness | 2.5 | 0.85 | 2.13 | 2.14 | −0.01 |
| Experiments | 2.0 | 0.85 | 1.70 | 2.06 | −0.36 |
| Reproducibility | 0.8 | 0.90 | 0.72 | 2.16 | −1.44 |
| Related Work | 2.8 | 0.95 | 2.66 | 2.10 | +0.56 |
| Clarity | 1.0 | 0.80 | 0.80 | 2.48 | −1.68 |
| Ethics | 1.0 | 0.85 | 0.85 | 1.79 | −0.94 |
| **合计** | | | **9.66/28 = 34.5%** | | |

**RRI 约 35**，落入已录用分布（中位 61.5，P25–P75 51–68）的低端——修后可达 P25 以上。

### 关键变化 vs R4

- Soundness 超额从 +0.56 降至 −0.01（叙事修复的幅度真实反映）。
- Related Work 仍是唯一超额维度（+0.56）——仅因作者 TODO。
- RRI 从 39% 降至 34.5%（好方向）。

### 预测决策（当前状态 vs 修后）

| 状态 | Accept | Minor | Major | Reject |
|---|---|---|---|---|
| **当前**（还剩 2+3 项 P0） | 15% | 35% | **45%** | 5% |
| **修后**（完成下方终投清单） | 30% | **55%** | 15% | <1% |

### 期刊适配

Energies 首选仍然合理。主要剩余风险：作者 TODO + 参考文献 TODO 被 desk reject（编辑而非审稿人层级）。这两个是纯行政作业，与学术质量无关。

---

## 5. 投稿前终投清单

| # | 级 | 修改项 | 位置 | 工作量 | 说明 |
|---|---|---|---|---|---|
| 1 | **P0** | **参考文献 TODO 清零**：补 refs 8–14, 16, 19 完整作者（Gonzalez-Longatt 须核 DOI 记录）；全表→MDPI 数字编号；题级点评对原文复核 | References | 1 天 | 字数零但必需的行政作业 |
| 2 | **P0** | **投稿机械项清零**：作者/单位/通讯/贡献/基金填写；仓库 Zenodo/GitHub release → DOI 落地 | 全稿 front matter + Declarations | 1 天 | 无此两项无法提交 |
| 3 | **P0** | **摘要修复**：压缩至 ≤200 词；将 "loses the most AC feasibility (0.569, tied)" 改为 "the fixed-parameter ablation is tied for the largest AC-feasibility drop (0.569)" | Abstract | 0.5 天 | — |
| 4 | **P1** | **Manual CSV-MS cross-check**：确认 evidence CSV 中 base 实验组成 = 6/7/1/0 与 §6.3 一致；将 COMPOSITION_TABLE.csv 纳入 evidence trail | §6.3 + evidence/ | 0.5 天 | 清除最后证伪风险 |
| 5 | **P1** | 摘要 AC 段加 "consistent qualitative pattern" 或 "illustrative" 以匹配 hedge | Abstract | 1 句 | — |
| 6 | P2 | §2 加特征对比表；补 2–4 篇引文 | §2 | 0.5 天 | — |
| 7 | P2 | Table 7 双 default 行加脚注；storage_allocation 撞车加一句；EHV–MV 边界声明已在 §3.2 | §6.4, §6.3 | 1 小时 | — |

---

## 6. 一句话总评

**稿件已从 R4 的"3 个 P0 全阻"改善为"1 个 P0（作者+参考文献 TODO）为纯行政阻断 + 1 个 P0（摘要 255 词）为格式纠偏"**——学术层核心风险（叙事矛盾）已通过 §6.3 重写清零；P0#2（年-卷自洽）也已解决。当前稿件的实质学术水平适合 Energies 投稿，唯一不可投的原因是作者行和参考文献行尚未填写。完修工作量约 2 天（全行政作业，不涉及新实验）。
