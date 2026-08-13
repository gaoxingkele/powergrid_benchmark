# mintou_p2 — CSA-LoadNet 投稿评审工作目录

## 论文信息

- **论文标题**: Cross-Series Context for 24-Step-Ahead Point Forecasting of Multi-Region Power Load: A Matched Rolling-Origin Component Evaluation
- **算法**: CSA-LoadNet
- **论文编号**: mintou_p2
- **当前目标期刊**: Electronics (MDPI)；备选 Applied Sciences (MDPI)
- **本次评估对象**: IEEE Access 与 MDPI Energies（对比是否改投）

## 本文件夹用途

存放 mintou_p2 的期刊投稿评审与修改完善方案，不存放实验代码或证据数据。

- `README.md` — 本说明文件
- `JOURNAL_REVIEW.md` — 期刊匹配度对比（IEEE Access vs Energies vs 现目标 Electronics）、写作修改清单、实验设计缺口、数据集缺口、P0/P1/P2 优先级行动清单
- `manuscript/DEEP_REVISION_EVIDENCE.md` — 当前标题、任务、组件、指标、负面结果及人工阻塞项的证据合同

## ARA 工程源路径

- ARA 主目录: `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p2_hygraph_load_forecasting\`
  - 论文骨架: `PAPER.md`
  - 逻辑层: `logic\problem.md`、`logic\claims.md`、`logic\experiments.md`、`logic\related_work.md`、`logic\concepts.md`、`logic\solution\method.md`、`logic\solution\constraints.md`
  - 证据层: `evidence\README.md`、`evidence\runs\`（含 OPSD v1-v4、SimBench v1-v3 各版本分析及 rolling 分析）、`evidence\tables\`、`evidence\source\`
  - 环境与代码: `src\environment.md`、`src\code\`、`src\configs\`
- 组合状态: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`
- 本地数据集缓存: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`；负荷预测基准数据 `data\public_datasets\time_series_market\load_forecasting_benchmarks\`

## 关键结论速览

OPSD lead-24 的主比较采用八个季度 rolling origins、每 origin 五个共同 seeds，并以 origin 为外层分析单位。29,815 参数且 head/优化/执行路径匹配的 target-self control 与 CSA-Poincaré-Shared 未分离（MAPE Holm p=0.984；WAPE raw p=0.227），因此固定切分中对较小 head TemporalOnly 的正面归因不支持“aggregation helps”主张。uniform、Euclidean 与 learned-scale 权重未建立优势；fixed-scale 呈不利名义趋势。shared-vs-independent control 虽有差异，但独立 encoder 改变 hidden width 与计算量，不能归因为 sharing。OPSD lead 1、SimBench、精确 Ausgrid、缺行后的 24-position 时间语义及其他限制见 `manuscript/DEEP_REVISION_EVIDENCE.md`。


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。
