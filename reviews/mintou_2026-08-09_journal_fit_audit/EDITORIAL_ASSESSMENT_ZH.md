# mintou 六篇论文逐段逐句期刊适配审查

审查日期：2026-08-09  
审查对象：六个项目中 2026-07-23 更新的 `manuscript/MANUSCRIPT.md`  
性质：只读投稿前评估；未修改任何论文正文。

## 1. 总结结论

六篇稿件均已形成完整的“问题—方法—实验—限制”叙事，统计检验、消融分析和负结果披露普遍强于本地同期同刊样本的常见下限。然而，**目前没有一篇达到可原样提交状态**。共同阻断项是作者/单位/基金/仓库 DOI 等占位符未清空、仍为 Markdown 主稿而非目标期刊模板，以及正文中残留内部投稿话语。科学层面，P2、P3、P4已接近期刊可审水平；P1需要把论文身份彻底稳定为“基准与机制边界研究”；P5、P6还面临核心组件贡献偏弱、外部效度不足以及姊妹稿同源风险。

按当前成熟度排序：**P4 > P2 ≈ P3 > P1 > P6 > P5**。

| 论文 | 当前目标 | 期刊适配 | 当前建议决定 | 最主要风险 |
|---|---|---:|---|---|
| P1 DSTAR-GRU | IEEE Access | Medium | 大修后再投 | 方法不赢主指标；论文身份在算法稿与基准稿之间摇摆；单一 cap 的方法结果 |
| P2 CSA-LoadNet | MDPI Electronics | Medium–High | 完成必修项后可投 | 架构创新弱；缺少层级预测 reconciliation 基线；正文偏短且长句密集 |
| P3 CARS-MODE | MDPI Energies | Medium–High | 大修后可投 | 标题核心“strategy-adaptive”在 proxy HV 上中性，AC 支持仅为组合层面定性证据 |
| P4 SHIELD-MOEA | MDPI Energies | High（六篇中最高） | 针对性大修后优先投 | screening 不提升质量且当前无实际 wall-clock 收益；恢复过程与 GA/DE 消融缺失 |
| P5 TRACE-MOEA | MDPI Energies（与 README 的 IEEE Access 冲突） | Medium–Low | 暂缓投稿 | preference adaptation 仅 +0.17%；无专家标签/电气验证/完整敏感性；参考文献陈旧；与 P6 同源 |
| P6 BiLo-NSGA | MDPI Applied Sciences | Medium | 大修并完成姊妹稿独立性审计后再投 | backward deletion 不增益；应用验证不足；与 P5 同源；重复 Limitations；句子过长 |

这里的“High”只表示题材和现有证据与期刊相配，不表示编辑一定录用。

## 2. 对照基线

本地参考集合包含 67 篇与六个主题相近、发表于目标四刊的 2023–2026 年论文；其中可读 PDF 按期刊统计如下。PDF 抽取的词数包含部分图表文字，Markdown 主稿词数不完全同口径，因此只用于判断明显偏离，不作为页数硬门槛。

| 期刊 | 本地样本数 | 页数中位数 | 正文词数中位数 | 单句平均词数的论文间中位数 |
|---|---:|---:|---:|---:|
| IEEE Access | 3 | 20 | 12,110 | 21.4 |
| Electronics | 15 | 21 | 7,103 | 22.1 |
| Energies | 36 | 23 | 7,541 | 24.0 |
| Applied Sciences | 13 | 24 | 7,814 | 22.3 |

六篇主稿正文（含表格、参考文献前）约为：P1 5858词、P2 5943词、P3 6937词、P4 7691词、P5 7663词、P6 8167词。P4–P6已达到同刊中位规模；P2略短但并非硬伤；P1显著短于仅有的3篇 IEEE Access 对照样本，但 IEEE Access 没有硬性页数下限，真正问题是验证覆盖而不是字数。

目标期刊的核心判断标准来自最新本地画像并以官网为准：

- IEEE Access：技术/科学 soundness、完整性、可复现性和清晰度；二元 Accept/Reject 模式意味着投稿时应接近终稿。官方入口：<https://ieeeaccess.ieee.org/authors/submission-guidelines/>。
- Electronics：电子/计算系统场景明确，方法完整，数据划分、超参数、基线和复现实验充分。官方要求：<https://www.mdpi.com/journal/electronics/instructions>。
- Energies：能源应用明确，模型需有实验、数值或真实数据验证；规划/优化稿尤其需要敏感性和工程解释。官方要求：<https://www.mdpi.com/journal/energies/instructions>。
- Applied Sciences：具体应用价值、超出理想化条件的验证、跨学科可读性及明确受益者。官方要求：<https://www.mdpi.com/journal/applsci/instructions>。

## 3. 逐句、逐段审查概览

逐句审查覆盖 1405 句；“BLOCK”表示投稿前必须处理，“REVISE”表示语言、逻辑或主张强度需修改，“CHECK”表示需作者/数据负责人复核，“PASS”表示未发现规则级问题，并不等于事实已由人工逐项复现实验。

| 论文 | 句数 | PASS | REVISE | CHECK | BLOCK | 段落数 | 需处理段落 |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 322 | 283 | 35 | 0 | 4 | 86 | 37 |
| P2 | 175 | 144 | 27 | 0 | 4 | 61 | 26 |
| P3 | 207 | 169 | 34 | 0 | 4 | 70 | 31 |
| P4 | 218 | 184 | 27 | 1 | 6 | 74 | 28 |
| P5 | 263 | 236 | 21 | 3 | 3 | 88 | 23 |
| P6 | 220 | 165 | 45 | 2 | 8 | 78 | 36 |

全文平均句长：P1 17.0、P2 26.3、P3 27.8、P4 27.3、P5 23.3、P6 30.0词。P2/P3/P4/P6明显高于对应期刊样本的约22–24词，P6最需要拆句。各句的文本、原始行号、状态、问题代码和中文建议见同目录的六个 `*_sentence_audit.csv`；逐段状态见 `*_paragraph_audit.csv`。

## 4. 共同章节问题

### 4.1 标题与摘要

摘要总体是六篇最成熟的部分：均给出数据规模、方法、比较对象、效应量/显著性和边界，且没有把负结果隐藏。需要统一减少“honest”“deliberately conservative”“without trusting the authors”等带辩护色彩的表达。标题中机制名必须与消融证据一致：P3的 strategy adaptation、P4的 scenario screening、P5的 preference adaptation、P6的 bidirectional search都存在“标题居中、增益却主要来自其他组件”的张力。

### 4.2 Introduction

问题—缺口—方法—贡献链完整，但若干段落同时承担背景、批评、方法动机和贡献声明，造成45–97词长句。应把每段限定为一个功能：背景事实；已知不足；本文问题；贡献与证据。删除“venues we target”“reviewers should treat … as a red flag”等编辑过程话语。

### 4.3 Related Work

文献分线合理，但P5的近三年参考文献严重不足；P1也偏旧。P3/P4、P5/P6均需要以清晰表格说明共享资产、不同研究问题、不同算法组件、不同实验和不同结论。不能只靠“companion study”段落自我声明独立性。

参考文献近三年（2023–2026）占比：P1 6/28（21.4%）、P2 11/30（36.7%）、P3 12/32（37.5%）、P4 17/45（37.8%）、P5 2/33（6.1%）、P6 18/32（56.2%）。经典算法引用可以保留，但P5必须系统补充2023–2026年的电网投资组合、偏好式多目标优化、可解释/可审计优化和工程验证文献。

### 4.4 Methodology

方法描述总体可复现，参数和算法步骤比普通应用稿完整。主要不足是“命名组件”与“已证明作用”不一致：

- P3：repair/diversity承载 proxy HV 增益，strategy adaptation只在粗粒度 AC 映射中显示差异。
- P4：repair承载质量增益，screening只减少代理评估次数，而且当前代理计算过快，未产生实际时间收益。
- P5：repair承载大部分增益，preference adaptation只有0.17%，trace archive尚未由用户研究证明有用。
- P6：forward insertion承载增益，backward deletion不贡献 HV。

因此必须二选一：补做能够直接验证命名组件价值的实验，或降低标题/摘要/贡献列表中该组件的中心地位。

### 4.5 Experimental Setup and Results

优点是 seeded runs、Holm校正、消融、敏感性、负结果和限制普遍齐全，显著高于三个MDPI期刊的常见最低线。主要欠缺：

- P1：0.60/0.80 cap只刻画任务，没有重跑完整方法排名；没有第二系统。
- P2：Ausgrid没有 bottom-up、MinT 等 reconciliation 专用基线；CPU轻量配置可能低估强模型。
- P3：AC层仅组合映射、每方法样本小，不能统计证明 adaptive component 的电气优势。
- P4：没有把 power flow/time-series simulation 放入筛选循环，故65%评估减少不能转化为实际速度收益；GA/DE hybrid未消融。
- P5：没有专家标签、AC/OPF验证和完整超参数敏感性；MTEP标签约98%为built，类别极不平衡。
- P6：没有专家标签、成本校准、第二数据集和load-flow验证；MTEP同样受高built基率限制。

### 4.6 Discussion, Limitations, Conclusions

证据边界写得诚实，这是明显优势。但六篇都存在一定程度的“方法学自传”和“预先替审稿人辩护”。例如“a reader equipped to distrust us”“worth a subsection”“not an inconvenience to be explained away”。应改为中性、可核验的学术语言。P6同时设置“7.1 Limitations and Future Work”和独立“8. Limitations”，结构重复，应合并。

### 4.7 投稿声明与格式

以下均属硬阻断项：

- 六篇均存在 `AUTHOR INPUT REQUIRED` 或等价占位符。
- P1/P4的作者、单位、通信作者信息仍为空；其他稿件仍缺经作者确认的CRediT、基金或仓库地址。
- 所有公开数据/代码承诺均写成“will be deposited”，但没有可点击的永久仓库/DOI。
- P5正文末尾保留内部 `Pre-Submission Checklist`，必须从论文删除。
- P5的 README 指向 IEEE Access，而当前主稿声明 MDPI Energies，必须冻结唯一目标期刊。
- 目前审查对象是 Markdown 主稿，不是目标期刊可提交的 LaTeX/Word/PDF；还没有模板分页、浮动体、图中文字和参考文献格式的最终质检。

## 5. 逐篇编辑结论

### P1 — IEEE Access

亮点是方法无优势时仍保留结果，且构建了可复现的curtailment-risk/onset benchmark。IEEE Access按soundness而非高创新度评审，因此负结果本身不是拒稿理由。风险在于论文标题和贡献应以benchmark为主，DSTAR-GRU只能是被研究对象；若仍按算法论文宣传，主指标被Persistence和ridge击败会直接破坏主张。建议补完整cap重跑或明确降为任务敏感性分析，并增加近期curtailment/onset forecasting文献。当前判定：**Major revision；不宜直接投。**

### P2 — Electronics

OPSD 24h上的显著改善、多个神经基线、消融和跨数据边界实验满足Electronics的应用ML审查逻辑。Poincaré/Euclidean/equal-weight不分胜负后将方法改为CSA-LoadNet是正确方向。主要补缺是层级场景reconciliation基线、仓库与CRediT占位符，以及长句压缩。当前判定：**最接近可投的一组之一；完成P0并补/解释reconciliation基线后可提交。**

### P3 — Energies

统计强度、敏感性和AC验证都达到较好水平；proxy与AC结论不一致反而有科学价值。问题是题名和方法名突出strategy adaptation，而其proxy贡献不显著，AC证据又不是节点级随机重复验证。应补专门的节点级/多工况AC对比或把adaptive component定位为辅助机制。当前判定：**Major revision后有较好机会。**

### P4 — Energies

主比较、worst-case readout、unseen stresses和AC层构成六篇中最完整的证据链。关键缺口是screening只节省代理评估次数而没有实际运行时间收益；标题仍把它放在中心。建议增加昂贵评估循环的小规模实证、补NoDE/NoGA消融，并将“resilience”严格限定为当前代理与N-1验证覆盖。当前判定：**六篇中优先投稿候选，但仍需一次针对性大修。**

### P5 — Energies

trace quarantine和外部效度梯度的设计值得保留，但方法名称中的preference adaptation只贡献0.17%，真实应用有效性仍没有专家标签、电气可行性或经济校准支持。参考文献只有2/33来自2023–2026，且末尾5条未在正文引用；姊妹稿引用仍是未完成条目。当前判定：**暂缓投稿；先补科学验证、更新文献并解决与P6的独立性。**

### P6 — Applied Sciences

预算敏感性与forward insertion的效应方向一致，统计包也充分；但backward deletion不改善HV，使“bidirectional”标题存在组件价值张力。Applied Sciences重视实际应用，而本文仍缺专家标签、货币成本和load-flow验证。P5/P6共享候选生成、数据源、基线与外部回测，必须提供可量化的文本/图表/实验独立性审计。当前判定：**Major revision；完成应用验证和姊妹稿审计后再投。**

## 6. 建议执行顺序

1. 冻结每篇唯一目标期刊、作者顺序、单位、通信作者、基金和数据/代码仓库。
2. 先解决科学阻断：P4昂贵评估/混合算子消融，P2 reconciliation基线，P3 adaptive机制电气验证，P1 cap重跑，P5/P6专家/电气/独立性验证。
3. 对P3/P4与P5/P6分别做共享资产和文本重合审计，形成随投稿信提交的透明披露材料。
4. 按六个逐句CSV处理BLOCK和REVISE项；优先拆分P6、P3、P4、P2的长句，删除辩护式元话语。
5. 转入IEEE Access或MDPI正式模板，完成交叉引用、图表、公式、参考文献和声明检查，再生成PDF做视觉质检。
6. 只有在实验结果、论文数字、公开仓库和PDF四者一致后，才进行最终投稿模拟评审。

## 7. 审查边界

本轮逐句标签检查语言、逻辑、期刊适配和显性主张风险；它没有重新运行全部实验，也没有逐项复核每个数值与原始CSV的一致性。`PASS`表示句子未触发本轮问题规则，不等于其事实自动成立。下一轮若进入修改阶段，应增加claim-to-evidence逐数核验和可执行代码复现。
