# 第三轮终审：逻辑与写作最终核验（P1--P6）

**审稿角色：** 逻辑/写作终审人  
**日期：** 2026-08-12  
**模式：** re-review；只读，不修改主稿  
**依据：** 六篇当前最新版 `MANUSCRIPT.md`、第二轮报告、`statistical_audit_v2/STATISTICAL_AUDIT_V2.md` 及其推断表。

## 终审结论

第二轮的 **3 个 BLOCKER 和全部 MAJOR 均已闭环**。当前未发现会阻止投稿打包的摘要--贡献--方法--结果--结论数字矛盾、旧统计口径残留、companion disclosure 冲突或外部效度越界主张。

`statistical_audit_v2` 的核心计数已一致进入相关稿件：

| 稿件 | 随机基线比较 | 显著胜 | 显著负 | 正均值差 | 确定性描述差异 | 当前稿一致性 |
|---|---:|---:|---:|---:|---:|---|
| P3 | 56 | 55 | 0 | 56 | 7 | 一致 |
| P4 | 32 | 32 | 0 | 32 | 16 | 一致 |
| P5 | 28 | 24 | 0 | 27 | 21 | 一致 |
| P6 | 40 | 36 | 0 | 37 | 16 | 一致 |

最终判定：**六篇均 PASS（逻辑/写作维度）**。以下残余均为 MINOR 编辑清理，不构成投稿阻断，也不要求重跑实验。

---

## P1：Operating-State Retrieval / Curtailment-Risk Benchmark

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- Abstract 已区分 stochastic ten seeds 与 deterministic single run。
- Contribution 3、Results、Figure 4 和 Conclusion 均把 TCN 定位为 prespecified unpaired analysis 下 unresolved，并单独披露 post-freeze paired sensitivity 的小幅 1 h 差异。
- Figure 4 已删除“every retrieval-free opponent”旧概括，改为逐项列出 NoSiamese、NoRetrievalBank、SmallBank、LSTM 和 MLP。
- Persistence 总体 MAE 最佳、Ridge 24 h onset 最佳、NREL-118 零阳性和无 cross-system-transfer claim 在摘要、结果与结论一致。
- 旧 paired p 值已由 `statistical_audit_v2` 当前值替换，未检出第二轮旧值残留。

### 残余 MINOR

- “statistically tied at the top”可进一步改为“unresolved against the two nominally higher encoder variants”，以完全统一 evidence-grade vocabulary；当前上下文已经解释不领先，因此不构成实质问题。

---

## P2：CSA-LoadNet / Hierarchical Load Forecasting

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- 第二轮 BLOCKER 已修复：Ausgrid CSA--DLinear under common OLS 在 Contribution 3 和 Results 中统一为 primary Holm `p=0.000985`；Conclusion 使用兼容的 `p<0.001`。
- OPSD 24 h 主结果在摘要、贡献、结果中一致：0.032345 vs. 0.033715，Holm `p=0.0085`；vs. TemporalOnly 0.034591，`p=0.0011`。
- exact Ausgrid 当前排名使用 DLinear Bottom-Up 0.28017、DLinear OLS 0.28047、CSA OLS 0.28949；旧 hierarchy 仅作 superseded provenance。
- weighting-form 结果统一为 unresolved，adjusted `p=1.000`，并明确 equivalence was not tested。
- primary Mann--Whitney 与 post-freeze paired sensitivity 已分层陈述；CI 明确为 pointwise、multiplicity-unadjusted。

### 残余 MINOR

- Limitations/Conclusion 仍有“inseparable from MLP, TCN, and PatchTST-lite”。为避免被理解为等效，建议最终语言清理时改为：

  > unresolved against MLP, TCN, and PatchTST-lite under the primary family

---

## P3：CARS-MODE

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- 摘要、贡献、Results 6.1 和 Conclusion 均使用 56 个随机基线比较、55 个显著胜、7 个 Weighted Sum 描述差异。
- 6.22% 已固定为相对 NSGA-II+Repair；6.34% 明确为相对 plain NSGA-II，不再混用比较对象。
- Discussion 已删除“best proxy optimizer”绝对表述，改为高于所有 external baselines，同时披露 FixedDE nominally higher and unresolved。
- Practical reading 已修复：front-returning methods 只在 proxy HV 上占优，AC 排名不保持该顺序；Standard DE 0.681 为最高 mapped AC-feasible rate。
- AC 证据全稿统一为 seed-0、composition-level、descriptive check；不再把 adaptation 写成电气因果来源。
- Conclusion 明确 adaptation 不改善 proxy 或 electrical performance，和 FixedDE +0.60% 负消融一致。

### 残余 MINOR

- Abstract 和 Discussion 的“never significantly different”建议统一为“unresolved in all seven scenarios”；当前并未声称等效，属于风格统一项。
- Table 5 caption 可像 P4--P6 一样补一句：Weighted Sum 的重复归档行不构成 seeded inference，以进一步提高跨稿一致性。

---

## P4：SHIELD-MOEA

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- 第二轮 BLOCKER 已修复：Contribution 3 现为 32 个 stochastic-baseline Holm-significant wins，加 16 个 deterministic descriptive gaps；与 Abstract、Methods、Results、Discussion 和 Conclusion 完全一致。
- sampled worst-envelope 结果统一为 0.26911、相对 NSGA-II +5.36%，并明确不证明 non-specialization、不界定 true worst case。
- “leakage-proof/certify”已替换为 direct-reuse-leakage-controlled；unseen-stress 只用于 test resistance，不作认证。
- screening 统一表述为减少 65% recorded calls、no difference detected、equivalence not tested；未声称质量等效或实际 wall-clock gain。
- AC 层统一为 composition-level descriptive check，并保留 matched-repair NSGA-II 0.694 高于 SHIELD-MOEA 0.685 的不利结果。

### 残余 MINOR

- Contribution 4 中“never significant”可改成“unresolved in all eight experiments”，与全套 evidence-grade vocabulary 完全一致。
- “Outage-aware search matters where outages matter”小标题若仍保留，可改为更中性的“Outage exposure and the AC composition difference”。正文已有 causal caveat，因此不构成实质问题。

---

## P5：TRACE-MOEA

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- 摘要、贡献、结果和结论均使用 28 个 stochastic-baseline comparisons、27 个正均值差、24 个 Holm-significant wins、21 个 deterministic descriptive gaps。
- preference adaptation 的 pooled 0.17% 已降为 cross-scenario correction 后 unresolved；full-vs-NSGA-II 的三个情景胜利不再被归因给 preference component。
- NERC/MTEP16 全稿统一为 descriptive external consistency；明确 project dependence、无 confirmatory family、98% strict-label build rate、19 个 explicit negatives，并不声称 above-chance portfolio performance。
- Limitations 已改为“External consistency is assessed descriptively only”，删除“validity established/validate alignment”回退措辞。
- P5/P6 共享声明现在一致：共享 versioned candidate generator、NERC source corpus、public MTEP16 records；operators、objectives、scenarios、run archives、selected portfolios 和 reported comparisons 为 paper-specific。
- deterministic rules 的 repeated provenance rows 与 effective sample size one 已在 Methods、Table 4 和 Results 中明确区分。

### 残余 MINOR

- Figure 6 caption 仍使用“External-validity ladder”，而章节标题和结论已经使用“External Consistency”。建议改为“External-consistency ladder”，避免标题级术语回退。
- Limitations 4 的“quarantine guarantees that trace statistics do not inflate performance”可更机械地写为“prevents trace statistics from entering objectives, selection, or the reported metric”；这样不会被理解为对全部间接计算效应的绝对保证。

---

## P6：BiLo-NSGA

**判定：PASS。无 BLOCKER，无 MAJOR。**

### 已闭环

- 第二轮 companion BLOCKER 已修复：Section 2.4、Section 3.4 和 Data Availability 均披露 candidate generator、NERC corpus 与 MTEP16 records 的共享范围，并列出 paper-specific assets。
- 摘要、贡献、Results 和 Conclusion 均使用 40 个 stochastic-baseline comparisons、37 个正均值差、36 个显著胜、16 个 deterministic descriptive gaps。
- Results 已把 0.75x 与 renewable-filtered comparisons 改为 unresolved against NSGA-II，不再写 statistically indistinguishable。
- budget analysis 已统一为 budget-indexed cross-scenario diagnostic，明确 weights 和 random streams 未固定，不能归因于 budget headroom 或 forward insertion。
- LooseBudget 6.35% 只支持 tested setup，不再写 universal “must”。
- NERC/MTEP16 统一为 descriptive external consistency；raw project-level p 值与“no portfolio-level significance / no above-chance inference”相邻披露。
- forward-dominant 主张已限定为 primary within-scenario family 的三个 resolved cells；atomic substitution 明确没有 accuracy gain。

### 残余 MINOR

- Contribution 4、Results 6.3/6.6 和 Conclusion 仍使用“mutually inseparable / is also inseparable”。为避免等效暗示，统一改为：

  > unresolved under the declared comparison family

- Conclusion 的“removing forward insertion is significantly harmful in three scenarios”与 primary family 一致，但可补“under the primary within-scenario family”，与 Abstract 完全镜像。

---

## 旧数值与证据等级全文搜索结论

第三轮针对第二轮旧口径进行了全文检索：

- 未再发现 P3 的旧 `62/63` 比较口径；
- 未再发现 P4 的旧 `40/40 Holm` 口径；
- 未再发现 P5 的旧 `45/49` 或 `48/49` 口径；
- 未再发现 P6 的旧 `52/56` 或 `53/56` 口径；
- 未再发现 P2 的旧 Ausgrid `p=0.0044`；
- P1/P2 paired sensitivity 已更新为 `statistical_audit_v2` 当前值，旧 paired p 值未残留；
- P5/P6 的 raw MTEP p 值仍保留，但已明确标为 descriptive diagnostics，未用于 confirmatory/above-chance claim。

## 最终决定

| 稿件 | BLOCKER | MAJOR | MINOR | 逻辑/写作终审 |
|---|---:|---:|---:|---|
| P1 | 0 | 0 | 1 | PASS |
| P2 | 0 | 0 | 1 | PASS |
| P3 | 0 | 0 | 2 | PASS |
| P4 | 0 | 0 | 2 | PASS |
| P5 | 0 | 0 | 2 | PASS |
| P6 | 0 | 0 | 2 | PASS |

**终审意见：六篇可通过逻辑/写作闸门。** 上述 MINOR 建议可在最终语言与 LaTeX 排版清理中完成；不需要为这些问题重新运行实验。该 PASS 仅覆盖本轮指定的内部逻辑、数字一致性、共享资产披露和证据等级措辞，不替代最终引用核验、图像分辨率检查、作者信息确认或期刊格式检查。
