# mintou_p2 — HyG-LoadFormer 投稿评审工作目录

## 论文信息

- **论文标题**: Hyperbolic Graph Neural Forecasting for Hierarchical Power Load Prediction in Smart Dispatch Systems
- **算法**: HyG-LoadFormer (Hyperbolic Graph Load Forecasting Transformer)
- **论文编号**: mintou_p2
- **当前目标期刊**: Electronics (MDPI)；备选 Applied Sciences (MDPI)
- **本次评估对象**: IEEE Access 与 MDPI Energies（对比是否改投）

## 本文件夹用途

存放 mintou_p2 的期刊投稿评审与修改完善方案，不存放实验代码或证据数据。

- `README.md` — 本说明文件
- `JOURNAL_REVIEW.md` — 期刊匹配度对比（IEEE Access vs Energies vs 现目标 Electronics）、写作修改清单、实验设计缺口、数据集缺口、P0/P1/P2 优先级行动清单

## ARA 工程源路径

- ARA 主目录: `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p2_hygraph_load_forecasting\`
  - 论文骨架: `PAPER.md`
  - 逻辑层: `logic\problem.md`、`logic\claims.md`、`logic\experiments.md`、`logic\related_work.md`、`logic\concepts.md`、`logic\solution\method.md`、`logic\solution\constraints.md`
  - 证据层: `evidence\README.md`、`evidence\runs\`（含 OPSD v1-v4、SimBench v1-v3 各版本分析及 rolling 分析）、`evidence\tables\`、`evidence\source\`
  - 环境与代码: `src\environment.md`、`src\code\`、`src\configs\`
- 组合状态: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`
- 本地数据集缓存: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`；负荷预测基准数据 `data\public_datasets\time_series_market\load_forecasting_benchmarks\`

## 关键结论速览

24h/day-ahead 是本文唯一可作主张的强信号（OPSD 固定切分 MAPE 0.0397 vs 最强基线 0.0563，rolling +39.16%）；1h 短时预测在 OPSD/SimBench 上均为记录在案的 limitation，投稿主张必须限定为 day-ahead 层级负荷预测。详见 `JOURNAL_REVIEW.md`。


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。