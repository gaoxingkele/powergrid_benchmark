# “原标题版”资产整合与证据边界矩阵

日期：2026-08-08（Asia/Shanghai）  
审计性质：只读资产审计，不是论文修改稿，不是实验完成声明  
目标：判断两份 CMC 原标题 DOCX、2026-08-08 上午生成的审稿/完整包，以及当前 Applied Sciences LaTeX 中的哪些内容可以进入“原标题版”，哪些必须重新计算，哪些只能作为诊断，哪些仍然缺失。

## 1. 状态定义

| 状态 | 含义 | 进入原标题版的条件 |
|---|---|---|
| **可直接继承** | 当前本地证据能支持同一任务、同一端点和同一边界下的陈述 | 保留原有来源标识、限制语和哈希/账本；不得扩大主张 |
| **需重算/重冻结** | 有代码、数据或结果基础，但代码版本、任务定义、端点或原标题主张发生变化 | 先冻结协议与资产哈希，再运行；新旧结果分开标记 |
| **仅诊断** | 可用于方法动机、流程验证、稳健性诊断或未来工作，但不能支撑原标题核心性能主张 | 明确标成 diagnostic / machine-silver / auxiliary，不进入主结论的优越性声明 |
| **缺失** | 当前审计范围未发现可核查实现、数据、预测账本或结果来源 | 补实现、补数据、补评价器并完成冻结实验；在此之前不得写成已完成 |

“可直接继承”不等于文字原样复制。原标题 DOCX 中缺少来源绑定的定量结果，即使数值看似合理，也不能因为概念与当前项目相似而继承。

## 2. 审计来源与客观盘点

### 2.1 两份 CMC 原标题 DOCX

1. `D:\aicoding\powergrid_benchmark\paper_projects\CMC\1副本Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports(1).docx`
   - 标题：**Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports**。
   - 325 个非空 OOXML 段落，约 7141 个空白分词词元、49,561 个字符。
   - 7 个正文章节，另有 References 和 Appendix；5 个 Word 表格。
   - DOCX 包内 `word/media/` 文件数为 **0**，即原稿没有实际嵌入的图像或算法框图。
   - OOXML 中检测到 72 个 `oMath` 节点、4 个数学段落；这说明原稿包含公式对象，但不证明公式对应的算法已经实现。

2. `D:\aicoding\powergrid_benchmark\paper_projects\CMC\1副本MA-SQLGrid_ A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases(1).docx`
   - 标题：**MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases**。
   - 427 个非空 OOXML 段落，约 9649 个空白分词词元、67,813 个字符。
   - 7 个正文章节，另有 References 和 Appendix；7 个 Word 表格。
   - DOCX 包内 `word/media/` 文件数为 **0**。
   - OOXML 中检测到 10 个 `oMath` 节点、1 个数学段落。

原稿的章节、表格和公式对象是真实存在的文档资产；原稿表内数值是否来自已运行实验，是另一个问题，必须由预测账本、数据清单、代码和运行记录证明。

### 2.2 09:15 审稿核查包

1. `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\reviewer_packages\C2GES_submission_review_2026-08-08.zip`
   - 102 个文件；ZIP 大小 1,450,713 字节；解压后文件总大小 7,889,446 字节。
   - 包含当前 Applied Sciences 稿、PDF、结果表、预测与标签账本、协议、验证脚本和 `SHA256SUMS.csv`。
   - 包内只有 2 个 Python 文件，均为稿件结果生成/核验脚本：`generate_canonical_tex.py`、`verify_claim_sources.py`；**不含 C²GES 主训练/推理算法源码**。
   - BGE 预测账本有 6000 行；NERC machine-silver development/frozen 最终标签各 75 行。

2. `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\reviewer_packages\MA_SQLGrid_submission_review_2026-08-08.zip`
   - 132 个文件；ZIP 大小 2,743,405 字节；解压后文件总大小 12,437,097 字节。
   - 包含当前稿件、PDF、BIRD 调用账本、GridDB 分析、语义可靠性、组件实验、machine-silver 标签和哈希清单。
   - 包内 8 个 Python 文件是分析、发布构建、输入核验和测试脚本；**没有发现原标题所述五智能体协商/投票系统的完整生成运行器**。
   - BIRD：Qwen 与 Granite 的调用账本各 2500 行，最终预测各 2000 行；合计 5000 次生成调用、4000 条最终预测。
   - GridDB canonical rows 为 1440 行；15-state suite outcomes 为 1440 行。
   - MA machine-silver development/frozen 最终标签分别为 121 行和 115 行。

### 2.3 09:25 完整投稿包

1. `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\email_delivery_2026-08-08\C2GES_Applied_Sciences_complete_2026-08-08.zip`
   - 164 个文件；ZIP 大小 3,473,913 字节；解压后文件总大小 15,515,819 字节。
   - 相比 09:15 包增加 MDPI class/style、完整 LaTeX 工程、框图/结果图、最终 PDF 和验证数据副本。
   - Python 资产仍以构建和稿件核验为主，不包含主训练/推理源码。

2. `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\email_delivery_2026-08-08\MA_SQLGrid_Applied_Sciences_complete_2026-08-08.zip`
   - 181 个文件；ZIP 大小 4,607,051 字节；解压后文件总大小 15,515,134 字节。
   - 增加完整 MDPI LaTeX、框图、结果图、最终 PDF和验证数据副本。
   - 包含结果重分析/发布脚本，但未发现原标题五智能体协商系统的完整生成运行器。

09:25 包主要是 09:15 审稿核查资产的“投稿可携带版本”，不是另一次独立实验。因此不能把两份包中重复的结果算成两套重复验证。

### 2.4 当前 Applied Sciences LaTeX

1. C²GES：`D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\C2GES\manuscript_applsci\paper_applsci.tex`
   - 当前标题：**Learnable Role-Conditioned Evidence Sentence Selection with Interpretable Mixture Reranking**。
   - 6 个主章节，10 个表格环境、9 个图环境、5 个公式环境。
   - 量化任务是 supplied-document FEVER evidence sentence selection，不是报告级摘要。
   - 当前文稿明确说明：local channel 是位置平滑，不是因果结构；没有推断物理因果图；NERC 标签是 machine-adjudicated silver，不是 domain-expert gold；不报告 NERC selector performance。

2. MA-SQLGrid：`D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\paper_applsci.tex`
   - 当前标题：**MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power Grid Maintenance Databases**。
   - 6 个主章节，9 个表格环境、9 个图环境、8 个公式环境。
   - 当前证据支持固定 multi-stage pipeline、prompt/context 因子、执行修复与可靠性诊断；文稿没有把它描述成已验证的五自主智能体协商系统。

另有 CMC 目录中的 Applied Sciences 副本：

- `D:\aicoding\powergrid_benchmark\paper_projects\CMC\C2GES\06_Applied_Sciences_Current\paper_applsci.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\CMC\MA-SQLGrid\06_Applied_Sciences_Current\paper_applsci.tex`

它们的内容规模和版本与 `applied_sciences_dual_rebuild` 下当前稿不同。原标题版整合时应先指定单一权威 LaTeX 根目录，避免两个“current”来源继续分叉。本报告将 `applied_sciences_dual_rebuild/*/manuscript_applsci/paper_applsci.tex` 视为本次上午包对应的权威当前稿。

## 3. C²GES 原稿主张清单

原稿章节结构为：Introduction；Related Work；Problem Formulation；The C²GES Method；Experimental Setup；Results and Analysis；Conclusion；另有 References 与 Appendix。

原稿提出的核心算法链为：

1. 从维护报告抽取 causal events/relations 并建立 causal graph；
2. 用 GNN/GAT 对因果句图编码；
3. 用 fine-tuned T5 生成 minimal counterfactual sentence；
4. 将反事实响应作为 causal importance 信号；
5. 结合语义、图结构与反事实分数选择 extractive summary。

原稿提出但当前上午包未找到对应来源绑定的主要数据/结果包括：

- `GridMaint-CausalSum`：500 documents，平均 45 句、参考摘要 4 句，80/10/10 划分；声称由电气工程/NLP 研究生人工标注摘要和 causal graph。
- 主表：C²GES 的 ROUGE-1/2/L 为 41.1/18.9/37.6，Graph F1 68.2，QA accuracy 71.5。
- 消融：去 counterfactual 后 Graph F1 54.9；去 GNN 后 44.3；去 causal graph 后 41.3。
- causal relation extraction：SemEval 2010 Task 8 F1 0.886，Causal-TimeBank F1 0.842。
- Pearson correlation between ROUGE-L and Graph F1 = 0.23。

以上数值确实存在于 DOCX 的 Word 表格或正文中，但在四个上午包内没有发现对应的 500-document 数据清单、人工标注账本、训练检查点、summary prediction ledger、causal graph gold、QA evaluator outputs 或统计输出。因此它们当前均不能作为原标题版的已完成实验结果。

## 4. C²GES 资产整合矩阵

| 原标题版要素 | 原稿资产 | 当前/上午包资产 | 状态 | 证据边界与整合方式 |
|---|---|---|---|---|
| 原标题与应用问题 | 原标题、动机、causal fidelity 概念完整 | 当前稿有技术报告检索动机与严格限制语 | **可直接继承** | 保留标题和问题动机；重写贡献，不能保留“已显著优于 BERTSum”等未核查句 |
| 作者与单位 | Liu Bijing、Yang Yong；两单位 | 当前 LaTeX 已有相同作者/单位结构 | **可直接继承** | 通讯邮箱按作者最终人工填写；本审计不验证身份或邮箱 |
| 句子编码/查询相关性 | 原稿有 BERT/GNN 叙述 | 当前真实实现为 MiniLM embedding + TF–IDF/query channel | **可直接继承（基础模块）** | 可以成为原标题版 lexical/semantic base scorer，不得称为 GNN |
| role-conditioned score | 原稿有 cause/effect role 设想 | FEVER supports/refutes role head、oracle/predicted/blind 三协议、5 seeds | **可直接继承（辅助实验）** | 只能支持 supplied-document evidence ranking；二元 FEVER role 不是电网因果角色 |
| local graph/chain signal | 原稿称 causal graph/GNN | 当前方法合同是 `exp(-|i-j|/3)` positional smoothing | **仅诊断** | 可作 no-graph/positional baseline；不能改名为 causal graph message passing |
| 真正 causal event graph | 原稿有概念与公式 | 上午包无 event-node/typed-edge graph ledger 或执行代码 | **缺失** | 需要事件节点、边类型、图构建器、序列化图、误差审计和消融 |
| GNN/GAT 编码 | 原稿附表列 2 GNN layers、8 heads | 当前上午包无 GNN 训练/推理实现与 checkpoint | **缺失** | 实现后与 non-GNN/position-only 在同一冻结划分上重算 |
| counterfactual perturbation | 原稿给出 T5 prompt 和分数叙述 | 当前包无 T5 counterfactual ledger、干预规则或模型响应账本 | **缺失** | 需先定义可重复干预、有效性/语义保持检查和失败类别，再运行 |
| extractive summarization selector | 原稿声称 4-sentence reference summary | 当前输出是 evidence sentence IDs at K=1/3/5/10 | **需重算/扩展** | 现有 selector 可作候选打分器；必须新增长度、去冗余、因果角色覆盖和报告级输出 |
| FEVER 8000/1500/1500 | 原稿没有该设计 | 文档分组、745/141/145 个文档、跨划分重叠 0；有哈希和预测 | **可直接继承（辅助基准）** | 只用于证据检索/选择能力，不得写成 power-grid summarization benchmark |
| FEVER 5-seed 主结果 | 原稿无 | K=3 predicted F1 0.4920、BM25 0.4864；role-effect CI 均跨 0 | **可直接继承（辅助结果）** | 保留 negative result；不能改写成因果角色显著有效 |
| BGE/MiniLM 强基线 | 原稿只列 BERTSum/GNN-Sum | BGE 6000-row ledger；K=3 对 full C²GES 差 -0.0021，Holm 后无 promoted finding | **可直接继承（辅助结果）** | 可作为强 reranker 对照，必须保留无显著差异结论 |
| 25-cell crossed seed sensitivity | 原稿无 | 5 upstream × 5 downstream，稿件报告 mean F1 0.4906 | **可直接继承（辅助稳定性）** | 说明它不重新估计原标题中的因果图/反事实效果 |
| NERC 官方报告资产 | 原稿笼统称 maintenance reports | 当前有两套各 75 问题的 disjoint machine-silver 记录 | **仅诊断/数据构造基础** | 可用于协议调试、句子 ID、角色候选和定性案例；不能当作专家金标或 selector accuracy |
| GridMaint-CausalSum 500 docs | 原稿声称已创建并人工标注 | 四个上午包未发现该数据集、标注账本或许可记录 | **缺失** | 不得沿用数据集名称和 500-doc 统计，除非找到原始资产并独立核验 |
| 原稿 ROUGE/Graph F1/QA 数值 | Word 表中存在 | 上午包无相应预测/参考/评价账本 | **缺失** | 从原标题版新数据和冻结评价器重算；旧数值不得进入 Results |
| SemEval/Causal-TimeBank 抽取数值 | Word 表中存在 | 上午包无训练/预测/评价资产 | **缺失** | 若保留此组件主张，需恢复实现与数据版本并重算；否则删除数值 |
| 原稿定性案例 | 有 Substation B/corrosion 人工示例 | 无来源报告 ID、句子 ID 或预测 ledger | **仅诊断** | 可以作为说明性 synthetic example，必须标明 illustrative，不得称为实际测试案例 |
| 当前 9 幅图 | 原稿无嵌图 | 有协议、分组、审计、forest、seed、compute 等图 | **可直接继承/改绘** | 统计结果图可保留；协议图可改造成原标题版子模块图；仍缺完整 causal graph + counterfactual algorithm diagram |
| 代码可复现绑定 | 原稿无 | 方法合同记录三个源码哈希 | **需重冻结** | 见下方哈希冲突；必须恢复旧快照或基于当前源码重跑 |

### 4.1 C²GES 已发现的哈希冲突

上午包中的方法合同：

`D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\reviewer_packages\C2GES_submission_review_2026-08-08\evidence_sources_flat\method_contract__method_implementation_contract.json`

记录：

- `c2ges_learnable.py`：`1dc73962...275f6`
- `predict_fever_labels.py`：`532e846e...80ce`
- `prepare_fever_benchmark.py`：`8f66d987...17a71`

当前本地文件：

- `D:\aicoding\powergrid_benchmark\paper_projects\2026_c2ges_engineeringletters\source\code\c2ges_learnable.py`：`473B36C3...33F8`
- `D:\aicoding\powergrid_benchmark\paper_projects\2026_c2ges_engineeringletters\source\code\predict_fever_labels.py`：`532E846E...80CE`
- `D:\aicoding\powergrid_benchmark\paper_projects\2026_c2ges_engineeringletters\source\code\prepare_fever_benchmark.py`：`8F66D987...17A71`

后二者匹配，`c2ges_learnable.py` 不匹配。因上午 ZIP 不含合同所对应的旧主源码，现阶段不能证明用当前源码可以逐字节重现上午结果。整合决策只能二选一：恢复哈希为 `1dc73962...275f6` 的旧源码快照；或把当前源码连同新增原标题模块重新冻结并重跑受影响实验。不能用旧结果配当前源码后宣称完全可复现。

## 5. MA-SQLGrid 原稿主张清单

原稿章节结构为：Introduction；Related Work；Problem Formulation and Framework Overview；The MA-SQLGrid Framework: Architecture and Protocols；Experimental Setup；Results and Analysis；Conclusion and Future Work；另有 References 与 Appendix。

原稿提出的核心系统为五个 LLM agents：NLU Analyst、Schema Cartographer、SQL Synthesizer、Validation Engine、Counterfactual Reasoner，并声称使用 negotiation、voting、iterative feedback。

原稿提出但当前上午包未找到对应来源绑定的主要数据/结果包括：

- `GridDB-Maintenance`：声称 1000 question–SQL pairs 由 domain experts 手工编写。
- Spider/WikiSQL/GridDB 主结果：MA-SQLGrid EX 分别为 88.2%、93.5%、91.7%。
- Spider ablation：去 Validation Engine -24.6 points；去 Schema Cartographer -18.9；去 NLU Analyst -7.1；去 Counterfactual Reasoner -5.8。
- perturbation robustness：Spider 下降 4.8%，GridDB 下降 3.5%。
- 表 6 的复杂度结果使用 `~` 近似值。

这些数值存在于 DOCX，但四个上午包不含相应 Spider/WikiSQL 预测账本、1000-pair expert-authored GridDB 清单、五智能体消息账本或对应评价输出，故不能作为原标题版现成结果。

## 6. MA-SQLGrid 资产整合矩阵

| 原标题版要素 | 原稿资产 | 当前/上午包资产 | 状态 | 证据边界与整合方式 |
|---|---|---|---|---|
| 原标题与高可靠 Text-to-SQL 问题 | 原标题、工业动机完整 | 当前稿有只读执行、安全、审计和人审边界 | **可直接继承** | 标题可保留；摘要/贡献必须与真正实现的 agent 协议一致 |
| 作者与单位 | Liu Bijing、Sun Chenglong、Yang Yong；两单位 | 当前稿有相同作者结构 | **可直接继承** | 通讯邮箱由作者最终填写；本审计不验证身份 |
| NLU/问题分解 | 原稿给 agent role 和 prompt | BIRD 有 decomposition 条件；GridDB 有固定 prompt stages | **需重算/角色化** | 可复用 prompt 与分解逻辑，但需独立结构化 I/O 和 agent ledger |
| Schema Cartographer | 原稿给 schema linking/pruning prompt | BIRD 有 schema selection；GridDB 有 compact/domain-grounded context | **可直接继承（能力基础）** | 当前结果支持 schema/context interventions，不等于自主 agent 协商 |
| SQL Synthesizer | 原稿给 PostgreSQL prompt | 当前 Qwen/Granite 生成账本完整 | **可直接继承（生成基础）** | 保留模型、量化、runtime、zero-retry 和 prompt 哈希边界 |
| Validation Engine | 原稿描述 sandbox execution/self-correction | BIRD bounded execution repair、GridDB direct SQLite re-execution | **可直接继承（执行基础）** | 作为 deterministic execution/safety agent 的核心；需补 agent message contract |
| Counterfactual Reasoner agent | 原稿描述对问题扰动并比较逻辑形式 | 当前有 15-state GridDB reliability stress test | **仅诊断/需实现** | 现有 stress test 可作离线反事实/状态诊断；没有证据证明运行时独立 agent 生成、质疑和反馈 |
| negotiation protocol | 原稿有文本与流程描述 | 上午包未发现逐轮 negotiation message ledger | **缺失** | 定义消息 schema、冲突类型、最大轮数、停止规则并运行消融 |
| voting protocol | 原稿有 majority/confidence-weighted 描述 | 上午包未发现候选投票记录或投票消融 | **缺失** | 实现候选池、各代理独立分数、确定性 tie-break 和完整账本 |
| shared blackboard/auditable dialogue | 原稿声称可审计对话 | 当前主要是 prompt/prediction/call ledger | **需扩展** | 现有 ledger 作底层；补 agent_id、input_hash、message、evidence、vote、decision、stop_reason |
| GridDB 当前数据 | 原稿称 1000 expert-authored pairs | 当前实际是 8 tables、98 rows、200 records（20 dev + 180 evaluation） | **可直接继承（按当前事实）** | 必须使用当前统计，不能沿用 1000 pairs 或 domain-expert authorship |
| GridDB 2×2 factorial | 原稿没有该设计 | 2 backbones × 4 cells × 180 = 1440 predictions；独立重执行 | **可直接继承** | 作为 multi-stage base system；保留“无 primary factorial execution effect 经 Holm 后成立”的负结果 |
| prospective component study | 原稿无 | 700 frozen calls；presented value evidence 对 Qwen +0.1059，Holm p=0.0310；Granite 不成立 | **可直接继承** | 可支撑 value evidence 组件的 backbone-specific 结论，不可推广成多智能体普遍优势 |
| BIRD Mini-Dev | 原稿用 Spider/WikiSQL | 500 items、11 SQLite DBs；5000 calls、4000 independently re-executed predictions | **可直接继承** | 作为公共外部基准；Qwen best schema selection 0.394，Granite best repair 0.236 |
| Spider/WikiSQL 原稿结果 | Word 表中存在 | 上午包无预测、模型快照和 evaluator ledger | **缺失** | 删除旧数值，或另建冻结协议后完整复跑；不能引用 DOCX 表作为证据 |
| GridDB 1000 expert pairs | Word 正文/表中存在 | 当前只有 200 records，且稿件说明不是新 sealed benchmark | **缺失/冲突** | 以当前 200-record data card 为准；除非恢复 1000-pair 原资产并证明专家标注，否则不得沿用 |
| RTS-GMLC pilot | 原稿无 | 10 tables、360,530 rows、55 automatic candidates | **仅诊断** | 机械连接和 portability；machine-silver 不是 external accuracy |
| SimBench pilot | 原稿无 | 8 tables、874 rows、36 automatic candidates | **仅诊断** | 同上；4 empty references 必须保留，不得静默删除 |
| machine adjudication | 原稿含“expert”导向表述 | development/frozen 标签、负控、列检查完整 | **仅诊断** | 必须称 machine-adjudicated silver；不得替代 qualified human expert review |
| 15-state semantic reliability | 原稿声称 counterfactual robustness | 66 order-insensitive questions；AND rates 0.6212–0.8182；Holm 后无 effect | **可直接继承（离线稳健性）** | 可作为 Counterfactual Critic 的评价数据/端点，但不是原稿 4.8%/3.5% 结果的验证 |
| 原稿五 agent ablation | Word 表中存在 | 当前只有 stage/component interventions，不是逐 agent removal | **缺失** | 完整五 agent 实现后补 single-agent、no-negotiation、no-vote、no-validator、no-critic 消融 |
| 当前 9 幅图 | 原稿无嵌图 | 有 executed pipeline、factorial design、external gate 和结果图 | **可直接继承/改绘** | 结果图可保留；现有 pipeline 图可作底图；仍需原标题版五 agent + blackboard + adjudication 主框图 |
| 原稿 Table 7 agent walkthrough | 有完整文字示例 | 无相应运行消息/SQL ledger | **仅诊断** | 可保留为 conceptual example，或用新运行账本替换成真实 case study |
| 生成运行器可携带性 | 原稿无代码 | 上午包主要含分析/核验代码 | **需补包/重冻结** | 正式原标题版 ZIP 必须加入执行五 agent 系统所需源码、配置、测试和 environment lock |

## 7. 当前可继承的定量事实（不得扩张）

### 7.1 C²GES

- FEVER document-grouped split：8000/1500/1500 instances；745/141/145 unique documents；pairwise overlap 0。
- K=3 mean evidence F1：oracle-label 0.4926、predicted-label 0.4920、label-blind 0.4910、BM25 0.4864。
- 所有 oracle/predicted/blind role-source primary contrasts 的 hierarchical interval 均跨 0；role-effect criterion 未满足。
- BGE K=3 F1 0.4890；相对 full C²GES 为 -0.0021；相对 BM25 为 +0.0026；Holm 后没有 promoted difference。
- NERC development/frozen 各 75 个问题；这些是 machine-adjudicated silver annotation-process assets，不是摘要或 selector 性能结果。

来源：

- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\C2GES\manuscript_applsci\generated\table_data_audit.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\C2GES\manuscript_applsci\generated\table_main_results.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\C2GES\manuscript_applsci\generated\table_role_effects.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\C2GES\manuscript_applsci\generated\table_bge_contrasts.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\reviewer_packages\C2GES_submission_review_2026-08-08.zip`

### 7.2 MA-SQLGrid

- GridDB：8 tables、98 rows、200 records；20 development、180 factorial evaluation；两骨干、四 cells，共 1440 predictions。
- 9 个 primary factorial execution tests 经 family-wise Holm 后没有满足 declared evidence rule；structural/projected-column adherence 不能替代 semantic correctness。
- prospective E1：Qwen n=170，effect +0.106，[0.028, 0.201]，Holm p=0.0310；Granite 不成立。E2 两骨干均未 promoted。
- BIRD Mini-Dev：500 items、11 databases；Qwen best schema selection 197/500=0.394；Granite best bounded repair 118/500=0.236。
- 15-state GridDB logical-AND：八 cells 的 suite rate 0.6212–0.8182；相关 effects 经 Holm 后均未成立。
- RTS-GMLC/SimBench 与 machine-silver 数据只支持 portability/annotation diagnostics，不支持 expert-grounded external accuracy。

来源：

- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_cell_summary_v2.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_core_inference_v3.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_primary_effects.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_bird_public_baselines.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_semantic_cell_robustness.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\manuscript_applsci\tables\table_semantic_effects.tex`
- `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\reviewer_packages\MA_SQLGrid_submission_review_2026-08-08.zip`

## 8. 按原标题版章节的资产注入方案

### 8.1 C²GES

| 原标题版章节 | 主要继承来源 | 必须新增/替换 |
|---|---|---|
| Introduction | 原标题 DOCX 的 causal-fidelity 问题；当前稿的证据边界、应用限制 | 删除未经证实的“显著领先”预告；将研究问题写成可由新实验回答的形式 |
| Related Work | 当前 LaTeX 已核查 bibliography 与 scope language；原稿主题分类 | 原稿引用尚未逐条核验，不能直接视为 verified；需统一 BibTeX 和 claim-source map |
| Problem Definition/Data | 当前 FEVER data audit、NERC packet/manifest | 新增 report-level summarization unit、summary reference、causal graph/intervention schema；不得复活无资产的 500-doc 统计 |
| Method | 当前 query/role/local reranker作为基础评分器 | 新增 typed causal graph、GNN/GAT、counterfactual intervention、coverage/redundancy constrained summarizer |
| Experiments | FEVER five-seed、BGE/MiniLM、NERC annotation-process diagnostics | 新的 report-level baselines、ROUGE/semantic/causal metrics、因果图与反事实消融、真实预测账本 |
| Results | 当前辅助结果和 negative findings | 原稿所有 GridMaint/ROUGE/Graph-F1/QA 数值必须由新运行替换 |
| Discussion/Limitations | 当前稿的 human/silver/licensing 与 non-causation 边界 | 讨论新增算法的实际证据，不用概念创新替代性能证据 |
| Figures/Tables | 当前 9 图和 10 表中与辅助实验有关者 | 新主框图、数据流程图、causal graph case、counterfactual intervention 图和报告级主结果表 |

### 8.2 MA-SQLGrid

| 原标题版章节 | 主要继承来源 | 必须新增/替换 |
|---|---|---|
| Introduction | 原标题 DOCX 的 multi-agent 工业问题；当前稿的高风险边界 | 贡献必须从“概念五 agent”升级为“有运行账本的五 agent”后再宣称 |
| Related Work | 当前 LaTeX 中 text-to-SQL、schema grounding、execution evaluation 边界 | 原稿引用和优先性声明需统一核查；保留不复现 DKA-SQL 的限制 |
| Problem/Data | 当前 GridDB/BIRD/RTS/SimBench data cards 和许可边界 | 用 200-record GridDB 事实替代原稿 1000 expert pairs；定义 agent message schema |
| Method | 当前 context selection、generation、safety、execution repair | 将五 agent、blackboard、negotiation、voting、counterfactual critic 实现为可执行模块 |
| Experiments | 1440 GridDB、700 component、5000 BIRD calls、15-state reliability | 新增 single-agent/multi-stage/no-negotiation/vote/full multi-agent 对比；固定调用预算和评分协议 |
| Results | 当前所有 hash-bound tables 与 negative findings | 原稿 Spider/WikiSQL、88.2/93.5/91.7、4.8%/3.5% 等必须删除或重跑替换 |
| Discussion/Limitations | 当前 human review、silver labels、license、deployment warnings | 分离 multi-agent coordination gain、candidate-count gain、repair gain和 token/latency cost |
| Figures/Tables | 当前 pipeline/factorial/external-gate 与结果图 | 新五 agent blackboard 框图、一次真实协商 trace、agent ablation/成本/稳定性图表 |

## 9. 原标题版正式补缺的最低证据门槛

### 9.1 C²GES

在下列资产出现之前，原标题中的 “Causal and Counterfactual Graph-Enhanced Extractive Summarization” 只能是设计目标，不能是已验证结论：

1. report-level source/summary pair manifest 和无泄漏划分；
2. causal event/edge schema、图序列化文件和构建审计；
3. GNN/GAT 可执行源码、测试、checkpoint 和训练 ledger；
4. counterfactual generator/intervention ledger、接受/拒绝规则和失败记录；
5. summary prediction ledger；
6. ROUGE、semantic similarity、causal-chain/graph、counterfactual sensitivity 和 redundancy evaluator；
7. 至少 lexical、graph-free、neural reranker、无 counterfactual、完整模型等有价值对比；
8. seed/document-level uncertainty 与预先声明的多重比较处理；
9. 若使用 NERC machine-silver，明确其只能训练/开发或诊断；不得称 human expert gold。

### 9.2 MA-SQLGrid

在下列资产出现之前，原标题中的 “Multi-Agent Framework” 不能仅靠五段 prompt 和流程图成立：

1. 五 agent 独立输入/输出 contract；
2. shared blackboard 状态与逐轮 message ledger；
3. negotiation conflict type、最大轮数和停止条件；
4. voting/candidate adjudication 规则与 tie-break；
5. execution/safety validator 的确定性事实记录；
6. counterfactual critic 的扰动、比较、反馈和失败 ledger；
7. single-call、multi-stage、parallel agents、no-negotiation、vote、full system 的公平对比；
8. 控制候选数量和调用预算，避免把更多 sampling 误判为 multi-agent gain；
9. 执行准确率、修复 rescue/harm、schema linking、robustness、token、latency 和 failure retention；
10. 正式源码、模型/runtime lock、配置、测试和可复现包。

## 10. 图表资产结论

- 两份原标题 DOCX 都没有嵌入图片，故不存在可以直接抽取的原算法框图。
- 当前 C²GES LaTeX 有 9 幅图，当前 MA-SQLGrid LaTeX 有 9 幅图；上午 09:25 完整包携带这些图及 PDF。
- 现有结果图与审计图可直接继承到相应的辅助实验小节，不能通过改标题变成新算法结果图。
- C²GES 仍缺“文本/事件 → typed causal graph → GNN → counterfactual intervention → constrained extractive summary”的主算法框图。
- MA-SQLGrid 仍缺“五 agent ↔ shared blackboard → negotiation/voting → execution evidence → adjudication”的主算法框图。
- GPTimg2 可用于生成视觉草图，但算法节点、箭头、符号和文字必须由实际实现 contract 驱动；生成图本身不是算法实现证据，最终宜转为可编辑矢量并人工校对。

## 11. 不能跨越的证据边界

1. 本审计没有调用外部 API、没有上传稿件、没有下载资料，也没有进行外部引用存在性验证。
2. 原标题 DOCX 中的参考文献和定量结果只证明“文档中写了这些内容”，不证明论文、数据、实验或数值已经核实。
3. ZIP 的 `SHA256SUMS.csv` 能证明包内文件完整性，不能单独证明实验设计有效或结论正确。
4. machine-adjudicated silver labels 不是 human/domain-expert gold。两个 NERC 75-item packets、MA 121/115-item 标签都必须保留这个命名。
5. 当前 FEVER 结果不能直接转换成 power-grid report summarization 结果；当前 multi-stage Text-to-SQL 结果不能直接转换成 multi-agent negotiation 结果。
6. 两份原稿中的 GridMaint-CausalSum、500 document manual annotation、GridDB 1000 expert pairs、Spider/WikiSQL 结果、原稿消融和 robustness 数值，在当前上午包中均没有找到足够的来源绑定；状态为缺失而不是“待包装”。
7. 上午包刻意排除了第三方原始数据、模型权重、凭据、事故运行和许可不允许重分发的材料；投稿时的数据可用性声明必须继续受第三方许可约束。

## 12. 审计结论

上午版并非没有可用资产。它为两篇原标题版提供了大量可核查的基础算法、数据审计、预测账本、统计分析、图表和失败边界：

- C²GES 可直接继承 FEVER 文档分组证据选择、query/role/local mixture、five-seed、BGE/MiniLM、crossed-seed 和 NERC machine-silver annotation-process 资产；但真正的 causal graph、GNN、counterfactual intervention、report-level summarization 和原标题主结果仍缺失。
- MA-SQLGrid 可直接继承 GridDB 固定多阶段流程、schema/context selection、生成/安全/执行修复、1440 canonical predictions、700-call component study、5000-call BIRD baseline、15-state reliability 和外部数据诊断；但五智能体运行时、协商、投票、blackboard 和逐 agent 消融仍缺失。

因此，原标题版的正确整合策略是：**以原标题 DOCX 保留研究问题与章节骨架，以当前 Applied Sciences 稿和上午包作为可核查证据底座，以新冻结实验填补标题核心算法；所有原稿旧数值在找到原始资产或完成重算之前不进入 Results。**
