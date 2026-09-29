# p6 BiLo-NSGA — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p6_bilonsga_project_review`
- **当前目标刊**: MDPI Applied Sciences(主)/ IEEE Access(次)
- **当前 RRI**: 2.491(中等偏高残留风险)
- **当前预测**: Major Revision → P0/P1 修复后 Accept with Minor Revision
- **🏆 6 项中统计信号最强**(44/48 Holm-significant,零失败)
- **⚠️ 与 p5 同源姊妹工程,跨文碰撞风险组合级 #1**

## 当前状态

✅ 已有(强证据):
- PAPER.md + logic/ + evidence/(10 runs + 6 tables)+ src/code/(2 files)+ trace/
- **6 项中最强统计信号**:44/48 Holm-significant,零失败
- +3.87% vs AHP-TOPSIS、+3.57% vs 最强消融(hypervolume proxy)
- ARA 工程完整

❌ 缺失 + 🚨 方法论问题:
- **Related work**:1 行占位符(只一行指针)
- **🚨 Backward search 是负贡献者**:NoBackwardSearch 消融 beats 完整方法 +0.16%(需要重设计算子或诚实呈现非对称性)
- **无外部 ground truth**:proxy benchmark,无专家标签、无成本校准、无潮流检查
- **完整论文正文**:零行
- **跨文差异化论证**(vs p5):无

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **Related work 从零写** | 4 | 5-7 天 | 当前只有 1 行指针,需要 2-3 页覆盖 3 个文献 strands |
| 2 | **🚨 Fix backward search 负贡献** | 3 | 3-5 天 | NoBackwardSearch 消融 beats 完整方法 +0.16%;要么重设计算子,要么诚实呈现非对称性 |
| 3 | **跨文差异化论证(vs p5)** | 3 | 2-3 天 | 显式对比 p5,解释本文独特贡献 |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 4 | 真实案例(当前只有 proxy benchmark) | 2 | 3-5 天 |
| 5 | 完整论文正文 + 受益者命名句("grid planners can use…") | 3 | 5-7 天 |
| 6 | `logic/` 占位符文件扩充 | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Major Revision
- **P0 完成后**:Minor Revision 概率上升
- **P0 + P1 完成后**:Accept with Minor Revision 概率高
- **最快路径**:**7-10 天** 写出可投稿稿件(5-7 天写作 + 2-3 天可视化证据,可并行)
- **投稿后**:**~15-16 天** Applied Sciences 首决

## 投稿顺序裁决(组合级)

### ❗ 与 p5 投稿顺序裁决

两个 Round 2 agent 意见相反:
- p5 agent 主张:p6 先 → p5 后(≥8-10 周)
- p6 agent 主张:p5 先(IEEE Access)→ p6 后(≥6 周,Applied Sciences)

**组合级裁决**:**p6 先投,p5 后投,间隔 ≥8-10 周**。理由:
- p6 统计信号更强(44/48 Holm-significant,6 项中最强)
- p6 工作量更短(7-10 天 vs 6 周)
- p6 先投 Applied Sciences 建立 benchmark;p5 后成 "traceability extension"
- 跨出版社分离(p6 MDPI Applied Sciences → p5 IEEE Access 后投)避免同 editor 碰撞

**关键前提**:
- **p6 的 backward search 负贡献问题必须先修复**(NoBackwardSearch beats 完整方法 +0.16%)
- 这是 p6 投稿的硬前提,不修不能投

### 投稿时间线

| 周 | 行动 |
|---|---|
| **W1** | 立即启动 p6 P0 修复 |
| **W1-2** | Related work 从零写 + fix backward search + 跨文差异化论证(7-10 天) |
| **W2-3** | 加真实案例 + 完整论文正文(3-5 天) |
| **W3-4** | 润色 + 投稿 MDPI Applied Sciences |
| **W4-5** | 等首决(预期 Minor Revision) |

## 行动清单(按天,立即启动)

| Day | 行动 |
|---|---|
| 1-7 | Related work 从零写(5-7 天,从 67 篇 target-journal papers 抽取) |
| 1-5 | Fix backward search 负贡献(并行,3-5 天) |
| 6-8 | 跨文差异化论证(vs p5,2-3 天) |
| 9-13 | 真实案例(3-5 天) |
| 9-15 | 完整论文正文 + 受益者命名句(5-7 天,与真实案例并行) |
| 16-17 | 润色 + 投稿 MDPI Applied Sciences |

## 组合级定位

- p6 是组合级 **P0 立即启动**的论文之一(与 p3 并列最快)
- **先投** p6,为 p5 建立 benchmark 基础
- 投稿时间:W1 启动 → W3-4 投稿 → W5-6 首决(Minor Revision 预期)
- p5 接受 p6 后 8-10 周再投稿

## 诚实边界

- Backward search 负贡献必须修复或诚实披露为"算子的已知非对称行为"
- 与 p5 的差异必须在 Introduction 显式对比,不能假装独立
- Related work 必须诚实覆盖 NSGA-for-project-review 既有工作
- Proxy benchmark 无外部 ground truth,需在 limitations 中诚实披露
- 投稿前必须 disclosed limitation:无专家标签、无成本校准、无潮流检查

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p6_bilonsga_project_review/` — ARA 工程本体
- **姊妹工程**:`D:\aicoding\powergrid_benchmark\mintou_p5_trace_moea_feasibility_review\`
