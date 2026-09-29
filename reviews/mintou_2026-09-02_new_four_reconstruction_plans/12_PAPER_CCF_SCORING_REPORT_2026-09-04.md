# 四篇论文 Paper_CCF 技能包评分评估报告

**评估日期：** 2026-09-04
**评估对象：** 四篇锁定标题论文的 Stage-2 候选分支头（canonical `journal_submission/paper.tex`）
**评分基准：** `D:/aicoding/mylib/Paper_CCF` 期刊画像（mdpi-energies / mdpi-electronics / mdpi-applied-sciences + mdpi-common + journal-selection-guide）+ 项目前评估（`05_MDPI_ORIGINAL_TARGET_PREASSESSMENT_2026-09-03.md`）最低接收门槛 + Stage-2 签核包项目红线
**mylib 状态：** 已 `git pull`，Already up to date。
**方法：** 每篇由独立评估代理全文通读（720–860 行 LaTeX），按 6 个维度 1–5 分评分；本报告作者对全部最高风险结论做了原文交叉验证（占位符数量、Data Availability 措辞、负结果主结论、联合开关、红线声明均逐条复核通过）。

## 一、汇总评分

| 论文 | SHA | 锁定标题 | 目标期刊 | 范围契合 | 证据门槛 | 完整性硬门槛 | 标题-内容一致 | 科学风险控制 | 门槛对照 | 标准化总分 | 就绪度 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `d76ee394f6a0` | Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution | Energies | 3 | 4 | 2 | 2 | 5 | 3 | **63** | 有条件可投 |
| P2 | `68cd1f233f9f` | Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization | Applied Sciences | 3 | 4 | 2 | 2 | 4 | 3 | **60** | 未达门槛 |
| P3 | `c49e16412e56` | Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm | Energies | 3 | 4 | 3 | 2 | 3 | 2 | **57** | 未达门槛 |
| P4 | `c138f7228c9e` | Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting | Electronics | 2 | 4 | 1 | 1 | 5 | 2 | **50** | 未达门槛 |

说明：
- 标准化总分为六维等权（每维 1–5 分，合计 /30 折算 100 制）。P4 代理在"投稿就绪度决定性维度"加权口径下给出 44 分（标题一致性、门槛对照、硬门槛三权重占 65%）；两种口径的排名一致：**P1 > P2 > P3 > P4**。
- 评分衡量的是"**以锁定标题投目标期刊的就绪度**"，不是 Stage-2 文献阶段质量。四篇作为 Stage-2 审计证据的质量（文献核验、红线保留、科学诚实性）全部在 4–5/5 档。

## 二、跨篇共同发现

1. **科学诚实度是四篇最强的共同资产（风险控制 5/5、5/5、3/5、4/5）。** 每篇都对己不利的结果完整保留并立为主结论：P1 偏好模块 0.17% 未决、归一化翻转排序（Table 9）；P2 "loses four of eight Holm-corrected NSGA-II contrasts and wins none"写入摘要；P3 FixedDE 三口径名义领先、指标排名反转全景表（Table 5/9）；P4 聚合对照 Holm p=0.984、DLinear 更优。四篇均以否定句封边 claim，达到方法学期刊级水准。
2. **投稿完整性硬门槛四篇全部未闭合（共同阻塞项）。** P1/P2/P3 各有 2 处 `[AUTHOR INPUT REQUIRED]` 占位符（Funding + Author Contributions），P4 有 **5 处**（Funding / Author Contributions / Acknowledgments / COI / AI 使用声明）。P2 另有一个诚信级红旗：COI 声明 "no conflicts of interest"，但作者单位是国网福建经研院——按 Applied Sciences 语料 11/11 硬规则，受利益相关电网公司雇佣必须在 COI 具名披露。四篇 Data Availability 均无持久公开链接（P1/P2/P3 为 "can be supplied before publication"，P4 明写 "No persistent public archive is verified"）。
3. **证据门槛四篇全部超配同刊语料（4/5）。** 30 种子 × 多情景 × 多方法主运行、Holm 校正 + 精确重跑八位小数零差异、双轴敏感性扫描、匹配预算/匹配时间双协议——远超 MDPI 语料"≥1 测试用例 + 情景自对比 + 敏感性分析"的常态底线。四篇的短板不在实验执行。
4. **标题-内容一致性是四篇的共同弱项（2/5、2/5、2/5、1/5）。** 锁定标题的机制承诺与当前证据强度之间存在结构性落差：P1 "Investment Effectiveness" 无工程效应解释；P2 "Bidirectional Local Search" 的替换算子全 8 场景无增益；P3 "Self-Adaption" 对应机制在三口径下名义落后于 FixedDE；P4 标题方法零实现（正文自证 "not a GCN or HGCN"）。
5. **P1/P2 共享池边界已做可审计分层**（机制分工、共享/专属范围四处交叉披露），最小发表单元风险有缓解但未消除。

## 三、分篇评分要点

### P1 — TRACE-MOEA → Energies（63，有条件可投，四篇中最高）

- **优势：** 科学诚实度 5/5；证据工程超配（3360 主运行 + 441 边界重跑 8 位小数复现 + 390 OFAT 敏感性 + 三预算匹配控制）；真实外部锚点（MTEP16 1218 项目反测，自限 descriptive）；对 "Hybrid" 有显式不承诺声明。
- **缺口：** 能源应用验证结构性缺失——无 AC 校验、无成本校准、定量结果全部是代理指标上的 MOEA 指标；0.89% HV 增益无工程效应解释（前评估点名风险未处置）；摘要首句未采用约定的 power-grid investment portfolio 连续语义（仅关键词有锚定）；Funding/CRediT 占位符；R-NSGA-II/MOEA/D 基线量级悬殊 + pymoo 版本未钉扎，头牌对比可被攻讦。
- **Top 风险：** ① "方法论文披能源外衣"——按 Energies 审稿人视角贡献落在进化计算而非能源；② 0.89% 增益被自家消融证伪到仅剩组装（偏好 0.17% 未决）；③ 编辑初筛完整性拦截。
- **结论：** 项目红线（proxy 需电气验证或严格 claim 边界）以"严格 claim 边界"方式守住，末段明列 "pending expert calibration, electrical validation, and a human study"。可投的前提是把卖点从"投资有效性优化"内部对齐为"带可检查事件摘要的预算约束组合搜索框架"。

### P2 — BiLo-NSGA → Applied Sciences（60，未达门槛）

- **优势：** 负 NSGA-II 结果全程可见且被立为主结论（红线保留完好）；元启发式高门槛下的基线宽度满足（7 基线 + 10 单开关消融 + 6 套超体积方案 + 7 格参数扫描）；等评价预算为主、等时间为辅的双协议与效应量/CI；MTEP16 真实历史回测层（自限 descriptive，5 组 caveat 如实披露）。
- **缺口：** 最低门槛第 3 条未满足——主基准成本为合成单位（"not calibrated currency"），全文无 LCC/NPV；第 2 条部分满足——MTEP16 是描述性回测而非进入推断协议的第二问题族；无精确/ε-constraint 参照（limitation 自认）；NDS-only 单元被 RandomMutationOnly 的变异率改动混杂；COI 雇佣披露缺失；摘要超 200 词上限。
- **Top 风险：** ① 应用可信度不达该刊应用主导逻辑（代理 + 描述性自限直接命中 desk-reject 特征）；② COI 与雇佣关系不匹配 + 双占位符触发初审完整性门禁；③ 元启发式负结果稿的贡献性否决——若无重新定位（"匹配代价审计协议"而非"算法优越"），第一轮即被拒。
- **结论：** 红线（负结果可见）满分保留；未达门槛的主因是成本校准缺失 + 投稿完整性 + 标题承诺错位。

### P3 — CARS-MODE → Energies（57，未达门槛）

- **优势：** 复现工程是四篇最强之一——2940 行档案精确重跑零差异；AC 层用 pandapower 真实潮流 + 4 个 SimBench MV 网络 + 三条件并查；指标排名反转完整披露，被指"指标挑选"的空间极小。
- **缺口（两条红线均失守）：** ① parameter 与 strategy adaptation 只有联合开关，无 Adaptive–Fixed / Fixed–Adaptive 两臂（红线 1）；② AC 映射是组合级启发规则、非 action-aligned 节点级动作，且只评估 run-index-0 单个妥协解、无种子复现（红线 2）。另：标题机制三口径名义落后（0.60%/0.52%/1.31%）致贡献坍缩为"审计工作流"；"Self-Adaption" 拼写风险未做任何处置（前评估风险清单中唯一未处置项）；"2940-run" 口径含 210 行确定性重复调用（已披露）；对照预算不平等且未认证、种子按方法哈希派生。
- **Top 风险：** ① 标题承诺被自身结论否定 + 应用刊接受"方法不优于自身对照"的纯方法论论文概率低；② "这不是规划论文"路径（决策变量非 action-aligned、成本未标定）；③ 对比公平性与指标选择攻击面。
- **结论：** 与签核包判定一致——红线未保留，Stage 3 必须先拆 2×2 四臂与 action-aligned AC。

### P4 — CSA-LoadNet → Electronics（50，未达门槛，四篇中最低）

- **优势：** 科学风险控制 5/5——红线在摘要/引言/方法/结论四处以原文显式保留，无一处淡化；全部不利结果完整保留；实验协议超配（3 数据集 × 双跨度、5 外部基线 + 5 消融 + 4 匹配对照、块级外单位精确推断）；修复了 fixed-split TemporalOnly 的 smaller-head 混杂。
- **缺口：** ① 标题方法零实现——全文无图卷积、无图拓扑、无 HGCN-vs-Euclidean GCN 对照（门槛 1/3/5 全空）；② 无任何可宣传的正贡献（主结论是 matched null result，作者自认无方法学新颖性）；③ 投稿硬门槛 5 项占位；④ 路由问题——按 open-data 语料路由提示，纯负荷预测无硬件/信号故事，更自然归宿是 Energies / Energy Reports / IEEE Access，而非 Electronics。
- **Top 风险：** ① 标题-内容完全背离（编辑层 return 级：正文白纸黑字声明"对标题中的图卷积方法不提供任何结果"）；② 零正结果 + 自认无新颖性 → 应用刊无接收槽位；③ 完整性全占位。
- **结论：** 本稿当前形态正确对应"Stage-2 审计证据包"而非可提交稿。44/50 分衡量的是以现标题投 Electronics 的就绪度；若仅按"实验执行 + 科学诚实"两维计分可达 90 分档——作为 Stage-2 内部证据它是高质量的。真实 HGCN 未实现前，该标题不可投稿，这与签核包红线完全一致。

## 四、与 Stage-2 批验收的关系

1. **四篇的 Stage-2 文献阶段质量得到独立评分支持：** 文献核验、红线保留、负结果可见性均达标（风险控制 3–5/5，红线逐条核对无一处被淡化或改写）。四篇的编译证据（28/29/29/25 页、0 未定义引用）与签核包一致。
2. **评分低分项全部落在 Stage-2 范围之外**（方法/实验阶段未完成、投稿后置字段未填），与签核包自身声明一致——"接受 Stage 2 不代表稿件可投"。
3. 从评分角度看，**对四个 Stage-2 SHA 的接受建议可以支持**；四篇的分差反映的是各稿距离"可投"的剩余工作量差异，其中 P1 剩余工作量最小、P4 最大。

## 五、进入第三阶段前必须挂账的阻塞项

| 论文 | Stage 3 必须处理（按优先级） | 投稿后置字段（可延至 Stage 7，但已挂账） |
|---|---|---|
| P1 | ① 摘要/引言/cover letter 补 power-grid investment portfolio 连续语义；② 为 0.89%/1.01% 补工程可读解释或把卖点对齐为"预算约束组合搜索框架"；③ pymoo 版本钉扎 + 基线公平性处置 | Funding、CRediT、Data Availability 持久链接 |
| P2 | ① 成本校准（LCC/NPV 或有来源归一化）；② 第二独立问题族；③ 精确/ε-constraint 小实例参照 | 同上 + COI 具名披露雇佣关系（诚信级） |
| P3 | ① 拆 2×2 四臂（红线 1）；② action-aligned AC 映射 + 种子复现（红线 2）；③ "Self-Adaption" 拼写处置方案 | Funding、CRediT、Data Availability |
| P4 | ① 实现真实 HGCN + 匹配欧式 GCN 消融（红线，否则标题不可投）；② 决定投稿路由（纯负荷预测 → Energies/Energy Reports/IEEE Access 更自然）；③ 若单独发表负结果审计需换真实标题 | 5 项占位（Funding/CRediT/Acknowledgments/COI/AI 声明） |

## 六、结论

- 四篇按 Paper_CCF 期刊画像评分为 **P1 63 / P2 60 / P3 57 / P4 50**（100 制，六维等权），就绪度依次为有条件可投 / 未达门槛 ×3。
- 四篇的共同强项是证据纪律与科学诚实性（远超目标期刊语料常态），共同弱项是标题-证据落差与投稿完整性未闭合。
- 评分支持对四个 SHA 的 **Stage-2 范围接受**；四篇均不具备以锁定标题直接投稿的条件，分差即各稿 Stage 3 剩余工作量的度量。
- 所有 IF/APC/周期数字为 Paper_CCF 技能包 2026-07 快照，投稿前须按各刊官网当年数据复核。

---
_评估口径：Paper_CCF 期刊模块画像 + `05` 前评估最低接收门槛 + Stage-2 签核包红线。评分不构成录用保证，也不替代编辑判断。_
