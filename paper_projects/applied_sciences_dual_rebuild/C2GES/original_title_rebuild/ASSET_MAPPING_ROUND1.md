# C²GES 原标题版资产映射与第一轮补缺报告

## Material Passport

- Artifact type: implementation and provenance audit
- Scope: `C2GES/original_title_rebuild/` only
- External API/network use: none
- Result status: code-level verification only; no manuscript performance metric is claimed
- Silver-label boundary: existing NERC role/evidence records remain machine-verified candidates, not human or expert gold

## 1. 审计结论

上午版资产不是废弃版本。它已经形成证据句选择所需的角色词典、查询相关性、句间图信号、链式支持、基线/消融接口、文档级统计和可审计数据构建器。原标题所需但此前没有形成独立正式实现的部分是：报告级因果事件图对象、可复现的结构干预运算、反事实敏感度，以及同时执行长度、角色覆盖、冗余抑制和原文顺序恢复的抽取式摘要器。

本轮没有修改历史冻结结果、CMC Word 原稿或任何既有结果目录。

## 2. 可复用资产台账

| 资产 | 当前 SHA-256 | 原标题版用途 | 本轮处理 |
|---|---|---|---|
| `2026_c2ges_engineeringletters/source/code/main.py` | `C2B8154C9BB9C8790A21B5835E05D82454C23A7FD7689088778D8BED01E0EF4E` | 条件定义、角色分层、消融、Bootstrap 与结果账本 | 设计复用，不修改 |
| `2026_c2ges_engineeringletters/source/code/c2ges_learnable.py` | `473B36C3BEABE8DFABDB6EC138FBBF1FCE82A1E3A4E85FDB2965890DEBFA33F8` | 可学习角色头、混合权重、FEVER 辅助能力实验 | 后续实验适配，不修改 |
| `workspace/verification_pilot/scripts/run_c2ges.py` | `F00273779DDDC1B8AB6C3D0C270362C9A13C6076AB32E6D82CD03BBE5CF603AD` | 五类角色词典、句图、链式支持和证据排序 | 角色词典和图思想适配到离线模块，不修改源文件 |
| `original_title_rebuild/build_nerc_summary_dataset.py` | `6BAFDD9295DACEF4FB37D7349874BB3A20DDE6AEC113A44C86D0BD0C50919FE5` | 官方 Executive Summary 参考、正文候选、哈希划分和来源审计 | 作为正式数据入口保留 |
| `original_title_rebuild/PROTOCOL.md` | 本轮冻结前状态 | 主/次指标、比较条件和不夸大规则 | 保留；正式运行前需连同新增模块重新冻结 |

哈希仅描述本次审计读取到的工作区状态，不表示它们与任何更早压缩包的冻结清单自动一致。

## 3. 新增最小正式模块

`c2ges_offline.py` 新增三个可执行部件：

1. `CausalEventGraph`：从句子、词典角色信号和可选银标角色证据生成带类型、有方向的句子级因果代理图。边方向由角色语义确定，不强迫等同于报告叙述顺序。
2. `intervene()` 与 `counterfactual_sensitivity()`：删除指定节点或指定边，并以类型化因果流损失计算确定性反事实敏感度。原图保持不变，所有未知节点干预均失败关闭。
3. `ConstrainedExtractiveSummarizer`：融合相关性、角色、图、反事实和位置分数；预算允许时覆盖“原因/触发—传播/影响—缓解”三类功能；随后使用冗余惩罚补足预算并恢复原文顺序。

该实现是透明、离线、确定性的最小方法核心。它不等价于结构因果模型，也不把词典或银标边解释为真实物理因果关系。

## 4. 单元测试覆盖

`test_c2ges_offline.py` 使用 Python 标准库 `unittest`，覆盖：

- 图构建的确定性、类型边和非因果句处理；
- 节点干预不修改原图且降低因果流；
- 边干预的精确性；
- 三类角色覆盖、句数预算和原文顺序恢复；
- 重复句 ID、非法权重、未知干预和非法预算的失败关闭行为。

现有 `test_build_nerc_summary_dataset.py` 继续覆盖真实本地数据构建、开发/测试划分及数据集哈希生成。其测试名中的“no reference prefix leakage”目前只间接检查构建成功，正式冻结前仍需补充逐文档文本重合阈值断言。

本轮实际验证记录：

- Python 3.10.11：`test_c2ges_offline.py` 的 6 项测试全部通过；该便携运行时启用了隔离路径，因此验证命令显式把本目录加入 `sys.path`。
- Python 3.12：同一 6 项测试全部通过。
- 真实本地数据构建 smoke test：纳入 21 份报告，哈希划分为 9 份开发集和 12 份测试集，排除 19 份；临时构建数据集 SHA-256 为 `171c3da96fb452e3c76e693aed6c81f2217fa368c3686593d7c4f0011e935166`。该数字是数据构建审计，不是模型效果。

## 5. 尚未完成、不得写成结果的正式实验项

- 尚未使用正式 NERC benchmark 对 `lead`、`centroid`、`textrank`、`role`、`graph_no_cf` 与 `c2ges_full` 进行统一运行。
- 尚未在开发集冻结混合权重；本轮权重只是可测试默认值，不能报告为调优结果。
- 尚未计算 ROUGE-1/2/L、角色覆盖、因果路径覆盖、冗余或报告级配对 Bootstrap。
- 尚未加入强语义编码器/重排序器对比，也没有证明新增反事实项带来统计或实际增益。
- 现有机器验证角色证据不是人工专家金标；若论文需要人工一致性结论，仍需真实人工协议和记录。
- 正式运行前必须生成包含数据、代码、配置、运行时和输出目录规则的新冻结清单及 SHA-256。

## 6. 下一轮接入点

正式 runner 应读取 `nerc_executive_summary_benchmark.jsonl`，对同一文档的全部条件使用相同候选句和预算；`graph_no_cf` 将反事实权重置零并重新归一化，`c2ges_full` 使用完整模块。所有预测需逐文档记录句 ID、分项得分、选择原因、图边、干预差值和来源哈希，以便论文表格能够回溯到原始运行资产。
