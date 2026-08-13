# mintou_p4 — SHIELD-MOEA 投稿评审工作目录

## 论文信息

- **标题**: SHIELD-MOEA: Scenario Screening with Disjoint Evaluation for Distribution-Network Resilience Planning
- **算法**: SHIELD-MOEA（Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience）
- **任务**: 负荷 / 停电代理场景下的配电网韧性规划（多目标进化优化），并以独立 AC 组合测试覆盖 DER 运行工况
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

## 当前证据快照（2026-08）

当前稿件使用 2640 条主档案记录（每个随机方法在 8 个实验标签下各 30 次调用）和 1296 个组合级 AC 案例。SHIELD-MOEA 的汇总平均标准 hypervolume 为 `0.27396193`，相对仅在最终种群执行事后修复的 NSGA-II 为 `+5.09%`，相对 plain NSGA-II 为 `+5.56%`。八个实验标签只对应五种实际生效的 p4 代理配置；配置中的 DER 输出乘数不进入 p4 的五个优化/评分目标，因此 `der_uncertainty` 不能作为 DER 输出不确定性证据。完整边界见 `manuscript/DEEP_REVISION_EVIDENCE.md` 和 `manuscript/EQUATION_IMPLEMENTATION_CONTRACT.md`。

阶段 `p4_s3_boundary_experiments` 另增 1050 条预声明、不可覆盖的边界运行（7 个预算/场景数/生存性系数设置 × 5 个方法 × 30 个种子）。在主评分定义下，SHIELD-MOEA 相对 NSGA-II+Repair 的组内均值差在七个设置中均为正（`+3.46%` 至 `+7.20%`）；但 1050 个前沿中有 441 个触发低侧裁剪，且裁剪会改变差值幅度。替代参考点 `1.2^5` 与不裁剪审计均未改变各组比较方向。新运行、边界表和哈希清单位于本工作树的 `evidence/`，预声明配置和本地运行器位于 `experiments/`。这些补充运行不替代历史主档案，也不改变 p3 声明。

阶段 `p4_s4_results_narrative` 未新增或重跑实验。`evidence/manifests/p4_s4_results_artifact_manifest_20260813.json` 对当前规划、推断、机制控制、敏感性、AC 与边界证据进行哈希固定，`manuscript/figures/build_results_artifacts.ps1` 据此重建四张主结果图与四张派生表。结果叙事先报告代理质量，再报告修复机制，最后把筛选的 65% 静态目标行缩减与 8/8 标签均未检出质量差异、未做等效检验及无墙钟节省同时呈现。四个同范围标签被明确标为独立优化器种子块，而非四个独立不确定性机制；AC 结果仅为固定组成映射下的说明性/关联性检查。

`manuscript/MANUSCRIPT.md` 是唯一规范稿源；`manuscript/journal_submission/` 是由规范稿生成的当前投稿工件目录。`manuscript/submission_preview/` 是本阶段之前生成的旧预览，不应作为当前科学主张的来源。构建状态与不可用依赖见 `manuscript/ARTIFACT_STATUS.md`。


## Round 2 评审产出 (2026-07-14)

本项目已完成 paper_reviews 7 维离线评审,分析结果已写入本目录:

| 文件 | 内容 |
|---|---|
| `ROUND2_REVIEW.md` | 完整 7 维评审(novelty/soundness/experiments/reproducibility/related_work/clarity/ethics),含 RRI、预测决策、允许修改范围、最快路径 |
| `GAP_ANALYSIS_ROUND2.md` | 每项目缺啥清单(P0/P1/P2 优先级 + 工作量估算 + 投稿可行性 + 行动清单 + 诚实边界 + 关联文件) |

组合级报告见 `D:\aicoding\powergrid_benchmark\reviews\2026-07-13_round2_mintou_summary.md`(6 项目对比 + 投稿顺序裁决 + 综合时间线)。
