# Round 2 — 6 个 mintou 项目 paper_reviews 综合评审总结

- **日期**: 2026-07-13
- **评审轮次**: Round 2 (6-mintou 全量 paper_reviews 7 维评审,离线结构化,基于 ARA 证据 + Paper_CCF 目标刊 distilled standards)
- **优先级**: 快发优先(允许算法/数据集/下游任务修改,但大方向不变)
- **评审输入**: 6 个 mintou ARA 工程 + JOURNAL_REVIEW.md + 目标刊画像 + 跨项目组合分析
- **评审输出**: 6 份独立评审 + 1 份组合级综合报告(本文件)
- **独立评审文件**:
  - `reviews/2026-07-13_round2_mintou_p1_dstar_gru_review.md`
  - `reviews/2026-07-13_round2_mintou_p2_hygloadformer_review.md`
  - `reviews/2026-07-13_round2_mintou_p3_carsmode_review.md`
  - `reviews/2026-07-13_round2_mintou_p4_shieldmoea_review.md`
  - `reviews/2026-07-13_round2_mintou_p5_tracemoea_review.md`
  - `reviews/2026-07-13_round2_mintou_p6_bilonsaga_review.md`

---

## 1. 组合级总览

| 项目 | 算法 | 目标刊(主/次) | RRI | 预测决策(当前) | 修复后预测 | 最快路径 |
|---|---|---|---|---|---|---|
| **p1** | DSTAR-GRU(调度) | IEEE Access / Energies | 30.4/100 | Reject(0.85)/ Major(0.75) | Major Revision(Energies) | **~18 天 → Energies** |
| **p2** | HyG-LoadFormer(负荷) | Electronics / Applied Sci | 25/100 | **Reject(两刊)** | Accept 概率高 | **4-6 周 → Electronics** |
| **p3** | CARS-MODE(配网规划) | Energies / Applied Sci | 42% | Major(60%)/ Desk(25%) | Accept 概率高 | **3-4 周 → Applied Sci** |
| **p4** | SHIELD-MOEA(韧性) | Energies / PCMP | 2.22/4.00 | Reject/Major | Minor-Major,高接受率 | **6-8 周 → Energies** |
| **p5** | TRACE-MOEA(评审) | Applied Sci / IEEE Access | 1.73/4.00 | Major Revision | Accept | **~6 周 → Applied Sci**(p6 之后) |
| **p6** | BiLo-NSGA(评审) | Applied Sci / IEEE Access | 2.491 | Major Revision | Accept Minor | **7-10 天 → Applied Sci**(先投) |

---

## 2. 🚨 组合级 5 大跨项目问题

### 2.1 【最紧急】p2 "Transformer/Neural" 命名技术上为假

**严重度**: fatal(severity 4)
**问题**: p2 整个实现是 **Python 标准库 ridge regression + hyperbolic 距离加权特征**,**零 PyTorch / 零 attention / 零神经网络**。`src/environment.md` 明确确认 "Python standard library only"。
**风险**: 即便 24h/day-ahead 信号真实(OPSD +39-42%),按现状投稿构成**夸大主张**,对作者和实验室声誉是组合级最大风险。Electronics 任何 soundness reviewer 都会抓到。
**修复选项**:
- **A. 诚实改名**:标题/摘要删 "Transformer/Neural/Neural",改为 "hyperbolic-distance-weighted ridge" 或类似 — 1-2 天
- **B. 真实现 PyTorch 实现**:Poincaré ball embedding + hyperbolic distance attention — 1-2 周
- **推荐**: 选 B(保留方法论主张),若时间紧则选 A(保留信号,改名)

### 2.2 所有 6 个项目的 Related Work 都缺失或近空

**严重度**: 组合级共性问题(所有 6 项都被判 severity 3-4)
- p1: 空(2 行指针)
- p2: 近空(2 行)
- p3: 近空(1 行指针)
- p4: 空(desk-reject 触发)
- p5: 近空(1 行)
- p6: 不存在(只一行指针)
**修复**: 每个项目需要 2-3 页,覆盖 3-5 个文献分支(literature strands)。建议用 `/ARA compiler` 从已缓存的 67 篇 target-journal papers(在 `ara_collections/target_journal_related/`)批量抽取。
**预计工作量**: 每个项目 5-7 天,可并行写作

### 2.3 Sensitivity Analysis 普遍缺失

**严重度**: Energies 和 Applied Sciences 的"隐性强制项"(其缺失是 #1 major-revision trigger)
- p3: 完全无
- p4: 完全无
- p5: 完全无
- p2: 完全无
- p6: 部分
- p1: 完全无
**修复**: 每个项目需要 ±20% 参数敏感性分析(3-5 参数)。3-5 天/项目。

### 2.4 Baseline Degeneracy (p2 特有,但组合级警示)

p2 的 3 个命名 baseline 在所有 metric 上产出**完全相同预测到小数点后 8 位**,另外 2 对同样模式。去重后只有 ~5 个独立 baseline,全是 naive/ridge 级,**真实数据上零神经网络**。
**警示**: 检查其他 5 个项目是否也有类似的 baseline 退化问题(ablation 是否真正独立)。

### 2.5 Cross-Paper Collision (p5/p6)

**严重度**: 组合级 #1 威胁
- 共享 data pipeline / 120-candidate pool / 4 baselines / 重叠 scenarios / 近同构 PAPER.md 模板
- IEEE Access "not distinct from prior publication" 红线
- **投稿顺序冲突**(见下节解决)

---

## 3. p5/p6 投稿顺序裁决

两个 agent 意见相反:
- **p5 agent 主张**: p6 先 → p5 后(≥8-10 周),Applied Sciences 先投
- **p6 agent 主张**: p5 先(IEEE Access)→ p6 后(≥6 周,Applied Sciences)

**裁决:p6 先投,p5 后投,间隔 ≥8-10 周**。理由:

| 维度 | p6 优势 | p5 劣势 |
|---|---|---|
| 统计信号 | **44/48 Holm-significant,零失败**(6 项目中最强) | +1.23% vs AHP-TOPSIS(弱于 p6) |
| 工作量 | **7-10 天可投** | 6 周可投 |
| 外部 ground truth | 无(但 p6 有更强统计补偿) | **无**(是致命缺口) |
| 方法论风险 | **Backward search 是负贡献**(NoBackwardSearch 消融 +0.16%,需修复或诚实呈现)| 暂无 |

**投稿顺序**:
1. **p6 先投 → MDPI Applied Sciences**(7-10 天写完 + 15-16 天首决)
2. **p5 后投 → IEEE Access**(6 周写完,等 p6 接受后作为 benchmark 引用;跨出版社避免同 editor 碰撞;间隔 ≥8-10 周)

**关键前提**:
- p6 的 backward search 负贡献问题必须先修复(重设计算子或诚实呈现非对称性)
- p5 必须在 6 周内加上外部 ground truth(LBNL Queued Up 历史结果匹配)

---

## 4. 综合优先级时间线(按"快发优先"排序)

### P0(立即启动,2-4 周)

| 周 | p3 CARS-MODE | p6 BiLo-NSGA |
|---|---|---|
| W1 | 加 sensitivity + IEEE 33-bus + 文献综述 | 写 related work + 修 backward search |
| W2 | 重定位到约束修复故事(丢 strategy-adaptive) | 加真实案例 + 跨文差异化论证 |
| W3 | 润色 + 投稿 Applied Sci | 润色 + 投稿 Applied Sci |
| W4 | 等首决 | 等首决 |

### P1(4-8 周)

| 周 | p4 SHIELD-MOEA | p5 TRACE-MOEA(等 p6 接受后启动) |
|---|---|---|
| W1-2 | 写 related work + 修 Weighted Sum 重复 + 修随机种子 | (等待 p6 接受) |
| W3-4 | 30 重复 + sensitivity + unify metrics | 加外部 ground truth + 3D sensitivity |
| W5-6 | 润色 + 投稿 Energies | 写完整稿件 + related work |
| W7-8 | 等首决 | 投稿 Applied Sci(等 p6 接受后) |

### P2(8-12 周,诚信修复后)

| 周 | p2 HyG-LoadFormer |
|---|---|
| W1-2 | **PyTorch 实现** Poincaré + hyperbolic attention + 修 baseline 退化(加 LSTM/TCN/DLinear/PatchTST 在真实数据)|
| W3 | Sensitivity + Panama 数据集 |
| W4 | Related work + 标题/摘要限定 day-ahead 24h + 删 "Smart Dispatch" |
| W5 | 润色 + 投稿 Electronics |
| W6-10 | 等首决(Major Revision 预期)|

### P3(12+ 周,重大改造后)

| 周 | p1 DSTAR-GRU |
|---|---|
| W1 | Claim restructuring(lead with stress subset 0.72%/3.08%)|
| W2-3 | DC-OPF feasibility layer(PGLib/MATPOWER/pandapower 已缓存)|
| W4 | ≥10 seeds + ≥10 rolling windows + Wilcoxon |
| W5 | Sensitivity analysis + 投稿 Energies |

---

## 5. 投稿顺序总览(Gantt 风格)

```
W1-4   [p3][p6] ← P0 立即启动
W4-8   [p4][p5 准备中]
W8-12  [p2 诚信修复][p5 投稿]
W12-16 [p1 改造]
```

**预计产出(按时间)**:
- **W3**: p3 投稿 Applied Sciences
- **W4**: p6 投稿 Applied Sciences
- **W5**: p3 首决(Minor Revision 预期)
- **W6**: p6 首决(Minor Revision 预期)
- **W8**: p4 投稿 Energies
- **W10**: p5 投稿 Applied Sci(p6 已接受后引用)
- **W12**: p2 投稿 Electronics(诚信修复后)
- **W15**: p1 投稿 Energies(改造后)

---

## 6. 诚实边界(组合级)

- **p2**: 若不改名或不真实现,按现状投稿构成"夸大主张",对作者/实验室声誉风险组合级最高
- **p5/p6**: 同时投稿会被交叉检索,必须错开 ≥8-10 周 + 跨出版社
- **p4**: PCMP 不可行(scope desk-reject),只能走 Energies
- **p1**: 0.08% 增益处于噪声量级,必须重定位到 stress subset 才勉强可投
- **所有项目**: Related work 全缺失,投稿前必须补齐
- **所有项目**: Sensitivity analysis 全缺失(Energies/Applied Sci 隐性强制项)
- **Cloubic LLM 端点仍超时**:本轮评审基于离线结构化分析,非实时 LLM 跑测;真实 paper_reviews 跑测需等网络恢复

---

## 7. 下一轮(Round 3)建议

1. **立即执行**:
   - p2 改名或 PyTorch 实现(诚信优先)
   - p3/p6 启动 P0 修复
   - 用 `/ARA compiler` 从 67 篇 target-journal papers 批量抽取 related work 素材
2. **W3-4**: 等 p3/p6 首决,根据 reviewer 反馈调整 p4/p5
3. **W8-12**: 等 p2 诚信修复完成,重新评估投稿可行性
4. **W12+**: 等 Cloubic 网络恢复,对 p3/p6 的真实稿件跑一次真实 LLM paper_reviews 7 维评审,与本轮离线分析对比

---

## 8. 三 skill 协同总结

### ARA
- 6 个 mintou 项目 ARA 工程已就绪,可直接进入编译阶段(`/ARA 编译 papers/mintou/mintou_p*`)
- 锁定 evidence 链,避免后续迭代破坏稳定基线
- 在 CLAUDE.md 加 end-of-session capture,让每轮工作自动记录

### paper_reviews
- 本轮离线评审已完成 6 项全量分析,产出 6 份独立评审 + 1 份组合报告
- 等 Cloubic 恢复后,对 p3/p6 真实稿件跑真实 LLM 评审
- 用 `--recommend` CLI flag 在 run_review 时自动打印快发 OA 推荐

### Paper_CCF
- 15 期刊画像 + 选刊对照表已作为所有评审的校准锚点
- 后续可用 `/Paper_CCF` 动态查询其他 venue(如 PCMP 可行性 / CSEE JPES Q1 选项)
- p5/p6 顺序冲突已通过 Paper_CCF 的 distilled standards 裁决(p6 信号更强 + Applied Sci 容忍 proxy)
