# Round-5 投稿前全审: TRACE-MOEA → Energies (Final Pre-Submission)

**论文 ID:** mintou_p5 (TRACE-MOEA)
**目标期刊:** MDPI Energies
**评审日期:** 2026-07-16
**评审依据:** 
- 画像校准: mdpi_energies.yaml + Energies Batch A (17篇) + B (17篇) 蒸馏样本
- 证据文件: `evidence/tables/real_project_review_leaderboard.csv` (3150 runs)
- 证据文件: `evidence/tables/real_project_review_significance.csv` (99 comparisons)
- 证据文件: `evidence/tables/real_nerc_rule_backtest.csv` (32 rows)
- 证据文件: `evidence/tables/real_mtep_backtest.csv` (32 rows)
- 新证据: Manuscript Section 6.4 预算敏感性 0.75x 扫描 (TRACE-MOEA 0.16606 vs NSGA-II 0.16378, +1.4%)
- 前次审稿: `ROUND_REVIEW.md` (Round-4); P1.1 敏感性分析部分解决

---

## 一、Desk Screen (形式审查)

| 项目 | 状态 | 备注 |
|---|---|---|
| [TODO] 标记 | **未完成** | Author Contributions, Funding, Data Availability (repository URL), 参考文献[28] companion 引用均为 [TODO] — 投稿前必须全部替换 |
| 声明五件套 | **不完整** | Author Contributions 为模板占位；Funding 为 [TODO]；AI use disclosure 缺失（MDPI 2025 起鼓励披露，见 mdpi.com/ethics） |
| Data Availability | **可接受模板** | 已给出所有公开源 URL（RTS-GMLC, SimBench, NERC, MISO），承诺释放仓库链接 + deprecated 版本透明保留 |
| Competing Interests | **通过** | "The authors declare no conflicts of interest" — 注意需根据实际作者单位判断是否需电网员工声明 |
| 参考文献格式 | MDPI 编号制 | 1–27 号 + 29–33 号有 DOI 格式大致正确；ref [28]（sibling）未填充；ref 数量 33 篇（含 placeholder），与已发表 Energies 中位 ~35 一致 |
| 近 5 年占比 | 粗估约 70–75% | 可接受 |
| 过度自引 | **无预警** | 仅 ref [11] Gao et al. 2023 涉及 Energies，无自引堆叠 |
| AI 使用声明 | **缺失** | MDPI 已要求披露 AI 辅助，Manuscript 末尾 Checklist 已提示但全文未置入声明 |
| 摘要长度 | ~250 词 | 在 MDPI Energies 200–250 词范围内，建议精炼至 220 词以内 |
| 图表占位 | **需处理** | Figure 1–3 引用 placeholder（`figures/fig_hv_boxplot.png` 等），需确认实际图片已生成且符合 300 dpi |

**Desk 结论:** 可通过初审，但[TODO]和 AI 声明必须在投稿前处理。参考文献数量和结构符合期刊基线。与 Round-4 相比无实质改进（TODO 项未填充）。

---

## 二、七维评审（机密，仅对作者公开）

### 2.1 Novelty — 原创性与贡献 (weight: 1.3, strictness: 0.85)

**评分: 7/10** (不变 vs Round-4)

TRACE-MOEA 的贡献结构为**机制组合/框架集成**（与已发表 Energies 论文的主流一致）。三个创新组件——preference-adaptive ranking layer, deterministic budget repair, quarantined decision trace archive——各自都不是全新发明，但**将三者整合到约束二进制组合优化上下文、并以电网审查可追溯性为设计目标**，构成清晰的定位空白。

加分项：
- 决策痕迹档案的设计理念（将可解释性嵌入搜索而非事后解释）有学术价值，在 MOEA+电网审查交叉领域确属首次
- 与 companion paper BiLo-NSGA 的差异化定位明确（selection/archiving vs. variation stage）

减分项：
- Preference-adaptive layer 的独立贡献被消融实验诚实揭示为极小（+0.17% pooled, 仅 1/7 场景显著）—— 这弱化了以该组件命名算法的合理性
- Budget repair operator（按 benefit-cost ratio 丢弃）本身是已知贪心策略的标准化应用
- **命名与证据的不对称仍未处理**（Round-4 P1.3 未实施）

**与已录用 Energies 基准对比:** 正样本 novelty 维度风险均值 2.87/4。本论文落在已发表论文的创新分布范围之内。

### 2.2 Soundness — 技术正确性 (weight: 1.4, strictness: 1.0)

**评分: 8/10** (不变 vs Round-4)

总体技术扎实，方法描述清晰可复现。
- 算法设计合理：标准 NSGA-II kernel + 三个 switchable 组件，每组件有独立消融开关
- 统计协议规范：30 seeds, Mann-Whitney U + Holm 校正, fixed method-independent normalization
- Benchmark 构建透明：120 candidates 从三个公数据源确定性推导

新发现：**预算敏感性扫描（0.75x）增加了 soundness 支撑证据**。+1.4% margin at tighter budget 与 repair mechanism 的预期行为一致（constraint binds harder → repair gap widens）。此证据链强化了 "repair operator 在 tight budget 下最有价值" 的机制论证。

需注意的问题：
- **0.75x 预算扫描的结果存于 manuscript 正文但未在 evidence CSV 文件中独立发布**。当前 evidence/tables 目录下无 `budget_sensitivity_075x.csv` 或类似文件。虽然 manuscript Section 6.4 声明了 "30 seeds, the full 15-method card, 120-candidate pool"，但仅有 TRACE-MOEA 和 NSGA-II 的 HV 数值被报告。建议在证据包中补充此扫描的完整 leaderboard。
- Budget repair 的确定性设计在混合整数背景下产生单一修复路径，降低种群多样性但未评估其代价
- Hyperparameter sensitivity scan 仍旧缺失（K=8, update cadence=5 未系统扫描）

### 2.3 Experiments — 实验与验证 (weight: 1.3, strictness: 1.0)

**评分: 7.5 → 7.8/10** (微升，因 0.75x 预算扫描部分弥补了敏感性缺口)

**核心发现：预算敏感性扫描部分解决了 Round-4 的 P1.1，但仍有缺口。**

正面：
- **新增的 0.75x 预算敏感性扫描 (Section 6.4)** 是正向信号。结果 (TRACE-MOEA +1.4% vs +0.89% at 1.0x) 符合 repair mechanism 在 tight budget 下价值更大的理论预期，增强了机制论证的可信度
- 7 个场景覆盖了 budget 水平、pool 子集和权重 emphasis
- Ablation 矩阵全面（8 个 ablation 覆盖组件、目标可见性、pool size 三个层面）
- External validity ladder（NERC rule + MISO MTEP16）仍是显著加分项

缺口（未解决）：
- **仍无双独立 benchmark pool**（Limitations 第 5 条自承）
- **仍无第二 pool 验证**（如 NREL-118 或 TAMU）
- **仍无 load-flow 验证**（Limitations 第 5 条自承）
- **仍无偏好层超参扫描**（K=8, update cadence=5 未系统扫描——Limitations 第 6 条自承）
- **0.75x 预算扫描的完整证据未发布到 evidence 目录**

Energies 常态中敏感性分析近乎强制（11/15 Batch B），本论文的单一 budget sensitivity 扫描是**部分满足但不是完全满足**。

### 2.4 Reproducibility — 可复现性 (weight: 1.1)

**评分: 9/10** (不变 vs Round-4)

最强的维度。承诺释放 3150 条 run records、significance tables、figure scripts、deprecated revision。

需补充：
- 确保 0.75x 预算扫描的完整运行结果加入 evidence 发布
- 确保计算环境（Python 版本、pymoo 版本、硬件规格）透明

### 2.5 Related Work — 相关工作与文献 (weight: 0.9)

**评分: 7/10** (不变 vs Round-4)

三条线覆盖必要范围。Section 2.4 Differentiation from companion 必要且清晰。但与 Round-4 一样，ref [28]（companion 引用）仍为 [TODO]。

### 2.6 Clarity — 价值/读者兴趣与表述 (weight: 1.0, strictness: 0.9)

**评分: 8/10** (不变 vs Round-4)

写作质量高：结构清晰、述评克制、外推谨慎。Claim 校准在 34 篇已发表样本中可排前 20%。Limitations 节 6 条全面诚实。

加分：新增的 0.75x 预算敏感性叙述 ("margin grows at tighter budget") 与限制自查 ("single-budget check is a minimum step") 同时存在，保持了之前的高克制度。

减分：摘要约 250 词可压缩；self-praising 形容词（"reproducible" "statistically disciplined" "honest"）稍有不适。

### 2.7 Ethics — 学术诚信与合规 (weight: 0.6)

**评分: 9/10** (不变 vs Round-4)

废弃版本透明保留为学术诚实典范。[TODO] AI 使用声明仍旧缺失——投稿前可解决。

---

## 三、Adversarial Review（证据盘问）

### Claim 1: "TRACE-MOEA attains pooled mean HV 0.17425, +0.89% above NSGA-II (0.17270)"

**证据:** `real_project_review_leaderboard.csv:2` — TRACE-MOEA 0.17424740 vs NSGA-II 0.17270385, rel diff = +0.8936%.

**验证通过.** 数值精确匹配。(0.17424740-0.17270385)/0.17270385 = 0.8936%.

### Claim 2: "38 of 42 Holm-corrected baseline wins and no significant baseline loss"

**证据:** `real_project_review_significance.csv` — 6 baselines x 7 scenarios = 42. 统计显著数:
- benchmark: 5/6 (vs NSGA-II p_holm=0.064, n.s.)
- budget_ranking: 5/6 (vs NSGA-II p_holm=0.053, n.s.)
- distribution: 5/6 (vs NSGA-II p_holm=1.0, n.s.)
- preference: 6/6
- reliability: 5/6 (vs NSGA-II p_holm=0.242, n.s.)
- renewable: 6/6
- traceability: 6/6
Total = 38. 无 baseline significant losses.

**验证通过.** 注意 distribution_project_review 中 TRACE-MOEA vs NSGA-II 名义上为负 (-0.13%, p_holm=1.0) —— manuscript 已如实报告。

### Claim 3: "the archive covers 98.6% of the projects in the returned front"

**证据:** `real_project_review_leaderboard.csv:2` — mean_decision_coverage = 0.98568820.

**验证通过.** 0.9857 ≈ 98.6%.

### Claim 4: "NERC rule backtest priority capture 1.34–1.55"

**证据:** `real_nerc_rule_backtest.csv:7` — benchmark 1.550030; `:23` — reliability 1.338031.

**验证通过.** 区间 [1.338, 1.550] 与 [1.34, 1.55] 匹配。

### Claim 5: "MISO MTEP16 outcome backtest: broad capture 1.070–1.079, r=0.151–0.169, p<=10^-6"

**证据:** `real_mtep_backtest.csv:4` — benchmark: capture_broad=1.079479, r_broad=0.168851, p_broad=0.000000.
`:22` — reliability: capture_broad=1.069633, r_broad=0.151092, p_broad=0.000001.

**验证通过.** 精确匹配。注意 round 表述 (1.070 != 1.069633) 在合理舍入范围内。

### Claim 6: "AHP-TOPSIS attains comparable or higher broad capture on both rungs"

**证据 (NERC):** `real_nerc_rule_backtest.csv:2` — AHP-TOPSIS benchmark 2.291668 (远高于 1.55). `:17` — reliability 1.628495 (高于 1.338).

**证据 (MTEP):** `real_mtep_backtest.csv:2` — AHP-TOPSIS benchmark capture_broad=1.100247 (高于 1.0795). `:20` — reliability 1.072263 (略高于 1.0696).

**验证通过.** 数据完全支持。

### Claim 7: "Preference-adaptive layer's isolated contribution is small (+0.17% pooled)"

**证据:** `real_project_review_leaderboard.csv:2` vs `:4` — TRACE-MOEA 0.174247 vs Ablation-NoPreferenceRanking 0.173956, rel diff = +0.167%.

**验证通过.** 精确匹配。

### Claim 8: "Removing risk objective significantly improves the method in traceability scenario"

**证据:** `real_project_review_significance.csv:92` — TRACE-MOEA vs Ablation-NoScheduleRisk in traceability: diff = -0.000585, p_holm = 0.0219, significant = True.

**验证通过.** Manuscript 的 honest negative result 处理得当。

### NEW Claim 9: "Budget sensitivity at 0.75x: TRACE-MOEA +1.4% (0.16606 vs NSGA-II 0.16378), margin GROWS at tighter budget"

**证据:** Manuscript Section 6.4 claims TRACE-MOEA 0.16606 vs NSGA-II 0.16378 at 0.75x budget, +1.4%.

**状态: 需部分确认（无独立证据文件）.** 此结果在 Manuscript 正文中作为叙述性报告出现，但 evidence/tables 目录下无对应的 budget sensitivity 证据 CSV 文件。与 Round-4 时的 7 个标准场景不同，0.75x 扫描的结果未作为结构化数据发布。虽然 manuscript 写明了具体数值 (0.16606, 0.16378) 和配置 (30 seeds, 15 methods, 120 candidates)，但无法像其他 claims 一样逐行验证。

**建议:** 在证据包中补充 `real_budget_sensitivity_075x.csv` 或类似文件，列出完整 leaderboard + significance 比较。

间接验证: "margin grows" 叙述与 Table 5 中的 budget_ranking_stability (0.88x, +1.09%) 一致——更紧的 budget 产生更大的 margin (0.75x → +1.4% > 0.88x → +1.09%)，模式合理。但此模式的完整证据（如 0.88x、1.0x、0.75x 三水平对比表）尚未以可复现形式发布。

---

## 四、Meta Review

### 相对于 Round-4 的变化

| 项目 | Round-4 状态 | Round-5 状态 | 变化 |
|---|---|---|---|
| P1.1 敏感性分析 | 缺失 | **部分解决**（0.75x budget scan added） | 部分正向 |
| P1.2 第二 pool | 缺失 | 仍缺失 | 未解决 |
| P1.3 命名不对称 | 未处理 | 未处理 | 未解决 |
| P1.4 load-flow 验证 | 缺失 | 仍缺失 | 未解决 |
| AI 声明 | 缺失 | 仍缺失 | 未解决 |
| [TODO] 标记 | 未填充 | 仍为 [TODO] | 未解决 |
| 证据完整性 | 完整 | 0.75x 结果缺证据文件 | 新增缺口 |

### 评分汇总

| 维度 | 分数 (0-10) | 权重 | 加权 | 较 Round-4 |
|---|---|---|---|---|
| Novelty | 7.0 | 1.3 | 9.1 | 不变 |
| Soundness | 8.0 | 1.4 | 11.2 | 不变（0.75x scan 增加机制证据但不做分数调整） |
| Experiments | 7.8 | 1.3 | 10.14 | +0.3（0.75x scan 部分弥补敏感性缺口） |
| Reproducibility | 9.0 | 1.1 | 9.9 | 不变（但 0.75x 缺少证据文件是逆向信号） |
| Related Work | 7.0 | 0.9 | 6.3 | 不变 |
| Clarity | 8.0 | 1.0 | 8.0 | 不变 |
| Ethics | 9.0 | 0.6 | 5.4 | 不变 |
| **总计** | | | **60.04 / 76** | +0.39 vs Round-4 59.65 |

### RRI (Review Risk Index)

**RRI = 61 / 100** (vs Round-4: 62 — 微小改善)

已发表 Energies 正样本: median=61.5, p25=51, p75=68, range [14,76]. 本论文 RRI 61 仍落在 median 附近。0.75x budget scan 的加入降低了敏感性缺口风险系数约 1–2 点，但未触及其他 P1 项（第二 pool、命名不对称、AI 声明）。

### 推荐决定: Major Revision (不变)

MDPI tiered 决策模型下大修是常态。原创贡献、统计严谨性和外部验证足以支持录用，但单一 benchmark + 不完整敏感性分析 + 命名不对称 + AI 声明缺失叠加后仍需要一轮大修级回复。0.75x 扫描使情况略有改善但不改变整体评级。

---

## 五、修改清单 (P0/P1/P2) — 相对于 Round-4 的更新

### P0 — 投稿前阻塞项（必须完成才能提交）

- [P0.1] **替换所有 [TODO] 标记**：Author Contributions（填入实际姓名角色）、Funding（填写资助号或无外部资助）、Data Availability（填充仓库 URL/DOI）、ref [28]（插入 companion paper 完整引用）
- [P0.2] **添加 AI/LLM 使用声明**（MDPI 鼓励披露格式；参见 BiLo-NSGA manuscript 的 Generative AI Statement 为例）
- [P0.3] 生成 300 dpi 实际 PNG 图片替换 `figures/fig_*.png` 占位；确认 Figure 1-3 在 MDPI 模板下可读
- [P0.4] 运行 iThenticate/CrossCheck 自检，确认与 BiLo-NSGA manuscript 无重叠句子
- [P0.5] **新于 Round-4：将 0.75x 预算扫描的完整运行结果发布到 evidence 目录**（作为 `real_budget_sensitivity_075x.csv`），确保与 3150 条 run records 一同释放

### P1 — 大修级修改（审稿人几乎必然要求）

- [P1.1] **敏感性分析（部分已解决，仍需扩展）**: 0.75x 预算扫描已新增，但 (a) 偏好层超参 K 和 update cadence 的 2–3 水平扫描 (b) objective weight 扰动下的 rank stability (c) pool size scaling（90/150 等扩展）仍未做。Limitations 第 6 条仍自承缺失。建议至少补充 (a) 的一个双水平扫描（如 K=4/16, cadence=3/10）
- [P1.2] **补充第二独立 benchmark pool**（from NREL-118 / TAMU synthetic / IEEE 300-bus): 仍是最大单一风险点。2–3 场景 main comparison 即可大幅降低风险
- [P1.3] **处理算法命名与 evidence 的不对称**: Preference-adaptive layer 贡献极小 (+0.17%), 0.75x scan 的结果并未改变此归因。建议弱化命名中的 "Preference-Adaptive" 或在前言/结论中明确其辅助角色
- [P1.4] **补充 load-flow 验证**: 至少对 TRACE-MOEA 输出的折中方案的 1–2 个做 pandapower AC power flow check

### P2 — 小修级修改（建议但非阻塞）

- [P2.1] 摘要压缩至 220 词以内
- [P2.2] 在 Introduction 或 Conclusion 中增加 "practical implications for utilities" 段落
- [P2.3] 检查全文对 companion paper 的引用一致性（"BiLo-NSGA [sibling]" vs "companion study"）
- [P2.4] 补充 ORCID 标识符（MDPI 版面要求）
- [P2.5] 确认 MDPI 模板格式（LaTeX/Word）正确应用
- [P2.6] 在 Limitations 或 Discussion 中增加一段关于 "废弃版本保留" 可能对读者造成的困惑的说明
- [P2.7] **新于 Round-4：将 0.75x 扫描的 margin pattern（0.75x > 0.88x > 1.0x）以紧凑表纳入 Section 6.4**

---

## 六、Round-4 审查项追踪矩阵

| 原 Round-4 项 | 状态 | 说明 |
|---|---|---|
| P0.1 [TODO] 标记 | **未解决** | 仍为 [TODO] |
| P0.2 AI 声明 | **未解决** | 缺失 |
| P0.3 图片占位 | **未解决** | 仍为 placeholder |
| P0.4 iThenticate | **未解决** | 未确认执行 |
| P1.1 敏感性分析 | **部分解决** | 0.75x budget scan 新增；其他维度未做 |
| P1.2 第二 pool | **未解决** | 完全未做 |
| P1.3 命名不对称 | **未解决** | 未处理 |
| P1.4 load-flow 验证 | **未解决** | 完全未做 |
| P2.1 摘要压缩 | **未解决** | 约 250 词未变 |
| P2.2 实践段落 | **未解决** | Discussion 已有但 Introduction 缺 |
| P2.3 引用一致性 | **未解决** | "sibling" vs "companion" 混用 |
| P2.4 ORCID | **未解决** | 未添加 |
| P2.5 模板格式 | **未解决** | 未确认 |
| P2.6 废弃版本说明 | **未解决** | 未添加 |

**总评:** 本论文在 Round-4 到 Round-5 之间的唯一实质性改进是 0.75x 预算敏感性扫描。该扫描的方向正确（结果模式合理、修复机制论证增强），但完整性和证据可复现性有缺口。14 个前次审查项中仅 1 项部分解决、0 项完全解决——意味着多数圆桌建议尚未被吸收。建议作者优先处理 P0 阻塞项（尤其是 [TODO] 和 AI 声明——这些半小时内可完成）和 P1.1（敏感性分析扩展），再考虑投稿时间线。核心学术贡献（统计严谨性、外部验证、证据透明度）在同类论文中仍属上乘，形式问题解决后有望在 Energies 发表。
