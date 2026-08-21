# 第三轮理论与创新终审（P1–P6）

**终审角色：** 理论基础、算法创新与证据边界审稿人  
**日期：** 2026-08-12  
**范围：** 六篇当前最新版 `MANUSCRIPT.md`；只读，不修改主稿。  
**判定口径：** `PASS` 表示创新身份、理论边界、负消融和外部证据等级已经闭合；“残余项”是不改变核心科学结论的提交前文字清理。本报告只判定理论/创新维度，不替代作者信息、基金、格式、引用与数据包终检。

## 1. 总体终审结论

| 论文 | 终审判定 | 已稳定的创新身份 | 残余风险等级 |
|---|---|---|---|
| P1 DSTAR-GRU | **PASS** | 参考政策代理基准 + onset protocol + 检索跨时域反转的机制审计 | Minor |
| P2 CSA-LoadNet | **PASS** | cross-series aggregation existence 的组件级实证审计；几何权重负结果 | Minor |
| P3 CARS-MODE | **PASS** | constraint-aware MO-DE 框架 + direct DE controls + adaptation null + proxy/physics gap | Minor |
| P4 SHIELD-MOEA | **PASS** | selective scenario exposure + disjoint-draw scoring + 场景调用节约；动态重筛 null | Minor |
| P5 TRACE-MOEA | **PASS** | metric-quarantined event provenance + constrained portfolio search；preference effect unresolved | Minor |
| P6 BiLo-NSGA | **PASS** | project-vocabulary local search + forward-side resolved cells + substitution audit semantic | Minor |

第三轮没有发现 BLOCKER 或需要新增实验才能维持现有主张的 MAJOR 问题。六篇均已从“所有组件均带来增益”的传统改进算法叙事，转为“完整框架表现、可归因组件、未决组件和外部边界分别陈述”的证据结构。

---

## 2. P1：Operating-State Retrieval Framework

### 判定：PASS

### 终审核对

- Abstract 明确 70% SNSP-type cap 生成 `curtailment-rate proxy`，并明确不是 observed dispatch-curtailment record。
- Introduction Contribution 1 已统一为 `reference-policy curtailment-risk proxy target`，III-A、Figure 1 caption 也使用同一术语。
- 检索组件的正结论只落在 1 h MAE 的预设去检索/退化检索对照；24 h onset warning 的负效应同时进入摘要、结果、讨论和结论。
- Persistence、ridge、raw kNN 等确定性基线只作单次描述，随机方法才进入十种子推断。
- NREL-118 全零审计被解释为冻结政策不可直接迁移，不再称外部性能验证。
- Conclusion 明确跨时域反转仅限固定测试年、测试 horizon 和 seed variability，并排除 forecasting superiority、OPF 和 uncalibrated transfer。

### 残余项（Minor）

Conclusion 首段仍写 `method-independent target follows a fixed 70% ... policy`，可再补一个 `proxy`，与摘要和贡献逐字一致：

> Its method-independent proxy target follows a fixed 70% SNSP-type reference policy.

这不影响当前科学判定。

### 最终创新边界

可声称：公开、方法独立的参考政策代理基准；稀疏序列的 onset evaluation；检索在该基准上随 horizon 改变作用方向。  
不可声称：真实调度弃电预测领先、跨系统迁移、检索普遍因果规律。

---

## 3. P2：CSA-LoadNet

### 判定：PASS

### 终审核对

- 正结果严格限定为 OPSD-24 h 上十种子 MLP comparator 与 no-aggregation ablation。
- TCN、PatchTST-lite、DLinear、LSTM 的 OPSD preliminary screen 明确只有三 seeds，不再作为同等强度 confirmatory evidence。
- Poincaré、Euclidean、equal-weight、fixed-curvature 被表述为 unresolved；正文明确 equivalence was not tested。
- OPSD-1 h 显著负、SimBench 未分离、Ausgrid 输给 DLinear 均进入贡献、结果、限制和结论。
- exact hierarchy 与 reconciliation 只证明结构 coherence，不再被写成准确性提升。
- 后验 claim downgrade/renaming 已披露，未冒充 preregistration。

### 残余项（Minor）

- 投稿前做一次 UTF-8/LaTeX 字符审计，确保 `Poincaré`、Mann–Whitney 等在 PDF 中不出现乱码。
- Highlights 和 cover letter 应继续使用 `component-level audit`，不要恢复为 `novel hyperbolic attention superiority`。

### 最终创新边界

可声称：在一个明确的 national-load day-ahead setting 中，cross-series aggregation 本身有可分离贡献；复杂权重形式在当前精度下没有分离。  
不可声称：跨数据集通用优越、hyperbolic geometry 获得实证支持、层次预测领先。

---

## 4. P3：CARS-MODE

### 判定：PASS

### 终审核对

- Contribution 1 已改为 `constraint-aware multi-objective DE framework with an audited strategy-adaptation feature`，并当场说明 adaptation 不是 proxy gain 来源。
- Abstract、VI-6.2、Discussion 和 Conclusion 均报告 FixedDE pooled +0.60% 且七场景 unresolved。
- Figure 3 caption 已改为固定 composition mapping 下 FixedDE 的 descriptive AC-feasible rate 较低，不再使用因果性的 “loses AC feasibility”。
- AC 层仅用于显示 proxy ranking 不等于 electrical ranking；seed-0 compromise composition 不再被当作自适应组件的统计证明。
- Weighted Sum 的有效样本量已设为 1，七个差异仅描述；55/56 推断胜场限定为 stochastic baselines。
- GDE3 与 NSDE 提供 direct MO-DE controls，但正文明确这些框架级胜利不能救回 adaptation component claim。
- Conclusion 最终落点是 constrained framework 的高 proxy HV 和 proxy/physics disagreement，而不是 self-adaptation breakthrough。

### 残余项（Minor）

题名仍以 `Strategy-Adaptive` 为显著识别词。当前正文已充分抵消过度解读，因此不构成阻断；但 short title、Highlights 和 cover letter 应优先称：

> a constraint-aware multi-objective DE framework with an audited, proxy-neutral adaptation feature

### 最终创新边界

可声称：在七个 SimBench-derived proxy scenarios 上相对 matched-repair NSGA-II、GDE3、NSDE 的框架级优势；repair/diversity 的组件作用；代理 HV 与 AC composition 排名不一致。  
不可声称：self-adaptation 提升 HV 或电气性能、composition mapping 证明 nodal planning quality。

---

## 5. P4：SHIELD-MOEA

### 判定：PASS

### 第二轮 BLOCKER 回归

**调用公式：已修复。** 正式定义现为

$$
C_{\mathrm{screened}}=GN_uK+N_rN_p|\mathcal S|
=12{,}800+5{,}120=17{,}920,
$$

其中 $N_u=80$、$N_p=40$、$N_r=8$。效率式同步给出 $1-17{,}920/51{,}200=0.65$，旧的 11,520 隐含公式已不存在。

**32+16 口径：已修复。** Abstract、Contribution 3、Results、Discussion 和 Conclusion 均统一为：四个 stochastic baselines × 八实验 = 32 个 Holm 推断比较；两个 deterministic rules × 八实验 = 16 个描述差异。

### 其他终审核对

- screening 只声称减少 recorded plan–scenario calls；正文明确未证明 wall-clock、energy 或 simulator cost 节约。
- no-screening 未显著不再被解释为 equivalence；正文明确 equivalence tolerance 未测试。
- periodic re-screening 与 fixed generation-1 worst-K unresolved，hybrid 与 DE-only unresolved，均已作为负组件结果保留。
- sampled worst-envelope HV 明确是 sample-dependent diagnostic；VI-6.2 已删除 “not specialized/degrade gracefully”的过强结论。
- disjoint scoring 被准确称为 direct-reuse leakage control，而不是普遍的 leakage-proof certification。
- 六网络 AC 层明确是 fixed composition mapping，matched-repair NSGA-II 略高的不利结果得到保留。

### 残余项（Minor）

Conclusion 的 `Screening reduces objective calls but not mean hypervolume`略像等效结论。建议最终排版时改为：

> Screening reduces recorded objective calls; no mean-hypervolume difference is detected, and equivalence is not established.

同段的 NoOutage AC 差异建议保留 `under the fixed composition mapping`。

### 最终创新边界

可声称：选择性场景暴露、可复算的 65% 调用计数下降、搜索/评分 draw 隔离、sampled worst-envelope diagnostics。  
不可声称：动态重筛优于固定 worst-K、筛选提升 HV、真实 tail robustness、AC superiority。

---

## 6. P5：TRACE-MOEA

### 判定：PASS

### 终审核对

- 三个确定性 ranking rules 的 30 个重复 invocations 明确只为 rectangular provenance，有效样本量为 1，不进入 U tests。
- Abstract/Contribution/Results/Conclusion 统一为 24/28 stochastic-baseline significant wins 和 21 deterministic descriptive gaps。
- NoPreferenceRanking pooled difference 仅 0.17%，跨场景 correction 后 unresolved；这一负结果贯穿摘要、贡献、结果、讨论、限制和结论。
- preference-emphasized scenarios 上对 NSGA-II 的胜利没有再被错误归因于 preference layer。
- archive quarantine 只证明 trace variables 不进入 metric/selection；正文明确不代表零计算或人工成本。
- 98.6% 被定义为 event coverage/software completeness，不是 explanation quality 或 human usefulness。
- NERC/MTEP 被统一降为 descriptive external consistency；项目依赖、construct overlap、98% build base rate 和 19 withdrawals 均已披露。

### 残余项（Minor）

Abstract 的 `archive provides audit evidence`可进一步精确为 `archive provides event provenance for audit`，避免被理解为已验证审计有效性。

标题含 `Investment-Effectiveness Review`，但正文已经稳定使用 proxy benchmark。cover letter 不得延伸为真实经济效果或已验证 human-review performance。

### 最终创新边界

可声称：偏好事件、repair drops 的 metric-quarantined provenance；相对测试随机基线的 proxy HV；偏好层优化作用未决。  
不可声称：偏好适应产生显著总体增益、trace improves reviewer decisions、外部记录证明 above-chance portfolio validity。

---

## 7. P6：BiLo-NSGA

### 判定：PASS

### 终审核对

- `forward-dominant` 在 Abstract、Introduction、VI-6.3、Discussion、Conclusion 中含义一致：resolved operator gains 出现在 forward side，不等于 pooled mean 提升。
- NoForward pooled mean 高于 full、full 只在 primary family 的 3/8 场景显著胜，均未隐藏。
- NoBackward pooled +0.61%、LegacyDeletion pooled +0.22%、全部场景 unresolved，atomic substitution 明确没有 accuracy gain。
- forward-only 被列为无需 replacement audit semantic 时的 lean configuration；full 只为记录 atomic remove–insert pair。
- 1600-neighbor PLS 只匹配 nominal evaluation ceiling，不宣称等 computational work；runtime 同时报告。
- AHP-TOPSIS/Greedy BCR 的确定性重复已从推断移除，36/40 stochastic wins 与 16 descriptive gaps 口径贯穿全文。
- 预算 multiplier 与 scalar weights 同时变化，已被降为 cross-scenario diagnostic，不作 slack causality。
- NERC/MTEP 只称 descriptive external consistency，不再声称 confirmatory review validity。

### 残余项（Minor）

Contribution 1 的 99.6% coverage 应继续理解为 logged-event coverage。Highlights 中不要把它压缩成 “99.6% explainability”。

`atomic substitution is more faithful/reviewable`仍是设计语义判断，没有 human study；当前正文已经清楚说明，可保留但不得升级为 improved audit outcomes。

### 最终创新边界

可声称：项目词汇局部移动、部分场景的 forward-side resolved gains、atomic replacement provenance、相对测试基线的 proxy HV。  
不可声称：forward search 普遍提升 pooled HV、bidirectional/substitution accuracy gain、历史结果证明真实 review quality。

---

## 8. 六篇终审一致性检查

### 通过项

1. **创新身份：** 每篇均能用一句不依赖“所有组件有效”的话说明贡献。
2. **理论动机：** 机制解释均区分设计动机、实验关联和因果证明。
3. **负消融：** P1 retrieval day-ahead harm、P2 geometry unresolved、P3 adaptation null、P4 dynamic/hybrid null、P5 preference null、P6 substitution null 均未被埋藏。
4. **统计单位：** 确定性规则与随机 seeds 已分离；主胜场数字在摘要、贡献、结果和结论一致。
5. **代理/物理边界：** proxy optimization 与 AC mapping 不再互相替代。
6. **外部一致性：** rule backtest、historical outcomes 与 expert/human validity 已分层。
7. **companion-paper 分离：** P3/P4 与 P5/P6 均声明共享候选生成或公开语料，但算法、目标、场景、run archive、selected portfolios 和 claims 分离。

### 非理论性提交提醒

部分稿件仍存在 `[AUTHOR INPUT REQUIRED]`、基金、ORCID、通讯信息和字符编码等制作事项。它们不影响本轮 PASS，但在正式投稿包 gate 中必须清零。

## 9. 最终判定

**六篇在“理论基础与创新边界”维度全部 PASS。** 当前不需要为了创新性再后验调参、制造正消融或机械增加公式/框图。剩余工作应集中于少量措辞一致性、作者与基金元数据、引用/编码以及最终 PDF 与证据包核验。
