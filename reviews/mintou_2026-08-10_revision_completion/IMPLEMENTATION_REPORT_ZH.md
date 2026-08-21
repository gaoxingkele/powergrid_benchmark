# Mintou 六篇论文缺口补强完成报告

日期：2026-08-10  
工作区：`D:/aicoding/powergrid_benchmark`

## 1. 完成边界

本轮直接修改六篇 `MANUSCRIPT.md` 主稿，并只使用已冻结的本地结果、公开数据衍生结果和现有统计表补强论证。没有为了得到更好看的数字而删除失败记录、重选种子、虚构新数据集、补造人工标注或宣称未执行的实验。期刊十篇对照组的自动统计只用于判断结构充分性；图、表和公式未机械填充到均值，以免重复展示同一证据。

## 2. 逐篇完成内容

### P1：DSTAR-GRU / IEEE Access

- 补齐 onset MAE、F1 的正式定义和评价口径。
- 新增 Figure 5，以 1 h/24 h、总体 MAE/onset MAE 的种子分布呈现不确定性。
- 将创新性限定为“可复现基准、检索机制的边界刻画”，不再暗示整体预测优于 persistence。
- 在摘要、结果、讨论和结论一致保留：检索在 1 h 有效、在 24 h onset warning 可能有害，朴素基线在部分主指标上获胜。
- 修正内部图表指代和过长复句；数据可得性改为与补充审查包一致的可核查表述。

### P2：CSA-LoadNet / Electronics

- 按执行代码补齐 MAPE、nMAE、sMAPE 公式；明确 nMAE 使用共同测试目标范围，而非训练范围。
- 新增 Figure 5，给出 OPSD、SimBench、Ausgrid 上相对于具名基线的十种子配对效应及种子级标准差。
- 把“跨序列注意力”的价值限定到有证据的 24 h 条件，明确 1 h、层次场景和几何解释的负面/不充分证据。
- 重写数据、方法、结果和讨论中的长句与跳跃段落；统一历史 CSV 名称与当前算法名的映射说明。

### P3：CARS-MODE / Energies

- 新增 Figure 6，展示折中投资组合中 reinforcement、storage、DER、automation 的组成差异。
- 加强规划组合、约束修复、自适应 DE 参数、HV 和 AC 验证之间的理论链条。
- 明确披露没有直接加入 JADE、SHADE、L-SHADE 等自适应 DE 比较器，避免把同族比较缺口隐藏在通用基线之后。
- 拆分问题定义、修复、敏感性、讨论和结论中的高负荷句；补齐公开 SimBench 衍生、2310 条运行记录及可复核资产说明。

### P4：SHIELD-MOEA / Energies

- 把负荷、DER、可靠性和韧性代理量改写为正式公式，并补齐五目标向量和预算约束。
- 新增 Figure 4 和 720 条已有冻结机制控制结果；后续敏感性与 AC 图重排为 Figures 5–6。
- 直接报告完整模型与 DE-only、fixed worst-K 在 8/8 设置不可区分，仅对 GA-only 在 3/8 设置占优；创新点限定为筛选经济性和防泄漏评价接口，而非虚构均值 HV 增益。
- 数据声明现同时覆盖 2400 条主运行记录和 720 条控制记录。

### P5：TRACE-MOEA / Energies

- 新增 Figure 4，展示 decision coverage 和每次运行 trace event 数量；外部有效性图顺延为 Figure 5。
- 细化偏好排序、约束修复、隔离审计档案与目标函数之间的职责边界。
- 明确缺少直接 preference-based EMO 比较器；不把弱偏好层效应包装为显著算法胜利。
- 加强外部有效性、预算敏感性、共享候选生成器与伴随论文独立性的披露。
- 更新投稿清单，使其准确反映 Figures 1–5 和已完成的数据可得性声明。

### P6：BiLo-NSGA / Applied Sciences

- 新增 Figure 5，联合展示局部移动次数和 HV；NERC 外部检验图顺延为 Figure 6。
- 将 forward insertion、backward deletion、dependency-aware move bonus、feasibility recovery 和审计轨迹的算法职责分开陈述。
- 在摘要、方法、结果、讨论和结论一致保留负结果：删除 backward search 后 pooled HV 约增加 0.16%，且各设置均不显著；其保留理由是审计和替换语义，而非精度增益。
- 明确缺少直接的项目词汇局部搜索比较器，并把边界/限制由五项修正为六项。

## 3. 当前结构与实验强度

下表的“对照均值”来自每篇目标期刊十篇方法或电网主题论文的自动抽取统计。期刊 PDF 中的公式/图计数会受子图和排版对象影响，因此仅作诊断，不是录用门槛。

| 论文 | 目标期刊 | 正文及参考文献词数 / 对照均值 | 公式 / 对照均值 | 图 / 对照均值 | 表 / 对照均值 | 数据集 | 实验设置 | 基线 | 消融/控制 | 有种子运行记录 | 预览页数 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | IEEE Access | 6160 / 7784 | 10 / 9.7 | 5 / 8.7 | 4 / 6.4 | 1 | 4 | 6 | 5 | 160 | 16 |
| P2 | Electronics | 6028 / 6714 | 10 / 19.3 | 5 / 11.3 | 4 / 5.3 | 3 | 5 | 5 | 5 | 420 | 15 |
| P3 | Energies | 6988 / 7856 | 11 / 30.9 | 6 / 12.3 | 8 / 8.4 | 1 | 7 | 6 | 4 | 2310 | 18 |
| P4 | Energies | 7313 / 7896 | 12 / 30.5 | 6 / 12.0 | 6 / 8.3 | 1 | 8 | 5 | 7 | 3120 | 19 |
| P5 | Energies | 7900 / 8562 | 8 / 25.3 | 5 / 10.5 | 6 / 6.5 | 3 | 10 | 6 | 8 | 3150 | 18 |
| P6 | Applied Sciences | 7329 / 8361 | 10 / 22.0 | 6 / 8.6 | 6 / 7.3 | 3 | 10 | 6 | 9 | 3840 | 19 |

公式和图的数量仍低于部分期刊样本均值，但六篇已经覆盖算法总览、实验流程、主结果、消融/控制、敏感性或外部验证以及新增机制诊断。继续按均值拆图或展开同一数学定义不会增加证据强度。真正能进一步提高外部效度的项目已作为限制写入正文，而没有以未经执行的结果补齐。

## 4. 新增图的证据追踪

| 论文 | 新图 | 直接输入 |
|---|---|---|
| P1 | `fig_seed_uncertainty` | `real_curtailment_results.csv` |
| P2 | `fig_cross_dataset_effects` | OPSD、SimBench、Ausgrid 的 v7 神经/额外种子结果 CSV |
| P3 | `fig_portfolio_composition` | `real_simbench_planning_compromise_compositions.csv` |
| P4 | `fig_mechanism_controls` | `real_simbench_planning_results.csv`、`real_shield_mechanism_controls_20260810.csv` |
| P5 | `fig_trace_diagnostics` | `real_project_review_results.csv` |
| P6 | `fig_move_diagnostics` | `real_project_review_results.csv` |

六图均提供 PNG、PDF 和 SVG；生成入口为 `scripts/mintou/generate_evidence_gap_figures.py`。

## 5. 核验结果

- 代码测试：`pytest -q tests/test_mintou_experiments.py`，12 项通过。
- 句段审计：六篇均已重新运行 `audit_sentence_paragraph_fit.py`；剩余 BLOCK 均为作者/基金事实字段，不是正文逻辑问题。
- 文献核验：P1 28/28、P2 30/30 在线核验；P3 27、P4 42、P5 32、P6 29 条自动核验。少量无 DOI 的经典书籍/论文需人工核查；少量 MDPI online year 与卷年不一致、以及会议年份元数据差异已保留为人工复核项，未擅自改写。
- 独立性：P5/P6 的共享候选生成器已显式披露；方法、目标、情景、实验和分析边界在两稿中分别声明。
- 构建：六篇均已从 Markdown 生成 LaTeX 和 PDF，未出现致命编译错误或未定义引用。当前 PDF 是 A4 通用审阅预览，不替代 IEEE/MDPI 官方投稿模板。
- 目视检查：六篇 PDF 首页、目录、作者区和正文起始均正常；新增图顺序连续，无缺号。

## 6. 仍需作者提供或最终投稿前执行

以下内容不能根据算法或本地数据推断，继续保留明确占位：

- P1：最终作者、ORCID、完整单位、通信作者、基金信息、IEEE biographies/照片。
- P2、P3、P5、P6：全体作者确认后的 CRediT 分工和已核实基金/APC 信息；另需补齐 ORCID。
- P4：最终作者、ORCID、完整单位、通信作者、CRediT 和基金/APC 信息。
- P3/P4/P6 的少量 Crossref 元数据差异以及经典无 DOI 条目需人工终审。
- 各稿最终切入目标期刊官方模板、图版面微调、相似性系统检查和全体作者逐项批准。

## 7. 不应被误解为“已经补完”的未来实验

正文已诚实列为外部效度扩展：P1 的第二独立电网；P2 的显式层次基线和更多独立数据源；P3 的 JADE/SHADE/L-SHADE；P4 的第二网络系统；P5 的直接 preference-based EMO 与真实评审标签；P6 的直接项目语义局部搜索比较器。除非实际执行并冻结，这些项目不得在当前稿中写成已完成结果。
