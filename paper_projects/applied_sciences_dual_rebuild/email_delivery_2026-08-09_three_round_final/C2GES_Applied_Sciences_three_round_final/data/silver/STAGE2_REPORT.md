# 阶段 2 报告：MA 全量 + C2GES v1.2 验证门与全量

- 日期：2026-08-07
- 授权：`STAGE2_AUTHORIZATION_20260807.json`（DUAL-LLM-ANNOTATION-20260807-02，调用上限 700）
- 协议（运行前程序化校验 SHA-256，全部通过）：
  - C2GES v1.1 `41053d9b…b994f`（验证门，未通过）→ v1.2 `40d5cc57…bf38`（现行）
  - MA v1.1 `926a0826…b75c`（现行）
- **全部产出均为 machine-adjudicated silver labels，不是 human/expert gold，不得以此名义引用。**
- 本文档合并替代早前仅含 v1.1 门禁失败的版本；v1.1 阶段的全部原始记录原样保留。

## 总结论

| 事项 | 结果 |
|---|---|
| C2GES v1.1 验证门 | **未通过**（12 条复标裁决率 0.75 > 0.50），催生了 v1.2 两级消解规则 |
| C2GES v1.2 验证门 | **通过**（Tier-2 C 裁决率 5/12 = 0.417 ≤ 0.50） |
| C2GES 全量 75 题 | 完成：agreement 30 / Tier-1 20 / Tier-2 25（技术性补跑后 **unresolved 0**） |
| MA 全量 121 条 | 完成：一致率 0.926、κ=0.764、13 条独立条目经裁决；负样本检出率补跑后 **0.733 ≥ 0.7**，但 wrong_column 族仅 0.30，仍是明确的可靠性限制 |
| 调用预算 | **518 / 700**（以 append-only 账本为准的精确计数，含 10 条补跑调用），无模型被停止，served id 全部合规 |

## 1. C2GES：v1.1 → v1.2 的演进与验证门

v1.1 验证门（12 条最难样本复标，R1–R7 prompt）裁决率 0.75，分歧分析显示主因是**证据集粒度差异**（一方多带背景句）而非实质性冲突。v1.2 相应改为两级规则：answerable 与 evidence_role 一致且无人弃权时，用确定性规则消解粒度差异（双方都 false → 空证据；子集关系 → 取较小集 subset_minimal；交集非空且 Jaccard≥0.5 → 取交集 intersection_consensus）；只有实质分歧（answerable/role 不同、弃权、交集为空或 Jaccard<0.5）才调 C。

v1.2 验证门复用 v1.1 的 12 对 A/B 标签（协议允许），仅重跑消解/裁决逻辑：

- Tier 分布：agreement 3、Tier-1 4（全部 subset_minimal）、Tier-2 5 → **Tier-2 率 0.417，通过门禁**。
- Tier-2 的 5 条中：2 条复用 v1.1 已有的成功 C 裁决（输入与裁决规则完全相同；重复调用属无意义消耗且违反"不因结果重试"精神）；3 条为 v1.1 时 C 超时的 unresolved 技术性重试，其中 1 条成功、2 条仍因 C 通道超时/网络错误记为 unresolved（记录保留）。
- 结果文件：`runs/c2ges_stage2/validation_gate/gate_result_v1_2.json`、`final_labels_v1_2.jsonl`、`adjudicated_v1_2.jsonl`。

## 2. C2GES 全量 75 题（v1.1 prompt + v1.2 消解）

全新标注（未复用 pilot/gate 任何标签），输出 `runs/c2ges_stage2/`。

| 指标 | v1.2 全量 (n=75) | v1.1 验证门 (n=12) | v1.0 pilot (n=25) |
|---|---|---|---|
| answerable 原始一致率 | 0.853 | 0.833 | 0.88 |
| answerable Cohen's kappa | 0.132 | 0.00 | 0.00 |
| evidence_role 一致率 | 0.853 | – | – |
| evidence 完全一致率 | 0.413 | 0.25 | 0.28 |
| evidence Jaccard 均值 | 0.599 | 0.483 | 0.551 |
| **C 裁决率（v1.2 为 Tier-2 率）** | **0.333** | 0.75（v1.1 规则）/ 0.417（v1.2 规则） | 0.76 |
| Tier-1 确定性消解率 | 0.267（subset_minimal 18、intersection_consensus 2） | – | – |
| 弃权 | A 12、B 0、C 4（裁决时弃权） | A 2、B 0、C 0 | A 2、B 0、C 0 |
| 格式失败 | 0 | 1（B qid 回显） | 0 |
| 终态 | agreement 30 / tier1 20 / adjudicated 25 / **unresolved 0**（补跑后） | – | 全部有终态 |

要点解读：

- v1.2 把 C 裁决率从 0.76 压到 0.333，其中 26.7% 的条目由 Tier-1 确定性规则消解——证实 pilot 期的高裁决率确实主要是粒度偏好差异。
- Tier-2 的 25 条中 12 条由 **A（DeepSeek）弃权**触发：R6 使 A 明显保守（16% 弃权率，B 为 0）。answerable κ=0.132 仍低，说明"显式陈述 vs 推理"的边界判断是剩余的主要实质分歧。
- 首轮 5 条 unresolved 全部因 Cloubic C 通道在 06:14–06:24 时段连续 read-timeout/网络错误；**2026-08-07 晚些时候的技术性补跑（同输入、同匿名映射、同裁决规则，每条最多 3 次尝试）5/5 全部成功**，终态更新并加 `note="resolved_by_technical_retry_20260807"`，原始超时记录保留在 raw_ledger.jsonl。
- 最终标签全部 answerable=true——本数据集中没有被判 false 的条目（A 的 12 次弃权在裁决后均被 C 判为可回答）。

Token 与延迟（C2GES 全量 + 补跑）：A 75 次（入 262,936 / 出 16,185，均 2.28s）；B 79 次（入 297,607 / 出 19,670，均 3.30s，4 次技术失败后重试成功）；C 42 次（含补跑 5 次，入/出 token 见 stats.json；首轮 17 次为超时/网络失败尝试，补跑 5 次全部一次成功、约 5–7s）。

## 3. MA 全量 121 条（91 原始 + 30 盲测负样本）

负样本与原始样本混合并以盲化 id（MA2_001–121）标注，A/B 提示形式完全一致。沙箱：121/121 只读执行成功。输出 `runs/ma_stage2/`。

| 指标 | 数值 |
|---|---|
| semantically_correct 原始一致率 | 0.926（112/121） |
| semantically_correct Cohen's kappa | **0.764**（pilot 时不可计算，现在有区分度） |
| 裁决 | 13 条独立条目进入裁决（10.7%）；首轮 C 成功 8 条、unresolved 5 条，**技术性补跑后 5/5 全部成功，unresolved 归零**（adjudicated.jsonl 共 18 条裁决记录，其中 5 条为同条目补跑） |
| 弃权 / 格式失败 / A·B API 失败 | 0 / 0 / B 1 次（重试成功） |

**负样本盲测检出率（final 判 semantically_correct=false 的比例）：总体 0.733（22/30，补跑后）——高于 0.7 的协议警示线；但 wrong_column 族检出率仅 0.30，仍须明确标记为标注器可靠性限制。**（补跑前为 0.60：4 条控制当时因 C 超时 unresolved 被保守计入未检出。）

| 扰动族 | n | 检出 | 检出率 |
|---|---|---|---|
| wrong_filter_value | 3 | 3 | 1.00 |
| wrong_aggregation | 4 | 4 | 1.00 |
| drop_order | 4 | 4 | 1.00 |
| drop_filter | 9 | 8 | 0.89 |
| **wrong_column** | **10** | **3** | **0.30** |

8 条未检出中 7 条是 wrong_column（SELECT 列换成同表另一列）：两个标注器系统性地忽视"列名语义是否匹配问题"，仅在结果列名明显答非所问时才判错。

91 条原始候选中判 false 的 3 条（均 semantic_mismatch）：SB-AUTO-005、SB-AUTO-014、RTS_AUTO_047（盲化 id MA2_076 / MA2_104 / MA2_118，见 `stats.json`）。错误分类分布（原始 91 条，补跑后）：none 88、semantic_mismatch 3。

Token 与延迟（MA 全量 + 补跑）：A 121 次（入 121,501 / 出 20,328，均 1.75s）；B 122 次（入 133,988 / 出 24,860，均 3.08s）；C 33 次（含补跑 5 次；首轮 20 次为超时/网络失败尝试，补跑 5 次全部一次成功）。

## 4. 合规声明

- 命名：全部产出为 machine-adjudicated silver labels；91 条原始候选仍为 AUTO_CANDIDATE，本阶段结果不得作为外部 gold 准确率引用。
- 目录：`runs/c2ges_pilot/`、`runs/ma_pilot/` 未被触碰；v1.1 验证门文件未覆盖（v1.2 结果写入新文件 `*_v1_2.*`）。
- 记录：全部失败/分歧/超时/重试记录保留（首轮 10 条 unresolved 及其后续补跑记录、C 的 45+ 次失败尝试、B 的 5 次失败尝试，均在 raw_ledger.jsonl；补跑成功的终态在 final_labels.jsonl 中带 `note="resolved_by_technical_retry_20260807"`）。补跑过程中曾因补跑记录键名笔误（`question_id` vs `qid`）导致 stats 重算崩溃：已修正解析视图 `adjudicated.jsonl` 中 5 条记录的键名以对齐该文件历史 schema，append-only 的 raw_ledger.jsonl 未做任何改动，统计代码亦已兼容两种键名。
- 重试：仅技术性（超时/5xx/网络）重试，最多 2 次，逐条入账；无任何因结果内容的重试。v1.1 的 3 条 C-unresolved 重试与本次 10 条补跑均为协议允许的不同时间技术重试（这些条目此前从未得到 C 的成功响应）。
- API key：对 `annotation_pilot_20260807/` 全部 65 个产出文件做程序化扫描（`.env`/`.env.cloubic` 所有 key 值比对），结果 NONE；账本只记 prompt SHA-256。
- served model id：A 恒为 `deepseek-v4-flash`（冻结豁免别名，逐次记录）；B `gemini-2.5-flash`、C `gpt-5.4` 均一致。
- 预算：**518 / 700**，按 append-only 账本精确计数：v1.1 验证门（含冒烟）37、v1.2 验证门 C 重试 9、C2GES 全量（含冒烟）191、MA 全量（含冒烟）271、unresolved 补跑 10。说明：运行器进程内计数器在并发运行时会低估（只计启动时已存在的账本记录），因此以账本事后计数为准；两个数字均远低于上限，停止门禁未触发。
- temperature=0、max_tokens=1024、直连无代理，全程遵守。

## 5. 对论文表述强度的建议

可以支撑：
- "双模型独立标注在答案判定（answerable / semantically_correct）维度一致性高（0.85 / 0.93），实质性分歧由第三模型裁决收敛"——MA 侧 κ=0.764 达到 substantial。
- "证据集粒度差异可通过确定性最小充分性规则消解，使裁决成本下降约一半"（C2GES：0.76 → 0.33）。
- "auto-candidate SQL 经双模型审核后 88/91 判为语义正确，3 条判 semantic_mismatch"——作为 silver-label 质量观察，非 gold 准确率。

不能支撑 / 必须声明的限制：
- **标注器对 wrong_column 类错误检出率仅 0.30**（总体检出率 0.733 虽高于 0.7 警示线，但按族分解后该族明显不可靠）：对"列语义匹配"类错误，LLM 标注器不可靠；凡依赖该维度正确性的结论必须人工复核或附加确定性校验。
- C2GES answerable κ=0.132：两模型对"可回答性"边界的校准差异大（A 弃权率 16% vs B 0%），silver 标签的 answerable=false 类结论（本次为 0 条）若出现需审慎对待。
- 验证门阶段的 2 条 unresolved（v1.2 门内 C 重试仍失败）保持缺失终态；全量两个数据集补跑后 unresolved 均为 0。
- 任何"人工/专家金标"表述均被治理红线禁止。
