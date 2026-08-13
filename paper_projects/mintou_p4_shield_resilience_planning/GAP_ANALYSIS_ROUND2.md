# p4 SHIELD-MOEA — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p4_shield_resilience_planning`
- **当前目标刊**: MDPI Energies(主)/ PCMP 不可行(次)
- **当前 RRI**: 2.22/4.00
- **当前预测**: Reject / Major Revision
- **修复后预测**: Minor-to-Major Revision,高接受概率

## 当前状态

✅ 已有:
- PAPER.md + logic/ + evidence/(12 runs + 8 tables)+ src/code/(2 files)+ trace/
- SimBench 衍生韧性规划 v2 公共基准,hypervolume proxy 0.79432775
- 领先最强 baseline MOEA/D +2.78%、最强 ablation NoScenarioScreen +3.26%

❌ 缺失 + 🚨 方法论问题:
- **Related work**:238 B 占位符(desk-reject 触发)
- **🚨 Weighted Sum ≡ Deterministic Planning 重复**:所有实验 bit-identical(severity 4)
- **随机种子问题**:当前 3 次重复近乎相同,需 30 次独立重复
- **Sensitivity analysis**:无(Energies 隐性强制)
- **Metric 命名不统一 + hypervolume proxy 未形式化定义**
- **完整论文正文**:零行

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **Related work 从零写** | 4 | 5-7 天 | 当前 238 B 占位符 = desk-reject 触发 |
| 2 | **Fix Weighted Sum ≡ Deterministic Planning 重复** | 4 | 3-5 天 | 所有实验 bit-identical,严重方法论 bug |
| 3 | **Fix random seeds + 跑 30 次独立重复** | 3 | 2-3 天 | 当前 3 次近乎相同,统计功效不足 |
| 4 | **Sensitivity analysis** | 3 | 3-5 天 | Energies #1 major-revision trigger,近强制 |
| 5 | **Unify metric 命名 + 形式化定义 hypervolume proxy** | 2 | 1-2 天 | 当前命名混乱,proxy 未定义 |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 6 | 完整论文正文 | 3 | 5-7 天 |
| 7 | `logic/` 占位符文件扩充 | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Reject / Major Revision(5 个 blocking issues)
- **P0 完成后(~7-10 天)**:Minor-to-Major Revision,高接受概率
- **总路径**:**~6-8 周** 到 MDPI Energies 发表

## PCMP 可行性分析

- **❌ PCMP 不可行**(scope desk-reject)
- 论文是"规划优化"问题,不是"保护/控制/故障/稳定"问题
- 要拉 PCMP 角度需要改下游任务(改成保护继电调参或自愈控制),违反"大方向不变"约束
- 详细可行性分析见 `ROUND2_REVIEW.md` 的 PCMP 章节

## 行动清单(按天)

| Day | 行动 |
|---|---|
| 1-7 | Related work 从零写(5-7 天,从 67 篇 target-journal papers 抽取) |
| 1-5 | Fix Weighted Sum ≡ Deterministic Planning 重复(并行) |
| 6-8 | Fix random seeds + 跑 30 次独立重复 |
| 9-13 | Sensitivity analysis(3-5 天) |
| 14-15 | Unify metric 命名 + 形式化定义 hypervolume proxy |
| 16-22 | 完整论文正文 |
| 23-30 | 润色 + 投稿 MDPI Energies |

## 组合级定位

- p4 是组合级 **P1**(W4-8)启动的论文(在 p3/p6 之后)
- 投稿时间:W1 启动 P0 → W4-5 投稿 → W8 首决
- 与 p1/p2/p3/p5/p6 无跨文碰撞风险

## 诚实边界

- Weighted Sum ≡ Deterministic Planning 重复必须修复或诚实披露为"当前实现的已知问题"
- 30 次重复必须真实独立(不同 seed,不同硬件时间戳)
- PCMP 角度不可强行拉(会被 desk-reject)
- Sensitivity analysis 必须真做(不能只写"future work")

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录,含 PCMP 可行性分析)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p4_shield_resilience_planning/` — ARA 工程本体
