# mintou_p4 — SHIELD-MOEA 投稿评审工作目录

## 论文信息

- **标题**: Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty
- **算法**: SHIELD-MOEA（Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience）
- **任务**: DER / 负荷 / 停电场景不确定性下的配电网韧性规划（多目标进化优化）
- **目标期刊**: MDPI Energies（首选）
- **备选期刊**: IEEE Access

## 本文件夹用途

存放 mintou_p4 的期刊投稿评审产出，与 ARA 工程本体分离：

- `README.md` — 本说明文件
- `JOURNAL_REVIEW.md` — IEEE Access vs MDPI Energies 匹配度评审、写作/实验/数据集缺口分析与 P0/P1/P2 行动清单

## ARA 源工程路径

- ARA 根目录: `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p4_shield_resilience_planning\`
  - 论文主页: `PAPER.md`
  - 逻辑层: `logic\problem.md`, `logic\claims.md`, `logic\experiments.md`, `logic\related_work.md`, `logic\concepts.md`, `logic\solution\method.md`, `logic\solution\constraints.md`
  - 证据层: `evidence\README.md`, `evidence\runs\`（含 SimBench v2 结果与保留的 v1 弱结果）, `evidence\tables\`, `evidence\source\`
  - 环境: `src\environment.md`
- 组合上下文: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`
- 本地数据集缓存: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`

## 当前证据快照（2026-07）

SimBench 衍生韧性规划 v2 公共基准：SHIELD-MOEA 平均 hypervolume proxy `0.79432775`，领先最强 baseline MOEA/D `+2.78%`、最强 ablation NoScenarioScreen `+3.26%`；尚无 AC/pandapower 潮流可行性验证与场景方差/重复实验，为提交前必须补齐的边界（详见 `JOURNAL_REVIEW.md`）。


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。