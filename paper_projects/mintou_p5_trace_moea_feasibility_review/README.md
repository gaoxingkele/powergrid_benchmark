# mintou_p5 — TRACE-MOEA 投稿评审工作目录

## 论文

- **标题**: Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization
- **算法**: TRACE-MOEA (Traceable Review-Aware Coevolutionary Multi-Objective Evolution)
- **任务**: 可追溯电网项目可行性评审与投资有效性多目标优化
- **目标期刊**: IEEE Access（主投）；MDPI Energies（备选）
- **当前状态**: `project_original_public_benchmark_v1`，公开基准代理信号（+1.23% vs AHP-TOPSIS，+3.71% vs 最强消融）

## 本文件夹用途

存放 mintou_p5 的期刊投稿评估产物（独立于 ARA 工程本体，不写入 ARA evidence/ 链）：

| 文件 | 内容 |
|---|---|
| `README.md` | 本说明 |
| `JOURNAL_REVIEW.md` | IEEE Access vs MDPI Energies 双刊差距评估、修改完善方案与 P0/P1/P2 行动清单（中文） |

## ARA 源路径

- ARA 工程根目录: `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p5_trace_moea_feasibility_review\`
  - 论文主页: `PAPER.md`
  - 逻辑链: `logic\problem.md`、`logic\claims.md`、`logic\experiments.md`、`logic\solution\method.md`、`logic\solution\constraints.md`
  - 证据链: `evidence\README.md`、`evidence\runs\`（含 v1/v2 weak、v3 near-miss、最终 analysis）、`evidence\tables\real_project_review_leaderboard.csv`
  - 实验代码入口: `src\code\run_real_project_review.py` → 主模块 `D:\aicoding\powergrid_benchmark\src\powergrid_benchmark\mintou_real_project_review.py`
- 组合状态: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`
- 数据缓存: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`（rts_gmlc / simbench / c2ges_nerc_reports 均已本地缓存）


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。