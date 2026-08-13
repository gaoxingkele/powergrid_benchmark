# p2 HyG-LoadFormer — Round 2 Gap Analysis

- **日期**: 2026-07-14
- **评审来源**: `ROUND2_REVIEW.md`(paper_reviews 7 维离线评审)
- **ARA 源路径**: `papers/mintou/mintou_p2_hygraph_load_forecasting`
- **当前目标刊**: MDPI Electronics(主)/ MDPI Applied Sciences(次)
- **当前 RRI**: 25/100
- **当前预测**: **Reject(两刊都拒)**
- **🚨 组合级 #1 诚信红旗**

## 当前状态

✅ 已有(强证据):
- 真实 24h/day-ahead 信号:**OPSD +39-42% vs 最强基线,rolling ±0.00056 极稳**
- +74-80% vs 最强消融,可分组件贡献
- v1→v4 负结果全保留(诚实证据链)
- ARA 工程完整(26 runs + 12 tables,6 项中最丰富)

❌ 缺失 + 🚨 诚信问题:
- **🚨 "Transformer/Neural" 命名技术上为假**:整个实现是 Python 标准库 ridge regression + hyperbolic-distance-weighted features,**零 PyTorch / 零 attention / 零神经网络**。`src/environment.md` 明确确认 "Python standard library only"。Electronics 任何 soundness reviewer 都会抓到,构成"夸大主张",对作者/实验室声誉风险组合级最高。
- **🚨 Baseline degeneracy**:3 个命名 baseline(Euclidean-GCN Ridge / GCN-Temporal Ridge / Ablation-EuclideanGraph)在所有 metric 上产出**完全相同预测到小数点后 8 位**。另外 2 对同样模式。去重后只有 ~5 个独立 baseline,全是 naive/ridge 级,**真实数据上零神经网络**。
- Related work:238 B 占位符
- Sensitivity analysis:无
- 完整论文正文:零行

## 必须补齐的缺口(按优先级)

### 🔴 P0(fatal,诚信 + 实验,不补不能投)

| # | 缺口 | 严重度 | 工作量 | 说明 |
|---|---|---|---|---|
| 1 | **🚨 诚信修复**:PyTorch 实现 Poincaré ball embedding + hyperbolic distance attention **OR 诚实改名** | 4 | **选项 A 1-2 天 / 选项 B 1-2 周** | 选项 A:标题/摘要删 "Transformer/Neural",改为 "hyperbolic-distance-weighted ridge";选项 B:真实现 PyTorch 保留方法论主张。**推荐选项 B** |
| 2 | **🚨 真实神经网络 baseline**:LSTM / TCN / DLinear / PatchTST 在真实数据上 | 4 | 3-5 天 | 当前零神经网络 baseline,必须补 |
| 3 | **🚨 Baseline degeneracy 修复**:找出 3 个 baseline 输出完全相同的原因 | 4 | 2-3 天 | 可能是同一个模型被命名了 3 次,需要去重或真实现 |

### 🟡 P1(serious,投稿前必补)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 4 | Sensitivity analysis(4 参数) | 3 | 2-3 天 |
| 5 | Panama 数据集加入(已缓存在 `data/public_datasets/`) | 2 | 1 天 |
| 6 | Related work survey:hyperbolic GNN / spatiotemporal GNN load forecasting / hierarchical forecasting | 3 | 5-7 天 |
| 7 | 标题/摘要限定 day-ahead 24h | 2 | 1 天 |
| 8 | **标题删 "Smart Dispatch"**(超出实际主张) | 2 | 0.5 天 |
| 9 | 完整论文正文 | 3 | 5-7 天 |

### 🟢 P2(minor,可选但有益)

| # | 缺口 | 严重度 | 工作量 |
|---|---|---|---|
| 10 | `logic/problem.md`、`concepts.md`、`constraints.md` 扩充(占位符) | 2 | 2 天 |

## 投稿可行性判断

- **当前状态**:Reject(两刊都拒)—— 诚信问题 + baseline degeneracy 是致命伤
- **P0 完成后**:Major Revision(Electronics,RRI 55-65)
- **P0 + P1 完成后**:Accept 概率高(Electronics,RRI 70-80)
- **最快路径**:**4-6 周** 投 MDPI Electronics(若选选项 A 改名 → 3-4 周;选项 B PyTorch 实现 → 4-6 周)

## 行动清单(按周)

| Week | 行动 |
|---|---|
| **W1-2** | **诚信修复**:选项 B PyTorch 实现 Poincaré + hyperbolic attention;同时修复 baseline degeneracy;加 LSTM/TCN/DLinear/PatchTST 在真实数据上 |
| **W3** | Sensitivity analysis(4 参数)+ Panama 数据集 |
| **W4** | Related work survey;标题/摘要限定 day-ahead 24h;标题删 "Smart Dispatch";MDPI 格式 |
| **W5** | 英语润色 + 内部一致性检查 + 投稿 Electronics Section AI 或 Power Electronics |
| **W6-10** | 等首决(Major Revision 预期)+ 修订 |

## 诚实边界

- 🚨 **按现状投稿构成"夸大主张"**:即便 24h/day-ahead 信号真实,"Transformer/Neural" 命名在技术上为假,任何 reviewer 检查 `src/environment.md` 都会发现
- 1h 短时预测是记录在案的 limitation,主张必须严格限定在 day-ahead 24h
- Related work 必须诚实覆盖 hyperbolic GNN + 负荷预测既有工作,避免选择性忽略
- 标题 "Smart Dispatch" 超出实际主张(论文只做 day-ahead load forecasting,不做 dispatch)
- Baseline degeneracy 必须修复或诚实披露("3 个 baseline 实际上等价")

## 组合级警示

- p2 是组合级 **#1 诚信红旗**,必须先修复再考虑投稿
- 即便信号真实(+39% day-ahead),按现状投稿对作者/实验室声誉风险最高
- 推荐修复顺序:**p2 诚信修复 → p3/p6 P0 → p4 P0 → p5 外部 ground truth → p1 改造**

## 关联文件

- `ROUND2_REVIEW.md` — 完整 7 维评审(已在本目录)
- `JOURNAL_REVIEW.md` — Round 1 期刊匹配度对比
- `README.md` — 工程索引
- `papers/mintou/mintou_p2_hygraph_load_forecasting/` — ARA 工程本体
- `src/environment.md` — 诚信问题关键证据("Python standard library only")
