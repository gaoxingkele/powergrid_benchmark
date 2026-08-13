# mintou_p3 — CARS-MODE 投稿评审工作目录

## 论文信息

- **论文标题**: Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration
- **算法**: CARS-MODE (Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution) — 约束感知修复 + 策略自适应多目标差分进化
- **任务**: 配电网扩展规划、DER 选址定容、储能配置的多目标优化
- **目标期刊**: MDPI Energies（首选）；MDPI Applied Sciences（备选）；本目录同时评估 IEEE Access 的可行性
- **当前证据状态**: SimBench DER/storage stress v5 公共基准，proxy hypervolume 0.55322842，超最强基线 NSGA-II 0.46%、超最强消融 FixedDE 0.19%；narrow_promising_public_signal

## 本文件夹用途

投稿前评审与修改规划工作目录，不存放论文源码或实验数据：

- `README.md` — 本文件，工程索引
- `JOURNAL_REVIEW.md` — IEEE Access vs MDPI Energies 双刊差距评估与修改完善方案（中文）

## ARA 源工程路径

论文的 Agent-Native Research Artifact 工程位于：

```
D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p3_samode_distribution_planning\
├── PAPER.md                        # 论文元信息与当前状态
├── logic\                          # problem / claims / experiments / related_work / concepts / solution
├── evidence\
│   ├── runs\                       # v1-v3 weak、v4 near-miss、v5 最终分析（负面证据保留）
│   ├── tables\                     # 各版本 leaderboard CSV
│   └── source\                     # SimBench 源数据画像
├── src\                            # 实验代码、配置、环境说明
└── trace\exploration_tree.yaml
```

相关上下文：

- 组合状态: `D:\aicoding\powergrid_benchmark\papers\mintou\portfolio_status.md`
- 数据缓存: `D:\aicoding\powergrid_benchmark\data\public_datasets\CACHE_STATUS.md`


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。