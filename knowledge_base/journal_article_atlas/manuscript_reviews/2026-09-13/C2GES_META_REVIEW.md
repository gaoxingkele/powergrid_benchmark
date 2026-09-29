# C²GES：Information 元解构分析

## 1. 对象与结论

对象：[当前诊断主稿](../../../../paper_projects/C2GES/Workspace/01_Manuscript/LaTeX/paper_applsci.tex)，SHA见README。目标索引仍为Applied Sciences；本分析使用Information元框架，不擅自转刊。

判断：**探索性E1、E3已经写入，不应再说没有完整因子消融；主要缺口转为叙事整合、代理指标的解释权限、机制结论的可迁移性。** 无真人E2，但当前已撤回结构有效性与系统优势主张；它不是把真人验证“做完了”，而是选择了证据负担不同的诊断路线。

## 2. 算法与实验分类

- L1：长技术文档信息抽取。
- L2：确定性抽取式摘要／启发式多信号排序。
- L3：lexical roles→typed proxy graph→路径参与→归一化分数→角色保留→冗余贪心→来源页定位。
- 理论：固定图上的路径删除恒等式、非负性和可加性；没有语义因果识别。
- 历史实验：15报告×7条件×2预算；布局、长度、编码截断、聚类和权重诊断。
- 当前探索试验：7系列×8方法×2预算=112格；E3为13配置标签×7系列×2预算=182格。AB-5=RP-11，AB-6=RP-10=G-T，故13标签在声明相同参数下仅10种唯一配置，不能把别名当独立复验。
- 机器审查：29个选中单元、两模型；不是两名独立人类，更不是完整边/路径/遗漏评价。

## 3. 逐章元映射

| 章节/源行 | 当前功能 | 主要接口问题 | 修改方向 |
|---|---|---|---|
| Abstract L22 | 负结果动机、方法、历史/探索结果、机器审查、边界 | 信息拥挤，当前探索结果不是首先展开的证据 | 先提出诊断问题，再当前控制实验，再必要历史对照 |
| Introduction L28 | 电力阅读需求、角色动机、图方法、历史语料、3RQ、贡献 | 后半清楚，但开头仍像欲证明工程阅读效果的方法论文 | 首段尽早转到“结构代理与真实摘要质量可能脱节” |
| Related Work L42 | 抽取、图/因果边界、电网文本 | 末段和对照表仍以旧NERC/strict ablation为中心 | 对照方法按预算控制、结构来源、消融、外部数据和验证类型，而非按期刊堆文献 |
| Methods L85 | 历史K预算、历史语料、未来协议、角色图、评分、AB、真人未来、调参、统计 | 当前/历史/未来三层穿插；读者难重建当前8方法 | 当前词数预算协议在前，历史差异表在后；未来协议移补充 |
| Results L289 | 历史导读→当前外部→因子→多节历史→软件 | 当前证据已放前，但大量旧表/图仍主导视觉 | 以外部公平比较、机制因子、机器审查三块作主体；历史缩为一个诊断节 |
| Discussion L527 | 系统比较、路径机制、方法学经验、工程意图、限制、未来 | 已新增可迁移经验，是实质进步；默认系统仍需更强理由 | 区分低信息角色、预算冲突、归一化、指标失配四个候选解释 |
| Conclusions L575 | 两类历史发现、探索负结果、默认系统 | 历史结果优先；一句因果连接不成立 | 当前发现→有限机制判断→建议配置范围→未证实事项 |

## 4. 应保留的优点

- table: tab:factorial-main ——AB、RP、G控制齐备，正文说明别名；不再只有Full/no-path两行。
- text: §4.3 “negative direction persisted after omitting each series in turn” ——LOSO加Jaccard区分了活跃但无收益与组件没运行；不显著未写成等价。
- table: tab:external-exploratory ——8方法相同候选、110/260词预算，所有主要系统区间跨零仍如实报告。
- text: §5.3 “hard coverage constraints and soft structural scores should be crossed factorially” ——可迁移方法学经验已经出现；下一步应增强证据，不是再添加泛泛教训。

## 5. 主要问题与关闭条件

### C2-M1：当前方法定义仍以历史K预算和报告级统计开篇

Severity: Major。Evidence Anchor: text: Task Formulation “For budget $K”及“The unit of analysis is the report”。Confidence: 5（与Layout-Aware Units词数预算、Statistical Analysis系列统计直接对照）。

当前核心实验是110/260词预算、系列等权，首个任务定义却仍是min(K,n)个单元。后文虽然解释了新协议，主方法接口不唯一。

修正：先定义词数约束下集合选择、完整排序跳过规则、reservation耗尽预算时行为；主统计单位定义series。历史K与15报告只在明确标记的旧协议说明中出现。验收：读者只读当前Methods就能重建探索试验，无需跨历史段拼接。

### C2-M2：当前外部基线身份及调参说明尚不集中

Severity: Major。Evidence Anchor: text: Development Selection and Comparators “PacSum-MiniLM tuning and performance evaluation remain blocked”对照table: tab:external-exploratory。Confidence: 5（正文状态交错）。

它可以指未来确认性运行被阻塞，并不说明表中结果虚假；但正文没有在同一处清楚给出当前8方法使用的是默认、equal-nine所选还是另一个v3配置。未来blocked与当前已运行应明确分开。

修正：一张“历史/当前探索/未来确认”参数表，逐方法列版本、权重、开发来源、调参次数、输入可见性、运行状态和配置文件路径。主图中的unrenormalized removal也应标历史。验收：八种方法和13配置标签均能唯一连到实际运行配置。

### C2-M3：no-path是相对Full的简化，不是所有配置中的最优选择

Severity: Major。Evidence Anchor: table: tab:factorial-main。Confidence: 5（表中数值）。

110词RP-00=0.1710、RP-01=0.1741，高于no-path的0.1668；260词RP-00=0.1870、G-U=0.1898，高于no-path的0.1844。不能由Full较差就推导typed+reservation no-path整体最优。

当前“provisional simpler”措辞已降级，这是优点；但默认的决策准则仍需补充。建议明确它只是Full的简化参考配置；若保留正式推荐，说明为什么保留typed和reservation，以及ROUGE、规则覆盖、冗余的偏好如何事前确定。不要事后挑最高点估计当新默认并重复检验同批系列。

### C2-M4：结构覆盖有机械自评成分，不能独立证明机制价值

Severity: Major。Evidence Anchor: table: tab:factorial-main Role=1.000及§4.3 by construction解释。Confidence: 5。

reservation本来就保留角色，role coverage变1主要检查机制执行；边也是由同一规则生成。原文已正确写成formal heuristic structure，但“结构收益”的科学含义因此仍有限。

修正：把这些指标列为内部行为指标，语义结构、来源忠实度、关键遗漏单列未测。若声称语义收益，需独立标签；若保持负结果诊断，可研究角色噪声、距离窗口、否定/指代、预算冲突的受控压力测试，清楚标注合成/探索性质。

### C2-M5：因子结果没有证实稳定冗余或普遍失败

Severity: Major。Evidence Anchor: table: tab:factorial-main与§4.3交互解释。Confidence: 5。

按四位表值计算，110词path效应在reservation关闭时+0.0031、开启时−0.0080，交互约−0.0111；260词对应−0.0135、−0.0072，交互约+0.0063。原文准确承认两个交互均未通过Holm。数字仅为表值算术，不是重新估计区间。

因此可以说预算依赖、观察到负向方向，不能说证明path无信息或reservation必然替代path。下一步将候选解释分别映射到鉴别实验；不要继续在同7系列反复改机制来获取显著结果。

### C2-m6：结论的一个逻辑连接及章节引用需修正

Severity: Minor。Evidence Anchor: text: Conclusions “showing that the original ablation was scale-coupled”。Confidence: 5。

未归一化比较均值较高不能证明尺度耦合；尺度耦合来自正权重1降到0.85、冗余系数仍0.5的定义。结论应拆开“定义导致耦合”和“归一化后仍未见收益”。另外历史文字仍硬编码Section 4.3/4.4，现已新增小节，需改为label引用并核对。Discussion把第二个限制写了两次second，属于小编辑问题。

## 6. 文笔和图表的实质改进

不是删掉所有限制，而是让每个段落完成单一论证工作：当前发现→独立证据→机制或备选解释→适用边界。未来真人样本数、冻结要求等整段计划不宜反复占据当前Methods和Discussion。历史显著性表、旧输出长度图、旧component图可集中到补充，正文优先展示当前交互与质量/覆盖的取舍。

三个Information范文的可借鉴点是方法接口与任务结果对应，不是它们的公式或图表数。C²GES需要更清晰的“为什么值得读”而不是更复杂的“系统如何构建”。

## 7. 最小修改序列

P0：统一当前预算与统计定义；当前/历史/未来参数表；修正默认配置范围；清理硬编码引用与结论逻辑。

P1：将现有7系列的贡献—配置—指标—区间—结论做成唯一证据矩阵；10唯一配置与13标签分别计数；将29单元机器审查从结构有效性证据中明确隔离。

P2：按作者选择，开展未见系列诊断复验或独立结构评价。仅用LLM合成数据可以检验实现与特定噪声假设，不能补成真实外部样本或真人E2。

总体建议：比SQL更需要一次主文级结构整理；不建议仅更换Information模板后立即提交。诊断路线本身可以成立，但是否具有足够发表价值仍取决于可迁移结论，而非本地READY标记。
