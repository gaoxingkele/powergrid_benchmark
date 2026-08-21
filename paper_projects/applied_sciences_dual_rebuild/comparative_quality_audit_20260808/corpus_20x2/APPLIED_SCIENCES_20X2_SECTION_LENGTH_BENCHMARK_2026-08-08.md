# Applied Sciences 20×2 对照语料与逐章节“中位数偏上”篇幅目标

日期：2026-08-08  
对象：C²GES 与 MA-SQLGrid 正式 LaTeX 预览稿  
统计目标：分别建立 20 篇同刊对照组，并按章节 P50、P60、P75 确定扩写目标。  
本轮性质：文献对标和篇幅规划；未修改论文正文，未生成或重跑论文实验。

## 1. 核心结论

1. 两套语料均为 **20 篇 Applied Sciences research article**，两组没有重复论文，共 40 篇。40 份官方 PDF 和 40 份官方 JATS XML 已下载，DOI、期刊名和 article-type 已逐篇机械核验。
2. “中位数偏上”被操作化为 **P60**；P75 作为防止扩写过度的上限。该规则比使用平均数稳健，因为 MA 组存在 44 页和 34 页的近期长文。
3. C²GES 对照组总页数 P50/P60/P75 为 **21.0/23.2/25.2 页**；MA-SQLGrid 对照组为 **22.5/23.0/24.2 页**。因此两篇的排版目标都应放在 **23–24 页（含参考文献）**，而不是机械追到最大值。
4. 按逐章 P60 计算，C²GES 正文目标约 **8550–9000 词**，当前约 3574 词；MA-SQLGrid 目标约 **8925–9325 词**，当前约 6266 词。两篇都需扩写，但增补位置不同。
5. P60 是本项目的编辑目标，不是 Applied Sciences 的录用门槛。期刊官方没有最大篇幅限制，重点仍是实验与方法是否完整、可复现。

## 2. 检索、筛选和核验

### 2.1 检索框架

来源限定为 Applied Sciences（ISSN 2076-3417），时间范围 2020–2026，实际纳入为 2022–2026。Crossref 初检使用下列主题簇：

- C²GES：power-grid NLP、power fault/maintenance knowledge graph、relation extraction、extractive summarization、graph summarization、technical report summarization、causal/counterfactual text graph。
- MA-SQLGrid：Text-to-SQL、schema linking、LLM SQL generation、natural-language database interfaces、multi-agent/agentic framework、power/microgrid multi-agent systems、execution validation。

检索产生 638 条去重候选记录。排除 review、editorial、special-issue introduction、无文本/数据库/多智能体方法实验的纯控制论文，以及无法获得官方 XML/PDF 的记录。最终人工目的性分层纳入 40 篇。

### 2.2 分层构成

| 对照组 | 直接同域/直接任务 | 方法/框架相似 | 2024–2026 近期论文 | 总数 |
|---|---:|---:|---:|---:|
| C²GES | 9 | 11 | 12 | 20 |
| MA-SQLGrid | 10 | 10 | 16 | 20 |

这不是随机抽样或 PRISMA 效果综述，而是为论文结构和写作充分性建立的 matched benchmarking corpus。它适合确定章节预算，不适合推断期刊总体录用概率。

## 3. 统计口径

- 页数来自官方 PDF，包含参考文献。
- 章节词数来自 JATS `<body>` 内段落文本，图题、表格和参考文献不计入章节正文。
- 将不同标题归一为六个角色：Introduction、Related Work/Background、Methods and Setup、Results and Analysis、Discussion and Limitations、Conclusions。
- 同一角色包含多个顶层章节时进行合计。例如 Dataset、Experimental Setup、Framework 均计入 Methods and Setup。
- Related Work 或 Discussion 没有独立章节时，不以零值压低统计；该角色使用“显式出现论文”的 present-only 分布。同时报告 Introduction+Related Work 和 Results+Discussion 的组合分布用于校验。
- 当前稿件词数由 TeX 段落解析器估算，和 JATS 计数器存在少量格式差异；目标采用 50 词粒度，不把个位数差异当作质量门槛。

## 4. C²GES：20 篇对照统计

### 4.1 全文规模

| 指标 | P25 | P50 | P60 | P75 | 当前 C²GES |
|---|---:|---:|---:|---:|---:|
| 页数（含参考文献） | 16.8 | 21.0 | 23.2 | 25.2 | 15 |
| 正文词数 | 6151 | 7604 | 8310 | 9559 | 3574（TeX 估算） |
| 正文段落 | 64.8 | 72.5 | 91.4 | 107.2 | 53 |
| 图 | 5.8 | 6.0 | 7.4 | 9.0 | 4 |
| 表 | 5.0 | 7.0 | 7.4 | 8.2 | 6 |
| 参考文献 | 29.5 | 39.5 | 44.4 | 49.2 | 31 |

公式 P60 为 17.4，但该统计混合了知识图谱神经模型、关系抽取和摘要算法。C²GES 不应为达到 17 个公式而数学化；只需确保每个核心量、路径效用、选择目标、复杂度和统计量定义完整。

### 4.2 逐章节分布

| 归一章节 | 显式出现 n | P50 词 | P60 词 | P75 词 | 同域 P50 | 方法 P50 | 近期 P50 | P60 段落 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Introduction | 20 | 927 | 1015 | 1123 | 1116 | 821 | 867 | 10.0 |
| Related Work/Background | 15 | 1037 | 1043 | 1160 | 1222 | 974 | 1046 | 9.4 |
| Methods and Setup | 19 | 3350 | 3565 | 3809 | 3225 | 3350 | 3516 | 39.4 |
| Results and Analysis | 20 | 1835 | 1874 | 2822 | 1854 | 1816 | 1879 | 21.8 |
| Discussion and Limitations | 5 | 665 | 675 | 689 | 809 | 665 | 641 | 9.4 |
| Conclusions | 20 | 353 | 404 | 483 | 359 | 347 | 353 | 4.4 |

Introduction+Related Work 的组合 P50/P60 为 1850/1957 词；Results+Discussion 的组合 P50/P60 为 1966/2058 词。这两个组合结果与逐节目标一致，说明 Related Work present-only 处理没有人为抬高总预算。

### 4.3 当前稿与目标

| 章节 | 当前词/段 | P60 基线 | 本项目目标 | 需要净变化 | 主要增补内容 |
|---|---:|---:|---:|---:|---|
| Introduction | 361 / 5 | 1015 / 10 | 1000–1050 / 9–11 | +639–689 | 电网维护报告需求、技术摘要问题、题名与 NERC proxy 的合理性、明确 RQ 和贡献差异 |
| Related Work | 215 / 4 | 1043 / 9.4 | 1050–1100 / 9–11 | +835–885 | 抽取摘要、图摘要、causal language、counterfactual explanation、电网文本/维护 KG；新增比较表 |
| Materials and Methods | 1565 / 25 | 3565 / 39.4 | 3550–3650 / 38–43 | +1985–2085 | 数据纳入与泄漏协议、贯穿式 toy example、typed graph/path 删除、伪代码与复杂度、baseline/hyperparameter 公平性、统计与复现 |
| Results | 610 / 10 | 1874 / 21.8 | 1850–2000 / 20–24 | +1240–1390 | 数据集描述、主效应解释、长度公平性派生分析、逐报告异质性、错误分类/案例、计算成本、开发集稳健性 |
| Discussion | 527 / 7 | 675 / 9.4 | 700–750 / 9–11 | +173–223 | 与同刊图摘要/KG方法对照、负消融含义、实际维护域迁移与安全边界 |
| Conclusions | 296 / 2 | 404 / 4.4 | 400–450 / 4–5 | +100–150 | 分为发现、机制结论、限制、未来验证；移除投稿包清单式文字 |
| **合计** | **3574 / 53** | **约 8576 / 94** | **约 8550–9000 / 90–100** | **约 +5000–5400** | 目标约 23–24 页 |

### 4.4 C²GES 扩写约束

- 不重新使用 test set 搜索反事实权重，不为“数据好看”改变冻结结果。
- 长度公平性、报告长度分层、候选长度分层必须只从冻结 ledger 做确定性派生，并标记为 post hoc diagnostic。
- 案例分析使用 rights-safe 非逐字摘要、sentence ID/page locator 或合成说明，不复制受限报告全文。
- 若没有专家语义标注，不能把 LLM 评判描述为真实电网专家裁决。
- 图表建议从 4 图/6 表提升至约 **7–8 图、7–8 表**：优先新增相关工作矩阵、toy-graph/algorithm walk-through、长度公平性图、错误分类表，而不是装饰性框图。

## 5. MA-SQLGrid：20 篇对照统计

### 5.1 全文规模

| 指标 | P25 | P50 | P60 | P75 | 当前 MA-SQLGrid |
|---|---:|---:|---:|---:|---:|
| 页数（含参考文献） | 19.0 | 22.5 | 23.0 | 24.2 | 20 |
| 正文词数 | 6170 | 7913 | 8615 | 9100 | 6266（TeX 估算） |
| 正文段落 | 73.2 | 108.5 | 126.4 | 144.5 | 83 |
| 图 | 3.8 | 9.0 | 11.0 | 13.2 | 4 |
| 表 | 3.8 | 6.0 | 6.4 | 8.2 | 12 |
| 参考文献 | 34.0 | 39.0 | 40.0 | 41.5 | 31 |

MA 当前表格数已经高于 P75，不再增加结果表数量作为默认目标。图数量偏少，但不应机械追到 11；应把若干大表转成 2–3 张信息密度高的结果图，同时保留机器完整表在 supplement。

### 5.2 逐章节分布

| 归一章节 | 显式出现 n | P50 词 | P60 词 | P75 词 | 同域 P50 | 方法 P50 | 近期 P50 | P60 段落 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Introduction | 20 | 923 | 1149 | 1358 | 1115 | 762 | 836 | 10.0 |
| Related Work/Background | 15 | 1120 | 1157 | 1431 | 940 | 1166 | 1120 | 12.4 |
| Methods and Setup | 20 | 3196 | 3670 | 4483 | 2842 | 4583 | 2820 | 55.4 |
| Results and Analysis | 19 | 1694 | 1877 | 2291 | 1212 | 2081 | 1588 | 25.8 |
| Discussion and Limitations | 8 | 521 | 674 | 1088 | 434 | 1082 | 521 | 8.0 |
| Conclusions | 19 | 389 | 398 | 517 | 246 | 394 | 396 | 5.0 |

Introduction+Related Work 的组合 P50/P60 为 1901/1961 词；Results+Discussion 的组合 P50/P60 为 2139/2277 词。

### 5.3 当前稿与目标

MA 当前独立 Discussion 为 807 词，Limitations and Future Work 为 416 词；对标时合计为 1223 词、15 段。

| 章节 | 当前词/段 | P60 基线 | 本项目目标 | 需要净变化 | 主要增补/重组内容 |
|---|---:|---:|---:|---:|---|
| Introduction | 655 / 7 | 1149 / 10 | 1125–1175 / 9–11 | +470–520 | 电网数据库风险场景、Text-to-SQL/domain adaptation 缺口、multi-agent 可检验定义、明确 RQ 与贡献 |
| Related Work | 582 / 9 | 1157 / 12.4 | 1150–1200 / 12–14 | +568–618 | Text-to-SQL、schema linking、execution validation、agentic pipeline、多智能体证据标准、电网 precedent；新增架构比较表 |
| Materials and Methods | 2355 / 31 | 3670 / 55.4 | 3650–3725 / 50–58 | +1295–1370 | 五角色 I/O contract、blackboard state machine、threat model、executor/adjudicator、实验—主张映射、协议与统计、复现环境 |
| Results | 1036 / 17 | 1877 / 25.8 | 1850–1925 / 24–28 | +814–889 | 总证据层级、GridDB/BIRD/component/multi-state 分块解释、错误和 abstention 类型、顺序敏感性、计算成本 |
| Discussion + Limitations | 1223 / 15 | 674 / 8；P75 1088 | 750–850 / 9–12 | **重组并压缩 373–473** | 合并重复审计说明，强化与 DKASQL/RGISQL/近期 MAS 的横向比较；保留证据边界 |
| Conclusions | 415 / 4 | 398 / 5 | 400–450 / 4–6 | 基本不变 | 移除编辑包交付清单，保留核心发现、未验证主张和下一实验 |
| **合计** | **6266 / 83** | **约 8925** | **约 8925–9325 / 110–125** | **约 +2660–3060** | 目标约 23–24 页 |

### 5.4 MA-SQLGrid 扩写约束

- 不能把 inherited GridDB/BIRD 或离线 selector 结果重新命名为完整五角色端到端实验。
- 如果没有新增 call-matched、gold-isolated 五角色实验，应把新篇幅用于方法复现、横向比较、错误分析和证据层级，而不是声称 multi-agent superiority。
- 如果补做新实验，应先冻结 single-call、staged single-candidate、fixed multi-candidate、full five-role 四个条件及相同生成预算，再执行；这将替代一部分历史审计散文，而不是无限增加总页数。
- 表格由 12 张控制在约 9–11 张主文表，其余移 supplement；图由 4 张提升到约 **7–9 张**，优先增加 experiment map、primary-effect summary、risk–coverage/abstention、failure taxonomy，而不是生成式装饰图。
- 参考文献建议从 31 增至约 **40–45 篇**，重点补直接 Text-to-SQL 和近期 agentic/multi-agent 论文。

## 6. 两篇统一执行规则

### 6.1 “中位数偏上”落地规则

1. 每章正文目标先达到 P60；超过 P75 时必须说明该章为何需要更长。
2. 若当前章节已高于 P60，例如 MA 的 Discussion+Limitations，则以重组、去重复和证据密度为目标，不继续扩写。
3. 每段以一个主要修辞任务为单位；C²GES 目标 90–100 段，MA 目标 110–125 段。公式引句、表格宣告句不得单独作为极短段。
4. 总页数以 23–24 页为目标，25 页为软上限；不能用空白、过大图片或冗长 captions 人为达到页数。
5. 新增的每一项结果必须能追溯到数据、代码、冻结 ledger 或明确的新实验协议。

### 6.2 推荐扩写顺序

1. 先补两篇 Related Work 和直接比较表，因为它们当前距离 P60 最大且不需要改变实验。
2. 再重写 Methods：从“审计事实罗列”转为读者可复现的任务定义、算法/系统过程、参数、复杂度、协议与边界。
3. 对现有数据运行合法的派生诊断，补 Results 的解释、异质性、失败模式和计算成本。
4. 重排 Discussion，确保每个主张依次回答：观察到了什么、为何可能发生、与相近论文有何不同、不能推出什么、下一步如何验证。
5. 最后重新排版 PDF，复核章节词数、段落数、页数、图表引用和 supplement 分流。

## 7. C²GES 20 篇语料

| 年份 | DOI | 分层 | 论文 |
|---:|---|---|---|
| 2023 | 10.3390/app131911074 | 直接电网文本 | A Combined Semantic Dependency and Lexical Embedding RoBERTa Model for Grid Field Relational Extraction |
| 2022 | 10.3390/app12146993 | 直接电网 KG | Construction of Power Fault Knowledge Graph Based on Deep Learning |
| 2024 | 10.3390/app14209462 | 直接电网 KG | Knowledge-Graph-Based Integrated Line Loss Evaluation Management System |
| 2025 | 10.3390/app15158188 | 直接电网 KG | A Power Monitor System Cybersecurity Alarm-Tracing Method Based on Knowledge Graph and GCNN |
| 2024 | 10.3390/app14146189 | 直接电网图方法 | Research on Power Cyber-Physical Cross-Domain Attack Paths Based on Graph Knowledge |
| 2026 | 10.3390/app16041985 | 近期维护 KG | Construction of Bridge Maintenance Knowledge Graph Based on Deep Learning |
| 2024 | 10.3390/app14072946 | 维护文本/LLM | Research on Large Language Model for Coal Mine Equipment Maintenance Based on Multi-Source Text |
| 2022 | 10.3390/app122412736 | 维护 KG | Towards Domain-Specific Knowledge Graph Construction for Flight Control Aided Maintenance |
| 2025 | 10.3390/app15074034 | 故障文本/LLM | Large Language Model Based Intelligent Fault Information Retrieval System for New Energy Vehicles |
| 2025 | 10.3390/app15126395 | 图式抽取摘要 | Using Graph-Based Maximum Independent Sets with Large Language Models for Extractive Text Summarization |
| 2024 | 10.3390/app14114671 | 超图抽取摘要 | Contextual Hypergraph Networks for Enhanced Extractive Summarization (MCHES) |
| 2022 | 10.3390/app12094479 | 语义抽取摘要 | A Novel Approach for Semantic Extractive Text Summarization |
| 2023 | 10.3390/app13031458 | 注意力抽取摘要 | Attentional Extractive Summarization |
| 2022 | 10.3390/app122010382 | 句图摘要 | Sentence Graph Attention for Content-Aware Summarization |
| 2022 | 10.3390/app12125854 | 技术报告摘要 | Deep Learning-Based Bug Report Summarization Using Sentence Significance Factors |
| 2024 | 10.3390/app14177548 | 近期摘要方法 | FrameSum: Leveraging Framing Theory and Deep Learning for Enhanced News Text Summarization |
| 2023 | 10.3390/app13137753 | KG 增强摘要 | Enhancing Abstractive Summarization with Extracted Knowledge Graphs and Multi-Source Transformers |
| 2024 | 10.3390/app14051880 | 多文档摘要 | TOMDS: Topic-Oriented Multi-Document Summarization |
| 2025 | 10.3390/app15042119 | 近期关系抽取 | An Entity-Relation Extraction Method Based on the Mixture-of-Experts Model and Dependency Parsing |
| 2025 | 10.3390/app15137435 | 跨文档关系抽取 | CLEAR: Cross-Document Link-Enhanced Attention for Relation Extraction |

## 8. MA-SQLGrid 20 篇语料

| 年份 | DOI | 分层 | 论文 |
|---:|---|---|---|
| 2025 | 10.3390/app152011121 | 直接 Text-to-SQL | DKASQL: Dynamic Knowledge Adaptation for Domain-Specific Text-to-SQL |
| 2024 | 10.3390/app142210359 | 直接 Text-to-SQL | RGISQL: Integrating Refined Grammatical Information into Relational Graph Neural Network for Text-to-SQL Task |
| 2025 | 10.3390/app15105306 | 直接 Text-to-SQL | Refining Zero-Shot Text-to-SQL Benchmarks via Prompt Strategies with Large Language Models |
| 2023 | 10.3390/app13042262 | 对话 Text-to-SQL | DIR: A Large-Scale Dialogue Rewrite Dataset for Cross-Domain Conversational Text-to-SQL |
| 2026 | 10.3390/app16020586 | 近期 LLM-SQL | Schema Retrieval with Embeddings and Vector Stores Using RAG and LLM-Based SQL Query Generation |
| 2025 | 10.3390/app152111399 | 多模型/SQL | Training a Team of Language Models as Options to Build an SQL-Based Memory |
| 2024 | 10.3390/app14177995 | 数据库 QA | Interactive Question-Answering with RAG for Personalized Databases |
| 2025 | 10.3390/app15147647 | 自然语言结构检索 | BIMCoder: A Comprehensive LLM Fusion Framework for Natural Language-Based BIM Information Retrieval |
| 2022 | 10.3390/app122211830 | 自然语言接口 | Building Natural Language Interfaces Using Natural Language Understanding and Generation |
| 2023 | 10.3390/app13085055 | 结构化 QA | A Method for Complex Question-Answering over Knowledge Graph |
| 2026 | 10.3390/app16041896 | 能源多智能体 | Multi-Agent-Based Smart-Home Energy Management with Adaptive Reasoning |
| 2025 | 10.3390/app15116079 | 多智能体编排 | Multi-Agent System for Smart Ro/Ro Terminal Management |
| 2026 | 10.3390/app16136715 | LLM 多智能体实验 | Differentiated Effects of Agent Diversity on Collective Decision-Making in LLM-Based Multi-Agent Delphi Systems |
| 2026 | 10.3390/app16115453 | 生成式 AI 多智能体 | An Exploratory Study of a Generative AI-Based Intelligent Tutoring System Using a Multi-Agent Architecture |
| 2025 | 10.3390/app152312547 | Agentic RAG | KA-RAG: Integrating Knowledge Graphs and Agentic Retrieval-Augmented Generation |
| 2026 | 10.3390/app16136787 | 近期多智能体框架 | AgentProphet: Source-Aware Multi-Agent Emerging Technology Forecasting |
| 2026 | 10.3390/app16073122 | 多智能体验证 | A Hybrid Multi-Agent System for Early Scam Detection in Crypto-Assets |
| 2025 | 10.3390/app151910358 | 电网多智能体 | Adaptive Energy Management for Smart Microgrids Using a Multi-Agent System with OPAL-RT Validation |
| 2023 | 10.3390/app13052865 | 电网多智能体 | Multi-Microgrid Energy Management Strategy Based on Multi-Agent Deep Reinforcement Learning |
| 2025 | 10.3390/app15020968 | 工业多智能体 | Multi-Agent-Based Intelligent Mine Gas State Decision-Making System |

## 9. 复现文件

- `corpus_manifest.json`：40 篇纳入记录、分层理由、官方 URL、PDF/XML SHA-256 和文件大小。
- `paper_level_stats.csv`：逐论文页数、总词数、段落、图、表、公式、参考文献及归一章节统计。
- `top_level_section_stats.csv`：所有原始顶层章节标题、归一角色、段落数和词数。
- `section_targets_p60.csv`：两组逐章节 P50/P60/P75、同域/方法/近期子组中位数。
- `corpus_20x2_summary.json`：完整分位数和子组统计。
- `query_crossref_candidates.py`、`build_corpus.py`、`analyze_20x2.py`：候选检索、下载核验和结构分析脚本。
- `C2GES/pdf|xml`、`MA_SQLGrid/pdf|xml`：40 篇官方全文的本地副本。

## 10. 局限与 AI 使用披露

语料为有目的的匹配样本，主题相似性依赖标题、摘要、方法和实验结构判断；不同研究类型的公式与图表需求不可机械迁移。部分论文把 Related Work 或 Discussion 合并到其他章节，present-only 统计虽避免零值偏差，但样本量较小，尤其 C²GES 的独立 Discussion 只有 5 篇。因此最终目标同时参考组合章节和同域/近期子组，而不只看单一分位数。

本次检索、候选筛选辅助、下载核验、JATS 结构解析、分位数计算和报告起草使用了 OpenAI Codex AI 辅助工具。所有纳入论文均通过官方 DOI/XML/PDF核验；统计由本地脚本从已保存文件确定性生成。AI 没有被当作论文作者、真实领域专家或实验标注者。
