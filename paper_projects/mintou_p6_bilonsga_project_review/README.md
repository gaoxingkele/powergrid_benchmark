# mintou_p6 — BiLo-NSGA 投稿评审工作目录

## 论文信息

- **标题**: Non-Dominated Sorting with Bidirectional Local Search for Budget-Constrained Power Grid Project Review
- **算法**: BiLo-NSGA (Bidirectional Local-search Non-dominated Sorting Genetic Algorithm) — 带前向/后向局部搜索的非支配排序遗传算法，面向预算约束电网项目评审与组合排序
- **当前目标期刊**: Applied Sciences (MDPI)；manifest 备选: IEEE Access
- **本次评估对象**: IEEE Access vs MDPI Energies 差距对比，及是否保留 Applied Sciences
- **当前状态**: `project_original_public_benchmark_v1` — 公共基准派生实验 v3，BiLo-NSGA 超最强基线 AHP-TOPSIS 3.87%、超最强消融 3.57%（hypervolume proxy）

## 本文件夹用途

投稿评审顾问工作产出目录，不属于 ARA 工程本体：

- `README.md` — 本说明
- `JOURNAL_REVIEW.md` — 期刊匹配度对比（IEEE Access vs Energies vs Applied Sciences）、写作修改清单、实验/数据缺口、与 p5 差异化风险评估、优先级行动清单

## ARA 源路径

- ARA 工程根目录: `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p6_bilonsga_project_review\`
  - 论文骨架: `PAPER.md`
  - 逻辑层: `logic\problem.md`、`logic\claims.md`、`logic\experiments.md`、`logic\related_work.md`、`logic\concepts.md`、`logic\solution\method.md`、`logic\solution\constraints.md`
  - 证据层: `evidence\README.md`、`evidence\runs\`（含 v1/v2 弱信号保留版）、`evidence\tables\`、`evidence\source\`
  - 代码/配置: `src\code\run_real_project_review.py`、`src\configs\real_project_review_config.json`、`src\environment.md`
  - 探索轨迹: `trace\exploration_tree.yaml`
- 组合上下文: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`、`papers\mintou\manifest.csv`
- 同源姊妹工程 (p5): `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p5_trace_moea_feasibility_review\`
- 数据缓存清单: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。