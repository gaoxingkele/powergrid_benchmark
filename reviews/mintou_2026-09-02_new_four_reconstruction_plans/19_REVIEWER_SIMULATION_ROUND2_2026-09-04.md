# 模拟技术审稿人评审 — 第二轮（R2）

**日期：** 2026-09-04
**方法：** 以 Paper_CCF 期刊画像 + 12 号评分报告为基准，按目标期刊审稿人视角对四篇模拟评审；每条意见给出「回应方向 / 已覆盖契约 / 新增规格」。
**用途：** 预演 harness `s09`（journal-fit and four technical reviewer pass）；新增规格并入 13–16 号契约与 17 号质量门。

---

## P1 — TRACE-MOEA（Energies）

### P1-R2-1（审稿人）
"All outcomes are dimensionless proxy indices; the manuscript never demonstrates electrical or economic validity. How can 'Investment Effectiveness' be claimed?"

**回应方向：** claim-boundary 路线（已在 13 号契约 §1/§2 冻结）：AC 校验 NO-GO 记录在案，摘要/结论维持 proxy 措辞，有效性由"可复现审计工作流 + 事件摘要"承载，cover letter 明示。
**已覆盖：** 13 号契约 §2、18 号 P1-R1-1/2/4。

### P1-R2-2（审稿人）
"R-NSGA-II and MOEA/D sit an order of magnitude below the proposed method; unequal tuning makes every head-to-head uninterpretable."

**回应方向：** 公平调参协议（13 号 §3）：同等调参预算、调参/评估分离、pymoo 钉扎、过程全记录——这是审稿人无法反驳的修复。
**已覆盖：** 13 号契约 §3。

### P1-R2-3（审稿人）
"A pooled 0.89% hypervolume gap has no engineering meaning. What does it buy an operator?"

**回应方向：** 预注册三张工程换算表（入选项目数差/预算利用率差/风险暴露分差），随主表同报（13 号 §5）。
**已覆盖：** 13 号契约 §5。

### P1-R2-4（审稿人）— **新增缺口**
"The event co-occurrence summary reports 98.6% — what decision does this information support? An interpretability claim without an interpretive demonstration is a dangling contribution."

**新增规格 P1-6（并入 17 号质量门）：** 讨论章节须写一段**解释性使用场景**：以 2 个典型场景（预注册选取）为例，展示事件共现摘要如何支持审查人复核某项目的入选稳定性（纯描述性，不新增统计推断）。若无法写出可读解释 → 事件摘要贡献降为"记录完整性"口径，摘要对应措辞下调。

---

## P2 — BiLo-NSGA（Applied Sciences）

### P2-R2-1（审稿人）
"Cost coefficients are synthetic. Applied Sciences' reviewer question is 'what real benefit', and uncalibrated units cannot answer it."

**回应方向：** MTEP16 分位数映射校准（方案 A）或 NO-GO 记录（14 号 §2）。
**已覆盖：** 14 号契约 §2。

### P2-R2-2（审稿人）
"The local-search baseline looks under-configured; and the proposed method still loses to NSGA-II in matched budget. What is the paper's contribution?"

**回应方向：** 公平调参 PLS/NSGA-II 后重跑；贡献定位 = 等代价审计协议 + 项目词表局部搜索 + 对 PLS 的确认性优势；红线句保留（14 号 §4/§7、18 号 P2-R1-1）。
**已覆盖：** 14 号契约 §3/§4/§7。

### P2-R2-3（审稿人）
"A single synthetic pool limits generality; the MTEP16 layer is only descriptive."

**回应方向：** MTEP16 升级为完整协议第二任务族；3 个小实例精确参照（14 号 §2/§6）。
**已覆盖：** 14 号契约 §2。

### P2-R2-4（审稿人）— **新增缺口**
"Delete-insert substitution shows no accuracy gain. Does it improve anything else — plan interpretability, cross-scenario stability, group coherence? If the operator reads plans, not hypervolumes, these outcomes matter."

**新增规格 P2-7（并入 14 号契约 §5/§6）：** 预注册**解释性结果族**：① 相邻情景下解的入选项目重叠率（Jaccard）；② 组标签一致性（同一组项目是否成块入选/落选）；③ 替换算子开启时的计划修订路径长度（修订到更优解所需步数，等于"审查人可读的修改建议"度量）。这些度量不依赖 hypervolume，可能构成"不吹精度"的正向贡献。度量公式先验冻结。

---

## P3 — CARS-MODE（Energies）

### P3-R2-1（审稿人）
"'Self-Adaption' is claimed but parameter and strategy adaptation are never isolated; the fixed variant nominally wins on three metrics."

**回应方向：** 2×2 四臂拆分（红线 1）+ 先验 Rugged 条件假设 + analytic HV 主指标（15 号 §2/§4/§5）。
**已覆盖：** 15 号契约 §2/§4/§5。

### P3-R2-2（审稿人）
"Metric selection flips the ranking (sampled/clipped vs analytic vs IGD+). Reporting only favorable metrics would be outcome-selective."

**回应方向：** 预注册 analytic HV 为主 + 全指标同表同显著度 + Table 5/9 反转表保留（15 号 §5）。
**已覆盖：** 15 号契约 §5。

### P3-R2-3（审稿人）
"Decision variables are portfolio-level; the pandapower layer is a compositional mapping of a single compromise solution. This is not distribution-network planning."

**回应方向：** action-aligned 节点级 AC 映射 + 种子复现（红线 2），或 NO-GO 记录 + cover letter 处置（15 号 §2）。
**已覆盖：** 15 号契约 §2。

### P3-R2-4（审稿人）— **新增缺口**
"2940 runs are reported but compute cost never enters the analysis. Adaptation has a cost; does it pay for itself?"

**新增规格 P3-7（并入 15 号契约 §5/§6）：** 预注册**性价比度量**：每臂的"达到给定 HV 阈值所需平均目标调用次数"（quality-per-evaluation）+ 墙钟/运行；若自适应臂在 Nominal 条件性价比不劣，构成独立的正当贡献位（与精度优势解耦）。

---

## P4 — CSA-LoadNet（Electronics）

### P4-R2-1（审稿人）
"The title promises a hyperbolic graph convolutional network; the manuscript states it implements no GCN. Desk reject on title-content mismatch."

**回应方向：** 红线路线：实现前不投（16 号契约红线声明）；Stage-6 产出结果后按双版 headline 改写；此意见在实现前无法回应——这是当前形态的既定事实，交由 Stage-3~6 解除。
**已覆盖：** 16 号契约 §2/§7。

### P4-R2-2（审稿人）
"How is the graph constructed? Correlation graphs built from test-period data leak information."

**回应方向：** 图构造零测试期泄漏条款（16 号 §2，前评估风险条款）。
**已覆盖：** 16 号契约 §2。

### P4-R2-3（审稿人）
"Forecasting papers here need persistence and ≥2 error metrics; MAE/RMSE are not in any main table."

**回应方向：** persistence 补齐 + MAE/WAPE/RMSE 主表承诺段（16 号 §2、18 号 P4-R1-2/3）。
**已覆盖：** 16 号契约 §2、18 号 R1。

### P4-R2-4（审稿人）— **新增缺口**
"The paper uses Poincaré distance inside attention but states the temperature is 'not curvature'. What, precisely, is the hyperbolic claim once a GCN exists?"

**新增规格 P4-8（并入 16 号契约 §2）：** HGCN 实现时，方法章节必须**显式定义曲率**：模型、映射（exp/log）、曲率参数的语义与学习方式；并在消融中区分"双曲聚合的贡献"与"图结构的贡献"（几何消融正交表已有，补一行"曲率定义先行"条款）。

---

## 本轮结论

- 12 条模拟意见中 8 条已由 13–16 号契约覆盖（回应方向明确）；
- 4 条新增缺口（P1-6 解释性使用场景、P2-7 解释性结果族、P3-7 性价比度量、P4-8 曲率定义先行）为契约补充项——**其中 P2-7 与 P3-7 可能产生新的正向贡献位**，值得 Stage-4 纳入冻结协议；
- 待办：将 4 条新增规格写回对应契约文档（下轮迭代执行）。
