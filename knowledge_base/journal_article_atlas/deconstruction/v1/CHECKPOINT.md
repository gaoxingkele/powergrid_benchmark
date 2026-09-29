# 全量解构执行检查点

## Information逐段无遗漏检查（当前用户优先事项）

- 用户明确要求无遗漏证明、修复漏项、扩展meta字段，并还原期刊常规框架。根代理新增audit_paragraph_coverage.py及information_coverage_rules.json，对050/516未覆盖块逐项读取归类。
- 050提取2048行、516提取1398行：每行恰一归属，未归类0、重复0；源/map哈希绑定。没有发现新增正文漏段。摘要、题注、公式、表格、声明等补为独立类别。仅证明指定解析器提取文本分区闭合，栅格/向量内容仍须视觉验证。
- 789第三篇尚未有全量paragraph_map，覆盖台账3743行均unassigned；原10示例不能充当完整映射。这是接下来最高优先缺口，不能写三篇已无遗漏。
- 新增export_information_paragraph_meta.py，导出114段/列表可读MD+机器JSON，含源位置/主要作用/概括/词数/顺序/词数占比；新增13类语义字段显式not_assessed，尚非全量语义标注。
- INFORMATION_COVERAGE_REPORT.md给出集合分区定义、测试范围、共同论证任务框架和剩余项；INFORMATION_BATCH修正旧版段落边界复核状态的矛盾。
- test_paragraph_coverage4项通过（真实分区、删除摘要、重复归属、错误源SHA）。无需重复扩展测试，后续主要工作是789的源文精确逐段映射及三篇语义/句级字段。

## 2026-09-13 首批18分组均有3篇与因子效应重算

- 最新索引55篇1034物理页，18个工作分组全部至少3篇，Energies4；源SHA匹配，全字段验收仍0。Remote Sensing第三篇SAR已实际落盘，其30页原文解构及证据边界在p_b9120f80f6832100。初批数量门已满足，完整目标未完成。
- scope_core/scope_other/scope_energy均返回usage limit错误，工作停止。无需等待或重复重启；根代理继续本地可完成工作。
- 本轮新增audit_tfe_factorial.py、3项有效测试和p_82d41dafd52827e4.factorial_audit.json；源哈希绑定Table5，计算12条件差、3主差、3二阶及1三阶有限差分。MLP平均MAPE+0.05625pp但RMSE-13.3685，说明指标/背景权衡。没有从8个汇总数制造CI或p值。
- 新增EXPERIMENT_COMPARISON_GUIDE.md，跨TLA/TFE/SAR/规划个案区分实验设计、配置数量、参数敏感性、替代实验和可视化，并提供主张→设计→配置→结果→结论关联字段。
- 待接手原队列Applied3：10.3390/app16125815、app131911074、app14093682；Energies3：en19092172、en13102559、en18184986。读取当前文件再确定已落盘项，不能依据失败代理的分工当完成。
- 原62覆盖审计仍是49case时的快照（13原覆盖、49未完成），须按新文件重算；全段落/211字段/独立复核仍须推进。保留完整范围。

## 2026-09-13 Sustainability三篇与53篇索引

- 上轮新增TLA实质分析及审计属progress。本轮完成25页TFE-iTransformer个案p_82d41dafd52827e4的JSON/MD，完整25页阅读、全部13图8表所在页视觉核查。34编号公式组，4实验族，固定iTransformer的TFE/TCN/MLP完整8配置。
- 新增SUSTAINABILITY_BATCH.md：三篇64页，按长期规划/单户小时/区域6小时分层，不汇总为期刊均值。
- 指标改进有负向条件效应；MAPE印刷缺绝对值、因果索引t+rk、乘法Prophet与加法公式/单位、K5与仅4IMF输入、Table6文字方向与百分点错误均源绑定记录。不是作者代码诊断。
- 最新索引53篇981页，源hash全匹配，全字段验收0。Future Internet3、Remote Sensing2、Sustainability3，其余场所均3；待Remote Sensing最后一篇后才达到18工作分组各3的初批数量门，仍不是全目标完成。
- ORIGINAL_CANDIDATE_COVERAGE已明确原62来自scope_records journal_core_candidate=true；49case审计快照中仅13原候选匹配，其余36新增样本不抵扣。原队列剩49待实质解构；63行core reading list因Machines身份错误多1，不作权威分母。
- scope_energy转原Energies队列最前3未完成项；scope_other继续SAR第三篇；scope_core Future Internet结果待主代理整合。难度维度存在早期口径漂移，必须按DESIGN锚点复核，不能沿用未经校准分数。
- 后续保留原62、18工作分组、逐段/211字段及独立复核范围，无删减。没有原论文改写、邮件或Git提交。

## 2026-09-13 TLA-LSTM实质解构与48篇索引

- 上一状态问答只做只读核查，没有新增解构，按目标推进标准不计实质进展；本轮新增了源绑定单篇记录和可复算数值审计。
- 最新索引48篇、874物理页，源SHA全部匹配；全字段验收仍0。Machines3、Atmosphere3、Sustainability2、Remote Sensing1；Future Internet仍缺批次。其余见INDEX。
- 新增Sustainability p_d564ed78dc6f82bd：16页全文、5–14页图表公式视觉核查，13编号公式组、9图、3表、2个完整报告实验族；无完整受控组件消融。不能把仅文字提及的融合比较算作已报告实验。
- 新增audit_tla11252.py及4测试。Table2/3的R2和MSE在同目标/同权重/整体计算假设下不相容，三位小数舍入无法解释；宏平均可能解除恒等式约束，但原文未说明。保留条件，不推断造假。另记录Intro加法/Methods乘法、2D/1D卷积、图6/9量纲展示与训练容量不匹配。
- 本轮数值审计4测试及索引4测试通过；这些仅证明算术和文件完整性，不替代独立语义审查。
- Sustainability剩余10.3390_su16177613.pdf（25页、SHA82d41dafd52827e433c5cbd4083721ba58719549d40989f10d78275f4702c5ae）仍只有首页核查，下一步完整解构，不计完成。
- scope_core已转Future Internet3；scope_other继续Remote Sensing另外2篇；scope_energy已完成Atmosphere3，转原62候选与现有个案DOI级覆盖对账，禁止新增样本替算原覆盖。
- 保留原62候选、15期刊与3会议工作分组，以及逐段/211字段/独立复核完整范围；不以每组3篇数量达标宣告目标完成。无原论文改写、外部LLM全文上传、提交或邮件。

## 2026-09-13 Sustainability 首篇与空缺期刊推进

- 最新索引42篇、768页，源SHA均匹配；Symmetry3、Processes3、Machines2、Sustainability1，其余以INDEX为准。全字段验收仍0。
- 根代理新增Sustainability长期规划p_c6289136e937a5f3：23页全文读完，关键数学与图表视觉核查，JSON/MD已落盘。Table8全11年MAPE9.1161%可复算，但训练2010-17和验证2010-20重叠；2035未来预测不同不能证明精度。Table4/5/6行和与区合计不符，Table7再汇总却一致；保留区分。
- discovery_sustainability.json注册3篇，OpenAlex/Unpaywall确认CCBY；主站403后公开出版商CDN HEAD200，aria2合法下载成功。另两篇sources/10.3390_su16177613.pdf（25页）与10.3390_su162411252.pdf（16页）只核首页，尚未全文分析，不能计入个案。
- 当前分工：scope_other已完成Symmetry转Remote Sensing3；scope_energy已完成Processes转Atmosphere3；scope_core仍Machines收尾。之后仍须Future Internet及Sustainability剩余，再继续原62队列和完整逐段/211字段/独立校验，不缩减范围。
- 本轮索引器4测试通过；只证明覆盖的结构与来源检查，不证明论文真实性或科学结论。无原文改写、无外部LLM全文上传、无提交。

## 2026-09-13 IEEE Access 批次完成后的检查点

- 最新索引37篇、638页，源哈希均匹配；IEEE Access达3篇，新增p_1d0f96081ce9a6ff（10页VMD-Pyraformer）和p_0e43fa69b58683db（9页DE-IHHO）。全字段验收仍0；下方31篇是历史状态。
- 新增IEEE_ACCESS_BATCH.md。三篇分别是资源权衡、流水线组合、逐级寻优，保留不同任务/误差尺度/统计缺口，不合并期刊均值。
- VMD篇全部11图4表视觉核查：RMSE/MAPE公式问题、三路融合缺定义、数据分解时间边界未交代。DE-IHHO篇9图6表视觉核查：印刷LSTM缺符号、平滑参数维度不清、多个机制同时改变且最终训练轮数100→200。仅报告印刷与方案证据，不推测代码实现。
- 当前Symmetry2、Machines1、Processes1，其余以新索引为准；代理持续补各自3篇。Processes的GHI个案必须标为辐照度接口层，不得冒称真实PV电功率验证；后续按任务分层，不用题目替代实际目标量。
- 本轮索引器4测试通过。测试覆盖来源/字段存在和空清单证明，不代表科学判断或独立复核通过。原62候选、15期刊和3会议、完整字段要求均未缩减。

## 2026-09-13 最新落盘推进（优先于下方历史数量）

- 本轮最终索引重新验证得到 31 篇、538 页，全部源 SHA 匹配；全字段验收仍为 0。Algorithms、Sensors、ISGT 各 3；IEEE Access 1。ISGT 工作分组含不同区域会议，须保留单篇精确会议信息，不可当作完全同一会刊版式的均值。
- 新增 IEEE Access p_76bd3403ef95b3c1 的 JSON/MD：10 页全文，图表所在页与算法/关键公式已视觉核查。双向主张对上行指标、量化残差定义、单组件消融和统计边界均保留，不据此替作者推测代码实现。
- 新增 ALGORITHMS_BATCH.md、SENSORS_BATCH.md，区分任务、目标量、实验类型和证据缺口；不发布期刊均值或录用概率。
- Sensors IIoT 独立补充材料明确未读，不能计为完成。各篇逐段计量与 211 字段仍须补齐。
- 后续并行任务为 Symmetry 3 篇、Processes 3 篇、ISGT 批次收尾；分派、下载和文本读取不计作解构报告完成。
- 上轮状态回答属只读核验，不是新增解构完成。本轮有新个案、批次对照和索引更新的实质进展。完整目标不缩减。

## 最新续轮状态（2026-09-13，覆盖下方历史阶段）

- 续轮后段已达到24篇、442页：新增Mathematics2、PESGM3、Algorithms2、Sensors1；实际数以INDEX重建结果为准。Math和PESGM各自已3篇，另有MATHEMATICS_BATCH.md和PESGM_BATCH.md。
- Sensors首篇ADTL（p_a1adf441aa349153）17页全部读完、10页视觉核查，JSON/MD/印刷数值与可运行算术审核已落盘。T3均值87.84对正文88.78；T5有两个QLD03负迁移配置；T6/T7改善/权衡分别记录。仅原文数值核对，不是原始数据复现。新增4项测试通过。
- Algorithms第三篇、Sensors另2篇、ISGT3篇继续在分工中；没有完成文件不计数。Mathematics新两篇的难度定义需由scope_core统一回项目0–4六维锚点，其发现旧评分不符合标准；恢复时核查修复是否已落盘。
- 已重新索引16篇、315页：Applied Sciences/Electronics/Energies/Information/IEEE SmartGridComm各3篇，Mathematics1篇；全部原件哈希匹配。
- 修复索引器对真实0表的错误拒绝：必须有来源哈希、全文页覆盖、明确source_reviewed_absent及0计数才可接受空清单。新增4项回归测试；不放宽缺失或未知对象。
- Information 050段落独立AI复核修正为63散文段＋3列表，正文仍6892词，散文均长108.31746词。原P009拆分后下游位置ID顺延；修正P004与原P043作用概括。原件未修改。
- Information 516的48段边界独立AI复核通过，词数7240；词级独立复算仍未完成。
- Information第三篇定向独立AI复核已纳入主记录：随机抽样与确定性选最优不等价，但跨分量加权重构与逐分量随机选模可以共存，不能泛化判冲突。
- 新增SMARTGRIDCOMM_BATCH.md，三篇按控制任务、物理接口、理论、实验/消融和统计证据对照。会议副本不用于正式会刊版式均值。
- 已分配继续补齐Mathematics另2篇、Algorithms3篇、IEEE PES General Meeting3篇。分配不是完成证据，恢复时检查实际文件及代理状态；不要预计入数量。
- 全字段验收仍0篇。原62候选及15期刊＋3会议的目标不变，不能凭16篇关闭目标。

最新检查入口：test_deconstruction_index.py、test_reviewed_paragraphs.py、test_info516_audit.py、test_atlas.py及index_deconstruction.py。测试只验证各自覆盖的数据处理/算术，不代替科学判断。

## 历史阶段记录（10篇时）

## 本轮已改变的实际状态

- 从只有计划/来源文件推进为10篇逐篇JSON＋MD实质解构：Applied Sciences 3、Electronics 3、Energies 3、Information 1。
- 原件总225页，索引脚本重新计算10份原件SHA，全部匹配；读取页码记录完整。该检查只能证明文件与覆盖记录一致，不替代科学审核。
- Information案例完成62个散文段＋3个列表项的人工式单助手边界映射、主要作用和计算长度。62段平均110.06词；含列表项正文6,892词，按声明tokenizer。
- 该案例核心内容有独立AI审核文件；3项修正及2项不确定已纳入主记录，不冒充全字段独立复核。
- 新增段落计量脚本及4项测试；新增跨格式索引器，保留不同对象计数口径，不把公式对象数当编号显示公式总数。

## 目标未关闭

62篇已有期刊AI候选中9篇已有本轮实质解构，另新增Information 1篇。不是62篇全部完成；15期刊＋3个工作选定会议尚未全部取得批量样本。10篇也仍有逐段/句级语言、未编号公式、全对象视觉、独立复核和字段映射缺项。

## 下一步可执行顺序

1. 使用 Information 段落映射/计量机制补齐首批9篇；每篇依据实际布局重建映射，不能复用其block编号或猜测段落。
2. 首批9篇交叉独立复核原件，逐项记录修正；不以测试通过替代语义核验。
3. 完成 Information 与 Mathematics 已登记候选的下载和全文解构，再补足其他缺口期刊及3个会议；默认aria2下载，身份和领域不匹配的不得凑数。
4. 继续原62篇队列；按任务层展示样本，未够样本和校准门不计算期刊平均难度。
5. 统一实质字段映射至211字段账本/关系表，再进行全量验收。不得仅填not_assessed即记完成。

## 可复现检查

```powershell
python -X utf8 knowledge_base/journal_article_atlas/scripts/test_reviewed_paragraphs.py
python -X utf8 knowledge_base/journal_article_atlas/scripts/index_deconstruction.py
```

索引输出位置：`INDEX.json`、`INDEX.md`。独立AI复核不是机构人工标注；没有调用外部LLM，没有更改原始论文，没有生成录用概率。
