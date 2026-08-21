# 第三轮统计终审：P1--P6

日期：2026-08-12  
角色：方法学与统计终审人  
模式：只读复审；未修改六篇主稿、实验档案、统计脚本或证据表。  
审查范围：修复后的 `exact_signflip_p`、回归测试、新导出的 P1/P2 primary/paired 表、P3/P4 探索性敏感性、P3--P6 确定性方法处理、跨场景 Holm 族，以及 P5/P6 外部回测的推断边界。

## 1. 最终判定

| 论文 | 判定 | 结论 |
|---|---|---|
| P1 DSTAR-GRU | **PASS** | 主分析、配对敏感性、效应量/区间边界和方法计数一致 |
| P2 CSA-LoadNet | **PASS** | 旧 Ausgrid 数字已清除；精确符号翻转修正后的三组关键 p 值均已同步 |
| P3 CARS-MODE | **BLOCKER** | 统计证据本身通过，但正文把 FixedDE 写成“unresolved in 0/7”，与证据和上下文相反 |
| P4 SHIELD-MOEA | **PASS** | 32/32 随机基线族、16 个确定性差距、NoOutage 双 Holm 族及探索性扫描均已正确定位 |
| P5 TRACE-MOEA | **PASS** | 随机/确定性划分、跨场景消融和外部描述性定位一致 |
| P6 BiLo-NSGA | **PASS** | 外部 broad-capture 排序和特征重叠表述已修复；3/8 主族与 4/8 探索族区分明确 |

六篇中只有 P3 留有一处会直接反转组件结论含义的文字阻断项。该项不要求重跑实验或重算统计；修正一句话后即可再做一次机械全文搜索确认。

## 2. 审计实现与证据链

### 2.1 `exact_signflip_p`：PASS

证据：`scripts/mintou/build_statistical_audit_v2.py:49--57`。

当前实现穷举全部 (2^n) 个符号向量，并返回

\[
p=\frac{\#\{|\bar d^*|\ge |\bar d_{obs}|\}}{2^n},
\]

不再错误地使用 Monte Carlo “+1”修正。函数文档明确称其为 complete sign enumeration 的 exact two-sided randomization p-value。

### 2.2 回归测试：PASS

执行：

```text
python -m unittest tests.test_mintou_statistical_audit_v2 -v
```

结果：4/4 通过。

- 十个全正差值返回 (2/2^{10}=0.001953125)；
- 观测均值为零的构造返回 1；
- sign balance 明确不按秩加权；
- 零差值被排除在 sign balance 分母之外。

`paired_sign_balance` 的名称和文档已明确其不是 Wilcoxon matched-pairs rank-biserial correlation（脚本 `:60--69`）。

### 2.3 新导出表与论文证据副本：PASS

SHA-256 逐字节比对结果：

- P1 `p1_primary_inference.csv` = `real_curtailment_primary_inference_v2.csv`；
- P1 `p1_paired_sensitivity.csv` = `real_curtailment_paired_sensitivity_v2.csv`；
- P2 `p2_primary_inference.csv` = `real_p2_primary_inference_v2.csv`；
- P2 `p2_paired_sensitivity.csv` = `real_p2_paired_sensitivity_v2.csv`；
- P3/P4 的 `stochastic_only_inference.csv` 分别与各自 `real_simbench_planning_inference_v2.csv` 相同；
- P5/P6 的 `stochastic_only_inference.csv` 分别与各自 `real_project_review_inference_v2.csv` 相同。

审计总表已明确：5000 次 bootstrap 区间是 pointwise、multiplicity-unadjusted；P1/P2 符号翻转只是后冻结配对敏感性；非显著结果解释为 unresolved 而非 equivalent。

## 3. 关键数字核验

### P1

- Primary：每时距 27 项（3 指标 × 9 个随机对手）；确定性方法只作单点描述。
- 配对表：54 项。
- 1 h MAE，NoSiamese 与 NoRetrievalBank：paired Holm (p=0.017578)，正文四舍五入为 0.0176。
- 1 h MAE，TCN：paired Holm (p=0.046875)，正文为 0.0469；主 MWU 仍未解决。
- 24 h onset F1：NoSiamese 0.017578、NoRetrievalBank 0.023438、LSTM 0.017578；正文分别为 0.0176、0.0234、0.0176。
- SmallBank 方法总数已由错误的 12 改为 14；Figure 4 图注已不再把 TCN 错误包含进“所有无检索方法显著较差”的范围。

判定：**PASS**。

### P2

- OPSD/SimBench 每个数据集--时距块为 6 个 proposed-versus-opponent 比较。
- Ausgrid 主分析按角色分成两个五项 Holm 族；配对敏感性包含全部十个对手。
- OPSD 1 h CSA-LoadNet vs MLP：exact (p=0.0078125)，paired Holm (p=0.046875)；正文 0.0469。
- OPSD 24 h CSA-LoadNet vs MLP、vs TemporalOnly：exact (p=0.001953125)，paired Holm (p=0.01171875)；正文 0.0117。
- Ausgrid OLS CSA-LoadNet vs DLinear：主 Holm (p=0.000984513)，paired Holm (p=0.01953125)；正文分别为 0.000985 和 0.0195。
- 引言中旧的非精确层级 p=0.0044 已删除；当前引言和结果统一为 0.000985。

判定：**PASS**。

### P3

- 随机基线族：56 项，56 个正均值，55 个显著胜，0 个显著负。
- 确定性方法：仅 Weighted Sum；7 个场景均为 `descriptive_deterministic_n1`。
- 关键消融跨场景族：NoDiversity 7/7 显著，NoRepair 7/7 显著，FixedDE 0/7 显著。
- 参数扫描已明确标注为 exploratory，六个 MWU p 值是 nominal、multiplicity-unadjusted；正文只描述均值模式，不再把它们作为确认性显著性族。

阻断项：`MANUSCRIPT.md:402` 写道：

> “FixedDE is unresolved in 0/7 under both families.”

这与审计结果和紧邻的 `MANUSCRIPT.md:404`（“not Holm-significant in any of the seven experiments”）相反。正确表述只能是以下二者之一：

- “FixedDE is **resolved in 0/7** under both families”；或
- “FixedDE is **unresolved in 7/7** under both families”。

该错误位于核心组件归因段，不能作为普通文风问题忽略。

判定：**BLOCKER**。只需修正文句，无须重算或重跑实验。

### P4

- 随机基线族：32 项，32 个显著胜，0 个显著负。
- 确定性方法：Weighted Sum、Deterministic Planning；16 个场景级差距均只作描述。
- 摘要、贡献、结果、讨论和结论现均使用 32/32 + 16，不再残留 40/40。
- NoOutage：主场景内族中 outage-contingency (p=0.0323)、restoration-aware (p=0.00910)；第二个跨八场景 Holm 族中分别为 0.0753（未显著）和 0.0243（显著）。`MANUSCRIPT.md:433` 正确并列两套判定。
- 参数扫描已改为 exploratory，九个 p 值明确为 nominal、multiplicity-unadjusted；结论只描述均值敏感性。
- sampled worst-envelope 段已删除不同归一化列的原始数值直接比较，并明确不证明非专门化、不界定真实尾部行为。

判定：**PASS**。

非阻断编辑建议：Table 4 的 CI 表注可进一步补入 “pointwise, multiplicity-unadjusted”，与 P5/P6 的表注完全统一；当前统计审计总表已说明这一属性，且 Table 4 所列 NSGA-II 判定不受影响。

### P5

- 随机基线族：28 项，27 个正均值，24 个显著胜，0 个显著负。
- 确定性方法：AHP-TOPSIS、Weighted Sum、Greedy BCR；21 个差距均为 `n_eff=1` 描述性比较。
- Random Feasible 正确作为随机方法进入推断族。
- NoPreferenceRanking：跨场景 Holm (p=0.0722)，0/7；NoScheduleRisk：关键 traceability 单元跨场景 (p=0.0510)，0/7。正文均称 exploratory/unresolved。
- Table 5 已明确 CI 为 pointwise、multiplicity-unadjusted，Holm rank-test p 值控制显著性结论。
- NERC/MTEP p 值被明确称为 raw/unadjusted descriptive diagnostics；正文承认构造重叠、组合内项目依赖、无确认性比较族、高建成基率和仅 19 个明确撤回项目。未作 above-chance、最佳对齐或真实工程效益推断。

判定：**PASS**。

### P6

- 随机基线族：40 项，37 个正均值，36 个显著胜，0 个显著负。
- 确定性外部基线：AHP-TOPSIS、Greedy BCR，共 16 个描述性差距；确定性消融 Ablation-WeightedRankingOnly 另有 8 个描述性差距。三者均为 `descriptive_deterministic_n1`。
- NoForwardSearch：主场景内族支持 3/8；探索性的 operator-specific 跨场景 Holm 族支持 4/8，新增 reliability-prioritized (p=0.04734)。`MANUSCRIPT.md:420` 已清楚区分两者。
- MTEP broad capture：AHP-TOPSIS 1.0995，BiLo-NSGA 1.0715，NoFeasibilityRecovery 1.0877，LowDependencyDensity 1.0716。正文已删除“超过七个外部基线”的错误，明确 AHP-TOPSIS 更高且两个消融也略高。
- “outcomes independent of featurization”已改为“outcome snapshots were not used in fitting”，同时承认 decision-time `appendix_status` 是 prognostic feature 并与 broad outcome 形成 construct overlap。
- 外部 p 值明确为 nominal project-level diagnostics；无组合保持检验和多重比较族，因此只作 descriptive external consistency，不作 portfolio-level significance 或 above-chance 推断。

判定：**PASS**。

## 4. 最终统计门槛

当前唯一强制修改：

1. 将 P3 `MANUSCRIPT.md:402` 的 “unresolved in 0/7” 改为 “resolved in 0/7” 或 “unresolved in 7/7”。
2. 修改后全文搜索 `unresolved in 0/7`，确认主稿、LaTeX、投稿预览和图表说明中无副本残留。

在该句修复之前，六篇组合不能整体标记为统计终审全通过。修复后，根据本轮已核验的代码、测试、CSV、证据副本和正文关键数字，不需要重新运行核心实验，也不需要再次改变 Holm 家族。
