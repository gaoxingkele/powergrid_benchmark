# MA-SQLGrid 与 C2GES 转投 MDPI Applied Sciences：长期目标与多智能体执行总纲

## 0. 总目标与边界

在标题只作必要的小幅调整、研究标识 MA-SQLGrid/C2GES 保持不变的前提下，将两篇 CMC 版本重建为两篇面向 MDPI *Applied Sciences* 的独立 Article。最终交付必须包括：两套可编译投稿源稿与 PDF、冻结的数据与实验清单、可重复实验日志和结果表、图表源文件、三轮审稿意见—回复矩阵、期刊合规检查报告。

本计划旨在显著提高投稿成熟度，不能承诺编辑或审稿人一定录用。任何未真实运行的实验、未经人工完成的“专家标注”、不存在的显著性结果均不得写进论文。

## 1. 成功标准

### 1.1 双论文共同验收门槛

1. 每篇正文目标 7000–9000 英文词、5–6 个一级正文节、正式排版目标 18–26 页；篇幅服从完整性，不机械凑数。
2. 每篇 2–4 幅框图、8–15 个实验结果图表；所有结果图从冻结 CSV/JSON 生成，禁止手填图中数值。
3. 至少一个真实或人工金标数据来源；合成或智能体辅助数据必须单独标识并披露生成与审核过程。
4. 主结论同时有主结果、消融、鲁棒性/敏感性、效率/成本和错误分析支持。
5. 同一测试实例上的方法比较使用配对统计；报告效应量、95% CI、多重比较校正和失败案例。
6. 代码从空输出目录可执行；固定依赖、随机种子、数据哈希、模型版本、提示词哈希和运行环境。
7. 三轮评审后 Critical 与 Major 问题均为 0；所有意见有 comment ID、证据、修改位置和回复。
8. MDPI 模板编译无错误、无未定义引用、无占位符；Author Contributions、Funding、Data Availability、Conflicts of Interest、伦理/AI 使用声明完整。
9. 本地缓存不等于允许再分发：每个进入论文/补充材料的数据源都必须保存许可证或明确只发布来源 URL、哈希、抽取脚本和派生 schema。

### 1.2 停止并请求用户决策的条件

- 需要新的收费 API 且预计费用超过预先批准的预算上限。
- 需要真实人类/领域专家标注，而作者无法安排最低审核量。
- 数据许可证不允许派生数据集再分发或论文使用。
- 新实验推翻当前核心结论，必须实质性改题或改变贡献边界。
- 两篇论文出现不可消除的数据/贡献重叠，可能构成切香肠或重复发表风险。

## 2. 目标刊画像带来的设计原则

10 篇 Applied Sciences 同主题 Article 的样本中位数为 24 页、7098 正文词、5 个一级节、26 个显示公式、1 个独立数据集/算例、9 幅图、5 张表、2 幅框图和 8.5 个实验结果图表。规划采用以下同期刊模式：

- 借鉴 Grid RoBERTa 论文：自建领域数据必须单列数据构建、标签体系与质量控制。
- 借鉴 DNN 电压控制论文：真实量测输入与仿真/执行标签可以组合，但来源和派生关系必须透明。
- 借鉴规划与调度论文：增加场景、规模、参数敏感性和工程可行性，而非只报单一准确率。
- 借鉴三数据集负荷预测论文：通用方法应做跨数据集验证，避免只在一个自建数据集上成立。
- 借鉴 GNN+LP 机组组合论文：跨系统规模验证、运行时间和失败率是算法应用价值的一部分。
- 借鉴 Graph-Mamba 与风机疲劳论文：真实数据、机制解释、可解释性和局限性应与主精度结果并列。

两篇的首选投稿路由均为 Applied Sciences **Computing and Artificial Intelligence** Section：MA-SQLGrid 对应 Database/Information Systems/Generative AI application，C2GES 对应 NLP/Information Retrieval/Explainable AI。Electrical, Electronics and Communications Engineering 可作为第二路由，但只有当主叙事更偏电网工程流程而非 AI 方法时选择。默认投 regular Section；Special Issue 仅在最终稿完成时重新核验 Guest Editor、范围与截止日期，不为追赶 SI 截止期牺牲人工审核和 sealed test。

## 3. 论文 A：MA-SQLGrid

### 3.1 建议标题

保守方案（优先）：

> **MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power-Grid Maintenance Databases**

若新增真实运行/故障数据库后需要扩大范围，只改一个短语：

> **MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power-Grid Maintenance and Operational Databases**

### 3.2 新核心主张

MA-SQLGrid 不是“提示词技巧”，而是面向电网维护/运行数据库的可审计 text-to-SQL 系统：紧凑上下文、领域值规范化、答案形状约束和参考答案无关的执行验证共同提高严格答案契约遵从，并降低 token、延迟和无效查询风险；只有新实验同时改善 order-insensitive/content 指标时，才能进一步声称改善了行内容检索。

当前 CMC 正式稿已有约 20 页、8558 正文词、6 个一级节、6 个公式、3 张主表、2 幅正文图和 46 条引用，文字规模已经达标，主要缺口是单一合成小库、因子未隔离、外部有效性和可视证据不足。现有 C4 相对 C2 的 strict execution accuracy 提升在 projection-tolerant 指标下反转；原模型 C5−C4 也不显著，必须作为诊断而非确定性收益。

### 3.3 研究问题

| RQ | 问题 | 所需证据 |
|---|---|---|
| MA-RQ1 | 完整流水线是否优于标准 text-to-SQL 基线？ | 多数据库、至少 2 个 API/本地模型、配对主结果 |
| MA-RQ2 | 紧凑上下文与答案形状各自贡献多少？ | 已注册的 full/compact × no-shape/shape 2×2 因子实验 |
| MA-RQ3 | 验证器何时真正修复，何时误修？ | repair precision/recall、净增益、错误转移矩阵、案例 |
| MA-RQ4 | 方法对规模、噪声、别名和模式变化是否稳健？ | 行数 ×10/×100、干扰表、列重命名、同义词、缺失值 |
| MA-RQ5 | 工程代价是否可接受？ | token、成本、p50/p95 延迟、重试率、SQL 执行时间 |
| MA-RQ6 | 能否迁移到未见数据库/未见查询模板？ | 数据库级和模板级严格隔离测试 |

### 3.4 数据集计划

| 数据层 | 来源 | 目标规模 | 用途 | 状态/要求 |
|---|---|---:|---|---|
| MA-D1 | GridDB-Maintenance-v2 v0.1 | 200 问题；冻结的 20 dev/180 test | 复现当前论文与主因子实验 | 已有；保持不可变 |
| MA-D2 | 本地 RTS-GMLC | 建议 180–300 问题 | 构建机组—时序—成本—约束—调度运行关系库 | 优先；标准公开系统，核验许可 |
| MA-D3 | 本地 SimBench | 建议 180–300 问题 | 构建资产—拓扑—电压等级—负荷/DER 关系库 | 优先；与 D2 模式不同 |
| MA-D4（可选外部有效性） | DGADB/DGANN 或 LBNL PMU Event Library | 100–180 问题 | 维护诊断或事件数据库零样本迁移 | 仅在 D1–D3 按期完成后执行 |

每个新库必须包含 `schema.sql`、SQLite 数据库、字段字典、来源/许可、问题与 gold SQL、执行结果哈希、查询模板族、难度标签、dev/test 划分、双重审核日志。模板生成的自然语言必须经过去模板化改写和抽样人工审核；同一模板族不得跨训练/测试泄漏。

现有 Q001–Q200 已被主实验、消融、调权、宽松指标和修复分析反复使用，不能继续称为完全未见测试。必须另建 sealed test：按“数据库 × 模板家族 × 语义意图”分组，至少 50–100 个从未用于开发的问题/数据库，其中 15%–20% 由真实人员提问或深度改写；sealed test 在方法和阈值冻结后仅运行一次。

### 3.5 方法与基线矩阵

核心条件：

1. Schema-only direct prompting。
2. Full schema + sampled values direct prompting。
3. CHESS-lite/generic schema linking baseline。
4. Compact context without answer-shape hints。
5. Full context with answer-shape hints。
6. Compact context with answer-shape hints。
7. MA-SQLGrid full pipeline without validator。
8. MA-SQLGrid full pipeline with bounded validator/repair。

模型层建议：一个当前闭源轻量模型、一个不同供应商模型、一个可在 RTX 3090 上运行的 7B–14B 开源代码/SQL 模型。正式比较冻结模型快照、温度和解码参数；若服务端模型漂移，保存返回时间、模型标识与完整响应哈希。

### 3.6 指标与统计

- Strict execution accuracy、content/projection-tolerant execution accuracy、valid SQL rate、test-suite accuracy。
- Schema-linking recall、answer-shape accuracy、validator trigger/repair precision、repair recall、harm rate。
- 输入/输出 token、美元成本、p50/p95 API 延迟、SQLite 执行时间、重试率。
- 对同一问题的成败结果使用 McNemar exact test；准确率差用问题级配对 bootstrap 95% CI；多条件比较做 Holm 校正。
- 随机模型至少 5 个种子；温度 0 服务至少 3 次一致性复核或对 25% 分层样本复核。

### 3.7 鲁棒性与错误分析

- 数据库规模：原始、10 倍、100 倍行数。
- 模式扰动：0/2/5/10 个语义相似干扰表、列顺序变化、别名、描述缺失、相似列名；full 与 compact 路径必须接收同一扰动数据库，禁止现有“干扰表只进入 full schema”的不对称设计。
- 语言扰动：电网缩写、口语、同义词、数值单位变化、中英术语混排（若数据支持）。
- 查询复杂度：单表、连接、嵌套、聚合、时间窗口、排序/Top-k。
- 错误分类：schema、value、join、filter、aggregation、projection/order、syntax、validator harm。

### 3.8 目标图表

框图：总体流水线；跨数据库实验协议；验证器决策/修复流程。结果图：主准确率与 CI、因子交互图、跨数据库热图、错误转移 Sankey/矩阵、规模鲁棒性、token–accuracy Pareto、延迟箱线图、典型成功/失败案例。主文目标 9–12 Figure、6–8 Table，其余进 Supplementary。

### 3.9 章节目标

1. Introduction：900–1200 词，3 个明确 gap，3–4 项贡献。
2. Related Work：800–1000 词，text-to-SQL、验证/修复、工业数据库问答。
3. Materials and Methods：2600–3300 词，任务、数据、方法、复杂度和可复现协议。
4. Experimental Setup：900–1300 词，数据库、基线、模型、指标、统计。
5. Results and Discussion：2300–3000 词，按 RQ 组织而非按图表流水账。
6. Conclusions：300–450 词，工程意义、局限和下一步。

### 3.10 MA-SQLGrid Go/No-Go

- Go：D1 因子实验完成；至少 D2 完成并无泄漏；完整方法在至少两个数据库上优于强基线，且 validator harm rate 被量化并受控。
- 已冻结的 2×2 factorial 目前只有 720 个 prompts，`prediction_count=0`；执行入口仍落到不可用的原 Krill responses wire。P0 必须先改成可配置 OpenAI-compatible endpoint，并保留 prompt/model/response hash。
- 答案形状规则与当前数据标注协议共同设计且 180/180 匹配，存在循环性风险；新库必须由独立标注/审核流程生成，并增加 shape-blind/shape-perturbation 审计。
- 降级方案：若 D2/D3 建库质量不足，题目保持 maintenance database，D1 作为主 benchmark，但增加严格因子、三模型、规模与模式扰动，明确单库局限。
- No-Go：跨数据库结果反向且无法给出诚实边界，或 gold SQL/执行结果混入提示或选择过程；safe SQL 低于 100% 或 provider failure 超过 1% 时先修系统，不进入论文组装。

建议量化门槛：2×2 因子在 2 个模型 × 3 次重复上完成；Compact 相对 Full 在相同 shape 条件下两模型均至少 +5 percentage points 且 95% CI 不跨 0；Shape 主效应同向为正；外部数据库平均提升至少 +5 points、任一数据库不劣于 −3 points；重复最大 spread ≤2 points、逐题 verdict agreement ≥97%；全部运行 trace/config/hash 覆盖率 100%。若未达到，门槛用于降级主张而不是伪造“通过”。

## 4. 论文 B：C2GES

### 4.1 建议标题

以当前最新版标题作小幅应用化调整：

> **Learnable Role-Conditioned Evidence Sentence Selection for Power-Grid Reliability Reports with Interpretable Mixture Reranking**

若 NERC 只能做案例而不能形成可信定量集，则保留当前标题：

> **Learnable Role-Conditioned Evidence Sentence Selection with Interpretable Mixture Reranking**

不得在只有定性 NERC 案例时把 “for Power-Grid Reliability Reports” 写成已验证的主任务范围。

### 4.2 新核心主张

C2GES 是一种轻量、可解释的角色条件证据句重排器。它将通用查询相关性、可学习角色兼容性和局部因果链一致性组合起来，在人工金标事实核查数据上验证学习有效性，并在 NERC 电网可靠性报告上验证跨域应用、角色可审计性和工程检索价值。

### 4.3 研究问题

| RQ | 问题 | 所需证据 |
|---|---|---|
| C2-RQ1 | 角色条件学习是否优于通用稀疏/稠密检索？ | FEVER 主结果，5 种子，强 reranker 基线 |
| C2-RQ2 | 角色头、局部图/链和混合约束是否必要？ | 完整消融、交互和权重分析 |
| C2-RQ3 | 对 K、文档长度、角色分布和查询改写是否稳健？ | K=1/3/5/10、长度分层、角色分层、paraphrase |
| C2-RQ4 | 是否能迁移到电网可靠性报告？ | NERC 定量审计集或诚实的定性+专家审核 |
| C2-RQ5 | 输出是否更可审计、更节省专家阅读成本？ | evidence coverage、冗余率、阅读压缩率、案例/专家评价 |
| C2-RQ6 | 精度收益是否值得计算代价？ | 参数量、训练/推理时间、GPU/CPU 内存、吞吐量 |

当前 FEVER 代码把 human-gold SUPPORTS/REFUTES 标签作为输入角色，因此现有结果只能称为 **oracle-label-conditioned evidence selection**。正式研究必须另外加入 label-blind 与 predicted-label 两种协议，不能把 oracle 条件结果当作标准 FEVER 检索结果。

### 4.4 数据集计划

| 数据层 | 来源 | 规模 | 用途 | 约束 |
|---|---|---:|---|---|
| C2-D1 | FEVER human-gold conversion | 4000 train/800 dev/800 test | 人工金标主学习与统计实验 | 保持文档/claim 隔离，冻结转换脚本 |
| C2-D2 | 本地 40 份 NERC 官方报告 | 40 文档 × 5 角色 = 200 查询 | 电网跨域验证 | 公开 PDF 不等于金标，必须补标签审计 |
| C2-D3（可选） | NERC 报告年份/事件类型 OOD 切分 | D2 的时间外或事件外子集 | 跨年份/事件迁移 | 不得把同一报告段落分到两侧 |

NERC 标签推荐三层流程：智能体 A/B 独立预标 → 智能体 C 冲突定位 → 作者/领域专家对全部冲突和至少 25% 无冲突样本人工复核。报告 raw agreement、Krippendorff's alpha 或多标签 F1、冲突率和仲裁规则。若没有真实人工复核，只能称 AI-assisted silver labels，不得称 human-gold。

高成功率方案要求至少两名具备电力系统背景的真实标注者独立标注 20–30 份报告、100–150 个问题，并由第三位真实人员裁决。智能体只能预标、整理冲突和生成审核界面，不能冒充人工专家。NERC 报告按事件家族分组，另做“过去年份 → 未来年份”外推；同一事件的年度报告、事件报告和建议报告不得跨训练/测试。

FEVER 转换数据本地实际可用约 10,000 train、1913 dev、1673 test，当前论文只取 4000/800/800。正式冻结前必须按原始 Wikipedia `title/document_id` 检查和重做分组；当前 800 个测试实例只覆盖约 292 个底层文档，现有代码却把 claim ID 写入 `doc_id`，所以旧的“document-cluster bootstrap”接近实例 bootstrap，旧 CI/p 值不得直接沿用。

### 4.5 方法与基线矩阵

基线：Lead-k、TF-IDF、BM25、TextRank/LexRank、SBERT、cross-encoder MiniLM、BGE reranker、query-only learnable model、lexicon-cue role model、零样本 LLM reranker（成本受控）。

消融：无角色头、无局部链、无 mixture floor、固定词典角色、点式损失替代 pairwise loss、冻结/微调编码器、不同候选池大小。已准备的 cross-encoder/BGE/LLM 脚本优先复用，结果不存在时不得在文中占位宣称。

任务协议必须平行报告：① oracle-label（给定 SUPPORTS/REFUTES）；② predicted-label（先预测标签再检索）；③ label-blind（完全不提供标签）。只有后两者可支持标准端到端证据检索主张。

### 4.6 指标与统计

- Evidence precision/recall/F1@K、Recall@K、MRR、nDCG@K、ROUGE-L。
- 角色宏平均/微平均、最差角色性能、长短文档分层性能。
- 阅读压缩率、证据冗余率、每查询延迟、吞吐量、显存/内存。
- 5 个训练种子报告 mean±SD；以文档/claim cluster bootstrap 给 95% CI；与主基线做配对 permutation/Wilcoxon，并 Holm 校正。
- 所有 cluster bootstrap 必须按底层 Wikipedia 文档或 NERC 报告聚类，不得按带 claim ID 的伪文档 ID 聚类。
- 同时报告绝对增益、相对增益和置信区间，禁止只突出相对百分比掩盖低绝对值。

### 4.7 NERC 应用验证

- 五角色：root cause、trigger event、propagation/response、impact、mitigation。
- 角色混淆矩阵；每角色 P/R/F1；跨报告年份和长度分层。
- 证据链连续性、跨段落证据覆盖、重复证据率。
- 至少 10 个可审计案例：正确、部分正确、语义相关但角色错误、跨段传播失败、表格/OCR 失败。
- 若能安排专家：盲评 C2GES/BM25/BGE 三种输出的 relevance、role fit、actionability，至少 2 名评审、30–50 个查询；否则不做“专家研究”声明。

### 4.8 目标图表

框图：数据/任务定义；C2GES mixture architecture；NERC 标注与审核流程。结果图：FEVER 主结果 CI、5 种子分布、K 敏感性、角色性能雷达/条形图、消融瀑布图、权重与案例可解释图、文档长度鲁棒性、NERC 角色混淆矩阵、精度–延迟 Pareto。主文目标 9–12 Figure、6–8 Table。

### 4.9 章节目标

1. Introduction：900–1200 词，强调可审计电网报告分析。
2. Related Work：800–1100 词，事实核查、证据选择、角色/因果检索、电网 NLP。
3. Data and Task：1000–1400 词，FEVER 转换与 NERC 审核协议。
4. Proposed C2GES Method：2000–2600 词，公式、训练目标、复杂度、解释性。
5. Experiments, Results and Discussion：2600–3300 词，按 RQ 组织。
6. Conclusions：300–450 词，应用边界、OCR/表格/跨段局限。

### 4.10 C2GES Go/No-Go

- Go：FEVER 五种子完成；至少加入 cross-encoder 与 BGE；role/no-role 增益跨种子稳定；NERC 有可信人工审核或明确 silver-label 限定。
- 现有单种子 FEVER K=3 结果仅支持谨慎结论：C2GES F1 约 0.5066，与 BM25 约 0.5030 统计持平；角色头相对 no-role 有小幅增益。正式稿不得写“全面优于 BM25”，除非新协议和五种子结果确实支持。
- 旧 NERC silver-label 结果中 zero-shot DeepSeek F1 约 0.5887，明显高于 C2GES 约 0.2983；若人工金标仍呈现这一格局，论文主张必须转为“准确率—成本—确定性—可审计性的 Pareto 权衡”，不能以最高精度为中心。
- 降级方案：NERC 无法形成可信定量集时，标题不宣称 power-grid 主验证，FEVER 为主、NERC 只作 case study，并把域迁移列为局限。
- No-Go：把智能体标注写成人工金标；同一 FEVER 文档跨划分；与 BM25/BGE 统计持平却宣称全面优越。

建议量化门槛：至少 8 个正式基线、5 个种子、K=1/3/5/10；五个种子至少四个保持 Full−No-role 同方向，平均增益目标 ≥0.010 且 95% CI 不跨 0；相对 BM25 的配对差异下界不低于 −0.01（统计不劣）；若有人类 NERC 金标，目标相对 BM25 ≥0.03 且 CI 不跨 0。人工标注双人集合 F1 目标 ≥0.80、句级 κ ≥0.75。性能门未达到时转向可审计性/效率贡献，不能修改数据或挑选子集来“达标”。

## 5. 两篇论文的差异化与重叠控制

| 维度 | MA-SQLGrid | C2GES |
|---|---|---|
| 核心任务 | 结构化数据库 text-to-SQL | 非结构化报告证据句检索 |
| 主数据 | SQLite 维护/事件数据库 | FEVER + NERC 文本报告 |
| 输出 | 可执行 SQL 与答案 | 可追溯 sentence IDs |
| 主要创新 | 上下文、答案契约、执行验证 | 角色头、mixture reranking、局部因果链 |
| 工程价值 | 数据库查询自动化与安全验证 | 可靠性报告审查与证据追踪 |
| 禁止复用 | 不使用 C2GES 的 NERC 标注作主 SQL 贡献 | 不使用 MA 的 SQL 问题/结果作检索样本 |

可共享背景文献、可复现框架和统计工具；不得复制引言段落、图、实验结果或把同一数据贡献在两篇中分别声称为首创。

## 6. 多智能体组织

实际并发上限为“总智能体 + 3 个工作智能体”，因此采用波次并行。所有工作智能体向独立 staging 文件或结果目录写入；只有总智能体可修改主 TeX、总表和最终图号。

### 6.1 总智能体

**PI-Integrator**：冻结范围与 claim ledger；批准实验 manifest；调度依赖；解决两篇重叠；整合正文、引用、图表和声明；运行编译与最终一致性检查；任何数值进入论文前追溯到 canonical result file。

### 6.2 写作智能体池

- W-MA-Method：MA 数据、方法、算法与复杂度。
- W-MA-Results：MA 实验、结果、错误分析和讨论。
- W-C2-Method：C2 数据、标注、方法与训练目标。
- W-C2-Results：C2 实验、跨域结果、解释性和局限。
- W-Literature：两篇独立的相关工作矩阵、2024–2026 参考更新和引用核验。
- W-Compliance：摘要、关键词、Data Availability、Author Contributions、Funding、COI、AI 使用披露与补充材料索引。

写作智能体不得直接编辑主稿；交付为 section draft + claim-to-evidence 表。无结果支持的句子标记 `[PENDING-EVIDENCE]`。

### 6.3 实验与数据智能体池

- E-MA-Data：D2/D3 建库、gold SQL、划分、泄漏和许可审计。
- E-MA-Factorial：2×2 因子、基线、跨模型正式运行。
- E-MA-Robustness：规模/模式/语言扰动、效率和 validator harm。
- E-C2-Data：FEVER 冻结与 NERC 预标/冲突包。
- E-C2-Models：五种子训练、消融和 K 敏感性。
- E-C2-Baselines：BM25/SBERT/cross-encoder/BGE/LLM 基线。
- E-Statistics：独立读取 canonical predictions，复算 CI、检验、效应量和多重校正。
- E-Reproducibility：从空目录运行 smoke/full command，核查环境、哈希、随机性和日志完整性。

### 6.4 图表智能体池

- V-Architecture：两篇总体框图、组件图和数据流程图，统一视觉规范但不复用版式。
- V-Results-MA：只从 MA canonical tables 生成主结果、交互、鲁棒性、Pareto 和错误图。
- V-Results-C2：只从 C2 canonical tables 生成种子、K、角色、混淆和 Pareto 图。
- V-QA：核对图中数值、单位、颜色盲友好、灰度可辨、字体、300/600 dpi 和缩小后可读性。

### 6.5 三轮专家评审智能体

第一轮“科学有效性”：

- R1-Method：任务定义、方法新颖性、基线公平性。
- R1-Stats：统计单元、CI、种子、显著性和结论强度。
- R1-Data：许可、划分、标签、泄漏和可复现性。

第二轮“应用与期刊适配”：

- R2-Power：电力系统场景真实性、工程术语、应用价值。
- R2-AppliedSciences：Section/期刊 fit、广泛读者可读性、同期刊对标。
- R2-VisualNarrative：图表证据链、章节节奏、讨论与局限。

第三轮“拒稿压力测试”：

- R3-Skeptic：以最苛刻 Reviewer 2 角度寻找夸大、薄弱基线和反例。
- R3-ClaimsCitations：逐句 claim-evidence-citation 审计、两篇重叠检查。
- R3-Submission：模板、声明、引用、图分辨率、补充材料、编译和匿名信息检查。

### 6.6 受 4 并发槽约束的执行波次

| 波次 | Worker A | Worker B | Worker C | PI-Integrator 同步工作 |
|---|---|---|---|---|
| W0（已完成） | MA 只读审计 | C2 只读审计 | 本地数据/资产审计 | 建立总目标与路线 |
| W1 科学阻断修复 | MA API/factorial 协议 | C2 文档分组与三协议 | 统计测试与 leakage tests | 审批 manifest v1 |
| W2 数据工程-A | MA RTS-GMLC DB | MA SimBench DB | MA gold SQL/审核包 | 冻结数据卡与许可 |
| W3 数据工程-B | C2 FEVER 重分组 | C2 NERC 预标/冲突包 | NERC 审核工具与 agreement | 冻结 title/claim 边界 |
| W4 Pilot | MA 10% pilot | C2 10% pilot | 复现/成本审计 | Go/No-Go 决策 |
| W5 正式实验-A | MA 因子/基线 | MA 跨库/鲁棒性 | MA 效率/错误分析 | 冻结 MA predictions |
| W6 正式实验-B | C2 五种子/消融 | C2 强基线 | C2 NERC/跨域 | 冻结 C2 predictions |
| W7 独立分析 | 配对统计 | 错误/案例审计 | 复现重跑 | 冻结 canonical tables |
| W8 写作-1 | MA 方法/实验 | C2 方法/实验 | 相关工作/合规 | 组装 Draft 1 |
| W9 图表 | 架构图 | MA 结果图 | C2 结果图 | 编号、图注和正文引用 |
| W10 Review 1 | 方法专家 | 统计专家 | 数据专家 | Revision 1 组装 |
| W11 Review 2 | 电力专家 | Applied Sciences 编辑视角 | 视觉叙事专家 | Revision 2 组装 |
| W12 Review 3 | Skeptical Reviewer 2 | Claim/citation 审计 | 投稿合规审计 | Revision 3 与交付 |

每个波次结束后才允许下一个依赖波次启动；审稿智能体只读，不能一边评审一边自行修稿。

## 7. 三轮修改闭环

每轮评审输出 `review_round_N/{paper}/comments.md`，字段固定为 `ID / severity / location / evidence / requested action / acceptance test`。

### Round 1 → Revision 1

优先修复数据、方法和统计。实验智能体重跑受影响条件，写作智能体只更新受影响小节；PI-Integrator 更新 claim ledger。验收：Critical=0，所有 Major 有结果文件或明确降级结论。

### Round 2 → Revision 2

强化应用场景、工程解释、跨学科可读性、图表证据链和真实局限。验收：每项贡献均回答“谁使用、在哪个流程使用、带来什么量化收益、在哪些条件下失效”。

### Round 3 → Revision 3

执行拒稿压力测试和投稿合规收口。禁止新增未充分验证的大主张；只做证据补强、措辞降级、引用/图表/格式修复。验收：Critical/Major=0，Minor 全关闭或有书面理由，主稿可从干净环境编译。

## 8. 阶段、依赖与建议时程

| 阶段 | 典型时长 | 并行工作 | 出口门槛 |
|---|---:|---|---|
| P0 冻结与注册 | 2–3 天 | 两篇基线、数据/模型/API 审计 | baseline hash、claim ledger、manifest v1 |
| P1 数据工程 | 1–2 周 | MA D2/D3；C2 FEVER/NERC | 数据卡、许可、划分、泄漏测试通过 |
| P2 Pilot | 3–5 天 | 两篇各 10% 样本 | 代码、指标、日志、成本估计通过 |
| P3 正式实验 | 1–2 周 | MA 主矩阵；C2 五种子/基线 | canonical predictions 冻结 |
| P4 鲁棒性与统计 | 1 周 | 扰动、效率、CI、错误分析 | 所有主要结论可追溯 |
| P5 图表与初稿 | 1–2 周 | 写作池与图表池 | 两篇 Draft 1 编译通过 |
| P6 第一轮评审/修改 | 4–6 天 | 三专家 + Revision 1 | 科学 Major 清零 |
| P7 第二轮评审/修改 | 4–6 天 | 三专家 + Revision 2 | 应用/叙事 Major 清零 |
| P8 第三轮评审/修改 | 3–5 天 | 三专家 + Revision 3 | 投稿检查全部通过 |

总体为约 8–12 周的稳健路线；若不做人工 NERC 审核或跨数据库数据构建，可缩短，但论文说服力也相应下降。

当前 PyTorch 为 CPU 构建，RTX 3090 尚不能直接用于训练；进入 W4 前需安装并验证 CUDA 版 PyTorch。Cross-encoder、BGE 与本地 7B/14B 模型权重尚未缓存，下载量与许可证须计入 P0；API 条件需先做 10% pilot 和费用上限审批。

## 9. 文件与交接规范

建议新执行根目录：`paper_projects/applied_sciences_dual_rebuild/`。

```text
MA_SQLGrid/
  frozen_baseline/  data/  configs/  runs/  canonical/  figures/  drafts/  reviews/
C2GES/
  frozen_baseline/  data/  configs/  runs/  canonical/  figures/  drafts/  reviews/
shared/
  environment/  style/  claim_ledgers/  review_templates/
```

- 原始 CMC/IEEE 源稿只读冻结，不在原目录直接开展多人并行改写。
- 每次运行都有 `run_id`、git commit/hash、config、seed、start/end time、stdout/stderr、environment lock 和输出校验和。
- `canonical/` 只由 PI-Integrator 在验收后写入；图表和正文只读取这里。
- 表格中的每个数字可追溯到 `run_id + row key`；正文主张可追溯到表/图/统计检验。
- 并行智能体不得同时编辑同一文件；冲突通过 staging 合并，不通过覆盖解决。

## 10. 优先执行顺序

1. 冻结两篇当前最新版及所有已有结果，建立 dirty-worktree 清单，不清理用户文件。
2. 完成 MA 已注册 2×2 因子实验和 C2 五种子 FEVER sweep；这是成本最低、信息增益最高的现成补强。
3. 运行 C2 cross-encoder/BGE 基线；决定其与 BM25 的真实位置。
4. 对 MA-D2/D3 做小样本数据可行性 pilot；只扩展通过质量门槛的数据库。
5. 决定 NERC 是否能完成真实人工审核；据此冻结 C2GES 标题和 claim 边界。
6. Pilot 通过后再启动完整 API/GPU 实验，避免大规模无效运行。
7. 结果冻结后才进入并行写作和图表阶段。
