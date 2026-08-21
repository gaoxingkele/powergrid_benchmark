# 闽投六篇论文系统性学术叙事修订日志

日期：2026-08-12  
对象：`paper_projects/mintou_p1_*` 至 `paper_projects/mintou_p6_*` 的当前 `MANUSCRIPT.md`

## 共同修订原则

本轮没有改写、删除或美化任何既有实验数字，也没有把未显著结果改写为等效、优越或因果结论。修订集中处理五类问题：题目承诺与组件证据不一致；版本、冻结和审计过程占据主叙事；框架级结果与组件级归因混用；代理指标与外部或物理验证混用；Discussion 和 Conclusion 重复列举免责声明而缺少机制解释。

六篇统一采用以下证据层级：主实验回答框架在当前任务上的表现；直接对照和消融回答具体组件是否贡献；外部一致性、AC 检查和迁移检查只回答其各自覆盖的外部问题；未通过直接实验的工程价值放入 future work，而不作为已经成立的结果。

## P1：Operating-State Retrieval / Curtailment-Risk Benchmark

- 保留“框架 + 公共基准”论文身份，删除把旧版失败过程列为第四项贡献的写法。
- 摘要重写为问题、基准、方法、跨时域结果和适用边界五步结构。
- 将旧版沿革压缩为“方法无关目标构造”的构念效度说明。
- 将结果中心固定为检索在 1 h MAE 上有益、在 24 h onset warning 上有害的跨时域反转。
- Discussion 从“为什么没有胜出也要发表”改为对决策支持的指标和基线要求。
- NREL-118 统一写为 fixed-cap applicability check，不再使用审计式标题。

## P2：CSA-LoadNet

- 保留现有题目，贡献核心明确为 OPSD 24 h 的 cross-series aggregation effect，而不是双曲几何。
- 将“命名历史”改为 weighting variants and artifact labels，只保留复现所需的一对一标签映射。
- 用“evidence hierarchy and claim calibration”替换 v5–v8 的项目沿革叙事。
- 区分三类证据：十种子决定性比较、三种子架构筛选、精确 Ausgrid 层级与 reconciliation。
- Conclusion 明确贡献为设置特定的聚合效应、accuracy/coherence 分离，以及未观察到权重形式差异。

## P3：CARS-MODE

- 题目改为 `Constraint-Aware Repair and Strategy-Pool Multi-Objective Differential Evolution`，避免把未获支持的 adaptation 写成题目主承诺。
- 第一项贡献改为具有可分离机制的约束感知框架；FixedDE 负向消融继续保留。
- Discussion 删除版本近失记录，改为解释为何完整框架可优于外部控制、同时仍不能把增益归因于自适应。
- Conclusion 明确 repair 和 diversity 是已解析的增益来源；adaptive controller 是已实现但未解析的组件。
- 代理 HV 与 AC 排名不一致被提升为构念效度主发现，而不是附带限制。

## P4：SHIELD-MOEA

- 题目改为 `Scenario Handling with Isolated Evaluation and Lookahead`，使 SHIELD 缩写、方法机制和证据保持一致，并删除会暗示已认证鲁棒性的 `Scenario-Hardened`。
- 贡献从六项压缩为四项：隔离评价、选择性 screening、框架结果与组件归因、sampled-envelope/AC/sensitivity 诊断。
- 明确 periodic re-screening、hybrid variation 和 resilience objective 没有解析出质量增益；repair 是主要增益来源。
- “worst-case robustness”统一改为 sampled worst-envelope，避免将 16 个采样场景写成总体最坏情况保证。
- Abstract 和 Conclusion 以 disjoint search/evaluation draws 为主方法价值，screening 仅作为 exposure/economy 机制。

## P5：TRACE-MOEA

- 题目改为 `Traceable Multi-Objective Evolution with Preference-Guided Ranking`，将证据充分的 traceability 置于 unresolved preference adaptation 之前。
- 摘要和贡献区分框架级 0.89% HV 结果、0.17% preference ablation、98.6% trace coverage 和描述性外部一致性。
- 将 audit archive、audit state 等主文术语统一为 decision trace / trace state；审计文献仅保留在理论来源处。
- 删除 deprecated pipeline 的正文叙事，明确标准 HV 不消费方法拥有变量即可。
- Discussion 明确不足 1% 的 NSGA-II 差距与 trace 输出是两个不同属性；trace 的人类价值尚待实验。
- 与 P6 的边界固定为 selection/ranking/trace 对 variation/local moves。

## P6：BiLo-NSGA

- 题目改为 `Forward-Dominant Project-Level Local Search`，删除题目中的 auditable，保留有直接消融支持的 forward-dominant。
- Abstract 明确三层结论：框架相对基线、forward-side resolved cells、substitution 未解析。
- 全文将 audit trail 统一为 decision trace / recorded move history；atomic substitution 的价值写为可审查替换语义，而非性能增益。
- 删除旧 composite-score 事故叙事，只说明标准 HV 与 trace variables 分离。
- 将 Future Work 与 Limitations 分工：前者列直接实验扩展，后者集中陈述当前证据边界。
- Conclusion 不再把 substitution 包装为双向增益，明确 forward-only 是精简实现，full variant 仅在需要 atomic replacement records 时有额外语义价值。

## 尚需作者人工确认

- P1、P4 的作者、单位、ORCID 和通讯作者信息仍为占位符。
- 六篇作者均需确认最终 CRediT、基金、利益冲突、AI assistance 和数据发布措辞。
- 外部数据的长期归档 DOI/commit/release 应在投稿前固定；当前稿件不将“可由通讯作者提供”误写为永久公开归档。

## 本轮验证范围

修订完成后将重建普通预览和目标期刊官方 LaTeX/PDF，并执行引用、数字、图表、标题、跨章节和 PDF 版式检查。实验结果文件本轮只读，不执行结果导向的重新调参。

## 验证结果

- 六篇普通预览与目标期刊正式模板均完成两轮构建。
- 正式 PDF 页数：P1 15 页，P2 19 页，P3 22 页，P4 24 页，P5 23 页，P6 24 页。
- 图数：8、8、9、9、8、9；表格块数：6、5、8、8、6、7；均与 Markdown 主稿一致。
- 参考文献：30、30、32、45、33、32，共 202 条；196 条经 DOI/Crossref 自动核验，6 条无 DOI 的标准或官方资料保留人工书目核对状态。
- 六篇 PDF 均无缺字警告、未定义引用或硬门槛占位符渗入正式模板。
- 闽投实验资产回归测试：`tests/test_mintou_experiments.py` 共 12 项，全部通过。
- 完整统计审计测试在默认 Python 3.14 环境未能收集，原因是本机 SciPy 二进制扩展损坏；Python 3.12 未安装 pytest。本轮未改动统计代码和实验数据，且既有统计表、PDF 构建和 12 项资产测试均通过。
- 同源论文独立性检查未发现相同结果表或相同研究图；相同文件仅为期刊模板的 ORCID 标志。文本重合主要来自共同标准方法、公共数据描述和共同参考文献，主方法、实验记录和结论已显式区分。

## 投稿门槛状态

学术叙事、期刊模板、引用和版式已完成本轮修订。仍不能在未确认信息的情况下替作者填写作者贡献和基金。P1、P4还缺作者/单位/通讯作者；P1缺IEEE作者简介；P2、P3、P5、P6缺经全体作者确认的 CRediT；六篇基金信息均需作者核定。这些属于投稿元数据门槛，不影响本轮正文与实验结论的完整性。
