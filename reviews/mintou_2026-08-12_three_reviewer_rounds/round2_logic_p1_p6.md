# 第二轮严苛复审：逻辑、论证与写作闭环（P1--P6）

**审稿角色：** 第二轮逻辑/写作复审人  
**日期：** 2026-08-12  
**模式：** re-review；只读，不修改主稿  
**核验重点：** 第一轮问题闭环、摘要--方法--结果--结论数字一致性、P5/P6 companion disclosure、预算与外部效度措辞、跨句逻辑和期刊写作风格。

## 总结性决定

第一轮后，六稿的统计表述和负结果披露有明显改善：确定性方法的伪重复推断已在 P3--P6 中剔除；P2 的旧 Ausgrid 结果已退出当前排名；P3 的 AC 层已降为组成级描述；P5/P6 的外部回测已明确降为 descriptive consistency；P6 的预算扫描已改为 budget-indexed cross-scenario diagnostic。

但本轮仍发现 **3 个投稿阻断项**：

1. P2 对同一 Ausgrid CSA--DLinear OLS 比较同时报告 Holm `p=0.0044` 和 `p=0.000985`；
2. P4 贡献列表仍称 “40 of 40 Holm-corrected baseline comparisons”，而摘要、方法、结果和结论已改为 32 个随机基线推断比较加 16 个确定性描述差异；
3. P6 Section 2.4 声称两稿“only”共享候选生成器，但 Section 3.4、Data Availability 以及 P5 均披露还共享 NERC corpus 与 MTEP16 source records。

因此六稿集合当前不能整体进入投稿打包。以下逐篇列出 BLOCKER / MAJOR / MINOR。

---

## P1：Operating-State Retrieval / Curtailment-Risk Benchmark

**阻断结论：无 BLOCKER。** 第一轮的种子范围和 TCN 中心贡献矛盾已基本闭环；仍需修一个图注与结论的统计措辞。

### MAJOR

1. **Figure 4 图注仍将 TCN 隐含成显著败者。** Abstract、Contribution 3、Results 6.3 和 6.6 都正确说明 TCN 在预设 Mann--Whitney family 中 unresolved；但 Figure 4(a) 写“significantly lower than every retrieval-free or retrieval-degraded opponent”以及“Only the two retrieval-preserving variants are indistinguishable”。TCN 是 non-retrieval learned control，却不满足该句。

   建议将图注限定为图中实际显著的命名比较：

   > At 1 h, DSTAR-GRU has significantly lower curtailment MAE than NoSiamese, NoRetrievalBank, SmallBank, LSTM, and MLP. The retrieval-preserving ablations and TCN are unresolved under the prespecified test.

2. **Conclusion 把 test-dependent TCN 写成单一“statistically indistinguishable”。** 同一结论段前一句已说明 post-freeze paired sensitivity 在 1 h 检出 borderline difference，后一句却无条件称 TCN statistically indistinguishable。应保持 primary/sensitivity 两层。

   建议改为：

   > TCN is unresolved under the prespecified unpaired analysis; only the post-freeze paired sensitivity resolves a small 1 h difference.

### MINOR

- Figure 4 图注若只展示一部分 control，应明确 “among the controls shown”，避免读者把图注理解成对 Table 2 全部方法的概括。
- “sign reversal”现已限定到 tested benchmark and horizons，闭环通过。

---

## P2：CSA-LoadNet / Hierarchical Load Forecasting

**阻断结论：存在 1 个 BLOCKER。** 第一轮的 MLP 排名、旧 Ausgrid provenance 和非显著等效性问题均已闭环；剩余阻断是同一比较的 Holm p 值不一致。

### BLOCKER

1. **Ausgrid CSA--DLinear OLS 的 Holm p 值前后不一致。** Introduction Contribution 3 报告 `p=0.0044`；Results exact-hierarchy 段报告 `p=0.000985`；Conclusion 仅写 `p<0.001`。这不是舍入差异，必须用冻结 inference table 确认唯一的 primary adjusted p，并让摘要/贡献/结果/表格/结论统一。

   可执行处理：

   - 以冻结的 exact-hierarchy comparison family 对应记录为唯一来源；
   - 若主值为 `0.000985`，Contribution 3 改为 `Holm p<0.001` 或 `p=0.000985`；
   - 若 `0.0044` 属于另一 comparison family 或旧表，应明确标注该 family，不能与主检验混用。

### MAJOR

无新增 MAJOR。

### MINOR

- Contribution 2 的 “all pairwise Holm p ≈ 1”不如 Results 的“equal 1”精确。建议统一成“all adjusted p=1.000”，同时保留“equivalence was not tested”。
- Figure 6 的 seed-paired 图已声明不承担推断，第一轮问题闭环通过。
- Figure 7 已使用 exact hierarchy under common OLS，旧 Ausgrid 列不再参与 current rank，闭环通过。

---

## P3：CARS-MODE

**阻断结论：无 BLOCKER。** 第一轮最严重的 AC 因果归因已经明显收敛，但 Discussion 仍有两句与结果表直接冲突。

### MAJOR

1. **“best proxy optimizer in this comparison”与 FixedDE 排名冲突。** Table 5 中 Ablation-FixedDE 的 pooled HV 为 0.04243，高于 CARS-MODE 的 0.04218；Discussion 却称 CARS-MODE “is the best proxy optimizer in this comparison”。即使 FixedDE 是 ablation，它仍是实际运行的优化配置。

   建议替换为：

   > CARS-MODE has higher proxy HV than every external baseline tested, while the FixedDE ablation is nominally higher and statistically unresolved.

2. **“front-returning methods ... perform better at both evaluation levels”被 AC 表直接反驳。** Discussion Practical reading 称 front-returning methods 优于 scalarized single-plan methods，且在两个评价层都更好；但 Standard DE 是 scalarized baseline，AC-feasible rate 0.681，为 Table 7 最高，高于 CARS-MODE 0.611。该句会损害全文强调的 proxy--physics disagreement。

   建议替换为：

   > Front-returning methods provide a trade-off set and dominate the scalarized controls on proxy hypervolume, but the AC composition check does not preserve that ordering; Standard DE has the highest mapped AC-feasible rate.

### MINOR

- Figure 3 caption 的 FixedDE “loses AC feasibility”仍略带因果/比赛语气；改为 “has a lower mapped AC-feasible rate in the descriptive composition check”。
- Results 6.3、Conclusion 已明确 seed-0/one-compromise-plan 限制，不再把 adaptation 当作电气因果来源，第一轮问题闭环通过。
- 6.22%（vs. NSGA-II+Repair）和 6.34%（vs. plain NSGA-II）现已点名比较对象，闭环通过。

---

## P4：SHIELD-MOEA

**阻断结论：存在 1 个 BLOCKER。** 摘要、方法、结果与结论的随机/确定性推断已修正，但 Contribution 3 仍保留旧统计口径。

### BLOCKER

1. **贡献列表的 `40/40 Holm` 与全文修正后的 inferential family 冲突。** Abstract、Methods 5.3、Results 6.1、Discussion 和 Conclusion 均使用：四个 stochastic baselines × 八个实验 = 32 个 Holm 推断比较；Weighted Sum 与 Deterministic Planning 共 16 个 experiment-level gaps，只作描述。Introduction Contribution 3 仍写“40 of 40 Holm-corrected baseline comparisons significant”。这会使编辑无法判断统计口径是否真正冻结。

   建议将 Contribution 3 替换为：

   > Across four stochastic baselines and eight experiments, SHIELD-MOEA records 32 of 32 Holm-significant wins; sixteen additional gaps against two deterministic rules are descriptive and favor SHIELD-MOEA.

### MAJOR

1. **Results 6.2 仍把 sampled worst-case 过读为非专门化和 graceful degradation。** 该段称 fronts “are not specialized to benign scenarios”且“degrade gracefully”，但 Limitations 7 和 Conclusion 已正确说明 16 个场景的 sample-dependent worst-case 不能认证真实 robustness。

   建议替换该段末部：

   > In the frozen evaluation sample, the worst-case-HV margin is similar to the mean-HV margin. This provides no observed mean--tail reversal in that sample, but it neither proves non-specialization nor bounds true worst-case behavior.

### MINOR

- “outage-aware search matters where outages matter”标题仍略强；正文已有 composition-level descriptive caveat，可改成“Outage exposure is associated with a larger AC composition difference in outage-heavy settings”。
- `leakage-proof/certify` 已大体替换为 direct-reuse leakage control，闭环通过。
- NoScenarioScreen 已改为“no difference detected; equivalence not tested”，闭环通过。

---

## P5：TRACE-MOEA

**阻断结论：无 BLOCKER。** 第一轮的组件因果归因、确定性伪重复、companion disclosure 和外部效度显著性过读基本闭环；仍有两处外部效度用词回退。

### MAJOR

1. **Limitations 与主结果的 descriptive-only 定位不一致。** Section 6.5 和 Conclusion 明确表示 project-level p 值没有保留 portfolio dependence 或 confirmatory family，因此只支持 descriptive external consistency。Limitations 1 却说 backtests “validate alignment”，Limitations 2 标题写“External validity established in weak form only”。“validate/established”会把已降级的证据重新抬高。

   建议替换为：

   > The NERC and MTEP checks assess descriptive alignment but do not validate review correctness.

   以及：

   > **External consistency assessed descriptively only.** Neither rung establishes external validity because portfolio-preserving confirmatory inference and expert ground truth are absent.

### MINOR

- Results 6.1 的“三个显著 full-vs-NSGA-II 情景”现已与 direct ablation 分开，Discussion 也明确不能归因于 preference layer，闭环通过。
- P5 Data Availability 与 Discussion 已披露 P5/P6 共享 candidate generator、NERC corpus、MTEP16 records，并说明 run archives/selected portfolios/comparisons 为 paper-specific，闭环通过。
- “exact methods do not scale”仍是过宽的文献判断，建议改为“can become computationally difficult for richer dependency structures at this pool size”。

---

## P6：BiLo-NSGA

**阻断结论：存在 1 个 BLOCKER。** 预算扫描和外部效度边界已闭环；阻断项是 companion disclosure 在 Section 2.4 内部仍自相矛盾。

### BLOCKER

1. **Section 2.4 的“share only the public candidate generator”与后文披露冲突。** Section 3.4、Data Availability 和 P5 均说明两稿还共享 public NERC corpus 与 MTEP16 source records，并分别运行冻结回测。“only”构成事实矛盾，也关系到重复发表/伴侣稿透明度。

   建议把 Section 2.4 替换为与 Section 3.4 完全一致的句子：

   > The two studies share the versioned candidate generator and the public NERC and MTEP16 source corpora. Their problem objectives, algorithm implementations, scenario definitions, run archives, selected portfolios, and reported comparisons are paper-specific.

### MAJOR

1. **非显著仍被写成“statistically indistinguishable”。** Results 6.1 对 0.75x 与 renewable-filtered pool 使用该词，但全文其他位置已经采用 unresolved。没有等效性检验时应保持同一标准。

   建议改为：

   > BiLo-NSGA is unresolved against NSGA-II, with nominal losses of 0.64% and 1.31% in those settings.

### MINOR

- Section 3.3 与 Results 6.2 均已把预算结果改为 budget-indexed cross-scenario comparison，并明确 scalar weights/seed streams 未固定，第一轮预算因果问题闭环通过。
- LooseBudget 已限定为 tested setup，不再使用 universal “must”，闭环通过。
- NERC/MTEP16 已统一为 descriptive consistency，不再声称 above-chance inference，闭环通过。
- Section 2.4 和 Discussion 应避免笼统写“analyses are independent”；优先使用可审计资产名（run archives、selected portfolios、reported comparisons）。

---

## 跨稿一致性与期刊风格检查

### BLOCKER

- 在修正上述三处硬矛盾前，不建议生成最终投稿 PDF/ZIP：数字或共享资产声明在编辑初审中即可被发现。

### MAJOR

- 六稿统一使用以下证据等级词汇：
  - 主检验显著：`significantly higher/lower under the prespecified family`；
  - 主检验不显著：`unresolved / no difference detected`；
  - 未做等效性检验：不得使用 `equivalent / indistinguishable / without loss`；
  - AC 单一组成映射：`descriptive composition-level check`；
  - NERC/MTEP project-level 非独立检验：`descriptive external consistency`，不得使用 `validated / above chance / established validity`。

### MINOR

- P3--P6 对 deterministic rules 的有效样本量说明现已基本一致，应继续在图注中把 repeated provenance rows 与 inferential n 分开。
- 在最终排版前做一次自动一致性表：从摘要、贡献、主结果、结论抽取每个核心数字及 comparator，确保每个值只有一个定义。

## 第二轮最终判定

| 稿件 | BLOCKER | MAJOR | 本轮判定 |
|---|---:|---:|---|
| P1 | 0 | 2 | 大修后可复核 |
| P2 | 1 | 0 | 阻断：统一 Ausgrid p 值 |
| P3 | 0 | 2 | 大修后可复核 |
| P4 | 1 | 1 | 阻断：修正 40/40 旧口径 |
| P5 | 0 | 1 | 小修至大修 |
| P6 | 1 | 1 | 阻断：统一 companion disclosure |

**集合判定：暂缓投稿打包。** 三个 BLOCKER 均为文本/口径修复，不要求重跑实验；修复后应进行一次短的第三轮数字与披露核验。
