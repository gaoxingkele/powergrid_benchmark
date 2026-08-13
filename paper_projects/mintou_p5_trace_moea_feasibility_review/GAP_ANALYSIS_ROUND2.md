# p5 TRACE-MOEA — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p5_trace_moea_feasibility_review`
- **当前目标刊**: MDPI Applied Sciences(主,修订)/ IEEE Access(次,修订)
- **当前 RRI**: 1.73/4.00
- **当前预测**: Major Revision
- **⚠️ 与 p6 同源姊妹工程,跨文碰撞风险组合级 #1**

## 当前状态

✅ 已有:
- PAPER.md + logic/ + evidence/(12 runs + 7 tables)+ src/code/(2 files)+ trace/
- 公开基准代理信号:+1.23% vs AHP-TOPSIS、+3.71% vs 最强消融
- ARA 工程完整

❌ 缺失 + 🚨 跨文碰撞:
- **🚨 与 p6(BiLo-NSGA)跨文碰撞**:共享 data pipeline / 120-candidate pool / 4 baselines / 重叠 scenarios / 近同构 PAPER.md 模板 —— IEEE Access "not distinct from prior publication" 红线
- **🚨 无外部 ground truth**:无专家标签、无历史结果、无校准成本,"feasibility review" 主张全靠 proxy 目标
- **Related work**:238 B 占位符(与其他 5 项完全相同)
- **Sensitivity analysis**:无
- **完整论文正文**:零行

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **🚨 外部 ground truth 锚定** | 4 | ~2 周 | LBNL Queued Up 历史结果匹配;否则 "feasibility review" 主张全靠 proxy,无法立足 |
| 2 | **🚨 跨文差异化论证(vs p6)** | 3 | 2-3 天 | 必须显式对比 p6,解释本文独特贡献 |
| 3 | **Related work 从 1 行占位符写 2-3 页** | 4 | 5-7 天 | |
| 4 | **三维 sensitivity(budget/weight/pool)** | 3 | 1-2 周 | Applied Sciences 隐性强制项 |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 5 | 完整稿件:Intro/Method/Results/Discussion + 编号贡献 + limitations + beneficiary 句 | 3 | 3-4 周 |
| 6 | `logic/` 占位符文件扩充 | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Major Revision
- **P0 完成后**:Minor Revision 概率上升
- **P0 + P1 完成后**:Accept 概率高
- **最快路径**:**~6 周** 投 MDPI Applied Sciences

## 投稿顺序裁决(组合级)

### ❗ 与 p6 投稿顺序裁决

两个 Round 2 agent 意见相反:
- p5 agent 主张:p6 先 → p5 后(≥8-10 周),Applied Sciences 先投
- p6 agent 主张:p5 先(IEEE Access)→ p6 后(≥6 周,Applied Sciences)

**组合级裁决**:**p6 先投,p5 后投,间隔 ≥8-10 周**。理由:
- p6 统计信号更强(44/48 Holm-significant,6 项中最强)
- p6 工作量更短(7-10 天 vs 6 周)
- p6 先投 Applied Sciences 建立 benchmark;p5 后成 "traceability extension"
- 跨出版社分离(p6 MDPI Applied Sciences → p5 IEEE Access 或 MDPI 后投)避免同 editor 碰撞

**关键前提**:
- p6 的 backward search 负贡献问题必须先修复
- p5 必须加外部 ground truth(LBNL Queued Up)

### 投稿时间线

| 周 | 行动 |
|---|---|
| W1-2 | 等 p6 完成 P0 并投稿 |
| W3-8 | 等 p6 接受 + 同时做 p5 P0 修复 |
| W8-10 | 等 p6 接受后,启动 p5 投稿 |
| W10 | 投稿 MDPI Applied Sciences(或 IEEE Access) |

## 行动清单(按周,等 p6 接受后启动)

| Week | 行动 |
|---|---|
| W1-2 | 外部 ground truth 锚定(LBNL Queued Up 历史结果匹配) |
| W2-3 | 三维 sensitivity(budget/weight/pool) |
| W3-4 | Related work(5-7 天)+ 跨文差异化论证(2-3 天) |
| W4-7 | 完整稿件 + 编号贡献 + limitations + beneficiary 句 |
| W8 | 润色 + 投稿(等 p6 接受后) |

## 组合级定位

- p5 是组合级 **P1**(W4-8)启动,但**实际投稿在 p6 接受后**(W8-10)
- 与 p6 同源姊妹工程,必须错开 ≥8-10 周
- 与 p1/p2/p3/p4 无跨文碰撞风险

## 诚实边界

- "Feasibility review" 主张必须有外部 ground truth 支撑,否则是虚假主张
- 与 p6 的差异必须在 Introduction 显式对比,不能假装独立
- Related work 必须诚实覆盖 MOEA-for-project-review 既有工作
- 若 LBNL Queued Up 不可用,需另寻 ground truth 锚点,否则投稿不可行

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p5_trace_moea_feasibility_review/` — ARA 工程本体
- **姊妹工程**:`D:\aicoding\powergrid_benchmark\mintou_p6_bilonsga_project_review\`
