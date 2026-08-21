# 第一轮独立评审：理论基础、创新性与期刊适配（P1–P6）

**评审角色：** 理论基础与创新性审稿人  
**评审日期：** 2026-08-12  
**证据范围：** 六篇最新版 `MANUSCRIPT.md`，并参照 `COMPREHENSIVE_SIX_PAPER_VS_10_REPORT_ZH.md`。本轮不改正文、不重算数据，不把外部领域惯例当作已核实事实。  
**判定原则：** 重点检查“创新主张—数学定义—对照实验—统计结论”是否闭合。图、公式只在帮助复现或解释因果链时建议增加，不按数量机械补齐。

## 一、总评

| 论文 | 目标期刊 | 当前最可辩护的创新 | 第一轮结论 | 最关键问题 |
|---|---|---|---|---|
| P1 DSTAR-GRU | IEEE Access | 方法无关的稀疏弃电风险基准、onset slice、检索机制随预测尺度反向变化 | **大修** | 目标是参考政策生成的代理量而非实测弃电；跨系统冻结审计为全零，方法结论只在单一 cap/单一系统成立 |
| P2 CSA-LoadNet | Electronics | 对“是否聚合”与“如何加权”做可分离、带负结果的组件审计 | **大修（接近小修）** | 唯一显著正结果仅在 OPSD-24 h；其余强基线曾只跑 3 seeds，且结论是结果后收窄，创新外推面很窄 |
| P3 CARS-MODE | Energies | 约束多目标 DE 的完整实现、直接 MO-DE 对照及代理优化—AC 验证分层 | **大修** | 标题核心“strategy-adaptive”在 HV 上无增益；AC 层不支持当前关于自适应机制的因果解释 |
| P4 SHIELD-MOEA | Energies | 搜索/评估场景隔离、worst-K 筛选的调用节约、六网络 AC 边界验证 | **大修** | 调用量数学定义与 17,920 的实现计数不一致；动态重筛与固定 worst-K 不可区分 |
| P5 TRACE-MOEA | Energies | 隔离于优化指标的决策轨迹归档、代理—规则—历史结果三层审计 | **大修** | 确定性基线的 30 次相同输出被纳入种子检验，存在伪重复；偏好层增益极弱且轨迹的人因价值未验证 |
| P6 BiLo-NSGA | Applied Sciences | 项目语义局部移动、预算恢复和逐移动审计；对前向/替换负结果如实分离 | **大修** | 确定性基线同样存在伪重复风险；前向消融的 pooled mean 更好，替换完全无精度证据，必须保持“局部有效”而非整体归因 |

六篇稿件的共同优点是：不再把所有组件都写成正贡献，直接基线、消融、外部一致性和不利结果多数已进入摘要或结论。共同风险则是把“系统设计贡献”写成“性能机制贡献”，以及把重复算法随机种子当成唯一的不确定性来源。第一轮不建议继续堆叠框图；应先修正统计单位、数学计数和因果措辞。

---

## 二、P1：DSTAR-GRU / Curtailment-Risk Benchmark

### 结论

**大修。** 稿件作为“基准与机制边界研究”有明确价值，但不应按预测 SOTA 论文包装。当前标题、摘要最后一句和引言第 39–46 行的自我定位基本正确；主要缺口是代理目标的构念有效性与跨政策稳健性。

### 已被证据支持的创新

1. 方法独立地先生成目标，再训练所有方法，修复了旧版本 proposed-method-exclusive bias；这是可复核的基准设计贡献（III-A、III-F）。
2. onset slice 揭示了总体 MAE 与事件预警的冲突；SmallBank 的最低 24 h MAE与 F1=0 是有价值的反例（VI-A）。
3. 1 h 与 24 h 的检索作用方向相反，并有单开关消融和 Holm 校正支持；该主张比“DSTAR-GRU 更准确”更有创新价值（VI-C）。

### Major 1：弃电标签是参考 cap 的代数代理，不是观测到的弃电决策

**证据：** Abstract/III-A 将 RTS-GMLC 的 day-ahead load 与 renewable series 经 70% SNSP-type cap 转换为标签；III-E 明确 cap=0.70 是 benchmark parameter；NREL-118 冻结 cap 审计没有正样本。  
**问题：** 当前贡献可证明“在该参考政策下预测所构造的风险量”，不能证明预测真实调度弃电。单独做 0.60/0.70/0.80 的标签稀疏度表，不等于证明检索符号反转对 cap 稳健。  
**必须修改：** 将全文首次出现的 target 统一称为 **reference-policy curtailment-risk proxy/target**；在摘要中把 “curtailment-rate target” 改为 “reference-policy proxy target”。若不新增实验，删除任何容易被读成实测弃电的措辞。

**建议替换句：**

> We construct a reproducible reference-policy curtailment-risk proxy from RTS-GMLC trajectories; it is not an observed dispatch curtailment record. All method-level conclusions are conditional on the 70% cap and the RTS-GMLC operating year.

### Major 2：跨系统审计是可迁移性反证，不是外部验证

**证据：** Abstract 报告 NREL-118 在冻结 cap 下无正目标小时；III-E 又明确未测试其他 cap 下的方法排序。  
**处理：** 保留该负结果，但把它放在“task-definition stress test”而非 external validation。投稿主张应限定为“公开单系统 benchmark prototype”。若要升级外部有效性，最有价值的补实验不是再加一个框图，而是在预先声明的新 cap 校准规则下，对第二系统重新生成非退化标签并完整复跑至少 persistence、ridge、TCN、DSTAR-GRU、NoRetrievalBank、NoSiamese；否则不要提出 transfer claim。

### Minor

- III-C 已定义 onset MAE/F1，但需要一句说明阈值校准与 onset 标签使用的时间信息完全隔离，避免读者误解 target-time 信息参与阈值选择。
- III-D 对确定性方法只作点估计、未做种子显著性比较是正确方向；表中应显式标注 “deterministic; no seed-level test”，不要用视觉星号暗示与随机方法等价的推断强度。
- 当前 8 幅图已足够。只建议在 Figure 1 或补充材料增加一张 **标签构造 DAG/数据流**，明确真实输入、政策参数、代理标签、训练预测之间的方向；无需再加算法装饰图。

### 期刊适配

IEEE Access 可接纳可复现系统/基准型贡献，但稿件价值来自透明失败与公开资产，而非算法领先。建议投稿身份写成 **benchmark and mechanism-audit study**。

---

## 三、P2：CSA-LoadNet

### 结论

**大修（若完成主张校准，可接近小修）。** 数学结构、层次一致性与实验链条已经基本闭合；最大风险不是公式不足，而是标题覆盖面大于唯一正结果的覆盖面。

### 已被证据支持的创新

1. OPSD 24 h 上 full model 相对 MLP 和 TemporalOnly 的显著优势，分别支撑“在该设置下具有竞争力”和“聚合本身有贡献”。
2. Poincaré、Euclidean、equal-weight、fixed curvature 全部不可区分，构成对复杂几何权重必要性的有价值负证据。
3. Ausgrid 精确层次重建和四种 reconciliation 把准确性与 coherence 分开，且明确承认 DLinear 胜出。

### Major 1：把单一正单元格写成局部组件发现，不写成通用模型创新

**证据：** VI/Limitations 显示五个数据集—horizon 设置中，只有 OPSD-24 h 对 MLP 和 no-aggregation 为显著正结果；OPSD-1 h 显著负，SimBench 未分离，Ausgrid 输给 DLinear。  
**问题：** “Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region…”尚可，但 Abstract/Conclusion 的 “strongest of five neural baselines” 容易掩盖：除 MLP 外的 OPSD/SimBench 外部神经基线来自早期 3-seed v6，而决策集推断主要是 10-seed v7。  
**必须修改：** 主结论写成 “beats the ten-seed MLP comparator and the no-aggregation ablation on OPSD-24 h”；其余 3-seed模型仅作支持性排序，不合并成同等强度的“five-baseline significance”印象。

**建议替换句：**

> The supported result is setting-specific: cross-series aggregation improves OPSD day-ahead accuracy relative to the ten-seed MLP comparator and the matched no-aggregation ablation. The study does not establish general superiority across horizons, datasets, or neural baseline families.

### Major 2：后验收窄需与验证性语言分离

**证据：** Discussion 7.1 明确承认 v7 结果后发生 claim downgrade and renaming，且无 preregistration。  
**处理：** 保留版本史，但将“prespecified comparisons”与“post-hoc surviving claim set”明确分开。可以说检验族预先固定，不能说最终创新假设被预注册。该修改不需要重跑实验。

### Minor

- 使用相同种子时，当前 Mann–Whitney 是保守的非配对检验；建议补充 seed-paired effect interval（不必替换主检验），提高效应量解释。
- `Poincaré` 等字符在当前 Markdown 显示为乱码，投稿前必须做 UTF-8/LaTeX 编码审计；这是制作问题而非理论问题。
- 不需要增加新框图。现有 8 幅图能覆盖架构、显著性矩阵、层次结构和结果。若加图，唯一有价值的是 rolling-origin/不同天气年效应图；否则保持现状。

### 期刊适配

Electronics 的算法应用与负结果审计方向匹配。稿件应突出 **component-level empirical audit of cross-series aggregation**，弱化“新注意力几何”。

---

## 四、P3：CARS-MODE

### 结论

**大修。** 直接 GDE3/NSDE 控制已显著增强框架级比较，但“strategy-adaptive”这一命名中心未获得代理 HV 的组件证据，AC 层也不足以建立其因果机制。

### 已被证据支持的创新

1. CARS-MODE 在七个代理规划场景中显著超过 GDE3 与 NSDE，直接补上了“DE 对 DE”的 comparator gap（VI-6.6）。
2. 预算 repair 与 crowding diversity 是可归因的 load-bearing components。
3. 将代理 HV 与 pandapower AC feasibility 分层，并主动报告代理冠军物理上只居中，是良好的规划论文方法论贡献。

### Major 1：自适应策略不是已证实的性能来源

**证据：** FixedDE pooled HV 比 full 高 0.60%，各场景均不显著；Conclusion 已承认 adaptation is proxy-neutral。  
**问题：** 题名 CARS-MODE 和 Discussion 的“adaptive component is associated with more favorable electrical behavior”仍容易让读者把框架胜利归因于 adaptation。  
**处理：** 保留算法名可以，但在 Abstract/Introduction 第一次出现时明确 “strategy adaptation is a design feature, not the source of the demonstrated HV gain”。贡献列表把“自适应机制”降为被审计对象，把直接 MO-DE 优势、repair/diversity 和 proxy-to-AC gap 放在前面。

### Major 2：AC 层不能支撑当前自适应因果解释

**证据：** V-5.4 只取三个实验的 seed-0 compromise plan，先压缩为 action counts，再用固定规则映射到四个网络；每方法 72 个 deterministic cases，正文承认不作显著性检验。Discussion 又解释 FixedDE 多一个 storage 导致过电压并称 adaptation 避免过度专化。  
**问题：** 这是 composition + mapping 的相关解释，不是策略自适应的随机化因果证据；单个 compromise plan 也不能代表 30-seed front 分布。  
**必须修改：** 将该段降格为 hypothesis，并删除 “shows the component’s real function” 一类确定性表述。

**建议替换句：**

> The AC composition check is consistent with, but does not identify, a beneficial role for adaptation. Because one compromise plan per scenario is mapped by deterministic placement rules, the observed feasibility difference may arise from plan selection or mapping as well as from the adaptive controller.

### Major 3：确定性 Weighted Sum 的显著性单位需单独处理

若 Weighted Sum 在每个场景生成完全相同的组合，则把同一输出复制 30 次后与 30 个随机种子做 Mann–Whitney 会构成伪重复。请核对 run archive：若方差为零且输入也未随 seed 变化，则该比较只能作为描述性差异，不能进入“n=30 per group”的显著胜场计数。对随机算法的 30-seed检验可保留。

### Minor

- 参数敏感性采用 10 seeds 且每点单独对 NSGA-II；应报告效应区间，并避免把 p 值当稳定性大小。
- AC 图已达到 9 幅，无需增加。最有价值的新增是多 seed compromise 或 front-sampled AC 分布，而不是新算法框图。
- “robust proxy optimizer”中的 robust 应限定为 tested scenarios/parameter sweep，避免被理解为鲁棒优化理论保证。

### 期刊适配

Energies 适配良好，但必须把论文身份从“改进型自适应 DE”调整为 **constrained MO-DE framework with an audited adaptation null result and physical-validation boundary**。

---

## 五、P4：SHIELD-MOEA

### 结论

**大修。** 六篇中应用证据最完整之一，且负组件结果披露充分；但场景调用量的数学闭合存在可复核的算术/符号冲突，必须在投稿前修正。

### 已被证据支持的创新

1. 搜索场景与认证场景使用不相交 seeds，并另设 unseen-stress ranges；这是清晰的防评估泄漏设计。
2. worst-K 筛选在不改变已测 front quality 的情况下减少场景目标调用；该贡献是 evaluation economy，而非精度提升。
3. 六网络、1296 AC cases 保留了 matched-repair NSGA-II 略优的不利结果，并能识别 outage-aware exposure 的 composition-level 物理差异。

### Major 1：17,920 次调用与公式不闭合

**证据：** IV 中给出的实现算式是 `80×4×40 + 8×40×16 = 17,920`；但紧邻公式写成 `N_p K G + N_p |S| N_screen`，且算法参数又称 population=40、每代 40 offspring。若 $N_p=40$，公式给出 11,520；若 $N_p=80$，第二项又应为 10,240。  
**问题：** 当前同一符号同时承担“搜索时被评分的 parent+offspring 数”和“screening 时当前 population 数”，导致 65% 节约无法由正式定义复算。  
**必须修改：** 分别定义 $N_{eval}$ 与 $N_{screen,pop}$，逐项写出初始化、每代父/子评估是否缓存、8 次 full-screen 是否复用当前目标值。用实际代码计数器核对后只保留一个数值。现有 65% 在闭合前不得作为 headline。

**建议公式模板：**

> (C_{mathrm{screen}}=G,N_{mathrm{active}}K+N_{mathrm{round}}N_{mathrm{pop}}|mathcal S|+C_{mathrm{init}}), where each term corresponds to a non-overlapping set of objective calls recorded by the implementation counter.

### Major 2：动态重筛不是已证实创新来源

**证据：** full 与 generation-1 fixed worst-K 在 8/8 场景不可区分；full 与 DE-only 同样 8/8 不可区分。  
**处理：** 把方法论贡献写为 **selective hard-scenario exposure plus disjoint certification**，不要写 periodic adaptation improves search。标题中的 “scenario-hardened/evaluative lookahead”可保留，但 Introduction contribution 2 的 “adaptive”应附 null result。

### Major 3：AC 差异不是 seeded causal estimate

NoOutage 0.574 vs full 0.685 是重要的物理一致性证据，但每方法 108 个 cases 由固定 composition mapping 产生，case 之间也共享网络与方案。继续称 composition-level check 是正确的；不得将 108 当作独立重复做显著性推断。

### Minor

- worst-case hypervolume 的计算需要在正文明确是逐场景 objective aggregation 后再算 HV，还是各场景 HV 的最小值；当前文字不足以排除两种解释。
- MOEA/D collapse 已正确限定为配置特异；主表视觉上应避免让这个极弱配置放大 full 的整体胜场数量。
- 9 幅图已经充分。修复调用计数后可在现有 Figure 4/7 加一个 objective-call panel，无需新增装饰性框图。

### 期刊适配

Energies 高度匹配。只要修正计数闭合并进一步弱化“dynamic”必要性，稿件的泄漏控制与物理边界具备明确应用价值。

---

## 六、P5：TRACE-MOEA

### 结论

**大修。** 轨迹 quarantine 是清晰的系统设计创新，外部效度梯子也比单纯 proxy benchmark 更成熟；但当前统计协议对确定性基线的处理可能使“45 significant wins”失真，这是投稿前必须清理的硬问题。

### 已被证据支持的创新

1. 归档状态通过单向写入与优化状态隔离，正文还明确 `⊥` 是实现不变量而非概率独立；理论表述基本闭合。
2. R-NSGA-II 直接偏好族对照和三预算扫描补齐了近期 baseline 价值问题。
3. NERC rule 与 MTEP16 outcomes 被限定为 weak-form alignment，且承认 AHP-TOPSIS/Weighted Sum 在部分外部视图更强。

### Major 1：确定性基线 30 次复制构成伪重复风险

**证据：** V-5.2 明确说 AHP-TOPSIS、Weighted Sum、Greedy BCR 等每场景产生完全相同的单一 portfolio、方差为零；随后又对所有 15 个 opponents 使用每组 n=30 的 Mann–Whitney。  
**问题：** 如果 30 行只是同一确定性输出的复制，而 candidate pool/reference sample/evaluation 也未随 seed 重采样，那么有效样本量是 1，不是 30。复制会人为制造极小 p 值，并污染“45 Holm-significant wins”。  
**必须修改：**

- 对随机算法/随机搜索继续使用 30-seed分布；
- 对确定性方法只报告效应差和 rank，不作 seed-level U test；或引入真正独立的问题实例/候选池 bootstrap 后再推断；
- 重算 49 次 baseline comparison 中的显著胜场数，摘要、引言、结果、结论同步更新。

### Major 2：偏好适应的价值应与总体框架价值分开

**证据：** NoPreferenceRanking 只损失 0.17% pooled HV，仅 1/7 场景显著且没有 p<0.01；偏好层主要增加 preference-elite trace。  
**处理：** 题名中的 preference-adaptive 可作为功能描述保留，但不能暗示它解释 +0.89% 对 NSGA-II 的总体差异。将贡献写成“preference-adaptive layer is audited and conditionally useful; repair-equipped kernel carries most measured quality”。

### Major 3：“zero metric cost”措辞不准确

Quarantine 能证明 archive **does not enter the metric**，不能证明产生 archive 没有计算、内存或维护成本，也不能证明没有机会成本。改为：

> The archive is metric-quarantined: its contents cannot improve the reported objective values by construction. Its computational and human-interpretation costs are reported separately and are not claimed to be zero.

### Minor

- 98.6% coverage 是软件覆盖率，不是解释充分性；正文已承认，建议摘要也用 “event coverage”而不是泛称 audit evidence。
- broad MTEP label 把 unresolved 当 negative，strict 又只有 19 withdrawals；两者应并列呈现，不能只把 broad p 值放摘要而省略 outcome-definition sensitivity。
- 8 幅图已足够。若新增证据，应优先做人类评审可用性/一致性实验；再生成框图不会弥补人因有效性缺口。

### 期刊适配

Energies 可接受面向投资评审的代理研究，但题目中的 investment-effectiveness 容易被理解为真实经济效果。建议全文稳定使用 **proxy investment-effectiveness review**，直到成本标定和专家标签完成。

---

## 七、P6：BiLo-NSGA

### 结论

**大修。** 最新标题加入 “Forward-Dominant”并在摘要明确否定 bidirectionality/substitution accuracy gain，方向正确；主要剩余问题是统计单位和局部搜索组件的价值边界。

### 已被证据支持的创新

1. 把 add/substitute/repair 定义为项目级、可审计移动，并给出逐移动 archive 与复杂度表达，数学定义较完整。
2. 加入 1600-neighbor Pareto Local Search，直接回答“是否只比通用 MOEA”的 comparator gap；8/8 场景显著更高。
3. budget scan、NoForward、NoBackward、LegacyDeletion 共同把“前向局部有效、替换无精度证据”说清楚。

### Major 1：确定性基线的 n=30 问题必须核查并重算

**证据：** V-5.2 声称 18 methods 全部 30 independent runs，V-5.3 又统一按 n=30 per group 检验；Greedy BCR 与 AHP-TOPSIS 按描述是确定性 ranking/fill。  
**问题：** 若它们的 30 行完全相同，则与 P5 相同，不能作为 30 个独立重复。  
**处理：** 分离 stochastic-versus-stochastic inference 与 deterministic comparator descriptive ranking，重算 “52 significant wins among 56”。Random Feasible 若每 seed 真正改变 permutation，可保留随机检验。

### Major 2：“forward-dominant”只能表示显著单元来源，不能表示 pooled 改进

**证据：** NoForward pooled mean 0.17257 高于 full 0.17190；full 只在 3/8 场景显著胜，其他 5 场景不显著。  
**处理：** 当前 VI-6.3 的定义是正确的，应复制到摘要首次使用处：forward-dominant means all statistically resolved operator gains occur on the forward side, not that forward search improves pooled performance。不要用 budget sensitivity 的跨场景趋势作为前向机制的因果证明，正文已经承认场景同时有其他差异。

### Major 3：atomic substitution 是审计语义，不是算法精度创新

**证据：** NoBackward pooled +0.61%，LegacyDeletion pooled +0.22%，8/8 均无显著差异；移除 substitution 还降低约 26% runtime。  
**处理：** Full version 与 lean forward-only configuration 应在 Discussion 明确形成部署选择：需要替换审计记录时用 full，只关心 HV/成本时用 lean。题名没有再用 bidirectional 是正确的。结论不得把 atomic substitution 列为性能贡献。

### Major 4：外部结果仍不足以称 review validity

MTEP broad capture 1.071、r=0.088 虽显著但效应小，strict label 只有 19 withdrawals；NERC rule 又有构念重叠。当前 weak-form consistency 表述应保持。Applied Sciences 版本还必须完成作者、基金、数据可得性等投稿字段；这些是提交完整性问题，不是科学创新。

### Minor

- PLS 的“1600 neighbor evaluations equals 40×40 budget”只匹配调用数，不匹配每次操作成本；应同时保留 runtime，避免称完全等算力。
- 复杂度式已说明双向不等收益，足够；无需再加定理。若需要增强理论基础，可给出 feasibility recovery termination 的一句有限步证明，但不要包装成新理论贡献。
- 9 幅图已经充分，Figure 9 已承担直接局部搜索/替换控制；无需再生成算法框图。

### 期刊适配

Applied Sciences 与应用型算法、公开 benchmark 和审计性主题匹配。可发表价值来自“项目语义搜索 + 透明边界”，不是 1.12% pooled HV 本身。

---

## 八、跨论文必须优先执行的修改顺序

1. **先修统计单位。** 核查 P3/P5/P6 所有 deterministic methods 的 per-seed 方差和输入是否真正变化；对复制行取消推断检验，重算摘要胜场。
2. **再修数学闭合。** 用代码计数器核对 P4 的 scenario-call 公式与 17,920/65%；在闭合前暂停效率 headline。
3. **统一机制归因。** P3 adaptation、P4 dynamic screening、P5 preference adaptation、P6 substitution 均应从“性能来源”降为“设计组件/受审计机制”，除非单开关实验显著支持。
4. **统一外部有效性阶梯。** proxy consistency、composition-level AC、historical alignment、expert/human validity 四层不得混写；没有专家标签的 P5/P6 不得声称真实 review effectiveness。
5. **最后再做版式。** 六篇当前图数与公式数均已够用。新增图只服务于标签构造、统计不确定性或外部验证；不建议为了期刊观感机械增加框图。

## 九、第一轮给总智能体的可执行决定

- **可直接文字修正，不需新实验：** P1 代理标签命名；P2 10-seed 与 3-seed证据分层；P3 AC 因果措辞；P4 dynamic null；P5 metric-quarantined 替代 zero cost；P6 forward-dominant 的严格定义。
- **必须重算/核对后才能改结论：** P3/P5/P6 deterministic comparator 的显著性计数；P4 objective-call 实现计数。
- **可选但高价值的新实验：** P1 第二系统非退化 cap 的完整方法复跑；P2 rolling-origin/weather-year replication；P3 多 seed/front-sampled AC validation；P5/P6 小规模真实专家排序及一致性。未完成这些实验时，以降格主张代替补造证据。

**第一轮总体判定：六篇均不建议按当前文本直接投稿；先完成上述硬修，再进入第二轮“统计与实验审稿”。**
