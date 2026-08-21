# 数据处理与正式实验统一总结（更新至 2026-08-08）

**范围：** C2GES 与 MA-SQLGrid 的数据构建、机器标注、正式实验、独立复算和论文证据边界。  
**总原则：** NERC、RTS-GMLC 和 SimBench 的标注产物均为 **machine-adjudicated silver labels（机器裁决银标）**，不是 human/expert gold。BIRD Mini-Dev 是公开 text-to-SQL 基准，其模型输出使用冻结协议和官方 EX 边界评价。

## 1. 数据资产总览

| 资产 | 规模 | 状态 | 论文中的证据角色 |
|---|---:|---|---|
| C2GES FEVER 转换 | 文档分组的训练/开发/测试集 | 已冻结并完成五种子、消融和交叉编码器实验 | C2GES 模型性能主证据 |
| C2GES NERC development silver | 15 文档 × 5 角色问题 = 75 项 | 双模型独立标注、规则消解、第三模型裁决完成 | 标注流程开发与一致性分析；不报告域模型 F1 |
| C2GES NERC frozen silver | 15 个未用于开发的文档 × 5 = 75 项 | 先冻结后标注；packet SHA-256 `36ab3b8f…73c7` | 冻结银标流程验证；不是专家金标 |
| MA RTS-GMLC/SimBench development | 91 候选 + 30 盲测负样本 | 机器裁决与确定性列校验完成 | 开发、错误分析和可移植性诊断 |
| MA RTS-GMLC/SimBench frozen silver | 85 新候选 + 30 盲测负样本 | 先冻结后标注；set SHA-256 `5d1ed4ea…5dc3` | 银标质量与防线验证；不作为模型外部准确率 |
| MA GridDB | 180 评估问题，8 表/98 行 | 双骨干 2×2、组件和语义压力实验完成 | MA-SQLGrid 本地域主实验 |
| BIRD Mini-Dev | 500 项、11 个数据库、2 模型、4 方法 | v1.1 正式运行及独立复算完成 | MA-SQLGrid 公开跨数据库基准 |

## 2. 机器标注体系与治理

- 标注器 A：DeepSeek 服务（实际 served ID 逐次记录）。
- 标注器 B：Gemini 2.5 Flash。
- 裁决器 C：GPT 系列服务，仅处理实质性分歧；标签身份匿名化。
- C2GES 使用两级消解：集合粒度差异由冻结的 Tier-1 规则处理，实质冲突才进入 Tier-2 裁决。
- MA 同时使用语义标注和确定性 SQLite 输出列校验；二者互补，避免将语言模型的列替换盲区当作正确样本。
- 所有原始调用账本 append-only；失败、分歧、弃权、技术重试和隔离条目均保留。
- 无真人专家复核，因此论文不得出现“expert-adjudicated”“human-gold”或等价表述。

## 3. C2GES NERC 银标结果

| 指标 | development（75） | frozen（75） |
|---|---:|---:|
| answerable 一致率 | 0.853 | 0.973 |
| evidence-role 一致率 | 0.853 | 0.973 |
| evidence 完全一致率 | 0.413 | 0.240 |
| evidence Jaccard | 0.599 | 0.631 |
| Tier-2 裁决数（率） | 25（0.333） | 13（0.173） |
| unresolved | 0 | 0 |
| 格式/API 失败 | 0 | 0 |

解释边界：frozen 集上的可回答性一致率更高，但证据集合完全一致率仍低，说明主要不确定性在句子集合粒度。Jaccard 和裁决率比完全一致率更能描述机器标注行为。这些数字评价标注流程，不评价 C2GES 在 NERC 上的选择性能。

## 4. MA 外部银标结果

### 4.1 Development-visible 候选

- 91 个 RTS-GMLC/SimBench 候选中，88 个通过机器语义审查，3 个因语义歧义或不匹配保持隔离。
- 30 个盲测负样本中，机器标注器检出 22 个；确定性列校验检出 9 个；联合覆盖 29/30（0.967）。
- 原有 Qwen 可移植性诊断包含 364 次调用，但仅作为字段缺失、列幻觉和 schema 序列化错误分析，不报告外部准确率。

### 4.2 Frozen silver set

- 85 个新候选与 30 个负样本在标注前完成冻结；115 项全部可执行。
- 两个机器标注器语义正确性一致率 0.878，Cohen's κ=0.668；17 项（0.148）进入裁决；0 unresolved。
- 85 个原始候选中 83 个通过，2 个保持隔离。
- 负样本机器检出率 28/30（0.933）；与确定性列校验联合后为 30/30（1.000）。

解释边界：这些结果说明银标与列校验防线可以发现候选缺陷，但不能替代电力系统领域专家对术语、单位、投影、等价 SQL、排序和并列规则的复核。

## 5. BIRD Mini-Dev 正式实验（MA-SQLGrid）

### 5.1 冻结与执行身份

- 协议：`MA-PUBLIC-BIRD-MINIDEV-v1.1`。
- 冻结 SHA-256：`0ABA454650C569D51183D4A96248FF977A5DBDF3A82A77C62592162F28F9F640`。
- 运行时：Python 3.10.11 / SQLite 3.40.1；llama.cpp b9637；本地 RTX 3090；Qwen 后 Granite 严格串行。
- 每个模型 2500 次调用、2000 条最终预测、0 重试；新增调用恰好 5000。
- 两个既有事故运行共 2476 次物理调用，完整保留且不进入论文结果；总物理调用数 7476。
- 后运行审计：13/13 PASS；在冻结运行时重新执行 4000 条预测和 500 条 gold SQL，0 个分数不一致。
- 审计文件 SHA-256：`62667A5510DD8AF88B9E12F890A8FE0B270A060C938BB3C104A1AB2FC3360727`。

### 5.2 Public EX 结果

每格为 accuracy [95% database-clustered composition-sensitivity interval]，分母均为 500。

| 模型 | B0 Direct | B1 Decomposition | B2 Schema selection | B3 Execution repair |
|---|---:|---:|---:|---:|
| Qwen2.5-Coder-7B | 0.378 [0.286, 0.470] | 0.302 [0.203, 0.401] | **0.394 [0.279, 0.511]** | 0.348 [0.250, 0.452] |
| Granite-3.3-8B | 0.204 [0.125, 0.284] | 0.210 [0.131, 0.294] | 0.202 [0.137, 0.273] | **0.236 [0.159, 0.318]** |

Holm 校正覆盖 12 个模型内方法两两对比。Qwen 中 decomposition 比 direct 低 7.6 个百分点（`p_Holm=0.0430`），schema selection 比 decomposition 高 9.2 个百分点（`p_Holm=0.0117`）；Granite 无对比通过校正。结果显示方法排序依赖骨干，不支持“单一流程普遍最优”。该实验不是 DKASQL 复现。

## 6. 两篇论文的实验状态

### C2GES

- FEVER 五种子主实验、九种既有模式、真实 no-floor/no-role 消融、MiniLM/BGE、5×5 upstream–downstream 敏感性分析均已完成并审计。
- NERC development/frozen 银标构建已完成，但只进入数据处理和治理章节，不进入域性能排行榜。
- 不需要重新运行模型实验。

### MA-SQLGrid

- GridDB 双骨干 2×2、700-call 组件实验、15-state 语义压力套件和外部可移植性诊断均已完成。
- BIRD v1.1 5000 次正式调用与全量独立复算已经完成，可进入论文。
- 不需要重新生成；后续仅需保持统计表、正文和审计产物一致。

## 7. 已知限制与投稿前事项

1. NERC、RTS-GMLC 和 SimBench 标签均无真人专家复核，只能称机器裁决银标。
2. C2GES 的 NERC 数字是标注流程统计，不能报告为 selector F1 或域准确率。
3. MA 外部银标不能把开发可见候选转化为 sealed human benchmark；BIRD 则提供公开跨数据库证据，但仅覆盖 11 个 Mini-Dev 数据库和两个量化模型快照。
4. GridDB、NERC 派生文本、RTS-GMLC 和 SimBench 的再分发仍需分别完成许可审查。
5. 投稿前仍需补齐永久仓库 URL/DOI、确认 grant number、作者贡献与全体作者批准，并按期刊当日政策复核声明。

## 8. 关键产物

- `annotation_pilot_20260807/STAGE2_REPORT.md`
- `annotation_pilot_20260807/STAGE3_REPORT.md`
- `MA_SQLGrid/public_baseline_protocol/BASELINE_PROTOCOL_FREEZE_v1_1.json`
- `MA_SQLGrid/public_baseline_protocol/formal_runs/MA_PUBLIC_BIRD_v1_1_qwen_clean1/`
- `MA_SQLGrid/public_baseline_protocol/formal_runs/MA_PUBLIC_BIRD_v1_1_granite_clean1/`
- `MA_SQLGrid/public_baseline_protocol/formal_runs/MA_PUBLIC_BIRD_v1_1_postrun_audit/POST_RUN_INDEPENDENT_AUDIT_v1_1.json`
