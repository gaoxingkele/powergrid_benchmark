# Journal Article Atlas：论文结构—证据—叙事解构库

目标不是另做一个写作模板，而是建立可追溯的「文章零件字典＋关系图＋同类文章分布＋难度画像」。第一轮以本地 MDPI 和 IEEE Access 电力相关参考论文为起点，结构可扩展到其他出版商、期刊和会议。自己的待投稿稿件不混入已发表参考分布。

## 从哪里看

1. [设计与统计口径](DESIGN.md)：哪些可以数、怎样数、怎样解释。
2. [字段字典](dictionary/FIELD_DICTIONARY.md)：字段定义、单位、层级及验证方式，由 `scripts/definitions.py` 生成。
3. [分类字典](dictionary/taxonomies.json)：公式、算法、实验、图表、理论、叙事动作和关系类型。
4. [期刊扩展规则](journal_profiles.json)：统一内核＋领域模块，区分官方来源与研究内建议。
5. [本地实测总表](outputs/paper_comparison.html)：本地 PDF 的自动候选值，**不是人工核验后的期刊平均水平**。
6. [统计画像](outputs/cohort_profiles.json)：样本数、有效值数、均值、中位数、分位数、缺失率和证据级别。
7. [执行与验收计划](EXECUTION_PLAN.md)：从自动候选到可用于评审校准的正式画像。
8. [skill 接口](skill/SKILL.md)：消费方必须保留证据状态，不按数量配额机械改稿。
9. [局部实填案例](examples/applsci_partial_case.md)：展示如何区分递增消融与heads敏感性，并将框架、表格和结论连接起来；不冒充完整人工校准。
10. [单篇检查表](REVIEW_CHECKLIST.md)：实际标注/复核时使用的19组验收问题。
11. [2026-09-13 同类型校准](calibration/2026-09-13_round1/COHORT_COMPARISON.md)：5个期刊、14篇来源筛选、8个任务组；框架与实验分类逐篇记录，数量仍为候选。
12. [全部15个期刊的覆盖缺口](calibration/2026-09-13_round1/JOURNAL_COVERAGE.md)：区分已筛选、样本不足和待补采，不跨任务拼凑期刊平均值。
13. [电力 × AI 全量范围核验](calibration/2026-09-13_power_ai_scope/SCOPE_REPORT.md)：现有169篇逐篇决定、原件核验、标题修订及版本隔离。
14. [可搜索的范围总表](calibration/2026-09-13_power_ai_scope/scope_browser.html)：按期刊、任务、算法或core_ai等标签查阅；[Markdown逐篇表](calibration/2026-09-13_power_ai_scope/ALL_ARTICLES.md)。
15. [新增全文解构批次](deconstruction/v1/INDEX.md)：持续扩展的实质逐篇JSON/MD，包含章节、公式、图表、实验与结论证据；数量以索引为准，完整验收仍未完成，不能与范围筛选或期刊校准混同。
16. [Information逐段个案](deconstruction/v1/papers/p_71fe4f1acd7e01c5.md)：62个正文段落＋3个列表项的来源映射和计算长度，核心内容附独立AI复核，非人工校准。
17. [Information首批三篇关系对照](deconstruction/v1/INFORMATION_BATCH.md)：任务、公式/图表、实验、统计和叙事并列，不跨年份与任务混算期刊均值。

本轮校准保存在独立 JSON 层，尚未合并进 `atlas.sqlite`；旧查询接口不会自动返回这些新记录。`source_screened_observations.json` 的42条已核对记录仅涉及任务、相关性和页数，不代表全文标注完成；详见该轮 `ROUND_STATUS.md`。

电力×AI全量范围层可通过 `py -3.12 -X utf8 knowledge_base/journal_article_atlas/scripts/query_power_ai_scope.py --journal "Energies" --keyword "规划"` 只读查询。默认筛选core_ai；`--decision computational_support` 可查询非AI电力计算支持文章。输出明确标为范围筛选，不是正式期刊标准。

## 数据组织

```text
原 PDF / XML / HTML（原址、只读、SHA-256）
  → paper / section / paragraph / equation / algorithm / experiment / table / figure
  → 带来源定位的 observation（字段值）＋ relation（逻辑边）
  → 按期刊 × 任务 × 文献类型 × 年份 × 证据等级分层
  → 描述分布、难度向量、证据质量向量、叙事与语言模式
  → 评审差距卡 / 写作规划 / 可追溯案例检索
```

`atlas.sqlite` 是可查询关系库；JSON 为便于版本控制和跨工具调用的交换层；HTML/Markdown 为阅读层。不把一张超宽表当作全部真相：例如“平均段落长度”可放总表，而每个段落的作用和前后衔接必须保存在子表中。

`outputs/corpus_manifest.json` 保存本轮入选原件与重复路径；`outputs/run_manifest.json` 绑定其 SHA-256 和解析实现哈希。当前输出属于可重建的试点工作结果，正式发布画像须按 EXECUTION_PLAN 另行冻结版本。

## 第一版的边界

新增实质全文解构请从[动态索引](deconstruction/v1/INDEX.md)进入；它与初期自动候选输出分开。首批对照表有[Information](deconstruction/v1/INFORMATION_BATCH.md)、[Mathematics](deconstruction/v1/MATHEMATICS_BATCH.md)、[SmartGridComm](deconstruction/v1/SMARTGRIDCOMM_BATCH.md)、[PESGM](deconstruction/v1/PESGM_BATCH.md)。批次达到3篇不等于全字段完成或期刊平均水平已校准。

新增批次对照：[Algorithms](deconstruction/v1/ALGORITHMS_BATCH.md)、[Sensors](deconstruction/v1/SENSORS_BATCH.md)、[IEEE Access](deconstruction/v1/IEEE_ACCESS_BATCH.md)。按实际预测目标、方法类别和证据强度分层使用，不把发表样本中的不足转化为投稿规范。

- 本地批量实测是解析器候选值；页数也只说明文件页数。公式、图表和段落未经逐项复核，不能冒充精确数值。
- 章节与段落按布局初分；PDF 文字块不等于语义段落。双栏和跨页合并需复核。
- 未开展双人一致性标注，未产生正式期刊难度系数或录用概率。
- 旧 `powergrid_paper/metadata/*distill*` 只作线索，不直接导入其“strong”等等级或含解析失败的均值。
- 本次不调用外部 LLM，不上传全文，也不改动参考论文或现有 journal skill。

## 运行

在仓库根目录，Python 3.12（本地已有 PyMuPDF）：

```powershell
py -3.12 -X utf8 knowledge_base/journal_article_atlas/scripts/definitions.py
py -3.12 -X utf8 knowledge_base/journal_article_atlas/scripts/atlas.py
py -3.12 -X utf8 knowledge_base/journal_article_atlas/scripts/test_atlas.py
```

第二条命令重新生成本库派生输出，不改源 PDF。不递归扫描论文项目联接、Git 工作树或整个磁盘。正式人工标注应保存在单独版本目录，不能写进自动输出文件。
