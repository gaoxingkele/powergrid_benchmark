# MA-SQLGrid 第二轮独立逻辑复审

## 复审结论

修订稿真正关闭了多项可核问题：v3/FINAL 版本归属、170项配对分母、“New v3”措辞、六图数量、协议估计量表和任意权重的限定均已修复。剩余核心障碍是标题所指的五角色效益仍未被实验估计，且主要电网语义证据来自一个开发可见的小型合成库。第二轮将原 Critical 降为 **Major residual**：稿件现在没有直接声称五角色 superiority，但“Robust Multi-Agent Framework for … Power Grid Databases”的投稿定位仍强于实证覆盖。

## 第一轮问题关闭矩阵

| Round-1项 | 状态 | 当前严重度 | 第二轮核验与精确锚点 | 仍需修复 |
|---|---|---|---|---|
| C1 无端到端五角色/多智能体效益实验 | **PARTIAL** | **MAJOR residual** | RQ1 已改为 software conformance（Introduction line 46）；Results opening line 359 明确“no result … estimates benefit”；Limitations lines 695–701 与 Conclusions lines 705–709 一致限定。可是 Title line 15 未变，Analyst/Cartographer 为 skeleton、Synthesizer 只包装外部 SQL，且全稿仍无 matched end-to-end experiment。 | 保留标题时补全新未见、物理调用/候选/模型/解码匹配的单体—分阶段—多候选—完整五角色比较；否则标题改为 auditable five-role architecture/evidence study。 |
| M1 高并列与顺序支配使选择器效应不可归因 | **PARTIAL** | **MAJOR if treated as performance；MINOR under current descriptive claim** | Results `tab:ties`, `tab:sensitivity`, lines 575–623 仍为 130/180 并列与 reverse-order 117–118；但 Abstract line 22、master protocol `tab:protocol-master`, `tab:offline` caption line 554、Discussion lines 677 onward 都正确降为 outcome-exposed descriptive behavior。 | 当前不可作为 performance contribution。新实验需预注册并列弃权/澄清、使用顺序不变规则或冻结多排列稳定性分析。 |
| M2 40/40/10/5/5 权重无理论或校准 | **PARTIAL** | **MINOR residual** | Methods line 241 已明确“illustrative…not learned, calibrated, or theoretically optimal”并列出五个软件不变量；这关闭了算法效益夸大，但没有使权重成为创新。 | 从贡献清单中排除权重；若希望成为方法贡献，在开发集定义损失和风险—覆盖效用，冻结校准后外测。 |
| M3 v3 与 FINAL 控制混合 | **CLOSED** | — | 新增 `tab:version-evidence`, lines 268–281，明确 v3 产生 5760/80/100/101，FINAL 只提供14项后置 conformance tests；Discussion line 685 和 Conclusions line 705 同步。 | 保持版本化措辞，打包文件也必须按版本分目录。 |
| M4 v3 evidence class 与 “New v3” caption 冲突 | **CLOSED** | — | `tab:offline` caption line 554 已改为“Descriptive release-v3 re-execution”；`tab:chronology` lines 190–210 和 Discussion line 677 一致。 | 无。 |
| M5 +0.1059 无法由表中170/180分母复算 | **CLOSED** | — | Component Results line 429 与 `tab:componentcounts` lines 436–451 已显示 Qwen 83/170→101/170、Granite 69/170→69/170，并把180项行分开。 | 建议补 discordant pair counts 到 supplement，但不再是正文逻辑缺口。 |
| M6 constructed witnesses 被外推为 counterfactual/semantic robustness | **CLOSED（正文主张）** | — | Methods lines 300–306 equivalent revised witness text、`tab:q039`、Results line 619 和 Conclusions line 709 均限定为 constructed projection/storage behavior，不称语义 rescue。 | keyword line 23 的 “counterfactual testing” 建议改为 “metamorphic testing”，避免元数据层再次扩大。 |
| m1 四图/六图冲突 | **CLOSED** | — | Methods line 355、Supplementary line 711、Acknowledgments line 717 均为 six。 | 无。 |
| m2 “robust”未操作化 | **PARTIAL** | **MINOR residual** | Abstract line 22 首段已操作化四个维度，`tab:robustness` 与 `tab:version-evidence` 给出边界。标题仍不带限定，Conclusion line 709 再次依赖正文解释 framework identity。 | 标题或副标题中加入 “read-only, evidence-complete” 限定；至少在关键词中移除未经同义验证的 counterfactual。 |

## 修改引入或暴露的新问题

### N1 — 电网标题与主要语义证据仍不相称

- **状态：OPEN；严重度：MAJOR。**
- **锚点：** Title line 15；Data Resources lines 136–146 and `tab:resources`：GridDB 仅1个合成库、8表、98行，evaluation partition development-visible；RTS-GMLC/SimBench 为零人工审查的 machine silver；BIRD 明确 non-grid。Limitations lines 691–697。
- **问题：** 软件执行边界可在 SQLite 上验证，但“for Text-to-SQL in Power Grid Databases”的语义有效性没有合格专家 gold 或外部真实电网查询集支持。该缺口与五角色效益缺口不同，不能由 BIRD 可移植性或 executor tests 替代。
- **修复：** 对 RTS-GMLC/SimBench 或许可明确的本地电网数据库建立双专家独立审查的 question–SQL gold，封存站点/数据库外部测试；至少报告 projection、单位、时界、排序和 tie semantics 的裁决前一致性。

### N2 — “Gold-isolated”软件属性容易与 outcome-exposed 科学设计混读

- **状态：PARTIAL；严重度：MINOR。**
- **锚点：** Algorithm `alg:coordination` caption line 284；Task boundary line 128；Chronology line 207 与 master table line 185；Discussion line 677。
- **问题：** 单次执行路径确实在 sealing 后才直接加载 raw gold，但 v3 冻结测试已访问同题 gold-derived outcomes。正文解释充分，但算法标题“Gold-isolated deterministic coordination”脱离上下文时可能被理解为整个研究 outcome-blind。
- **修复：** caption 改为“Within-run raw-gold-isolated coordination”，并在算法下增加一句“not study-process outcome blindness for release v3”。

### N3 — robustness 主表仍把两个版本放在同一维度行

- **状态：PARTIAL；严重度：MINOR。**
- **锚点：** `tab:robustness` Resource boundedness row line 260 同时列 timeout/opcode/row 与 FINAL raw-cell/total-result/width；紧随其后的 `tab:version-evidence` 才拆分。
- **问题：** 版本矩阵已足以消除实质误解，但第一张 robustness 表单行仍产生“统一系统同时具备全部控制”的第一印象。
- **修复：** 把 Resource boundedness 拆成 Release-v3 与 FINAL-additive 两行，或在该行 Registered operation 列直接标 `[v3]`/`[FINAL]`。

## 第二轮可投稿性判断

作为 **software architecture + retrospective evidence audit**，稿件已具备较强透明度；作为标题通常暗示的 **经验证 robust multi-agent Text-to-SQL 方法**，证据仍不足。投稿前最重要的不是继续扩写历史实验，而是决定是否补端到端未见实验和电网专家语义集。若不补，应进一步收窄标题和贡献身份。

