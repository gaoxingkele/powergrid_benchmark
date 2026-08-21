# 第二轮方法学与统计复审：P1--P6

日期：2026-08-12  
角色：方法学与统计审稿人  
范围：六篇当前 `MANUSCRIPT.md`、`statistical_audit_v2/`、审计生成脚本及对应 v2 证据表。  
边界：本轮只读核验；未修改主稿、实验档案或证据 CSV。

## 1. 总体结论

| 论文 | 本轮总评 | 投稿前状态 | 最关键原因 |
|---|---|---|---|
| P1 DSTAR-GRU | **MAJOR** | 需统计报告修订 | 配对“精确”检验实现有系统性偏差；主分析效应量/区间仍不完整；另有方法总数和图注范围错误 |
| P2 CSA-LoadNet | **BLOCKER** | 暂不可提交 | 引言仍使用已废弃层级的 Ausgrid p 值；配对审计修正后有一项显著性判定改变 |
| P3 CARS-MODE | **MAJOR** | 需统计报告修订 | 核心随机/确定性处理已正确，但参数扫描的多重性族和完整效应量报告不足 |
| P4 SHIELD-MOEA | **BLOCKER** | 暂不可提交 | 引言仍称 40/40，而当前合法随机基线族是 32/32；最坏情形段落仍跨不同归一化列比较并作过强推断 |
| P5 TRACE-MOEA | **MINOR** | 小修后可进入下一轮 | 核心统计已基本修复；需明确 bootstrap CI 为未校正、逐比较区间，并继续把外部回测限定为描述性 |
| P6 BiLo-NSGA | **BLOCKER** | 暂不可提交 | 外部回测正文声称超过七个外部基线，但表中 AHP-TOPSIS 明确更高；“独立于特征化”表述也与 `appendix_status` 的预后相关性冲突 |

六篇稿件均已正确区分多数确定性方法的有效样本量为 1 与随机方法的 30 个种子，P3--P6 的主 Holm 族计数现与 `STATISTICAL_AUDIT_V2.md` 一致：P3 为 56/55/0，P4 为 32/32/0，P5 为 28/24/0，P6 为 40/36/0（比较数/显著胜/显著负）。这一轮没有发现需要重新运行全部优化实验的证据；需要重跑的是统计审计脚本及其派生表，而不是核心方法运行档案。

## 2. 跨论文统计审计发现

### 2.1 BLOCKER：`exact_signflip_p` 并非真正的精确穷举 p 值

证据锚点：`scripts/mintou/build_statistical_audit_v2.py:49--56`。

脚本已经穷举全部 (2^n) 个符号排列，却返回

\[
p=\frac{b+1}{2^n+1},
\]

其中 (b) 是不弱于观测统计量的排列数。“+1”修正适用于随机抽取有限置换时的保守估计，不应再用于完整穷举。完整穷举的精确双侧随机化 p 值应为 (b/2^n)。例如 (n=10)、全部差值同向时，当前值为 (3/1025=0.002926829)，精确值应为 (2/1024=0.001953125)。

只读复算显示：

- P1 的配对敏感性数值会改变，但当前报告的显著/未显著判定不变。
- P2 的 OPSD 1 h、CSA-LoadNet 对 MLP：原始精确 p 应由 (9/1025=0.00878049) 改为 (8/1024=0.0078125)；六项 Holm 族的校正值由 0.0526829 改为 **0.046875**，判定由未解决变为显著。
- P2 的 OPSD 24 h 两个全同向对比，六项族校正值应由 0.017561 改为约 **0.011719**；Ausgrid CSA-LoadNet 对 DLinear 的十项族校正值应由 0.029268 改为约 **0.019531**。这些判定方向不变。

要求：删除穷举后的“+1”修正，增加 n 很小的解析回归测试，重新生成 P1/P2 配对 CSV、证据副本和所有引用配对 p 值的正文。主分析仍可保持 Mann--Whitney U，不应把修正后的配对敏感性改写为预注册主分析。

### 2.2 MAJOR：`paired_rank_biserial_sign` 不是通常意义的 Wilcoxon 配对秩二列相关

证据锚点：`scripts/mintou/build_statistical_audit_v2.py:59--63`。

实现是非零差值的符号平衡 ((n_+-n_-)/n)，没有使用差值绝对值的秩。因此 CSV 的列名含 `_sign` 尚算谨慎，但函数名 `paired_rank_biserial` 容易被误读为 Wilcoxon matched-pairs rank-biserial effect。要求二选一：

1. 将函数及报告名称改为 `paired_sign_balance`，并给出定义；或
2. 真正计算配对秩二列相关，并说明零差值处理。

不得把当前值称为一般的“paired rank-biserial correlation”。

### 2.3 MAJOR：bootstrap CI 与 Holm 检验不是同一推断对象

`STATISTICAL_AUDIT_V2.md:4` 说明区间来自固定种子 20260812 的 5000 次均值差 bootstrap。它们是逐比较、未作同时覆盖校正的均值差区间；Holm 校正的是基于秩的 Mann--Whitney p 值。因估计量、检验统计量和多重性处理不同，可能出现 CI 不跨零而 Holm p 不显著的情况。这不必然是计算错误，但每篇稿件首次出现区间时必须明确写成“pointwise, multiplicity-unadjusted 95% bootstrap CI for the mean difference”，并以 Holm p 值作为预先声明的显著性判定。

### 2.4 MAJOR：跨场景消融族与场景内族必须同时命名

`p3_...p6_critical_ablation_cross_scenario.csv` 已提供第二个、跨场景 Holm 族。稿件应区分：

- 主分析：每个场景内“完整方法对随机对手”的 Holm 族；
- 补充分析：同一关键消融跨全部场景的第二个 Holm 族。

两者不可择优引用。典型例子是 P4 的 NoOutage：场景内校正下 outage-contingency 为 0.0323、restoration-aware 为 0.00910；跨八场景再次校正后分别为 **0.0753（未显著）**与 **0.0243（显著）**。因此“恰好两个实验显著”只能明确限定为场景内主族，不能作为跨场景的组件结论。

## 3. 逐篇复审

## P1 — DSTAR-GRU

**总评：MAJOR。** 样本单位与确定性方法处理已经明显改善：随机方法每设置十个种子；Persistence、Seasonal、Ridge、raw-feature kNN 只作单点描述；每个预测时距的主 Holm 族为 3 个指标 × 9 个随机对手 = 27 项（`MANUSCRIPT.md:131`）。主分析和后冻结配对敏感性也已清楚分层。

### BLOCKER

- 无独立的主结果 blocker；但跨论文的精确符号翻转实现必须修复后才能冻结最终版配对数字。

### MAJOR

1. 配对 p 值来自上述非精确实现。即使 P1 判定不变，也不能继续称现有数值为 exact。
2. 主 Mann--Whitney 家族主要报告 Holm p 值，尚未为关键比较系统报告预声明的 rank-biserial effect 和区间。正文只给若干配对均值差 CI（`MANUSCRIPT.md:335--337`），不足以替代主分析的效应量报告。
3. 年度时间序列被压缩为模型种子间变异；CI 不覆盖测试年份/事件块抽样的不确定性。稿件结论已限定为固定测试年和 seed variability（`MANUSCRIPT.md:430`），因此可保留为限制，但不得把区间解释为跨年份或跨事件泛化区间。

### MINOR

1. `MANUSCRIPT.md:279` 称 SmallBank 是“all twelve methods”中最好，但表述上下文的排行榜是 14 个方法（同段也报告 rank 8/14）。改为 14。
2. Figure 4 图注 `MANUSCRIPT.md:343` 称胜过“every retrieval-free or retrieval-degraded opponent”，但 TCN 也是无检索模型且主分析未解决。应限定为“displayed prespecified removal/degradation controls”，不要涵盖 TCN。

## P2 — CSA-LoadNet

**总评：BLOCKER。** 方法公平性和层级重建较上一版显著改善：Ausgrid 17 节点精确层级、11 个模型统一十种子、同一 OLS 变换下比较，且初步三种子筛选与十种子确认已明确区分。

### BLOCKER

1. `MANUSCRIPT.md:52` 仍写“Ausgrid 对 DLinear，Holm p=0.0044”，这是已经废弃的旧层级结果；当前精确层级正文 `MANUSCRIPT.md:375` 的主分析为 **0.000985**。同一稿件同时使用新旧层级数字，必须删除旧值并全稿搜索旧层级遗留。
2. 修正精确符号翻转实现后，OPSD 1 h 对 MLP 的配对敏感性由 0.052683 变为 **0.046875**，跨越 0.05。必须重新生成表、正文和结论措辞；同时继续标注它只是后冻结敏感性，不能覆盖主 MWU 结论。

### MAJOR

1. 当前正文的 OPSD 24 h paired Holm p=0.0176（`MANUSCRIPT.md:323`）和 Ausgrid paired Holm p=0.0293（`MANUSCRIPT.md:375`）也受同一实现问题影响，应整体重算，不能只改跨阈值的一行。
2. 配对敏感性族大小需明确：OPSD/SimBench 每个数据集-时距块的族及 Ausgrid 十项族应在统计方法或表注中列出。当前读者无法从正文直接判断 0.0293 是在五项还是十项族中得到。
3. 主分析的 rank-biserial effect 与区间仍不完整；精选 paired mean-difference CI 不能替代主分析效应量。

### MINOR

- `MANUSCRIPT.md:391` 的 Figure 6 误差棒是匹配种子相对变化的标准差，不是 CI；正文已说明，但图内/图注应避免让它看起来像显著性误差棒。

## P3 — CARS-MODE

**总评：MAJOR。** 确定性伪重复已正确移除：Weighted Sum 的七个差距为描述性；56 个随机基线比较中 55 个显著且无显著负向结果，与 v2 审计一致。Table 6 的 NSGA-II 效应、均值差 CI、rank-biserial 和当前 Holm p 也与证据表一致。FixedDE 的负消融结果和 AC 组合层的非因果定位均处理得较诚实。

### BLOCKER

- 无。

### MAJOR

1. 参数敏感性表 `MANUSCRIPT.md:445--460` 报告六个 MWU 原始 p 值并据此称“significant throughout”，但没有声明或校正这一六项家族。即使按 Holm 复算预计不会改变这些判定，也必须预先声明族、给校正 p 值，或把整段明确降为探索性并删除总体显著性断言。
2. v2 表含完整 56 项效应量和 pointwise CI，正文只展示对 NSGA-II 的精选结果。至少应在补充材料中给出完整当前表并从统计方法、数据可用性和相关表注直接引用。
3. 第二跨场景族应在消融段落明确。NoDiversity 在 7/7 场景、NoRepair 在 7/7 场景均通过各自跨场景 Holm；FixedDE 在 0/7 场景通过。尤其 NoRepair 的 storage_allocation 在跨场景族 p=0.01765，而其场景内全对手族 p=0.05765，说明两套族会给不同判定，必须并列解释而非选用较有利者。

### MINOR

- AC 层每方法每实验只有一个确定性折中计划，二元可行性病例共享网络与映射规则，不是 72 个独立算法重复。稿件已大体称为 qualitative/composition-level；所有“rate difference”均应保持描述性。

## P4 — SHIELD-MOEA

**总评：BLOCKER。** 主统计族已经从含确定性重复的旧 40 项修正为 32 个随机基线比较，两个确定性规则贡献 16 个描述差距；摘要、结果和结论大多已采用正确数字。Table 4 的主要效应/CI/p 值与 v2 证据一致。

### BLOCKER

1. `MANUSCRIPT.md:41` 仍称“40 of 40 Holm-corrected baseline comparisons”，与摘要的 32、结果的 32/32 和结论的 32 直接冲突。必须改为 **32/32 stochastic-baseline comparisons**，并另述 16 个确定性差距为描述性。
2. `MANUSCRIPT.md:413` 将 worst-case HV 0.269 与 mean HV 0.274 直接比较并称“tracks its mean closely”，但方法部分 `MANUSCRIPT.md:261,312` 已说明二者采用不同固定归一化边界，只能在各自列内比较。该跨标度比较无效，必须删除。

### MAJOR

1. 同段由一个 16 场景样本的 worst-case 指标推断“not specialized to benign scenarios; degrade gracefully”强于证据。限制部分已承认它不是真正极值界（`MANUSCRIPT.md:579`）。应改为“在该固定 16 场景评估样本中保持相对基线的正差距”，不得上升为稳健性认证。
2. NoOutage 的“exactly two experiments”表述 `MANUSCRIPT.md:427` 只对场景内主族成立。跨八场景的第二 Holm 族仅 restoration-aware 保持显著（0.0243），outage-contingency 为 0.0753。需在句中标明 family，并把组件结论依据限定到跨场景结果。
3. 参数扫描 `MANUSCRIPT.md:445--465` 含九个 MWU p 值，没有声明多重性族或调整。至少应按三个轴分别或九项整体声明校正策略；否则保留为探索性，且只描述均值趋势。

### MINOR

- AC 可行率是固定组合映射的构成层诊断，不是种子级因果试验。`MANUSCRIPT.md:500` 的“physically relevant change”可改为“composition-level electrical difference”，与该段后半的限制一致。

## P5 — TRACE-MOEA

**总评：MINOR。** 本轮统计框架基本合格。Random Feasible 已正确纳入随机对手；AHP-TOPSIS、Weighted Sum、Greedy BCR 按确定性处理。28 个随机基线比较中 27 个均值为正、24 个 Holm 显著、0 个显著负；21 个确定性差距均为描述性，均与 v2 审计一致。NoPreferenceRanking 与 NoScheduleRisk 的第二跨场景族分别为 p=0.0722 和 0.0510，稿件已诚实降为未解决。MTEP/NERC 也已明确降为描述性外部一致性，不再声称组合层面的 above-chance 有效性。

### BLOCKER

- 无。

### MAJOR

- 无新的核心主分析缺陷。

### MINOR

1. 首次出现 bootstrap CI 时明确标注其为 pointwise、multiplicity-unadjusted mean-difference CI，并说明 Holm rank test 决定显著性。例如 reliability-driven 的 CI 可不跨零而 Holm p=0.242；这不是自相矛盾，但当前稿件没有解释不同估计量和校正层级。
2. `MANUSCRIPT.md:496` 对 AHP-TOPSIS 的两个 Kendall tau 使用“both significant”，而本节总体承认没有预注册外部比较族。建议改为“raw, unadjusted associations”并保留描述性定位。
3. 完整 v2 推断表虽已在方法中指名，投稿包需确保实际作为补充材料包含，而非仅存在于本地证据目录。

## P6 — BiLo-NSGA

**总评：BLOCKER。** 主实验的确定性/随机性处理、40 个随机基线比较、36 个显著胜和 16 个确定性描述差距均与 v2 一致。工作量匹配也已从“相同计算预算”收窄为 1600 个候选邻域的名义上限，表述更准确。

### BLOCKER

1. Table 6 的 AHP-TOPSIS broad capture 为 **1.0995**（`MANUSCRIPT.md:467`），高于 BiLo-NSGA 的 **1.071**；但 `MANUSCRIPT.md:477` 声称 BiLo-NSGA“exceeds the seven external baselines”。下一段 `MANUSCRIPT.md:479` 又正确承认 AHP-TOPSIS 最高。必须删除错误的全胜陈述，改为逐一列出实际排序或仅称超过若干进化基线。

### MAJOR

1. `MANUSCRIPT.md:446,568` 称 MTEP16 outcomes “independent of ... candidate featurization”，但 `MANUSCRIPT.md:488` 明确 `appendix_status` 是特征且与 broad outcomes 相关。可以说 outcome fields 未用于拟合/特征构造，不能说结果在统计意义上独立于特征化。建议改为：“Outcome snapshots were not used in fitting; decision-time appendix status is prognostic and creates construct overlap.”
2. Forward insertion 的主场景内族支持 3/8；第二跨场景族额外使 reliability-prioritized 达到 p=0.04734，从而为 4/8。稿件必须始终把 3/8 称为 primary within-scenario family，把 4/8 称为 post-freeze exploratory cross-scenario family，不能合并成单一“4/8 supported”结论。当前正文大体这样做，应全稿保持一致。
3. 外部回测的项目级 p 值没有保持组合选择造成的依赖，也没有比较族。稿件已将其降为描述性，但所有“above uniform draw”必须只指 capture 的数值定义，不得暗示经校正的显著优于随机组合。

### MINOR

1. 对 NoForwardSearch 的均值差 CI 同样是未校正逐比较区间；需解释其与 Holm 判定的关系。
2. 标题中的“Forward-Dominant”应继续由操作性定义支撑：仅表示已解析的局部算子证据集中在 forward side，而不是 pooled mean、所有场景或所有外部结果都由 forward insertion 改善。

## 4. 投稿前最低统计修订清单

1. 修复 `exact_signflip_p`，加解析回归测试，重新生成 P1/P2 配对审计及正文引用数字。
2. P2 删除旧 Ausgrid p=0.0044；统一为当前精确层级结果。
3. P4 全稿统一 32 个随机比较 + 16 个确定性描述差距；删除 mean/worst-case 跨归一化列比较。
4. P6 修正 broad-capture 全胜假陈述及“独立于特征化”措辞。
5. P3/P4 为参数扫描声明 Holm 家族或明确降为探索性，不再使用未校正 p 值作总体显著性结论。
6. 六篇统一定义：主检验、Holm 家族、效应量、pointwise bootstrap CI、配对敏感性、跨场景补充族；完整 v2 表纳入补充材料。
7. 对 P3--P6 保留确定性方法 n_eff=1 和“无种子级 p 值”的处理；不得恢复矩形档案中的重复伪样本。
8. 外部回测若不增加组合保持的置换/重采样设计，则继续严格限定为描述性外部一致性，不作 above-chance、有效性或真实工程效益推断。

## 5. 复审判定

第二轮没有支持“六篇均可直接投稿”的统计结论。P2、P4、P6 存在可定位且可修复的投稿阻断项；P1、P3 需要较实质的统计报告修订；P5 接近合格，仅需小修。完成上述最低清单并重新导出审计证据后，建议进入第三轮独立一致性复核，重点做全文数字搜索、表/图/摘要/结论四向核对，而不必在没有新科学问题的情况下重跑全部核心实验。
