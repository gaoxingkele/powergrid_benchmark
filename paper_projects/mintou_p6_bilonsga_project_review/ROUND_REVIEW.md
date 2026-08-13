# Round-5 投稿前全审: BiLo-NSGA → Applied Sciences (Final Pre-Submission)

**论文 ID:** mintou_p6 (BiLo-NSGA)
**目标期刊:** MDPI Applied Sciences
**评审日期:** 2026-07-16
**评审依据:** 
- 画像校准: mdpi_applied_sciences.yaml + Applied Sciences 已发表论文 11 篇蒸馏
- 证据文件: `evidence/tables/real_project_review_leaderboard.csv` (3840 runs)
- 证据文件: `evidence/tables/real_project_review_significance.csv` (120 comparisons)
- 证据文件: `evidence/tables/real_nerc_rule_backtest.csv` (34 rows)
- 证据文件: `evidence/tables/real_mtep_backtest.csv` (34 rows)
- 新验证: Manuscript Table 5 budget_sensitivity (0.75x) — BiLo-NSGA 0.16013 vs NSGA-II 0.16067, -0.33%, p=1.0 n.s.
- 前次审稿: `ROUND_REVIEW.md` (Round-4); P1.2 敏感性分析需补充

---

## 一、Desk Screen (形式审查)

| 项目 | 状态 | 备注 |
|---|---|---|
| [TODO] 标记 | **未完成** | Author Contributions、Funding、Data Availability（仓库 URL）、Acknowledgments 均为 [TODO]/占位 |
| 声明五件套 | **不完整** | Author Contributions 为模板占位；Funding 未填写；Acknowledgments 为 [TODO] |
| Data Availability | **可接受模板** | 已声明所有公开数据源 URL（RTS-GMLC、SimBench、NERC、MISO），承诺释放 pipeline + implementation + run records |
| Competing Interests | **通过** | "The authors declare no conflicts of interest" |
| AI 使用声明 | **存在** | Section "Generative AI Statement" 已包含，明确声明使用了 "generative AI tools (Claude, Anthropic) for language refinement, literature summary, and formatting assistance" —— 这是三个评审论文中唯一有 AI 声明的，符合 MDPI 政策 |
| 参考文献格式 | **需转换** | 当前为 author-year 引用（Harvard 风格），Applied Sciences 使用 MDPI 编号制 |
| 参考文献数量 | 42 条 | 在 Applied Sciences 已发表中位 28–53 范围内，合理 |
| 近 5 年占比 | 粗估约 55–65% | 包含部分经典引用（Saaty 1980, Hwang 1981）—— 偏低但合理 |
| 过度自引 | **无明显** | 未发现作者团队自引堆叠 |
| 图表 | 占位 | `figures/fig_hv_boxplot.png`, `figures/fig_budget_sensitivity.png`, `figures/fig_ablation.png`, `figures/fig_nerc_backtest.png` 共 4 图 —— 未确认实际图片质量 |
| 摘要长度 | ~220 词 | 在 Applied Sciences 可接受范围内，建议精炼至 200 词 |

**Desk 结论:** 可通过初审。参考格式转换是阻塞项。AI 声明存在为正确定位。

---

## 二、七维评审（机密，仅对作者公开）

### 2.1 Novelty — 原创性与贡献 (weight: 1.2, strictness: 0.95)

**评分: 7/10** (不变 vs Round-4)

BiLo-NSGA 的贡献定位为**已有算法改进（local search 嵌入 NSGA-II 变异阶段）+ 场景适配（电网预算约束审查）**，属于 Applied Sciences 主流。

减分项：
- **Backward deletion 被消融证明不贡献**（Ablation-NoBackwardSearch 0.17294 > BiLo-NSGA 0.17267）—— "bidirectional" 命名与证据的矛盾在任何 AI 审稿中都会触发问题
- **0.75x 预算扫描结果强化了 forward 的不对称性**：tight budget 下 forward 的 slack 少，margin 收窄至统计无差异（-0.33%, p=1.0）—— 此结果虽合理但强调 forward insertion 是唯一贡献组件，使 "bidirectional" 标签更加脆弱
- 命名校准建议 Round-4 的 P1.1（改为 "BiLo-NSGA: A Non-Dominated Sorting Algorithm with Forward Budget-Aware Local Search"）仍未实施

### 2.2 Soundness — 技术正确性 (weight: 1.4, strictness: 1.0)

**评分: 7.5/10** (不变 vs Round-4)

算法设计清晰，消融归因干净，统计协议规范（30 seeds, MW + Holm）。0.75x 预算扫描的 -0.33% n.s. 结果增强了机制论证的可信度——tight budget 下 forward insertion 的 slack 减少导致 margin 收窄，这个模式是合理且预期中的。

仍需质疑：
- Scalarized fitness acceptance criterion 的超参（归一化权重、penalty coefficient）仍无敏感性分析
- Dependency bonus 1.06 因子值仍无敏感性
- **0.75x 预算扫描表明 BiLo-NSGA 在 tight budget 下与 NSGA-II 无差异**—— manuscript Table 5 已诚实报告此点，审稿人会追问 "why keep the overhead of local search when it adds nothing at tight budgets?"

### 2.3 Experiments — 实验与验证 (weight: 1.3, strictness: 1.0)

**评分: 7.5/10** (不变 vs Round-4)

正面：
- 8 个场景覆盖 budget 水平 0.75x/0.88x/1.00x/1.20x、pool 子集和 dependency 结构的多轴变化
- **预算敏感性分析（Section 6.2, Figure 2）是本论文最独特的贡献**—— margin 随 budget 放松从 -0.33% (0.75x) 单调增长到 +3.40% (1.20x) 的模式提供了强机制证据
- 9 ablations 归因充分

缺点：
- **单一 benchmark 家族**（120 candidates, 一个 RTS-GMLC+SimBench+NERC 衍生池）
- **无敏感性分析**（scalarization weight / penalty / dependency bonus / depth 未系统扫描）
- **No load-flow verification**（Limitations 第 5 条已确认）

Budget sensitivity 扫描虽有但不够：Section 6.2 的 4 水平扫描（0.75x/0.88x/1.00x/1.20x）已经是本论文实验设计的亮点。但这属于"问题参数"的敏感性，而非"方法超参"的敏感性——仍缺后者的扫描。

### 2.4 Reproducibility — 可复现性 (weight: 1.1)

**评分: 8.5/10** (不变 vs Round-4)

承诺释放全部 3840 runs + significance + backtest + deprecated versions。算法披露充分。重复 Round-4 的评价：Applied Sciences 中仅 1/11 有代码开源，本论文的透明度属期刊 top 10%。

### 2.5 Related Work — 相关工作与文献 (weight: 0.9)

**评分: 7/10** (不变 vs Round-4)

三条线覆盖合理。2.4 节对 companion TRACE-MOEA 的描述中 "cooperative coevolutionary" 与 TRACE-MOEA 自身描述 "preference-adaptive ranking" 不完全对齐——需校准两篇之间的交叉引用。

### 2.6 Clarity — 价值/读者兴趣与表述 (weight: 1.05, strictness: 1.0)

**评分: 8/10** (不变 vs Round-4)

Applied Sciences 特别重视应用价值。引言第 2 段 "The intended beneficiaries of this work are grid planning departments and investment review boards" 直接点名受众，符合该刊惯例。

新增的 0.75x 预算敏感性分析在 Section 6.2 中以单调增长模式呈现（margin 从 -0.33% 到 +3.40%），叙事清晰。负结果管理（backward deletion 和 tight budget 下无优势）保持高水平学术诚实。

### 2.7 Ethics — 学术诚信与合规 (weight: 0.6)

**评分: 9.5/10** (不变 vs Round-4)

AI 使用声明存在且规范；废弃版本透明保留；companion 关系明确声明。

---

## 三、Adversarial Review（证据盘问）

### Claim 1: "BiLo-NSGA attains pooled mean HV 0.17267, 1.57% above NSGA-II (0.17000)"

**证据:** `real_project_review_leaderboard.csv:3` — BiLo-NSGA 0.17267347 vs NSGA-II 0.17000297, rel diff = +1.571%.

**验证通过.** 精确匹配。

### Claim 2: "44 of 48 baseline comparisons are Holm-significant wins and zero significant losses"

**证据:** `real_project_review_significance.csv` — 6 baselines x 8 experiments = 48. 统计显著数:
- budget_constrained: 5/6 (vs NSGA-II p_holm=0.389, n.s.)
- budget_sensitivity: 5/6 (vs NSGA-II p_holm=1.0, n.s.)
- dependency_constrained: 6/6
- local_move_explainability: 6/6
- project_pool_scalability: 6/6
- ranking_robustness: 6/6
- reliability_prioritized: 6/6
- renewable_accommodation: 4/6 (vs NSGA-II p=1.0, vs NSGA-III p=0.097, n.s.)
Total = 44. 零 significant losses.

**验证通过.** Manuscript 声明正确。特别注意 renewable_accommodation 和 budget_sensitivity 两个场景在 baseline 对比中的非显著结果 manuscript Table 5 已如实报告。

### Claim 3: "98.6% decision coverage"

**证据:** `real_project_review_leaderboard.csv:3` — mean_decision_coverage = 0.98642397.

**验证通过.** 0.9864 ≈ 98.6%.

### Claim 4: "NERC priority capture 1.35–1.62"

**证据:** `real_nerc_rule_backtest.csv:6` — budget_constrained 1.615684; `:25` — reliability 1.352714.

**验证通过.** 区间 [1.353, 1.616] ≈ [1.35, 1.62].

### Claim 5: "MTEP16 broad capture 1.084, r=0.105, p=0.0006"

**证据:** `real_mtep_backtest.csv:4` — BiLo-NSGA budget_constrained: capture_broad=1.084299, r_broad=0.105016, p_broad=0.000609.

**验证通过.** 精确匹配。

### Claim 6: "AHP-TOPSIS achieves the highest nominal broad capture (1.100)"

**证据:** `real_mtep_backtest.csv:3` — AHP-TOPSIS budget: 1.099519.

**验证通过.**

### Claim 7: "Backward deletion does not contribute; NoBackwardSearch +0.16% above full method"

**证据:** `real_project_review_leaderboard.csv:2` vs `:3` — NoBackwardSearch 0.172943 vs BiLo-NSGA 0.172673, diff = +0.156%. Not significant in any experiment.

**验证通过.** 论文最诚实的负结果。

### Claim 8: "Forward insertion carries the gain; NoForwardSearch loses 0.56%"

**证据:** `real_project_review_leaderboard.csv:8` — NoForwardSearch 0.171708 vs proposed 0.172673, diff = -0.56%. Significance in 5/8 experiments.

**验证通过.**

### NEW Claim 9: "Budget sensitivity at 0.75x: BiLo-NSGA -0.33% vs NSGA-II, n.s."

**证据:** `real_project_review_significance.csv:29` — p6 budget_sensitivity: BiLo-NSGA 0.16013204 vs NSGA-II 0.16066951, diff = -0.00053747, p_holm = 1.0, significant = False.

**验证通过.** 精确匹配。Manuscript Table 5: BiLo-NSGA 0.16013 vs NSGA-II 0.16067, -0.33%, Holm p=1.0, not significant. 数据完全一致。

此结果与 P5 (TRACE-MOEA) 的 0.75x 结果 (TRACE-MOEA +1.4% vs NSGA-II) 形成鲜明对比——原因符合各自机制设计：
- P5 TRACE-MOEA: repair operator 在 tight budget 下最有价值 (margin GROWS from +0.89% at 1.0x to +1.4% at 0.75x)
- P6 BiLo-NSGA: forward insertion 依赖 budget slack, tight budget 下无 slack 可供填充 (margin SHRINKS from +1.57% at 1.0x to -0.33% at 0.75x)

这个对比本身就是一种机制验证——两个算法在不同 budget regime 下的性能反转验证了它们依赖不同机制。

---

## 四、Meta Review

### 相对于 Round-4 的变化

| 项目 | Round-4 状态 | Round-5 状态 | 变化 |
|---|---|---|---|
| P1.2 敏感性分析 (weight/penalty/bonus/depth) | 缺失 | 仍完全缺失 | 未解决 |
| P1.1 命名校准 ("bidirectional") | 未处理 | 未处理 | 未解决 |
| P1.3 第二 pool | 缺失 | 仍缺失 | 未解决 |
| P1.4 companion 投稿策略说明 | 未处理 | 未处理 | 未解决 |
| 证据完整性 | 完整 | 完整 (0.75x 结果有 significance.csv 支持) | 无变化 |
| [TODO] 标记 | 未填充 | 仍为 [TODO] | 未解决 |

### 评分汇总

| 维度 | 分数 (0-10) | 权重 | 加权 | 较 Round-4 |
|---|---|---|---|---|
| Novelty | 7.0 | 1.2 | 8.4 | 不变 |
| Soundness | 7.5 | 1.4 | 10.5 | 不变 |
| Experiments | 7.5 | 1.3 | 9.75 | 不变 (预算敏感性分析 Round-4 已计入) |
| Reproducibility | 8.5 | 1.1 | 9.35 | 不变 |
| Related Work | 7.0 | 0.9 | 6.3 | 不变 |
| Clarity | 8.0 | 1.05 | 8.4 | 不变 |
| Ethics | 9.5 | 0.6 | 5.7 | 不变 |
| **总计** | | | **58.4 / 76** | 不变 |

### RRI (Review Risk Index)

**RRI = 58 / 100** (不变 vs Round-4)

Applied Sciences 已发表论文的 RRI 分布无量化数据（仅 Exemplars 三档标记）。58 对应 Major Revision 区间（可挽救），略低于 TRACE-MOEA 的 61（RRI 越低越安全）。

### 推荐决定: Major Revision (不变)

与 Round-4 相同。0.75x 预算扫描的确认未改变整体评价——该数据已存在于 Round-4 审阅的 manuscript 中，本 round 仅完成证据验证。

---

## 五、修改清单 (P0/P1/P2) — 相对于 Round-4 的更新

### P0 — 投稿前阻塞项（必须完成才能提交）

- [P0.1] **替换所有 [TODO] 标记**：Author Contributions（CRediT 角色填入实际姓名）、Funding（填写资助号或声明无外部资助）、Data Availability（填入仓库 URL/DOI）、Acknowledgments
- [P0.2] **转换参考文献为 MDPI 编号制**（当前为 author-year，Applied Sciences 使用 [1][2]...[N] 格式）
- [P0.3] 生成 300 dpi 实际 PNG 图片替换 `figures/fig_*.png` 占位（共 4 图）
- [P0.4] 运行 iThenticate 自检，确认与 TRACE-MOEA manuscript 无重叠句子

### P1 — 大修级修改（审稿人几乎必然要求）

- [P1.1] **处理 "bidirectional" 命名与证据矛盾**（Round-4 延续项）：建议改名为去 "Bidirectional" 的版本或在前言/摘要中明确声明 asymmetric nature 并解释保留 backward pass 的理由（audit completeness + substitution semantics）。0.75x 扫描结果进一步强化了前向不对称性——tight budget 下唯一可能是 forward 的 slack 也消失了，说明算法的全部价值来自 forward insertion under slack。
- [P1.2] **补充敏感性分析**（Round-4 延续项，Applied Sciences 6/11 有）：至少应覆盖 (a) local search acceptance scalarization 权重扰动 (b) penalty coefficient 变化 (c) dependency bonus factor 1.03/1.06/1.12 三水平。最少做 (a)+(c) 两个扫描
- [P1.3] **补充第二 benchmark pool**（Round-4 延续项）：建议从 NREL-118 或 TAMU synthetic 构建第二池。2 scenarios x main comparison 即可
- [P1.4] **讨论 companion papers 同时提交的 editorial 问题**（Round-4 延续项）：在 cover letter 中主动说明两篇 companion 论文的对齐与区分

### P2 — 小修级修改（建议但非阻塞）

- [P2.1] 摘要精炼至 200 词：突出 budget sensitivity 和 forward/backward asymmetry
- [P2.2] 在 Related Work 中增加 1-2 条 Applied Sciences 近 2 年的相关论文引用
- [P2.3] 补充 ORCID 标识符（MDPI 版面要求）
- [P2.4] 在 Discussion 最后增加 "Limitations and Future Work" 子节，将 Section 8 的 5 条限制与可操作的 next steps 配对
- [P2.5] 校准两篇 companion paper 之间对彼此的机制描述：当前 "cooperative coevolutionary" vs "preference-adaptive ranking" 不一致

---

## 六、Round-4 审查项追踪矩阵

| 原 Round-4 项 | 状态 | 说明 |
|---|---|---|
| P0.1 [TODO] 标记 | **未解决** | 仍为 [TODO] |
| P0.2 参考格式转换 | **未解决** | 仍为 author-year |
| P0.3 图片占位 | **未解决** | 仍为 placeholder |
| P0.4 iThenticate | **未解决** | 未确认 |
| P1.1 命名校准 | **未解决** | "bidirectional" 未改 |
| P1.2 敏感性分析 | **未解决** | 完全未做 |
| P1.3 第二 pool | **未解决** | 完全未做 |
| P1.4 companion 投稿策略 | **未解决** | 未处理 |
| P2.1 摘要压缩 | **未解决** | ~220 词未变 |
| P2.2 Applied Sci 引用 | **未解决** | 已引 4 篇目标期刊可补至 5-6 |
| P2.3 ORCID | **未解决** | 未添加 |
| P2.4 limitations + next steps | **未解决** | 未添加配对 |
| P2.5 跨篇机制描述校准 | **未解决** | 描述不一致 |

---

## 七、跨论文对比观察 (P5 vs P6)

### 0.75x 预算敏感性的对比验证

| 指标 | P5 TRACE-MOEA | P6 BiLo-NSGA |
|---|---|---|
| Pooled HV at 1.0x | 0.17425 (+0.89% vs NSGA-II) | 0.17267 (+1.57% vs NSGA-II) |
| HV at 0.75x | 0.16606 (+1.4% vs NSGA-II) | 0.16013 (-0.33% vs NSGA-II, n.s.) |
| Margin direction | **GROWS** as budget tightens | **SHRINKS** as budget tightens |
| Mechanism supported | Repair operator binds harder | Forward insertion needs slack |
| 0.75x 证据来源 | Manuscript叙述 (无单独证据文件) | significance.csv 行 29 (有证据文件) |

学术观察：TRACE-MOEA 和 BiLo-NSGA 在 0.75x 预算下的性能反转（一个 +1.4%、一个 -0.33%）本身就是对两种算法不同机制的有力验证——TRACE-MOEA 的 repair operator 在 tight budget 下提供价值，BiLo-NSGA 的 forward insertion 依赖 budget slack。这种互补性在 cover letter 中可被用作两篇 companion 论文区分而非冗余的证据。

---

**总评:** BiLo-NSGA 的学术贡献（预算敏感性模式、负结果透明报告、消融归因干净）在 Applied Sciences 同类论文中属上乘。与 Round-4 相比无实质改进——0.75x 预算敏感性数据在 Round-4 审阅时已存在于 manuscript，本轮仅完成证据验证，未发现新的不一致。所有 13 个前次审查项均未解决。建议作者在投稿前优先处理 P0 阻塞项（参考格式转换——主要阻塞，AI 声明已存在所以不需要加）和 P1.2（敏感性分析），命名校准 (P1.1) 和 companion 投稿策略 (P1.4) 在 cover letter 中即可回应。
