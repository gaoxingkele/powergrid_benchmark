# p1 DSTAR-GRU — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p1_dstar_gru_dispatch`
- **当前目标刊**: IEEE Access(主)/ MDPI Energies(次)
- **当前 RRI**: 30.4/100
- **当前预测**: IEEE Access Reject(0.85)/ MDPI Energies Major Revision(0.75)
- **Soundness 单维占总风险 56%**

## 当前状态

✅ 已有:
- PAPER.md + logic/ + evidence/(10 runs + 7 tables)+ src/code/(2 files)+ trace/
- ARA 工程完整,实验数据存在

❌ 缺失:
- **Related work**:238 B 占位符(与其他 5 项完全相同)
- **完整论文正文**:零行(只有 ARA manifest)
- **DC-OPF 可行性验证**:无(0.08% 主增益处于噪声量级,无 OPF/UC 证明)
- **统计稳健性**:无多 seed、无 rolling windows、无显著性检验
- **Sensitivity analysis**:无(Energies 隐性强制项)

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **Claim restructuring** | 3 | 1-2 天 | Lead with stress subset 增益 0.72%/3.08%;overall 降为 "competitive parity"(0.08% 不可主张) |
| 2 | **DC-OPF 可行性验证** | 4 | 5-7 天 | 用 PGLib/MATPOWER/pandapower(已缓存在 `data/public_datasets/`)验证 DSTAR-GRU 推荐的调度在 OPF 下可行 |
| 3 | **统计稳健性** | 4 | 3-5 天 | ≥10 seeds + ≥10 rolling windows + Wilcoxon 显著性检验 |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 4 | Sensitivity analysis | 3 | 2-3 天 |
| 5 | Related work 从 238 B 占位符写 2-3 页 | 3 | 3-5 天 |
| 6 | 完整论文正文(Intro/Method/Results/Discussion) | 3 | 5-7 天 |

### 🟢 P2(minor,可选但有益)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 7 | `src/code/` 扩充(当前仅 2 个入口文件) | 2 | 1 天 |
| 8 | `logic/problem.md`、`concepts.md`、`constraints.md` 扩充(均为占位符) | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Reject(IEEE Access)/ Major Revision(Energies)
- **P0 完成后**:Major Revision(Energies,接受概率上升)
- **P0 + P1 完成后**:Minor Revision(Energies,接受概率高)
- **最快路径**:**~18 天** 投 MDPI Energies(W1 修 claim + W2-3 跑 OPF + W4 写 related work + W5 润色 + 投稿)

## 组合级警示

- p1 是 6 项中**最慢**的投稿路径(18 天,其他 7-10 天到 4-6 周)
- 0.08% 主增益是组合级最弱信号,即便重定位到 stress subset,仍需要 OPF 验证才能过 Energies 底线
- **建议**:p1 放到最后投(在 p3/p6/p4/p2 之后),作为组合收官文

## 行动清单(按天)

| Day | 行动 |
|---|---|
| 1-2 | Claim restructuring:重写 PAPER.md + claims.md,lead with stress subset 0.72%/3.08% |
| 3-9 | DC-OPF 验证:用 PGLib/MATPOWER/pandapower 验证调度可行性(5-7 天) |
| 10-14 | 统计稳健性:≥10 seeds + ≥10 rolling windows + Wilcoxon(3-5 天) |
| 15-16 | Sensitivity analysis:±20% 参数(2 天) |
| 17-21 | Related work:从 67 篇 target-journal papers 抽取,写 2-3 页 |
| 22-28 | 完整稿件:Intro/Method/Results/Discussion(5-7 天) |
| 29-30 | 润色 + 投稿 MDPI Energies |

## 诚实边界

- 若 OPF 验证显示 DSTAR-GRU 推荐不可行,需彻底改造方法(可能转向 stress subset + 简化任务)
- 0.08% 主增益不可主张为"显著提升",只能称 "competitive parity with stress-subset advantage"
- Related work 必须诚实覆盖 GRU-for-dispatch 既有工作,避免选择性忽略
- 投稿前必须 disclosed limitation:仅 RTS-GMLC 单系统 + 3 windows + 噪声量级主增益

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p1_dstar_gru_dispatch/` — ARA 工程本体
