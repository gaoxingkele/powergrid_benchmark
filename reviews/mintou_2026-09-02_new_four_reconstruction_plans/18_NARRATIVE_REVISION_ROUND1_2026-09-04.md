# 叙事层修改规格 — 第一轮（R1）

**日期：** 2026-09-04
**生效时点：** 全部规格在 harness Stage-7（`s07_results_first_manuscript`）应用；P2 摘要压缩版可提前交作者预览确认。
**格式：** 每项给出「位置 / 现状摘要 / 目标替换文本 / 依据」。

---

## P1 — TRACE-MOEA（Energies）

### P1-R1-1 摘要首句：power-grid 语义锚定
- **位置：** abstract 首句
- **现状：** "Utilities reviewing large grid-project queues need constrained portfolio search and inspectable summaries of events generated during optimization."
- **目标：** "Power-grid investment portfolio optimization requires constrained search over large project queues and inspectable summaries of optimization events."
- **依据：** 05 前评估 §4.1（锁定标题无 power grid，须摘要首句/关键词/cover letter 连续补偿）；12 评分报告 P1 缺口 2。关键词 "power grid investment review" 已有，保留。

### P1-R1-2 引言首段：审查语境补投资组合语义
- **位置：** Introduction 第 1 段
- **目标：** 在 "select from predefined projects under a budget" 处补 "—an investment portfolio optimization problem with hard budget constraints"。
- **依据：** 同上；为 Section 选择与审稿人第一印象服务。

### P1-R1-3 Headline 双版本（Stage-6 结果决定用哪版，预写）
- **版本 A（H1 通过）：** "In scenarios where preference information is identifiable in the data (pre-registered H-Pref condition), preference-guided elitism yields significant hypervolume gains over NSGA-II; outside this condition the effect is absent."
- **版本 B（H1 不通过）：** "TRACE-MOEA provides a reproducible budget-constrained proxy-search framework with measurable event summaries; it does not establish an independent preference-adaptation benefit, normalization-invariant superiority, or project-level lineage."
- **依据：** 13 号契约 §4/§7；两版都不得删除 legacy 0.89%/0.17%/Table 9 内容。

### P1-R1-4 cover letter 要点（3 句模板）
"锁定标题不含 power grid，但本文研究的是电网投资组合审查问题（第 1 段与关键词明示），Section 建议 F1 Electrical Power System。贡献定位为带可检查事件摘要的预算约束组合搜索框架（可复现审计工作流），非算法优越性声明。数据与代码声明见 Data Availability。"

---

## P2 — BiLo-NSGA（Applied Sciences）

### P2-R1-1 摘要压缩至 ≤200 词（172 词版，红线句保留）
- **位置：** abstract 整段替换
- **目标文本：**

> Utilities select grid-investment portfolios under hard annual budgets, yet generic evolutionary operators do not express changes in review terms. BiLo-NSGA embeds affordable insertion, atomic delete-insert substitution, a heuristic group-label bonus, and feasibility recovery within non-dominated sorting. We compare a metered stage-local BiLo-NSGA with a specified NSGA-II and Pareto Local Search on 120 public-proxy candidates, eight scenarios, and 30 common seeds. Under an exact 3200-unit evaluation budget, mean feasible-front hypervolume is 0.16277 for BiLo-NSGA, 0.17213 for NSGA-II, and 0.11626 for local search: BiLo-NSGA loses four of eight Holm-corrected NSGA-II contrasts and wins none, while exceeding the disclosed local-search configuration in all eight; equal-time comparisons show three significant wins, two losses, and three unresolved contrasts. Bound, clipping, reference-point, and local-parameter checks preserve the pooled ordering but change gap magnitudes, and the joint proposal-cap setting (2,2) is descriptively 4.29% above the registered (8,4) setting. Matched evidence thus supports a feasible project-vocabulary search framework and a bounded advantage over the disclosed local-search configuration, not superiority over NSGA-II. Run-level event summaries are not lineage or replay records.

- **依据：** 12 评分报告（摘要 ~220 词超限）；红线句 "loses four of eight... and wins none" 与 "not superiority over NSGA-II" 原样保留；"charging every population-objective evaluation or evaluated local proposal" 压缩为 "exact 3200-unit evaluation budget"（计量语义保留，细节在正文 § 实验设置）。

### P2-R1-2 COI 具名披露模板（需作者确认后填）
- **目标文本：** "The authors are employed by the Economic and Technological Research Institute of State Grid Fujian Electric Power Co., Ltd., and the research was conducted within their institutional scope. The authors declare no personal financial conflicts of interest beyond this employment."
- **依据：** Applied Sciences 语料硬规则（受利益相关电网公司雇佣必须具名披露）；替换现 "no conflicts of interest" 空洞声明。

### P2-R1-3 标题术语补偿（正文首次出现处）
- **目标：** 正文首次出现 "evolutionary" 处加括注 "henceforth, evolutionary (the locked title uses the short form)"——由 Stage-7 视排版决定是否保留括注，或改为 cover letter 一句话说明。
- **依据：** 12 评分报告（"Evolution Algorithm" 非标准措辞，标题锁定）。

### P2-R1-4 cover letter 要点
"标题与本文的锁定标题一致（'Evolution Algorithm' 为作者锁定措辞）。核心贡献定位为等代价审计协议 + 项目词表局部搜索框架，BiLo-NSGA 对 NSGA-II 的负结果作为诚实负结果保留并构成本文的边界声明（红线要求）。Section 建议 Energy Science and Technology。"

---

## P3 — CARS-MODE（Energies）

### P3-R1-1 "Self-Adaption" 拼写处置（cover letter 一句话）
- **目标文本：** "The locked title uses 'Self-Adaption'; the standard spelling in the text is 'self-adaptation'."
- **依据：** 前评估 §6.4（拼写风险）；标题锁定不可改，正文统一用标准拼写并在首次出现处注明。

### P3-R1-2 Headline 双版本（Stage-6 结果决定，预写）
- **版本 A（H1 通过）：** "Adaptive parameter control improves analytic hypervolume specifically under high-DER, tight-budget (rugged) planning conditions; outside these conditions its effect is not separable from fixed settings."
- **版本 B（H1 不通过）：** "CARS-MODE establishes a reproducible constrained-search and metric-sensitivity workflow for screening proxy fronts; the combined adaptation bundle remains unresolved against the fixed configuration."
- **依据：** 15 号契约 §4/§7；两版都必须保留 FixedDE 名义领先与 Table 5/9 反转表。

### P3-R1-3 引言 "action-aligned" 边界句保持
- 现状已合格（摘要明写 "portfolio proxy rather than action-aligned expansion decisions"），Stage-7 不得弱化此句；若 S3 完成 action-aligned AC 映射，此句按新证据升级，升级须走 harness claim 门禁。

---

## P4 — CSA-LoadNet → HGCN（Electronics）

### P4-R1-1 红线表述保留清单（Stage-7 强制核对）
- 四处红线句（摘要 "not a GCN or HGCN... No GCN or HGCN experiment or result is reported"；引言；方法；结论）在 Stage-6 产出真实 HGCN 结果前**不得删除或弱化**；Stage-6 后按新证据替换并保留 legacy 结果为预注册历史章节。
- **依据：** 16 号契约红线声明；12 评分报告（这是全稿当前最强的科学资产）。

### P4-R1-2 persistence 基线段落模板（待 Stage-4 填充数字）
- **目标（占位段落）：** "Persistence serves as the method-independent reference: the last available processed value is carried forward to the target position. On the Ausgrid hierarchy at lead 24 its WAPE is [VALUE], on OPSD lead 24 [VALUE], and on SimBench [VALUE]."
- **依据：** 12 评分报告（persistence 全稿缺失，Electronics 预测类底线要求）。

### P4-R1-3 MAE/RMSE 主表承诺段
- **目标：** 实验设置处写明 "MAE, WAPE, and RMSE are reported in every main results table"（Stage-6 填充数值）；当前 "preserved in the evidence tables" 措辞改为实际入表。
- **依据：** 12 评分报告缺口；Electronics 画像"预测类 ≥2 指标"底线。

### P4-R1-4 路由双版 cover letter 要点（决策门触发后选用）
- **Electronics 版（HGCN 实现且 H1 通过）：** Section 建议 Artificial Intelligence；贡献定位为"双曲图卷积在层级结构负荷数据上的条件化优势（匹配欧式 GCN 消融）"。
- **Energies/IEEE Access 版（H1 不通过触发路由决策门）：** 需标题豁免；定位为纯负荷预测的组件级审计 + rolling-origin 协议研究。
- **依据：** 16 号契约 §7；Paper_CCF open-data 语料路由提示（纯负荷预测 → Energies / Energy Reports / IEEE Access）。

---

## 附：本轮未改项与原因

- **四篇 canonical paper.tex 未做直接修改**：Stage-2 分支未合并（合并后 harness 会继续写这些文件），且 Stage-7 将从实验 manifest 重生成正文——手改会被覆盖。所有规格已在本文档固化，由 Stage-7 统一应用。
- **P1/P3/P4 摘要暂不压缩**：当前词数合规（166/157/~200-220）；P4 摘要边缘超限待 Stage-6 改写时一并处理。
