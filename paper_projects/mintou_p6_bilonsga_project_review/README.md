# mintou_p6 — BiLo-NSGA 投稿评审工作目录

## 论文信息

- **标题**: BiLo-NSGA: Budget-Aware Project-Level Local Moves with Accepted-Move Logging for Power-Grid Portfolio Optimization
- **算法**: BiLo-NSGA — 在非支配排序框架中测试预算感知的项目级插入与原子替换，并记录已提交的局部移动和确定性修复事件；名称不扩展为“bidirectional”性能主张
- **当前目标期刊**: Applied Sciences (MDPI)；manifest 备选: IEEE Access
- **本次评估对象**: IEEE Access vs MDPI Energies 差距对比，及是否保留 Applied Sciences
- **当前状态**: P6 local-search evidence contract — 以标准 hypervolume、场景内比较和实际运行级事件日志为边界；不主张前向支配、依赖协同效应、审计完整性或推荐路径

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
- 同源姊妹工程 (p5): `mintou_p5_trace_moea_feasibility_review`（共享候选生成管线及公开 NERC/MTEP16 源资产；方法、场景、运行记录和分析按论文区分）
- 数据缓存清单: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。
