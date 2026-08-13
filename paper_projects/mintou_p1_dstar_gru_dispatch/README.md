# mintou_p1_dstar_gru_dispatch — 投稿评审工作目录

- **论文标题**: A Reproducible Retrospective Curtailment-Risk Benchmark and Fair Evaluation of GRU Learned-Space Retrieval on RTS-GMLC
- **论文方法名**: GRU-LSR (GRU learned-space retrieval); `DSTAR-GRU` 仅保留为冻结实验表中的历史标识
- **任务边界**: 基于 RTS-GMLC 8784 行源文件的前 8760 个交付时刻（清单终点为 12 月 30 日）进行 1 h/24 h 回溯滞后预测；现有资产没有预测发布时间或数据版本字段，因此不主张完整日历年、运营日前预测、调度或数字孪生能力
- **目标期刊**: IEEE Access（备选: Electronics；本目录同时评估 MDPI Energies）
- **本文件夹用途**: 存放该论文面向期刊投稿的评审与修改完善方案（`JOURNAL_REVIEW.md`），基于 ARA 工程证据对照期刊画像产出差距分析与优先级行动清单。
- **ARA 源路径**: `papers/mintou/mintou_p1_dstar_gru_dispatch`（PAPER.md、logic/、evidence/、src/）

## 文件

| 文件 | 内容 |
|---|---|
| `README.md` | 本说明 |
| `JOURNAL_REVIEW.md` | IEEE Access vs MDPI Energies 匹配度对比、写作修改清单、实验设计缺口、数据集缺口、P0/P1/P2 行动清单 |
| `manuscript/MANUSCRIPT.md` | 以研究问题组织、由公平运行结果支撑的正文 |
| `manuscript/TABLE_TO_CONFIG_MANIFEST.md` | 正文表格和图片到公平运行清单与冻结输出的映射 |
| `manuscript/DEEP_REVISION_EVIDENCE.md` | 标题、估计量、比较预算、负结果与未解决人工占位符的证据契约 |
| `manuscript/P1_S5_THREE_ROUND_CLOSURE.md` | 顺序逻辑、方法统计与理论创新对抗审查的闭环记录及未验证项 |
| `manuscript/SUPPLEMENTARY_METHODS_AND_AUDIT.md` | 运行环境、版本历史、复现核查与详尽审计记录 |
| `experiments/p1_s3_fair_v1/run_manifest.json` | 当前正文结果的冻结运行清单与输出哈希 |


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。
