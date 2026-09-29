# p3 CARS-MODE — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p3_samode_distribution_planning`
- **当前目标刊**: MDPI Energies(主)/ MDPI Applied Sciences(次)
- **当前 RRI**: 11.75/28 (42%)
- **当前预测**: Major Revision 60% / Desk-Reject 25% / Minor Revision 15%

## 当前状态

✅ 已有:
- PAPER.md + logic/ + evidence/(18 runs + 11 tables)+ src/code/(2 files)+ trace/
- SimBench DER/storage stress v5 公共基准,hypervolume 0.55322842,超最强基线 NSGA-II 0.46%
- 约束修复故事强证据:违反率 21.5% → 7.0%

❌ 缺失:
- **Related work**:238 B 占位符(与其他 5 项完全相同)
- **Sensitivity analysis**:完全无(Energies #1 major-revision trigger)
- **IEEE 33-bus 标准测试系统**:只用非标准 SimBench
- **完整论文正文**:零行
- **经济量化**(IRR/回收年限,Applied Sciences 隐性必需):无

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **Sensitivity analysis** | 4 | 3-5 天 | Energies #1 major-revision trigger,近强制 |
| 2 | **Literature review** | 4 | 5-7 天 | 从 1 行占位符写 30+ 论文跨 5 子主题(否则 desk-reject 触发) |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 3 | IEEE 33-bus 标准测试系统(pandapower 内置,零下载) | 3 | 2-3 天 |
| 4 | 完整论文正文 | 3 | 5-7 天 |
| 5 | 受益者命名句("grid planners can use…",Applied Sciences 必需) | 2 | 0.5 天 |

### 🟢 P2(可选,影响刊物选择)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 6 | 重定位到约束修复故事(丢弱证据的 strategy-adaptive 组件) | 2 | 2-3 天 |
| 7 | 经济量化(IRR/回收年限,Applied Sciences 隐性必需) | 2 | 2-3 天 |
| 8 | `logic/` 占位符文件扩充 | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Major Revision 60% / Desk-Reject 25% / Minor Revision 15%
- **P0 完成后**:Minor Revision 概率上升
- **P0 + P1 完成后**:Accept 概率高
- **最快路径**:
  - **Path B**(简化重定位 + MDPI Applied Sciences,~3-4 周):丢 strategy-adaptive,围绕约束修复故事
  - **Path C**(激进简化 + MDPI Energies,~3 周)

## 行动清单(按天)

| Day | 行动 |
|---|---|
| 1-5 | Sensitivity analysis(3-5 天) |
| 6-8 | IEEE 33-bus 标准测试系统(2-3 天) |
| 9-15 | Literature review:从 67 篇 target-journal papers 抽取,写 30+ 论文跨 5 子主题(5-7 天) |
| 16-17 | 重定位到约束修复故事(2 天) |
| 18-24 | 完整稿件:Intro/Method/Results/Discussion + 受益者命名句(5-7 天) |
| 25-28 | 润色 + 投稿 MDPI Applied Sciences(Path B)或 Energies(Path C) |

## 组合级定位

- p3 是组合级 **P0 立即启动**的论文之一(与 p6 并列最快)
- 投稿时间:W1 启动 → W3 投稿 → W5 首决(Minor Revision 预期)
- 与 p4/p5/p1 无跨文碰撞风险

## 诚实边界

- Strategy-adaptive 组件只有 0.19% 证据支持,重定位时需诚实披露为"探索性附加"或直接丢
- 0.46% 增益不可主张为"显著提升",需 sensitivity 支持
- Related work 必须诚实覆盖 MOEA-for-distribution-planning 既有工作
- 经济量化若不做,只能投 Energies(不能投 Applied Sciences)

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p3_samode_distribution_planning/` — ARA 工程本体
