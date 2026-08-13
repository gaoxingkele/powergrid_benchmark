# mintou_p3 — CARS-MODE 投稿评审工作目录

## 论文信息

- **论文标题**: CARS-MODE: Constraint-Aware Repair and Strategy-Pool Multi-Objective Differential Evolution on a SimBench-Derived Mixed-Voltage Portfolio Proxy
- **算法**: CARS-MODE (Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution) — 约束感知修复 + 策略自适应多目标差分进化
- **任务**: SimBench 衍生的混合电压等级配电规划组合代理上的多目标优化；不是动作对齐的配电网扩展研究
- **目标期刊**: MDPI Energies（首选）；MDPI Applied Sciences（备选）；本目录同时评估 IEEE Access 的可行性
- **当前证据状态**: 2940 次精确复现覆盖 6 个独立配置和 1 个 base 配置内部重复。按 6 个配置等权汇总，sampled-bound/clipped hypervolume 为 CARS-MODE 0.04240、NSGA-II+Repair 0.03998（+6.06%）；但审计发现 2281 个低于下界而被裁剪的坐标。采用不裁剪的解析可行边界与参考点 1.05 后，CARS-MODE 为 0.00043464、NSGA-II+Repair 为 0.00043530，CARS-MODE 排名第 4；common-reference IGD+ 排名第 5。FixedDE 在三个配置等权指标上均保持名义优势，适应机制未解决。AC 层仅为归档 seed-0 组合诊断，不具备多种子或层级不确定性；其工程价值是筛选与暴露 proxy--physics 分歧，而不是物理可行性认证。

## 本文件夹用途

投稿前评审、验证与修改工作目录。P3 S3 新验证证据保存在 `evidence/runs/p3_s3_planning_validation_20260813/`：

- `README.md` — 本文件，工程索引
- `JOURNAL_REVIEW.md` — IEEE Access vs MDPI Energies 双刊差距评估与修改完善方案（中文）
- `manuscript/` — 与新参考点/裁剪审计对齐的论文、深度修订证据合同及派生表
- `scripts/` — 只读调用共享 P3 规划实现的精确复现与诊断脚本，以及从 `evidence/runs/p3_s4_results_narrative_20260813/manifest.json` 统一生成结果表图的脚本；未改写共享 P3/P4 代码

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
