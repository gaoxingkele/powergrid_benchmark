# Round-3 投稿前自检评审：mintou_p6 (BiLo-NSGA) — MDPI Applied Sciences

- 评审日期：2026-07-16（离线模式，paper_reviews 框架：mdpi_applied_sciences.yaml + accepted_profile）
- 稿件：`mintou_p6_bilonsga_project_review/manuscript/MANUSCRIPT.md`（4 图，300 dpi）
- 证据核对源：`papers/mintou/mintou_p6_bilonsga_project_review/evidence/`（leaderboard / significance / nerc / **mtep**）、`src/configs/real_project_review_config.json`、`src/powergrid_benchmark/mintou_real_project_review.py`
- 前序：Round-2 评审（2026-07-13）预测 Major→post-fix Minor；本轮核查 Round-2 修改项落实情况 + 新增 MTEP 证据的并入问题

---

## 0. Desk Screen（编辑部初筛视角）

| 检查项 | 状态 |
|---|---|
| IMRaD 结构 + 量化摘要（给出 1.57%、44/48 等具体数字） | 通过（该刊惯例） |
| MDPI 四件套（Author Contributions / Funding / DA / COI） | 已搭好模板，**含 [TODO] 占位** — 提交前必须填齐 |
| 作者/单位/通讯 | **[TODO] 未填** |
| Data Availability 仓库 URL/DOI | **[TODO] 未填** — MDPI 强制项，缺失即技术性退修 |
| [sibling] 参考文献 | **占位符** — p5 手稿尚不存在（`mintou_p5_.../manuscript/` 目录不存在，仅 32 行 PAPER.md 骨架），提交时无法给出可解析引文 |
| 图件 | 4 张 300 dpi PNG 齐全，灰阶+单蓝主色，风格克制专业 |
| 参考文献 28 条 | 略低于该刊常态底线（~30，中位 41）；近 5 年占比约 46%（达标） |
| 英语质量 | 良好，无明显粗糙段落 |

结论：内容层面可进入外审；但 5 处 [TODO] 中任何一处带入投稿都会在编辑部环节被打回。

---

## 1. 七维逐条 Findings（severity 0–4 × confidence 0–1 × fixability 0–1）

### 1.1 Novelty（权重 1.2）— 得分 7.0/10

**N1 [sev 2 | conf 0.9 | fix 0.9] — [sibling] 引文在投稿时不可解析。**
Section 2.4、3.4、7、DA 声明五处引用 [sibling]（TRACE-MOEA 姊妹稿），但 p5 手稿尚未写出。MDPI 不接受 reference list 中的 "to be inserted upon publication"。修法：保留 2.4 的机制区分段（这是对 Round-2 F1.1 的正确落实），但把 [sibling] 从参考文献表移为正文内注（"a companion study currently in preparation"），或等 p5 获得 preprint DOI 后再投。
**N2 [sev 1 | conf 0.85 | fix 0.95] — "budget-parity substitution" 措辞超出实现。**
Section 2.4 与 gap 陈述把 substitution 说成与 forward/backward 并列的移动类型（"whose substitution moves exchange projects at budget parity"），而 Section 4 明确 substitution 只是"插入+删除在同一 pass 内的涌现效果"，代码中也无独立 substitution 算子。审稿人对照 4.7 伪代码会发现不一致。修法：2.4/2.4 末尾 gap 句改为 "emergent budget-parity substitution (an accepted insertion followed by an accepted deletion)"。
**N3 [sev 0（正面）] —** 组合式创新 + 应用场景针对性论证符合该刊接受画像（11/11 无全新算法）；逐组件 Motivation 段（4.2–4.6）落实了 Round-2 F1.2；"预算词汇表局部搜索 + per-move audit trail" 的 gap 陈述具体、可检验。

### 1.2 Soundness（权重 1.4，最高）— 得分 7.5/10

**S1 [sev 3 | conf 0.95 | fix 0.9] — 最重要发现：MTEP 回验证据已存在，稿件却在三处声称其为 future work。**
`evidence/tables/real_mtep_backtest.csv` + `evidence/runs/real_mtep_backtest_analysis.md`（status `public_miso_mtep16_outcome_backtest_v1`）是稿件完成后新增的真实外部锚：MISO MTEP16 Appendix A/B 共 1218 个真实项目、以 2016–2018 季度快照 + 2026 in-service 名单为**真实结局标签**（built=924 / withdrawn=19 / deferred=39 / unresolved=236），特征仅用 2016 年决策时点字段，与候选构造零构念重叠。结果：BiLo-NSGA broad outcome-capture 1.084（point-biserial r=0.105，p=0.0006）与 1.065（r=0.080，p=0.010），显著高于随机且高于全部演化基线（NSGA-II 仅 1.012/1.014，n.s.），但低于 AHP-TOPSIS（1.100/1.097）；strict 标签方向一致但检验力不足。
而稿件 Section 6.4（"the required true external anchor — a historical backtest against MISO MTEP project decisions — remains future work"）、Limitation 3、Conclusion 三处仍称 MTEP 为未来工作。投稿即发布仓库（DA 声明承诺公开 evidence trail），届时"论文说没做、仓库里躺着结果"构成事实不一致；且这是白白放弃一条**恰好补强本文最大弱点（外部效度）**的证据——它把 external-validity ladder 从"consistency 阶"推进到"真实历史结局阶"，同时诚实边界（strict 欠检验力、~98% 建成基率天花板、renewable 类型在 MTEP16 中近乎缺失、Appendix-status 特征的注意事项）在 analysis.md 中已写好，可直接移植。
**必须并入**（新 Section 6.5 + 改写 Limitation 3 + Conclusion + 摘要末句可选），并以 weak-form 措辞呈现：真实结局对齐存在且显著、优于所有演化基线、但效应量小且 AHP-TOPSIS 更高（与 NERC 节已有的 "by construction / evidence-weighting" 论证同构）；expert labels 仍留作 future work。
**S2 [sev 0（正面）] — 全部数字核对通过。** 逐项核验：pooled HV 0.17267/1.57%/6.35%/24.4%；44/48 Holm 显著胜、0 显著负、4 个 n.s. 案例及其归属；Table 5 全部 8 行均值/相对差/p 值；消融百分比（−79.4/−1.28/−0.56/−0.55/−0.39/−0.07/+0.16/−0.03/−6.13）；backward 最大单实验差 Holm p=0.325；forward 5/8 显著；NERC capture 1.62/1.35、NSGA-II 1.57、AHP 2.31/1.60、τ=0.44/0.50、BiLo τ=0.06/0.17 n.s.、Greedy BCR 0.23–0.45 负 τ、MOEA/D reliability 面板缺席；3430 moves/run、coverage 98.6%、front 38.6 vs 40.0、cost index 0.948 vs 0.940、runtime 0.193/0.080 s；16×8×30=3840 runs；代码超参（depth 8/4、bonus 1.06、pop 40、gen 40、2048 参考组合、ref point 1.1）与 4.2–4.7 一致。**无一处与 CSV/代码矛盾。**
**S3 [sev 0（正面）] —** backward 负贡献的诚实处理（6.3 + Discussion "one passenger under redesign"）正是该刊奖励的坦诚风格，落实了 Round-2 F1.3 的 option (b)。

### 1.3 Experiments（权重 1.3）— 得分 8.0/10

**E1 [sev 1 | conf 0.9 | fix 0.95] — NERC 回验文字有选择性强调。**
6.4 写 "above NSGA-II in the budget-constrained scenario (1.57)"，属实；但未提 reliability 面板中 NSGA-II（1.403）反超 BiLo（1.353），也未提 budget 面板中 NoForwardSearch/ShallowLocalSearch（1.67）高于全法（1.62）。Figure 4 已如实画出全部条形，审稿人一眼可见文字与图的重心差。修法：加一句 "in the reliability panel NSGA-II attains a slightly higher capture (1.40 vs. 1.35), and single-objective-leaning ablations can exceed the full method — consistent with the dilution argument above"。
**E2 [sev 1 | conf 0.8 | fix 0.9] —** 若并入 MTEP（S1），须说明其协议差异：10 seeds/compromise portfolio（而主实验 30 seeds/HV），并解释 point-biserial + Mann-Whitney 为主读数、capture 为效应量的原因（strict 基率 ~98% 的天花板）——analysis.md 已备好措辞。
**E3 [sev 0（正面）] —** 6 基线 + 9 消融 + 30 seeds + Holm 校正超出该刊元启发式子领域门槛（7–9 基线常态）；预算敏感性曲线（Fig 2）正中该刊"应用可信度货币"；两个 n.s. 场景（0.75x、renewable pool）被正面讨论而非隐藏；LooseBudget −6.13% 给出"硬约束须在搜索期内生效"的机制论证。Round-2 F3.1/F3.2/F3.3 全部落实。
**E4 [sev 1 | conf 0.6 | fix 0.7] —** 预算扫描仅 4 档（0.75/0.88/1.00/1.20），Round-2 建议的 0.5x/1.5x 外延未做；非必需（现有 4 档已支撑结论），审稿人若问可在修回补（~3 分钟计算量）。

### 1.4 Reproducibility（权重 1.1）— 得分 7.5/10

**R1 [sev 2 | conf 0.95 | fix 1.0] —** 仓库 URL/DOI [TODO]。MDPI DA 强制项；建议 Zenodo DOI（顺带把共享管线命名为公共基准，落实 Round-2 的 "PGReview-120" 策略）。
**R2 [sev 0（正面）] —** 数字↔CSV↔代码三方一致（见 S2）；v1 循环评价指标的弃用被明文披露并保留 deprecated 工件，透明度是加分项；NERC 数据只引 metadata + 官方 URL，无 PDF 再分发问题。
**R3 [sev 1 | conf 0.7 | fix 0.9] —** 正文引用了 `evidence/...csv` 相对路径（Table 1/3/4/5 标题内）；投稿版应改为指向公开仓库的路径或删去内部路径，避免暴露未发布目录结构。

### 1.5 Related Work（权重 0.9）— 得分 6.5/10

**RW1 [sev 1 | conf 0.95 | fix 1.0] — Behzadian et al., 2012 在参考文献表中但正文从未引用。** MDPI 编辑部会要求逐条对应；在 2.2 的 TOPSIS 句补引或删除。
**RW2 [sev 1 | conf 0.85 | fix 1.0] — Qi et al. 卷号/年份不一致：**"Energies **2025**, **19**(1), 210" — Energies 第 19 卷对应 2026 年（第 18 卷才是 2025）。应为 2026, 19(1) 并同步正文引注 [Qi et al., 2025]→[2026]（或核实真实出处）。
**RW3 [sev 1 | conf 0.8 | fix 0.9] —** 28 条略低于该刊 ~30 底线/中位 41；三线（knapsack-MOEA / 电网投资 / memetic）覆盖是好的，补 3–5 条 2024–2026 近作即可（顺带稀释对 MDPI 系刊物的集中度：MDPI 系约 12/28）。
**RW4 [sev 0（正面）] —** 2.4 对 TRACE-MOEA 的机制/问题框架双轴区分具体、可证伪（"neither contains the other's core operator"），是 Round-2 差异化方案的正确执行。

### 1.6 Clarity（权重 1.05）— 得分 8.0/10

**C1 [sev 0（正面）] —** 受益者点名（Intro："grid planning departments and investment review boards…"；Discussion 给出面向 planning department 的三条操作性解读）；量化摘要；条目化贡献；5 条 limitations 的坦诚清单 — 全部命中该刊接受画像的显性特征。
**C2 [sev 1 | conf 0.7 | fix 0.9] —** Figure 1 纵轴从 0 起，顶部六法箱体被压扁，主要对比（BiLo vs NSGA-II/III）几乎不可分辨；建议加截断轴或每面板自适应 y 范围（保留全轴小图作 inset 亦可）。
**C3 [sev 0 | conf 0.9] —** Table 4 按 HV 排序把 NoBackwardSearch 排在提出法之上——诚实且与 6.3 叙事一致，保留即可（审稿人视为坦诚信号）。

### 1.7 Ethics（权重 0.6）— 得分 7.5/10

**ETH1 [sev 1 | conf 0.9 | fix 1.0] —** 四件套已搭好但含 [TODO]；另 MDPI 现行政策要求披露生成式 AI 在写作中的使用情况——按实际情况添加或确认不适用。
**ETH2 [sev 1 | conf 0.85 | fix 0.8] — 姊妹稿共享基准已双处显式声明（3.4 + DA），这是对 salami-slicing 红线的正确防御；剩余风险取决于执行纪律：**保持 p5/p6 不同出版商 + ≥6 周投稿间隔（Round-2 方案），且 p6 若先投，正文对 p5 的描述须与 p5 最终稿一致（当前 p5 尚无手稿，2.4 的描述基于其设计文档，存在漂移风险——p5 成稿后需回核一次）。
**ETH3 [sev 0（正面）] —** v1 循环指标的弃用与保留披露、audit-trail 统计不进评价指标的双重声明，均是超出该刊平均水准的诚信实践。

---

## 2. 对抗核验（对最严重 3 条 finding 的自我反驳）

**A. S1（MTEP 应并入）— 试图反驳：**
(i) "MTEP 是稿后新证据，不并入也不算错"？不成立：DA 声明承诺发布完整 evidence trail，`real_mtep_backtest.csv` 首列即 `paper=p6`，发布之日起 6.4/L3/结论三处 "remains future work" 即为与自家公开工件矛盾的陈述。(ii) "并入反而有害——效应量太小（1.08x）且 AHP-TOPSIS 更强，会削弱论文"？部分成立但可控：analysis.md 已给出与 6.4 同构的辩护（AHP 的 broad 优势部分来自 Appendix-status/evidence 加权；strict 面板 BiLo 1.013 为全场最高之一；所有演化基线均 n.s.）；且"weak-form 支持 + 诚实边界"正是该刊奖励的姿态，比"声称没做"风险低得多。(iii) 反向核查数据可信性：pool/标签计数（1097/844/17/201/35）在 CSV 与 analysis.md 一致，p 值内部一致（BiLo r=0.105 @ n≈1045 → p~6e-4 量级，吻合）。**结论：finding 成立，维持 sev 3；修复方向为并入而非删除工件。**

**B. N1（sibling 引文不可解析）— 试图反驳：**
"可以以 'unpublished work' 形式引用"？MDPI 允许正文内 "(in preparation)" 式提及，但不允许无法解析的条目占据 reference list；当前 [sibling] 在参考文献表中且被 5 处引用。若 p5 两周内产出 preprint DOI 则本条自动消解——但今日状态下（p5 manuscript 目录不存在）finding 成立。**维持 sev 2，fixability 0.9。**

**C. E1（NERC 选择性强调）— 试图反驳：**
"文字陈述字面为真，且 Figure 4 完整展示了全部方法，不构成选择性报告"？核对属实：图与 CSV 完全一致，未隐藏任何条目；且 6.4 已主动披露对己不利的 AHP 优势与 τ 不显著。因此这不是 integrity 问题，只是文字重心与图的不对称。**降级确认为 sev 1（润色级），不影响决策。**

---

## 3. Meta 决策

### 维度得分与加权

| 维度 | 得分 | 权重 | 备注 |
|---|---|---|---|
| novelty | 7.0 | 1.2 | 组合式创新达标；sibling 引文待解 |
| soundness | 7.5 | 1.4 | 数字全部核验通过；MTEP 不一致是唯一扣分主项 |
| experiments | 8.0 | 1.3 | 超出子领域门槛；敏感性曲线到位 |
| reproducibility | 7.5 | 1.1 | 待仓库 DOI |
| related_work | 6.5 | 0.9 | 28 条略薄 + 1 条未引用 + 1 处卷号错误 |
| clarity | 8.0 | 1.05 | 接受画像显性特征全命中 |
| ethics | 7.5 | 0.6 | 四件套占位待填；共享基准声明是防御亮点 |
| **加权均分** | **7.46** | | 阈值 5.5；accept_mean 6.0 |

### 预测决策：**Accept after Minor Revision**（若审稿人自行发现仓库中的 MTEP 工件而稿件未提，则有滑向 Major 的尾部风险 ~20%）

Round-2 的三大修改项（手稿成文、p5 差异化、可视化证据）已高质量落实；本轮不存在 yaml 红线触发项；剩余问题全部为高 fixability 的文字/事务级修改，唯 MTEP 并入需要一节新增写作（证据与诚实边界文本已在 analysis.md 备好，预计 0.5–1 天）。

### 修改清单（按优先级）

| 优先级 | 修改 | 对应 finding |
|---|---|---|
| **P0** | 并入 MTEP16 真实结局回验：新增 Section 6.5（weak-form 措辞 + 10-seed 协议说明 + 诚实边界四条：strict 欠检验力 / 98% 建成基率天花板 / renewable 类型缺失 / Appendix-status 特征注意），同步改写 Section 6.4 末句、Limitation 3、Conclusion；摘要末句可加 "and a historical backtest against MISO MTEP16 outcomes shows selection–outcome alignment significantly above chance" | S1, E2 |
| **P0** | 填齐全部 [TODO]：作者/单位/通讯/CRediT/Funding/仓库 DOI（建议 Zenodo，顺带命名共享基准）；[sibling] 改为正文内注或等 p5 preprint DOI | N1, R1, ETH1 |
| **P1** | 参考文献修缮：Behzadian 补引或删除；Qi et al. 卷号年份改正（Energies 19(1)=2026）；补 3–5 条 2024–2026 近作至 ≥30 条 | RW1–RW3 |
| **P1** | NERC 节补一句承认 reliability 面板 NSGA-II capture 略高（1.40 vs 1.35）及单目标倾向消融可超过全法，与稀释论证呼应 | E1 |
| **P2** | 措辞对齐："budget-parity substitution" 改为 emergent 表述；正文内 `evidence/...` 内部路径改指公开仓库；Figure 1 y 轴截断/inset 提升可读性 | N2, R3, C2 |
| **P2**（修回备用） | 预算扫描外延 0.5x/1.5x 两档；p5 成稿后回核 2.4 描述一致性 | E4, ETH2 |

---

*本评审基于对稿件全文、四张图、全部 8 个证据 CSV、配置 JSON 与算法实现源码的静态核对；所有数字断言均已逐项复算（见 S2）。未执行外部网络检索；期刊政策以 Paper_CCF/accepted_profile 蒸馏为准，投稿前请以期刊官网为最终依据。*
