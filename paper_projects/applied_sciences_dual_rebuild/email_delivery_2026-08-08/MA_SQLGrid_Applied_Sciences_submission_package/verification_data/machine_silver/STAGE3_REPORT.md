# 阶段 3 第一批报告：MA 收尾（修复 + 列校验防线）与 C2GES sealed set 标注

- 日期：2026-08-07
- 授权：`STAGE3_AUTHORIZATION_20260807.json`（DUAL-LLM-ANNOTATION-20260807-03，调用上限 550，独立计数）
- 协议（运行前程序化校验 SHA-256）：`C2GES_SEALED_SET_PROTOCOL_v1.json` = `f1929ee6…4eb0` ✔（MA sealed 协议本批不使用）
- **全部产出均为 machine-adjudicated silver labels，不是 human/expert gold。**

## 总结论

| 事项 | 结果 |
|---|---|
| 3 条问题候选修复（v2 工件） | 3 条 fixed_sql 沙箱可执行；重标注：1 条通过、2 条仍判 false（原因见下，含一处裁决器自相矛盾） |
| 确定性列校验防线 | 91 条原始 0 列错配；30 负样本中捕获 wrong_column 9/10；**标注器+列校验联合覆盖 29/30 = 0.967** |
| C2GES sealed 75 题 | 冻结后标注完成：agreement 18 / Tier-1 44 / Tier-2 13，**Tier-2 率 0.173**，0 unresolved、0 失败 |
| 预算 | **172 / 550**（账本精确计数） |

## 1. 三条问题候选的修复与重标注（任务 1）

修复工件 `runs/ma_stage2/candidate_fixes_v2.jsonl`（原 91 条文件未动；original_sql_sha256 入账）。修复依据裁决器 minimal_fix + 只读 DISTINCT/schema 实地查询：

| 候选 | 修复 | 沙箱 | A/B 重标注 | 最终结论 |
|---|---|---|---|---|
| SB-AUTO-005 | `WHERE generator_type='lv_RES'`（域内仅 lv_RES×133 + Hydro_MV×1，physical_type 全为 RES，无字面 'Distributed' 值） | 1 行 | A=false / B=true → C 裁决 | **semantically_correct=true**（C：lv_RES 是可辩护的"分布式"读法） |
| SB-AUTO-014 | 同上过滤 + 保留 `SUM(maximum_active_power_mw)` | 1 行 | A=false / B=true → C 裁决 | **仍 false**（C：schema 无明确 distributed 标记，lv_RES 是"不可靠假设"） |
| RTS_AUTO_047 | 增加 `AND reserve_product LIKE 'Spin_%'` | 3 行 | A=true / B=false → C 裁决 | **仍 false**（C：问题要求 each product，过滤 spinning 反而过度约束） |

必须如实指出的两点：

- **裁决器对同一假设（lv_RES≈分布式）在 005 和 014 上给出了相反结论**；且 RTS_AUTO_047 阶段 2 裁决说"缺 spinning 过滤"、阶段 3 裁决说"不该加 spinning 过滤"——该问题文本（"maximum spinning reserve requirement for each product"）自身存在歧义，机器裁决无法在歧义上收敛。**建议：RTS_AUTO_047 标记为"问题需人工修订"；SB-AUTO-005/014 的分布式语义需数据字典级确认。**在人工确认前，这 3 条不应进入任何 benchmark 声明。
- 数据坑：SimBench `maximum_active_power_mw` 全列为 NULL（SB-AUTO-014 的"maximum"度量在该库上恒为 NULL），已写入 fix_rationale。

## 2. 确定性列校验防线（任务 2）

`column_check.py` → `runs/ma_stage2/column_check_report.json`。规则：候选 SQL 沙箱只读执行的结果列名（有序）与期望列比对（RTS 取 `answer_shape.columns`；SimBench 取其 gold_sql 沙箱结果列；负样本继承源问题期望列）。

- **91 条原始：0 条列错配**（与阶段 2 的 3 条 false 均为过滤类问题一致）。
- **30 条负样本捕获 9 条，全部为 wrong_column 族（9/10 = 0.90）**；其余四族 0 捕获属设计预期（列校验不管过滤/聚合/排序）。唯一漏网的 wrong_column（MA2_040 / 源 SB-AUTO-021）因扰动保留了 `AS` 别名、输出列名未变，但被标注器检出。

组合防线（任一检出即算覆盖）：

| 扰动族 | n | 标注器检出 | 列校验捕获 | 联合覆盖 |
|---|---|---|---|---|
| wrong_column | 10 | 3 | 9 | **10（1.00）** |
| drop_filter | 9 | 8 | 0 | 8（0.89） |
| wrong_filter_value | 3 | 3 | 0 | 3（1.00） |
| wrong_aggregation | 4 | 4 | 0 | 4（1.00） |
| drop_order | 4 | 4 | 0 | 4（1.00） |
| **合计** | **30** | 22 | 9 | **29（0.967）** |

唯一双层漏检的是 1 条 drop_filter 控制。**结论：阶段 2 发现的标注器 wrong_column 盲区（0.30）已被确定性列校验有效补齐（联合 1.00）；当前残余风险集中在"丢过滤但列名不变"型错误（0.89）。**

## 3. C2GES sealed set 冻结与全量标注（任务 3）

冻结（先冻结后标注，运行器强制校验）：
- 选集：`agent_audit_40doc/` 排除 15 个 dev 文档后 25 个候选，按 doc_id 排序取前 15 个满足 ≥40 句且 5 问题的文档 → **nerc_001…nerc_015 全部入选**（无跳过；另有 10 个合格未用）。所有文件均含 doc_id（文件名回退未触发）；manifest.json 已跳过。
- `runs/c2ges_stage3/sealed_packet.jsonl`：与 blind_packet 同 schema（**未复制 audit 的 answer/evidence/verification 字段**，无泄漏声明在 manifest）；packet sha256 `36ab3b8f…73c7`，15 个文档逐文档 sha256 见 `sealed_manifest.json`（custodian=annotation-pipeline）。
- 插曲：首次冻结后标注端哈希校验失败——Windows 文本写入把 LF 转成了 CRLF。校验逻辑按设计拦截，改为字节写入后重新冻结（期间零标注调用），二次校验通过。

标注（v1.1 prompt + v1.2 两级消解，75 题全新标注）：

| 指标 | sealed (n=75) | dev 全量 v1.2 (n=75) |
|---|---|---|
| answerable 一致率 / κ | **0.973** / 0.00（边际偏斜，73/75 双 true） | 0.853 / 0.132 |
| evidence_role 一致率 | 0.973 | 0.853 |
| evidence 完全一致率 | 0.24 | 0.413 |
| evidence Jaccard 均值 | 0.631 | 0.599 |
| Tier 分布 | agreement 18 / **Tier-1 44 (58.7%)** / Tier-2 13 | 30 / 20 / 25 |
| **Tier-2 C 裁决率** | **0.173** | 0.333 |
| Tier-1 细分 | subset_minimal 38、intersection_consensus 6 | 18 / 2 |
| 弃权 | A 2、B 0、C 1 | A 12、B 0、C 4 |
| 格式失败 / API 失败 / unresolved | 0 / 0 / **0** | 0 / 0 / 0（补跑后） |
| 终态 answerable=false | 0 | 0 |

解读：sealed 集上 A/B 实质性分歧率（Tier-2 0.173）显著低于 dev 集（0.333），A 弃权从 12 降到 2——dev 集的"可回答性边界"分歧在 sealed 集上很少见（可能因 sealed 文档问题与该集建设时验证过、句子切分更规整）。粒度差异仍是主旋律（58.7% 走 Tier-1），由确定性规则消解。两集合证据完全一致率都低（0.24–0.41），再次印证证据标注应以 Jaccard/集合指标报告、配合 Tier-1 消解，而非追求完全一致。

Token 与延迟（sealed）：A 75 次（入 281,207 / 出 18,737，均 2.51s）；B 75 次（入 313,374 / 出 24,541，均 3.75s）；C 13 次（入 58,820 / 出 3,106，均 6.35s，零失败——C 通道本次全程稳定）。

## 4. 合规声明

- 命名：全部 machine-adjudicated silver labels；sealed 标签与 dev 标签分开报告。
- 未修改两篇稿件；未改动原 91 条候选文件；未覆盖 pilot/stage2 任何输出（任务 1/2 新文件均落在 `runs/ma_stage2/` 的新文件名，stage2 的 raw_ledger.jsonl 未被追加——修复重标注使用独立账本 `fix_reannotation.raw_ledger.jsonl`）。
- sealed 纪律：冻结哈希先于一切标注调用；首次 CRLF 哈希不匹配被拦截后重新冻结，期间零调用；audit 答案/证据字段未进入 packet，未向任何模型展示。
- 失败/分歧记录全保留；无内容性重试（本批零技术重试需求）；temperature=0、max_tokens=1024、直连。
- API key：对 `annotation_pilot_20260807/` 全部 82 个产出文件程序化扫描，结果 NONE。
- served model id：A=`deepseek-v4-flash`（豁免别名）、B=`gemini-2.5-flash`、C=`gpt-5.4`，全部一致，无门禁触发。
- 预算：172 / 550（修复重标注 9 + sealed 冒烟 6 + sealed 全量 157，含全部尝试）。

## 5. 产出文件清单（本批新增）

```
annotation_pilot_20260807/
├── build_sealed_packet.py          # sealed 选集+冻结脚本
├── fix_candidates_v2.py            # 3 条修复生成+沙箱验证
├── column_check.py                 # 确定性列校验
├── STAGE3_REPORT.md                # 本报告
├── runs/ma_stage2/
│   ├── candidate_fixes_v2.jsonl                # 3 条 v2 修复（原文件未动）
│   ├── fix_reannotation.jsonl                  # 修复版 A/B/C 重标注结论
│   ├── fix_reannotation.raw_ledger.jsonl       # 独立账本（9 次调用）
│   ├── fix_reannotation.execution_facts.jsonl
│   └── column_check_report.json                # 121 条列校验 + 按族捕获率
└── runs/c2ges_stage3/
    ├── sealed_packet.jsonl         # 冻结 packet（sha256 36ab3b8f…）
    ├── sealed_manifest.json        # 逐文档哈希 + 无泄漏声明 + custodian
    ├── sample_manifest.json        # 75 题清单
    ├── raw_ledger.jsonl            # 157 次调用（含冒烟 6）
    ├── labels_A.jsonl / labels_B.jsonl
    ├── adjudicated.jsonl           # 13 条裁决
    ├── final_labels.jsonl          # 75 条终态（18 agreement / 44 tier1 / 13 adjudication）
    └── stats.json
```

---

# 第二批：MA-SQLGrid sealed set 生成、冻结与全量标注（2026-08-07）

协议：`MA_SEALED_SET_PROTOCOL_v1.json`（SHA-256 `fc422fef…2a4e`，运行前程序化校验通过）。授权同 STAGE3_AUTHORIZATION_20260807.json（550 上限，与第一批连续计数）。

## 总结论（第二批）

| 事项 | 结果 |
|---|---|
| sealed 题库 | **85 条冻结**（45 RTS + 40 SimBench，17 个全新模板族 RS01–09 / SS01–08，每族 5 实例；2 个候选实例因零计数答案被按规则丢弃并记录） |
| 负样本 | 30 条（15+15），五族分布 10/3/8/2/7，全部可执行且结果集与原 SQL 不同 |
| 全量标注 115 条 | 完成：一致率 0.878、κ=0.668、裁决 17 条（0.148）、**0 unresolved、0 格式失败** |
| 负样本检出率 | **总体 0.933（28/30）**；wrong_column 0.75（6/8），其余四族全部 1.00 |
| 列校验联合覆盖 | **30/30 = 1.000**（列校验捕获 wrong_column 8/8，与标注器互补） |
| 预算 | **427 / 550**（本批 255：sealed 标注 230 A/B + 17 裁决 + 8 次 B 技术重试） |

## 1. sealed 题库生成与冻结

- 新族设计覆盖 dev 未用表/操作：RTS 侧 reserve_requirements_da 峰值/均值、dispatch_da 时间窗聚合与 committed 计数、branches 额定值、generator_costs 启动成本排名、load_timeseries_da 区域峰值、renewable_availability_da 可用率；SimBench 侧 lines 长度/载流/负载率、transformers 容量、loads×voltage_level 聚合、switches 状态、buses 电压等级。
- 参数全部来自只读 DISTINCT/范围探测（fuel、reserve_product、region、电压等级、额定值范围等），保证过滤有匹配行；dispatch_da 仅覆盖 2020-07-05..18，相关模板只用 7 月日期。
- 验证门槛：可执行 + 结果非空 + 非全 NULL + COUNT>0 + SQL 去重。2 条丢弃（OLTC 变压器计数=0、电压等级 3 负荷计数=0），已补 2 条有效实例；丢弃与补入全部记入 `sealed_manifest.json` 的 generation_log。
- 冻结：`runs/ma_stage3/sealed_questions.jsonl`（字节写入，规避 CRLF 坑）sha256 `5d1ed4ea…5dc3` + `sealed_manifest.json`（逐条哈希、custodian、无泄漏声明）；标注运行器在每次启动时强制重校验该哈希。
- 每条含 answer_shape（columns/column_count，来自实际执行）、difficulty、split=sealed_test、human_reviewed=false。

## 2. 全量标注结果（115 = 85 原始 + 30 盲测负样本，盲化 id MA3_001–115）

| 指标 | sealed (n=115) | dev 91+30 (n=121) |
|---|---|---|
| semantically_correct 一致率 | 0.878 | 0.926 |
| Cohen's kappa | 0.668 | 0.764 |
| 裁决条目数（率） | 17（0.148） | 13（0.107） |
| 弃权 / 格式失败 / unresolved | 0 / 0 / 0 | 0 / 0 / 0（补跑后） |
| 负样本检出率 | **0.933** | 0.733 |
| wrong_column 族检出率 | 0.75（6/8） | 0.30（3/10） |
| 其它四族检出率 | 全部 1.00 | 0.75–1.00 |
| 列校验联合覆盖 | **1.000（30/30）** | 0.967（29/30） |

- 85 条 sealed 原始中 2 条判 false（RTS_SEALED_033/043，均 semantic_mismatch）：两者都是 RS02 族——问题文本写了"each **spinning** reserve product"而 SQL 未加 spinning 过滤（该表恰好只含 spinning 产品，结果实际正确）。与阶段 2 的 RTS_AUTO_047 同源：**问题措辞与 SQL 的"显式过滤"严格性不一致**。教训已明确：生成模板时问题中的限定词必须在 SQL 中有对应谓词。这 2 条在人工复核前不进入任何 benchmark 声明。
- 漏检的 2 条负样本（MA3_034、MA3_104）均为 wrong_column 且源问题出自 SimBench（SELECT 列偷换后列名仍"看起来合理"），与 dev 集观察一致。
- Token/延迟（sealed）：A 115 次（入 114,444 / 出 19,305，均 1.70s）；B 123 次（入 126,670 / 出 23,830，均 3.20s，8 次技术重试均成功）；C 17 次（入 23,732 / 出 2,913，均 4.79s，零失败）。

## 3. 合规声明（第二批）

- 先冻结后标注：sealed packet 哈希由运行器在标注前强制校验（C2GES 与 MA sealed 均如此）；负样本生成在冻结之后、标注之前。
- silver labels 命名；未改稿件；未覆盖旧目录（`runs/ma_stage3/` 全部为新文件）。
- 失败/丢弃记录保留（题库 generation_log、负样本 generation_log、B 的 8 次重试尝试均入账）。
- 无内容性重试；temperature=0；直连；served id 全部合规（A=deepseek-v4-flash 豁免别名、B=gemini-2.5-flash、C=gpt-5.4）。
- API key：对全部 95 个产出文件程序化扫描，结果 NONE。
- 预算 427/550 = c2ges sealed 163 + 修复重标注 9 + ma sealed 255（账本精确计数）。

## 4. 产出文件清单（第二批新增）

```
runs/ma_stage3/
├── sealed_questions.jsonl          # 85 条冻结题库（sha256 5d1ed4ea…）
├── sealed_manifest.json            # 逐条哈希 + 生成日志 + 无泄漏声明
├── negative_controls_manifest.json # 30 条负样本 + 生成日志
├── sample_manifest.json            # 115 条盲化映射（MA3_001–115）
├── execution_facts.jsonl           # 沙箱执行事实（115/115 可执行）
├── raw_ledger.jsonl                # 255 次调用（含冒烟 4）
├── labels_A.jsonl / labels_B.jsonl
├── adjudicated.jsonl               # 17 条裁决
├── final_labels.jsonl              # 115 条终态（98 agreement / 17 adjudication）
├── column_check_report.json        # sealed 列校验（wrong_column 8/8）
└── stats.json
```
