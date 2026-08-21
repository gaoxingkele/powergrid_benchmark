# C²GES 原标题版离线正式运行 v0.1 报告

## Material Passport

- Experiment ID: `C2GES-NERC-FORMAL-v0.1-20260808`
- Status: `COMPLETE` and independently reproduced
- Execution mode: offline; no API or network call
- Test unit: report
- Test reports: 16
- Conditions per report: 6
- Prediction rows: 96
- Extraction budget: 5 sentences
- Freeze manifest SHA-256: `406ee363703fa5850339c586bfae87b403431bfec12294e3bc77787bec0fc477`
- Evidence boundary: role evidence is machine-verified silver candidate evidence, not human/expert gold

## 1. 数据边界修复

第一次数据构建发现 `nerc_008` 的 Executive Summary 被错误延伸到 25,209 词。原因是报告用 `Chapter 1: ...` 作为摘要结束边界，而旧规则未识别该标题。该首个目录已保留为诊断资产，未被覆盖或纳入正式冻结。

数据构建器随后增加确定性的 `Chapter 1` 结束规则和回归测试。重新构建得到28份可用报告：12份开发集、16份测试集，另12份按明确原因排除。正式测试参考摘要词数范围为279–2298，中位数790.5；候选句数范围为20–60，中位数54。

## 2. 冻结与复现

冻结清单逐项固定并验证：

- 配置 SHA-256：`FDECF9030CB2AD92F1F00EA9EA9B666C6C3BEC595AB2731698657FF413391DD5`
- 数据集 SHA-256：`3B74CA2EE3D2DD207341BC870B8B5319AB935566670B2FD7C192E7BB725A7C48`
- 数据构建器、方法模块和正式 runner 的代码哈希
- Python 3.12.10、NetworkX 3.6.1、rouge-score 0.1.2

Run 01 和全新目录的 Run 02 reproduction 均完成。以下三个核心输出逐字节哈希一致：

| Artifact | SHA-256 |
|---|---|
| `predictions.jsonl` | `4c1ed85dbbdbd0de76f02fd93ee96559b497e5764fb00e2b5d104802a91ab8b2` |
| `aggregate_metrics.json` | `4dd1e32756e84c4867ab855bdc4157686ffd5d1db319fe669264889c33e2bd1e` |
| `paired_bootstrap.json` | `f7e697aa8159991a0cf06a956d02e0b8d672925b9844b4fccd306aee1f7f3762` |

完整性检查确认每份报告恰有六个条件、每条预测恰有五个不重复句 ID，全部指标为有限的 `[0,1]` 数值。

## 3. 聚合结果

| Condition | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Silver Role Coverage | Redundancy |
|---|---:|---:|---:|---:|---:|
| Lead | 0.2220 | 0.0876 | 0.1262 | 0.2125 | 0.0539 |
| Centroid | 0.2564 | **0.1002** | **0.1405** | 0.2500 | 0.1645 |
| TextRank | 0.2218 | 0.0822 | 0.1267 | 0.1625 | 0.1845 |
| Role | 0.2367 | 0.0831 | 0.1185 | **0.4250** | 0.0614 |
| Graph without CF | **0.2647** | 0.0939 | 0.1326 | 0.4125 | 0.0820 |
| C²GES Full | 0.2608 | 0.0934 | 0.1323 | 0.3750 | 0.0683 |

粗体仅标记该列的观察最大值，不表示统计优势。

## 4. 配对报告级 Bootstrap

每项比较使用10,000次报告级重采样。完整 C²GES 相对 Lead 的 ROUGE-1 平均差为 `+0.0388`，95% percentile CI `[+0.0136, +0.0663]`；相对 TextRank 为 `+0.0390`，CI `[+0.0070, +0.0782]`。其余 ROUGE-1/2/L 比较的区间均跨越零，包括：

- C²GES Full − Centroid，ROUGE-L：`−0.0082`，CI `[−0.0259, +0.0058]`；
- C²GES Full − Role，ROUGE-L：`+0.0138`，CI `[−0.0063, +0.0368]`；
- C²GES Full − Graph without CF，ROUGE-L：`−0.0003`，CI `[−0.0053, +0.0055]`。

输出中的 bootstrap `p` 值没有做多重比较校正，只能作为探索性诊断，不能单独写成确认性显著性结论。

## 5. 可写入论文的有限结论

该运行支持以下事实性描述：离线图约束方法在这个16报告测试集上降低了相对 Centroid/TextRank 的句间冗余；完整方法的观察 ROUGE-1 高于 Lead 和 TextRank，且对应报告级 Bootstrap 区间未跨零。它不支持“完整 C²GES 全面优于所有基线”或“反事实模块已被证明有效”。Centroid 获得最高观察 ROUGE-2/ROUGE-L，Graph without CF 的观察 ROUGE-1 略高于完整模型。

## 6. 下一轮必须补强的实验设计

1. 当前 `graph_no_cf` 使用独立注册的非反事实权重，不是从完整模型仅删除一个通道的严格单因素消融。若论文要归因反事实价值，应冻结 v0.2：从完整权重删除 CF 后按比例归一化其余四项，其他设置不变。
2. 目前所有混合权重是预注册默认值，尚未在12份开发报告上执行嵌套或锁定的权重选择。不得称其为最优权重。
3. 需要增加至少一个强语义摘要/重排序基线；当前比较只能证明相对轻量离线基线的行为。
4. 参考摘要普遍长于五句预测，ROUGE 的长度敏感性需通过10句预算或长度匹配实验检查。
5. 银标角色覆盖只能作为诊断。没有真实人工标注时，不得报告专家一致性或人工金标准确率。

## 7. 权威产物位置

- 冻结数据：`formal_assets/dataset_nerc_exec_v0_1_chapterfix_20260808/`
- 正式结果：`formal_runs/C2GES_NERC_FORMAL_v0_1_20260808_run01/`
- 独立复现：`formal_runs/C2GES_NERC_FORMAL_v0_1_20260808_run02_reproduction/`

第一轮错误边界数据目录 `formal_assets/dataset_nerc_exec_v0_1_20260808/` 只保留作事故/诊断记录，明确排除于论文结果。
